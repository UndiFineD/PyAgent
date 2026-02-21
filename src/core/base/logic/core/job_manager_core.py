#!/usr/bin/env python3
"""Job manager core - minimal parser-safe implementation."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional, List
import uuid


class JobStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class AgentJob:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: JobStatus = JobStatus.PENDING
    payload: Dict[str, Any] = field(default_factory=dict)
    result: Optional[Any] = None
    error: Optional[str] = None


class JobManagerCore:
    """Manages the lifecycle of persistent agent jobs (minimal stub)."""

    def __init__(self) -> None:
        self._jobs: Dict[str, AgentJob] = {}

    async def create_job(self, payload: Dict[str, Any]) -> str:
        job = AgentJob(payload=payload)
        self._jobs[job.id] = job
        return job.id

    async def update_job_status(self, job_id: str, status: JobStatus, result: Any = None, error: Optional[str] = None) -> None:
        if job_id in self._jobs:
            job = self._jobs[job_id]
            job.status = status
            if result is not None:
                job.result = result
            if error is not None:
                job.error = error

    def get_job(self, job_id: str) -> Optional[AgentJob]:
        return self._jobs.get(job_id)

    async def list_active_jobs(self) -> List[AgentJob]:
        return [j for j in self._jobs.values() if j.status in (JobStatus.PENDING, JobStatus.RUNNING)]
