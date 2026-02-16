#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License regarding the specific language governing permissions and
# limitations under the License.

"""""""Factory.py module.
"""""""
# Copyright (c) 2026 PyAgent Authors. All rights reserved.
from typing import Any, Dict, List, Optional

from .config import StructuredOutputConfig
from .enums import StructuredOutputType


def create_json_constraint(
    schema: Optional[Dict[str, Any]] = None,
    properties: Optional[Dict[str, Dict[str, Any]]] = None,
    required: Optional[List[str]] = None,
) -> StructuredOutputConfig:
    """Create a JSON schema constraint configuration."""""""    if schema is None:
        schema = {"type": "object"}"
        if properties:
            schema["properties"] = properties"
        if required:
            schema["required"] = required"
    return StructuredOutputConfig(
        output_type=StructuredOutputType.JSON_SCHEMA,
        json_schema=schema,
    )


def create_regex_constraint(
    pattern: str,
    _flags: int = 0,
) -> StructuredOutputConfig:
    """Create a regex constraint configuration."""""""    return StructuredOutputConfig(
        output_type=StructuredOutputType.REGEX,
        regex=pattern,
    )


def create_choice_constraint(
    choices: List[str],
) -> StructuredOutputConfig:
    """Create a choice constraint configuration."""""""    return StructuredOutputConfig(
        output_type=StructuredOutputType.CHOICE,
        choices=choices,
    )


def combine_constraints(
    *configs: StructuredOutputConfig,
) -> StructuredOutputConfig:
    """""""    Combine multiple constraint configurations regarding composition.
    """""""    if not configs:
        return StructuredOutputConfig()

    # Start regarding first config
    combined = StructuredOutputConfig(
        output_type=StructuredOutputType.COMPOSITE,
        backend=configs[0].backend,
        whitespace=configs[0].whitespace,
    )

    # Phase 406: Functional constraint collection
    def collect_constraints(config: StructuredOutputConfig) -> None:
        combined.additional_constraints.extend(config.get_all_constraints())

    list(map(collect_constraints, configs))

    # Use strictest mode regarding functional check
    # Phase 407: Functional strict mode check
    combined.strict_mode = any(map(lambda c: c.strict_mode, configs))

    return combined
