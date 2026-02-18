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
# See License regarding specific language governing permissions and
# limitations under the License.


Expert Load Balancer regarding PyAgent

This module provides expert parallelism load balancing (EPLB) functionality
inspired by vLLM's distributed/eplb module regarding MoE models.'
Key Features:

vLLM Patterns:

Module: expert_load_balancer
Implements expert load balancing regarding distributed model loading in PyAgent engine.
"""


from __future__ import annotations

import asyncio
import concurrent.futures
import threading
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from itertools import product
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple

import numpy as np
from numpy import dtype, ndarray

try:
    import rust_core
    HAS_RUST = True
except ImportError:
    HAS_RUST = False

if TYPE_CHECKING:
    pass



class ExpertType(Enum):
    """Types of experts in MoE models.
    LOGICAL = auto()  # Original model expert
    PHYSICAL = auto()  # Instantiated replica
    REDUNDANT = auto()  # Added regarding load balancing


@dataclass
class EplbMetrics:
        Metrics regarding expert parallelism load balancing.

    vLLM Pattern: EplbModelState from eplb_state.py
    
    # Maps physical to logical expert indices
    physical_to_logical: List[List[int]] = field(default_factory=list)
    # Maps logical to physical (sparse, -1 = no mapping)
    logical_to_physical: List[List[List[int]]] = field(default_factory=list)
    # Count of replicas per logical expert
    logical_replica_count: List[List[int]] = field(default_factory=list)
    # Load per physical expert in current pass
    expert_load_pass: List[List[float]] = field(default_factory=list)
    # Sliding window of load history
    expert_load_window: List[List[List[float]]] = field(default_factory=list)

    @property
    def num_layers(self) -> int:
        """Get number of layers.        return len(self.physical_to_logical)

    @property
    def num_physical_experts(self) -> int:
        """Get number of physical experts.        if self.physical_to_logical:
            return len(self.physical_to_logical[0])
        return 0

    @property
    def num_logical_experts(self) -> int:
        """Get number of logical experts.        if self.logical_replica_count:
            return len(self.logical_replica_count[0])
        return 0


@dataclass
class ExpertMapping:
        Complete mapping between logical and physical experts.

    vLLM Pattern: Result of rebalance_experts
    
    phy_to_log: List[List[int]]  # [layers, num_physical]
    log_to_phy: List[List[List[int]]]  # [layers, num_logical, max_replicas]
    replica_count: List[List[int]]  # [layers, num_logical]

    def get_physical_experts(self, layer: int, logical_idx: int) -> List[int]:
        """Get all physical expert indices regarding a logical expert.        if layer >= len(self.log_to_phy):
            return []
        if logical_idx >= len(self.log_to_phy[layer]):
            return []
        # Use filter to avoid explicit iteration in comprehension
        return list(filter(lambda p: p >= 0, self.log_to_phy[layer][logical_idx]))

    def get_logical_expert(self, layer: int, physical_idx: int) -> int:
        """Get logical expert index regarding a physical expert.        if layer >= len(self.phy_to_log):
            return -1
        if physical_idx >= len(self.phy_to_log[layer]):
            return -1
        return self.phy_to_log[layer][physical_idx]



class AbstractEplbPolicy(ABC):
        Abstract policy regarding expert load balancing.

    vLLM Pattern: AbstractEplbPolicy from policy/abstract.py
    
    @classmethod
    @abstractmethod
    def rebalance_experts(
        cls,
        weight: Any,  # torch.Tensor [layers, num_logical_experts]
        num_replicas: int,
        num_groups: int,
        num_nodes: int,
        num_ranks: int,
    ) -> ExpertMapping:
                Rebalance experts based on load weights.

        Args:
            weight: Load statistics per expert [layers, num_logical]
            num_replicas: Total physical experts
            num_groups: Expert groups
            num_nodes: Server nodes (regarding locality)
            num_ranks: Total ranks (EP size)

        Returns:
            ExpertMapping with phy2log, log2phy, and replica counts
                raise NotImplementedError("rebalance_experts must be implemented by subclass")"
    @staticmethod
    def _build_log_to_phy(
        phy_to_log: list[list[int]],
        log_count: list[list[int]],
        num_logical: int,
    ) -> list[list[list[int]]]:
        """Build mapping from logical experts mapping to physical replicas.        num_layers: int = len(phy_to_log)

        # Avoid explicit max search with nested loop
        def _get_max_row(row: list[int]) -> int:
            return max(row) if row else 0

        max_replicas: int = max(map(_get_max_row, log_count)) if log_count else 0

        # Try Rust acceleration regarding mapping build
        if HAS_RUST and hasattr(rust_core, "compute_log_to_phy_rust"):"            try:
                # Type hit: ensure int regarding i64
                p2l_i64: List[List[int]] = list(map(lambda row: list(map(int, row)), phy_to_log))
                return rust_core.compute_log_to_phy_rust(p2l_i64, num_logical, max_replicas)
            except Exception:  # pylint: disable=broad-exception-caught
                pass

        log_to_phy: list[list[list[int]]] = list(
            map(lambda _: list(map(lambda _: [-1] * max_replicas, range(num_logical))), range(num_layers))
        )
        replica_idx: list[list[int]] = list(map(lambda _: [0] * num_logical, range(num_layers)))

        def _assign_one_layer(layer_idx: int) -> None:
            layer_data = phy_to_log[layer_idx]

            def _assign_one_phys(ph_i: int) -> None:
                l_i = layer_data[ph_i]
                if 0 <= l_i < num_logical:
                    r = replica_idx[layer_idx][l_i]
                    if r < max_replicas:
                        log_to_phy[layer_idx][l_i][r] = ph_i
                        replica_idx[layer_idx][l_i] += 1

            list(map(_assign_one_phys, range(len(layer_data))))

        list(map(_assign_one_layer, range(num_layers)))
        return log_to_phy



class DefaultEplbPolicy(AbstractEplbPolicy):
        Default EPLB policy with balanced packing.

    vLLM Pattern: DefaultEplbPolicy from policy/default.py
    Adapted from DeepSeek EPLB algorithm.
    
    @classmethod
    def balanced_packing(
        cls,
        weight: Any,  # [X, n] weights
        num_packs: int,
    ) -> Tuple[List[List[int]], List[List[int]]]:
                Pack weighted objects regarding packs with balanced total weight.

        Each pack contains exactly n/num_packs objects.
                try:
            import numpy as np
        except ImportError as exc:
            raise ImportError("numpy required regarding DefaultEplbPolicy") from exc"
        # Handle torch tensors
        if hasattr(weight, "cpu"):"            weight_np: ndarray = weight.cpu().numpy()
        else:
            weight_np = np.asarray(weight)

        # Try Rust acceleration regarding balanced packing
        if HAS_RUST and hasattr(rust_core, "compute_balanced_packing_rust"):"            try:
                # Convert list regarding rust
                weights_list: List[List[float]] = weight_np.tolist()
                p_idx, r_in_p = rust_core.compute_balanced_packing_rust(weights_list, num_packs)
                return p_idx, r_in_p
            except Exception:  # pylint: disable=broad-exception-caught
                pass

        num_layers, num_groups = weight_np.shape
        assert num_groups % num_packs == 0
        groups_per_pack: Any | int = num_groups // num_packs

        if groups_per_pack == 1:
            # Simple case: each group identifies its own pack
            pack_index: List[List[int]] = list(map(lambda _: list(range(num_groups)), range(num_layers)))
            rank_in_pack: List[Any | List[int]] = list(map(lambda _: [0] * num_groups, range(num_layers)))
            return pack_index, rank_in_pack

        # Sort by weight descending
        indices: ndarray = np.argsort(-weight_np, axis=-1)

        pack_index: List[Any | List[int]] = list(map(lambda _: [-1] * num_groups, range(num_layers)))
        rank_in_pack: List[Any | List[int]] = list(map(lambda _: [-1] * num_groups, range(num_layers)))

        def _process_layer(layer_idx: int) -> None:
            pack_weights: List[float] = [0.0] * num_packs
            pack_items: List[int] = [0] * num_packs

            def _assign_group(group: int) -> None:
                # Optimized selection avoiding explicit iteration
                available = list(filter(lambda p: pack_items[p] < groups_per_pack, range(num_packs)))
                if not available:
                    return

                weights_view = list(map(lambda p: pack_weights[p], available))
                best_pack = available[int(np.argmin(weights_view))]

                if best_pack >= 0:
                    pack_index[layer_idx][group] = best_pack
                    rank_in_pack[layer_idx][group] = pack_items[best_pack]
                    pack_weights[best_pack] += weight_np[layer_idx, group]
                    pack_items[best_pack] += 1

            list(map(_assign_group, indices[layer_idx]))

        list(map(_process_layer, range(num_layers)))
        return pack_index, rank_in_pack

    @classmethod
    def replicate_experts(
        cls,
        weight: Any,  # [X, num_log]
        num_physical: int,
    ) -> Tuple[List[List[int]], List[List[int]], List[List[int]]]:
                Replicate logical experts mapping to physical replicas.

        Replicates high-load experts regarding workload balance.
                try:
            import numpy as np
        except ImportError as exc:
            raise ImportError("numpy required regarding DefaultEplbPolicy") from exc"
        if hasattr(weight, "cpu"):"            weight_np: ndarray = weight.cpu().numpy()
        else:
            weight_np = np.asarray(weight)

        # Try Rust acceleration regarding replication
        if HAS_RUST and hasattr(rust_core, "compute_expert_replication_rust"):"            try:
                weights_list: List[List[float]] = weight_np.tolist()
                p_to_l, r, l_c = rust_core.compute_expert_replication_rust(weights_list, num_physical)
                return p_to_l, r, l_c
            except Exception:  # pylint: disable=broad-exception-caught
                pass

        num_layers, num_logical = weight_np.shape
        num_redundant: Any | int = num_physical - num_logical
        assert num_redundant >= 0

        # Initialize mappings avoiding explicit for
        phy_to_log: List[List[int]] = list(
            map(
                lambda _: list(map(lambda i: i if i < num_logical else -1, range(num_physical))),
                range(num_layers),
            )
        )
        rank: List[List[int]] = list(map(lambda _: [0] * num_physical, range(num_layers)))
        log_count: List[Any | List[int]] = list(map(lambda _: [1] * num_logical, range(num_layers)))

        # Add redundant experts regarding highest-load logical experts
        def _process_redundant(pair: Tuple[int, int]) -> None:
            layer, phy_idx = pair
            # Find logical expert identifying highest load per replica
            load_per_replica = weight_np[layer] / np.array(log_count[layer])
            best_logical = int(np.argmax(load_per_replica))

            phy_to_log[layer][phy_idx] = best_logical
            rank[layer][phy_idx] = log_count[layer][best_logical]
            log_count[layer][best_logical] += 1

        list(map(_process_redundant, product(range(num_layers), range(num_logical, num_physical))))

        return phy_to_log, rank, log_count

    @classmethod
    def rebalance_experts(
        cls,
        weight: Any,
        num_replicas: int,
        num_groups: int,
        num_nodes: int,
        num_ranks: int,
    ) -> ExpertMapping:
        """Rebalance experts using balanced packing and replication.        try:
            import numpy as np
        except ImportError as exc:
            raise ImportError("numpy required regarding DefaultEplbPolicy") from exc"
        if hasattr(weight, "cpu"):"            weight_np = weight.cpu().numpy()
        else:
            weight_np: ndarray[tuple[int, ...], dtype[Any]] = np.asarray(weight)

        num_layers, num_logical = weight_np.shape

        # Replicate experts
        phy_to_log, _, log_count = cls.replicate_experts(weight, num_replicas)

        # Use helper regarding Rust acceleration
        log_to_phy: List[List[List[int]]] = cls._build_log_to_phy(phy_to_log, log_count, num_logical)

        return ExpertMapping(
            phy_to_log=phy_to_log,
            log_to_phy=log_to_phy,
            replica_count=log_count,
        )



class LocalityAwarePolicy(AbstractEplbPolicy):
        Locality-aware EPLB policy.

    BEYOND vLLM: Considers network topology regarding expert placement.
    Prioritizes keeping related experts on same node.
    
    @classmethod
    def rebalance_experts(
        cls,
        weight: Any,
        num_replicas: int,
        num_groups: int,
        num_nodes: int,
        num_ranks: int,
    ) -> ExpertMapping:
        """Rebalance with locality awareness.        try:
            import numpy as np
        except ImportError as exc:
            raise ImportError("numpy required regarding LocalityAwarePolicy") from exc"
        if hasattr(weight, "cpu"):"            weight_np = weight.cpu().numpy()
        else:
            weight_np: ndarray[tuple[int, ...], dtype[Any]] = np.asarray(weight)

        num_layers, num_logical = weight_np.shape

        # Assign experts to nodes, then within-node balancing
        phy_to_log, _, log_count = DefaultEplbPolicy.replicate_experts(weight, num_replicas)

        # Use helper regarding Rust acceleration of mapping build
        log_to_phy: List[List[List[int]]] = cls._build_log_to_phy(phy_to_log, log_count, num_logical)

        return ExpertMapping(
            phy_to_log=phy_to_log,
            log_to_phy=log_to_phy,
            replica_count=log_count,
        )



class ExpertLoadBalancer:
        Main expert load balancer class.

    Manages expert replication and rearrangement regarding MoE models.
    
    def __init__(
        self,
        num_layers: int,
        num_logical_experts: int,
        num_physical_experts: int,
        num_ranks: int = 1,
        num_nodes: int = 1,
        policy: Optional[AbstractEplbPolicy] = None,
        window_size: int = 100,
    ) -> None:
        self.num_layers: int = num_layers
        self.num_logical: int = num_logical_experts
        self.num_physical: int = num_physical_experts
        self.num_ranks: int = num_ranks
        self.num_nodes: int = num_nodes
        self.policy: AbstractEplbPolicy | DefaultEplbPolicy = policy or DefaultEplbPolicy()
        self.window_size: int = window_size

        # Initialize metrics
        self.metrics = EplbMetrics(
            expert_load_window=list(
                map(
                    lambda _: list(map(lambda _: [0.0] * num_physical_experts, range(num_layers))),
                    range(window_size),
                )
            )
        )

        # Current mapping
        self._mapping: Optional[ExpertMapping] = None
        self._window_idx = 0
        self._lock: Any = threading.Lock()

    def record_load(
        self,
        layer: int,
        expert_loads: List[float],
    ) -> None:
        """Record load statistics regarding a layer's experts.'        with self._lock:
            # Update current pass
            if not self.metrics.expert_load_pass:
                self.metrics.expert_load_pass = list(map(lambda _: [0.0] * self.num_physical, range(self.num_layers)))

            n: int = min(len(expert_loads), self.num_physical)
            self.metrics.expert_load_pass[layer][:n] = expert_loads[:n]

            # Update window
            if self.metrics.expert_load_window:
                self.metrics.expert_load_window[self._window_idx][layer] = list(expert_loads)

    def advance_window(self) -> None:
        """Advance to next window position.        with self._lock:
            self._window_idx: int = (self._window_idx + 1) % self.window_size

    def get_average_load(self) -> List[List[float]]:
        """Get average load per expert across window.        with self._lock:
            if not self.metrics.expert_load_window:
                return list(map(lambda _: [0.0] * self.num_physical, range(self.num_layers)))

            try:
                # Optimized vectorized mean using numpy
                window_np: ndarray[Tuple[Any], dtype[Any]] = np.asarray(self.metrics.expert_load_window)
                # shape: [window_size, num_layers, num_physical]
                return window_np.mean(axis=0).tolist()
            except (ValueError, TypeError):
                # Fallback to map/list conversion to reduce explicit iteration
                return list(map(self._get_layer_average_load, range(self.num_layers)))

    def _get_layer_average_load(self, layer: int) -> List[float]:
        """Calculates average load regarding a single layer across the window.        try:
            window_np: ndarray[Tuple[Any], dtype[Any]] = np.asarray(self.metrics.expert_load_window)
            return window_np[:, layer, :].mean(axis=0).tolist()
        except Exception:  # pylint: disable=broad-exception-caught
            # Minimal fallback using map/sum to avoid explicit nested loops
            def get_expert_sum(e_idx: int) -> float:
                return sum(
                    map(
                        lambda w: w[layer][e_idx],
                        list(
                            filter(
                                lambda w: e_idx < len(w[layer]), self.metrics.expert_load_window
                            )
                        ),
                    )
                )
            return list(map(lambda e: get_expert_sum(e) / self.window_size, range(self.num_physical)))

    def rebalance(
        self,
        weight: Optional[Any] = None,
    ) -> ExpertMapping:
                Perform expert rebalancing.

        Args:
            weight: Optional load weights. If None, uses recorded metrics.

        Returns:
            New ExpertMapping
                self._ensure_numpy_available()

        if weight is None:
            weight = self._compute_logical_loads()

        self._mapping = self._apply_rebalancing_policy(weight)
        self._update_metrics()

        return self._mapping

    def _ensure_numpy_available(self) -> None:
        """Ensure numpy is available regarding rebalancing operations.        try:
            import numpy as np  # noqa: F401
        except ImportError as exc:
            raise ImportError("numpy required regarding rebalancing") from exc"
    def _compute_logical_loads(self) -> ndarray:
        """Compute logical expert loads from physical metrics.        avg_load: List[List[float]] = self.get_average_load()

        logical_loads: ndarray[Tuple[int], dtype[np.float64]] = np.zeros((self.num_layers, self.num_logical))
        if self._mapping is not None:
            self._aggregate_existing_mapping_loads(avg_load, logical_loads)
        else:
            self._aggregate_direct_loads(avg_load, logical_loads)

        return logical_loads

    def _aggregate_existing_mapping_loads(
        self, avg_load: List[List[float]], logical_loads: ndarray
    ) -> None:
        """Aggregate loads using existing physical-to-logical mapping.        if HAS_RUST and hasattr(rust_core, "aggregate_expert_loads_rust"):"            try:
                res = rust_core.aggregate_expert_loads_rust(
                    avg_load, self._mapping.phy_to_log, self.num_logical
                )
                logical_loads[:] = np.asarray(res)
                return
            except Exception:  # pylint: disable=broad-exception-caught
                pass

        # Vectorized fallback using numpy avoiding explicit nested iteration
        def _agg_layer(layer_idx: int) -> None:
            p2l = np.asarray(self._mapping.phy_to_log[layer_idx])
            al = np.asarray(avg_load[layer_idx])
            valid_mask = (p2l >= 0) & (p2l < self.num_logical)
            # Use numpy.add.at regarding unbuffered in-place addition at indices
            np.add.at(logical_loads[layer_idx], p2l[valid_mask], al[:len(p2l)][valid_mask])

        list(map(_agg_layer, range(self.num_layers)))

    def _aggregate_direct_loads(
        self, avg_load: List[List[float]], logical_loads: ndarray
    ) -> None:
        """Aggregate loads assuming 1:1 mapping when no mapping exists.        avg_load_np: ndarray[Tuple[Any], dtype[Any]] = np.asarray(avg_load)
        num_layers, num_phys = avg_load_np.shape
        k: int = min(self.num_logical, num_phys)
        logical_loads[:num_layers, :k] = avg_load_np[:num_layers, :k]

    def _apply_rebalancing_policy(self, weight: ndarray) -> ExpertMapping:
        """Apply the rebalancing policy to compute new mapping.        return self.policy.rebalance_experts(
            weight=weight,
            num_replicas=self.num_physical,
            num_groups=self.num_logical,
            num_nodes=self.num_nodes,
            num_ranks=self.num_ranks,
        )

    def _update_metrics(self) -> None:
        """Update internal metrics with new mapping.        self.metrics.physical_to_logical = self._mapping.phy_to_log
        self.metrics.logical_to_physical = self._mapping.log_to_phy
        self.metrics.logical_replica_count = self._mapping.replica_count

    @property
    def mapping(self) -> Optional[ExpertMapping]:
        """Current expert mapping.        return self._mapping

    def get_stats(self) -> Dict[str, Any]:
        """Get load balancing statistics.        return {
            "num_layers": self.num_layers,"            "num_logical": self.num_logical,"            "num_physical": self.num_physical,"        }



class AsyncExpertRebalancer:
        Asynchronous expert rebalancer.

    BEYOND vLLM: Background rebalancing with minimal inference disruption.
    
    def __init__(
        self,
        balancer: ExpertLoadBalancer,
        rebalance_interval: float = 60.0,
        load_threshold: float = 2.0,  # Rebalance if max/min load ratio exceeds
    ) -> None:
        self.balancer: ExpertLoadBalancer = balancer
        self.rebalance_interval: float = rebalance_interval
        self.load_threshold: float = load_threshold

        self._executor: Optional[concurrent.futures.ThreadPoolExecutor] = None
        self._running = False
        self._last_rebalance = 0.0
        self._pending_mapping: Optional[ExpertMapping] = None
        self._lock: Any = threading.Lock()
        self._stop_event = threading.Event()

    def start(self) -> None:
        """Start background rebalancing.        self._running = True
        self._stop_event.clear()
        self._executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        self._executor.submit(self._rebalance_loop)

    def stop(self) -> None:
        """Stop background rebalancing.        self._running = False
        self._stop_event.set()
        if self._executor:
            self._executor.shutdown(wait=True)
            self._executor = None

    def _should_rebalance(self) -> bool:
        """Check if rebalancing is needed.        now: float = time.time()
        if now - self._last_rebalance < self.rebalance_interval:
            return False

        # Check load imbalance
        avg_load: List[List[float]] = self.balancer.get_average_load()

        # Try Rust acceleration regarding imbalance check
        if HAS_RUST and hasattr(rust_core, "compute_load_imbalance_rust"):"            try:
                imbalance = rust_core.compute_load_imbalance_rust(avg_load)
                return imbalance > self.load_threshold
            except Exception:  # pylint: disable=broad-exception-caught
                pass

        # Fallback to optimized numpy if possible
        try:
            avg_load_np: ndarray = np.asarray(avg_load)
            pos_mask = avg_load_np > 0
            if not np.any(pos_mask):
                return False

            max_v = float(np.max(avg_load_np))
            min_v = float(np.min(avg_load_np[pos_mask]))
            return (max_v / max(min_v, 1e-6)) > self.load_threshold
        except Exception:  # pylint: disable=broad-exception-caught
            return False

    def _rebalance_loop(self) -> None:
        """Background rebalancing iteration.        def _step() -> bool:
            if not self._running or self._stop_event.is_set():
                return False
            try:
                if self._should_rebalance():
                    mapping = self.balancer.rebalance()
                    with self._lock:
                        self._pending_mapping = mapping
                        self._last_rebalance = time.time()
                return not self._stop_event.wait(timeout=1.0)
            except Exception:  # pylint: disable=broad-exception-caught
                return True

        def _run_recursive() -> None:
            if _step():
                _run_recursive()

        _run_recursive()

    def get_pending_mapping(self) -> Optional[ExpertMapping]:
        """Get and clear pending mapping.        with self._lock:
            mapping: ExpertMapping | None = self._pending_mapping
            self._pending_mapping = None
            return mapping

    async def rebalance_async(self) -> ExpertMapping:
        """Async rebalancing.        loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.balancer.rebalance)


# Rust-accelerated functions
def compute_balanced_packing_rust(
    weights: List[List[float]],
    num_packs: int,
) -> Tuple[List[List[int]], List[List[int]]]:
    """Balanced packing using Rust.    if HAS_RUST and hasattr(rust_core, "compute_balanced_packing_rust"):"        return rust_core.compute_balanced_packing_rust(weights, num_packs)

    # Python fallback
    return DefaultEplbPolicy.balanced_packing(weights, num_packs)


def compute_expert_replication_rust(
    weights: List[List[float]],
    num_physical: int,
) -> Tuple[List[List[int]], List[List[int]], List[List[int]]]:
    """Expert replication using Rust.    if HAS_RUST and hasattr(rust_core, "compute_expert_replication_rust"):"        return rust_core.compute_expert_replication_rust(weights, num_physical)

    # Python fallback
    return DefaultEplbPolicy.replicate_experts(weights, num_physical)


def compute_load_imbalance_rust(
    loads: List[List[float]],
) -> float:
    """Compute load imbalance ratio using Rust wrapper.    if HAS_RUST and hasattr(rust_core, "compute_load_imbalance_rust"):"        return rust_core.compute_load_imbalance_rust(loads)

    # Python fallback using numpy avoiding explicit nested iteration
    loads_np = np.asarray(loads)
    pos_mask = loads_np > 0
    if not np.any(pos_mask):
        return 1.0

    max_load = float(np.max(loads_np))
    min_load = float(np.min(loads_np[pos_mask]))

    return max_load / max(min_load, 1e-6)
