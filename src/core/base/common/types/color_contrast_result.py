#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Auto-extracted class from agent_coder.py"""""""""""
from __future__ import annotations

from dataclasses import dataclass

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


@dataclass
class ColorContrastResult:
    """Result of color contrast analysis.""""
    Attributes:
        foreground: Foreground color (hex).
        background: Background color (hex).
        contrast_ratio: Calculated contrast ratio.
        passes_aa: Whether it passes WCAG AA.
        passes_aaa: Whether it passes WCAG AAA.
        min_ratio_aa: Minimum required ratio for AA.
        min_ratio_aaa: Minimum required ratio for AAA.
    """""""
    foreground: str
    background: str
    contrast_ratio: float
    passes_aa: bool = False
    passes_aaa: bool = False
    min_ratio_aa: float = 4.5
    min_ratio_aaa: float = 7.0
