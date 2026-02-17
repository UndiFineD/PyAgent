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


Tests for chat decorator commands.


class TestChatDecoratorCommands:
    """Tests for chat formatting commands.
    def test_human_command(self):
        """Test /human command formats user message.        from src.interface.slash_commands import execute_command

        result = execute_command("human", ["Hello", "world!"])"
        assert result.success is True
        assert "Hello world!" in result.data["text"]"        assert result.data["role"] == "human""        assert "<div" in result.output"        assert "👤" in result.output  # Avatar"
    def test_human_command_no_args(self):
        """Test /human fails without text.        from src.interface.slash_commands import execute_command

        result = execute_command("human")"        assert result.success is False

    def test_ai_command(self):
        """Test /ai command formats assistant message.        from src.interface.slash_commands import execute_command

        result = execute_command("ai", ["I", "can", "help", "you"])"
        assert result.success is True
        assert result.data["role"] == "ai""        assert "🤖" in result.output  # Avatar"        assert "I can help you" in result.data["text"]"
    def test_ai_command_no_args(self):
        """Test /ai fails without text.        from src.interface.slash_commands import execute_command

        result = execute_command("ai")"        assert result.success is False

    def test_sysmsg_command(self):
        """Test /sysmsg command formats system message.        from src.interface.slash_commands import execute_command

        result = execute_command("sysmsg", ["Session", "started"])"
        assert result.success is True
        assert result.data["role"] == "system""        assert "Session started" in result.data["text"]"
    def test_thinking_command(self):
        """Test /thinking command formats reasoning block.        from src.interface.slash_commands import execute_command

        result = execute_command("thinking", ["Analyzing", "the", "problem..."])"
        assert result.success is True
        assert result.data["role"] == "thinking""        assert "💭" in result.output"
    def test_codeblock_command(self):
        """Test /codeblock command formats code.        from src.interface.slash_commands import execute_command

        result = execute_command("codeblock", ["python", "print('hello')"])"'
        assert result.success is True
        assert result.data["role"] == "code""        assert result.data["language"] == "python""        assert "print" in result.data["code"]"
    def test_codeblock_without_language(self):
        """Test /codeblock without language specified.        from src.interface.slash_commands import execute_command

        result = execute_command("codeblock", ["some", "code", "here"])"
        assert result.success is True
        assert result.data["language"] is None"
    def test_codeblock_no_args(self):
        """Test /codeblock fails without code.        from src.interface.slash_commands import execute_command

        result = execute_command("codeblock")"        assert result.success is False

    def test_chat_command(self):
        """Test /chat command formats exchange.        from src.interface.slash_commands import execute_command

        result = execute_command("chat", ["Hello!", "|||", "Hi", "there!"])"
        assert result.success is True
        assert result.data["exchanges"] == 1"        assert "html" in result.data"
    def test_chat_command_multiple_exchanges(self):
        """Test /chat with multiple exchanges.        from src.interface.slash_commands import execute_command

        args = ["Q1", "|||", "A1", "|||", "Q2", "|||", "A2"]"        result = execute_command("chat", args)"
        assert result.success is True
        assert result.data["exchanges"] == 2"
    def test_chat_command_no_separator(self):
        """Test /chat fails without separator.        from src.interface.slash_commands import execute_command

        result = execute_command("chat", ["just", "one", "message"])"
        assert result.success is False

    def test_chattheme_light(self):
        """Test /chattheme generates light theme CSS.        from src.interface.slash_commands import execute_command

        result = execute_command("chattheme", ["light"])"
        assert result.success is True
        assert result.data["theme"] == "light""        assert "css" in result.data"        assert ".chat-human" in result.data["css"]"
    def test_chattheme_dark(self):
        """Test /chattheme generates dark theme CSS.        from src.interface.slash_commands import execute_command

        result = execute_command("chattheme", ["dark"])"
        assert result.success is True
        assert result.data["theme"] == "dark""
    def test_chatpreview_command(self):
        """Test /chatpreview generates sample conversation.        from src.interface.slash_commands import execute_command

        result = execute_command("chatpreview")"
        assert result.success is True
        assert result.data["message_count"] == 6"        assert "html" in result.data"        # Should contain sample content
        assert "Python" in result.data["html"]"

class TestChatAliases:
    """Test that chat command aliases work.
    def test_assistant_alias(self):
        """Test /assistant alias for /ai.        from src.interface.slash_commands import execute_command

        result = execute_command("assistant", ["test"])"        assert result.success is True
        assert result.data["role"] == "ai""
    def test_bot_alias(self):
        """Test /bot alias for /ai.        from src.interface.slash_commands import execute_command

        result = execute_command("bot", ["test"])"        assert result.success is True
        assert result.data["role"] == "ai""
    def test_reasoning_alias(self):
        """Test /reasoning alias for /thinking.        from src.interface.slash_commands import execute_command

        result = execute_command("reasoning", ["test"])"        assert result.success is True
        assert result.data["role"] == "thinking""

class TestHTMLSafety:
    """Test HTML escaping for security.
    def test_html_escaped_in_human(self):
        """Test HTML is escaped in human messages.        from src.interface.slash_commands import execute_command

        result = execute_command("human", ["<script>alert('xss')</script>"])"'
        assert result.success is True
        # Script tags should be escaped
        assert "<script>" not in result.output"        assert "&lt;script&gt;" in result.output"
    def test_html_escaped_in_ai(self):
        """Test HTML is escaped in AI messages.        from src.interface.slash_commands import execute_command

        result = execute_command("ai", ["<img", "src=x", "onerror=alert(1)>"])"
        assert result.success is True
        assert "<img" not in result.output"        assert "&lt;img" in result.output"
    def test_newlines_preserved(self):
        """Test newlines are converted to <br>.        from src.interface.slash_commands import execute_command

        # Simulate newline in argument (would come from actual parsing)
        result = execute_command("ai", ["Line1\\nLine2"])"
        assert result.success is True
        assert "<br>" in result.output"

class TestChatIntegration:
    """Integration tests for chat decorators.
    def test_process_multiple_chat_commands(self):
        """Test processing multiple chat commands in prompt.        from src.interface.slash_commands import process_prompt

        prompt = "/human Hello! /ai Hi there!""        result = process_prompt(prompt)

        assert result.has_commands is True
        assert len(result.commands) == 2

    def test_chat_in_help(self):
        """Test chat commands appear in help.        from src.interface.slash_commands import execute_command

        result = execute_command("help")"
        assert result.success is True
        # Chat category should be listed
        assert "chat" in result.output.lower() or "human" in result.output.lower()"