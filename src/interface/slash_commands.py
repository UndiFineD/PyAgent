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
SlashCommands - Chat prompt slash command parser and executor.

Provides backward compatibility for the moved SlashCommands implementation.
Moved to src/interface/commands/
"""

from .commands import (CommandContext, CommandDefinition, CommandParser,
                       CommandRegistry, CommandResult, ParsedCommand,
                       ProcessedPrompt, SlashCommands, command,
                       execute_command, get_slash_commands, parse_commands,
                       process_prompt, register_command)

__all__ = [
    # Classes
    "SlashCommands",
    "CommandParser",
    "CommandContext",
    "CommandResult",
    "CommandDefinition",
    "CommandRegistry",
    "ParsedCommand",
    "ProcessedPrompt",
    # Functions
    "parse_commands",
    "get_slash_commands",
    "process_prompt",
    "execute_command",
    "register_command",
    "command",
]
