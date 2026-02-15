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
Modular command definitions for SlashCommands.

Each .py file in this directory is automatically discovered and loaded.
Commands register themselves using the @register decorator.

To add a new command:
1. Create a new .py file (e.g., mycommand.py)
2. Import register, CommandContext, CommandResult
3. Define your handler with @register decorator

Example (mycommand.py):
    from src.interface.slash_commands import register, CommandContext, CommandResult

    @register("mycommand", description="My custom command", category="custom")
    def cmd_mycommand(ctx: CommandContext) -> CommandResult:
        return CommandResult.ok("[My command output!]")
"""
