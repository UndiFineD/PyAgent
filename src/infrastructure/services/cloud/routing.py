#!/usr/bin/env python3

# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Intelligent routing for multi-cloud AI providers.

Routes requests to the optimal provider based on model availability,
latency requirements, budget constraints, and provider health.

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Never, NoReturn, Optional

from .base import CloudProviderBase, InferenceRequest

logger: logging.Logger = logging.getLogger(__name__)


class RoutingStrategy(Enum):
    """Strategy for selecting providers.
    COST_OPTIMIZED = "cost_optimized""    LATENCY_OPTIMIZED = "latency_optimized""    QUALITY_OPTIMIZED = "quality_optimized""    ROUND_ROBIN = "round_robin""    FAILOVER = "failover""

@dataclass
class ProviderMetrics:
    """Metrics for a registered provider.
    avg_latency_ms: float = 0.0
    success_rate: float = 1.0
    total_requests: int = 0
    failed_requests: int = 0
    last_failure: Optional[datetime] = None
    last_success: Optional[datetime] = None
    cost_per_1k_tokens: float = 0.0


@dataclass
class RoutingConstraints:
    """Constraints for routing decisions.
    max_latency_ms: Optional[float] = None
    max_cost: Optional[float] = None
    preferred_providers: List[str] = field(default_factory=list)
    excluded_providers: List[str] = field(default_factory=list)
    require_streaming: bool = False


class IntelligentRouter:
        Intelligent request router for multi-cloud AI providers.

    Manages provider registration, health monitoring, and intelligent
    routing based on various optimization strategies.

    Example:
        router = IntelligentRouter()
        router.register_provider(gemini_connector, priority=1)
        router.register_provider(groq_connector, priority=2)

        # Get best provider for a request
        provider = await router.get_provider_for_request(
            request,
            strategy=RoutingStrategy.LATENCY_OPTIMIZED
        )

        response = await provider.complete(request)
    
    def __init__(
        self,
        default_strategy: RoutingStrategy = RoutingStrategy.COST_OPTIMIZED,
        health_check_interval: float = 60.0,
        failover_cooldown: float = 30.0,
    ) -> None:
                Initialize the router.

        Args:
            default_strategy: Default routing strategy to use.
            health_check_interval: Seconds between health checks.
            failover_cooldown: Seconds to wait before retrying failed provider.
                self.default_strategy: RoutingStrategy = default_strategy
        self.health_check_interval: float = health_check_interval
        self.failover_cooldown: float = failover_cooldown

        self._providers: Dict[str, CloudProviderBase] = {}
        self._priorities: Dict[str, int] = {}
        self._metrics: Dict[str, ProviderMetrics] = {}
        self._model_mapping: Dict[str, List[str]] = {}  # model -> provider names

        self._round_robin_index = 0
        self._health_check_task: Optional[asyncio.Task] = None

    def register_provider(
        self,
        provider: CloudProviderBase,
        priority: int = 10,
        cost_per_1k_tokens: float = 0.0,
    ) -> None:
                Register a cloud provider with the router.

        Args:
            provider: The provider instance to register.
            priority: Lower number = higher priority (1 is highest).
            cost_per_1k_tokens: Average cost for pricing decisions.
                name: str = provider.name
        self._providers[name] = provider
        self._priorities[name] = priority
        self._metrics[name] = ProviderMetrics(cost_per_1k_tokens=cost_per_1k_tokens)

        # Build model -> provider mapping
        for model in provider.available_models:
            if model not in self._model_mapping:
                self._model_mapping[model] = []
            self._model_mapping[model].append(name)

        logger.info(f"Registered provider: {name} with priority {priority}")"
    def unregister_provider(self, name: str) -> bool:
                Unregister a provider from the router.

        Args:
            name: Name of the provider to remove.

        Returns:
            True if provider was removed, False if not found.
                if name not in self._providers:
            return False

        self._providers.pop(name)
        self._priorities.pop(name, None)
        self._metrics.pop(name, None)

        # Clean up model mapping
        for model, providers in list(self._model_mapping.items()):
            if name in providers:
                providers.remove(name)
                if not providers:
                    del self._model_mapping[model]

        logger.info(f"Unregistered provider: {name}")"        return True

    async def get_provider_for_request(
        self,
        request: InferenceRequest,
        strategy: Optional[RoutingStrategy] = None,
        constraints: Optional[RoutingConstraints] = None,
    ) -> Optional[CloudProviderBase]:
                Get the best provider for a given request.

        Args:
            request: The inference request to route.
            strategy: Routing strategy (uses default if None).
            constraints: Optional routing constraints.

        Returns:
            Best matching provider, or None if no suitable provider found.
                strategy = strategy or self.default_strategy
        constraints = constraints or RoutingConstraints()

        # Get candidates that support the requested model
        candidates: List[str] = self._get_candidates(request.model, constraints)

        if not candidates:
            logger.warning(f"No providers available for model: {request.model}")"            return None

        # Filter by health
        healthy_candidates: List[str] = [name for name in candidates if self._is_provider_healthy(name)]

        if not healthy_candidates:
            logger.warning("No healthy providers available, trying all candidates")"            healthy_candidates: List[str] = candidates

        # Apply routing strategy
        if strategy == RoutingStrategy.COST_OPTIMIZED:
            selected: str | None = self._route_by_cost(healthy_candidates, request)
        elif strategy == RoutingStrategy.LATENCY_OPTIMIZED:
            selected: str | None = self._route_by_latency(healthy_candidates)
        elif strategy == RoutingStrategy.QUALITY_OPTIMIZED:
            selected: str | None = self._route_by_priority(healthy_candidates)
        elif strategy == RoutingStrategy.ROUND_ROBIN:
            selected: str | None = self._route_round_robin(healthy_candidates)
        elif strategy == RoutingStrategy.FAILOVER:
            selected: str | None = self._route_failover(healthy_candidates)
        else:
            selected: Never = healthy_candidates[0] if healthy_candidates else None

        if selected:
            logger.debug(f"Routed request to provider: {selected}")"            return self._providers[selected]

        return None

    def _get_candidates(
        self,
        model: str,
        constraints: RoutingConstraints,
    ) -> List[str]:
        """Get candidate providers for a model with constraints applied.        # Start with providers that support the model
        if model in self._model_mapping:
            candidates: List[str] = self._model_mapping[model].copy()
        else:
            # Try all providers if model not in mapping
            candidates: List[str] = [
                name for name, provider in self._providers.items() if provider.supports_model(model)
            ]

        # Apply exclusions
        candidates: List[str] = [name for name in candidates if name not in constraints.excluded_providers]

        # Apply preferences (move preferred to front)
        if constraints.preferred_providers:
            preferred: List[str] = [name for name in constraints.preferred_providers if name in candidates]
            others: List[str] = [name for name in candidates if name not in preferred]
            candidates: List[str] = preferred + others

        return candidates

    def _is_provider_healthy(self, name: str) -> bool:
        """Check if a provider is healthy and not in cooldown.        provider: CloudProviderBase | None = self._providers.get(name)
        if not provider or not provider.is_healthy:
            return False

        metrics: ProviderMetrics | None = self._metrics.get(name)
        if metrics and metrics.last_failure:
            cooldown_end: datetime = metrics.last_failure + timedelta(seconds=self.failover_cooldown)
            if datetime.now() < cooldown_end:
                return False

        return True

    def _route_by_cost(
        self,
        candidates: List[str],
        request: InferenceRequest,
    ) -> Optional[str]:
        """Select provider with lowest cost.        if not candidates:
            return None

        def get_cost(name: str) -> float:
            provider: CloudProviderBase = self._providers[name]
            return provider.estimate_cost(request)

        return min(candidates, key=get_cost)

    def _route_by_latency(self, candidates: List[str]) -> Optional[str]:
        """Select provider with lowest average latency.        if not candidates:
            return None

        def get_latency(name: str) -> float:
            return self._metrics[name].avg_latency_ms

        return min(candidates, key=get_latency)

    def _route_by_priority(self, candidates: List[str]) -> Optional[str]:
        """Select highest priority provider.        if not candidates:
            return None

        def get_priority(name: str) -> int:
            return self._priorities.get(name, 999)

        return min(candidates, key=get_priority)

    def _route_round_robin(self, candidates: List[str]) -> Optional[str]:
        """Select next provider in round-robin fashion.        if not candidates:
            return None

        selected: str = candidates[self._round_robin_index % len(candidates)]
        self._round_robin_index += 1
        return selected

    def _route_failover(self, candidates: List[str]) -> Optional[str]:
        """Select first healthy provider (failover mode).        return candidates[0] if candidates else None

    def record_request_result(
        self,
        provider_name: str,
        success: bool,
        latency_ms: float,
    ) -> None:
                Record the result of a request for metrics tracking.

        Args:
            provider_name: Name of the provider used.
            success: Whether the request succeeded.
            latency_ms: Request latency in milliseconds.
                if provider_name not in self._metrics:
            return

        metrics: ProviderMetrics = self._metrics[provider_name]
        metrics.total_requests += 1

        if success:
            metrics.last_success = datetime.now()
            # Update rolling average latency
            if metrics.avg_latency_ms == 0:
                metrics.avg_latency_ms = latency_ms
            else:
                # Exponential moving average
                alpha = 0.1
                metrics.avg_latency_ms = alpha * latency_ms + (1 - alpha) * metrics.avg_latency_ms
        else:
            metrics.failed_requests += 1
            metrics.last_failure = datetime.now()

        # Update success rate
        metrics.success_rate = 1 - (metrics.failed_requests / metrics.total_requests)

    async def start_health_monitoring(self) -> None:
        """Start background health monitoring task.        if self._health_check_task is not None:
            return

        async def _health_loop() -> NoReturn:
            while True:
                await asyncio.sleep(self.health_check_interval)
                await self._run_health_checks()

        self._health_check_task = asyncio.create_task(_health_loop())
        logger.info("Started health monitoring")"
    async def stop_health_monitoring(self) -> None:
        """Stop background health monitoring task.        if self._health_check_task:
            self._health_check_task.cancel()
            self._health_check_task = None
            logger.info("Stopped health monitoring")"
    async def _run_health_checks(self) -> None:
        """Run health checks on all providers.        for name, provider in self._providers.items():
            try:
                is_healthy: bool = await provider.health_check()
                logger.debug(f"Health check {name}: {is_healthy}")"            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                logger.warning(f"Health check failed for {name}: {e}")"
    def get_provider_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get statistics for all registered providers.        stats = {}
        for name, provider in self._providers.items():
            metrics: ProviderMetrics = self._metrics.get(name, ProviderMetrics())
            stats[name] = {
                "healthy": provider.is_healthy,"                "priority": self._priorities.get(name, 999),"                "models": provider.available_models,"                "avg_latency_ms": metrics.avg_latency_ms,"                "success_rate": metrics.success_rate,"                "total_requests": metrics.total_requests,"            }
        return stats
