# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Data-parallel coordination logic.
"""

from __future__ import annotations

import logging
import threading
from typing import (
    Dict,
    Optional,
)

import numpy as np

from .config import EngineIdentity, EngineState, LoadBalancingStrategy, ParallelConfig
from .messages import MetricsMessage

logger = logging.getLogger(__name__)


class DPCoordinator:
    """Coordinator for data-parallel engine instances.

    Inspired by vLLM's DPCoordinator and dp_lb_pool patterns.
    Manages multiple engine instances and distributes requests.
    """

    def __init__(
        self,
        parallel_config: ParallelConfig,
        load_balancing: LoadBalancingStrategy = LoadBalancingStrategy.ROUND_ROBIN,
    ):
        self.config = parallel_config
        self.load_balancing = load_balancing

        self._engines: Dict[str, EngineIdentity] = {}
        self._engine_states: Dict[str, EngineState] = {}
        self._engine_metrics: Dict[str, MetricsMessage] = {}

        self._round_robin_idx = 0
        self._lock = threading.Lock()
        self._running = False

    def register_engine(self, identity: EngineIdentity) -> None:
        """Register a new engine instance.

        Args:
            identity: Engine identity.
        """
        with self._lock:
            self._engines[identity.engine_id] = identity
            self._engine_states[identity.engine_id] = EngineState.READY
            self._engine_metrics[identity.engine_id] = MetricsMessage()
            logger.info("Registered engine: %s", identity)

    def deregister_engine(self, engine_id: str) -> None:
        """Deregister an engine instance.

        Args:
            engine_id: Engine ID to deregister.
        """
        with self._lock:
            self._engines.pop(engine_id, None)
            self._engine_states.pop(engine_id, None)
            self._engine_metrics.pop(engine_id, None)
            logger.info("Deregistered engine: %s", engine_id)

    def select_engine(self, request_id: str = None) -> Optional[str]:
        """Select an engine for processing.

        Args:
            request_id: Request ID (for consistent hashing).

        Returns:
            Engine ID, or None if no engines available.
        """
        with self._lock:
            ready_engines = [
                eid for eid, state in self._engine_states.items()
                if state == EngineState.READY
            ]

            if not ready_engines:
                return None

            if self.load_balancing == LoadBalancingStrategy.ROUND_ROBIN:
                idx = self._round_robin_idx % len(ready_engines)
                self._round_robin_idx += 1
                return ready_engines[idx]

            elif self.load_balancing == LoadBalancingStrategy.LEAST_LOADED:
                # Select engine with lowest queue depth
                min_load = float('inf')
                selected = ready_engines[0]
                for eid in ready_engines:
                    metrics = self._engine_metrics.get(eid)
                    if metrics and metrics.queue_depth < min_load:
                        min_load = metrics.queue_depth
                        selected = eid
                return selected

            elif self.load_balancing == LoadBalancingStrategy.RANDOM:
                return ready_engines[np.random.randint(len(ready_engines))]

            elif self.load_balancing == LoadBalancingStrategy.CONSISTENT_HASH:
                if request_id:
                    idx = hash(request_id) % len(ready_engines)
                    return ready_engines[idx]
                return ready_engines[0]

            return ready_engines[0]

    def update_metrics(self, engine_id: str, metrics: MetricsMessage) -> None:
        """Update metrics for an engine.

        Args:
            engine_id: Engine ID.
            metrics: Updated metrics.
        """
        with self._lock:
            self._engine_metrics[engine_id] = metrics

    def set_engine_state(self, engine_id: str, state: EngineState) -> None:
        """Set engine state.

        Args:
            engine_id: Engine ID.
            state: New state.
        """
        with self._lock:
            if engine_id in self._engine_states:
                self._engine_states[engine_id] = state

    def get_engine_states(self) -> Dict[str, EngineState]:
        """Get all engine states."""
        with self._lock:
            return dict(self._engine_states)

    @property
    def num_engines(self) -> int:
        """Number of registered engines."""
        return len(self._engines)

    @property
    def num_ready(self) -> int:
        """Number of ready engines."""
        with self._lock:
            return list(self._engine_states.values()).count(EngineState.READY)
