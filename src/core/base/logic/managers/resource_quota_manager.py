<<<<<<< HEAD
#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

=======
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
"""
Manager for Resource Quotas and budget enforcement.
(Facade for src.core.base.common.resource_core)
"""
<<<<<<< HEAD

from src.core.base.common.resource_core import \
    QuotaConfig, ResourceCore as StandardResourceQuotaManager
=======
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)

from src.core.base.common.resource_core import (
    ResourceCore as StandardResourceQuotaManager,
    QuotaConfig,
    ResourceUsage
)

class ResourceQuotaManager(StandardResourceQuotaManager):
<<<<<<< HEAD
    """
    Facade for ResourceCore to maintain backward compatibility.
    Resource enforcement logic is now centralized in the Infrastructure/Common tier.
    """


__all__ = ["QuotaConfig", "ResourceQuotaManager"]
=======
    """
    Facade for ResourceCore to maintain backward compatibility.
    Resource enforcement logic is now centralized in the Infrastructure/Common tier.
    """
    pass
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
