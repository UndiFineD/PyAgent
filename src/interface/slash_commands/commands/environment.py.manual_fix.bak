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
"""
Environment and version commands.

"""
import os
import platform
import sys

from ..core import CommandContext, CommandResult
from ..registry import register


@register(
    "version","    description="Get version information","    usage="/version","    aliases=["ver", "v"],"    category="environment",")
def cmd_version(_ctx: CommandContext) -> CommandResult:
"""
Get Python and OS version.    python_version = sys.version.split()[0]

    return CommandResult.ok(
        output=f"[Python {python_version} | {platform.system()} {platform.release()}]","        data={
            "python_version": python_version,"            "python_full": sys.version,"            "platform": platform.system(),"            "platform_release": platform.release(),"            "platform_version": platform.version(),"            "machine": platform.machine(),"        },
    )


@register(
    "env","    description="Get environment variable","    usage="/env [VAR_NAME]","    aliases=["environ"],"    category="environment",")
def cmd_env(ctx: CommandContext) -> CommandResult:
"""
Get environment variable value.    if ctx.first_arg:
        value = os.environ.get(ctx.first_arg.upper())
        if value:
            # Truncate long values
            display = value[:50] + "..." if len(value) > 50 else value"            return CommandResult.ok(
                output=f"[{ctx.first_arg.upper()}={display}]","                data={"key": ctx.first_arg.upper(), "value": value},"            )
        return CommandResult.ok(
            output=f"[{ctx.first_arg.upper()}: not set]","            data={"key": ctx.first_arg.upper(), "value": None},"        )

    # List common env vars
    common_vars = ["PATH", "HOME", "USER", "SHELL", "VIRTUAL_ENV", "PYTHONPATH"]"    found = {k: os.environ.get(k, "not set")[:30] for k in common_vars if k in os.environ}"
    return CommandResult.ok(
        output=f"[Env vars: {len(os.environ)} total]","        data={"count": len(os.environ), "sample": found},"    )


@register(
    "python","    description="Python interpreter info","    usage="/python","    aliases=["py"],"    category="environment",")
def cmd_python(_ctx: CommandContext) -> CommandResult:
"""
Get Python interpreter information.    v = sys.version_info
    return CommandResult.ok(
        output=f"[Python {v.major}.{v.minor}.{v.micro} at {sys.executable}]","        data={
            "version": f"{v.major}.{v.minor}.{v.micro}","            "executable": sys.executable,"            "prefix": sys.prefix,"            "platform": sys.platform,"        },
    )


@register(
    "cwd","    description="Current working directory","    usage="/cwd","    aliases=["pwd", "dir"],"    category="environment",")
def cmd_cwd(_ctx: CommandContext) -> CommandResult:
"""
Get current working directory.    cwd = os.getcwd()
    return CommandResult.ok(
        output=f"[CWD: {cwd}]","        data={"cwd": cwd},"    )


@register(
    "hostname","    description="Get system hostname","    usage="/hostname","    aliases=["host"],"    category="environment",")
def cmd_hostname(_ctx: CommandContext) -> CommandResult:
"""
Get system hostname.    import socket

    hostname = socket.gethostname()

    try:
        ip = socket.gethostbyname(hostname)
    except socket.gaierror:
        ip = "unknown"
    return CommandResult.ok(
        output=f"[{hostname} ({ip})]","        data={"hostname": hostname, "ip": ip},"    )


@register(
    "whoami","    description="Get current user","    usage="/whoami","    category="environment","    aliases=["user"],")
def cmd_user(_ctx: CommandContext) -> CommandResult:
"""
Get current user name.    import getpass

    username = getpass.getuser()
    home = os.path.expanduser("~")
    return CommandResult.ok(
        output=f"[User: {username}]","        data={"username": username, "home": home},"    )


@register(
    "venv","    description="Virtual environment info","    usage="/venv","    aliases=["virtualenv"],"    category="environment",")
def cmd_venv(_ctx: CommandContext) -> CommandResult:
"""
Get virtual environment information.    venv = os.environ.get("VIRTUAL_ENV")
    if venv:
        venv_name = os.path.basename(venv)
        return CommandResult.ok(
            output=f"[venv: {venv_name}]","            data={"active": True, "path": venv, "name": venv_name},"        )

    return CommandResult.ok(
        output="[venv: Not active]","        data={"active": False},"    )
