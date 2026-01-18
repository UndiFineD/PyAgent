# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""
Engine lifecycle management for inference engines.

This module implements engine state management and lifecycle control,
inspired by vLLM's v1/engine/core.py architecture.

Key Components:
    - EngineState: Enum for engine states (INITIALIZING, READY, RUNNING, etc.)
    - EngineConfig: Configuration for engine lifecycle
    - EngineLifecycleManager: Manages engine state transitions

Example:
    >>> from src.infrastructure.engine import EngineLifecycleManager, EngineConfig
    >>> 
    >>> config = EngineConfig(max_requests=100)
    >>> manager = EngineLifecycleManager(config)
    >>> 
    >>> manager.start()  # INITIALIZING -> READY
    >>> manager.step()   # READY -> RUNNING -> READY
    >>> manager.shutdown()  # -> SHUTTING_DOWN -> DEAD
"""

from __future__ import annotations

import asyncio
import enum
import logging
import signal
import threading
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Set

from .RequestLifecycle import (
    FinishReason,
    Request,
    RequestQueue,
    RequestStatus,
    RequestTracker,
)

logger = logging.getLogger(__name__)


# ==============================================================================
# Engine State Enum
# ==============================================================================

class EngineState(enum.Enum):
    """
    State of the inference engine.

    State machine:
        INITIALIZING -> READY -> RUNNING <-> SLEEPING
                                    |
                              SHUTTING_DOWN -> DEAD
    """
    INITIALIZING = "initializing"   # Engine is starting up
    READY = "ready"                 # Ready to accept requests
    RUNNING = "running"             # Processing requests
    SLEEPING = "sleeping"           # Power-saving mode
    SHUTTING_DOWN = "shutting_down" # Graceful shutdown in progress
    DEAD = "dead"                   # Engine is terminated

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
_ENGINE_TRANSITIONS: Dict[EngineState, Set[EngineState]] = {
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

class EngineLifecycleManager:
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
    ):
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
        
        # Sleep mode state
        self._sleep_level = 0
        self._wake_tags: Optional[List[str]] = None
        
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
                except Exception as e:
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
        
        # Signal shutdown
        self._shutdown_event.set()
        
        # Transition to shutting down
        if not self._transition_to(EngineState.SHUTTING_DOWN):
            # Force transition if we're in a terminal state
            if not self._state.is_terminal():
                self._state = EngineState.SHUTTING_DOWN
        
        # Drain requests if configured
        if self.config.drain_requests_on_shutdown:
            start_time = time.time()
            while self.request_queue.has_unfinished_requests():
                if time.time() - start_time > timeout:
                    logger.warning(
                        "Shutdown timeout: %d requests still pending",
                        self.request_queue.get_num_unfinished(),
                    )
                    # Abort remaining requests
                    for request in self.request_queue.get_waiting_requests():
                        self.request_queue.abort_request(request.request_id)
                    for request in self.request_queue.get_running_requests():
                        self.request_queue.abort_request(request.request_id)
                    break
                time.sleep(0.1)
        
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

    def wake_up(self, tags: Optional[List[str]] = None) -> bool:
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

    def abort_requests(self, request_ids: List[str]) -> List[Request]:
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

    def step(self) -> List[Request]:
        """
        Execute a single engine step.

        This schedules waiting requests, processes them, and returns
        any requests that completed during this step.

        Returns:
            List of requests that finished during this step
        """
        if self._shutdown_event.is_set():
            return []
        
        # Transition to running if we have work
        if self._state == EngineState.READY and self.request_queue.has_unfinished_requests():
            self._transition_to(EngineState.RUNNING)
        
        if self._state != EngineState.RUNNING:
            return []
        
        finished = []
        
        try:
            # Schedule waiting requests
            available_slots = (
                self.config.max_requests - self.request_queue.get_num_running()
            )
            if available_slots > 0:
                self.request_queue.schedule_next(available_slots)
            
            # Record step timing
            self._step_count += 1
            self._last_step_time = time.time()
            
            # Process running requests (placeholder - actual processing
            # would happen in a subclass or via callbacks)
            for request in self.request_queue.get_running_requests():
                # Check if request should stop (e.g., hit max_tokens)
                if request.should_stop():
                    reason = FinishReason.LENGTH
                    if request.output_token_ids and request.eos_token_id:
                        if request.output_token_ids[-1] == request.eos_token_id:
                            reason = FinishReason.STOP
                    
                    self.request_queue.finish_request(
                        request.request_id,
                        reason,
                    )
                    self.tracker.record_request(request)
                    finished.append(request)
                    
                    if self.config.on_request_complete:
                        try:
                            self.config.on_request_complete(request)
                        except Exception as e:
                            logger.exception("Error in completion callback: %s", e)
            
            # Transition back to ready if no work remains
            if not self.request_queue.has_unfinished_requests():
                self._transition_to(EngineState.READY)
        
        except Exception as e:
            self._last_error = e
            self._error_count += 1
            logger.exception("Error during step: %s", e)
            if self.config.on_error:
                self.config.on_error(e)
        
        return finished

    async def step_async(self) -> List[Request]:
        """Async version of step()."""
        return await asyncio.get_event_loop().run_in_executor(None, self.step)

    # -------------------------------------------------------------------------
    # Health & Monitoring
    # -------------------------------------------------------------------------

    def health_check(self) -> Dict[str, Any]:
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

    def get_stats(self) -> Dict[str, Any]:
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
        def signal_handler(signum, frame):
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
