#!/usr/bin/env python3

"""FeatureStoreAgent for PyAgent.
Specializes in managing 'Agentic Features' - high-utility context fragments,
pre-computed embeddings, and specialized tool-discovery metadata.
Inspired by MLOps best practices.
"""

import logging
import json
from src.core.base.version import VERSION
from pathlib import Path
from typing import Dict, List, Any, Optional
from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import as_tool

__version__ = VERSION

class FeatureStoreAgent(BaseAgent):
    """Manages the lifecycle of high-utility context features for the fleet."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.feature_dir = Path("data/memory/agent_store/features")
        self.feature_dir.mkdir(parents=True, exist_ok=True)
        self._system_prompt = (
            "You are the Feature Store Agent. Your role is to serve high-utility 'Agentic Features' "
            "to the rest of the fleet. You ensure that common code patterns, pre-validated logic blocks, "
            "and performance characteristics are indexed and retrieved efficiently."
        )

    @as_tool
    def register_feature(self, feature_name: str, value: Any, metadata: Optional[Dict[str, Any]] = None) -> str:
        """Registers a new feature in the store.
        
        Args:
            feature_name: Unique identifier for the feature (e.g., 'python_error_patterns').
            value: The data or logic representing the feature.
            metadata: Additional context (e.g., 'version', 'source_agent').
        """
        output_path = self.feature_dir / f"{feature_name}.json"
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump({"value": value, "metadata": metadata or {}}, f, indent=4)
            return f"Feature '{feature_name}' successfully registered in store."
        except Exception as e:
            return f"Failed to register feature: {e}"

    @as_tool
    def get_feature(self, feature_name: str) -> Optional[Any]:
        """Retrieves a feature from the store."""
        path = self.feature_dir / f"{feature_name}.json"
        if not path.exists():
            return None
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("value")
        except Exception as e:
            logging.error(f"Error reading feature {feature_name}: {e}")
            return None

    @as_tool
    def list_features(self) -> List[str]:
        """Lists all available features in the store."""
        return [f.stem for f in self.feature_dir.glob("*.json")]

    def improve_content(self, input_text: str) -> str:
        """Advisory on feature engineering for agents."""
        return "I am serving current agentic features. Recommend a feature for extraction?"

if __name__ == "__main__":
    from src.core.base.utilities import create_main_function
    main = create_main_function(FeatureStoreAgent, "Feature Store Agent", "Feature life-cycle management")
    main()
