"""
Tests for SlashCommands - Chat prompt slash command parser and executor.
"""

import os
import re
import time
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
    
    def test_parse_commands_with_text_between(self):
        """Test parsing commands with text between them."""
        from src.interface.slash_commands import parse_commands
        
        result = parse_commands("Hello /datetime and /stats please")
        assert len(result) == 2
        assert result[0].command == "datetime"
        assert result[1].command == "stats"
    
    def test_parse_no_commands(self):
        """Test parsing text without commands."""
        from src.interface.slash_commands import parse_commands
        
        result = parse_commands("No commands here")
        assert len(result) == 0
    
    def test_parse_command_positions(self):
        """Test that command positions are recorded."""
        from src.interface.slash_commands import parse_commands
        
        prompt = "Hello /datetime world"
        result = parse_commands(prompt)
        
        assert result[0].start == 6
        assert result[0].end > result[0].start


class TestCommandResult:
    """Tests for CommandResult."""
    
    def test_ok_result(self):
        """Test creating OK result."""
        from src.interface.slash_commands import CommandResult
        
        result = CommandResult.ok("Hello", {"key": "value"})
        assert result.success is True
        assert result.output == "Hello"
        assert result.data == {"key": "value"}
        assert result.error is None
    
    def test_fail_result(self):
        """Test creating fail result."""
        from src.interface.slash_commands import CommandResult
        
        result = CommandResult.fail("Something went wrong")
        assert result.success is False
        assert result.error == "Something went wrong"
        assert "Error" in result.output


class TestCommandContext:
    """Tests for CommandContext."""
    
    def test_arg_string(self):
        """Test arg_string property."""
        from src.interface.slash_commands import CommandContext
        
        ctx = CommandContext(command="test", args=["hello", "world"])
        assert ctx.arg_string == "hello world"
    
    def test_first_arg(self):
        """Test first_arg property."""
        from src.interface.slash_commands import CommandContext
        
        ctx = CommandContext(command="test", args=["first", "second"])
        assert ctx.first_arg == "first"
    
    def test_first_arg_empty(self):
        """Test first_arg with no args."""
        from src.interface.slash_commands import CommandContext
        
        ctx = CommandContext(command="test", args=[])
        assert ctx.first_arg is None


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
        assert defn.description == "Test command"
    
    def test_register_with_aliases(self):
        """Test registering command with aliases."""
        from src.interface.slash_commands import CommandRegistry, CommandContext, CommandResult
        
        registry = CommandRegistry()
        
        def handler(ctx: CommandContext) -> CommandResult:
            return CommandResult.ok("test")
        
        registry.register("test", handler, aliases=["t", "tst"])
        
        # All should resolve to the same command
        assert registry.get("test") is not None
        assert registry.get("t") is not None
        assert registry.get("tst") is not None
    
    def test_command_decorator(self):
        """Test @command decorator."""
        from src.interface.slash_commands import CommandRegistry, CommandContext, CommandResult
        
        registry = CommandRegistry()
        
        @registry.command("greet", description="Greet someone")
        def cmd_greet(ctx: CommandContext) -> CommandResult:
            return CommandResult.ok(f"Hello, {ctx.first_arg or 'world'}!")
        
        defn = registry.get("greet")
        assert defn is not None
        assert defn.description == "Greet someone"
    
    def test_list_commands(self):
        """Test listing commands."""
        from src.interface.slash_commands import CommandRegistry, CommandContext, CommandResult
        
        registry = CommandRegistry()
        
        def handler(ctx: CommandContext) -> CommandResult:
            return CommandResult.ok("test")
        
        registry.register("visible", handler)
        registry.register("hidden", handler, hidden=True)
        
        visible = registry.list_commands(include_hidden=False)
        all_cmds = registry.list_commands(include_hidden=True)
        
        assert len(visible) == 1
        assert len(all_cmds) == 2


class TestSlashCommands:
    """Tests for SlashCommands class."""
    
    def test_execute_datetime(self):
        """Test executing /datetime command."""
        from src.interface.slash_commands import SlashCommands
        
        slash = SlashCommands()
        result = slash.execute("datetime")
        
        assert result.success is True
        assert "UTC" in result.output
        assert "utc" in result.data
        assert "timestamp" in result.data
    
    def test_execute_date(self):
        """Test executing /date command."""
        from src.interface.slash_commands import SlashCommands
        
        slash = SlashCommands()
        result = slash.execute("date")
        
        assert result.success is True
        assert re.match(r'\[\d{4}-\d{2}-\d{2}\]', result.output)
    
    def test_execute_time(self):
        """Test executing /time command."""
        from src.interface.slash_commands import SlashCommands
        
        slash = SlashCommands()
        result = slash.execute("time")
        
        assert result.success is True
        assert "UTC" in result.output
    
    def test_execute_version(self):
        """Test executing /version command."""
        from src.interface.slash_commands import SlashCommands
        
        slash = SlashCommands()
        result = slash.execute("version")
        
        assert result.success is True
        assert "Python" in result.output
        assert "python_version" in result.data
    
    def test_execute_uptime(self):
        """Test executing /uptime command."""
        from src.interface.slash_commands import SlashCommands
        
        slash = SlashCommands()
        result = slash.execute("uptime")
        
        assert result.success is True
        assert "Uptime" in result.output
        assert "uptime_seconds" in result.data
    
    def test_execute_tokens(self):
        """Test executing /tokens command."""
        from src.interface.slash_commands import SlashCommands
        
        slash = SlashCommands()
        result = slash.execute("tokens", ["hello", "world"])
        
        assert result.success is True
        assert "tokens" in result.output.lower()
        assert result.data["words"] == 2
    
    def test_execute_tokens_requires_args(self):
        """Test /tokens fails without args."""
        from src.interface.slash_commands import SlashCommands
        
        slash = SlashCommands()
        result = slash.execute("tokens")
        
        assert result.success is False
        assert "requires arguments" in result.error
    
    def test_execute_env(self):
        """Test executing /env command."""
        from src.interface.slash_commands import SlashCommands
        
        slash = SlashCommands()
        
        # Test with existing var
        with patch.dict(os.environ, {"TEST_VAR": "test_value"}):
            result = slash.execute("env", ["TEST_VAR"])
            assert result.success is True
            assert "test_value" in result.output
    
    def test_execute_env_not_found(self):
        """Test /env with non-existent variable."""
        from src.interface.slash_commands import SlashCommands
        
        slash = SlashCommands()
        result = slash.execute("env", ["NONEXISTENT_VAR_12345"])
        
        assert result.success is True
        assert "not set" in result.output
    
    def test_execute_unknown_command(self):
        """Test executing unknown command."""
        from src.interface.slash_commands import SlashCommands
        
        slash = SlashCommands()
        result = slash.execute("unknowncommand123")
        
        assert result.success is False
        assert "Unknown command" in result.error
    
    def test_execute_help(self):
        """Test executing /help command."""
        from src.interface.slash_commands import SlashCommands
        
        slash = SlashCommands()
        result = slash.execute("help")
        
        assert result.success is True
        assert "commands" in result.data
    
    def test_execute_help_specific(self):
        """Test executing /help for specific command."""
        from src.interface.slash_commands import SlashCommands
        
        slash = SlashCommands()
        result = slash.execute("help", ["datetime"])
        
        assert result.success is True
        assert "datetime" in result.data["name"]
    
    def test_execute_uuid(self):
        """Test executing /uuid command."""
        from src.interface.slash_commands import SlashCommands
        
        slash = SlashCommands()
        result = slash.execute("uuid")
        
        assert result.success is True
        # UUID format check
        assert re.match(r'\[[a-f0-9-]{36}\]', result.output)
    
    def test_execute_random(self):
        """Test executing /random command."""
        from src.interface.slash_commands import SlashCommands
        
        slash = SlashCommands()
        result = slash.execute("random", ["10"])
        
        assert result.success is True
        assert result.data["max"] == 10
        assert 1 <= result.data["value"] <= 10
    
    def test_execute_cwd(self):
        """Test executing /cwd command."""
        from src.interface.slash_commands import SlashCommands
        
        slash = SlashCommands()
        result = slash.execute("cwd")
        
        assert result.success is True
        assert result.data["cwd"] == os.getcwd()
    
    def test_execute_python(self):
        """Test executing /python command."""
        from src.interface.slash_commands import SlashCommands
        import sys
        
        slash = SlashCommands()
        result = slash.execute("python")
        
        assert result.success is True
        assert result.data["executable"] == sys.executable
    
    def test_alias_resolution(self):
        """Test that aliases work."""
        from src.interface.slash_commands import SlashCommands
        
        slash = SlashCommands()
        
        # /dt is alias for /datetime
        result = slash.execute("dt")
        assert result.success is True
        assert "UTC" in result.output
        
        # /ver is alias for /version
        result = slash.execute("ver")
        assert result.success is True
        assert "Python" in result.output


class TestProcessPrompt:
    """Tests for processing full prompts."""
    
    def test_process_single_command(self):
        """Test processing prompt with single command."""
        from src.interface.slash_commands import SlashCommands
        
        slash = SlashCommands()
        result = slash.process("What time is it? /datetime")
        
        assert result.has_commands is True
        assert len(result.commands) == 1
        assert "UTC" in result.processed
    
    def test_process_multiple_commands(self):
        """Test processing prompt with multiple commands."""
        from src.interface.slash_commands import SlashCommands
        
        slash = SlashCommands()
        result = slash.process("/datetime /version")
        
        assert len(result.commands) == 2
        assert result.all_succeeded is True
        assert "UTC" in result.processed
        assert "Python" in result.processed
    
    def test_process_inline_replacement(self):
        """Test that commands are replaced inline."""
        from src.interface.slash_commands import SlashCommands
        
        slash = SlashCommands()
        result = slash.process("Hello /version and more")
        
        # Command should be replaced with output
        assert "/version" not in result.processed
        assert "Python" in result.processed
        assert "Hello" in result.processed
        # Note: text after command until next / or newline becomes args
    
    def test_process_remove_commands(self):
        """Test removing commands from prompt."""
        from src.interface.slash_commands import SlashCommands
        
        slash = SlashCommands()
        result = slash.process("Hello /datetime world", remove_commands=True)
        
        # Command text should be removed
        assert "/datetime" not in result.processed
        # Results should still be captured
        assert result.has_commands is True
    
    def test_process_no_commands(self):
        """Test processing prompt without commands."""
        from src.interface.slash_commands import SlashCommands
        
        slash = SlashCommands()
        result = slash.process("Just regular text here")
        
        assert result.has_commands is False
        assert result.processed == "Just regular text here"
    
    def test_process_command_data(self):
        """Test accessing command data from result."""
        from src.interface.slash_commands import SlashCommands
        
        slash = SlashCommands()
        result = slash.process("/version")
        
        data = result.command_data
        assert "version" in data
        assert "python_version" in data["version"]
    
    def test_process_command_outputs(self):
        """Test accessing command outputs from result."""
        from src.interface.slash_commands import SlashCommands
        
        slash = SlashCommands()
        result = slash.process("/version")
        
        outputs = result.command_outputs
        assert "version" in outputs
        assert "Python" in outputs["version"]


class TestConvenienceFunctions:
    """Tests for module-level convenience functions."""
    
    def test_get_slash_commands(self):
        """Test getting default instance."""
        from src.interface.slash_commands import get_slash_commands
        
        slash = get_slash_commands()
        assert slash is not None
        
        # Should return same instance
        slash2 = get_slash_commands()
        assert slash is slash2
    
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
        assert "Python" in result.output
    
    def test_register_command_function(self):
        """Test register_command function."""
        from src.interface.slash_commands import (
            register_command,
            execute_command,
            CommandContext,
            CommandResult,
        )
        
        def custom_handler(ctx: CommandContext) -> CommandResult:
            return CommandResult.ok("[Custom command executed!]")
        
        register_command("custom_test", custom_handler, description="Test custom")
        
        result = execute_command("custom_test")
        assert result.success is True
        assert "Custom command" in result.output


class TestSystemCommands:
    """Tests for system-related commands (require psutil)."""
    
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
        assert "RAM" in result.output
        assert "cpu_percent" in result.data
    
    def test_memory_command(self):
        """Test /memory command."""
        from src.interface.slash_commands import SlashCommands
        
        slash = SlashCommands()
        result = slash.execute("memory")
        
        assert result.success is True
        assert "System" in result.output
        assert "Process" in result.output
        assert "system_used_mb" in result.data
    
    def test_health_command(self):
        """Test /health command."""
        from src.interface.slash_commands import SlashCommands
        
        slash = SlashCommands()
        result = slash.execute("health")
        
        assert result.success is True
        assert "Health" in result.output
        assert result.data["status"] in ["healthy", "degraded", "unhealthy"]
        assert "score" in result.data


class TestEdgeCases:
    """Tests for edge cases."""
    
    def test_empty_prompt(self):
        """Test processing empty prompt."""
        from src.interface.slash_commands import SlashCommands
        
        slash = SlashCommands()
        result = slash.process("")
        
        assert result.has_commands is False
        assert result.processed == ""
    
    def test_command_only_prompt(self):
        """Test prompt that is just a command."""
        from src.interface.slash_commands import SlashCommands
        
        slash = SlashCommands()
        result = slash.process("/version")
        
        assert result.has_commands is True
        assert "Python" in result.processed
    
    def test_commands_at_line_start(self):
        """Test commands at start of lines."""
        from src.interface.slash_commands import SlashCommands
        
        slash = SlashCommands()
        result = slash.process("/datetime\n/version")
        
        # Both should be parsed
        assert len(result.commands) >= 1
    
    def test_get_help_method(self):
        """Test get_help method."""
        from src.interface.slash_commands import SlashCommands
        
        slash = SlashCommands()
        
        # Help for all commands
        help_all = slash.get_help()
        assert "Available commands" in help_all
        
        # Help for specific command
        help_dt = slash.get_help("datetime")
        assert "datetime" in help_dt
        
        # Unknown command
        help_unknown = slash.get_help("unknownxyz")
        assert "Unknown" in help_unknown
