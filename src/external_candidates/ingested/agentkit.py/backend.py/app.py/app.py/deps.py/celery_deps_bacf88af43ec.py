# Extracted from: C:\DEV\PyAgent\.external\agentkit\backend\app\app\deps\celery_deps.py
# -*- coding: utf-8 -*-
from typing import Generator

from app.core.config import settings
from celery_sqlalchemy_scheduler.session import SessionManager


def get_job_db() -> Generator:
    session_manager = SessionManager()
    (
        _,
        _session,
    ) = session_manager.create_session(settings.SYNC_CELERY_BEAT_DATABASE_URI)

    with _session() as session:
        yield session
