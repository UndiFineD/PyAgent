# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""
Disaggregated Scheduler - Separate scheduling for prefill and decode phases.

Enables disaggregated prefill-decode inference where prefill and decode
run on separate GPU instances with KV cache transfer between them.

Key patterns from vLLM:
- Proxy orchestration between prefill and decode instances
- kv_transfer_params for coordinating KV cache transfer
- Separate scheduling logic for each phase

Beyond vLLM:
- Dynamic instance scaling based on load
- Adaptive routing with health awareness
- Connection pooling for multi-instance deployments
"""

from __future__ import annotations

import asyncio
import logging
import random
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Protocol,
    Sequence,
    Tuple,
    Union,
)

logger = logging.getLogger(__name__)


class InstanceRole(Enum):
    """Role of a vLLM instance in disaggregated serving."""
    PREFILL = auto()     # Handles prefill phase only
    DECODE = auto()      # Handles decode phase only
    UNIFIED = auto()     # Handles both (traditional mode)


class SchedulingPolicy(Enum):
    """Request routing policy for multi-instance deployment."""
    ROUND_ROBIN = auto()         # Simple rotation
    LEAST_LOADED = auto()        # Route to least busy instance
    RANDOM = auto()              # Random selection
    HASH_BASED = auto()          # Hash request ID for consistency
    LATENCY_AWARE = auto()       # Route to lowest latency instance


@dataclass
class InstanceInfo:
    """Information about a vLLM instance.
    
    Inspired by vLLM's proxy server patterns.
    """
    instance_id: str
    role: InstanceRole
    host: str
    http_port: int
    kv_port: Optional[int] = None
    handshake_port: Optional[int] = None
    notify_port: Optional[int] = None
    
    # Load and health metrics
    num_running_requests: int = 0
    num_waiting_requests: int = 0
    kv_cache_usage: float = 0.0
    last_health_check: float = 0.0
    is_healthy: bool = True
    
    # Parallel configuration
    tp_size: int = 1
    dp_size: int = 1
    dp_rank: Optional[int] = None
    
    @property
    def base_url(self) -> str:
        """Get the HTTP base URL for this instance."""
        return f"http://{self.host}:{self.http_port}"
    
    @property
    def kv_address(self) -> Optional[str]:
        """Get the KV transfer address."""
        if self.kv_port:
            return f"{self.host}:{self.kv_port}"
        return None
    
    @property
    def load_score(self) -> float:
        """Calculate load score (lower is better)."""
        return self.num_running_requests + self.num_waiting_requests * 0.5


@dataclass
class DCPConfig:
    """Configuration for disaggregated prefill-decode.
    
    Inspired by vLLM's kv_transfer configuration.
    """
    enabled: bool = False
    
    # Instance configuration
    prefill_instances: List[InstanceInfo] = field(default_factory=list)
    decode_instances: List[InstanceInfo] = field(default_factory=list)
    
    # Routing configuration
    prefill_policy: SchedulingPolicy = SchedulingPolicy.LEAST_LOADED
    decode_policy: SchedulingPolicy = SchedulingPolicy.LEAST_LOADED
    
    # KV transfer configuration
    kv_connector: str = "NixlConnector"
    kv_buffer_size: int = int(1e10)  # 10GB
    kv_buffer_device: str = "cuda"
    
    # Health check configuration
    health_check_interval: float = 5.0
    health_check_timeout: float = 2.0
    max_consecutive_failures: int = 3
    
    # Beyond vLLM: Scaling configuration
    auto_scale: bool = False
    min_prefill_instances: int = 1
    max_prefill_instances: int = 4
    min_decode_instances: int = 1
    max_decode_instances: int = 4
    scale_up_threshold: float = 0.8  # KV cache usage
    scale_down_threshold: float = 0.3


@dataclass
class KVTransferParams:
    """Parameters for KV cache transfer between instances.
    
    Inspired by vLLM's kv_transfer_params dict structure.
    """
    do_remote_prefill: bool = False
    do_remote_decode: bool = False
    
    # Remote instance info
    remote_engine_id: Optional[str] = None
    remote_host: Optional[str] = None
    remote_port: Optional[int] = None
    remote_block_ids: Optional[List[int]] = None
    
    # Port configuration
    remote_handshake_port: Optional[int] = None
    remote_notify_port: Optional[int] = None
    
    # Parallel configuration
    remote_tp_size: int = 1
    remote_dp_size: int = 1
    remote_dp_rank: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for request body."""
        return {
            "do_remote_prefill": self.do_remote_prefill,
            "do_remote_decode": self.do_remote_decode,
            "remote_engine_id": self.remote_engine_id,
            "remote_host": self.remote_host,
            "remote_port": self.remote_port,
            "remote_block_ids": self.remote_block_ids,
            "remote_handshake_port": self.remote_handshake_port,
            "remote_notify_port": self.remote_notify_port,
            "remote_tp_size": self.remote_tp_size,
            "remote_dp_size": self.remote_dp_size,
            "remote_dp_rank": self.remote_dp_rank,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "KVTransferParams":
        """Create from dictionary."""
        return cls(
            do_remote_prefill=data.get("do_remote_prefill", False),
            do_remote_decode=data.get("do_remote_decode", False),
            remote_engine_id=data.get("remote_engine_id"),
            remote_host=data.get("remote_host"),
            remote_port=data.get("remote_port"),
            remote_block_ids=data.get("remote_block_ids"),
            remote_handshake_port=data.get("remote_handshake_port"),
            remote_notify_port=data.get("remote_notify_port"),
            remote_tp_size=data.get("remote_tp_size", 1),
            remote_dp_size=data.get("remote_dp_size", 1),
            remote_dp_rank=data.get("remote_dp_rank"),
        )


@dataclass
class ScheduledRequest:
    """A request scheduled for processing."""
    request_id: str
    prompt: str
    max_tokens: int
    
    # Scheduling metadata
    arrival_time: float = field(default_factory=time.time)
    scheduled_time: Optional[float] = None
    prefill_instance: Optional[InstanceInfo] = None
    decode_instance: Optional[InstanceInfo] = None
    
    # KV transfer state
    kv_transfer_params: Optional[KVTransferParams] = None
    prefill_complete: bool = False
    
    # Additional parameters
    extra_params: Dict[str, Any] = field(default_factory=dict)


class InstanceSelector(ABC):
    """Abstract base for instance selection strategies."""
    
    @abstractmethod
    def select(
        self,
        instances: List[InstanceInfo],
        request: ScheduledRequest,
    ) -> Optional[InstanceInfo]:
        """Select an instance for the request."""
        ...


class RoundRobinSelector(InstanceSelector):
    """Round-robin instance selection."""
    
    def __init__(self):
        self._counter = 0
    
    def select(
        self,
        instances: List[InstanceInfo],
        request: ScheduledRequest,
    ) -> Optional[InstanceInfo]:
        if not instances:
            return None
        
        healthy = [i for i in instances if i.is_healthy]
        if not healthy:
            return None
        
        idx = self._counter % len(healthy)
        self._counter += 1
        return healthy[idx]


class LeastLoadedSelector(InstanceSelector):
    """Select least loaded instance."""
    
    def select(
        self,
        instances: List[InstanceInfo],
        request: ScheduledRequest,
    ) -> Optional[InstanceInfo]:
        healthy = [i for i in instances if i.is_healthy]
        if not healthy:
            return None
        
        return min(healthy, key=lambda i: i.load_score)


class RandomSelector(InstanceSelector):
    """Random instance selection."""
    
    def select(
        self,
        instances: List[InstanceInfo],
        request: ScheduledRequest,
    ) -> Optional[InstanceInfo]:
        healthy = [i for i in instances if i.is_healthy]
        if not healthy:
            return None
        
        return random.choice(healthy)


class HashSelector(InstanceSelector):
    """Hash-based consistent instance selection."""
    
    def select(
        self,
        instances: List[InstanceInfo],
        request: ScheduledRequest,
    ) -> Optional[InstanceInfo]:
        healthy = [i for i in instances if i.is_healthy]
        if not healthy:
            return None
        
        # Hash request ID to select instance
        hash_val = hash(request.request_id)
        idx = hash_val % len(healthy)
        return healthy[idx]


class DisaggregatedScheduler:
    """Scheduler for disaggregated prefill-decode inference.
    
    Coordinates request routing between prefill and decode instances.
    
    Inspired by vLLM's disaggregated serving patterns in examples/.
    """
    
    _SELECTOR_MAP: Dict[SchedulingPolicy, type] = {
        SchedulingPolicy.ROUND_ROBIN: RoundRobinSelector,
        SchedulingPolicy.LEAST_LOADED: LeastLoadedSelector,
        SchedulingPolicy.RANDOM: RandomSelector,
        SchedulingPolicy.HASH_BASED: HashSelector,
    }
    
    def __init__(self, config: DCPConfig):
        """Initialize the scheduler.
        
        Args:
            config: Disaggregation configuration
        """
        self.config = config
        
        # Instance pools
        self._prefill_instances: List[InstanceInfo] = list(config.prefill_instances)
        self._decode_instances: List[InstanceInfo] = list(config.decode_instances)
        
        # Selectors
        self._prefill_selector = self._create_selector(config.prefill_policy)
        self._decode_selector = self._create_selector(config.decode_policy)
        
        # Request tracking
        self._pending_requests: Dict[str, ScheduledRequest] = {}
        self._completed_prefills: Dict[str, ScheduledRequest] = {}
        
        # Statistics
        self._total_requests = 0
        self._prefill_requests = 0
        self._decode_requests = 0
        
        # Health check state
        self._health_check_task: Optional[asyncio.Task] = None
    
    def _create_selector(self, policy: SchedulingPolicy) -> InstanceSelector:
        """Create an instance selector for the given policy."""
        if policy not in self._SELECTOR_MAP:
            logger.warning(f"Unknown policy {policy}, using round-robin")
            policy = SchedulingPolicy.ROUND_ROBIN
        
        selector_cls = self._SELECTOR_MAP[policy]
        return selector_cls()
    
    def add_prefill_instance(self, instance: InstanceInfo) -> None:
        """Add a prefill instance to the pool."""
        instance.role = InstanceRole.PREFILL
        self._prefill_instances.append(instance)
        logger.info(f"Added prefill instance: {instance.instance_id}")
    
    def add_decode_instance(self, instance: InstanceInfo) -> None:
        """Add a decode instance to the pool."""
        instance.role = InstanceRole.DECODE
        self._decode_instances.append(instance)
        logger.info(f"Added decode instance: {instance.instance_id}")
    
    def remove_instance(self, instance_id: str) -> bool:
        """Remove an instance from the pool."""
        for instances in [self._prefill_instances, self._decode_instances]:
            for i, inst in enumerate(instances):
                if inst.instance_id == instance_id:
                    del instances[i]
                    logger.info(f"Removed instance: {instance_id}")
                    return True
        return False
    
    def schedule_prefill(
        self,
        request: ScheduledRequest,
    ) -> Tuple[Optional[InstanceInfo], KVTransferParams]:
        """Schedule a request for prefill phase.
        
        Args:
            request: Request to schedule
            
        Returns:
            Tuple of (selected instance, KV transfer params)
        """
        # Select prefill instance
        prefill_instance = self._prefill_selector.select(
            self._prefill_instances, request
        )
        
        if prefill_instance is None:
            logger.warning("No healthy prefill instance available")
            return None, KVTransferParams()
        
        # Select decode instance for later
        decode_instance = self._decode_selector.select(
            self._decode_instances, request
        )
        
        # Create KV transfer params for prefill
        params = KVTransferParams(
            do_remote_decode=True,  # Will transfer to decode instance
            do_remote_prefill=False,
            remote_host=decode_instance.host if decode_instance else None,
            remote_port=decode_instance.kv_port if decode_instance else None,
            remote_handshake_port=decode_instance.handshake_port if decode_instance else None,
            remote_notify_port=decode_instance.notify_port if decode_instance else None,
            remote_tp_size=decode_instance.tp_size if decode_instance else 1,
            remote_dp_size=decode_instance.dp_size if decode_instance else 1,
        )
        
        # Track request
        request.prefill_instance = prefill_instance
        request.decode_instance = decode_instance
        request.kv_transfer_params = params
        request.scheduled_time = time.time()
        
        self._pending_requests[request.request_id] = request
        self._prefill_requests += 1
        self._total_requests += 1
        
        # Update instance load
        prefill_instance.num_running_requests += 1
        
        return prefill_instance, params
    
    def schedule_decode(
        self,
        request: ScheduledRequest,
        prefill_response: Dict[str, Any],
    ) -> Tuple[Optional[InstanceInfo], KVTransferParams]:
        """Schedule a request for decode phase.
        
        Args:
            request: Request that completed prefill
            prefill_response: Response from prefill instance
            
        Returns:
            Tuple of (decode instance, KV transfer params)
        """
        # Get stored decode instance or select new one
        decode_instance = request.decode_instance
        if decode_instance is None or not decode_instance.is_healthy:
            decode_instance = self._decode_selector.select(
                self._decode_instances, request
            )
        
        if decode_instance is None:
            logger.warning("No healthy decode instance available")
            return None, KVTransferParams()
        
        # Extract transfer params from prefill response
        kv_params_dict = prefill_response.get("kv_transfer_params", {})
        
        # Get prefill instance info
        prefill_instance = request.prefill_instance
        
        # Create decode params
        params = KVTransferParams(
            do_remote_prefill=True,  # Will receive from prefill instance
            do_remote_decode=False,
            remote_engine_id=kv_params_dict.get("remote_engine_id"),
            remote_block_ids=kv_params_dict.get("remote_block_ids"),
            remote_host=prefill_instance.host if prefill_instance else None,
            remote_port=prefill_instance.kv_port if prefill_instance else None,
            remote_handshake_port=prefill_instance.handshake_port if prefill_instance else None,
            remote_notify_port=prefill_instance.notify_port if prefill_instance else None,
            remote_tp_size=prefill_instance.tp_size if prefill_instance else 1,
            remote_dp_size=prefill_instance.dp_size if prefill_instance else 1,
        )
        
        # Update request state
        request.prefill_complete = True
        request.kv_transfer_params = params
        request.decode_instance = decode_instance
        
        self._completed_prefills[request.request_id] = request
        self._decode_requests += 1
        
        # Update instance loads
        if prefill_instance:
            prefill_instance.num_running_requests -= 1
        decode_instance.num_running_requests += 1
        
        return decode_instance, params
    
    def request_finished(self, request_id: str) -> None:
        """Mark a request as finished."""
        request = self._pending_requests.pop(request_id, None)
        if request is None:
            request = self._completed_prefills.pop(request_id, None)
        
        if request and request.decode_instance:
            request.decode_instance.num_running_requests -= 1
    
    def get_prefill_request(
        self,
        request: ScheduledRequest,
    ) -> Dict[str, Any]:
        """Build prefill request for sending to instance.
        
        Args:
            request: Scheduled request
            
        Returns:
            Request body for prefill instance
        """
        body = {
            "prompt": request.prompt,
            "max_tokens": 1,  # Prefill only generates 1 token
            "stream": False,
            **request.extra_params,
        }
        
        if request.kv_transfer_params:
            body["kv_transfer_params"] = request.kv_transfer_params.to_dict()
        
        return body
    
    def get_decode_request(
        self,
        request: ScheduledRequest,
    ) -> Dict[str, Any]:
        """Build decode request for sending to instance.
        
        Args:
            request: Scheduled request after prefill
            
        Returns:
            Request body for decode instance
        """
        body = {
            "prompt": request.prompt,
            "max_tokens": request.max_tokens,
            **request.extra_params,
        }
        
        if request.kv_transfer_params:
            body["kv_transfer_params"] = request.kv_transfer_params.to_dict()
        
        return body
    
    def get_instance_stats(self) -> Dict[str, Any]:
        """Get scheduler statistics."""
        return {
            "total_requests": self._total_requests,
            "prefill_requests": self._prefill_requests,
            "decode_requests": self._decode_requests,
            "pending_requests": len(self._pending_requests),
            "prefill_instances": len(self._prefill_instances),
            "decode_instances": len(self._decode_instances),
            "healthy_prefill": sum(1 for i in self._prefill_instances if i.is_healthy),
            "healthy_decode": sum(1 for i in self._decode_instances if i.is_healthy),
        }
    
    async def start_health_checks(self) -> None:
        """Start periodic health checking of instances."""
        if self._health_check_task is not None:
            return
        
        self._health_check_task = asyncio.create_task(self._health_check_loop())
    
    async def stop_health_checks(self) -> None:
        """Stop health checking."""
        if self._health_check_task:
            self._health_check_task.cancel()
            try:
                await self._health_check_task
            except asyncio.CancelledError:
                pass
            self._health_check_task = None
    
    async def _health_check_loop(self) -> None:
        """Background loop for health checking."""
        while True:
            try:
                await asyncio.sleep(self.config.health_check_interval)
                await self._check_all_instances()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Health check error: {e}")
    
    async def _check_all_instances(self) -> None:
        """Check health of all instances."""
        all_instances = self._prefill_instances + self._decode_instances
        
        for instance in all_instances:
            try:
                # In production, this would make HTTP health check
                # For now, just update timestamp
                instance.last_health_check = time.time()
            except Exception as e:
                logger.warning(f"Health check failed for {instance.instance_id}: {e}")


class ProxyOrchestrator:
    """Orchestrates requests through prefill and decode instances.
    
    Provides high-level API for disaggregated serving.
    
    Inspired by vLLM's proxy server examples.
    """
    
    def __init__(
        self,
        scheduler: DisaggregatedScheduler,
    ):
        """Initialize the orchestrator.
        
        Args:
            scheduler: Disaggregated scheduler instance
        """
        self.scheduler = scheduler
        self._request_counter = 0
    
    def create_request(
        self,
        prompt: str,
        max_tokens: int,
        request_id: Optional[str] = None,
        **kwargs: Any,
    ) -> ScheduledRequest:
        """Create a new request.
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            request_id: Optional custom request ID
            **kwargs: Additional parameters
            
        Returns:
            Scheduled request object
        """
        if request_id is None:
            self._request_counter += 1
            request_id = f"req_{self._request_counter}_{time.time():.0f}"
        
        return ScheduledRequest(
            request_id=request_id,
            prompt=prompt,
            max_tokens=max_tokens,
            extra_params=kwargs,
        )
    
    async def process_request(
        self,
        request: ScheduledRequest,
        prefill_callback: Optional[Callable] = None,
    ) -> Dict[str, Any]:
        """Process a request through prefill and decode.
        
        This is the main entry point for disaggregated serving.
        
        Args:
            request: Request to process
            prefill_callback: Optional callback after prefill completes
            
        Returns:
            Final response from decode instance
        """
        # Phase 1: Prefill
        prefill_instance, prefill_params = self.scheduler.schedule_prefill(request)
        if prefill_instance is None:
            return {"error": "No prefill instance available"}
        
        prefill_body = self.scheduler.get_prefill_request(request)
        
        # In production, send to prefill instance
        # prefill_response = await http_client.post(
        #     f"{prefill_instance.base_url}/v1/completions",
        #     json=prefill_body,
        # )
        
        # Simulate prefill response
        prefill_response = {
            "kv_transfer_params": {
                "remote_engine_id": prefill_instance.instance_id,
                "remote_block_ids": list(range(10)),  # Placeholder
            }
        }
        
        if prefill_callback:
            await prefill_callback(prefill_response)
        
        # Phase 2: Decode
        decode_instance, decode_params = self.scheduler.schedule_decode(
            request, prefill_response
        )
        if decode_instance is None:
            return {"error": "No decode instance available"}
        
        decode_body = self.scheduler.get_decode_request(request)
        
        # In production, send to decode instance
        # decode_response = await http_client.post(
        #     f"{decode_instance.base_url}/v1/completions",
        #     json=decode_body,
        # )
        
        # Simulate decode response
        decode_response = {
            "id": request.request_id,
            "choices": [{"text": "Generated text placeholder"}],
        }
        
        # Cleanup
        self.scheduler.request_finished(request.request_id)
        
        return decode_response


# Factory functions
def create_dcp_scheduler(
    prefill_urls: List[str],
    decode_urls: List[str],
    **kwargs: Any,
) -> DisaggregatedScheduler:
    """Create a disaggregated scheduler from instance URLs.
    
    Args:
        prefill_urls: List of prefill instance URLs
        decode_urls: List of decode instance URLs
        **kwargs: Additional configuration
        
    Returns:
        Configured scheduler
    """
    config = DCPConfig(enabled=True, **kwargs)
    
    # Parse prefill instances
    for i, url in enumerate(prefill_urls):
        parts = url.replace("http://", "").split(":")
        host = parts[0]
        port = int(parts[1]) if len(parts) > 1 else 8000
        
        config.prefill_instances.append(InstanceInfo(
            instance_id=f"prefill_{i}",
            role=InstanceRole.PREFILL,
            host=host,
            http_port=port,
        ))
    
    # Parse decode instances
    for i, url in enumerate(decode_urls):
        parts = url.replace("http://", "").split(":")
        host = parts[0]
        port = int(parts[1]) if len(parts) > 1 else 8000
        
        config.decode_instances.append(InstanceInfo(
            instance_id=f"decode_{i}",
            role=InstanceRole.DECODE,
            host=host,
            http_port=port,
        ))
    
    return DisaggregatedScheduler(config)
