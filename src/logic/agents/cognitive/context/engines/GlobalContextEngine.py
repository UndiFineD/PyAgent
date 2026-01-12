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

from __future__ import annotations

from src.core.base.version import VERSION
__version__ = VERSION

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.


"""Advanced Long-Term Memory (LTM) for agents.
Consolidates episodic memories into semantic knowledge and persistent preferences.
Inspired by mem0 and BabyAGI patterns.
"""




import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

from src.logic.agents.cognitive.context.engines.GlobalContextCore import GlobalContextCore

class GlobalContextEngine:
    """
    Manages persistent project-wide knowledge and agent preferences.
    Shell for GlobalContextCore.
    """
    
    def __init__(self, workspace_root: str = None, fleet: Any = None) -> None:
        if fleet and hasattr(fleet, "workspace_root"):
            self.workspace_root = Path(fleet.workspace_root)
        elif workspace_root:
            self.workspace_root = Path(workspace_root)
        else:
            self.workspace_root = Path(".")
            
        self.context_file = self.workspace_root / ".agent_global_context.json"
        self.shard_dir = self.workspace_root / ".agent_shards"
        self.core = GlobalContextCore()
        self.memory: Dict[str, Any] = {
            "facts": {},
            "preferences": {},
            "constraints": [],
            "insights": [],
            "entities": {},
            "lessons_learned": []
        }
        self._loaded_shards = set()
        self.load()

    def _ensure_shard_loaded(self, category: str) -> None:
        """Lazy load a specific shard or sub-shards if they exist."""
        if category in self._loaded_shards:
            return None
            
        # Check for sub-shards (Phase 104)
        shard_files = list(self.shard_dir.glob(f"{category}_*.json"))
        if shard_files:
            if category not in self.memory: self.memory[category] = {}
            for s_file in shard_files:
                try:
                    shard_data = json.loads(s_file.read_text(encoding="utf-8"))
                    self.memory[category].update(shard_data)
                except Exception as e:
                    logging.warning(f"Failed to load sub-shard {s_file.name}: {e}")
            logging.info(f"Context: Loaded {len(shard_files)} sub-shards for '{category}'.")
        else:
            shard_file = self.shard_dir / f"{category}.json"
            if shard_file.exists():
                try:
                    shard_data = json.loads(shard_file.read_text(encoding="utf-8"))
                    self.memory[category] = shard_data
                    logging.info(f"Context: Lazy-loaded shard '{category}' from disk.")
                except Exception as e:
                    logging.warning(f"Failed to load shard {category}: {e}")
        
        self._loaded_shards.add(category)

    def get(self, category: str, key: Optional[str] = None) -> Any:
        """Retrieves data with lazy shard loading."""
        self._ensure_shard_loaded(category)
        data = self.memory.get(category)
        if key and isinstance(data, dict):
            return data.get(key)
        return data

    def set_with_conflict_resolution(self, category: str, key: str, value: Any, strategy: str = "latest") -> None:
        """Sets a value in memory, resolving conflicts if the key already exists."""
        self._ensure_shard_loaded(category)
        if category not in self.memory:
            self.memory[category] = {}
        
        if not isinstance(self.memory[category], dict):
            # If it's not a dict, we can't key it, so we just overwrite it if possible or skip
            self.memory[category] = {key: value}
        else:
            existing = self.memory[category].get(key)
            if existing is not None:
                resolved = self.core.resolve_conflict(existing, value, strategy)
                self.memory[category][key] = resolved
            else:
                self.memory[category][key] = value
        
        self.save()

    def load(self) -> None:
        """Loads default context state."""
        if self.context_file.exists():
            try:
                data = json.loads(self.context_file.read_text(encoding="utf-8"))
                # Filter out what's in the default file
                self.memory.update(data)
                self._loaded_shards.add("default")
            except Exception as e:
                logging.error(f"Failed to load GlobalContext: {e}")

    def save(self) -> None:
        """Saves context to disk with optimization for large datasets."""
        try:
            # Logic for sharding large datasets (Phase 101)
            # Phase 119: Adaptive rebalancing automatically scales shard count
            shards = self.core.partition_memory(self.memory, max_entries_per_shard=2000)
            
            # Phase 119: Check for shard bloat to notify system for potential migration
            bloated = self.core.detect_shard_bloat(shards)
            if bloated:
                logging.warning(f"CONTEXT: Detected bloat in shards {bloated}. Adaptive rebalancing triggered.")

            # Save default state
            self.context_file.write_text(json.dumps(shards["default"], indent=2), encoding="utf-8")
            
            # Save extra shards
            if len(shards) > 1:
                self.shard_dir.mkdir(exist_ok=True)
                for shard_name, shard_data in shards.items():
                    if shard_name == "default": continue
                    shard_file = self.shard_dir / f"{shard_name}.json"
                    shard_file.write_text(json.dumps(shard_data, indent=2), encoding="utf-8")
                    
        except Exception as e:
            logging.error(f"Failed to save GlobalContext: {e}")

    def trigger_rebalance(self) -> None:
        """Manually force a rebalancing of the context shards."""
        logging.info("CONTEXT: Triggering manual shard rebalancing...")
        self.save()


    def add_fact(self, key: str, value: Any) -> None:
        """Adds or updates a project fact."""
        self._ensure_shard_loaded("facts")
        self.memory["facts"][key] = self.core.prepare_fact(key, value)
        self.save()

    def add_insight(self, insight: str, source_agent: str) -> None:
        """Adds a high-level insight learned from tasks."""
        self._ensure_shard_loaded("insights")
        entry = self.core.prepare_insight(insight, source_agent)
        # Avoid duplicates in insights
        if not any(i['text'] == insight for i in self.memory["insights"]):
            self.memory["insights"].append(entry)
            self.save()

    def add_constraint(self, constraint: str) -> None:
        """Adds a project constraint."""
        if constraint not in self.memory["constraints"]:
            self.memory["constraints"].append(constraint)
            self.save()

    def add_entity_info(self, entity_name: str, attributes: Dict[str, Any]) -> None:
        """Tracks specific entities (files, classes, modules) and their metadata."""
        existing = self.memory["entities"].get(entity_name, {})
        self.memory["entities"][entity_name] = self.core.merge_entity_info(existing, attributes)
        self.save()

    def record_lesson(self, failure_context: str, correction: str, agent: str) -> None:
        """Records a learned lesson to prevent future errors."""
        lesson = {
            "failure": failure_context,
            "correction": correction,
            "agent": agent,
            "timestamp": datetime.now().isoformat()
        }
        self.memory["lessons_learned"].append(lesson)
        self.memory["lessons_learned"] = self.core.prune_lessons(self.memory["lessons_learned"])
        self.save()

    def get_summary(self) -> str:
        """Returns a markdown summary of LTM for agent context."""
        return self.core.generate_markdown_summary(self.memory)

    def consolidate_episodes(self, episodes: List[Dict[str, Any]]) -> None:
        """Analyzes episodic memories to extract long-term insights."""
        # This would typically use an LLM to find patterns.
        # For now, we look for repeated failures or success patterns.
        agent_stats: Dict[str, Dict[str, int]] = {}
        for ep in episodes:
            agent = ep["agent"]
            if agent not in agent_stats:
                agent_stats[agent] = {"success": 0, "fail": 0}
            if ep["success"]:
                agent_stats[agent]["success"] += 1
            else:
                agent_stats[agent]["fail"] += 1
                
        for agent, stats in agent_stats.items():
            if stats["fail"] > 3:
                self.add_insight(f"{agent} is struggling with current tasks. Context injection might be insufficient.", "LTM_System")
            elif stats["success"] > 10:
                self.add_insight(f"{agent} is highly reliable for current task types.", "LTM_System")
