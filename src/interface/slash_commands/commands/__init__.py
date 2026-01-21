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
