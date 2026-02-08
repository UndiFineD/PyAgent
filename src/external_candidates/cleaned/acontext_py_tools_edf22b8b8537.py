# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\acontext.py\src.py\client.py\acontext_py.py\src.py\acontext.py\resources.py\tools_edf22b8b8537.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\Acontext\src\client\acontext-py\src\acontext\resources\tools.py

"""Tool endpoints."""

from ..client_types import RequesterProtocol

from ..types.tool import FlagResponse, ToolReferenceData


class ToolsAPI:
    def __init__(self, requester: RequesterProtocol) -> None:

        self._requester = requester

    def rename_tool_name(self, *, rename: list[dict[str, str]]) -> FlagResponse:
        """Rename tool names within a project.

        Args:

            rename: List of dictionaries with old_name and new_name keys.

        Returns:

            FlagResponse containing status and errmsg fields.

        """

        payload = {"rename": rename}

        data = self._requester.request("PUT", "/tool/name", json_data=payload)

        return FlagResponse.model_validate(data)

    def get_tool_name(self) -> list[ToolReferenceData]:
        """Get all tool names within a project.

        Returns:

            List of ToolReferenceData objects.

        """

        data = self._requester.request("GET", "/tool/name")

        return [ToolReferenceData.model_validate(item) for item in data]
