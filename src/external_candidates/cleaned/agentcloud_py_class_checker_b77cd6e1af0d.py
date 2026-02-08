# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agentcloud.py\agent_backend.py\src.py\utils.py\class_checker_b77cd6e1af0d.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agentcloud\agent-backend\src\utils\class_checker.py

from typing import Any, Type


def check_instance_of_class(instance: Any, class_type: Type[Any]) -> Any:
    if not isinstance(instance, class_type):
        raise AssertionError(f"Expected instance of {class_type.__name__}, got {type(instance).__name__}")

    return instance
