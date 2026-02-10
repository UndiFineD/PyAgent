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

import uuid
from typing import Dict, Any


class JobManagerCore:
    """
    Domain logic for managing asynchronous jobs and task lifecycles in the PyAgent system.
    """
    def __init__(self):
        self.jobs: Dict[str, Dict[str, Any]] = {}

    async def submit_job(self, task_data: Dict[str, Any]) -> str:
        job_id = str(uuid.uuid4())
        self.jobs[job_id] = {
            "status": "pending",
            "data": task_data,
            "result": None
        }
        return job_id

    async def get_job_status(self, job_id: str) -> Dict[str, Any]:
        return self.jobs.get(job_id, {"status": "not_found"})

    async def update_job_progress(self, job_id: str, status: str, result: Any = None):
        if job_id in self.jobs:
            self.jobs[job_id]["status"] = status
            if result is not None:
                self.jobs[job_id]["result"] = result
