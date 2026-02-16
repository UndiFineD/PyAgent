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
Cache and observability commands.
"""

from ..core import CommandContext, CommandResult
from ..registry import register


@register(
    "cache",
    description="Cache statistics",
    usage="/cache",
    aliases=["caches"],
    category="observability",
)
def cmd_cache(_ctx: CommandContext) -> CommandResult:
    """Get cache statistics."""
    cache_stats = {}

    # Check for common caches
    try:
        from src.observability.logging.enhanced_logger import \
            get_dedup_cache_info

        cache_stats["logger_dedup"] = get_dedup_cache_info()
    except ImportError:
        pass

    total_entries = sum(info.get("currsize", 0) if isinstance(info, dict) else 0 for info in cache_stats.values())

    return CommandResult.ok(
        output=f"[Caches: {len(cache_stats)} active, {total_entries} entries]",
        data={
            "caches": cache_stats,
            "total_entries": total_entries,
        },
    )


@register(
    "counters",
    description="Show structured counters",
    usage="/counters",
    aliases=["metrics"],
    category="observability",
)
def cmd_counters(_ctx: CommandContext) -> CommandResult:
    """Get structured counter statistics."""
    # This would typically access global counter instances
    # For now, show available counter types
    counter_types = ["RequestCounter", "CacheCounter", "PoolCounter", "QueueCounter"]

    return CommandResult.ok(
        output=f"[Counter types: {', '.join(counter_types)}]",
        data={"types": counter_types},
    )


@register(
    "telemetry",
    description="Show telemetry info",
    usage="/telemetry",
    aliases=["usage"],
    category="observability",
)
def cmd_telemetry(_ctx: CommandContext) -> CommandResult:
    """Get telemetry/usage information."""
    try:
        from src.observability.telemetry.usage_message import (
            detect_cloud_provider, get_platform_summary,
            is_usage_stats_enabled)

        provider = detect_cloud_provider()
        enabled = is_usage_stats_enabled()
        summary = get_platform_summary()

        return CommandResult.ok(
            output=f"[Provider: {provider}, Stats: {'enabled' if enabled else 'disabled'}]",
            data={
                "provider": provider,
                "stats_enabled": enabled,
                "platform": summary,
            },
        )
    except ImportError:
        return CommandResult.ok(
            output="[Telemetry: Module not available]",
            data={"available": False},
        )


@register(
    "logs",
    description="Show log deduplication stats",
    usage="/logs",
    aliases=["logstats"],
    category="observability",
)
def cmd_logs(_ctx: CommandContext) -> CommandResult:
    """Get log deduplication statistics."""
    try:
        from src.observability.logging.enhanced_logger import \
            get_dedup_cache_info

        info = get_dedup_cache_info()

        return CommandResult.ok(
            output=f"[Log dedup caches: {len(info)} levels]",
            data={"caches": info},
        )
    except ImportError:
        return CommandResult.ok(
            output="[Logs: Enhanced logger not available]",
            data={"available": False},
        )
