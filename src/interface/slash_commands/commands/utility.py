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
Utility commands - tokens, uuid, random, help.
"""

import random as random_module
import uuid as uuid_module

from src.interface.slash_commands.core import CommandContext, CommandResult
from src.interface.slash_commands.registry import get_global_registry, register


@register(
    "tokens",
    description="Count tokens in text",
    usage="/tokens <text>",
    aliases=["tok", "tokenize"],
    requires_args=True,
    category="utility",
)
def cmd_tokens(ctx: CommandContext) -> CommandResult:
    """Estimate token count for text."""
    text = ctx.arg_string

    # Simple token estimation (words + punctuation)
    # For accurate counts, would need tiktoken/tokenizers
    words = len(text.split())
    chars = len(text)

    # Rough estimate: ~4 chars per token for English
    estimated_tokens = max(1, chars // 4)

    return CommandResult.ok(
        output=f"[~{estimated_tokens} tokens, {words} words, {chars} chars]",
        data={
            "estimated_tokens": estimated_tokens,
            "words": words,
            "characters": chars,
            "text": text,
        },
    )


@register(
    "uuid",
    description="Generate a UUID",
    usage="/uuid",
    aliases=["id", "guid"],
    category="utility",
)
def cmd_uuid(ctx: CommandContext) -> CommandResult:
    """Generate a new UUID."""
    new_uuid = str(uuid_module.uuid4())
    return CommandResult.ok(
        output=f"[{new_uuid}]",
        data={"uuid": new_uuid},
    )


@register(
    "random",
    description="Generate random number",
    usage="/random [max]",
    aliases=["rand", "rnd"],
    category="utility",
)
def cmd_random(ctx: CommandContext) -> CommandResult:
    """Generate random number."""
    max_val = 100
    min_val = 1

    if ctx.first_arg:
        try:
            max_val = int(ctx.first_arg)
        except ValueError:
            pass

    if len(ctx.args) >= 2:
        try:
            min_val = int(ctx.args[0])
            max_val = int(ctx.args[1])
        except ValueError:
            pass

    value = random_module.randint(min_val, max_val)
    return CommandResult.ok(
        output=f"[{value}]",
        data={"value": value, "min": min_val, "max": max_val},
    )


@register(
    "choice",
    description="Random choice from options",
    usage="/choice option1 option2 ...",
    aliases=["pick", "choose"],
    requires_args=True,
    category="utility",
)
def cmd_choice(ctx: CommandContext) -> CommandResult:
    """Pick a random choice from arguments."""
    if not ctx.args:
        return CommandResult.fail("Provide options to choose from")

    chosen = random_module.choice(ctx.args)
    return CommandResult.ok(
        output=f"[{chosen}]",
        data={"choice": chosen, "options": ctx.args},
    )


@register(
    "hash",
    description="Hash text with SHA256",
    usage="/hash <text>",
    aliases=["sha256"],
    requires_args=True,
    category="utility",
)
def cmd_hash(ctx: CommandContext) -> CommandResult:
    """Hash text using SHA256."""
    import hashlib

    text = ctx.arg_string
    hash_value = hashlib.sha256(text.encode()).hexdigest()

    return CommandResult.ok(
        output=f"[{hash_value[:16]}...]",
        data={"hash": hash_value, "algorithm": "sha256", "input": text},
    )


@register(
    "base64",
    description="Base64 encode text",
    usage="/base64 <text>",
    aliases=["b64"],
    requires_args=True,
    category="utility",
)
def cmd_base64(ctx: CommandContext) -> CommandResult:
    """Base64 encode text."""
    import base64

    text = ctx.arg_string
    encoded = base64.b64encode(text.encode()).decode()

    return CommandResult.ok(
        output=f"[{encoded}]",
        data={"encoded": encoded, "original": text},
    )


@register(
    "length",
    description="Get text length",
    usage="/length <text>",
    aliases=["len"],
    requires_args=True,
    category="utility",
)
def cmd_length(ctx: CommandContext) -> CommandResult:
    """Get length of text."""
    text = ctx.arg_string

    return CommandResult.ok(
        output=f"[{len(text)} chars]",
        data={"length": len(text), "text": text},
    )


@register(
    "help",
    description="Show help for commands",
    usage="/help [command]",
    aliases=["h", "?"],
    category="utility",
)
def cmd_help(ctx: CommandContext) -> CommandResult:
    """Get help for commands."""
    registry = get_global_registry()

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
                "category": defn.category,
            },
        )

    # List all commands by category
    categories = registry.list_categories()
    all_commands = []

    for cat in categories:
        commands = registry.list_commands(category=cat)
        all_commands.extend([c.name for c in commands])

    return CommandResult.ok(
        output=f"[Commands: {', '.join('/' + c for c in sorted(all_commands))}]",
        data={"commands": sorted(all_commands), "categories": categories},
        inline=False,
    )


@register(
    "echo",
    description="Echo text back",
    usage="/echo <text>",
    category="utility",
)
def cmd_echo(ctx: CommandContext) -> CommandResult:
    """Echo the input text."""
    text = ctx.arg_string or ""
    return CommandResult.ok(
        output=f"[{text}]" if text else "[]",
        data={"text": text},
    )


@register(
    "upper",
    description="Convert to uppercase",
    usage="/upper <text>",
    aliases=["uppercase"],
    requires_args=True,
    category="utility",
)
def cmd_upper(ctx: CommandContext) -> CommandResult:
    """Convert text to uppercase."""
    text = ctx.arg_string.upper()
    return CommandResult.ok(output=f"[{text}]", data={"text": text})


@register(
    "lower",
    description="Convert to lowercase",
    usage="/lower <text>",
    aliases=["lowercase"],
    requires_args=True,
    category="utility",
)
def cmd_lower(ctx: CommandContext) -> CommandResult:
    """Convert text to lowercase."""
    text = ctx.arg_string.lower()
    return CommandResult.ok(output=f"[{text}]", data={"text": text})
