# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-klavis\mcp_servers\freshdesk\tools\accounts.py
import logging
from typing import Any, Dict, List, Optional

from .base import handle_freshdesk_error, make_freshdesk_request, remove_none_values

logger = logging.getLogger(__name__)


async def get_current_account() -> Dict[str, Any]:
    """
    Retrieve the current account.

    Returns:
        Dict containing the account data or error information
    """
    try:
        return await make_freshdesk_request("GET", "/account")
    except Exception as e:
        return handle_freshdesk_error(e, "retrieve", "current account")
