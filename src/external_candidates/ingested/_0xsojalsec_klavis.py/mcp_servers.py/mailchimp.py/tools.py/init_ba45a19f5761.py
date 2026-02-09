# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-klavis\mcp_servers\mailchimp\tools\__init__.py
from .audiences import (
    create_audience,
    delete_audience,
    get_all_audiences,
    get_audience_info,
    update_audience,
)
from .auth import get_account_info, ping_mailchimp
from .base import mailchimp_token_context
from .campaigns import (
    create_campaign,
    delete_campaign,
    get_all_campaigns,
    get_campaign_info,
    schedule_campaign,
    send_campaign,
    set_campaign_content,
)
from .members import (
    add_member_tags,
    add_member_to_audience,
    delete_member,
    get_audience_members,
    get_member_activity,
    get_member_info,
    remove_member_tags,
    update_member,
)

__all__ = [
    # Auth/Account
    "ping_mailchimp",
    "get_account_info",
    # Audiences/Lists
    "get_all_audiences",
    "create_audience",
    "get_audience_info",
    "update_audience",
    "delete_audience",
    # Members/Contacts
    "get_audience_members",
    "add_member_to_audience",
    "get_member_info",
    "update_member",
    "delete_member",
    "add_member_tags",
    "remove_member_tags",
    "get_member_activity",
    # Campaigns
    "get_all_campaigns",
    "create_campaign",
    "get_campaign_info",
    "set_campaign_content",
    "send_campaign",
    "schedule_campaign",
    "delete_campaign",
    # Base
    "mailchimp_token_context",
]
