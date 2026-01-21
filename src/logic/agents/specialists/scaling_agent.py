# Copyright 2026 PyAgent Authors
# ScalingAgent: Fleet Expansion and Resource Orchestration - Phase 319 Enhanced

from __future__ import annotations
from src.core.base.lifecycle.version import VERSION
import logging
import asyncio
import time
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.common.base_utilities import as_tool

__version__ = VERSION

class ProviderType(Enum):
    LOCAL = "local"
    GITHUB = "github"
    AZURE = "azure"
    OLLAMA = "ollama"
    VLLM = "vllm"

class ScalingStrategy(Enum):
    ROUND_ROBIN = "round_robin"
    LEAST_LOADED = "least_loaded"
    LATENCY_WEIGHTED = "latency_weighted"
    COST_OPTIMIZED = "cost_optimized"
    PRIORITY_BASED = "priority_based"

@dataclass
class ProviderMetrics:
    """Tracks metrics for a compute provider."""
    provider_type: ProviderType
    active_agents: int = 0
    capacity: int = 10
    avg_latency_ms: float = 100.0
    error_rate: float = 0.0
    cost_per_token: float = 0.0
    last_health_check: float = field(default_factory=time.time)
    is_healthy: bool = True

@dataclass
class ScalingDecision:
    """Represents a scaling action."""
    action: str  # "scale_up", "scale_down", "rebalance", "migrate"
    provider: ProviderType
    target_count: int
    reason: str
    urgency: float = 0.5  # 0.0 to 1.0

class ScalingAgent(BaseAgent):
    """
    Agent specializing in dynamic fleet scaling, multi-provider deployment,
    load balancing, and high-concurrency async operations coordination.
    """

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._providers: Dict[ProviderType, ProviderMetrics] = {
            ProviderType.LOCAL: ProviderMetrics(ProviderType.LOCAL, capacity=5, cost_per_token=0.0),
            ProviderType.GITHUB: ProviderMetrics(ProviderType.GITHUB, capacity=50, cost_per_token=0.0),
            ProviderType.AZURE: ProviderMetrics(ProviderType.AZURE, capacity=100, cost_per_token=0.002),
            ProviderType.OLLAMA: ProviderMetrics(ProviderType.OLLAMA, capacity=3, cost_per_token=0.0),
        }
        self._scaling_history: List[ScalingDecision] = []
        self._current_strategy = ScalingStrategy.LATENCY_WEIGHTED
        self._system_prompt = (
            "You are the Scaling Agent. You optimize swarm density and manage "
            "compute resources across multiple providers (GitHub, Azure, Local, Ollama). "
            "You ensure high availability, low latency, and cost efficiency."
        )

    @property
    def total_capacity(self) -> int:
        return sum(p.capacity for p in self._providers.values() if p.is_healthy)

    @property
    def total_active(self) -> int:
        return sum(p.active_agents for p in self._providers.values())

    @property
    def utilization(self) -> float:
        cap = self.total_capacity
        return self.total_active / cap if cap > 0 else 0.0

    @as_tool
    async def recommend_fleet_size(
        self, 
        task_backlog: int, 
        avg_latency: float,
        priority: str = "balanced"
    ) -> Dict[str, Any]:
        """Calculates optimal agent count based on workload and strategy."""
        # Calculate base target
        if priority == "speed":
            target = task_backlog  # 1:1 ratio for max speed
        elif priority == "cost":
            target = max(3, task_backlog // 4)  # Minimize agents
        else:
            target = max(5, int(task_backlog / 2) if avg_latency < 1.0 else task_backlog)
        
        # Distribute across providers based on strategy
        distribution = self._calculate_distribution(target, priority)
        
        # Generate scaling decisions
        decisions = []
        for provider_type, count in distribution.items():
            metrics = self._providers.get(provider_type)
            if metrics:
                diff = count - metrics.active_agents
                if diff > 0:
                    decisions.append(ScalingDecision(
                        action="scale_up",
                        provider=provider_type,
                        target_count=count,
                        reason=f"Backlog requires {diff} more agents",
                        urgency=min(1.0, avg_latency / 2.0)
                    ))
                elif diff < 0:
                    decisions.append(ScalingDecision(
                        action="scale_down",
                        provider=provider_type,
                        target_count=count,
                        reason=f"Excess capacity, reducing by {-diff}",
                        urgency=0.2
                    ))
        
        self._scaling_history.extend(decisions)
        
        return {
            "recommended_total": target,
            "provider_distribution": {k.value: v for k, v in distribution.items()},
            "decisions": [
                {"action": d.action, "provider": d.provider.value, "target": d.target_count, "reason": d.reason}
                for d in decisions
            ],
            "current_utilization": f"{self.utilization:.1%}",
            "strategy": self._current_strategy.value
        }

    @as_tool
    async def coordinate_async_handoff(
        self, 
        swarm_id: str, 
        payload: Dict, 
        strategy: Optional[str] = None
    ) -> Dict[str, Any]:
        """Coordinates load balancing across a swarm with configurable strategy."""
        strat = ScalingStrategy(strategy) if strategy else self._current_strategy
        
        # Select target provider based on strategy
        target = self._select_provider(strat)
        
        logging.info(f"ScalingAgent: Routing swarm {swarm_id} to {target.value} via {strat.value}")
        
        # Simulate async handoff
        await asyncio.sleep(0.05)
        
        # Update metrics
        if target in self._providers:
            self._providers[target].active_agents += 1
        
        return {
            "success": True,
            "swarm_id": swarm_id,
            "routed_to": target.value,
            "strategy": strat.value,
            "payload_keys": list(payload.keys())
        }

    @as_tool
    async def health_check_providers(self) -> Dict[str, Any]:
        """Performs health checks on all compute providers."""
        results = {}
        
        for provider_type, metrics in self._providers.items():
            # Simulate health check
            await asyncio.sleep(0.02)
            
            # Update health status (in real impl, would ping actual endpoints)
            metrics.last_health_check = time.time()
            
            results[provider_type.value] = {
                "healthy": metrics.is_healthy,
                "active_agents": metrics.active_agents,
                "capacity": metrics.capacity,
                "utilization": f"{metrics.active_agents / metrics.capacity:.1%}" if metrics.capacity > 0 else "N/A",
                "avg_latency_ms": metrics.avg_latency_ms,
                "error_rate": f"{metrics.error_rate:.1%}"
            }
        
        return {
            "providers": results,
            "total_healthy": sum(1 for m in self._providers.values() if m.is_healthy),
            "total_capacity": self.total_capacity,
            "overall_utilization": f"{self.utilization:.1%}"
        }

    @as_tool
    async def set_scaling_strategy(self, strategy: str) -> Dict[str, Any]:
        """Updates the load balancing strategy."""
        try:
            self._current_strategy = ScalingStrategy(strategy)
            return {"success": True, "new_strategy": strategy}
        except ValueError:
            return {
                "success": False, 
                "error": f"Unknown strategy: {strategy}",
                "valid_strategies": [s.value for s in ScalingStrategy]
            }

    @as_tool
    async def get_scaling_report(self) -> Dict[str, Any]:
        """Returns comprehensive scaling metrics and history."""
        return {
            "current_strategy": self._current_strategy.value,
            "providers": {
                pt.value: {
                    "active": m.active_agents,
                    "capacity": m.capacity,
                    "latency_ms": m.avg_latency_ms,
                    "cost_per_token": m.cost_per_token,
                    "healthy": m.is_healthy
                }
                for pt, m in self._providers.items()
            },
            "utilization": f"{self.utilization:.1%}",
            "recent_decisions": [
                {"action": d.action, "provider": d.provider.value, "reason": d.reason}
                for d in self._scaling_history[-10:]
            ]
        }

    def _calculate_distribution(self, target: int, priority: str) -> Dict[ProviderType, int]:
        """Distributes agent count across providers based on priority."""
        healthy = {pt: m for pt, m in self._providers.items() if m.is_healthy}
        
        if priority == "cost":
            # Prefer free providers
            result = {}
            remaining = target
            for pt in [ProviderType.LOCAL, ProviderType.OLLAMA, ProviderType.GITHUB, ProviderType.AZURE]:
                if pt in healthy and remaining > 0:
                    alloc = min(remaining, healthy[pt].capacity)
                    result[pt] = alloc
                    remaining -= alloc
            return result
        
        elif priority == "speed":
            # Prefer low-latency providers
            sorted_providers = sorted(healthy.items(), key=lambda x: x[1].avg_latency_ms)
            result = {}
            remaining = target
            for pt, m in sorted_providers:
                if remaining > 0:
                    alloc = min(remaining, m.capacity)
                    result[pt] = alloc
                    remaining -= alloc
            return result
        
        else:  # balanced
            total_cap = sum(m.capacity for m in healthy.values())
            return {
                pt: max(1, int(target * (m.capacity / total_cap)))
                for pt, m in healthy.items()
            } if total_cap > 0 else {}

    def _select_provider(self, strategy: ScalingStrategy) -> ProviderType:
        """Selects a provider based on the current strategy."""
        healthy = [pt for pt, m in self._providers.items() if m.is_healthy]
        
        if not healthy:
            return ProviderType.LOCAL
        
        if strategy == ScalingStrategy.ROUND_ROBIN:
            # Simple round robin
            idx = len(self._scaling_history) % len(healthy)
            return healthy[idx]
        
        elif strategy == ScalingStrategy.LEAST_LOADED:
            return min(healthy, key=lambda pt: self._providers[pt].active_agents / max(1, self._providers[pt].capacity))
        
        elif strategy == ScalingStrategy.LATENCY_WEIGHTED:
            return min(healthy, key=lambda pt: self._providers[pt].avg_latency_ms)
        
        elif strategy == ScalingStrategy.COST_OPTIMIZED:
            return min(healthy, key=lambda pt: self._providers[pt].cost_per_token)
        
        else:  # PRIORITY_BASED
            return healthy[0]
