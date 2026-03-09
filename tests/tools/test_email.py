#!/usr/bin/env python3
"""Tests for the email templating helper in the pm package."""

from tools.pm import email


def test_render_status_email():
    tpl = "Hello {{name}}"
    out = email.render(tpl, {"name": "Alice"})
    assert "Alice" in out
