from __future__ import annotations
from typing import Dict, List, Any, Optional

class ModelRegistryCore:
    """
    ModelRegistryCore manages the PEFT (LoRA/QLoRA) adapter registry.
    It maps request types to specific expert adapters.
    """

    def __init__(self) -> None:
        # Registry mapping intent/type to adapter path
        self.adapter_registry: Dict[str, str] = {
            "python_expert": "models/forge/adapters/python_312_lora",
            "security_audit": "models/forge/adapters/security_specialist_lora",
            "documentation": "models/forge/adapters/docgen_lora",
            "rust_developer": "models/forge/adapters/rust_migration_expert"
        }

    def get_adapter_for_task(self, task_type: str) -> Optional[str]:
        """Returns the adapter path for a given task type."""
        return self.adapter_registry.get(task_type.lower())

    def should_trigger_finetuning(self, quality_history: List[float], threshold: float = 0.6) -> bool:
        """
        Determines if fine-tuning is needed (e.g., last 5 scores below threshold).
        """
        if len(quality_history) < 5:
            return False
        
        last_5 = quality_history[-5:]
        return all(q < threshold for q in last_5)

    def register_new_adapter(self, name: str, path: str):
        """Adds a new adapter to the registry."""
        self.adapter_registry[name.lower()] = path

    def list_adapters(self) -> List[str]:
        """Lists all registered expert adapters."""
        return list(self.adapter_registry.keys())
