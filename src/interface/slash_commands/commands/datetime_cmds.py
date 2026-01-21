"""
DateTime commands - date, time, datetime, uptime.
"""

import time
from datetime import datetime, timezone

from src.interface.slash_commands.registry import register
from src.interface.slash_commands.core import CommandContext, CommandResult

# Track start time for uptime
_start_time = time.time()


@register(
    "datetime",
    description="Get current server date and time",
    usage="/datetime",
    aliases=["dt", "now"],
    category="datetime",
)
def cmd_datetime(ctx: CommandContext) -> CommandResult:
    """Get current date and time in UTC."""
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


@register(
    "date",
    description="Get current server date",
    usage="/date",
    category="datetime",
)
def cmd_date(ctx: CommandContext) -> CommandResult:
    """Get current date."""
    now = datetime.now(timezone.utc)
    return CommandResult.ok(
        output=f"[{now.strftime('%Y-%m-%d')}]",
        data={"date": now.strftime('%Y-%m-%d'), "iso": now.date().isoformat()},
    )


@register(
    "time",
    description="Get current server time",
    usage="/time",
    category="datetime",
)
def cmd_time(ctx: CommandContext) -> CommandResult:
    """Get current time."""
    now = datetime.now(timezone.utc)
    return CommandResult.ok(
        output=f"[{now.strftime('%H:%M:%S')} UTC]",
        data={"time": now.strftime('%H:%M:%S'), "timezone": "UTC"},
    )


@register(
    "uptime",
    description="Get process uptime",
    usage="/uptime",
    aliases=["up"],
    category="datetime",
)
def cmd_uptime(ctx: CommandContext) -> CommandResult:
    """Get process uptime."""
    uptime_seconds = time.time() - _start_time

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


@register(
    "timestamp",
    description="Get Unix timestamp",
    usage="/timestamp",
    aliases=["ts", "epoch"],
    category="datetime",
)
def cmd_timestamp(ctx: CommandContext) -> CommandResult:
    """Get current Unix timestamp."""
    now = time.time()
    return CommandResult.ok(
        output=f"[{int(now)}]",
        data={"timestamp": now, "timestamp_int": int(now)},
    )
