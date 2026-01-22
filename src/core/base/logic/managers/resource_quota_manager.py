"""
Manager for Resource Quotas and budget enforcement.
(Facade for src.core.base.common.resource_core)
"""

from src.core.base.common.resource_core import (
    ResourceCore as StandardResourceQuotaManager,
    QuotaConfig,
    ResourceUsage
)

class ResourceQuotaManager(StandardResourceQuotaManager):
    """
    Facade for ResourceCore to maintain backward compatibility.
    Resource enforcement logic is now centralized in the Infrastructure/Common tier.
    """
    pass
