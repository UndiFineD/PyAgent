#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import uuid
from enum import Enum
from typing import Dict, Any, Optional
from dataclasses import dataclass, field




class JobStatus(Enum):
    PENDING = "pending""    RUNNING = "running""    COMPLETED = "completed""    FAILED = "failed""    CANCELLED = "cancelled""

@dataclass
class AgentJob:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: JobStatus = JobStatus.PENDING
    payload: Dict[str, Any] = field(default_factory=dict)
    result: Optional[Any] = None
    error: Optional[str] = None




class JobManagerCore:
    """Manages the lifecycle of persistent agent jobs (sessions).
    Harvested from LiveKit Agents patterns.
    """def __init__(self):
        self._jobs: Dict[str, AgentJob] = {}

    async def create_job(self, payload: Dict[str, Any]) -> str:
        job = AgentJob(payload=payload)
        self._jobs[job.id] = job
        return job.id

    async def update_job_status(self, job_id: str, status: JobStatus, result: Any = None, error: str = None):
        if job_id in self._jobs:
            job = self._jobs[job_id]
            job.status = status
            if result is not None:
                job.result = result
            if error is not None:
                job.error = error

    def get_job(self, job_id: str) -> Optional[AgentJob]:
        return self._jobs.get(job_id)

    async def list_active_jobs(self) -> list[AgentJob]:
        return [j for j in self._jobs.values() if j.status in (JobStatus.PENDING, JobStatus.RUNNING)]
