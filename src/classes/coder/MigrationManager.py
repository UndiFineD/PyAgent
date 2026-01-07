#!/usr/bin/env python3

"""Auto-extracted class from agent_coder.py"""

from __future__ import annotations

from .MigrationRule import MigrationRule
from .MigrationStatus import MigrationStatus

from base_agent import BaseAgent
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple
import ast
import hashlib
import logging
import math
import re
import shutil
import subprocess
import tempfile

class MigrationManager:
    """Manages code migration from old APIs to new ones.

    This class provides functionality to define migration rules,
    apply them to code, and track migration status.

    Attributes:
        rules: List of migration rules.

    Example:
        >>> manager=MigrationManager()
        >>> manager.add_rule(MigrationRule(
        ...     name="urllib2_to_urllib",
        ...     old_pattern=r"import urllib2",
        ...     new_pattern="import urllib.request",
        ...     description="Migrate urllib2 to urllib.request"
        ... ))
        >>> code, results=manager.apply_migrations("import urllib2")
    """

    def __init__(self) -> None:
        """Initialize the migration manager."""
        self.rules: List[MigrationRule] = []

    def add_rule(self, rule: MigrationRule) -> None:
        """Add a migration rule.

        Args:
            rule: The migration rule to add.
        """
        self.rules.append(rule)

    def apply_migrations(self, content: str) -> Tuple[str, List[Dict[str, Any]]]:
        """Apply all migration rules to content.

        Args:
            content: The source code to migrate.

        Returns:
            Tuple of migrated content and list of applied migrations.
        """
        result = content
        applied: List[Dict[str, Any]] = []

        for rule in self.rules:
            if rule.status == MigrationStatus.SKIPPED:
                continue
            rule.status = MigrationStatus.IN_PROGRESS
            new_result = re.sub(rule.old_pattern, rule.new_pattern, result)
            if new_result != result:
                applied.append({
                    "rule": rule.name,
                    "description": rule.description,
                    "breaking_change": rule.breaking_change
                })
                rule.status = MigrationStatus.COMPLETED
                result = new_result
            else:
                rule.status = MigrationStatus.PENDING

        return result, applied

    def get_pending_migrations(self) -> List[MigrationRule]:
        """Get list of pending migration rules.

        Returns:
            List of rules with pending status.
        """
        return [r for r in self.rules if r.status == MigrationStatus.PENDING]
