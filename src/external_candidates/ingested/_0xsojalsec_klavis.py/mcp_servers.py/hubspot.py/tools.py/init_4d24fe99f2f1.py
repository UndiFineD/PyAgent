# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-klavis\mcp_servers\hubspot\tools\__init__.py
from .base import (
    auth_token_context,
)
from .companies import (
    hubspot_create_companies,
    hubspot_delete_company_by_id,
    hubspot_get_companies,
    hubspot_get_company_by_id,
    hubspot_update_company_by_id,
)
from .contacts import (
    hubspot_create_contact,
    hubspot_delete_contact_by_id,
    hubspot_get_contact_by_id,
    hubspot_get_contacts,
    hubspot_update_contact_by_id,
)
from .deals import (
    hubspot_create_deal,
    hubspot_delete_deal_by_id,
    hubspot_get_deal_by_id,
    hubspot_get_deals,
    hubspot_update_deal_by_id,
)
from .notes import (
    hubspot_create_note,
)
from .properties import (
    hubspot_create_property,
    hubspot_list_properties,
    hubspot_search_by_property,
)
from .tasks import (
    hubspot_create_task,
    hubspot_delete_task_by_id,
    hubspot_get_task_by_id,
    hubspot_get_tasks,
    hubspot_update_task_by_id,
)
from .tickets import (
    hubspot_create_ticket,
    hubspot_delete_ticket_by_id,
    hubspot_get_ticket_by_id,
    hubspot_get_tickets,
    hubspot_update_ticket_by_id,
)

__all__ = [
    # Base
    "auth_token_context",
    # Properties
    "hubspot_list_properties",
    "hubspot_search_by_property",
    "hubspot_create_property",
    # Contacts
    "hubspot_get_contacts",
    "hubspot_get_contact_by_id",
    "hubspot_delete_contact_by_id",
    "hubspot_create_contact",
    "hubspot_update_contact_by_id",
    # Companies
    "hubspot_get_companies",
    "hubspot_get_company_by_id",
    "hubspot_create_companies",
    "hubspot_update_company_by_id",
    "hubspot_delete_company_by_id",
    # Deals
    "hubspot_get_deals",
    "hubspot_get_deal_by_id",
    "hubspot_create_deal",
    "hubspot_update_deal_by_id",
    "hubspot_delete_deal_by_id",
    # Tickets
    "hubspot_get_tickets",
    "hubspot_get_ticket_by_id",
    "hubspot_create_ticket",
    "hubspot_update_ticket_by_id",
    "hubspot_delete_ticket_by_id",
    # Notes
    "hubspot_create_note",
    # Tasks
    "hubspot_get_tasks",
    "hubspot_get_task_by_id",
    "hubspot_create_task",
    "hubspot_update_task_by_id",
    "hubspot_delete_task_by_id",
]
