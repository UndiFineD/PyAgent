#!/usr/bin/env python3

"""Auto-extracted class from agent_context.py"""

from __future__ import annotations

from src.logic.agents.cognitive.context.models.SharedContext import SharedContext
from src.logic.agents.cognitive.context.models.SharingPermission import SharingPermission

from src.core.base.BaseAgent import BaseAgent
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import hashlib
import json
import logging
import re
import zlib

class ContextSharingManager:
    """Manages context sharing across team members.

    Provides functionality for sharing and synchronizing context.

    Example:
        >>> manager=ContextSharingManager()
        >>> shared=manager.share("context.md", ["user1", "user2"])
    """

    def __init__(self, owner: str = "current_user") -> None:
        """Initialize sharing manager."""
        self.owner: str = owner
        self.shared_contexts: Dict[str, SharedContext] = {}
        self._contents: Dict[str, str] = {}

    def create_shared(
        self,
        content: str,
        context_id: Optional[str] = None,
        permission: SharingPermission = SharingPermission.READ_ONLY,
    ) -> SharedContext:
        if context_id is None:
            context_id = f"context_{len(self.shared_contexts) + 1}"
        shared = SharedContext(
            context_id=context_id,
            owner=self.owner,
            shared_with=[],
            permission=permission,
            last_sync=datetime.now().isoformat(),
        )
        self.shared_contexts[context_id] = shared
        self._contents[context_id] = content
        return shared

    def share_with(self, context_id: str, user: str) -> None:
        shared = self.shared_contexts.get(context_id)
        if not shared:
            raise KeyError(f"Unknown context_id: {context_id}")
        if user not in shared.shared_with:
            shared.shared_with.append(user)
        shared.last_sync = datetime.now().isoformat()

    def set_permission(self, context_id: str, permission: SharingPermission) -> None:
        shared = self.shared_contexts.get(context_id)
        if not shared:
            raise KeyError(f"Unknown context_id: {context_id}")
        shared.permission = permission
        shared.last_sync = datetime.now().isoformat()

    def revoke_access(self, context_id: str, user: str) -> None:
        shared = self.shared_contexts.get(context_id)
        if not shared:
            raise KeyError(f"Unknown context_id: {context_id}")
        if user in shared.shared_with:
            shared.shared_with.remove(user)
        shared.last_sync = datetime.now().isoformat()

    def get_shared_contexts(self) -> List[SharedContext]:
        return list(self.shared_contexts.values())

    def share(
        self,
        context_id: str,
        users: List[str],
        owner: str = "current_user",
        permission: SharingPermission = SharingPermission.READ_ONLY
    ) -> SharedContext:
        """Share context with users.

        Args:
            context_id: Context identifier.
            users: List of usernames to share with.
            owner: Owner username.
            permission: Permission level.

        Returns:
            SharedContext configuration.
        """
        # Backwards compatible API: keep accepting explicit owner/users.
        self.owner = owner
        shared = self.create_shared("", context_id=context_id, permission=permission)
        for user in users:
            self.share_with(shared.context_id, user)
        return shared

    def get_shared_users(self, context_id: str) -> List[str]:
        """Get users a context is shared with.

        Args:
            context_id: Context identifier.

        Returns:
            List of usernames.
        """
        shared = self.shared_contexts.get(context_id)
        return shared.shared_with if shared else []
