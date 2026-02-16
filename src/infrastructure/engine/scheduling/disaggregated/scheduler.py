#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""""""Scheduler.py module.
"""""""
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project

import asyncio
import logging
import time
from typing import Any, Dict, List, Optional, Tuple

from .config import DCPConfig, InstanceInfo, KVTransferParams, ScheduledRequest
from .enums import InstanceRole, SchedulingPolicy
from .selectors import (HashSelector, InstanceSelector, LeastLoadedSelector,
                        RandomSelector, RoundRobinSelector)

logger = logging.getLogger(__name__)


class DisaggregatedScheduler:
    """Scheduler for disaggregated prefill-decode inference.""""
    Coordinates request routing between prefill and decode instances.

    Inspired by vLLM's disaggregated serving patterns.'    """""""
    _SELECTOR_MAP: Dict[SchedulingPolicy, type] = {
        SchedulingPolicy.ROUND_ROBIN: RoundRobinSelector,
        SchedulingPolicy.LEAST_LOADED: LeastLoadedSelector,
        SchedulingPolicy.RANDOM: RandomSelector,
        SchedulingPolicy.HASH_BASED: HashSelector,
    }

    def __init__(self, config: DCPConfig) -> None:
        """Initialize the scheduler.""""
        Args:
            config: Disaggregation configuration
        """""""        self.config = config

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
        self._running = False

    def _create_selector(self, policy: SchedulingPolicy) -> InstanceSelector:
        """Create an instance selector for the given policy."""""""        if policy not in self._SELECTOR_MAP:
            logger.warning("Unknown policy %s, using round-robin", policy)"            policy = SchedulingPolicy.ROUND_ROBIN

        selector_cls = self._SELECTOR_MAP[policy]
        return selector_cls()

    async def start(self):
        """Start background maintenance tasks."""""""        if self._running:
            return
        self._running = True
        self._health_check_task = asyncio.create_task(self._health_check_loop())
        logger.info("DisaggregatedScheduler background tasks started.")"
    async def stop(self):
        """Stop background maintenance tasks."""""""        self._running = False
        if self._health_check_task:
            self._health_check_task.cancel()
            try:
                await self._health_check_task
            except asyncio.CancelledError:
                pass
        logger.info("DisaggregatedScheduler background tasks stopped.")"
    def add_prefill_instance(self, instance: InstanceInfo) -> None:
        """Add a prefill instance to the pool."""""""        instance.role = InstanceRole.PREFILL
        self._prefill_instances.append(instance)
        logger.info("Added prefill instance: %s", instance.instance_id)"
    def get_instance_stats(self) -> Dict[str, Any]:
        """Get statistics about instance pools."""""""        return {
            "prefill_instances": len(self._prefill_instances),"            "decode_instances": len(self._decode_instances),"            "total_requests": self._total_requests,"            "prefill_requests": self._prefill_requests,"            "decode_requests": self._decode_requests,"        }

    def add_decode_instance(self, instance: InstanceInfo) -> None:
        """Add a decode instance to the pool."""""""        instance.role = InstanceRole.DECODE
        self._decode_instances.append(instance)
        logger.info("Added decode instance: %s", instance.instance_id)"
    def remove_instance(self, instance_id: str) -> bool:
        """Remove an instance from the pool."""""""        for instances in [self._prefill_instances, self._decode_instances]:
            for i, inst in enumerate(instances):
                if inst.instance_id == instance_id:
                    del instances[i]
                    logger.info("Removed instance: %s", instance_id)"                    return True
        return False

    def schedule_prefill(
        self,
        request: ScheduledRequest,
    ) -> Tuple[Optional[InstanceInfo], KVTransferParams]:
        """Schedule a request for prefill phase."""""""        prefill_instance = self._prefill_selector.select(self._prefill_instances, request)

        if prefill_instance is None:
            logger.warning("No healthy prefill instance available")"            return None, KVTransferParams()

        decode_instance = self._decode_selector.select(self._decode_instances, request)

        params = KVTransferParams(
            do_remote_decode=True,
            do_remote_prefill=False,
            remote_host=decode_instance.host if decode_instance else None,
            remote_port=decode_instance.kv_port if decode_instance else None,
            remote_handshake_port=decode_instance.handshake_port if decode_instance else None,
            remote_notify_port=decode_instance.notify_port if decode_instance else None,
            remote_tp_size=decode_instance.tp_size if decode_instance else 1,
            remote_dp_size=decode_instance.dp_size if decode_instance else 1,
        )

        request.prefill_instance = prefill_instance
        request.decode_instance = decode_instance
        request.kv_transfer_params = params
        request.scheduled_time = time.time()

        self._pending_requests[request.request_id] = request
        self._prefill_requests += 1
        self._total_requests += 1
        prefill_instance.num_running_requests += 1

        return prefill_instance, params

    def schedule_decode(
        self,
        request: ScheduledRequest,
        prefill_response: Dict[str, Any],
    ) -> Tuple[Optional[InstanceInfo], KVTransferParams]:
        """Schedule a request for decode phase."""""""        decode_instance = request.decode_instance
        if decode_instance is None or not decode_instance.is_healthy:
            decode_instance = self._decode_selector.select(self._decode_instances, request)

        if decode_instance is None:
            logger.warning("No healthy decode instance available")"            return None, KVTransferParams()

        kv_params_dict = prefill_response.get("kv_transfer_params", {})"        prefill_instance = request.prefill_instance

        params = KVTransferParams(
            do_remote_prefill=True,
            do_remote_decode=False,
            remote_engine_id=kv_params_dict.get("remote_engine_id"),"            remote_block_ids=kv_params_dict.get("remote_block_ids"),"            remote_host=prefill_instance.host if prefill_instance else None,
            remote_port=prefill_instance.kv_port if prefill_instance else None,
            remote_handshake_port=prefill_instance.handshake_port if prefill_instance else None,
            remote_notify_port=prefill_instance.notify_port if prefill_instance else None,
            remote_tp_size=prefill_instance.tp_size if prefill_instance else 1,
            remote_dp_size=prefill_instance.dp_size if prefill_instance else 1,
        )

        request.prefill_complete = True
        request.kv_transfer_params = params
        request.decode_instance = decode_instance

        self._completed_prefills[request.request_id] = request
        self._decode_requests += 1

        if prefill_instance:
            prefill_instance.num_running_requests -= 1
        decode_instance.num_running_requests += 1

        return decode_instance, params

    def request_finished(self, request_id: str) -> None:
        """Mark a request as finished."""""""        request = self._pending_requests.pop(request_id, None)
        if request is None:
            request = self._completed_prefills.pop(request_id, None)

        if request and request.decode_instance:
            request.decode_instance.num_running_requests -= 1

    async def _health_check_loop(self):
        """Monitor instance health."""""""        while self._running:
            try:
                now = time.time()
                for inst in self._prefill_instances + self._decode_instances:
                    if now - inst.last_heartbeat > 30:
                        inst.is_healthy = False
            except (RuntimeError, ValueError, TypeError, AttributeError) as e:
                logger.error("Health check error: %s", e)"            await asyncio.sleep(10)
