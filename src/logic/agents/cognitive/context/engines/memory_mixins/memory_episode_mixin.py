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

"""
Memory episode mixin for recording agent experiences.
"""

import logging
from datetime import datetime
from typing import Any

class MemoryEpisodeMixin:
    """Methods for recording and updating episodes."""

    def record_episode(  # pylint: disable=too-many-positional-arguments
        self,
        agent_name: str,
        task: str,
        outcome: str,
        success: bool,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """Records an agent's experience with semantic indexing and utility scoring."""
        episode = self.core.create_episode(agent_name, task, outcome, success, metadata)
        self.episodes.append(episode)

        # Add to vector db for semantic recall
        collection = self._init_db()
        if collection:
            try:
                doc = self.core.format_for_indexing(episode)
                collection.add(
                    documents=[doc],
                    metadatas=[
                        {
                            "agent": episode["agent"],
                            "success": str(episode["success"]),
                            "timestamp": episode["timestamp"],
                            "utility_score": float(episode["utility_score"]),
                        }
                    ],
                    ids=[f"mem_{len(self.episodes)}_{int(datetime.now().timestamp())}"],
                )
            except (RuntimeError, ValueError, AttributeError) as e:
                logging.error(f"Failed to index memory: {e}")

        self.save()

    def update_utility(self, memory_id: str, increment: float) -> None:
        """Updates the utility score of a specific memory episode."""
        collection = self._init_db()
        if not collection:
            return

        try:
            # Fetch existing metadata
            result = collection.get(ids=[memory_id])
            if result and result["metadatas"]:
                meta = result["metadatas"][0]
                old_score = float(meta.get("utility_score", 0.5))
                new_score = self.core.calculate_new_utility(old_score, increment)
                meta["utility_score"] = new_score

                collection.update(ids=[memory_id], metadatas=[meta])

                # Update local list too
                for _ep in self.episodes:
                    # Note: memory_id format check or matching logic here
                    pass
        except (RuntimeError, ValueError, AttributeError) as e:
            logging.error(f"Failed to update utility for {memory_id}: {e}")