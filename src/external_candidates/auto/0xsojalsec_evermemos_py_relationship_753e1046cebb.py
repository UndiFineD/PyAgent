# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_evermemos.py\src.py\infra_layer.py\adapters.py\out.py\persistence.py\document.py\memory.py\relationship_753e1046cebb.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-EverMemOS\src\infra_layer\adapters\out\persistence\document\memory\relationship.py

from datetime import datetime

from typing import Any, Dict, List, Optional

from beanie import Indexed

from pydantic import ConfigDict, Field

from pymongo import ASCENDING, DESCENDING, IndexModel

from core.oxm.mongo.audit_base import AuditBase

from core.oxm.mongo.document_base import DocumentBase

class Relationship(DocumentBase, AuditBase):

    """

    Relationship document model

    Describes relationships between entities, supporting multiple relationship types and detailed information.

    """

    # Composite primary key

    source_entity_id: Indexed(str) = Field(

        ..., description="Source entity ID, part of composite primary key"

    )

    target_entity_id: Indexed(str) = Field(

        ..., description="Target entity ID, part of composite primary key"

    )

    # Relationship information

    relationship: List[Dict[str, str]] = Field(

        ...,

        description="List of relationships, each containing fields such as type, content, detail",

    )

    # General fields

    extend: Optional[Dict[str, Any]] = Field(

        default=None, description="Reserved extension field"

    )

    model_config = ConfigDict(

        collection="relationships",

        validate_assignment=True,

        json_encoders={datetime: lambda dt: dt.isoformat()},

        json_schema_extra={

            "example": {

                "source_entity_id": "entity_001",

                "target_entity_id": "entity_002",

                "relationship": [

                    {

                        "type": "Interpersonal relationship",

                        "content": "Project collaboration",

                        "detail": "Collaborated on the e-commerce platform refactoring project",

                    },

                    {

                        "type": "Work relationship",

                        "content": "Superior-subordinate",

                        "detail": "Zhang San is responsible for guiding Li Si's technical work",

                    },

                ],

                "extend": {"strength": "strong", "context": "work environment"},

            }

        },

    )

    class Settings:

        """Beanie Settings"""

        name = "relationships"

        indexes = [

            IndexModel(

                [("source_entity_id", ASCENDING), ("target_entity_id", ASCENDING)],

                unique=True,

                name="idx_source_target_unique",

            ),

            IndexModel(

                [("target_entity_id", ASCENDING), ("source_entity_id", ASCENDING)],

                unique=True,

                name="idx_target_source_unique",

            ),

            IndexModel([("created_at", DESCENDING)], name="idx_created_at"),

            IndexModel([("updated_at", DESCENDING)], name="idx_updated_at"),

        ]

        validate_on_save = True

        use_state_management = True

