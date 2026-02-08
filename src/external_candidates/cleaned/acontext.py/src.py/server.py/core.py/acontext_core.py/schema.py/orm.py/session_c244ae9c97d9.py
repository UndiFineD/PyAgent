# Extracted from: C:\DEV\PyAgent\.external\Acontext\src\server\core\acontext_core\schema\orm\session.py
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Column, ForeignKey, Index
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from ..utils import asUUID
from .base import ORM_BASE, CommonMixin

if TYPE_CHECKING:
    from .message import Message
    from .project import Project
    from .space import Space
    from .task import Task


@ORM_BASE.mapped
@dataclass
class Session(CommonMixin):
    __tablename__ = "sessions"

    __table_args__ = (
        Index("ix_session_project_id", "project_id"),
        Index("ix_session_space_id", "space_id"),
        Index("ix_session_session_project_id", "id", "project_id"),
    )

    project_id: asUUID = field(
        metadata={
            "db": Column(
                UUID(as_uuid=True),
                ForeignKey("projects.id", ondelete="CASCADE"),
                nullable=False,
            )
        }
    )

    space_id: Optional[asUUID] = field(
        default=None,
        metadata={
            "db": Column(
                UUID(as_uuid=True),
                ForeignKey("spaces.id", ondelete="SET NULL"),
                nullable=True,
            )
        },
    )

    configs: Optional[dict] = field(default=None, metadata={"db": Column(JSONB, nullable=True)})

    # Relationships
    project: "Project" = field(init=False, metadata={"db": relationship("Project", back_populates="sessions")})

    space: Optional["Space"] = field(
        default=None,
        init=False,
        metadata={"db": relationship("Space", back_populates="sessions")},
    )

    messages: List["Message"] = field(
        default_factory=list,
        metadata={"db": relationship("Message", back_populates="session", cascade="all, delete-orphan")},
    )

    tasks: List["Task"] = field(
        default_factory=list,
        metadata={"db": relationship("Task", back_populates="session", cascade="all, delete-orphan")},
    )
