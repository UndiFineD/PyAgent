# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-ovo\ovo\core\utils\param_validation.py
import copy
from pathlib import Path

import jsonschema


def validate_params(params: dict, schema: dict) -> None:
    """Validate input parameters against JSON schema.

    Args:
        params: Dictionary of input parameters.
        schema: JSON schema dictionary.

    Raises:
        jsonschema.ValidationError: If validation fails.
    """
    params = coerce_types(params, schema)
    jsonschema.validate(instance=params, schema=schema)


def coerce_types(params, schema):
    """Auto-convert parameter value types based on JSON schema."""

    # Remove None values, they are not passed to nextflow by scheduler
    params = {k: v for k, v in params.items() if v is not None}

    for key, value in params.items():
        if isinstance(value, Path):
            params[key] = str(value.resolve())
        if key in schema.get("properties", {}):
            prop = schema["properties"][key]
            if "type" in prop:
                target_type = prop["type"]
                if target_type == "integer":
                    try:
                        params[key] = int(value)
                    except (ValueError, TypeError):
                        pass
                elif target_type == "number":
                    try:
                        params[key] = float(value)
                    except (ValueError, TypeError):
                        pass
                elif target_type == "boolean":
                    if isinstance(value, str):
                        if value.lower() in ["true", "1", "yes"]:
                            params[key] = True
                        elif value.lower() in ["false", "0", "no"]:
                            params[key] = False
    return params


def flatten_schema(schema: dict) -> dict:
    """
    Flattens a JSON Schema that uses allOf + definitions into a single-level schema.
    """
    schema = copy.deepcopy(schema)  # don’t mutate original
    root = {
        "type": "object",
        "properties": {},
        "required": [],
        "additionalProperties": schema.get("additionalProperties", False),
    }

    for entry in schema.get("allOf", []):
        if "$ref" in entry:
            ref = entry["$ref"]
            # assumes refs are of the form "#/definitions/NAME"
            _, _, name = ref.partition("#/definitions/")
            definition = schema["definitions"][name]

            # merge properties
            props = definition.get("properties", {})
            root["properties"].update(props)

            # merge required keys
            root["required"].extend(definition.get("required", []))

    # deduplicate required
    root["required"] = list(dict.fromkeys(root["required"]))
    return root
