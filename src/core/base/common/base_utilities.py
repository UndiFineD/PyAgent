#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
"""Utilities used across base modules.

Small, well-typed helper functions and decorators used by agents and tools.
Focus on low-risk, testable behaviors: replacement helpers, logging setup,
and tool wrappers that record interactions to the fleet recorder when present.
"""

import os

from pathlib import Path
import re
import logging
import inspect
import argparse
import sys
import json
import time
from typing import Union, Callable, Any
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.common.file_system_core import FileSystemCore
_fs = FileSystemCore()


def _bulk_replace_python_fallback(
    file_paths: list[Union[str, Path]], old_pattern: str, new_string: str, use_regex: bool
) -> dict[str, bool]:
    results = {}
    for path_in in file_paths:
        path = Path(path_in)
        if not _fs.exists(path):
            results[str(path)] = False
            continue
        content = _fs.read_text(path)
        if use_regex:
            new_content, count = re.subn(old_pattern, new_string, content)
            changed = count > 0
        else:
            changed = old_pattern in content
            new_content = content.replace(old_pattern, new_string)
        if changed:
            _fs.atomic_write(path, new_content)
            results[str(path)] = True
        else:
            results[str(path)] = False
    return results


def bulk_replace_files(
    file_paths: list[Union[str, Path]],
    old_pattern: str,
    new_string: str,
    use_regex: bool = False,
) -> dict[str, bool]:
    """
    Performs a bulk string or regex replacement across multiple files.
    Returns a mapping of file path to boolean (True if file was modified).
    Phase 318: Rust-Native Parallel Engine.
    """
    try:
        # pylint: disable=import-outside-toplevel
        from ...rust_bridge import RustBridge
    except (ImportError, ValueError):
        # pylint: disable=import-outside-toplevel
        from src.core.rust_bridge import RustBridge

    if RustBridge.is_rust_active():
        str_paths = [str(p) for p in file_paths]
        replacements = {old_pattern: new_string}
        return RustBridge.bulk_replace_files(str_paths, replacements)

    return _bulk_replace_python_fallback(file_paths, old_pattern, new_string, use_regex)


def bulk_replace(
    file_paths: list[str | Path],
    old_pattern: str,
    new_string: str,
    use_regex: bool = False,
) -> dict[str, bool]:
    """
    Performs a bulk string or regex replacement across multiple files.
    Returns a mapping of file path to boolean (True if file was modified).
    Phase 318: Rust-Native Parallel Engine.
    """
    # 1. High-Speed Rust Acceleration (Phase 318)
    try:
        # pylint: disable=import-outside-toplevel
        from ...rust_bridge import RustBridge
    except (ImportError, ValueError):
        # pylint: disable=import-outside-toplevel
        from src.core.rust_bridge import RustBridge

    if RustBridge.is_rust_active():
        str_paths = [str(p) for p in file_paths]
        replacements = {old_pattern: new_string}
        return RustBridge.bulk_replace_files(str_paths, replacements)

    # Use the existing python fallback implementation to avoid duplication
    return _bulk_replace_python_fallback(file_paths, old_pattern, new_string, use_regex)


def setup_logging(verbosity_arg: int = 0) -> None:
    """Configure logging based on verbosity level."""
    level = logging.INFO
    if verbosity_arg >= 2:
        level = logging.DEBUG
    elif verbosity_arg == 1:
        level = logging.INFO

    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        force=True,
    )


def _record_tool_execution(self: Any, func_name: str, args: tuple, kwargs: dict, result: Any) -> None:
    """Record a tool execution to the fleet recorder if available.

    Separated into a helper to keep the decorator logic small and testable.
    Critical exceptions (KeyboardInterrupt, SystemExit) are re-raised.
    """
    try:
        shard_result = str(result)
        if len(shard_result) > 2000:
            shard_result = shard_result[:2000] + "... [TRUNCATED]"

        prompt_trace = f"TOOL_EXECUTION: {func_name}\nArgs: {args}\nKwargs: {kwargs}"

        self.fleet.recorder.record_interaction(
            provider="agent_tool",
            model=self.__class__.__name__,
            prompt=prompt_trace,
            result=shard_result,
            meta={
                "tool": func_name,
                "agent": self.__class__.__name__,
                "timestamp_ms": int(time.time() * 1000),
            },
        )
    except (RuntimeError, OSError, AttributeError, ValueError, TypeError) as e:
        # Re-raise critical signals and otherwise log for debugging.
        if isinstance(e, (KeyboardInterrupt, SystemExit)):
            raise
        logging.debug("_record_tool_execution failed: %s", e)


def as_tool(priority: int = 0, category: str | None = None) -> Callable:
    """Decorator to mark a method as a tool for the ToolRegistry.
    Automatically records tool interactions to the fleet context shards for autonomous learning.
    Can be used as @as_tool or @as_tool(priority=10).
    """
    # pylint: disable=import-outside-toplevel
    from functools import wraps

    def decorator(func: Callable) -> Callable:
        if inspect.iscoroutinefunction(func):

            @wraps(func)
            async def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
                # Phase 108: Enhanced Traceability
                logging.debug("Executing async tool %s on %s", func.__name__, self.__class__.__name__)

                result = await func(self, *args, **kwargs)

                # Autonomous Logic Harvesting:
                if hasattr(self, "fleet") and self.fleet and hasattr(self.fleet, "recorder"):
                    try:
                        _record_tool_execution(self, func.__name__, args, kwargs, result)
                    except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                        if isinstance(e, (KeyboardInterrupt, SystemExit)):
                            raise
                        logging.debug("Failed to record tool interaction: %s", e)

                return result
        else:

            @wraps(func)
            def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
                # Phase 108: Enhanced Traceability

                logging.debug("Executing tool %s on %s", func.__name__, self.__class__.__name__)

                result = func(self, *args, **kwargs)

                # Autonomous Logic Harvesting:
                if hasattr(self, "fleet") and self.fleet and hasattr(self.fleet, "recorder"):
                    try:
                        _record_tool_execution(self, func.__name__, args, kwargs, result)
                    except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                        if isinstance(e, (KeyboardInterrupt, SystemExit)):
                            raise
                        logging.debug("Failed to record tool interaction: %s", e)

                return result

        # pylint: disable=protected-access
        wrapper._is_tool = True
        wrapper._tool_priority = priority
        if category:
            wrapper._tool_category = category

        return wrapper

    # Support @as_tool without parentheses
    if callable(priority):
        f = priority
        priority = 0
        return decorator(f)

    return decorator


def create_main_function(agent_class: type[BaseAgent], description: str, context_help: str) -> Callable[[], None]:
    """Create a main function for an agent class."""

    def main() -> None:
        parser = argparse.ArgumentParser(description=description)
        parser.add_argument(
            "--describe-backends",
            action="store_true",
            help="Print which AI backends are available / configured and exit",
        )
        parser.add_argument(
            "--backend",
            choices=["auto", "copilot", "gh", "github-models"],
            default=None,
            help="Select backend (overrides DV_AGENT_BACKEND for this run only)",
        )
        parser.add_argument(
            "--strategy",
            choices=["direct", "cot", "reflexion"],
            default="direct",
            help="Select reasoning strategy (direct, cot, reflexion)",
        )
        parser.add_argument(
            "--verbose",
            "-v",
            action="count",
            default=0,
            help="Increase verbosity (can be used multiple times, e.g. -vv)",
        )
        parser.add_argument(
            "--no-cascade",
            action="store_true",
            help="Prevent this agent from launching other agents (internal use)",
        )
        parser.add_argument(
            "--json",
            action="store_true",
            help="Output result as JSON (useful for n8n/automation integration)",
        )
        parser.add_argument("--context", required=True, help=context_help)
        parser.add_argument("--prompt", required=True, help="Prompt for improving the content")
        parser.add_argument(
            "--delegate",
            help="Agent type to delegate a sub-task to (e.g., SearchAgent)",
        )
        args = parser.parse_args()
        setup_logging(args.verbose)

        if args.backend:
            os.environ["DV_AGENT_BACKEND"] = args.backend

        agent = agent_class(args.context)

        # If delegation is requested via CLI
        if args.delegate:
            logging.info("CLI Delegation: %s -> %s", agent_class.__name__, args.delegate)
            result = agent.delegate_to(args.delegate, args.prompt)
            if args.json:
                sys.stdout.write(json.dumps({"delegation_result": result}) + "\n")
            else:
                sys.stdout.write(f"Delegation Result:\n{result}\n")
            return

        # Normal execution
        # Honor parent/guard flag to avoid cascading agent invocations
        if getattr(args, "no_cascade", False) or os.environ.get("DV_AGENT_PARENT"):
            # pylint: disable=protected-access
            agent._no_cascade = True
            logging.info("No-cascade mode enabled for this agent (prevents spawning other agents)")

        # Set strategy based on argument (stub: always direct)
        # If you want to support other strategies, implement them here

        agent.read_previous_content()
        agent.improve_content(args.prompt)
        agent.update_file()
        diff = agent.get_diff()

        if args.json:
            result = {
                "agent": agent_class.__name__,
                "file_path": str(agent.file_path),
                "updated": bool(diff),
                "diff": diff,
                "content_length": len(agent.current_content),
            }
            sys.stdout.write(json.dumps(result, indent=2) + "\n")
        else:
            if diff:
                logging.info("%s updated:", agent_class.__name__.replace("Agent", "").lower())
                logging.info(diff)
            else:
                logging.info("No changes made to %s.", agent_class.__name__.replace("Agent", "").lower())

    return main
