#!/usr/bin/env python3
# Refactored by copilot-placeholder
# Refactored by copilot-placeholder
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Engine lifecycle management module for coordinating engine states and request processing.
"""

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project

from __future__ import annotations

import asyncio
import enum
import logging
import signal
import threading
import time
from dataclasses import dataclass
from typing import Any, Callable, Optional, Set

from .request_lifecycle import (FinishReason, Request, RequestQueue,
                                RequestTracker)

logger = logging.getLogger(__name__)


# ==============================================================================
# Engine State Enum
# ==============================================================================
class EngineState(enum.Enum):
    """Enumeration of possible engine lifecycle states."""

    INITIALIZING = "initializing"  # Engine is starting up
    READY = "ready"  # Ready to accept requests
    RUNNING = "running"  # Processing requests
    SLEEPING = "sleeping"  # Power-saving mode
    SHUTTING_DOWN = "shutting_down"  # Graceful shutdown in progress
    DEAD = "dead"  # Engine is terminated

    def __str__(self) -> str:
        return self.value

    def is_active(self) -> bool:
        """Check if the engine is in an active state."""
        return self in (EngineState.READY, EngineState.RUNNING)

    def can_accept_requests(self) -> bool:
        """Check if the engine can accept new requests."""
        return self in (EngineState.READY, EngineState.RUNNING)

    def is_terminal(self) -> bool:
        """Check if the engine is in a terminal state."""
        return self == EngineState.DEAD


# Valid state transitions
_ENGINE_TRANSITIONS: dict[EngineState, Set[EngineState]] = {
    EngineState.INITIALIZING: {EngineState.READY, EngineState.DEAD},
    EngineState.READY: {
        EngineState.RUNNING,
        EngineState.SLEEPING,
        EngineState.SHUTTING_DOWN,
    },
    EngineState.RUNNING: {
        EngineState.READY,
        EngineState.SLEEPING,
        EngineState.SHUTTING_DOWN,
    },
    EngineState.SLEEPING: {
        EngineState.READY,
        EngineState.RUNNING,
        EngineState.SHUTTING_DOWN,
    },
    EngineState.SHUTTING_DOWN: {EngineState.DEAD},
    EngineState.DEAD: set(),  # Terminal state
}


# ==============================================================================
# Engine Configuration
# ==============================================================================


@dataclass
class EngineConfig:
    """
    Configuration for the engine lifecycle manager.

    Attributes:
        max_requests: Maximum concurrent requests
        max_tokens_per_step: Maximum tokens to process per step
        step_timeout: Timeout for each step in seconds
        shutdown_timeout: Timeout for graceful shutdown
        drain_requests_on_shutdown: Whether to complete pending requests
        enable_sleep_mode: Whether sleep mode is enabled
        sleep_level: Default sleep level (1-3)
        health_check_interval: Interval for health checks
    """

    max_requests: int = 256
    max_tokens_per_step: int = 8192
    step_timeout: float = 30.0
    shutdown_timeout: float = 60.0
    drain_requests_on_shutdown: bool = True
    enable_sleep_mode: bool = True
    sleep_level: int = 1
    health_check_interval: float = 5.0

    # Callback configuration
    on_state_change: Optional[Callable[[EngineState, EngineState], None]] = None
    on_request_complete: Optional[Callable[[Request], None]] = None
    on_error: Optional[Callable[[Exception], None]] = None


# ==============================================================================
# Engine Lifecycle Manager
# ==============================================================================


class EngineLifecycleManager:  # pylint: disable=too-many-public-methods
    """
    Manages the lifecycle of an inference engine.

    This class handles state transitions, request management, and
    graceful shutdown following vLLM's EngineCore patterns.

    Attributes:
        config: Engine configuration
        state: Current engine state
        request_queue: Queue for managing requests
        tracker: Request lifecycle tracker
    """

    def __init__(
        self,
        config: Optional[EngineConfig] = None,
        request_queue: Optional[RequestQueue] = None,
        sleep_fn: Callable[[float], None] | None = None,
    ) -> None:
        """
        Initialize the engine lifecycle manager.

        Args:
            config: Engine configuration
            request_queue: Optional pre-configured request queue
        """
        self.config = config or EngineConfig()
        self.request_queue = request_queue or RequestQueue()
        self.tracker = RequestTracker()

        self._state = EngineState.INITIALIZING
        self._lock = threading.RLock()
        self._shutdown_event = threading.Event()
        self._drain_complete = threading.Event()

        # Sleep function; default to a threading.Event().wait-based implementation
        if sleep_fn is None:
            def _wait(t: float) -> None:
                threading.Event().wait(t)

            self._sleep_fn = _wait
        else:
            self._sleep_fn = sleep_fn

        # Sleep mode state
        self._sleep_level = 0
        self._wake_tags: Optional[list[str]] = None

        # Step counting
        self._step_count = 0
        self._last_step_time: Optional[float] = None

        # Error tracking
        self._last_error: Optional[Exception] = None
        self._error_count = 0

    # -------------------------------------------------------------------------
    # State Properties
    # -------------------------------------------------------------------------

    @property
    def state(self) -> EngineState:
        """Get the current engine state."""
        return self._state

    def is_sleeping(self) -> bool:
        """Check if the engine is in sleep mode."""
        return self._state == EngineState.SLEEPING

    def is_ready(self) -> bool:
        """Check if the engine is ready."""
        return self._state == EngineState.READY

    def is_running(self) -> bool:
        """Check if the engine is running."""
        return self._state == EngineState.RUNNING

    def is_shutting_down(self) -> bool:
        """Check if the engine is shutting down."""
        return self._state == EngineState.SHUTTING_DOWN

    def is_dead(self) -> bool:
        """Check if the engine is dead."""
        return self._state == EngineState.DEAD

    def can_accept_requests(self) -> bool:
        """Check if the engine can accept new requests."""
        return self._state.can_accept_requests()

    # -------------------------------------------------------------------------
    # State Transitions
    # -------------------------------------------------------------------------

    def _transition_to(self, new_state: EngineState) -> bool:
        """
        Transition to a new state with validation.

        Returns:
            True if the transition was successful
        """
        with self._lock:
            valid_targets = _ENGINE_TRANSITIONS.get(self._state, set())
            if new_state not in valid_targets:
                logger.warning(
                    "Invalid state transition: %s -> %s",
                    self._state,
                    new_state,
                )
                return False

            old_state = self._state
            self._state = new_state

            logger.info("Engine state: %s -> %s", old_state, new_state)

            # Call state change callback
            if self.config.on_state_change:
                try:
                    self.config.on_state_change(old_state, new_state)
                except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                    logger.exception("Error in state change callback: %s", e)

            return True

    # -------------------------------------------------------------------------
    # Lifecycle Methods
    # -------------------------------------------------------------------------

    def start(self) -> bool:
        """
        Start the engine (transition from INITIALIZING to READY).

        Returns:
            True if the engine started successfully
        """
        if self._state != EngineState.INITIALIZING:
            logger.warning("Cannot start engine from state %s", self._state)
            return False

        return self._transition_to(EngineState.READY)

    def shutdown(self, timeout: Optional[float] = None) -> bool:
        """
        Shutdown the engine gracefully.

        Args:
            timeout: Timeout for shutdown (uses config default if None)

        Returns:
            True if shutdown completed successfully
        """
        timeout = timeout or self.config.shutdown_timeout

        self._signal_shutdown()
        self._transition_to(EngineState.SHUTTING_DOWN)

        if self.config.drain_requests_on_shutdown:
            self._drain_pending_requests(timeout)

        return self._transition_to(EngineState.DEAD)

    def _signal_shutdown(self) -> None:
        """Signal shutdown event to notify all waiters."""
        self._shutdown_event.set()

    def _abort_all_pending_requests(self) -> None:
        """Abort all waiting and running requests in the queue."""
        for request in self.request_queue.get_waiting_requests():
            self.request_queue.abort_request(request.request_id)
        for request in self.request_queue.get_running_requests():
            self.request_queue.abort_request(request.request_id)

    def _drain_pending_requests(self, timeout: float) -> None:
        """Drain pending requests before shutdown."""
        start = time.time()
        while time.time() - start < timeout:
            waiting = self.request_queue.get_waiting_requests()
            running = self.request_queue.get_running_requests()
            if not waiting and not running:
                break
            self._sleep_briefly()
        # After timeout or when drained, abort any remaining requests
        self._abort_all_pending_requests()

    def _sleep_briefly(self) -> None:
        # Helper to sleep briefly, compatible with sync context
        try:
            if asyncio.get_event_loop().is_running():
                # If in async context, schedule async sleep
                asyncio.create_task(self._async_sleep())
            else:
                # Use configured sleep function to avoid blocking time.sleep in hot paths
                self._sleep_fn(0.1)
        except (RuntimeError, AttributeError):
            # Fallback to configured sleep function
            self._sleep_fn(0.1)

    async def _async_sleep(self) -> bool:
        await asyncio.sleep(0.1)

        self._drain_complete.set()
        return self._transition_to(EngineState.DEAD)

    def sleep(self, level: int = 1) -> bool:
        """
        Put the engine to sleep.

        Args:
            level: Sleep level (1 = light, 2 = medium, 3 = deep)

        Returns:
            True if the engine went to sleep
        """
        if not self.config.enable_sleep_mode:
            logger.warning("Sleep mode is not enabled")
            return False

        if not self._state.is_active():
            logger.warning("Cannot sleep from state %s", self._state)
            return False

        self._sleep_level = min(max(level, 1), 3)
        logger.info("Engine sleeping at level %d", self._sleep_level)
        return self._transition_to(EngineState.SLEEPING)

    def wake_up(self, tags: Optional[list[str]] = None) -> bool:
        """
        Wake up the engine from sleep.

        Args:
            tags: Optional tags to filter wake-up

        Returns:
            True if the engine woke up
        """
        if self._state != EngineState.SLEEPING:
            return True  # Already awake

        self._wake_tags = tags
        self._sleep_level = 0
        logger.info("Engine waking up (tags: %s)", tags)
        return self._transition_to(EngineState.READY)

    # -------------------------------------------------------------------------
    # Request Management
    # -------------------------------------------------------------------------

    def add_request(self, request: Request) -> bool:
        """
        Add a request to the engine.

        Args:
            request: The request to add

        Returns:
            True if the request was accepted
        """
        if not self.can_accept_requests():
            logger.warning(
                "Cannot accept request in state %s",
                self._state,
            )
            return False

        # Check capacity
        if self.request_queue.get_num_unfinished() >= self.config.max_requests:
            logger.warning("Engine at capacity (%d requests)", self.config.max_requests)
            return False

        self.request_queue.add_request(request)
        return True

    def abort_requests(self, request_ids: list[str]) -> list[Request]:
        """
        Abort one or more requests.

        Args:
            request_ids: IDs of requests to abort

        Returns:
            List of aborted requests
        """
        aborted = self.request_queue.abort_requests(request_ids)
        for request in aborted:
            self.tracker.record_request(request)
        return aborted

    def get_num_unfinished_requests(self) -> int:
        """Get the number of unfinished requests."""
        return self.request_queue.get_num_unfinished()

    def has_unfinished_requests(self) -> bool:
        """Check if there are unfinished requests."""
        return self.request_queue.has_unfinished_requests()

    # -------------------------------------------------------------------------
    # Step Execution
    # -------------------------------------------------------------------------

    def step(self) -> list[Request]:
        """
        Execute a single engine step.

        This schedules waiting requests, processes them, and returns
        any requests that completed during this step.

        Returns:
            List of requests that finished during this step
        """
        if self._shutdown_event.is_set():
            return []

        self._transition_to_running_if_needed()

        if self._state != EngineState.RUNNING:
            return []

        finished = []

        try:
            self._schedule_waiting_requests()
            self._record_step_timing()
            finished = self._process_running_requests()
            self._transition_to_ready_if_idle()

        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            self._handle_step_error(e)

        return finished

    def _transition_to_running_if_needed(self) -> None:
        """Transition to running state if there are unfinished requests."""
        if self._state == EngineState.READY and self.request_queue.has_unfinished_requests():
            self._transition_to(EngineState.RUNNING)

    def _schedule_waiting_requests(self) -> None:
        """Schedule waiting requests into available slots."""
        available_slots = self.config.max_requests - self.request_queue.get_num_running()
        if available_slots > 0:
            self.request_queue.schedule_next(available_slots)

    def _record_step_timing(self) -> None:
        """Record timing information for this step."""
        self._step_count += 1
        self._last_step_time = time.time()

    def _process_running_requests(self) -> list[Request]:
        """Process all currently running requests and return finished ones."""
        finished = []
        for request in self.request_queue.get_running_requests():
            if request.should_stop():
                finished_request = self._finish_request(request)
                finished.append(finished_request)
        return finished

    def _finish_request(self, request: Request) -> Request:
        """Finish a request and handle completion callbacks."""
        reason = self._determine_finish_reason(request)

        self.request_queue.finish_request(request.request_id, reason)
        self.tracker.record_request(request)

        if self.config.on_request_complete:
            try:
                self.config.on_request_complete(request)
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                logger.exception("Error in completion callback: %s", e)

        return request

    def _determine_finish_reason(self, request: Request) -> FinishReason:
        """Determine why a request finished."""
        reason = FinishReason.LENGTH
        if request.output_token_ids and request.eos_token_id:
            if request.output_token_ids[-1] == request.eos_token_id:
                reason = FinishReason.STOP
        return reason

    def _transition_to_ready_if_idle(self) -> None:
        """Transition back to ready state if no work remains."""
        if not self.request_queue.has_unfinished_requests():
            self._transition_to(EngineState.READY)

    def _handle_step_error(self, error: Exception) -> None:
        """Handle errors that occur during step execution."""
        self._last_error = error
        self._error_count += 1
        logger.exception("Error during step: %s", error)
        if self.config.on_error:
            self.config.on_error(error)

    async def step_async(self) -> list[Request]:
        """Async version of step()."""
        return await asyncio.get_event_loop().run_in_executor(None, self.step)

    # -------------------------------------------------------------------------
    # Health & Monitoring
    # -------------------------------------------------------------------------

    def health_check(self) -> dict[str, Any]:
        """
        Perform a health check.

        Returns:
            Dictionary with health status
        """
        return {
            "healthy": not self._state.is_terminal(),
            "state": str(self._state),
            "num_waiting": self.request_queue.get_num_waiting(),
            "num_running": self.request_queue.get_num_running(),
            "step_count": self._step_count,
            "error_count": self._error_count,
            "last_error": str(self._last_error) if self._last_error else None,
            "last_step_time": self._last_step_time,
        }

    def is_healthy(self) -> bool:
        """Check if the engine is healthy."""
        return not self._state.is_terminal() and self._error_count == 0

    def get_stats(self) -> dict[str, Any]:
        """Get engine statistics."""
        return {
            "state": str(self._state),
            "step_count": self._step_count,
            "error_count": self._error_count,
            "sleep_level": self._sleep_level,
            **self.tracker.as_dict(),
        }

    # -------------------------------------------------------------------------
    # Signal Handling
    # -------------------------------------------------------------------------

    def setup_signal_handlers(self) -> None:
        """Set up signal handlers for graceful shutdown."""

        def signal_handler(signum: int, _frame: Any) -> None:
            logger.info("Received signal %s, initiating shutdown", signum)
            self.shutdown()

        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)

    # -------------------------------------------------------------------------
    # Context Manager
    # -------------------------------------------------------------------------

    def __enter__(self) -> "EngineLifecycleManager":
        """Enter context manager."""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit context manager with cleanup."""
        self.shutdown()
