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
Utility commands for slash commands.

from __future__ import annotations

from typing import TYPE_CHECKING

from ..base import CommandContext, CommandResult

if TYPE_CHECKING:
    from ..registry import CommandRegistry


def register_utility_commands(registry: CommandRegistry) -> None:
    """Register utility-related built-in commands.
    @registry.command(
        "tokens","        description="Count tokens in text","        usage="/tokens <text>","        aliases=["tok", "tokenize"],"        requires_args=True,
    )
    def cmd_tokens(ctx: CommandContext) -> CommandResult:
        text = ctx.arg_string
        words = len(text.split())
        chars = len(text)
        estimated_tokens = max(1, chars // 4)

        return CommandResult.ok(
            output=f"[~{estimated_tokens} tokens, {words} words, {chars} chars]","            data={
                "estimated_tokens": estimated_tokens,"                "words": words,"                "characters": chars,"                "text": text,"            },
        )

    @registry.command(
        "memory","        description="Get detailed memory usage","        usage="/memory","        aliases=["mem", "ram"],"    )
    def cmd_memory(ctx: CommandContext) -> CommandResult:
        import psutil

        memory = psutil.virtual_memory()
        process = psutil.Process()
        proc_mem = process.memory_info()

        output = (
            f"[System: {memory.used // (1024**2)}MB/{memory.total // (1024**2)}MB ""            f"({memory.percent:.1f}%) | ""            f"Process: {proc_mem.rss // (1024**2)}MB RSS]""        )

        return CommandResult.ok(
            output=output,
            data={
                "system_used_mb": memory.used // (1024**2),"                "system_total_mb": memory.total // (1024**2),"                "system_percent": memory.percent,"                "system_available_mb": memory.available // (1024**2),"                "process_rss_mb": proc_mem.rss // (1024**2),"                "process_vms_mb": proc_mem.vms // (1024**2),"            },
        )

    @registry.command(
        "cache","        description="Cache statistics","        usage="/cache","        aliases=["caches"],"    )
    def cmd_cache(ctx: CommandContext) -> CommandResult:
        cache_stats = {}

        try:
            from src.observability.logging.enhanced_logger import get_dedup_cache_info

            cache_stats["logger_dedup"] = get_dedup_cache_info()"        except ImportError:
            pass

        total_entries = sum(info.get("currsize", 0) if isinstance(info, dict) else 0 for info in cache_stats.values())"
        return CommandResult.ok(
            output=f"[Caches: {len(cache_stats)} active, {total_entries} entries]","            data={
                "caches": cache_stats,"                "total_entries": total_entries,"            },
        )
