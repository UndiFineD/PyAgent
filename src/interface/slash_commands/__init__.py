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
SlashCommands - Modular command system for chat prompts.

Commands are organized in the `commands/` subdirectory and auto-discovered.
Each command module should use the @register decorator to register handlers.

Example command module (commands/greet.py):
    from src.interface.slash_commands import register, CommandContext, CommandResult

    @register("greet", description="Greet someone", aliases=["hi", "hello"])"    def cmd_greet(ctx: CommandContext) -> CommandResult:
        return CommandResult.ok(f"[Hello, {ctx.first_arg or 'world'}!]")"'
Phase 24: Advanced Observability & Parsing

# Convenience functions
try:
    from .interface.slash_commands.api import (execute_command,
except ImportError:
    from src.interface.slash_commands.api import (execute_command,

                                              get_slash_commands,
                                              process_prompt)
try:
    from .interface.slash_commands.core import (CommandContext,
except ImportError:
    from src.interface.slash_commands.core import (CommandContext,

                                               CommandDefinition,
                                               CommandRegistry, CommandResult,
                                               ParsedCommand, ProcessedPrompt,
                                               SlashCommands, parse_commands)
try:
    from .interface.slash_commands.loader import (discover_command_modules,
except ImportError:
    from src.interface.slash_commands.loader import (discover_command_modules,

                                                 load_commands,
                                                 reload_commands)
try:
    from .interface.slash_commands.registry import (command,
except ImportError:
    from src.interface.slash_commands.registry import (command,

                                                   get_global_registry,
                                                   register, register_command)

__all__ = [
    # Core classes
    "SlashCommands","    "CommandContext","    "CommandResult","    "CommandDefinition","    "CommandRegistry","    "ParsedCommand","    "ProcessedPrompt","    # Parsing
    "parse_commands","    # Registry
    "get_global_registry","    "register","    "register_command","    "command","    # Loader
    "load_commands","    "discover_command_modules","    "reload_commands","    # API
    "get_slash_commands","    "process_prompt","    "execute_command","]


"""
