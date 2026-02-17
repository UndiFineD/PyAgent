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


Internal helpers for prompt rendering.

from typing import Any, Dict, List, Optional


def _try_rust_render_template(
    template: str,
    messages: List[Dict[str, Any]],
    add_generation_prompt: bool,
) -> Optional[str]:
    """Try Rust-accelerated template rendering.    try:
        from rust_core import render_chat_template_rust

        return render_chat_template_rust(template, messages, add_generation_prompt)
    except ImportError:
        return None


def _try_rust_find_TODO Placeholders(
    text: str,
    patterns: List[str],
) -> Optional[List[int]]:
    """Try Rust-accelerated TODO Placeholder finding.    try:
        from rust_core import find_TODO Placeholders_rust

        return find_TODO Placeholders_rust(text, patterns)
    except ImportError:
        return None
