# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""
ChatTemplateRegistry Facade.

This module provides a backward-compatible interface to the modularized
chat template registry implementation.
"""

from .registry import (
    TemplateType,
    TemplateConfig,
    RenderOptions,
    MODEL_TEMPLATE_MAP,
    DEFAULT_CONFIG,
    ChatTemplate,
    JinjaTemplate,
    ChatTemplateRegistry,
    TemplateResolver,
    register_template,
    get_template,
    render_template,
    detect_template_type,
)

__all__ = [
    "TemplateType",
    "TemplateConfig",
    "RenderOptions",
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
