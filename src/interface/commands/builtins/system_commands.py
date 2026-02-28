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

"""
Built-in system commands for slash commands.
"""

from __future__ import annotations

import os
import platform
import sys
import time
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from ..base import CommandContext, CommandResult

if TYPE_CHECKING:
    from ..registry import CommandRegistry


_builtins_registered = False


def register_system_commands(registry: CommandRegistry, start_time: float) -> None:
    """Register system-related built-in commands."""

    @registry.command(
        "datetime",
        description="Get current server date and time",
        usage="/datetime",
        aliases=["dt", "now"],
    )
    def cmd_datetime(ctx: CommandContext) -> CommandResult:
        now = datetime.now(timezone.utc)
        local_now = datetime.now()
        return CommandResult.ok(
            output=f"[{now.strftime('%Y-%m-%d %H:%M:%S')} UTC]",
            data={
                "utc": now.isoformat(),
                "local": local_now.isoformat(),
                "timestamp": now.timestamp(),
                "timezone": time.tzname[0],
            },
        )

    @registry.command(
        "date",
        description="Get current server date",
        usage="/date",
    )
    def cmd_date(ctx: CommandContext) -> CommandResult:
        now = datetime.now(timezone.utc)
        return CommandResult.ok(
            output=f"[{now.strftime('%Y-%m-%d')}]",
            data={"date": now.strftime("%Y-%m-%d"), "iso": now.date().isoformat()},
        )

    @registry.command(
        "time",
        description="Get current server time",
        usage="/time",
    )
    def cmd_time(ctx: CommandContext) -> CommandResult:
        now = datetime.now(timezone.utc)
        return CommandResult.ok(
            output=f"[{now.strftime('%H:%M:%S')} UTC]",
            data={"time": now.strftime("%H:%M:%S"), "timezone": "UTC"},
        )

    @registry.command(
        "stats",
        description="Get system statistics",
        usage="/stats",
        aliases=["sys", "system"],
    )
    def cmd_stats(ctx: CommandContext) -> CommandResult:
        import psutil

        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage("/")

        output = (
            f"[CPU: {cpu_percent:.1f}% | "
            f"RAM: {memory.percent:.1f}% ({memory.used // (1024**3):.1f}GB/{memory.total // (1024**3):.1f}GB) | "
            f"Disk: {disk.percent:.1f}%]"
        )

        return CommandResult.ok(
            output=output,
            data={
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "memory_used_gb": memory.used / (1024**3),
                "memory_total_gb": memory.total / (1024**3),
                "disk_percent": disk.percent,
                "disk_used_gb": disk.used / (1024**3),
                "disk_total_gb": disk.total / (1024**3),
            },
        )

    @registry.command(
        "uptime",
        description="Get process uptime",
        usage="/uptime",
        aliases=["up"],
    )
    def cmd_uptime(ctx: CommandContext) -> CommandResult:
        uptime_seconds = time.time() - start_time

        days = int(uptime_seconds // 86400)
        hours = int((uptime_seconds % 86400) // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        seconds = int(uptime_seconds % 60)

        if days > 0:
            uptime_str = f"{days}d {hours}h {minutes}m"
        elif hours > 0:
            uptime_str = f"{hours}h {minutes}m {seconds}s"
        else:
            uptime_str = f"{minutes}m {seconds}s"

        return CommandResult.ok(
            output=f"[Uptime: {uptime_str}]",
            data={
                "uptime_seconds": uptime_seconds,
                "days": days,
                "hours": hours,
                "minutes": minutes,
                "seconds": seconds,
            },
        )

    @registry.command(
        "version",
        description="Get version information",
        usage="/version",
        aliases=["ver", "v"],
    )
    def cmd_version(ctx: CommandContext) -> CommandResult:
        python_version = sys.version.split()[0]

        return CommandResult.ok(
            output=f"[Python {python_version} | {platform.system()} {platform.release()}]",
            data={
                "python_version": python_version,
                "python_full": sys.version,
                "platform": platform.system(),
                "platform_release": platform.release(),
                "platform_version": platform.version(),
                "machine": platform.machine(),
            },
        )

    @registry.command(
        "env",
        description="Get environment variable",
        usage="/env [VAR_NAME]",
        aliases=["environ"],
    )
    def cmd_env(ctx: CommandContext) -> CommandResult:
        if ctx.first_arg:
            value = os.environ.get(ctx.first_arg.upper())
            if value:
                display = value[:50] + "..." if len(value) > 50 else value
                return CommandResult.ok(
                    output=f"[{ctx.first_arg.upper()}={display}]",
                    data={"key": ctx.first_arg.upper(), "value": value},
                )
            return CommandResult.ok(
                output=f"[{ctx.first_arg.upper()}: not set]",
                data={"key": ctx.first_arg.upper(), "value": None},
            )

        common_vars = ["PATH", "HOME", "USER", "SHELL", "VIRTUAL_ENV", "PYTHONPATH"]
        found = {k: os.environ.get(k, "not set")[:30] for k in common_vars if k in os.environ}

        return CommandResult.ok(
            output=f"[Env vars: {len(os.environ)} total]",
            data={"count": len(os.environ), "sample": found},
        )

    @registry.command(
        "health",
        description="System health check",
        usage="/health",
        aliases=["ping", "status"],
    )
    def cmd_health(ctx: CommandContext) -> CommandResult:
        import psutil

        cpu = psutil.cpu_percent(interval=0.1)
        mem = psutil.virtual_memory().percent

        health_score = 100
        issues = []

        if cpu > 90:
            health_score -= 30
            issues.append("high CPU")
        elif cpu > 70:
            health_score -= 10

        if mem > 90:
            health_score -= 30
            issues.append("high memory")
        elif mem > 80:
            health_score -= 10

        status = "healthy" if health_score >= 80 else "degraded" if health_score >= 50 else "unhealthy"

        return CommandResult.ok(
            output=f"[Health: {status} ({health_score}/100)]",
            data={
                "status": status,
                "score": health_score,
                "cpu_percent": cpu,
                "memory_percent": mem,
                "issues": issues,
            },
        )

    @registry.command(
        "help",
        description="Show help for commands",
        usage="/help [command]",
        aliases=["h", "?"],
    )
    def cmd_help(ctx: CommandContext) -> CommandResult:
        if ctx.first_arg:
            defn = registry.get(ctx.first_arg)
            if not defn:
                return CommandResult.ok(output=f"[Unknown command: {ctx.first_arg}]")

            aliases_str = f" (aliases: {', '.join('/' + a for a in defn.aliases)})" if defn.aliases else ""
            output = f"[/{defn.name}{aliases_str}: {defn.description}]"
            if defn.usage:
                output = f"[Usage: {defn.usage}]"

            return CommandResult.ok(
                output=output,
                data={
                    "name": defn.name,
                    "description": defn.description,
                    "usage": defn.usage,
                    "aliases": defn.aliases,
                },
            )

        commands = registry.list_commands()
        cmd_names = sorted([f"/{c.name}" for c in commands])

        return CommandResult.ok(
            output=f"[Commands: {', '.join(cmd_names)}]",
            data={"commands": [c.name for c in commands]},
            inline=False,
        )

    @registry.command(
        "gpu",
        description="GPU information",
        usage="/gpu",
        aliases=["cuda", "nvidia"],
    )
    def cmd_gpu(ctx: CommandContext) -> CommandResult:
        try:
            import torch

            if torch.cuda.is_available():
                gpu_count = torch.cuda.device_count()
                current_device = torch.cuda.current_device()
                gpu_name = torch.cuda.get_device_name(current_device)
                gpu_memory = torch.cuda.get_device_properties(current_device).total_memory
                gpu_memory_gb = gpu_memory / (1024**3)

                return CommandResult.ok(
                    output=f"[GPU: {gpu_name} ({gpu_memory_gb:.1f}GB) x{gpu_count}]",
                    data={
                        "available": True,
                        "count": gpu_count,
                        "name": gpu_name,
                        "memory_gb": gpu_memory_gb,
                    },
                )
        except ImportError:
            pass

        return CommandResult.ok(
            output="[GPU: Not available]",
            data={"available": False},
        )

    @registry.command(
        "python",
        description="Python interpreter info",
        usage="/python",
        aliases=["py"],
    )
    def cmd_python(ctx: CommandContext) -> CommandResult:
        v = sys.version_info
        return CommandResult.ok(
            output=f"[Python {v.major}.{v.minor}.{v.micro} at {sys.executable}]",
            data={
                "version": f"{v.major}.{v.minor}.{v.micro}",
                "executable": sys.executable,
                "prefix": sys.prefix,
                "platform": sys.platform,
            },
        )

    @registry.command(
        "cwd",
        description="Current working directory",
        usage="/cwd",
        aliases=["pwd", "dir"],
    )
    def cmd_cwd(ctx: CommandContext) -> CommandResult:
        cwd = os.getcwd()
        return CommandResult.ok(
            output=f"[CWD: {cwd}]",
            data={"cwd": cwd},
        )

    @registry.command(
        "uuid",
        description="Generate a UUID",
        usage="/uuid",
        aliases=["id", "guid"],
    )
    def cmd_uuid(ctx: CommandContext) -> CommandResult:
        import uuid

        new_uuid = str(uuid.uuid4())
        return CommandResult.ok(
            output=f"[{new_uuid}]",
            data={"uuid": new_uuid},
        )

    @registry.command(
        "random",
        description="Generate random number",
        usage="/random [max]",
        aliases=["rand", "rnd"],
    )
    def cmd_random(ctx: CommandContext) -> CommandResult:
        import random

        max_val = 100
        if ctx.first_arg:
            try:
                max_val = int(ctx.first_arg)
            except ValueError:
                pass

        value = random.randint(1, max_val)
        return CommandResult.ok(
            output=f"[{value}]",
            data={"value": value, "max": max_val},
        )
