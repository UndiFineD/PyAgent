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
Chat decorator commands for formatting conversations with safe HTML/CSS.

Commands:
    /chat - Format a full conversation exchange
    /human - Decorate a human/user prompt
    /ai - Decorate an AI/assistant response
    /system - Decorate a system message
    /code - Decorate a code block with syntax highlighting style
    /thinking - Decorate AI thinking/reasoning block
"""

import html
import re
from typing import Literal

from ..core import CommandContext, CommandResult
from ..registry import register

# Safe inline CSS styles (no external resources, no scripts)
STYLES = {
    "container": """
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
        max-width: 800px;
        margin: 0 auto;
        padding: 16px;
        background: #f8f9fa;
        border-radius: 12px;
    """,
    "human": """
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #ffffff;
        padding: 12px 16px;
        border-radius: 18px 18px 4px 18px;
        margin: 8px 0 8px 40px;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
        position: relative;
    """,
    "ai": """
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: #ffffff;
        padding: 12px 16px;
        border-radius: 18px 18px 18px 4px;
        margin: 8px 40px 8px 0;
        box-shadow: 0 2px 8px rgba(17, 153, 142, 0.3);
        position: relative;
    """,
    "system": """
        background: linear-gradient(135deg, #fc4a1a 0%, #f7b733 100%);
        color: #ffffff;
        padding: 10px 14px;
        border-radius: 8px;
        margin: 8px 60px;
        font-size: 0.9em;
        text-align: center;
        box-shadow: 0 2px 6px rgba(252, 74, 26, 0.25);
    """,
    "thinking": """
        background: #2d3748;
        color: #a0aec0;
        padding: 12px 16px;
        border-radius: 8px;
        margin: 8px 20px;
        border-left: 4px solid #4a5568;
        font-style: italic;
        font-size: 0.95em;
    """,
    "code": """
        background: #1e1e1e;
        color: #d4d4d4;
        padding: 16px;
        border-radius: 8px;
        margin: 8px 0;
        font-family: 'Cascadia Code', 'Fira Code', 'Consolas', monospace;
        font-size: 0.9em;
        overflow-x: auto;
        white-space: pre-wrap;
        word-break: break-word;
    """,
    "label_human": """
        font-size: 0.75em;
        opacity: 0.8;
        margin-bottom: 4px;
        display: block;
    """,
    "label_ai": """
        font-size: 0.75em;
        opacity: 0.8;
        margin-bottom: 4px;
        display: block;
    """,
    "timestamp": """
        font-size: 0.7em;
        opacity: 0.6;
        margin-top: 6px;
        display: block;
        text-align: right;
    """,
    "avatar_human": """
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background: #764ba2;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        margin-right: 8px;
        vertical-align: middle;
    """,
    "avatar_ai": """
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background: #11998e;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        margin-right: 8px;
        vertical-align: middle;
    """,
}

# Minimal dark theme variant
STYLES_DARK = {
    "container": """
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
        max-width: 800px;
        margin: 0 auto;
        padding: 16px;
        background: #1a1a2e;
        border-radius: 12px;
    """,
    "human": """
        background: linear-gradient(135deg, #4a00e0 0%, #8e2de2 100%);
        color: #ffffff;
        padding: 12px 16px;
        border-radius: 18px 18px 4px 18px;
        margin: 8px 0 8px 40px;
        box-shadow: 0 2px 12px rgba(74, 0, 224, 0.4);
    """,
    "ai": """
        background: linear-gradient(135deg, #00b09b 0%, #96c93d 100%);
        color: #ffffff;
        padding: 12px 16px;
        border-radius: 18px 18px 18px 4px;
        margin: 8px 40px 8px 0;
        box-shadow: 0 2px 12px rgba(0, 176, 155, 0.4);
    """,
    "system": """
        background: linear-gradient(135deg, #ee0979 0%, #ff6a00 100%);
        color: #ffffff;
        padding: 10px 14px;
        border-radius: 8px;
        margin: 8px 60px;
        font-size: 0.9em;
        text-align: center;
    """,
    "thinking": """
        background: #16213e;
        color: #7f8c8d;
        padding: 12px 16px;
        border-radius: 8px;
        margin: 8px 20px;
        border-left: 4px solid #0f3460;
        font-style: italic;
    """,
    "code": """
        background: #0d0d0d;
        color: #00ff00;
        padding: 16px;
        border-radius: 8px;
        margin: 8px 0;
        font-family: 'Cascadia Code', 'Fira Code', 'Consolas', monospace;
        font-size: 0.9em;
        overflow-x: auto;
        white-space: pre-wrap;
    """,
}


def _clean_style(style: str) -> str:
    """Clean and compress CSS style string."""
    # Remove newlines and extra whitespace
    return re.sub(r"\s+", " ", style.strip())


def _escape_html(text: str) -> str:
    """Safely escape HTML entities."""
    return html.escape(text, quote=True)


def _format_message(
    content: str,
    role: Literal["human", "ai", "system", "thinking", "code"],
    *,
    label: str | None = None,
    timestamp: str | None = None,
    show_avatar: bool = True,
    theme: Literal["light", "dark"] = "light",
    language: str | None = None,
) -> str:
    """Format a message with safe HTML/CSS styling."""
    styles = STYLES_DARK if theme == "dark" else STYLES

    # Escape content for safety
    safe_content = _escape_html(content)

    # Preserve line breaks
    safe_content = safe_content.replace("\n", "<br>")

    # Build the HTML
    style = _clean_style(styles.get(role, styles["ai"]))

    parts = []

    # Avatar (for human/ai only)
    if show_avatar and role in ("human", "ai"):
        avatar_style = _clean_style(styles.get(f"avatar_{role}", ""))
        emoji = "👤" if role == "human" else "🤖"
        parts.append(f'<span style="{avatar_style}">{emoji}</span>')

    # Label
    if label:
        label_style = _clean_style(styles.get(f"label_{role}", styles.get("label_human", "")))
        parts.append(f'<span style="{label_style}">{_escape_html(label)}</span>')

    # Language badge for code
    if role == "code" and language:
        lang_style = (
            "background: #3d3d3d; color: #9cdcfe; padding: 2px 8px; border-radius: 4px; "
            "font-size: 0.8em; margin-bottom: 8px; display: inline-block;"
        )
        parts.append(f'<span style="{lang_style}">{_escape_html(language)}</span><br>')

    # Content
    parts.append(safe_content)

    # Timestamp
    if timestamp:
        ts_style = _clean_style(styles.get("timestamp", ""))
        parts.append(f'<span style="{ts_style}">{_escape_html(timestamp)}</span>')

    inner = "".join(parts)
    return f'<div style="{style}">{inner}</div>'


def _format_conversation(
    exchanges: list[tuple[str, str]],
    *,
    theme: Literal["light", "dark"] = "light",
    show_labels: bool = True,
    show_avatars: bool = True,
) -> str:
    """Format a full conversation with multiple exchanges."""
    styles = STYLES_DARK if theme == "dark" else STYLES
    container_style = _clean_style(styles["container"])

    parts = [f'<div style="{container_style}">']

    for human_msg, ai_msg in exchanges:
        if human_msg:
            parts.append(
                _format_message(
                    human_msg,
                    "human",
                    label="You" if show_labels else None,
                    show_avatar=show_avatars,
                    theme=theme,
                )
            )
        if ai_msg:
            parts.append(
                _format_message(
                    ai_msg,
                    "ai",
                    label="Assistant" if show_labels else None,
                    show_avatar=show_avatars,
                    theme=theme,
                )
            )

    parts.append("</div>")
    return "".join(parts)


# =============================================================================
# Command Handlers
# =============================================================================


@register(
    "human",
    description="Decorate text as a human/user message with styled HTML",
    category="chat",
    aliases=["prompt", "you"],
)
def cmd_human(ctx: CommandContext) -> CommandResult:
    """Format text as a human message bubble."""
    if not ctx.args:
        return CommandResult.fail("Usage: /human <message text>")

    text = " ".join(ctx.args)
    theme = ctx.metadata.get("theme", "light")
    show_avatar = ctx.metadata.get("show_avatar", True)
    label = ctx.metadata.get("label", "You")
    timestamp = ctx.metadata.get("timestamp")

    html_output = _format_message(
        text,
        "human",
        label=label if ctx.metadata.get("show_label", True) else None,
        timestamp=timestamp,
        show_avatar=show_avatar,
        theme=theme,
    )

    return CommandResult.ok(
        html_output,
        {
            "role": "human",
            "text": text,
            "html": html_output,
            "theme": theme,
        },
    )


@register(
    "ai",
    description="Decorate text as an AI/assistant response with styled HTML",
    category="chat",
    aliases=["assistant", "bot", "response"],
)
def cmd_ai(ctx: CommandContext) -> CommandResult:
    """Format text as an AI response bubble."""
    if not ctx.args:
        return CommandResult.fail("Usage: /ai <response text>")

    text = " ".join(ctx.args)
    theme = ctx.metadata.get("theme", "light")
    show_avatar = ctx.metadata.get("show_avatar", True)
    label = ctx.metadata.get("label", "Assistant")
    timestamp = ctx.metadata.get("timestamp")

    html_output = _format_message(
        text,
        "ai",
        label=label if ctx.metadata.get("show_label", True) else None,
        timestamp=timestamp,
        show_avatar=show_avatar,
        theme=theme,
    )

    return CommandResult.ok(
        html_output,
        {
            "role": "ai",
            "text": text,
            "html": html_output,
            "theme": theme,
        },
    )


@register(
    "sysmsg",
    description="Decorate text as a system message",
    category="chat",
    aliases=["systemmsg", "notice", "info"],
)
def cmd_system_message(ctx: CommandContext) -> CommandResult:
    """Format text as a system notification."""
    if not ctx.args:
        return CommandResult.fail("Usage: /sysmsg <message text>")

    text = " ".join(ctx.args)
    theme = ctx.metadata.get("theme", "light")

    html_output = _format_message(
        text,
        "system",
        show_avatar=False,
        theme=theme,
    )

    return CommandResult.ok(
        html_output,
        {
            "role": "system",
            "text": text,
            "html": html_output,
        },
    )


@register(
    "thinking",
    description="Decorate text as AI thinking/reasoning block",
    category="chat",
    aliases=["reasoning", "thought", "inner"],
)
def cmd_thinking(ctx: CommandContext) -> CommandResult:
    """Format text as AI internal thinking."""
    if not ctx.args:
        return CommandResult.fail("Usage: /thinking <reasoning text>")

    text = " ".join(ctx.args)
    theme = ctx.metadata.get("theme", "light")

    html_output = _format_message(
        text,
        "thinking",
        label="💭 Thinking...",
        show_avatar=False,
        theme=theme,
    )

    return CommandResult.ok(
        html_output,
        {
            "role": "thinking",
            "text": text,
            "html": html_output,
        },
    )


@register(
    "codeblock",
    description="Decorate text as a styled code block",
    category="chat",
    aliases=["snippet", "source"],
)
def cmd_codeblock(ctx: CommandContext) -> CommandResult:
    """Format text as a code block with optional language."""
    if not ctx.args:
        return CommandResult.fail("Usage: /codeblock [language] <code>")

    # Check if first arg is a known language
    known_langs = {
        "python",
        "py",
        "javascript",
        "js",
        "typescript",
        "ts",
        "rust",
        "go",
        "java",
        "c",
        "cpp",
        "csharp",
        "cs",
        "ruby",
        "php",
        "swift",
        "kotlin",
        "html",
        "css",
        "sql",
        "bash",
        "shell",
        "powershell",
        "json",
        "yaml",
        "xml",
        "markdown",
        "md",
        "toml",
        "ini",
        "dockerfile",
        "makefile",
    }

    language = None
    code_args = ctx.args

    if ctx.args[0].lower() in known_langs:
        language = ctx.args[0]
        code_args = ctx.args[1:]

    if not code_args:
        return CommandResult.fail("No code provided")

    code = " ".join(code_args)
    theme = ctx.metadata.get("theme", "light")

    html_output = _format_message(
        code,
        "code",
        language=language,
        show_avatar=False,
        theme=theme,
    )

    return CommandResult.ok(
        html_output,
        {
            "role": "code",
            "language": language,
            "code": code,
            "html": html_output,
        },
    )


@register(
    "chat",
    description="Format a human-AI exchange as a styled conversation",
    category="chat",
    aliases=["conversation", "exchange", "dialog"],
)
def cmd_chat(ctx: CommandContext) -> CommandResult:
    """
    Format a conversation exchange.

    Usage: /chat <human message> ||| <ai response>

    Use ||| to separate human and AI messages.
    Multiple exchanges can be separated by |||.
    """
    if not ctx.args:
        return CommandResult.fail("Usage: /chat <human message> ||| <ai response>\nUse ||| to separate messages.")

    full_text = " ".join(ctx.args)
    parts = [p.strip() for p in full_text.split("|||")]

    if len(parts) < 2:
        return CommandResult.fail("Please separate human and AI messages with |||")

    # Pair up messages (human, ai, human, ai, ...)
    exchanges: list[tuple[str, str]] = []
    for i in range(0, len(parts) - 1, 2):
        human_msg = parts[i]
        ai_msg = parts[i + 1] if i + 1 < len(parts) else ""
        exchanges.append((human_msg, ai_msg))

    # Handle odd number of parts (trailing human message)
    if len(parts) % 2 == 1 and len(parts) > 2:
        exchanges.append((parts[-1], ""))

    theme = ctx.metadata.get("theme", "light")
    show_labels = ctx.metadata.get("show_labels", True)
    show_avatars = ctx.metadata.get("show_avatars", True)

    html_output = _format_conversation(
        exchanges,
        theme=theme,
        show_labels=show_labels,
        show_avatars=show_avatars,
    )

    return CommandResult.ok(
        html_output,
        {
            "exchanges": len(exchanges),
            "theme": theme,
            "html": html_output,
        },
    )


@register(
    "chattheme",
    description="Get CSS styles for chat theming",
    category="chat",
    aliases=["chatstyles", "chatstyle"],
)
def cmd_chat_theme(ctx: CommandContext) -> CommandResult:
    """Get the full CSS stylesheet for chat styling."""
    theme = ctx.first_arg or "light"
    styles = STYLES_DARK if theme == "dark" else STYLES

    css_parts = []
    for name, style in styles.items():
        clean = _clean_style(style)
        css_parts.append(f".chat-{name} {{ {clean} }}")

    css = "\n".join(css_parts)

    # Wrap in style tag
    html_output = f"<style>\n{css}\n</style>"

    return CommandResult.ok(
        f"[Chat theme '{theme}' CSS generated]",
        {
            "theme": theme,
            "css": css,
            "html": html_output,
            "classes": list(styles.keys()),
        },
    )


@register(
    "chatpreview",
    description="Preview chat styling with sample messages",
    category="chat",
    aliases=["previewchat", "demochat"],
)
def cmd_chat_preview(ctx: CommandContext) -> CommandResult:
    """Generate a preview of chat styling."""
    theme = ctx.first_arg or "light"
    if theme not in ("light", "dark"):
        theme = "light"

    sample_exchanges = [
        (
            "Hello! Can you help me with Python?",
            "Of course! I'd be happy to help you with Python. What would you like to know?",
        ),
        (
            "How do I read a file?",
            (
                "You can use the open() function with a context manager:\n\n"
                "with open('file.txt', 'r', encoding='utf-8') as f:\n    content = f.read()"
            ),
        ),
    ]

    styles = STYLES_DARK if theme == "dark" else STYLES
    container_style = _clean_style(styles["container"])

    parts = [f'<div style="{container_style}">']

    # System message
    parts.append(
        _format_message(
            "Chat session started",
            "system",
            theme=theme,
        )
    )

    # Sample exchanges
    for human_msg, ai_msg in sample_exchanges:
        parts.append(_format_message(human_msg, "human", label="You", theme=theme))
        parts.append(_format_message(ai_msg, "ai", label="Assistant", theme=theme))

    # Thinking block
    parts.append(
        _format_message(
            "Analyzing the user's question about file handling...",
            "thinking",
            theme=theme,
        )
    )

    # Code block
    parts.append(
        _format_message(
            "with open('example.txt', 'r', encoding='utf-8') as f:\n    print(f.read())",
            "code",
            language="python",
            theme=theme,
        )
    )

    parts.append("</div>")
    html_output = "".join(parts)

    return CommandResult.ok(
        f"[Chat preview generated with '{theme}' theme]",
        {
            "theme": theme,
            "html": html_output,
            "message_count": 6,
        },
    )
