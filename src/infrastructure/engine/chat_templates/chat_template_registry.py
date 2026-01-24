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
ChatTemplateRegistry Facade.

This module provides a backward-compatible interface to the modularized
chat template registry implementation.
"""

from .registry import (DEFAULT_CONFIG, MODEL_TEMPLATE_MAP, ChatTemplate,
                       ChatTemplateRegistry, JinjaTemplate, ModelType,
                       RenderOptions, TemplateConfig, TemplateInfo,
                       TemplateResolver, TemplateType, detect_template_type,
                       get_template, register_template, render_template)

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
