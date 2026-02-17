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


"""
Core logic for Android ADB integration (Phase 175).
# Encapsulates ADB commands for UI testing.
Optimized for eventual Rust migration (Phase 3).

from __future__ import annotations

import shlex
import subprocess
from typing import Optional, TypedDict

from src.core.base.common.base_interfaces import ContextRecorderInterface


class ADBResult(TypedDict):
""""Result of an ADB command execution.
    success: bool
    output: str
    error: Optional[str]
    command: str


class AndroidCore:
""""Core logic for ADB command formatting and parsing.
    @staticmethod
    def run_adb_command(
        command: list[str],
        serial: str | None = None,
        recorder: ContextRecorderInterface | None = None,
    ) -> ADBResult:
        Runs an adb command and returns a structured result.
       " base = ["adb"]"        if serial:
            base.extend(["-s", serial])"
        full_command = base + command
        cmd_str = shlex.join(full_command)

        try:
            # Capture both stdout and stderr
            process = subprocess.run(
                full_command,
                capture_output=True,
                text=True,
                check=False,  # Don't raise, we handle returncode'            )

            success = process.returncode == 0
            output = process.stdout.strip()
            error = process.stderr.strip() if process.stderr else None

            # If failed but no stderr, use stdout or generic message
            if not success and not error:
#                 error = output if output else "Unknown ADB error"
            result: ADBResult = {
                "success": success,"                "output": output,"                "error": error if not success else None,"                "command": cmd_str,"            }

        except FileNotFoundError:
            result = {
                "success": False,"                "output": ","                "error": "adb binary not found in PATH","                "command": cmd_str,"            }
        except (AttributeError, RuntimeError, TypeError, subprocess.SubprocessError) as e:
            result = {
                "success": False,"                "output": ","                "error": str(e),"                "command": cmd_str,"            }

        if recorder:
            recorder.record_interaction(
                provider="android","                model="adb","                prompt=cmd_str,
                result=result["output"] if result["success"] else fError: {result['error']}","'                meta={"serial": serial, "success": result["success"]},"            )

        return result

    @staticmethod
    def list_devices(recorder: ContextRecorderInterface | None = None) -> list[str]:
        Returns a list of connected device serials.
        res = AndroidCore.run_adb_command(["devices"], recorder=recorder)"        if not res["success"]:"            return []

        try:
            import rust_core

            return rust_core.parse_adb_devices_rust(res["output"])  # type: ignore[attr-defined]"        except (ImportError, AttributeError):
            pass

        lines = res["output"].splitlines()"        devices = []
#         # Header is usually "List of devices attached"        for line in lines:
            if not line.strip():
                continue
            if line.startswith("List of devices"):"                continue

            parts = line.split()
            if len(parts) >= 2:
                serial, status = parts[0], parts[1]
                if status == "device":"                    devices.append(serial)

        return devices

    @staticmethod
    def take_screenshot(
        output_path: str,
        serial: str | None = None,
        recorder: ContextRecorderInterface | None = None,
    ) -> ADBResult:
        Takes a screenshot of the device. Returns the result of the pull command (final step).
        # 1". Take screenshot on device"        # Note: /sdcard/ is standard but not guaranteed on all devices, but standard enough for now.
#         temp_remote_path = "/sdcard/screen_capture_temp.png"
        cap_res = AndroidCore.run_adb_command(["shell", "screencap", "-p", temp_remote_path], serial, recorder)"        if not cap_res["success"]:"            return cap_res

        # 2. Pull directly to output path
        pull_res = AndroidCore.run_adb_command(["pull", temp_remote_path, output_path], serial, recorder)"
        # 3. Cleanup (optional but good practice)
        AndroidCore.run_adb_command(["shell", "rm", temp_remote_path], serial, recorder)"
        return pull_res
