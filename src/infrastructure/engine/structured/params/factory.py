# Copyright (c) 2026 PyAgent Authors. All rights reserved.
from typing import Any, Dict, List, Optional
from .enums import StructuredOutputType
from .config import StructuredOutputConfig

def create_json_constraint(
    schema: Optional[Dict[str, Any]] = None,
    properties: Optional[Dict[str, Dict[str, Any]]] = None,
    required: Optional[List[str]] = None,
) -> StructuredOutputConfig:
    """Create a JSON schema constraint configuration."""
    if schema is None:
        schema = {"type": "object"}

        if properties:
            schema["properties"] = properties

        if required:
            schema["required"] = required

    return StructuredOutputConfig(
        output_type=StructuredOutputType.JSON_SCHEMA,
        json_schema=schema,
    )

def create_regex_constraint(
    pattern: str,
    flags: int = 0,
) -> StructuredOutputConfig:
    """Create a regex constraint configuration."""
    return StructuredOutputConfig(
        output_type=StructuredOutputType.REGEX,
        regex=pattern,
    )

def create_choice_constraint(
    choices: List[str],
) -> StructuredOutputConfig:
    """Create a choice constraint configuration."""
    return StructuredOutputConfig(
        output_type=StructuredOutputType.CHOICE,
        choices=choices,
    )

def combine_constraints(
    *configs: StructuredOutputConfig,
) -> StructuredOutputConfig:
    """
    Combine multiple constraint configurations.
    """
    if not configs:
        return StructuredOutputConfig()

    # Start with first config
    combined = StructuredOutputConfig(
        output_type=StructuredOutputType.COMPOSITE,
        backend=configs[0].backend,
        whitespace=configs[0].whitespace,
    )

    # Collect all constraints
    for config in configs:
        constraints = config.get_all_constraints()
        combined.additional_constraints.extend(constraints)

    # Use strictest mode
    combined.strict_mode = any(c.strict_mode for c in configs)

    return combined
