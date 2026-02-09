# Extracted from: C:\DEV\PyAgent\.external\agno\libs\agno\agno\infra\context.py
from typing import Optional

from agno.api.schemas.workspace import WorkspaceSchema
from pydantic import BaseModel


class ContainerContext(BaseModel):
    """ContainerContext is a context object passed when creating containers."""

    # Workspace name
    workspace_name: str
    # Workspace schema from the API
    workspace_schema: Optional[WorkspaceSchema] = None
    # Path to the workspace directory inside the container
    workspace_root: str
    # Path to the workspace parent directory inside the container
    workspace_parent: str
    # Path to the requirements.txt file relative to the workspace_root
    requirements_file: Optional[str] = None
