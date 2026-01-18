# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""
Chat template registry package for Jinja2 and custom template management.
"""

from .config import (
    TemplateType,
    TemplateConfig,
    RenderOptions,
    MODEL_TEMPLATE_MAP,
    DEFAULT_CONFIG,
)
from .base import ChatTemplate
from .jinja import JinjaTemplate
from .registry import ChatTemplateRegistry
from .resolver import TemplateResolver
from .utils import (
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
