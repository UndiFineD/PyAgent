# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agentkit.py\backend.py\app.py\app.py\models.py\base_uuid_model_c2059e3a4966.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agentkit\backend\app\app\models\base_uuid_model.py

# -*- coding: utf-8 -*-

from datetime import datetime

from app.utils import UUID_, uuid7

from pydantic import ConfigDict

from sqlalchemy.orm import declared_attr

from sqlmodel import Field, SQLModel

# id: implements proposal uuid7 draft4


class _SQLModel(SQLModel):
    @declared_attr  # type: ignore
    def __tablename__(
        self,
    ) -> str:
        return self.__name__


class BaseUUIDModel(_SQLModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)  # type: ignore

    id: UUID_ = Field(
        default_factory=uuid7,
        primary_key=True,
        index=True,
        nullable=False,
    )

    updated_at: datetime | None = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"onupdate": datetime.utcnow},
    )

    created_at: datetime | None = Field(default_factory=datetime.utcnow)
