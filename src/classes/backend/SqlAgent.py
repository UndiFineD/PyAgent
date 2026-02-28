#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

from __future__ import annotations
from src.core.base.version import VERSION
import sqlite3
import json
import os
import gzip
import logging
import time
from typing import List, Dict, Any, Optional

__version__ = VERSION

class SqlMetadataHandler:
    """Relational metadata overlay for compressed interaction shards."""

    def __init__(self, db_path: str = "data/memory/agent_store/metadata.db", shards_dir: str = "data/memory/agent_store/memory_shards", fleet: Any | None = None) -> None:
        if fleet and hasattr(fleet, "recorder") and shards_dir == "data/memory/agent_store/memory_shards":
            self.shards_dir = str(fleet.recorder.log_dir)
        else:
            self.shards_dir = shards_dir
        
        self.db_path = db_path
        self._init_db()

    def _init_db(self) -> None:
        """Initializes the SQLite schema with Phase 108 high-performance settings."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            # High-performance PRAGMAs for trillion-parameter scale metadata
            conn.execute("PRAGMA journal_mode = WAL")
            conn.execute("PRAGMA synchronous = NORMAL")
            conn.execute("PRAGMA cache_size = -64000")  # 64MB cache
            conn.execute("PRAGMA temp_store = MEMORY")
            
            cursor = conn.cursor()
            # Table for interactions
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS interactions (
                    id TEXT PRIMARY KEY,
                    shard_id INTEGER,
                    timestamp REAL,
                    agent_name TEXT,
                    task_type TEXT,
                    success INTEGER
                )
            """)
            # Table for technical debt tracking (Phase 107)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS technical_debt (
                    file_path TEXT,
                    issue_type TEXT,
                    message TEXT,
                    fixed INTEGER,
                    timestamp REAL
                )
            """)

            # Table for interaction tags (Phase 106)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS metadata_tags (
                    id TEXT,
                    tag TEXT,
                    PRIMARY KEY (id, tag)
                )
            """)
            
            # Table for AI Lessons / Extracted Intelligence (Phase 108)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS intelligence_lessons (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_interaction_id TEXT,
                    lesson_text TEXT,
                    category TEXT,
                    timestamp REAL
                )
            """)

            # Phase 108: Full-Text Search for Trillion-Parameter Scale Intelligence Search
            try:
                cursor.execute("""
                    CREATE VIRTUAL TABLE IF NOT EXISTS intelligence_search USING fts5(
                        lesson_text,
                        category,
                        content='intelligence_lessons',
                        content_rowid='id'
                    )
                """)
                # Trigger to keep FTS in sync
                cursor.execute("""
                    CREATE TRIGGER IF NOT EXISTS ai_intelligence_ai AFTER INSERT ON intelligence_lessons BEGIN
                        INSERT INTO intelligence_search(rowid, lesson_text, category) VALUES (new.id, new.lesson_text, new.category);
                    END
                """)
            except sqlite3.OperationalError:
                logging.warning("FTS5 not supported in this SQLite build. Logic falling back to standard LIKE.")
            
            # Phase 107/108 Optimized Indexes for Meta-Scale Data
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_agent_name ON interactions (agent_name)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_task_type ON interactions (task_type)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON interactions (timestamp)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_tags ON metadata_tags (tag)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_lessons_cat ON intelligence_lessons (category)")
            
            conn.commit()

    def optimize_db(self) -> None:
        """Runs maintenance operations for large datasets (Phase 108)."""
        db_size_mb = os.path.getsize(self.db_path) / (1024 * 1024)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("PRAGMA journal_mode = WAL")
            conn.execute("VACUUM")
            conn.execute("ANALYZE")
            # Phase 108: Reindex for massive FTS5 performance
            conn.execute("REINDEX")
            logging.info(f"SQL Metadata DB optimized (Size: {db_size_mb:.1f}MB, WAL/VACUUM/ANALYZE/REINDEX).")
        
        # Phase 108: Scalability Gatekeeping (Prep for trillion-parameter community data)
        if db_size_mb > 1024:
            # 1GB threshold for relational sharding
             logging.warning("SQL Metadata DB exceeds scale thresholds. Partitioning registry recommended.")

    def _rotate_metadata_shard(self) -> None:
        """Logic for metadata sharding/rotation."""
        pass

    def record_lesson(self, interaction_id: str, text: str, category: str = "General") -> None:
        """Persists an extracted AI lesson to the intelligence table."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO intelligence_lessons (source_interaction_id, lesson_text, category, timestamp)
                VALUES (?, ?, ?, ?)
            """, (interaction_id, text, category, time.time()))
            conn.commit()

    def get_intelligence_summary(self) -> list[dict[str, Any]]:
        """
        Generates a summary of harvested intelligence lessons.
        Optimized for high-scale analysis of trillion-parameter related interaction logs.
        """
        results = []
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            # Select most frequent failure categories and their latest lessons
            query = """
                SELECT category, COUNT(*) as count, MAX(lesson_text) as sample_lesson
                FROM intelligence_lessons
                GROUP BY category
                ORDER BY count DESC
            """
            cursor.execute(query)
            for row in cursor.fetchall():
                results.append(dict(row))
        return results

    def index_shards(self) -> int:
        """Scans shards and populates the metadata DB."""
        indexed_count = 0
        shard_files = [f for f in os.listdir(self.shards_dir) if f.endswith(".jsonl.gz")]
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            for shard_file in shard_files:
                # shard_YYYYMM_000.jsonl.gz -> 000
                try:
                    shard_num = int(shard_file.split("_")[-1].split(".")[0])
                except Exception:
                    shard_num = 0
                shard_path = os.path.join(self.shards_dir, shard_file)
                
                try:
                    with gzip.open(shard_path, "rt", encoding="utf-8") as f:
                        for line in f:
                            data = json.loads(line)
                            meta = data.get("meta", {})
                            i_id = meta.get("id", f"{shard_num}_{indexed_count}")
                            
                            # Insert interaction metadata
                            cursor.execute("""
                                INSERT OR REPLACE INTO interactions (id, shard_id, timestamp, agent_name, task_type, success)
                                VALUES (?, ?, ?, ?, ?, ?)
                            """, (
                                i_id,
                                shard_num,
                                data.get("timestamp", 0),
                                meta.get("agent", "unknown"),
                                meta.get("type", "generic"),
                                1 if meta.get("status") == "success" else 0
                            ))
                            
                            # Insert tags if present
                            if "tags" in meta:
                                for tag in meta["tags"]:
                                    cursor.execute("INSERT OR IGNORE INTO metadata_tags VALUES (?, ?)", (i_id, tag))
                            
                            indexed_count += 1
                except Exception as e:
                    logging.error(f"Failed to index shard {shard_file}: {e}")
            conn.commit()
        return indexed_count

    def query_interactions(self, sql_where: str) -> list[dict[str, Any]]:
        """Query interactions using SQL syntax."""
        results = []
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            query = f"SELECT * FROM interactions WHERE {sql_where}"
            cursor.execute(query)
            for row in cursor.fetchall():
                results.append(dict(row))
        return results

    def record_debt(self, file_path: str, issue_type: str, message: str, fixed: bool) -> None:
        """Persists identified technical debt to the relational DB."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO technical_debt (file_path, issue_type, message, fixed, timestamp)
                VALUES (?, ?, ?, ?, ?)
            """, (file_path, issue_type, message, 1 if fixed else 0, time.time()))
            conn.commit()

    def bulk_record_interactions(self, interaction_data: list[tuple]) -> int:
        """
        Efficiently inserts multiple interactions in a single transaction.
        Essential for processing 'trillion-parameter' scale interaction datasets.
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("PRAGMA journal_mode = WAL")
            cursor = conn.cursor()
            cursor.executemany("""
                INSERT OR REPLACE INTO interactions (id, shard_id, timestamp, agent_name, task_type, success)
                VALUES (?, ?, ?, ?, ?, ?)
            """, interaction_data)
            conn.commit()
            return cursor.rowcount
