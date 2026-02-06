# Extracted from: C:\DEV\PyAgent\.external\Acontext\src\server\core\acontext_core\schema\orm\tool_reference.py
from dataclasses import dataclass, field
from optparse import Option
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Column, ForeignKey, Index, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from ..utils import asUUID
from .base import ORM_BASE, CommonMixin

if TYPE_CHECKING:
    from .message import Message
    from .project import Project
    from .space import Space
    from .task import Task
    from .tool_sop import ToolSOP


@ORM_BASE.mapped
@dataclass
class ToolReference(CommonMixin):
    __tablename__ = "tool_references"

    __table_args__ = (
        Index("ix_tool_reference_project_id", "project_id"),
        Index("ix_tool_reference_project_id_name", "project_id", "name"),
    )

    name: str = field(metadata={"db": Column(String, nullable=False)})

    project_id: asUUID = field(
        metadata={
            "db": Column(
                UUID(as_uuid=True),
                ForeignKey("projects.id", ondelete="CASCADE"),
                nullable=False,
            )
        }
    )

    description: Optional[str] = field(
        default=None, metadata={"db": Column(String, nullable=True)}
    )
    arguments_schema: Optional[dict] = field(
        default=None, metadata={"db": Column(JSONB, nullable=True)}
    )

    # Relationships
    project: "Project" = field(
        init=False,
        metadata={"db": relationship("Project", back_populates="tool_references")},
    )

    tool_sops: List["ToolSOP"] = field(
        default_factory=list,
        metadata={
            "db": relationship(
                "ToolSOP", back_populates="tool_reference", cascade="all, delete-orphan"
            )
        },
    )
