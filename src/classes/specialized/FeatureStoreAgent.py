#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""FeatureStoreAgent for PyAgent.
Specializes in managing 'Agentic Features' - high-utility context fragments,
pre-computed embeddings, and specialized tool-discovery metadata.
Inspired by MLOps best practices.
"""

from __future__ import annotations
from src.core.base.version import VERSION
import logging
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import as_tool
from src.logic.agents.intelligence.core.SynthesisCore import SynthesisCore

__version__ = VERSION

class FeatureStoreAgent(BaseAgent):
    """Manages the lifecycle of high-utility context features for the fleet.
    Integrated with SynthesisCore for feature vectorization and insight merging.
    """

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.feature_dir = Path("data/memory/agent_store/features")
        self.feature_dir.mkdir(parents=True, exist_ok=True)
        self.core = SynthesisCore()

    @as_tool
    def store_vectorized_insight(self, insight_text: str, tags: list[str]) -> str:
        """
        Vectorizes a text insight and stores it for swarm-wide retrieval.
        """
        vector = self.core.vectorize_insight(insight_text)
        feature_name = f"insight_{hash(insight_text)}"
        return self.register_feature(feature_name, vector, {"original_text": insight_text, "tags": tags})

    @as_tool
    def merge_swarm_insights(self, feature_names: list[str]) -> list[float]:
        """
        Merges multiple vectorized insights into a single 'Global Fleet Vector'.
        """
        vectors = []
        for name in feature_names:
            v = self.get_feature(name)
            if v:
                vectors.append(v)
        
        return self.core.merge_feature_vectors(vectors)

    @as_tool
    def register_feature(self, feature_name: str, value: Any, metadata: dict[str, Any] | None = None) -> str:
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
    def get_feature(self, feature_name: str) -> Any | None:
        """Retrieves a feature from the store."""
        path = self.feature_dir / f"{feature_name}.json"
        if not path.exists():
            return None
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
                return data.get("value")
        except Exception as e:
            logging.error(f"Error reading feature {feature_name}: {e}")
            return None

    @as_tool
    def list_features(self) -> list[str]:
        """Lists all available features in the store."""
        return [f.stem for f in self.feature_dir.glob("*.json")]

    def improve_content(self, input_text: str) -> str:
        """Advisory on feature engineering for agents."""
        return "I am serving current agentic features. Recommend a feature for extraction?"

if __name__ == "__main__":
    from src.core.base.utilities import create_main_function
    main = create_main_function(FeatureStoreAgent, "Feature Store Agent", "Feature life-cycle management")
    main()