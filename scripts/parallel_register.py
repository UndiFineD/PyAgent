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

from __future__ import annotations

import argparse
import json
import os
import tempfile
import time
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

DEFAULT_REGISTER = Path(".github/agents/data/parallel_agents_register.json")
KNOWN_AGENTS = [
    "@0master",
    "@1project",
    "@2think",
    "@3design",
    "@4plan",
    "@5test",
    "@6code",
    "@7exec",
    "@8ql",
    "@9git",
    "@10idea",
]


class RegisterConflictError(RuntimeError):
    """Raised when a file lock conflicts with an existing active lock."""


def _utc_now() -> str:
    """Get the current UTC time as an ISO 8601 string."""
    return datetime.now(timezone.utc).isoformat()


def _new_agent_state() -> dict[str, Any]:
    """Create a new agent state dictionary with default values."""
    return {
        "status": "idle",
        "work_package_id": "",
        "depends_on": [],
        "touching_files": [],
        "planned_files": [],
        "lock_ids": [],
        "updated_at": "",
    }


def _normalize_register(data: dict[str, Any]) -> dict[str, Any]:
    """Normalize the register data structure, ensuring all required fields are present."""
    data.setdefault("schema_version", "1.0.0")
    data.setdefault("register_id", "parallel-agents-register")
    data.setdefault("description", "Shared coordination register for parallel agent work, file touches, and file locks.")
    data.setdefault("updated_at", "")
    data.setdefault("updated_by", "")
    data.setdefault("active_project_id", "")
    data.setdefault("active_branch", "")
    data.setdefault("active_wave_id", "")
    data.setdefault("waves", [])
    data.setdefault("agents", {})
    data.setdefault("file_locks", [])
    data.setdefault("lockfiles", [])
    data.setdefault("event_log", [])

    for agent in KNOWN_AGENTS:
        if agent not in data["agents"]:
            data["agents"][agent] = _new_agent_state()
        else:
            current = data["agents"][agent]
            default = _new_agent_state()
            for key, value in default.items():
                current.setdefault(key, value)

    return data


@contextmanager
def _register_mutex(lock_path: Path, timeout_seconds: float = 8.0) -> Iterator[None]:
    """Context manager for acquiring a mutex on the register file."""
    start = time.monotonic()
    while True:
        try:
            fd = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.close(fd)
            break
        except FileExistsError:
            if time.monotonic() - start > timeout_seconds:
                raise TimeoutError(f"Timed out waiting for register lock: {lock_path}")
            time.sleep(0.05)

    try:
        yield
    finally:
        if lock_path.exists():
            lock_path.unlink()


def _load_register(register_path: Path) -> dict[str, Any]:
    """Load the parallel register from a JSON file."""
    if not register_path.exists():
        return _normalize_register({})

    raw = register_path.read_text(encoding="utf-8")
    data = json.loads(raw)
    return _normalize_register(data)


def _atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    """Atomically write a JSON payload to a file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=str(path.parent), delete=False) as tmp:
        json.dump(payload, tmp, indent=2, ensure_ascii=False)
        tmp.write("\n")
        temp_name = tmp.name
    os.replace(temp_name, path)


def _append_unique(items: list[str], value: str) -> None:
    """Append a value to a list if it is not already present."""
    if value and value not in items:
        items.append(value)


def _refresh_lockfiles(register: dict[str, Any]) -> None:
    """Refresh the list of lockfiles in the register."""
    register["lockfiles"] = sorted(
        {
            str(lock["file_path"])
            for lock in register["file_locks"]
            if lock.get("status") == "active" and lock.get("file_path")
        }
    )


def _append_event(register: dict[str, Any], event_type: str, actor: str, payload: dict[str, Any]) -> None:
    """Append an event to the register's event log."""
    register["event_log"].append(
        {
            "ts": _utc_now(),
            "event": event_type,
            "actor": actor,
            "payload": payload,
        }
    )


def _touch_metadata(register: dict[str, Any], updated_by: str, project_id: str, branch: str, wave_id: str) -> None:
    """Update the metadata of the register with the provided information."""
    register["updated_at"] = _utc_now()
    register["updated_by"] = updated_by
    if project_id:
        register["active_project_id"] = project_id
    if branch:
        register["active_branch"] = branch
    if wave_id:
        register["active_wave_id"] = wave_id


def _ensure_agent(register: dict[str, Any], agent: str) -> dict[str, Any]:
    """Ensure that *agent* exists in the register and return its state dictionary."""
    if agent not in register["agents"]:
        register["agents"][agent] = _new_agent_state()
    return register["agents"][agent]


def acquire_lock(
    register_path: Path,
    agent: str,
    work_package_id: str,
    file_path: str,
    lock_id: str,
    project_id: str,
    branch: str,
    wave_id: str,
) -> dict[str, Any]:
    """Acquire a lock in the parallel register.

    Args:
        register_path: Path to the parallel register JSON file.
        agent: Name of the agent acquiring the lock.
        work_package_id: ID of the work package associated with the lock.
        file_path: Path to the file being locked.
        lock_id: ID of the lock to be acquired.
        project_id: ID of the project associated with the lock.
        branch: Branch name associated with the lock.
        wave_id: ID of the wave associated with the lock.

    Returns:
        A dictionary containing the status and details of the acquired lock.

    """
    mutex = register_path.with_suffix(register_path.suffix + ".lock")

    with _register_mutex(mutex):
        register = _load_register(register_path)

        for lock in register["file_locks"]:
            if lock.get("status") != "active":
                continue
            if lock.get("file_path") != file_path:
                continue
            if lock.get("owner_agent") == agent and lock.get("work_package_id") == work_package_id:
                continue
            raise RegisterConflictError(
                f"Lock conflict on {file_path}: {lock.get('owner_agent')}:{lock.get('work_package_id')}"
            )

        lock_record = {
            "lock_id": lock_id,
            "file_path": file_path,
            "owner_agent": agent,
            "work_package_id": work_package_id,
            "status": "active",
            "acquired_at": _utc_now(),
            "released_at": "",
        }
        register["file_locks"].append(lock_record)

        agent_state = _ensure_agent(register, agent)
        agent_state["status"] = "in-progress"
        agent_state["work_package_id"] = work_package_id
        _append_unique(agent_state["lock_ids"], lock_id)
        _append_unique(agent_state["touching_files"], file_path)
        agent_state["updated_at"] = _utc_now()

        _touch_metadata(register, updated_by=agent, project_id=project_id, branch=branch, wave_id=wave_id)
        _append_event(
            register,
            "acquire-lock",
            agent,
            {"lock_id": lock_id, "file_path": file_path, "work_package_id": work_package_id},
        )
        _refresh_lockfiles(register)
        _atomic_write_json(register_path, register)

    return {"status": "ok", "lock_id": lock_id, "file_path": file_path, "agent": agent}


def release_lock(register_path: Path, agent: str, lock_id: str, wave_id: str) -> dict[str, Any]:
    """Release a lock in the parallel register.

    Args:
        register_path: Path to the parallel register JSON file.
        agent: Name of the agent releasing the lock.
        lock_id: ID of the lock to be released.
        wave_id: ID of the wave associated with the lock.

    Returns:
        A dictionary containing the status and details of the released lock.

    """
    mutex = register_path.with_suffix(register_path.suffix + ".lock")

    with _register_mutex(mutex):
        register = _load_register(register_path)
        released: dict[str, Any] | None = None

        for lock in register["file_locks"]:
            if lock.get("lock_id") != lock_id:
                continue
            if lock.get("status") != "active":
                break
            if lock.get("owner_agent") != agent:
                raise PermissionError(f"Lock {lock_id} belongs to {lock.get('owner_agent')}, not {agent}")
            lock["status"] = "released"
            lock["released_at"] = _utc_now()
            released = lock
            break

        if released is None:
            raise KeyError(f"Active lock not found: {lock_id}")

        agent_state = _ensure_agent(register, agent)
        agent_state["lock_ids"] = [item for item in agent_state["lock_ids"] if item != lock_id]
        agent_state["updated_at"] = _utc_now()

        _touch_metadata(register, updated_by=agent, project_id="", branch="", wave_id=wave_id)
        _append_event(
            register,
            "release-lock",
            agent,
            {"lock_id": lock_id, "file_path": released["file_path"], "work_package_id": released["work_package_id"]},
        )
        _refresh_lockfiles(register)
        _atomic_write_json(register_path, register)

    return {"status": "ok", "lock_id": lock_id, "agent": agent}


def touch_file(
    register_path: Path,
    agent: str,
    work_package_id: str,
    file_path: str,
    kind: str,
    project_id: str,
    branch: str,
    wave_id: str,
) -> dict[str, Any]:
    """Touch a file in the parallel register.

    Args:
        register_path: Path to the parallel register JSON file.
        agent: Name of the agent touching the file.
        work_package_id: ID of the work package associated with the file.
        file_path: Path to the file being touched.
        kind: Type of touch operation ("planned" or "touching").
        project_id: ID of the project associated with the file.
        branch: Branch name associated with the file.
        wave_id: ID of the wave associated with the file.

    Returns:
        A dictionary containing the status and details of the touched file.

    """
    if kind not in {"planned", "touching"}:
        raise ValueError("kind must be one of: planned, touching")

    mutex = register_path.with_suffix(register_path.suffix + ".lock")

    with _register_mutex(mutex):
        register = _load_register(register_path)
        agent_state = _ensure_agent(register, agent)

        agent_state["status"] = "in-progress"
        agent_state["work_package_id"] = work_package_id
        agent_state.setdefault("planned_files", [])
        agent_state.setdefault("touching_files", [])

        target_key = "planned_files" if kind == "planned" else "touching_files"
        _append_unique(agent_state[target_key], file_path)
        agent_state["updated_at"] = _utc_now()

        _touch_metadata(register, updated_by=agent, project_id=project_id, branch=branch, wave_id=wave_id)
        _append_event(
            register,
            "touch-file",
            agent,
            {
                "work_package_id": work_package_id,
                "file_path": file_path,
                "kind": kind,
            },
        )
        _atomic_write_json(register_path, register)

    return {"status": "ok", "agent": agent, "file_path": file_path, "kind": kind}


def close_wave(register_path: Path, actor: str, wave_id: str, note: str) -> dict[str, Any]:
    """Close a wave in the parallel register.

    Args:
        register_path: Path to the parallel register JSON file.
        actor: Name of the actor closing the wave.
        wave_id: ID of the wave to close.
        note: Note or description for the wave.

    Returns:
        A dictionary containing the status and details of the closed wave.

    """
    mutex = register_path.with_suffix(register_path.suffix + ".lock")

    with _register_mutex(mutex):
        register = _load_register(register_path)

        for lock in register["file_locks"]:
            if lock.get("status") == "active" and lock.get("work_package_id", "").startswith(wave_id):
                lock["status"] = "released"
                lock["released_at"] = _utc_now()

        register["waves"].append(
            {
                "wave_id": wave_id,
                "status": "closed",
                "closed_at": _utc_now(),
                "closed_by": actor,
                "note": note,
            }
        )

        if register.get("active_wave_id") == wave_id:
            register["active_wave_id"] = ""

        for agent_name, state in register["agents"].items():
            if state.get("work_package_id", "").startswith(wave_id):
                state["status"] = "idle"
                state["work_package_id"] = ""
                state["lock_ids"] = []
                state["touching_files"] = []
                state["updated_at"] = _utc_now()
                _append_event(register, "wave-agent-reset", actor, {"agent": agent_name, "wave_id": wave_id})

        _touch_metadata(register, updated_by=actor, project_id="", branch="", wave_id="")
        _append_event(register, "close-wave", actor, {"wave_id": wave_id, "note": note})
        _refresh_lockfiles(register)
        _atomic_write_json(register_path, register)

    return {"status": "ok", "wave_id": wave_id, "closed_by": actor}


def open_wave(
    register_path: Path,
    actor: str,
    wave_id: str,
    project_id: str,
    branch: str,
    note: str,
) -> dict[str, Any]:
    """Open a wave in the parallel register.

    Args:
        register_path: Path to the parallel register JSON file.
        actor: Name of the actor opening the wave.
        wave_id: ID of the wave to open.
        project_id: ID of the project associated with the wave.
        branch: Branch name associated with the wave.
        note: Note or description for the wave.

    Returns:
        A dictionary containing the status and details of the opened wave.

    """
    mutex = register_path.with_suffix(register_path.suffix + ".lock")

    with _register_mutex(mutex):
        register = _load_register(register_path)

        if register.get("active_wave_id") and register.get("active_wave_id") != wave_id:
            raise RegisterConflictError(
                f"Cannot open {wave_id}: active wave already set to {register.get('active_wave_id')}"
            )

        for wave in register["waves"]:
            if wave.get("wave_id") == wave_id and wave.get("status") == "open":
                _touch_metadata(register, updated_by=actor, project_id=project_id, branch=branch, wave_id=wave_id)
                _append_event(register, "open-wave", actor, {"wave_id": wave_id, "note": note, "idempotent": True})
                _atomic_write_json(register_path, register)
                return {"status": "ok", "wave_id": wave_id, "opened_by": actor, "idempotent": True}

        register["waves"].append(
            {
                "wave_id": wave_id,
                "status": "open",
                "opened_at": _utc_now(),
                "opened_by": actor,
                "note": note,
            }
        )
        _touch_metadata(register, updated_by=actor, project_id=project_id, branch=branch, wave_id=wave_id)
        _append_event(register, "open-wave", actor, {"wave_id": wave_id, "note": note, "idempotent": False})
        _atomic_write_json(register_path, register)

    return {"status": "ok", "wave_id": wave_id, "opened_by": actor, "idempotent": False}


def _build_parser() -> argparse.ArgumentParser:
    """Build the argument parser for the parallel register CLI."""
    parser = argparse.ArgumentParser(description="Manage the parallel agents register atomically.")
    parser.add_argument("--register", default=str(DEFAULT_REGISTER), help="Path to parallel register JSON")

    subparsers = parser.add_subparsers(dest="command", required=True)

    acquire = subparsers.add_parser("acquire-lock", help="Acquire a file lock for a work package")
    acquire.add_argument("--agent", required=True)
    acquire.add_argument("--work-package-id", required=True)
    acquire.add_argument("--file", required=True)
    acquire.add_argument("--lock-id", default="")
    acquire.add_argument("--project-id", default="")
    acquire.add_argument("--branch", default="")
    acquire.add_argument("--wave-id", default="")

    release = subparsers.add_parser("release-lock", help="Release a lock by lock id")
    release.add_argument("--agent", required=True)
    release.add_argument("--lock-id", required=True)
    release.add_argument("--wave-id", default="")

    touch = subparsers.add_parser("touch-file", help="Record a planned or touched file for an agent package")
    touch.add_argument("--agent", required=True)
    touch.add_argument("--work-package-id", required=True)
    touch.add_argument("--file", required=True)
    touch.add_argument("--kind", choices=["planned", "touching"], default="touching")
    touch.add_argument("--project-id", default="")
    touch.add_argument("--branch", default="")
    touch.add_argument("--wave-id", default="")

    close = subparsers.add_parser("close-wave", help="Close a parallel wave and clear remaining active locks")
    close.add_argument("--actor", required=True)
    close.add_argument("--wave-id", required=True)
    close.add_argument("--note", default="")

    open_parser = subparsers.add_parser("open-wave", help="Open a parallel wave and set wave metadata")
    open_parser.add_argument("--actor", required=True)
    open_parser.add_argument("--wave-id", required=True)
    open_parser.add_argument("--project-id", required=True)
    open_parser.add_argument("--branch", required=True)
    open_parser.add_argument("--note", default="")

    return parser


def main() -> int:
    """Main entry point for the parallel register CLI."""
    args = _build_parser().parse_args()
    register_path = Path(args.register).resolve()

    try:
        if args.command == "acquire-lock":
            lock_id = args.lock_id or f"lock-{uuid.uuid4().hex[:12]}"
            result = acquire_lock(
                register_path=register_path,
                agent=args.agent,
                work_package_id=args.work_package_id,
                file_path=args.file,
                lock_id=lock_id,
                project_id=args.project_id,
                branch=args.branch,
                wave_id=args.wave_id,
            )
        elif args.command == "release-lock":
            result = release_lock(
                register_path=register_path,
                agent=args.agent,
                lock_id=args.lock_id,
                wave_id=args.wave_id,
            )
        elif args.command == "touch-file":
            result = touch_file(
                register_path=register_path,
                agent=args.agent,
                work_package_id=args.work_package_id,
                file_path=args.file,
                kind=args.kind,
                project_id=args.project_id,
                branch=args.branch,
                wave_id=args.wave_id,
            )
        elif args.command == "close-wave":
            result = close_wave(
                register_path=register_path,
                actor=args.actor,
                wave_id=args.wave_id,
                note=args.note,
            )
        elif args.command == "open-wave":
            result = open_wave(
                register_path=register_path,
                actor=args.actor,
                wave_id=args.wave_id,
                project_id=args.project_id,
                branch=args.branch,
                note=args.note,
            )
        else:
            raise ValueError(f"Unsupported command: {args.command}")
    except RegisterConflictError as exc:
        print(f"PARALLEL_REGISTER_CONFLICT {exc}")
        return 2
    except Exception as exc:  # pragma: no cover - surface operational failures clearly
        print(f"PARALLEL_REGISTER_ERROR {type(exc).__name__}: {exc}")
        return 1

    print(f"PARALLEL_REGISTER_OK command={args.command} result={json.dumps(result, ensure_ascii=False)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
