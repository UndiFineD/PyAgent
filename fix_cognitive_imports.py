#!/usr/bin/env python3
"""Script to fix imports in cognitive agents."""
import os

ROOT = "src/logic/agents/cognitive"
REPLACEMENTS = {
    "from src.logic.mixins.orchestration_mixin": "from src.core.base.mixins.orchestration_mixin",
    "from src.logic.mixins.identity_mixin": "from src.core.base.mixins.identity_mixin",
    "from src.logic.mixins.persistence_mixin": "from src.core.base.mixins.persistence_mixin",
    "from src.logic.mixins.knowledge_mixin": "from src.core.base.mixins.knowledge_mixin",
    "from src.logic.mixins.governance_mixin": "from src.core.base.mixins.governance_mixin",
    "from src.logic.mixins.reflection_mixin": "from src.core.base.mixins.reflection_mixin",
    "from src.logic.mixins.multimodal_mixin": "from src.core.base.mixins.multimodal_mixin",
    "from src.logic.mixins.reasoning_mixin": "from src.core.base.mixins.reasoning_mixin",
    "from src.core.base.entrypoint": "from src.core.base.common.base_utilities",
}

for dirpath, _, filenames in os.walk(ROOT):
    for filename in filenames:
        if not filename.endswith(".py"):
            continue
        path = os.path.join(dirpath, filename)
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
        except OSError:
            continue

        new_content = content
        for old, new in REPLACEMENTS.items():
            new_content = new_content.replace(old, new)

        if new_content != content:
            print(f"Fixed imports in {path}")
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_content)
