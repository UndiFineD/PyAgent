# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-klavis\mcp_servers\notion\tools\comments.py
from typing import Any, Dict, List, Optional

from .base import clean_notion_response, get_notion_client, handle_notion_error


async def create_comment(
    parent: Dict[str, Any],
    rich_text: List[Dict[str, Any]],
    discussion_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Create a comment on a page or discussion."""
    try:
        notion = get_notion_client()

        comment_data = {"rich_text": rich_text}

        if discussion_id:
            comment_data["discussion_id"] = discussion_id
        else:
            comment_data["parent"] = parent

        response = notion.comments.create(**comment_data)
        return clean_notion_response(response)

    except Exception as e:
        return handle_notion_error(e)


async def get_comments(
    block_id: str, start_cursor: Optional[str] = None, page_size: Optional[int] = None
) -> Dict[str, Any]:
    """Retrieve comments from a page or block."""
    try:
        notion = get_notion_client()

        params = {"block_id": block_id}
        if start_cursor:
            params["start_cursor"] = start_cursor
        if page_size:
            params["page_size"] = page_size

        response = notion.comments.list(**params)
        return clean_notion_response(response)

    except Exception as e:
        return handle_notion_error(e)
