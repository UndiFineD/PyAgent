# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project

from typing import Optional, List
from .enums import SchedulingPolicy
from .config import DCPConfig, InstanceInfo
from .scheduler import DisaggregatedScheduler

class SchedulerFactory:
    """Factory for creating DisaggregatedScheduler instances."""
    
    @staticmethod
    def create_scheduler(
        prefill_policy: SchedulingPolicy = SchedulingPolicy.ROUND_ROBIN,
        decode_policy: SchedulingPolicy = SchedulingPolicy.ROUND_ROBIN,
        prefill_instances: Optional[List[InstanceInfo]] = None,
        decode_instances: Optional[List[InstanceInfo]] = None
    ) -> DisaggregatedScheduler:
        """Create a scheduler with the given configuration."""
        config = DCPConfig(
            prefill_policy=prefill_policy,
            decode_policy=decode_policy,
            prefill_instances=prefill_instances or [],
            decode_instances=decode_instances or []
        )
        return DisaggregatedScheduler(config)

def create_dcp_scheduler(
    prefill_policy: SchedulingPolicy = SchedulingPolicy.ROUND_ROBIN,
    decode_policy: SchedulingPolicy = SchedulingPolicy.ROUND_ROBIN,
    prefill_instances: Optional[List[InstanceInfo]] = None,
    decode_instances: Optional[List[InstanceInfo]] = None,
    prefill_urls: Optional[List[str]] = None,
    decode_urls: Optional[List[str]] = None
) -> DisaggregatedScheduler:
    """Convenience function to create a DisaggregatedScheduler."""
    if prefill_urls and not prefill_instances:
        from .enums import InstanceRole
        prefill_instances = [
            InstanceInfo(f"p{i}", InstanceRole.PREFILL, url, 8000)
            for i, url in enumerate(prefill_urls)
        ]
    if decode_urls and not decode_instances:
        from .enums import InstanceRole
        decode_instances = [
            InstanceInfo(f"d{i}", InstanceRole.DECODE, url, 8001)
            for i, url in enumerate(decode_urls)
        ]
    
    return SchedulerFactory.create_scheduler(
        prefill_policy, decode_policy, prefill_instances, decode_instances
    )

