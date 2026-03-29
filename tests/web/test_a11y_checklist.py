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
"""Static source-level WCAG 2.1 AA accessibility checklist for the NebulaOS dark theme.
prj0000071 — dark-mode-accessibility
"""

import pathlib

_WEB = pathlib.Path("web")


def _read(path: str) -> str:
    return (_WEB / path).read_text(encoding="utf-8")


# ── Window.tsx ──────────────────────────────────────────────────────────────


def test_window_minimize_has_aria_label() -> None:
    """Minimize button must have an accessible name."""
    assert 'aria-label="Minimize"' in _read("components/Window.tsx")


def test_window_maximize_restore_has_aria_label() -> None:
    """Maximize/Restore button must advertise its dynamic accessible name."""
    content = _read("components/Window.tsx")
    assert "'Restore'" in content and "'Maximize'" in content, (
        "Maximize/Restore button needs dynamic aria-label with both states"
    )


def test_window_close_has_aria_label() -> None:
    """Close button must have an accessible name."""
    assert 'aria-label="Close"' in _read("components/Window.tsx")


def test_window_menu_has_aria_label() -> None:
    """Menu button must have an accessible name."""
    assert 'aria-label="Window menu"' in _read("components/Window.tsx")


def test_window_controls_have_focus_visible_ring() -> None:
    """Window control buttons must have a visible focus indicator for keyboard users."""
    assert "focus-visible:ring-" in _read("components/Window.tsx")


# ── Paint.tsx ────────────────────────────────────────────────────────────────


def test_paint_pencil_has_aria_label() -> None:
    """Pencil tool button must have an accessible name."""
    assert 'aria-label="Pencil"' in _read("apps/Paint.tsx")


def test_paint_eraser_has_aria_label() -> None:
    """Eraser tool button must have an accessible name."""
    assert 'aria-label="Eraser"' in _read("apps/Paint.tsx")


def test_paint_clear_has_aria_label() -> None:
    """Clear-canvas button must have an accessible name."""
    assert 'aria-label="Clear canvas"' in _read("apps/Paint.tsx")


def test_paint_color_input_has_aria_label() -> None:
    """Colour picker input must have an accessible name."""
    assert 'aria-label="Stroke colour"' in _read("apps/Paint.tsx")


def test_paint_range_input_has_aria_label() -> None:
    """Stroke-width range input must have an accessible name."""
    assert 'aria-label="Stroke width"' in _read("apps/Paint.tsx")


# ── Editor.tsx ───────────────────────────────────────────────────────────────


def test_editor_textarea_has_focus_ring() -> None:
    """Editor textarea must not suppress focus ring without a replacement."""
    content = _read("apps/Editor.tsx")
    assert "focus:ring-2" in content, "Editor textarea is missing a visible focus ring"


# ── App.tsx ───────────────────────────────────────────────────────────────────


def test_app_toggle_has_focus_ring() -> None:
    """Taskbar toggle switch must have a visible focus ring."""
    content = _read("App.tsx")
    # The toggle uses focus:ring-2 focus:ring-blue-400
    assert "focus:ring-2" in content, "Toggle switch is missing a visible focus ring"


# ── ProjectManager.tsx ────────────────────────────────────────────────────────


def test_project_card_has_role_button() -> None:
    """Project card must declare its interactive role for assistive technology."""
    assert 'role="button"' in _read("apps/ProjectManager.tsx")


def test_project_card_has_tab_index() -> None:
    """Project card must be keyboard-focusable."""
    assert "tabIndex={0}" in _read("apps/ProjectManager.tsx")


def test_project_card_has_keyboard_handler() -> None:
    """Project card must respond to Enter and Space key presses."""
    content = _read("apps/ProjectManager.tsx")
    assert "onKeyDown" in content, "Project card is missing onKeyDown keyboard handler"
    assert "'Enter'" in content or '"Enter"' in content, "onKeyDown must handle Enter key"
    assert "' '" in content or '" "' in content or "'Space'" in content or '"Space"' in content or "' '" in content, (
        "onKeyDown must handle Space key"
    )


def test_project_card_has_aria_expanded() -> None:
    """Project card must communicate expanded/collapsed state."""
    assert "aria-expanded" in _read("apps/ProjectManager.tsx")


# ── themes.css ────────────────────────────────────────────────────────────────


def test_accent_colour_passes_aa_contrast() -> None:
    """--color-accent must be #f25e77 (≥ 4.5:1 contrast against --color-bg #1a1a2e)."""
    content = _read("styles/themes.css")
    assert "--color-accent: #f25e77" in content, (
        "--color-accent must be #f25e77 for WCAG AA contrast; found something else"
    )
