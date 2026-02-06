# Extracted from: C:\DEV\PyAgent\.external\skills\skills\lraivisto\researchvault\scripts\core.py
import hashlib
import json
import os
import sqlite3
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Type

import requests

import scripts.db as db
from scripts.scuttle import ArtifactDraft, Connector, IngestResult


class MissingAPIKeyError(Exception):
    pass


class IngestService:
    """Service to manage connector registration and ingestion routing."""

    def __init__(self):
        self._connectors: List[Connector] = []

    def register_connector(self, connector: Connector):
        self._connectors.append(connector)

    def get_connector_for(self, source: str) -> Optional[Connector]:
        for connector in self._connectors:
            if connector.can_handle(source):
                return connector
        return None

    def ingest(self, project_id: str, source: str) -> IngestResult:
        connector = self.get_connector_for(source)
        if not connector:
            return IngestResult(
                success=False, error=f"No connector found for source: {source}"
            )

        try:
            draft = connector.fetch(source)
            # Add to database (Finding table)
            add_insight(
                project_id,
                draft.title,
                draft.content,
                source_url=source,
                tags=",".join(draft.tags),
                confidence=draft.confidence,
            )
            # Log event
            log_event(
                project_id,
                "INGEST",
                "connector_fetch",
                draft.raw_payload or {"title": draft.title},
                confidence=draft.confidence,
                source=draft.source,
                tags=",".join(draft.tags),
            )
            return IngestResult(
                success=True, metadata={"title": draft.title, "source": draft.source}
            )
        except Exception as e:
            return IngestResult(success=False, error=str(e))


def perform_brave_search(query):
    api_key = os.environ.get("BRAVE_API_KEY")
    if not api_key:
        raise MissingAPIKeyError("BRAVE_API_KEY not found in environment variables.")

    url = "https://api.search.brave.com/res/v1/web/search"
    headers = {"X-Subscription-Token": api_key, "Accept": "application/json"}
    params = {"q": query}

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def log_search(query, result):
    query_hash = hashlib.sha256(query.lower().strip().encode()).hexdigest()
    conn = db.get_connection()
    c = conn.cursor()
    now = datetime.now().isoformat()
    c.execute(
        "INSERT OR REPLACE INTO search_cache VALUES (?, ?, ?, ?)",
        (query_hash, query, json.dumps(result), now),
    )
    conn.commit()
    conn.close()


def check_search(query, ttl_hours=24):
    query_hash = hashlib.sha256(query.lower().strip().encode()).hexdigest()
    conn = db.get_connection()
    c = conn.cursor()
    c.execute(
        "SELECT result, timestamp FROM search_cache WHERE query_hash=?", (query_hash,)
    )
    row = c.fetchone()
    conn.close()
    if row:
        result, timestamp = row
        try:
            cached_time = datetime.fromisoformat(timestamp)
            if datetime.now() - cached_time < timedelta(hours=ttl_hours):
                return json.loads(result)
        except ValueError:
            pass
    return None


def start_project(project_id, name, objective, priority=0):
    conn = db.get_connection()
    c = conn.cursor()
    now = datetime.now().isoformat()
    c.execute(
        "INSERT OR IGNORE INTO projects VALUES (?, ?, ?, ?, ?, ?)",
        (project_id, name, objective, "active", now, priority),
    )
    conn.commit()
    conn.close()
    print(f"Project '{name}' ({project_id}) initialized with priority {priority}.")


def log_event(
    project_id, event_type, step, payload, confidence=1.0, source="unknown", tags=""
):
    conn = db.get_connection()
    c = conn.cursor()
    now = datetime.now().isoformat()
    c.execute(
        "INSERT INTO events (project_id, event_type, step, payload, confidence, source, tags, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (
            project_id,
            event_type,
            step,
            json.dumps(payload),
            confidence,
            source,
            tags,
            now,
        ),
    )
    conn.commit()
    conn.close()


def get_status(project_id, tag_filter=None):
    conn = db.get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM projects WHERE id=?", (project_id,))
    project = c.fetchone()
    if not project:
        conn.close()
        return None

    query = "SELECT event_type, step, payload, confidence, source, timestamp, tags FROM events WHERE project_id=?"
    params = [project_id]
    if tag_filter:
        query += " AND tags LIKE ?"
        params.append(f"%{tag_filter}%")
    query += " ORDER BY id DESC LIMIT 10"

    c.execute(query, params)
    events = c.fetchall()
    conn.close()
    return {"project": project, "recent_events": events}


def update_status(project_id, status=None, priority=None):
    try:
        conn = db.get_connection()
        c = conn.cursor()
        if status:
            c.execute("UPDATE projects SET status=? WHERE id=?", (status, project_id))
            if c.rowcount == 0:
                print(f"Error: Project '{project_id}' not found.")
            else:
                print(f"Project '{project_id}' status updated to '{status}'.")
        if priority is not None:
            c.execute(
                "UPDATE projects SET priority=? WHERE id=?", (priority, project_id)
            )
            if c.rowcount == 0:
                print(f"Error: Project '{project_id}' not found.")
            else:
                print(f"Project '{project_id}' priority updated to {priority}.")
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()


def list_projects():
    conn = db.get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM projects ORDER BY priority DESC, created_at DESC")
    projects = c.fetchall()
    conn.close()
    return projects


def add_insight(project_id, title, content, source_url="", tags="", confidence=1.0):
    conn = db.get_connection()
    c = conn.cursor()
    now = datetime.now().isoformat()
    # Migration v2 uses 'findings' table. Insights table is legacy.
    import json
    import uuid

    finding_id = f"fnd_{uuid.uuid4().hex[:8]}"
    evidence = json.dumps({"source_url": source_url})

    c.execute(
        """INSERT INTO findings (id, project_id, title, content, evidence, confidence, tags, created_at)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (finding_id, project_id, title, content, evidence, confidence, tags, now),
    )
    conn.commit()
    conn.close()


def get_insights(project_id, tag_filter=None):
    conn = db.get_connection()
    c = conn.cursor()
    # Migration v2 uses 'findings' table.
    if tag_filter:
        c.execute(
            "SELECT title, content, evidence, tags, created_at, confidence FROM findings WHERE project_id=? AND tags LIKE ? ORDER BY created_at DESC",
            (project_id, f"%{tag_filter}%"),
        )
    else:
        c.execute(
            "SELECT title, content, evidence, tags, created_at, confidence FROM findings WHERE project_id=? ORDER BY created_at DESC",
            (project_id,),
        )
    rows = c.fetchall()
    conn.close()
    return rows


def get_ingest_service():
    """Returns a pre-configured IngestService with all connectors registered."""
    from scripts.scuttle import (
        GrokipediaConnector,
        MoltbookScuttler,
        RedditScuttler,
        WebScuttler,
        YouTubeConnector,
    )

    service = IngestService()
    service.register_connector(RedditScuttler())
    service.register_connector(MoltbookScuttler())
    service.register_connector(GrokipediaConnector())
    service.register_connector(YouTubeConnector())
    service.register_connector(WebScuttler())
    return service
