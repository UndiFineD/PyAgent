# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-klavis\mcp_servers\salesforce\tools\__init__.py
# Salesforce MCP Server Tools
# This package contains all the tool implementations organized by object type

from .accounts import create_account, delete_account, get_accounts, update_account
from .base import access_token_context, instance_url_context
from .campaigns import create_campaign, delete_campaign, get_campaigns, update_campaign
from .cases import create_case, delete_case, get_cases, update_case
from .contacts import create_contact, delete_contact, get_contacts, update_contact
from .leads import convert_lead, create_lead, delete_lead, get_leads, update_lead
from .metadata import describe_object, execute_soql_query
from .opportunities import (
    create_opportunity,
    delete_opportunity,
    get_opportunities,
    update_opportunity,
)

__all__ = [
    # Accounts
    "get_accounts",
    "create_account",
    "update_account",
    "delete_account",
    # Contacts
    "get_contacts",
    "create_contact",
    "update_contact",
    "delete_contact",
    # Opportunities
    "get_opportunities",
    "create_opportunity",
    "update_opportunity",
    "delete_opportunity",
    # Leads
    "get_leads",
    "create_lead",
    "update_lead",
    "delete_lead",
    "convert_lead",
    # Cases
    "get_cases",
    "create_case",
    "update_case",
    "delete_case",
    # Campaigns
    "get_campaigns",
    "create_campaign",
    "update_campaign",
    "delete_campaign",
    # Metadata & Queries
    "describe_object",
    "execute_soql_query",
    # Base
    "access_token_context",
    "instance_url_context",
]
