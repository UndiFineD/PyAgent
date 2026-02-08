# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_evermemos.py\src.py\infra_layer.py\adapters.py\out.py\persistence.py\document.py\memory.py\conversation_meta_0c20509451c2.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-EverMemOS\src\infra_layer\adapters\out\persistence\document\memory\conversation_meta.py

"""

ConversationMeta Beanie ODM model

A conversation metadata document model based on Beanie ODM, storing complete metadata of conversations.

"""

from datetime import datetime

from typing import Any, Dict, List, Optional

from beanie import Indexed

from common_utils.datetime_utils import get_timezone

from pydantic import BaseModel, ConfigDict, Field

from pymongo import ASCENDING, DESCENDING, TEXT, IndexModel

from core.oxm.mongo.audit_base import AuditBase

from core.oxm.mongo.document_base import DocumentBase


class UserDetailModel(BaseModel):
    """User detail nested model

    Used to store user basic information and additional extended information

    """

    full_name: str = Field(..., description="User full name")

    role: Optional[str] = Field(default=None, description="User role, e.g.: user, assistant, admin, etc.")

    extra: Optional[Dict[str, Any]] = Field(default=None, description="Extension fields, supporting dynamic schema")


class ConversationMeta(DocumentBase, AuditBase):
    """

    Conversation metadata document model

    Stores complete metadata of conversations, including scene, participants, tags, etc.

    Used for context management and memory retrieval in multi-turn conversations.

    """

    # Version information

    version: str = Field(..., description="Data version number, e.g.: 1.0.0")

    # Scene information

    scene: str = Field(
        ...,
        description="Scene identifier, used to distinguish different application scenarios",
    )

    scene_desc: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Scene description information, typically containing fields like bot_ids",
    )

    # Conversation basic information

    name: str = Field(..., description="Conversation name")

    description: Optional[str] = Field(default=None, description="Conversation description")

    group_id: Indexed(str) = Field(..., description="Group ID, used to associate a group of conversations")

    # Time information

    conversation_created_at: str = Field(..., description="Conversation creation time, ISO format string")

    default_timezone: Optional[str] = Field(
        default_factory=lambda: get_timezone().key,
        description="Default timezone, e.g.: UTC",
    )

    # Participant information

    user_details: Dict[str, UserDetailModel] = Field(
        default_factory=dict,
        description="Dictionary of participant details, key is dynamic user ID (e.g., user_001, robot_001), value is user detail",
    )

    # Tags and categories

    tags: List[str] = Field(
        default_factory=list,
        description="List of tags, used for classification and retrieval",
    )

    model_config = ConfigDict(
        # Collection name
        collection="conversation_metas",
        # Validation configuration
        validate_assignment=True,
        # JSON serialization configuration
        json_encoders={datetime: lambda dt: dt.isoformat()},
        # Example data
        json_schema_extra={
            "example": {
                "version": "1.0.0",
                "scene": "scene_a",
                "scene_desc": {"bot_ids": ["aaa", "bbb", "ccc"]},
                "name": "User health consultation conversation",
                "description": "Conversation records between user and AI assistant regarding Beijing travel, health management, sports rehabilitation, etc.",
                "group_id": "chat_user_001_assistant",
                "conversation_created_at": "2025-08-26T00:00:00Z",
                "default_timezone": "UTC",
                "user_details": {
                    "user_001": {
                        "full_name": "User",
                        "role": "User",
                        "extra": {
                            "height": 170,
                            "weight": 86,
                            "bmi": 29.8,
                            "waist_circumference": 104,
                            "origin": "Sichuan",
                            "preferences": {
                                "food": "hotpot",
                                "activities": "group activities",
                            },
                        },
                    },
                    "robot_001": {
                        "full_name": "AI Assistant",
                        "role": "Assistant",
                        "extra": {"type": "assistant"},
                    },
                },
                "tags": [
                    "health consultation",
                    "travel planning",
                    "sports rehabilitation",
                    "diet advice",
                ],
            }
        },
    )

    class Settings:
        """Beanie settings"""

        name = "conversation_metas"

        indexes = [
            # group_id index (high-frequency query)
            IndexModel([("group_id", ASCENDING)], name="idx_group_id"),
            # scene index (scene query)
            IndexModel([("scene", ASCENDING)], name="idx_scene"),
            # Composite index: group_id + scene (common compound query)
            IndexModel(
                [("group_id", ASCENDING), ("scene", ASCENDING)],
                name="idx_group_id_scene",
            ),
        ]

        validate_on_save = True

        use_state_management = True
