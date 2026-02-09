# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-market-claude-code-skills\transcript-fixer\scripts\cli\__init__.py
"""
CLI Module - Command-Line Interface Handlers

This module contains command handlers and argument parsing:
- commands: Command handler functions (cmd_*)
- argument_parser: CLI argument configuration
"""

from .argument_parser import create_argument_parser
from .commands import (
    cmd_add_correction,
    cmd_approve,
    cmd_audit_retention,
    cmd_config,
    cmd_health,
    cmd_init,
    cmd_list_corrections,
    cmd_metrics,
    cmd_migration,
    cmd_review_learned,
    cmd_run_correction,
    cmd_validate,
)

__all__ = [
    "cmd_init",
    "cmd_add_correction",
    "cmd_list_corrections",
    "cmd_run_correction",
    "cmd_review_learned",
    "cmd_approve",
    "cmd_validate",
    "cmd_health",
    "cmd_metrics",
    "cmd_config",
    "cmd_migration",
    "cmd_audit_retention",
    "create_argument_parser",
]
