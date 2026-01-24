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

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""
Chat template registry package for Jinja2 and custom template management.
"""

from .base import ChatTemplate  # noqa: F401
from .config import (DEFAULT_CONFIG, MODEL_TEMPLATE_MAP, ModelType,  # noqa: F401
                     RenderOptions, TemplateConfig, TemplateInfo, TemplateType)
from .jinja import JinjaTemplate  # noqa: F401
from .registry import ChatTemplateRegistry  # noqa: F401
from .resolver import TemplateResolver  # noqa: F401
from .utils import (detect_template_type, get_template, register_template,  # noqa: F401
                    render_template)

__all__ = [
    "TemplateType",
    "TemplateConfig",
    "TemplateInfo",
    "RenderOptions",
    "ModelType",
    "MODEL_TEMPLATE_MAP",
    "DEFAULT_CONFIG",
    "ChatTemplate",
    "JinjaTemplate",
    "ChatTemplateRegistry",
    "TemplateResolver",
    "register_template",
    "get_template",
    "render_template",
    "detect_template_type",
]
