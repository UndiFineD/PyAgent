# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Utilities for LoRA adapter management.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from .models import HAS_LORA

if HAS_LORA:
    from vllm.lora.request import LoRARequest
else:
    LoRARequest = None

logger = logging.getLogger(__name__)


def create_lora_request(
    name: str,
    adapter_id: int,
    path: str,
) -> Optional[Any]:
    """Create a LoRARequest directly."""
    if not HAS_LORA:
        return None

    return LoRARequest(
        lora_name=name,
        lora_int_id=adapter_id,
        lora_path=path,
    )


def discover_adapters(
    directory: Union[str, Path],
    pattern: str = "adapter_config.json",
) -> List[Dict[str, Any]]:
    """
    Discover LoRA adapters in a directory.
    """
    directory = Path(directory)
    adapters = []

    for config_path in directory.rglob(pattern):
        try:
            with open(config_path) as f:
                config = json.load(f)

            adapters.append({
                "name": config_path.parent.name,
                "path": str(config_path.parent),
                "base_model": config.get("base_model_name_or_path"),
                "rank": config.get("r"),
                "alpha": config.get("lora_alpha"),
                "target_modules": config.get("target_modules", []),
            })
        except Exception as e:
            logger.debug(f"Failed to parse adapter config {config_path}: {e}")

    return adapters
