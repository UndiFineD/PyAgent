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
"""Validation tests for mobile-responsive-nebula-os (prj0000058).

Each test validates file content — no running server required.
"""

from pathlib import Path

WEB_DIR = Path(__file__).parent.parent / "web"
STYLES_DIR = WEB_DIR / "styles"


def _find_responsive_css() -> Path | None:
    """Return the first CSS file in web/ that contains a media query."""
    for css in WEB_DIR.rglob("*.css"):
        if "@media" in css.read_text(encoding="utf-8"):
            return css
    return None


def test_web_contains_css_with_responsive_media_queries():
    """Test 1: web/ has a CSS file with @media responsive queries."""
    css_file = _find_responsive_css()
    assert css_file is not None, (
        "No CSS file with @media queries found under web/. Expected web/styles/responsive.css or similar."
    )
    content = css_file.read_text(encoding="utf-8")
    assert "@media" in content


def test_responsive_css_has_mobile_max_width_768():
    """Test 2: The responsive CSS file has a max-width: 768px breakpoint."""
    css_file = _find_responsive_css()
    assert css_file is not None, "No responsive CSS file found."
    content = css_file.read_text(encoding="utf-8")
    assert "768px" in content, "Expected a max-width: 768px mobile breakpoint in the responsive CSS."
    assert "max-width" in content


def test_responsive_css_has_tablet_breakpoint():
    """Test 3: The responsive CSS file has a tablet breakpoint (769px or 1024px)."""
    css_file = _find_responsive_css()
    assert css_file is not None, "No responsive CSS file found."
    content = css_file.read_text(encoding="utf-8")
    has_tablet = "1024px" in content or "769px" in content
    assert has_tablet, "Expected a tablet breakpoint (769px or 1024px) in the responsive CSS."


def test_app_tsx_imports_or_references_responsive_styles():
    """Test 4: web/App.tsx imports responsive styles or index.tsx imports responsive CSS."""
    app_tsx = WEB_DIR / "App.tsx"
    index_tsx = WEB_DIR / "index.tsx"
    assert app_tsx.exists() or index_tsx.exists(), "Neither App.tsx nor index.tsx found."
    found = False
    for candidate in [app_tsx, index_tsx]:
        if candidate.exists():
            content = candidate.read_text(encoding="utf-8")
            if "responsive" in content.lower() or "nebula-desktop" in content or "nebula-taskbar" in content:
                found = True
                break
    assert found, (
        "Expected web/App.tsx or web/index.tsx to reference responsive styles "
        "(import 'responsive', 'nebula-desktop', or 'nebula-taskbar')."
    )


def test_responsive_css_has_at_least_3_rules_for_window_or_taskbar():
    """Test 5: The responsive CSS contains at least 3 rules targeting .nebula-window or .nebula-taskbar."""
    css_file = _find_responsive_css()
    assert css_file is not None, "No responsive CSS file found."
    content = css_file.read_text(encoding="utf-8")
    window_count = content.count(".nebula-window")
    taskbar_count = content.count(".nebula-taskbar")
    total = window_count + taskbar_count
    assert total >= 3, (
        f"Expected at least 3 rules targeting .nebula-window or .nebula-taskbar, "
        f"found {total} (.nebula-window={window_count}, .nebula-taskbar={taskbar_count})."
    )
