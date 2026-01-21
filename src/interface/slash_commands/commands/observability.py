"""
Cache and observability commands.
"""

from src.interface.slash_commands.registry import register
from src.interface.slash_commands.core import CommandContext, CommandResult


@register(
    "cache",
    description="Cache statistics",
    usage="/cache",
    aliases=["caches"],
    category="observability",
)
def cmd_cache(ctx: CommandContext) -> CommandResult:
    """Get cache statistics."""
    cache_stats = {}
    
    # Check for common caches
    try:
        from src.observability.logging.enhanced_logger import get_dedup_cache_info
        cache_stats["logger_dedup"] = get_dedup_cache_info()
    except ImportError:
        pass
    
    total_entries = sum(
        info.get("currsize", 0) if isinstance(info, dict) else 0 
        for info in cache_stats.values()
    )
    
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
def cmd_counters(ctx: CommandContext) -> CommandResult:
    """Get structured counter statistics."""
    try:
        from src.observability.stats.structured_counter import (
            RequestCounter,
            CacheCounter,
        )
        
        # This would typically access global counter instances
        # For now, show available counter types
        counter_types = ["RequestCounter", "CacheCounter", "PoolCounter", "QueueCounter"]
        
        return CommandResult.ok(
            output=f"[Counter types: {', '.join(counter_types)}]",
            data={"types": counter_types},
        )
    except ImportError:
        return CommandResult.ok(
            output="[Counters: Module not available]",
            data={"available": False},
        )


@register(
    "telemetry",
    description="Show telemetry info",
    usage="/telemetry",
    aliases=["usage"],
    category="observability",
)
def cmd_telemetry(ctx: CommandContext) -> CommandResult:
    """Get telemetry/usage information."""
    try:
        from src.observability.telemetry.usage_message import (
            detect_cloud_provider,
            is_usage_stats_enabled,
            get_platform_summary,
        )
        
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
def cmd_logs(ctx: CommandContext) -> CommandResult:
    """Get log deduplication statistics."""
    try:
        from src.observability.logging.enhanced_logger import get_dedup_cache_info
        
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
