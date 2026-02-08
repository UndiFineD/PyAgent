# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_evermemos.py\src.py\core.py\tenants.py\tenantize.py\kv.py\redis.py\tenant_key_utils_e8296b973124.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-EverMemOS\src\core\tenants\tenantize\kv\redis\tenant_key_utils.py

"""

Redis tenant key utility functions module

Provides tenant isolation for Redis key names by prepending the tenant ID to achieve multi-tenant data isolation.

"""

from typing import Optional

from core.tenants.tenant_contextvar import get_current_tenant_id


def patch_redis_tenant_key(key: str) -> str:
    """

    Add tenant prefix to Redis key name

    Retrieve the tenant ID from the current context and prepend it to the key to achieve multi-tenant data isolation.

    If no tenant information is set in the current context, return the original key.

    Format: {tenant_id}:{key}

    Args:

        key: Original Redis key name

    Returns:

        str: Redis key name with tenant prefix; if no tenant, return the original key

    Examples:

        >>> # Assume current tenant ID is "tenant_001"

        >>> patch_redis_tenant_key("conversation_data:group_123")

        'tenant_001:conversation_data:group_123'

        >>> # If no tenant is set

        >>> patch_redis_tenant_key("conversation_data:group_123")

        'conversation_data:group_123'

    """

    tenant_id: Optional[str] = get_current_tenant_id()

    if tenant_id:
        # When tenant ID exists, concatenate tenant prefix

        return f"{tenant_id}:{key}"

    # When no tenant ID exists, return the original key

    return key
