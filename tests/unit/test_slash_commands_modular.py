"""
Tests for modular SlashCommands system.
"""

import os
import re
from unittest.mock import patch

import pytest


class TestParseCommands:
    """Tests for command parsing."""

    def test_parse_single_command(self):
        """Test parsing a single command."""
        from src.interface.slash_commands import parse_commands

        result = parse_commands("/datetime")
        assert len(result) == 1
        assert result[0].command == "datetime"
        assert result[0].args == []

    def test_parse_command_with_args(self):
        """Test parsing command with arguments."""
        from src.interface.slash_commands import parse_commands

        result = parse_commands("/tokens hello world")
        assert len(result) == 1
        assert result[0].command == "tokens"
        assert result[0].args == ["hello", "world"]

    def test_parse_command_in_text(self):
        """Test parsing command embedded in text."""
        from src.interface.slash_commands import parse_commands

        result = parse_commands("What is /datetime right now?")
        assert len(result) == 1
        assert result[0].command == "datetime"

    def test_parse_multiple_commands(self):
        """Test parsing multiple commands."""
        from src.interface.slash_commands import parse_commands

        result = parse_commands("/datetime /stats /version")
        assert len(result) == 3
        assert result[0].command == "datetime"
        assert result[1].command == "stats"
        assert result[2].command == "version"

    def test_parse_no_commands(self):
        """Test parsing text without commands."""
        from src.interface.slash_commands import parse_commands

        result = parse_commands("No commands here")
        assert len(result) == 0


class TestCommandResult:
    """Tests for CommandResult."""

    def test_ok_result(self):
        """Test creating OK result."""
        from src.interface.slash_commands import CommandResult

        result = CommandResult.ok("Hello", {"key": "value"})
        assert result.success is True
        assert result.output == "Hello"
        assert result.data == {"key": "value"}

    def test_fail_result(self):
        """Test creating fail result."""
        from src.interface.slash_commands import CommandResult

        result = CommandResult.fail("Something went wrong")
        assert result.success is False
        assert result.error == "Something went wrong"


class TestCommandRegistry:
    """Tests for CommandRegistry."""

    def test_register_command(self):
        """Test registering a command."""
        from src.interface.slash_commands import CommandRegistry, CommandContext, CommandResult

        registry = CommandRegistry()

        def handler(ctx: CommandContext) -> CommandResult:
            return CommandResult.ok("test")

        registry.register("test", handler, description="Test command")

        defn = registry.get("test")
        assert defn is not None
        assert defn.name == "test"

    def test_register_with_aliases(self):
        """Test registering command with aliases."""
        from src.interface.slash_commands import CommandRegistry, CommandContext, CommandResult

        registry = CommandRegistry()

        def handler(ctx: CommandContext) -> CommandResult:
            return CommandResult.ok("test")

        registry.register("test", handler, aliases=["t", "tst"])

        assert registry.get("test") is not None
        assert registry.get("t") is not None
        assert registry.get("tst") is not None

    def test_unregister_command(self):
        """Test unregistering a command."""
        from src.interface.slash_commands import CommandRegistry, CommandContext, CommandResult

        registry = CommandRegistry()

        def handler(ctx: CommandContext) -> CommandResult:
            return CommandResult.ok("test")

        registry.register("test", handler, aliases=["t"])
        assert registry.get("test") is not None

        registry.unregister("test")
        assert registry.get("test") is None
        assert registry.get("t") is None

    def test_enable_disable_command(self):
        """Test enabling/disabling commands."""
        from src.interface.slash_commands import CommandRegistry, CommandContext, CommandResult

        registry = CommandRegistry()

        def handler(ctx: CommandContext) -> CommandResult:
            return CommandResult.ok("test")

        registry.register("test", handler)
        assert registry.is_enabled("test") is True

        registry.disable("test")
        assert registry.get("test") is None  # Disabled, not accessible
        assert registry.get_all("test") is not None  # But still exists

        registry.enable("test")
        assert registry.get("test") is not None

    def test_list_by_category(self):
        """Test listing commands by category."""
        from src.interface.slash_commands import CommandRegistry, CommandContext, CommandResult

        registry = CommandRegistry()

        def handler(ctx: CommandContext) -> CommandResult:
            return CommandResult.ok("test")

        registry.register("cmd1", handler, category="system")
        registry.register("cmd2", handler, category="system")
        registry.register("cmd3", handler, category="utility")

        system_cmds = registry.list_commands(category="system")
        assert len(system_cmds) == 2

        utility_cmds = registry.list_commands(category="utility")
        assert len(utility_cmds) == 1


class TestSlashCommands:
    """Tests for SlashCommands class."""

    def test_execute_datetime(self):
        """Test executing /datetime command."""
        from src.interface.slash_commands import SlashCommands

        slash = SlashCommands()
        result = slash.execute("datetime")

        assert result.success is True
        assert "UTC" in result.output

    def test_execute_date(self):
        """Test executing /date command."""
        from src.interface.slash_commands import SlashCommands

        slash = SlashCommands()
        result = slash.execute("date")

        assert result.success is True
        assert re.match(r'\[\d{4}-\d{2}-\d{2}\]', result.output)

    def test_execute_version(self):
        """Test executing /version command."""
        from src.interface.slash_commands import SlashCommands

        slash = SlashCommands()
        result = slash.execute("version")

        assert result.success is True
        assert "Python" in result.output

    def test_execute_uptime(self):
        """Test executing /uptime command."""
        from src.interface.slash_commands import SlashCommands

        slash = SlashCommands()
        result = slash.execute("uptime")

        assert result.success is True
        assert "Uptime" in result.output

    def test_execute_tokens(self):
        """Test executing /tokens command."""
        from src.interface.slash_commands import SlashCommands

        slash = SlashCommands()
        result = slash.execute("tokens", ["hello", "world"])

        assert result.success is True
        assert result.data["words"] == 2

    def test_execute_tokens_requires_args(self):
        """Test /tokens fails without args."""
        from src.interface.slash_commands import SlashCommands

        slash = SlashCommands()
        result = slash.execute("tokens")

        assert result.success is False

    def test_execute_env(self):
        """Test executing /env command."""
        from src.interface.slash_commands import SlashCommands

        slash = SlashCommands()

        with patch.dict(os.environ, {"TEST_VAR": "test_value"}):
            result = slash.execute("env", ["TEST_VAR"])
            assert result.success is True
            assert "test_value" in result.output

    def test_execute_unknown_command(self):
        """Test executing unknown command."""
        from src.interface.slash_commands import SlashCommands

        slash = SlashCommands()
        result = slash.execute("unknowncommand123")

        assert result.success is False

    def test_execute_uuid(self):
        """Test executing /uuid command."""
        from src.interface.slash_commands import SlashCommands

        slash = SlashCommands()
        result = slash.execute("uuid")

        assert result.success is True
        assert re.match(r'\[[a-f0-9-]{36}\]', result.output)

    def test_execute_random(self):
        """Test executing /random command."""
        from src.interface.slash_commands import SlashCommands

        slash = SlashCommands()
        result = slash.execute("random", ["10"])

        assert result.success is True
        assert 1 <= result.data["value"] <= 10

    def test_alias_resolution(self):
        """Test that aliases work."""
        from src.interface.slash_commands import SlashCommands

        slash = SlashCommands()

        # /dt is alias for /datetime
        result = slash.execute("dt")
        assert result.success is True
        assert "UTC" in result.output


class TestProcessPrompt:
    """Tests for processing full prompts."""

    def test_process_single_command(self):
        """Test processing prompt with single command."""
        from src.interface.slash_commands import SlashCommands

        slash = SlashCommands()
        result = slash.process("What time is it? /datetime")

        assert result.has_commands is True
        assert len(result.commands) == 1

    def test_process_multiple_commands(self):
        """Test processing prompt with multiple commands."""
        from src.interface.slash_commands import SlashCommands

        slash = SlashCommands()
        result = slash.process("/datetime /version")

        assert len(result.commands) == 2
        assert result.all_succeeded is True

    def test_process_no_commands(self):
        """Test processing prompt without commands."""
        from src.interface.slash_commands import SlashCommands

        slash = SlashCommands()
        result = slash.process("Just regular text here")

        assert result.has_commands is False


class TestConvenienceFunctions:
    """Tests for module-level convenience functions."""

    def test_get_slash_commands(self):
        """Test getting default instance."""
        from src.interface.slash_commands import get_slash_commands

        slash = get_slash_commands()
        assert slash is not None

    def test_process_prompt_function(self):
        """Test process_prompt function."""
        from src.interface.slash_commands import process_prompt

        result = process_prompt("/datetime")
        assert result.has_commands is True

    def test_execute_command_function(self):
        """Test execute_command function."""
        from src.interface.slash_commands import execute_command

        result = execute_command("version")
        assert result.success is True


class TestModularLoader:
    """Tests for command module loading."""

    def test_discover_modules(self):
        """Test discovering command modules."""
        from src.interface.slash_commands.loader import discover_command_modules

        modules = discover_command_modules()
        assert len(modules) > 0
        assert "datetime_cmds" in modules
        assert "system" in modules
        assert "utility" in modules

    def test_load_commands(self):
        """Test loading all commands."""
        from src.interface.slash_commands.loader import load_commands, get_loaded_modules

        count = load_commands()
        assert count > 0

        loaded = get_loaded_modules()
        assert len(loaded) > 0


class TestCustomCommands:
    """Tests for registering custom commands."""

    def test_register_custom_command(self):
        """Test registering a custom command."""
        from src.interface.slash_commands import (
            register_command,
            execute_command,
            CommandContext,
            CommandResult,
        )

        def custom_handler(ctx: CommandContext) -> CommandResult:
            return CommandResult.ok("[Custom executed!]")

        register_command("mycustom", custom_handler, description="My custom command")

        result = execute_command("mycustom")
        assert result.success is True
        assert "Custom" in result.output

    def test_register_decorator(self):
        """Test @register decorator."""
        from src.interface.slash_commands import (
            register,
            execute_command,
            CommandContext,
            CommandResult,
        )

        @register("decorated_cmd", description="Decorated command")
        def cmd_decorated(ctx: CommandContext) -> CommandResult:
            return CommandResult.ok("[Decorated!]")

        result = execute_command("decorated_cmd")
        assert result.success is True


class TestSystemCommands:
    """Tests for system commands (require psutil)."""

    @pytest.fixture(autouse=True)
    def check_psutil(self):
        """Skip if psutil not available."""
        pytest.importorskip("psutil")

    def test_stats_command(self):
        """Test /stats command."""
        from src.interface.slash_commands import SlashCommands

        slash = SlashCommands()
        result = slash.execute("stats")

        assert result.success is True
        assert "CPU" in result.output

    def test_memory_command(self):
        """Test /memory command."""
        from src.interface.slash_commands import SlashCommands

        slash = SlashCommands()
        result = slash.execute("memory")

        assert result.success is True
        assert "System" in result.output

    def test_health_command(self):
        """Test /health command."""
        from src.interface.slash_commands import SlashCommands

        slash = SlashCommands()
        result = slash.execute("health")

        assert result.success is True
        assert "Health" in result.output


class TestUtilityCommands:
    """Tests for utility commands."""

    def test_echo(self):
        """Test /echo command."""
        from src.interface.slash_commands import execute_command

        result = execute_command("echo", ["hello", "world"])
        assert result.success is True
        assert "hello world" in result.output

    def test_hash(self):
        """Test /hash command."""
        from src.interface.slash_commands import execute_command

        result = execute_command("hash", ["test"])
        assert result.success is True
        assert "hash" in result.data

    def test_base64(self):
        """Test /base64 command."""
        from src.interface.slash_commands import execute_command

        result = execute_command("base64", ["hello"])
        assert result.success is True
        assert result.data["encoded"] == "aGVsbG8="

    def test_choice(self):
        """Test /choice command."""
        from src.interface.slash_commands import execute_command

        result = execute_command("choice", ["a", "b", "c"])
        assert result.success is True
        assert result.data["choice"] in ["a", "b", "c"]

    def test_upper_lower(self):
        """Test /upper and /lower commands."""
        from src.interface.slash_commands import execute_command

        result = execute_command("upper", ["hello"])
        assert result.data["text"] == "HELLO"

        result = execute_command("lower", ["HELLO"])
        assert result.data["text"] == "hello"


class TestEnvironmentCommands:
    """Tests for environment commands."""

    def test_hostname(self):
        """Test /hostname command."""
        from src.interface.slash_commands import execute_command

        result = execute_command("hostname")
        assert result.success is True
        assert "hostname" in result.data

    def test_user(self):
        """Test /user command."""
        from src.interface.slash_commands import execute_command

        result = execute_command("user")
        assert result.success is True
        assert "username" in result.data

    def test_venv(self):
        """Test /venv command."""
        from src.interface.slash_commands import execute_command

        result = execute_command("venv")
        assert result.success is True
        assert "active" in result.data


class TestDateTimeCommands:
    """Tests for datetime commands."""

    def test_timestamp(self):
        """Test /timestamp command."""
        from src.interface.slash_commands import execute_command

        result = execute_command("timestamp")
        assert result.success is True
        assert "timestamp" in result.data
        assert result.data["timestamp"] > 0
