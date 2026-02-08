# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_evermemos.py\src.py\infra_layer.py\adapters.py\out.py\persistence.py\document.py\memory.py\entity_b58411cefdf0.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-EverMemOS\src\infra_layer\adapters\out\persistence\document\memory\entity.py

from datetime import datetime

from typing import Any, Dict, List, Optional

from beanie import PydanticObjectId

from pydantic import ConfigDict, Field

from pymongo import ASCENDING, DESCENDING, TEXT, IndexModel

from core.oxm.mongo.audit_base import AuditBase

from core.oxm.mongo.document_base import DocumentBase


class Entity(DocumentBase, AuditBase):
    """

    Entity document model

    Stores entity information extracted from episodic memory, including people, projects, organizations, etc.

    """

    # Basic information

    name: str = Field(..., description="Entity name")

    type: str = Field(..., description="Entity type (Project, Person, Organization, etc.)")

    aliases: Optional[List[str]] = Field(default=None, description="Associated aliases")

    # Common fields

    extend: Optional[Dict[str, Any]] = Field(default=None, description="Reserved extension field")

    model_config = ConfigDict(
        collection="entities",
        validate_assignment=True,
        json_encoders={datetime: lambda dt: dt.isoformat()},
        json_schema_extra={
            "example": {
                "name": "Zhang San",
                "type": "Person",
                "aliases": ["Xiao Zhang", "Engineer Zhang", "zhangsan"],
                "extend": {
                    "department": "Technology Department",
                    "level": "Senior Engineer",
                },
            }
        },
    )

    @property
    def entity_id(self) -> Optional[PydanticObjectId]:

        return self.id

    class Settings:
        """Beanie settings"""

        name = "entities"

        indexes = [
            # Note: entity_id maps to the _id field, MongoDB automatically creates a primary key index on _id
            IndexModel([("aliases", ASCENDING)], name="idx_aliases", sparse=True),
            IndexModel([("created_at", DESCENDING)], name="idx_created_at"),
            IndexModel([("updated_at", DESCENDING)], name="idx_updated_at"),
        ]

        validate_on_save = True

        use_state_management = True
