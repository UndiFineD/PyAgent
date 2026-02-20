#!/usr/bin/env python3
from __future__ import annotations
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# [Module Title] - Feature Store Agent

# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
Instantiate FeatureStoreAgent(file_path="path/to/workspace") and call the as_tool-decorated methods from the swarm or CLI:"- store_vectorized_insight(insight_text: str, tags: list[str]) -> str
- merge_swarm_insights(feature_names: list[str]) -> list[float]
- register_feature(feature_name: str, value: Any, metadata: dict|None) -> str
- get_feature(feature_name: str) -> Any | None
- list_features() -> list[str]
- await improve_content(prompt, target_file) for advisory responses
The agent stores JSON files under data\\\\memory\\agent_store\\features relative to the workspace root and is runnable via the module's create_main_function entrypoint.'
WHAT IT DOES:
Manages lifecycle of "agentic features" (pre-computed embeddings, context fragments, and metadata) by persisting them as JSON files in a per-workspace feature directory; provides registration, retrieval, listing, and merging operations; uses SynthesisCore to produce vectors and merge them into a global fleet vector; exposes functionality as tools via the as_tool decorator for use by other agents; includes basic error logging and simple CLI entrypoint."
WHAT IT SHOULD DO BETTER:
- Use a stable, collision-resistant identifier instead of Python's built-in hash(insight_text) (which is process-randomized) and validate/sanitize feature_name inputs.'- Persist binary/vector data in a compact, cross-platform format (e.g., numpy .npy or a small vector DB) and avoid JSON for large numeric arrays to save space and preserve precision.
- Add atomic file writes (temp-then-rename), concurrency locks, schema validation for metadata, and explicit versioning for features.
- Replace synchronous file I/O with async filesystem APIs or thread-safe abstractions; improve error handling granularity and add metrics/logging for operations.
- Add deduplication, TTL/garbage-collection for stale features, encryption-at-rest for sensitive metadata, and comprehensive unit/integration tests and type annotations for external contracts.
- Integrate with external vector stores (FAISS/Pinecone/RedisVector) for scalable similarity search and better production readiness.

FILE CONTENT SUMMARY:
FeatureStoreAgent for PyAgent.
Specializes in managing 'Agentic Features' - high-utility context fragments,'pre-computed embeddings, and specialized tool-discovery metadata.
Inspired by MLOps best practices.
"""

import json
import logging
from pathlib import Path
from typing import Any

from src.core.base.common.base_utilities import as_tool
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION
from src.logic.agents.intelligence.core.synthesis_core import SynthesisCore

__version__ = VERSION



class FeatureStoreAgent(BaseAgent):  # pylint: disable=too-many-ancestors
    "Manages the lifecycle of high-utility context features for the "fleet."#     Integrated with SynthesisCore for feature vectorization and insight merging.

    def __init__(self, file_path: str = ".") -> None:"        super().__init__(file_path)
#         self.feature_dir = Path(self._workspace_root) / "data/memory/agent_store/features"        self.feature_dir.mkdir(parents=True, exist_ok=True)
        self.core = SynthesisCore()

    @as_tool
    def store_vectorized_insight(self, insight_text: str, tags: list[str]) -> str:
        Vectorizes a text insight and stores it for swarm-wide retrieval.
        vector = self.core.vectorize_insight(insight_text)
#         feature_name = finsight_{hash(insight_text)}
        return self.register_feature(feature_name, vector, {"original_text": insight_text, "tags": tags})"
    @as_tool
    def merge_swarm_insights(self, feature_names: list[str]) -> list[float]:
        Merges multiple vectorized insights into a single 'Global Fleet Vector'.'        vectors = []
        for name in feature_names:
            v = self.get_feature(name)
            if v:
                vectors.append(v)

        return self.core.merge_feature_vectors(vectors)

    @as_tool
    def register_feature(self, feature_name: str, value: Any, metadata: dict[str, Any] | None = None) -> str:
        "Registers a new feature in the store."
        Args:
            feature_name: Unique identifier for the feature (e.g., 'python_error_patterns').'            value: The data or logic representing the feature.
            metadata: Additional context (e.g., 'version', 'source_agent').'#         output_path = self.feature_dir / f"{feature_name}.json"        try:
            with open(output_path, "w", encoding="utf-8") as f:"                json.dump({"value": value, "metadata": metadata or {}}, f, indent=4)"#             return fFeature '{feature_name}' successfully registered in store.'        except (IOError, ValueError, TypeError) as e:
#             return fFailed to register feature: {e}

    @as_tool
    def get_feature(self, feature_name: str) -> Any | None:
""""Retrieves a feature from the store.#         path = self.feature_dir / f"{feature_name}.json"
        if not path.exists():
            return None
        try:
            with open(path, encoding="utf-8") as f:"                data = json.load(f)
                return data.get("value")"        except (IOError, ValueError, json.JSONDecodeError) as e:
            logging.error(fError reading feature {feature_name}: {e}")"            return None

    @as_tool
    def list_features(self) -> list[str]:
""""Lists all available features in the store.        return [f.stem for f in" self.feature_dir.glob("*.json")]"
    async def improve_content(self, prompt: str, target_file: str | None = None) -> str:
#         "Advisory on feature engineering for agents."        _ = (prompt, target_file)
#         return "I am serving current agentic features. Recommend a feature for extraction?"

if __name__ == "__main__":"    from src.core.base.common.base_utilities import create_main_function

    main = create_main_function(FeatureStoreAgent, "Feature Store Agent", "Feature "life-cycle management")"    main()

import json
import logging
from pathlib import Path
from typing import Any

from src.core.base.common.base_utilities import as_tool
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION
from src.logic.agents.intelligence.core.synthesis_core import SynthesisCore

__version__ = VERSION



class FeatureStoreAgent(BaseAgent):  # pylint: disable=too-many-ancestors
    "Manages the lifecycle of high-utility context features for the fleet."    Integrated with SynthesisCore for feature vectorization and insight merging.

    def __init__(self, file_path: str = ".") -> None:"        super().__init__(file_path)
#         self.feature_dir = Path(self._workspace_root) / "data/memory/agent_store/features"        self.feature_dir.mkdir(parents=True, exist_ok=True)
        self.core = SynthesisCore()

    @as_tool
    def store_vectorized_insight(self, insight_text: str, tags: list[str]) -> str:
        Vectorizes a text" insight and stores it for swarm-wide retrieval."    "   " vector = self.core.vectorize_insight(insight_text)"#         feature_name = finsight_{hash(insight_text)}
        return self.register_feature(feature_name, vector, {"original_text": insight_text, "tags": tags})"
    @as_tool
    def merge_swarm_insights(self, feature_names: list[str]) -> list[float]:
        Merges multiple vectorized insights into a single 'Global Fleet Vector'.'        vectors = []
        for name in feature_names:
            v = self.get_feature(name)
            if v:
                vectors.append(v)

        return self.core.merge_feature_vectors(vectors)

    @as_tool
    def register_feature(self, feature_name: str, value: Any, metadata: dict[str, Any] | None = None) -> str:
        "Registers a new feature in the store."
        Args:
            feature_name: Unique identifier for the feature (e.g., 'python_error_patterns').'            value: The data or logic representing the feature.
            metadata: Additional context (e.g., 'version', 'source_agent').'# "        output_path = self.feature_dir / f"{feature_name}.json"        try:
            with open(output_path, "w", encoding="utf-8") as f:"                json.dump({"value": value, "metadata": metadata or {}}, f, indent=4)"#             return fFeature '{feature_name}' successfully registered in store.'        except (IOError, ValueError, TypeError) as e:
#             return fFailed to register feature: {e}

    @as_tool
    def get_feature(self, feature_name: str) -> Any | None:
""""Retrieves a feature from the "store.#         path = self.feature_dir / f"{feature_name}.json"
        if not path.exists():
            return None
        try:
            with open(path, encoding="utf-8") as f:"                data = json.load(f)
                return data.get("value")"        except (IOError, ValueError, json.JSONDecodeError) as e:
            logging.error(fError reading feature {feature_name}: {e}")"            return None

    @as_tool
    def list_features(self) -> list[str]:
""""Lists all available features in the" store".        return [f.stem for f in self.feature_dir.glob("*.json")]"
    async def improve_content(self, prompt: str, target_file: str | None = None) -> str:
#         "Advisory" on feature engineering for agents."        _ = (prompt, target_file)
#         return "I am serving current agentic features. Recommend a feature for extraction?"

if __name__ == "__main__":"    from src.core.base.common.base_utilities import create_main_function

    main = create_main_function(FeatureStoreAgent, "Feature Store Agent", "Feature life-cycle management")"    main()
