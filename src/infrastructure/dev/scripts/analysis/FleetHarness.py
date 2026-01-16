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

"""Unified Fleet Harness for repository management and repair."""

from __future__ import annotations
import argparse
import subprocess
import sys
from pathlib import Path

from src.core.base.BaseInterfaces import ContextRecorderInterface
from src.infrastructure.backend.LocalContextRecorder import LocalContextRecorder

SCRIPTS_DIR = Path(__file__).parent
MGMT_DIR = SCRIPTS_DIR / "management"


def run_script(
    script_path: Path,
    args: list[str] | None = None,
    recorder: ContextRecorderInterface | None = None,
) -> None:
    """Executes an internal management script and records the invocation."""
    if not script_path.exists():
        print(f"Error: Script {script_path} not found.")
        return

    cmd = [sys.executable, str(script_path)] + (args or [])

    print(f"Executing: {' '.join(cmd)}")

    if recorder:
        recorder.record_interaction(
            provider="fleet",
            model="harness",
            prompt=" ".join(cmd),
            result="launched",
            meta={"script": str(script_path), "args": args or []},
        )

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing script: {e}")


def main() -> None:
    parser = argparse.ArgumentParser(description="PyAgent Fleet Harness")
    subparsers = parser.add_subparsers(dest="command", help="Management commands")

    # Heal
    subparsers.add_parser("heal", help="Run autonomous fleet healing")

    # Restore
    subparsers.add_parser("restore", help="Restore fleet state")

    # Improve

    improve_parser = subparsers.add_parser("improve", help="Run self-improvement cycle")
    improve_parser.add_argument("-c", "--cycles", type=int, default=1)
    improve_parser.add_argument(
        "-p", "--prompt", type=str, default="docs/notes/prompt.txt"
    )

    args, unknown = parser.parse_known_args()
    recorder: ContextRecorderInterface | None = LocalContextRecorder(Path.cwd())

    if args.command == "heal":
        run_script(SCRIPTS_DIR / "run_autonomous_fleet_healing.py", unknown, recorder)
    elif args.command == "restore":
        run_script(SCRIPTS_DIR / "fleet_restoration.py", unknown, recorder)
    elif args.command == "improve":
        run_script(
            SCRIPTS_DIR / "run_fleet_self_improvement.py",
            ["-c", str(args.cycles), "-p", args.prompt] + unknown,
            recorder,
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
