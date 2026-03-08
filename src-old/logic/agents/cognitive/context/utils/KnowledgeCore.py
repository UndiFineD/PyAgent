#!/usr/bin/env python3

"""
LLM_CONTEXT_START

## Source: src-old/logic/agents/cognitive/context/utils/KnowledgeCore.description.md

# KnowledgeCore

**File**: `src\logic\agents\cognitive\context\utils\KnowledgeCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 118  
**Complexity**: 5 (moderate)

## Overview

KnowledgeCore logic for specialized workspace analysis.
Contains pure regex and indexing logic for fast symbol discovery.

## Classes (1)

### `KnowledgeCore`

KnowledgeCore logic for specialized workspace analysis.
Uses SQLite FTS5 for extreme scalability (Trillion-Parameter compatible).

**Methods** (5):
- `__init__(self, workspace_root)`
- `_init_db(self)`
- `extract_symbols_from_python(self, content)`
- `extract_backlinks_from_markdown(self, content)`
- `build_symbol_map(self, root, extension_patterns)`

## Dependencies

**Imports** (9):
- `json`
- `logging`
- `pathlib.Path`
- `re`
- `sqlite3`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/cognitive/context/utils/KnowledgeCore.improvements.md

# Improvements for KnowledgeCore

**File**: `src\logic\agents\cognitive\context\utils\KnowledgeCore.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 118 lines (medium)  
**Complexity**: 5 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `KnowledgeCore_test.py` with pytest tests

## Best Practices Checklist

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

"""
KnowledgeCore logic for specialized workspace analysis.
Contains pure regex and indexing logic for fast symbol discovery.
"""

import re
import json
import logging
import sqlite3
from pathlib import Path
from typing import Dict, List, Any, Optional


class KnowledgeCore:
    """
    KnowledgeCore logic for specialized workspace analysis.
    Uses SQLite FTS5 for extreme scalability (Trillion-Parameter compatible).
    """

    def __init__(self, workspace_root: Optional[str] = None) -> None:
        """Initialize the KnowledgeCore with an optional workspace root."""
        self.workspace_root = Path(workspace_root) if workspace_root else None
        self.db_path = (
            self.workspace_root / "data/agents/store" / "knowledge_graph.db"
            if self.workspace_root
            else None
        )
        self._init_db()

    def _init_db(self) -> None:
        """Initializes the SQLite FTS5 database for high-performance indexing."""
        if not self.db_path:
            return

        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            # FTS5 table for fast symbol/content search
            cursor.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS symbols_idx USING fts5(
                    symbol, file_path, category, content UNINDEXED
                )
            """)
            # Interaction storage for AI lessons (Phase 108)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ai_lessons (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    prompt_hash TEXT UNIQUE,
                    lesson TEXT,
                    importance REAL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            conn.close()
        except Exception as e:
            logging.error(f"Failed to initialize KnowledgeCore DB: {e}")

    def extract_symbols_from_python(self, content: str) -> List[str]:
        """Extracts class and function names from Python content."""
        if not content:
            return []
        return re.findall(r"(?:class|def)\s+([a-zA-Z_][a-zA-Z0-9_]*)", content)

    def extract_backlinks_from_markdown(self, content: str) -> List[str]:
        """Extracts [[WikiStyle]] backlinks from markdown content."""
        if not content:
            return []
        return re.findall(r"\[\[(.*?)\]\]", content)

    def build_symbol_map(
        self, root: Path, extension_patterns: Dict[str, str]
    ) -> Dict[str, List[str]]:
        """
        Scans a directory and indexes symbols in SQLite for fast retrieval.
        Optimized for massive datasets with transaction batching.
        """
        symbol_map = {}
        if not self.db_path:
            return {}

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM symbols_idx")  # Refresh index

            batch_data = []
            for ext, pattern in extension_patterns.items():
                for p in root.rglob(f"*{ext}"):
                    if any(
                        part in str(p)
                        for part in ["__pycache__", "venv", ".git", "node_modules"]
                    ):
                        continue
                    try:
                        content = p.read_text(encoding="utf-8")
                        matches = re.findall(pattern, content)
                        rel_path = str(p.relative_to(root))

                        for match in matches:
                            key = match if ext != ".md" else f"link:{match}"
                            category = (
                                "python_symbol" if ext == ".py" else "markdown_link"
                            )
                            batch_data.append((key, rel_path, category, content[:1000]))

                            if key not in symbol_map:
                                symbol_map[key] = []
                            symbol_map[key].append(rel_path)

                        # Commit in batches of 500 records
                        if len(batch_data) >= 500:
                            cursor.executemany(
                                "INSERT INTO symbols_idx VALUES (?, ?, ?, ?)",
                                batch_data,
                            )
                            batch_data = []

                    except Exception as e:
                        logging.debug(f"Failed to scan {p}: {e}")

            if batch_data:
                cursor.executemany(
                    "INSERT INTO symbols_idx VALUES (?, ?, ?, ?)", batch_data
                )

            conn.commit()
            conn.close()
        except Exception as e:
            logging.error(f"KnowledgeCore indexing failed: {e}")

        return symbol_map
