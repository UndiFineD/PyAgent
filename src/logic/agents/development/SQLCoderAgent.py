#!/usr/bin/env python3
# Copyright (c) 2025 PyAgent contributors
# Licensed under the Apache License, Version 2.0 (the "License");

"""Agent specializing in SQL and database scripts."""

from __future__ import annotations

from src.logic.agents.development.CoderAgent import CoderAgent
from src.core.base.utilities import create_main_function
import logging

class SQLCoderAgent(CoderAgent):
    """Agent for auditing and improving SQL scripts."""
    
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._language = "sql"
        # SQL-specific instructions
        self._system_prompt = (
            "You are a SQL Expert and Database Administrator. "
            "Focus on query performance, indexing, security (injection prevention), "
            "and adherence to standard SQL patterns or specific dialects (PostgreSQL, MySQL, T-SQL)."
        )

    def _get_default_content(self) -> str:
        return "-- SQL Script\nSELECT 1;\n"

if __name__ == "__main__":
    main = create_main_function(SqlAgent, "SQL Agent", "Path to SQL file")
    main()

