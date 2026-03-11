#!/usr/bin/env python3
"""Tests for the email templating helper in the pm package."""

from tools.pm import email


def test_render_status_email() -> None:
    """Test that the render function can process a simple template."""
    tpl = "Hello {{name}}"
    import asyncio
    out = asyncio.run(email.render(tpl, {"name": "Alice"}))
    assert "Alice" in out
