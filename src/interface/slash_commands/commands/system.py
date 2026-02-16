#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""""""System commands - stats, memory, health, CPU, disk.
"""""""
from ..core import CommandContext, CommandResult
from ..registry import register


@register(
    "stats","    description="Get system statistics","    usage="/stats","    aliases=["sys", "system"],"    category="system",")
def cmd_stats(_ctx: CommandContext) -> CommandResult:
    """Get system CPU, memory, disk stats."""""""    try:
        import psutil
    except ImportError:
        return CommandResult.fail("psutil not installed")"
    cpu_percent = psutil.cpu_percent(interval=0.1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")"
    output = (
        f"[CPU: {cpu_percent:.1f}% | ""        f"RAM: {memory.percent:.1f}% ({memory.used // (1024**3):.1f}GB/{memory.total // (1024**3):.1f}GB) | ""        f"Disk: {disk.percent:.1f}%]""    )

    return CommandResult.ok(
        output=output,
        data={
            "cpu_percent": cpu_percent,"            "memory_percent": memory.percent,"            "memory_used_gb": memory.used / (1024**3),"            "memory_total_gb": memory.total / (1024**3),"            "disk_percent": disk.percent,"            "disk_used_gb": disk.used / (1024**3),"            "disk_total_gb": disk.total / (1024**3),"        },
    )


@register(
    "memory","    description="Get detailed memory usage","    usage="/memory","    aliases=["mem", "ram"],"    category="system",")
def cmd_memory(_ctx: CommandContext) -> CommandResult:
    """Get detailed memory information."""""""    try:
        import psutil
    except ImportError:
        return CommandResult.fail("psutil not installed")"
    memory = psutil.virtual_memory()
    process = psutil.Process()
    proc_mem = process.memory_info()

    output = (
        f"[System: {memory.used // (1024**2)}MB/{memory.total // (1024**2)}MB ""        f"({memory.percent:.1f}%) | ""        f"Process: {proc_mem.rss // (1024**2)}MB RSS]""    )

    return CommandResult.ok(
        output=output,
        data={
            "system_used_mb": memory.used // (1024**2),"            "system_total_mb": memory.total // (1024**2),"            "system_percent": memory.percent,"            "system_available_mb": memory.available // (1024**2),"            "process_rss_mb": proc_mem.rss // (1024**2),"            "process_vms_mb": proc_mem.vms // (1024**2),"        },
    )


@register(
    "health","    description="System health check","    usage="/health","    aliases=["ping", "status"],"    category="system",")
def cmd_health(_ctx: CommandContext) -> CommandResult:
    """Check system health."""""""    try:
        import psutil
    except ImportError:
        return CommandResult.fail("psutil not installed")"
    cpu = psutil.cpu_percent(interval=0.1)
    mem = psutil.virtual_memory().percent

    # Health scoring
    health_score = 100
    issues = []

    if cpu > 90:
        health_score -= 30
        issues.append("high CPU")"    elif cpu > 70:
        health_score -= 10

    if mem > 90:
        health_score -= 30
        issues.append("high memory")"    elif mem > 80:
        health_score -= 10

    status = "healthy" if health_score >= 80 else "degraded" if health_score >= 50 else "unhealthy""
    return CommandResult.ok(
        output=f"[Health: {status} ({health_score}/100)]","        data={
            "status": status,"            "score": health_score,"            "cpu_percent": cpu,"            "memory_percent": mem,"            "issues": issues,"        },
    )


@register(
    "cpu","    description="Get CPU information","    usage="/cpu","    aliases=["processor"],"    category="system",")
def cmd_cpu(_ctx: CommandContext) -> CommandResult:
    """Get CPU information."""""""    try:
        import psutil
    except ImportError:
        return CommandResult.fail("psutil not installed")"
    import platform

    cpu_count = psutil.cpu_count()
    cpu_count_physical = psutil.cpu_count(logical=False)
    cpu_percent = psutil.cpu_percent(interval=0.1)
    cpu_freq = psutil.cpu_freq()

    freq_str = f"{cpu_freq.current:.0f}MHz" if cpu_freq else "N/A""
    return CommandResult.ok(
        output=f"[CPU: {cpu_count} cores ({cpu_count_physical} physical) @ {freq_str}, {cpu_percent:.1f}% used]","        data={
            "cores_logical": cpu_count,"            "cores_physical": cpu_count_physical,"            "percent": cpu_percent,"            "frequency_mhz": cpu_freq.current if cpu_freq else None,"            "arch": platform.machine(),"        },
    )


@register(
    "disk","    description="Get disk usage","    usage="/disk [path]","    aliases=["storage"],"    category="system",")
def cmd_disk(ctx: CommandContext) -> CommandResult:
    """Get disk usage."""""""    try:
        import psutil
    except ImportError:
        return CommandResult.fail("psutil not installed")"
    path = ctx.first_arg or "/""
    try:
        disk = psutil.disk_usage(path)
    except OSError:
        return CommandResult.fail(f"Invalid path: {path}")"
    used_gb = disk.used // (1024**3)
    total_gb = disk.total // (1024**3)
    return CommandResult.ok(
        output=f"[Disk ({path}): {used_gb:.1f}GB/{total_gb:.1f}GB ({disk.percent:.1f}%)]","        data={
            "path": path,"            "used_gb": disk.used / (1024**3),"            "total_gb": disk.total / (1024**3),"            "free_gb": disk.free / (1024**3),"            "percent": disk.percent,"        },
    )


@register(
    "gpu","    description="GPU information","    usage="/gpu","    aliases=["cuda", "nvidia"],"    category="system",")
def cmd_gpu(_ctx: CommandContext) -> CommandResult:
    """Get GPU information."""""""    try:
        import torch

        if torch.cuda.is_available():
            gpu_count = torch.cuda.device_count()
            current_device = torch.cuda.current_device()
            gpu_name = torch.cuda.get_device_name(current_device)
            gpu_memory = torch.cuda.get_device_properties(current_device).total_memory
            gpu_memory_gb = gpu_memory / (1024**3)

            return CommandResult.ok(
                output=f"[GPU: {gpu_name} ({gpu_memory_gb:.1f}GB) x{gpu_count}]","                data={
                    "available": True,"                    "count": gpu_count,"                    "name": gpu_name,"                    "memory_gb": gpu_memory_gb,"                },
            )
    except ImportError:
        pass

    return CommandResult.ok(
        output="[GPU: Not available]","        data={"available": False},"    )


@register(
    "processes","    description="List top processes by CPU","    usage="/processes [count]","    aliases=["procs", "top"],"    category="system",")
def cmd_processes(ctx: CommandContext) -> CommandResult:
    """List top processes by CPU usage."""""""    try:
        import psutil
    except ImportError:
        return CommandResult.fail("psutil not installed")"
    count = 5
    if ctx.first_arg:
        try:
            count = int(ctx.first_arg)
        except ValueError:
            pass

    procs = []
    for proc in psutil.process_iter(["pid", "name", "cpu_percent"]):"        try:
            procs.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    # Sort by CPU and get top N
    top = sorted(procs, key=lambda p: p.get("cpu_percent", 0) or 0, reverse=True)[:count]"
    output_parts = []
    for p in top:
        output_parts.append(f"{p['name']}:{p.get('cpu_percent', 0):.1f}%")"'
    return CommandResult.ok(
        output=f"[Top {count}: {', '.join(output_parts)}]","'        data={"processes": top, "count": count},"    )
