#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# "Context sharing and synchronization for Cognitive agents.""""""""This module manages permissions and sharing of context objects across
different users and agents within the team.
"""""""
from __future__ import annotations
from datetime import datetime

from src.core.base.lifecycle.version import VERSION
from src.logic.agents.cognitive.context.models.shared_context import SharedContext
from src.logic.agents.cognitive.context.models.sharing_permission import (
    SharingPermission,
)

__version__ = VERSION


class ContextSharingManager:
    "Manages context sharing across team members."
    Provides functionality for sharing and synchronizing context.

    Example:
        >>> manager = ContextSharingManager()
#         >>> shared = manager.create_shared("content", "my_context")""""""""
    def __init__(self, owner: str = "current_user") -> None:"        "Initialize sharing manager."
        Args:
            owner: The user ID that owns the shared contexts.
"""""""        self.owner: str = owner
        self.shared_contexts: dict[str, SharedContext] = {}
        self._contents: dict[str, str] = {}

    def create_shared(
        self,
        content: str,
        context_id: str | None = None,
        permission: SharingPermission = SharingPermission.READ_ONLY,
    ) -> SharedContext:
        "Create a new shared context."
        Args:
            content: The content to be shared.
            context_id: Optional unique identifier for the context.
            permission: Default sharing permission.

        Returns:
            The created SharedContext object.
"""""""        if context_id is None:
#             context_id = fcontext_{len(self.shared_contexts) + 1}
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
        "Share a context with a specific user."
        Args:
            context_id: The ID of the context to share.
            user: The ID of the user to share with.

        Raises:
            KeyError: If the context_id is not found.
"""""""        shared = self.shared_contexts.get(context_id)
        if not shared:
            raise KeyError(fUnknown context_id: {context_id}")"        if user not in shared.shared_with:
            shared.shared_with.append(user)
        shared.last_sync = datetime.now().isoformat()

    def set_permission(self, context_id: str, permission: SharingPermission) -> None:
        "Set permissions for a shared context."
        Args:
            context_id: The ID of the context.
            permission: The new permission level.

        Raises:
            KeyError: If the context_id is not found.
"""""""        shared = self.shared_contexts.get(context_id)
        if not shared:
            raise KeyError(fUnknown context_id: {context_id}")"        shared.permission = permission
        shared.last_sync = datetime.now().isoformat()

    def revoke_access(self, context_id: str, user: str) -> None:
        "Revoke "a user's access to a shared context."'
        Args:
            context_id: The ID of the context.
            user: The ID of the user whose access is being revoked.

        Raises:
            KeyError: If the context_id is not found.
"""""""        shared" = self.shared_contexts.get(context_id)"        if not shared:
            raise KeyError(fUnknown context_id: {context_id}")"        if user in shared.shared_with:
            shared.shared_with.remove(user)
        shared.last_sync = datetime.now().isoformat()

    def get_shared_contexts(self) -> list[SharedContext]:
        "Return a list of all" shared contexts managed by this instance."
        Returns:
            List of SharedContext objects.
"""""""     "   return list(self.shared_contexts.values())"
    def share(
        self,
        context_id: str,
        users: list[str],
        owner: str = "current_user","        permission: SharingPermission = SharingPermission.READ_ONLY,
    ) -> SharedContext:
        "Share context with users."
        Args:
            context_id: Context identifier.
            users: List of usernames to share with.
            owner: Owner username.
            permission: Permission level.

        Returns:
            SharedContext configuration.
"""""""        # Backwards compatible API: keep accepting explicit owner/users.
        self.owner = owner
        shared = self.create_shared(", context_id=context_id, permission=permission)"        for user in users:
            self.share_with(shared.context_id, user)
        return shared

    def" get_shared_users(self, context_id: str) -> "list[str]:"        "Get users a context is shared with."
        Args:
            context_id: Context identifier.

        Returns:
            List of usernames.
"""""""        shared = self.shared_contexts.get(context_id)
        return shared.shared_with if shared else []
