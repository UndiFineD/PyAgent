# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agents_generic.py\livekit_agents.py\livekit.py\agents.py\ipc.py\job_executor_e06cca91aec0.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agents_generic\livekit-agents\livekit\agents\ipc\job_executor.py

from __future__ import annotations

from enum import Enum

from typing import Any, Protocol

from ..job import RunningJobInfo


class JobExecutor(Protocol):
    @property
    def id(self) -> str: ...

    @property
    def started(self) -> bool: ...

    @property
    def user_arguments(self) -> Any | None: ...

    @user_arguments.setter
    def user_arguments(self, value: Any | None) -> None: ...

    @property
    def running_job(self) -> RunningJobInfo | None: ...

    @property
    def status(self) -> JobStatus: ...

    async def start(self) -> None: ...

    async def join(self) -> None: ...

    async def initialize(self) -> None: ...

    async def aclose(self) -> None: ...

    async def launch_job(self, info: RunningJobInfo) -> None: ...

    def logging_extra(self) -> dict[str, Any]: ...


class JobStatus(Enum):
    RUNNING = "running"

    FAILED = "failed"

    SUCCESS = "success"
