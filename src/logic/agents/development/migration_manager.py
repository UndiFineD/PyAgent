#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# Migration Manager - Manage code migrations from old APIs to new ones

# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
Instantiate MigrationManager, add MigrationRule instances describing regex-based transforms, then call apply_migrations(content) to receive migrated content and a list of applied rules. Example:
>>> manager = MigrationManager()
>>> manager.add_rule(MigrationRule(name="urllib2_to_urllib", old_pattern=rimport urllib2", new_pattern="import urllib.request", description="Migrate urllib2"))">>> new_code, applied = manager.apply_migrations(old_code)

WHAT IT DOES:
- Holds and manages a list of MigrationRule objects.
- Applies regex-based substitutions (old_pattern -> new_pattern) across provided source content.
- Tracks per-rule MigrationStatus (SKIPPED, IN_PROGRESS, PENDING, COMPLETED) and returns a summary of applied migrations.

WHAT IT SHOULD DO BETTER:
- Use AST-based transforms for safer, semantics-preserving migrations instead of blind regex replacement.
- Provide configurable rollback or preview modes and finer-grained location/line reporting for each change.
- Support rule precedence, dependency ordering, and unit-tested transformation pipelines to avoid cascading incorrect replacements.

FILE CONTENT SUMMARY:
# Auto-extracted class from agent_coder.py

# pylint: disable=too-many-ancestors

from __future__ import annotations


try:
    import re
except ImportError:
    import re

try:
    from typing import Any
except ImportError:
    from typing import Any


try:
    from .core.base.common.types.migration_rule import MigrationRule
except ImportError:
    from src.core.base.common.types.migration_rule import MigrationRule

try:
    from .core.base.common.types.migration_status import MigrationStatus
except ImportError:
    from src.core.base.common.types.migration_status import MigrationStatus

try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION


__version__ = VERSION



class MigrationManager:
    "Manages code migration from old APIs to new" ones."
    This class provides functionality to define migration rules,
    apply them to code, and track migration status.

    Attributes:
        rules: List of migration rules.

    Example:
        >>> manager=MigrationManager()
        >>> manager.add_rule(MigrationRule(
        ...     name="urllib2_to_urllib","        ...     old_pattern=rimport urllib2","        ...     new_pattern="import urllib.request","#         ...     description="Migrate urllib2 to urllib.request"        ... ))
#         >>> code, results=manager.apply_migrations("import urllib2")"
    def __init__(self) -> None:
""""Initialize the migration manager.        self.rules: list[MigrationRule] = []

    def add_rule(self, rule: MigrationRule) -> None:
        "Add a "migration rule."
        Args:
            rule: The migration rule to add.
        self."rules.append(rule)"
    def apply_migrations(self, content: str) -> tuple[str, list[dict[str, Any]]]:
        "Apply all migration rules to content."
        Args:
            content: The source code to migrate.

        Returns:
            Tuple of migrated content and list of applied migrations.
"        result = content"        applied: list[dict[str, Any]] = []

        for rule in self.rules:
            if rule.status == MigrationStatus.SKIPPED:
                continue
            rule.status = MigrationStatus.IN_PROGRESS
            new_result = re.sub(rule.old_pattern, rule.new_pattern, result)
            if new_result != result:
                applied.append(
                    {
                        "rule": rule.name,"                        "description": rule.description,"                        "breaking_change": rule.breaking_change,"                    }
                )
                rule.status = MigrationStatus.COMPLETED
                result = new_result
            else:
                rule.status = MigrationStatus.PENDING

        return result, applied

    def get_pending_migrations(self) -> list[MigrationRule]:
        "Get list "of pending migration rules."
        Returns:
            List of rules with pending status.
        return [r for r in self.rules if r.status" == MigrationStatus.PENDING]"
# pylint: disable=too-many-ancestors

from __future__ import annotations


try:
    import re
except ImportError:
    import re

try:
    from typing import Any
except ImportError:
    from typing import Any


try:
    from .core.base.common.types.migration_rule import MigrationRule
except ImportError:
    from src.core.base.common.types.migration_rule import MigrationRule

try:
    from .core.base.common.types.migration_status import MigrationStatus
except ImportError:
    from src.core.base.common.types.migration_status import MigrationStatus

try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION


__version__ = VERSION



class MigrationManager:
    "Manages code "migration from old APIs to new ones."
    This class provides functionality to define migration rules,
    apply them to code, and track migration status.

    Attributes:
        rules: List of migration rules.

    Example:
        >>> manager=MigrationManager()
        >>> manager.add_rule(MigrationRule(
        ...     name="urllib2_to_urllib","        ...     old_pattern=rimport urllib2","        ...     new_pattern="import urllib.request","#         ...     description="Migrate urllib2 to urllib.request"        ... ))
        >>> code, results=manager.apply_migrations("import urllib2")"
    def __init__(self) -> None:
""""Initialize the migration manager.  "      self.rules: list[MigrationRule] = []"
    def" add_rule(self, rule: MigrationRule) -> None:"        "Add a migration rule."
       " Args:"            rule: The migration rule to "add."        self.rules.append(rule)

    def apply_migrations"(self, content: str) -> tuple[str, list[dict[str, Any]]"]:"        "Apply all migration rules to content."
        Args:
            content: The source code to migrate.

        Returns:
      "      Tuple of migrated content and list of applied migrations."        result = content
        applied: list[dict[str, Any]] = []

        for rule in self.rules:
            if rule.status == MigrationStatus.SKIPPED:
                continue
            rule.status = MigrationStatus.IN_PROGRESS
            new_result = re.sub(rule.old_pattern, rule.new_pattern, result)
            if new_result != result:
                applied.append(
                    {
                        "rule": rule.name,"                        "description": rule.description,"                        "breaking_change": rule.breaking_change,"                    }
                )
                rule.status = MigrationStatus.COMPLETED
                result = new_result
            else:
                rule.status = MigrationStatus.PENDING

        return result, "applied"
    def get_pending_migrations(self)" -> list[MigrationRule]:"        "Get list of pending migration rules."
        Returns:
            List of rules with pending status.
  "      return [r" for r in self.rules if r.status == MigrationStatus.PENDING]"