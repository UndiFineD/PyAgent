#!/usr/bin/env python3

"""Fleet-wide manager for database schema discovery and metadata storage."""

from __future__ import annotations

import logging
from typing import Dict, List, Any

class SchemaManager:
    """Discovers and caches database schemas across the fleet."""
    
    def __init__(self) -> None:
        self.schemas: Dict[str, Dict[str, Any]] = {} # db_path -> schema_map

    def register_schema(self, db_id: str, tables: Dict[str, List[str]]) -> str:
        """Registers a database schema (tables and columns)."""
        self.schemas[db_id] = tables
        logging.info(f"SchemaManager: Registered schema for {db_id} with {len(tables)} tables.")

    def get_context_for_agent(self, db_id: str) -> str:
        """Generates a schema summary for an agent's system prompt."""
        if db_id not in self.schemas:
            return "No schema information available."
        
        summary = [f"Database: {db_id}"]
        for table, cols in self.schemas[db_id].items():
            summary.append(f"- Table: {table} (Columns: {', '.join(cols)})")
        return "\n".join(summary)

    def list_known_databases(self) -> List[str]:
        """Returns IDs of all registered databases."""
        return list(self.schemas.keys())
