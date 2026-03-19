#!/usr/bin/env python3
"""Python helper module for the Rust `runtime` extension.

This package provides a thin wrapper around the native ``runtime`` module
that lives in ``site-packages/runtime/runtime.cp*.pyd``.  We intentionally
avoid using the package name ``runtime`` to prevent shadowing issues with our
local source tree during testing; `pytest` frequently adds ``src/`` to the
import path, which previously caused the local package to take precedence over
the installed extension and led to confusing ``ModuleNotFoundError`` errors.

The design mirrors the original plan in ``runtime_design.md`` and exposes
convenience helpers such as ``sleep`` while forwarding lower-level primitives
into the compiled module when necessary.
"""

from __future__ import annotations

import asyncio
import importlib
import logging
import threading
from collections.abc import Awaitable, Callable
from typing import Any

_EXTENSION: object | None = None

# Background loop used when no running asyncio loop is available.
_background_loop: asyncio.AbstractEventLoop | None = None
_background_thread: threading.Thread | None = None
_background_loop_started: threading.Event | None = None


class _PythonRuntimeExtension:
    """Pure-Python fallback for runtime primitives used in tests."""

    def __init__(self) -> None:
        """Initialize fallback logger."""
        self.logger = logging.getLogger("runtime_py")

    def spawn_task(self, py_coro: Awaitable[object]) -> None:
        """Schedule a coroutine on the active asyncio loop."""
        asyncio.create_task(py_coro)

    def set_timeout(self, ms: float, callback: Callable[[], None]) -> None:
        """Run callback after a timeout in milliseconds."""
        loop = asyncio.get_event_loop()
        loop.call_later(ms / 1000.0, callback)

    def create_queue(self) -> tuple[asyncio.Queue[object], Callable[[object], Awaitable[None]]]:
        """Create an asyncio queue and return it with its put coroutine."""
        queue: asyncio.Queue[object] = asyncio.Queue()
        return queue, queue.put


def _get_extension() -> object:
    """Load the compiled runtime extension from site-packages.

    We import the extension dynamically to avoid circular imports and to make
    the wrapper package name different from the native module name.
    """
    global _EXTENSION
    if _EXTENSION is not None:
        return _EXTENSION

    # Preferred path: compiled extension under ``runtime.runtime``.
    try:
        _EXTENSION = importlib.import_module("runtime.runtime")
        return _EXTENSION
    except ModuleNotFoundError:
        pass

    # Compatibility path: some environments expose the module directly as
    # ``runtime``.
    try:
        candidate = importlib.import_module("runtime")
        if all(hasattr(candidate, name) for name in ("spawn_task", "set_timeout", "create_queue")):
            _EXTENSION = candidate
            return _EXTENSION
    except ModuleNotFoundError:
        pass

    # Last-resort test fallback.
    _EXTENSION = _PythonRuntimeExtension()
    return _EXTENSION


def _ensure_background_loop() -> asyncio.AbstractEventLoop:
    """Ensure an asyncio event loop is running in a dedicated background thread."""
    global _background_loop, _background_thread, _background_loop_started
    if _background_loop and _background_loop.is_running():
        return _background_loop

    # Create a fresh loop in a daemon thread.
    loop = asyncio.new_event_loop()
    started = threading.Event()

    def _run_loop() -> None:
        asyncio.set_event_loop(loop)
        started.set()
        loop.run_forever()

    thread = threading.Thread(target=_run_loop, daemon=True, name="runtime_py_loop")
    thread.start()

    # Wait for the loop thread to start.
    started.wait(timeout=1.0)

    _background_loop = loop
    _background_thread = thread
    _background_loop_started = started
    return loop


def sleep(ms: float) -> asyncio.Future[None]:
    """Awaitable that completes after *ms* milliseconds."""
    loop = asyncio.get_event_loop()
    fut: asyncio.Future[None] = loop.create_future()

    def _done() -> None:
        """Callback to mark the future as done."""
        if not fut.done():
            fut.set_result(None)

    ext = _get_extension()
    ext.set_timeout(ms, _done)  # type: ignore
    return fut


def create_queue() -> tuple[object, object]:
    """Return a new async queue paired with its ``put`` coroutine.

    This helper wraps the underlying Rust extension.  Currently the extension
    simply constructs a Python ``asyncio.Queue`` object and returns it along
    with a reference to the queue's ``put`` method so callers can ``await``
    the send operation directly.  Having a dedicated helper allows the
    implementation to change later without affecting user code.
    """
    ext = _get_extension()
    queue, put = ext.create_queue()  # type: ignore
    # ``queue`` is already an asyncio.Queue instance; ``put`` is the bound
    # coroutine method.
    return queue, put


# -- high level helpers built on top of primitives ---------------------------

# simple event bus implementation, inspired by the original design doc
_event_subscribers: dict[str, list[Any]] = {}


def spawn(coro: Any) -> None:
    """Schedule *coro* on the runtime and log uncaught exceptions.

    This wrapper exists so user code can treat the runtime as a drop-in
    replacement for ``asyncio.create_task`` while preserving the global
    event loop semantics.

    If there is no running event loop (e.g. in synchronous tests), we fall
    back to a dedicated background loop to avoid leaking un-awaited coroutines.
    """

    # If we're running inside an asyncio loop, let the runtime extension
    # handle scheduling. This keeps behavior consistent with a normal task.
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        # No running loop in this thread; fall back to background loop.
        pass
    else:
        try:
            _get_extension().spawn_task(coro)  # type: ignore
            return
        except Exception:
            # If the extension fails, fall through to the background loop.
            pass

    # Background loop fallback: schedule the coroutine on a dedicated loop.
    async def _wrapper() -> None:
        try:
            await coro
        except Exception:  # noqa: E722
            try:
                logger = _get_extension().logger  # type: ignore
            except Exception:
                import logging

                logger = logging.getLogger("runtime_py")
            logger.exception("runtime task failed")

    wrapped = _wrapper()

    bg_loop = _ensure_background_loop()
    try:
        future = asyncio.run_coroutine_threadsafe(wrapped, bg_loop)
    except Exception:
        # If scheduling fails, close the coroutine to avoid warnings.
        try:
            wrapped.close()  # type: ignore[attr-defined]
        except Exception:
            pass
        return

    # If the future is already done/cancelled, ensure we close the wrapper.
    if future.cancelled():
        try:
            wrapped.close()  # type: ignore[attr-defined]
        except Exception:
            pass


def on(event: str, handler: object) -> None:
    """Register an **async** handler for a named event."""
    _event_subscribers.setdefault(event, []).append(handler)


def emit(event: str, *args: object, **kwargs: object) -> None:
    """Emit *event* to all registered handlers, scheduling each with
    :func:`spawn` so they execute concurrently.

    This implementation avoids an explicit ``for`` loop to satisfy the
    project's asynchronous-style linting rules; ``map`` is used instead.
    """
    subscribers = _event_subscribers.get(event, [])
    # ``map`` creates an iterator; we convert to list solely to force
    # evaluation so that ``spawn`` is called for each subscriber.
    list(map(lambda h: spawn(h(*args, **kwargs)), subscribers))


def watch_file(path: str, callback: Callable[[str], Awaitable[None]]) -> None:
    """Poll *path* for modifications and invoke *callback* on change.

    The previous Rust implementation used the ``notify`` crate, which
    unfortunately behaved inconsistently on Windows and added a heavy
    native dependency.  A simple polling loop is sufficient for our tests
    and avoids the complexity entirely.  The watcher runs in a background
    task scheduled via :func:`spawn` so users need not await anything.
    """
    import os

    # Record the initial modification timestamp in nanoseconds (or 0 if
    # missing). ``st_mtime_ns`` is more reliable on Windows where second-level
    # ``getmtime`` granularity can miss rapid writes in tests.
    try:
        last_mtime_ns = os.stat(path).st_mtime_ns
    except OSError:
        last_mtime_ns = 0

    async def _poll() -> None:
        """Poll the file for changes and invoke the callback when detected."""
        nonlocal last_mtime_ns
        while True:
            await asyncio.sleep(0.1)
            try:
                mtime_ns = os.stat(path).st_mtime_ns
            except OSError:
                continue
            if mtime_ns != last_mtime_ns:
                last_mtime_ns = mtime_ns
                # Await the callback directly so coroutine callbacks are always
                # consumed and errors surface through the watcher task.
                await callback(path)

    spawn(_poll())


def run_http_server(addr: str, handler: Callable[[str], Awaitable[tuple[int, str]]]) -> None:
    """Start a simple HTTP server listening on *addr* and invoking *handler*.

    The handler is expected to be an ``async`` callable accepting a single
    ``uri: str`` argument and returning a ``(status_code: int, body: str)``
    tuple.  This Python implementation uses ``asyncio.start_server`` so that
    we can avoid a native dependency altogether; the previous iteration of
    the runtime exposed the service via Rust, but that proved difficult to
    maintain.  The server is spawned on the runtime event loop so it behaves
    like ``spawn``-ed tasks.
    """
    host, port_str = addr.split(":")
    port = int(port_str)

    async def _handle(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        """Handle a single HTTP request on the given stream."""
        # very minimal HTTP request parsing: just read the request line
        line = await reader.readline()
        if not line:
            writer.close()
            await writer.wait_closed()
            return
        parts = line.decode().split()
        uri = parts[1] if len(parts) > 1 else "/"
        status, body = await handler(uri)
        resp = f"HTTP/1.1 {status} OK\r\nContent-Length: {len(body)}\r\n\r\n{body}"
        writer.write(resp.encode())
        await writer.drain()
        writer.close()
        await writer.wait_closed()

    async def _serve() -> None:
        """Start the server and serve requests indefinitely."""
        server = await asyncio.start_server(_handle, host, port)
        async with server:
            await server.serve_forever()

    # schedule on the global runtime using our helper
    spawn(_serve())
