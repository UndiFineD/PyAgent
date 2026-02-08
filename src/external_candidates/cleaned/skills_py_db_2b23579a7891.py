# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\skills.py\skills.py\lraivisto.py\researchvault.py\scripts.py\db_2b23579a7891.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\skills\skills\lraivisto\researchvault\scripts\db.py

import json

import os

import sqlite3

import uuid


# Path to the research database

DB_PATH = os.path.expanduser("~/.openclaw/workspace/memory/research_vault.db")


def get_connection():
    """Returns a connection to the SQLite database."""

    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    return sqlite3.connect(DB_PATH)


def init_db():
    """Initialize the database and run versioned migrations."""

    conn = get_connection()

    c = conn.cursor()

    # Ensure schema_version table exists

    c.execute("""CREATE TABLE IF NOT EXISTS schema_version (version INTEGER PRIMARY KEY)""")

    _run_migrations(c)

    conn.commit()

    conn.close()


def _run_migrations(cursor):
    """Run pending versioned migrations."""

    cursor.execute("SELECT version FROM schema_version")

    row = cursor.fetchone()

    current_version = row[0] if row else 0

    migrations = [
        _migration_v1,  # Initial schema
        _migration_v2,  # Add artifacts, findings, links
        _migration_v3,  # Backfill insights -> findings
    ]

    for i, migration_fn in enumerate(migrations):
        version = i + 1

        if version > current_version:
            print(f"Running migration v{version}...")

            migration_fn(cursor)

            if current_version == 0:
                cursor.execute("INSERT INTO schema_version (version) VALUES (?)", (version,))

                current_version = version

            else:
                cursor.execute("UPDATE schema_version SET version = ?", (version,))

                current_version = version


def _migration_v1(cursor):
    """Initial schema baseline."""

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS projects

                 (id TEXT PRIMARY KEY, name TEXT, objective TEXT, status TEXT, created_at TEXT, priority INTEGER DEFAULT 0)"""
    )

    cursor.execute("""CREATE TABLE IF NOT EXISTS events

                 (id INTEGER PRIMARY KEY AUTOINCREMENT, project_id TEXT, event_type TEXT, 

                  step INTEGER, payload TEXT, confidence REAL DEFAULT 1.0, source TEXT DEFAULT 'unknown', 

                  tags TEXT DEFAULT '', timestamp TEXT,

                  FOREIGN KEY(project_id) REFERENCES projects(id))""")

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS search_cache

                 (query_hash TEXT PRIMARY KEY, query TEXT, result TEXT, timestamp TEXT)"""
    )

    cursor.execute("""CREATE TABLE IF NOT EXISTS insights

                 (id INTEGER PRIMARY KEY AUTOINCREMENT, project_id TEXT, title TEXT, 

                  content TEXT, source_url TEXT, tags TEXT, timestamp TEXT,

                  FOREIGN KEY(project_id) REFERENCES projects(id))""")


def _migration_v2(cursor):
    """Add artifacts, findings, and links tables."""

    cursor.execute("""CREATE TABLE IF NOT EXISTS artifacts

                 (id TEXT PRIMARY KEY, project_id TEXT, type TEXT, path TEXT, 

                  metadata TEXT, created_at TEXT,

                  FOREIGN KEY(project_id) REFERENCES projects(id))""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS findings

                 (id TEXT PRIMARY KEY, project_id TEXT, title TEXT, 

                  content TEXT, evidence TEXT, confidence REAL, 

                  tags TEXT, created_at TEXT,

                  FOREIGN KEY(project_id) REFERENCES projects(id))""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS links

                 (id INTEGER PRIMARY KEY AUTOINCREMENT, source_id TEXT, target_id TEXT, 

                  link_type TEXT, metadata TEXT, created_at TEXT)""")


def _migration_v3(cursor):
    """Backfill insights to findings."""

    cursor.execute("SELECT project_id, title, content, source_url, tags, timestamp FROM insights")

    insights = cursor.fetchall()

    for ins in insights:
        project_id, title, content, source_url, tags, timestamp = ins

        # Generate a semi-stable ID for the finding

        import json

        import uuid

        finding_id = f"fnd_{uuid.uuid4().hex[:8]}"

        evidence = json.dumps({"source_url": source_url})

        cursor.execute(
            """INSERT INTO findings (id, project_id, title, content, evidence, confidence, tags, created_at)

                          VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (finding_id, project_id, title, content, evidence, 1.0, tags, timestamp),
        )
