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
"""Validation tests for prj0000061: CSS custom-property theme system."""

from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
THEMES_CSS = REPO_ROOT / "web" / "styles" / "themes.css"
USE_THEME_HOOK = REPO_ROOT / "web" / "hooks" / "useTheme.ts"
THEME_SELECTOR = REPO_ROOT / "web" / "components" / "ThemeSelector.tsx"


def test_themes_css_exists():
    """themes.css must be present in web/styles/."""
    assert THEMES_CSS.exists(), f"Expected {THEMES_CSS} to exist"


def test_themes_css_has_three_themes():
    """themes.css must define the dark (:root), light, and retro theme contexts."""
    content = THEMES_CSS.read_text(encoding="utf-8")
    assert ":root" in content, "themes.css must contain :root block"
    assert 'data-theme="light"' in content, 'themes.css must contain [data-theme="light"] selector'
    assert 'data-theme="retro"' in content, 'themes.css must contain [data-theme="retro"] selector'


def test_themes_css_uses_css_variables():
    """themes.css must define CSS custom properties (--color-bg at minimum)."""
    content = THEMES_CSS.read_text(encoding="utf-8")
    assert "--color-bg" in content, "themes.css must define --color-bg custom property"


def test_use_theme_hook_exists():
    """useTheme.ts hook must be present in web/hooks/."""
    assert USE_THEME_HOOK.exists(), f"Expected {USE_THEME_HOOK} to exist"


def test_theme_selector_component_exists():
    """ThemeSelector.tsx component must be present in web/components/."""
    assert THEME_SELECTOR.exists(), f"Expected {THEME_SELECTOR} to exist"
