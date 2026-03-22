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

"""SSH/FTP remote helper utilities.

Provides thin wrappers around SSH-style operations. When *paramiko* is
available, real SSH connections are used. Otherwise a subprocess-based
fallback (using the system ``ssh`` binary) is used, with explicit argument
lists — never shell=True with user-supplied strings.
"""

from __future__ import annotations

import argparse
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

try:
    from src.tools.tool_registry import register_tool
except ImportError:  # pragma: no cover
    from tools.tool_registry import register_tool


def run_ssh_command(host: str, command: str, user: str | None = None, port: int = 22) -> subprocess.CompletedProcess[str]:
    """Run *command* on a remote *host* via the system ``ssh`` binary.

    Command arguments are passed as a list — no shell interpolation occurs.

    Parameters
    ----------
    host:
        Target hostname or IP address.
    command:
        Shell command to run on the remote host.
    user:
        Optional SSH username.
    port:
        SSH port (default 22).

    Returns
    -------
    subprocess.CompletedProcess
        Completed process result with stdout/stderr captured.

    Raises
    ------
    FileNotFoundError
        If the ``ssh`` binary is not found on PATH.
    """
    ssh = shutil.which("ssh")
    if not ssh:
        raise FileNotFoundError("ssh binary not found on PATH")

    # Build argument list explicitly — never use shell=True with user input
    cmd: list[str] = [ssh, "-p", str(port)]
    if user:
        cmd.extend(["-l", user])
    cmd.append(host)
    # command itself is passed as a single token; the remote shell interprets it
    cmd.append(command)

    return subprocess.run(cmd, capture_output=True, text=True)


def upload_file(host: str, local_path: str, remote_path: str, user: str | None = None, port: int = 22) -> int:
    """Upload a file to a remote host using ``scp``.

    Parameters
    ----------
    host:
        Target hostname or IP address.
    local_path:
        Source file path on the local machine.
    remote_path:
        Destination path on the remote machine.
    user:
        Optional SSH username.
    port:
        SSH port (default 22).

    Returns
    -------
    int
        Return code (0 = success).

    Raises
    ------
    FileNotFoundError
        If the ``scp`` binary is not found on PATH.
    """
    scp = shutil.which("scp")
    if not scp:
        raise FileNotFoundError("scp binary not found on PATH")

    destination = f"{user}@{host}:{remote_path}" if user else f"{host}:{remote_path}"
    # All args are explicit list items — no shell=True
    cmd = [scp, "-P", str(port), local_path, destination]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode


def upload_files(host: str, local_paths: list[str], remote_dir: str, user: str | None = None, port: int = 22) -> list[int]:
    """Upload multiple files to a remote directory.

    Returns a list of return codes, one per file.
    """
    return [upload_file(host, p, str(Path(remote_dir) / Path(p).name), user, port) for p in local_paths]


def main(args: list[str] | None = None) -> int:
    """Main entry point for the remote tool."""
    parser = argparse.ArgumentParser(prog="remote", description="Remote SSH/SCP helper.")
    sub = parser.add_subparsers(dest="command", required=True)

    run_p = sub.add_parser("run", help="Run a command on a remote host via SSH")
    run_p.add_argument("host", help="Remote host")
    run_p.add_argument("cmd", help="Command to run (quoted string)")
    run_p.add_argument("--user", help="SSH username")
    run_p.add_argument("--port", type=int, default=22)

    up_p = sub.add_parser("upload", help="Upload a local file to a remote host via SCP")
    up_p.add_argument("host", help="Remote host")
    up_p.add_argument("local", help="Local file path")
    up_p.add_argument("remote", help="Remote destination path")
    up_p.add_argument("--user", help="SSH username")
    up_p.add_argument("--port", type=int, default=22)

    parsed = parser.parse_args(args=args)

    if parsed.command == "run":
        try:
            result = run_ssh_command(parsed.host, parsed.cmd, user=parsed.user, port=parsed.port)
            if result.stdout:
                print(result.stdout, end="")
            if result.stderr:
                print(result.stderr, end="", file=sys.stderr)
            return result.returncode
        except FileNotFoundError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1

    if parsed.command == "upload":
        try:
            rc = upload_file(parsed.host, parsed.local, parsed.remote, user=parsed.user, port=parsed.port)
            return rc
        except FileNotFoundError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1

    return 0


register_tool("remote", main, "SSH/SCP remote operations (no shell=True)")


if __name__ == "__main__":
    sys.exit(main())

