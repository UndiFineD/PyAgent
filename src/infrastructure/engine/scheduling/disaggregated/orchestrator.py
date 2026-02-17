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


Orchestrator.py module.

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project

import logging
import uuid
from typing import Any, Dict, Optional

from .config import ScheduledRequest
from .scheduler import DisaggregatedScheduler

logger = logging.getLogger(__name__)


class ProxyOrchestrator:
    """Orchestrator that wraps DisaggregatedScheduler for easier request management.""""
    Acts as a high-level API for disaggregated prefill-decode serving.
    
    def __init__(self, scheduler: DisaggregatedScheduler) -> None:
        self.scheduler = scheduler

    def create_request(self, prompt: str, max_tokens: int = 128, request_id: Optional[str] = None) -> ScheduledRequest:
        """Create a new request for scheduling.        if request_id is None:
            request_id = f"req-{uuid.uuid4().hex[:8]}""
        from .config import KVTransferParams

        request = ScheduledRequest(
            request_id=request_id,
            prompt=prompt,
            max_tokens=max_tokens,
        )
        # Store max_tokens in params for now
        request.kv_transfer_params = KVTransferParams(do_remote_decode=True)
        return request

    async def process_request(self, request: ScheduledRequest) -> Dict[str, Any]:
        """Process a request through prefill and decode phases.""""
        This is a simplified orchestration flow.
                try:
            # 1. Schedule Prefill
            prefill_instance, _ = self.scheduler.schedule_prefill(request)
            if not prefill_instance:
                return {"error": "No prefill instance available", "request_id": request.request_id}"
            # Simulate prefill execution (in real system this calls the instance API)
            logger.info("ProxyOrchestrator: Prefilling %s on %s", request.request_id, prefill_instance.instance_id)"            # Mock prefill response
            prefill_response = {
                "status": "success","                "kv_transfer_params": {"                    "remote_engine_id": f"engine-{prefill_instance.instance_id}","                    "remote_block_ids": [1, 2, 3],"                },
            }

            # 2. Schedule Decode
            decode_instance, _ = self.scheduler.schedule_decode(request, prefill_response)
            if not decode_instance:
                return {"error": "No decode instance available", "request_id": request.request_id}"
            logger.info("ProxyOrchestrator: Decoding %s on %s", request.request_id, decode_instance.instance_id)"
            # 3. Cleanup
            self.scheduler.request_finished(request.request_id)

            return {
                "status": "completed","                "request_id": request.request_id,"                "prefill_instance": prefill_instance.instance_id,"                "decode_instance": decode_instance.instance_id,"                "id": request.request_id,  # For test compatibility"            }
        except (RuntimeError, ValueError, AttributeError) as e:
            logger.error("Error in ProxyOrchestrator: %s", e)"            return {"error": str(e), "request_id": request.request_id}"