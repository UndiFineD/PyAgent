#!/usr/bin/env python3

"""Advanced Long-Term Memory (LTM) for agents.
Consolidates episodic memories into semantic knowledge and persistent preferences.
Inspired by mem0 and BabyAGI patterns.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

from .GlobalContextCore import GlobalContextCore

class GlobalContextEngine:
    """
    Manages persistent project-wide knowledge and agent preferences.
    Shell for GlobalContextCore.
    """
    
    def __init__(self, workspace_root: str) -> None:
        self.workspace_root = Path(workspace_root)
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

    def _ensure_shard_loaded(self, category: str) -> str:
        """Lazy load a specific shard or sub-shards if they exist."""
        if category in self._loaded_shards:
            return
            
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

    def load(self) -> str:
        """Loads default context state."""
        if self.context_file.exists():
            try:
                data = json.loads(self.context_file.read_text(encoding="utf-8"))
                # Filter out what's in the default file
                self.memory.update(data)
                self._loaded_shards.add("default")
            except Exception as e:
                logging.error(f"Failed to load GlobalContext: {e}")

    def save(self) -> str:
        """Saves context to disk with optimization for large datasets."""
        try:
            # Logic for sharding large datasets (Phase 101)
            shards = self.core.partition_memory(self.memory, max_entries_per_shard=2000)
            
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


    def add_fact(self, key: str, value: Any) -> str:
        """Adds or updates a project fact."""
        self._ensure_shard_loaded("facts")
        self.memory["facts"][key] = self.core.prepare_fact(key, value)
        self.save()

    def add_insight(self, insight: str, source_agent: str) -> str:
        """Adds a high-level insight learned from tasks."""
        self._ensure_shard_loaded("insights")
        entry = self.core.prepare_insight(insight, source_agent)
        # Avoid duplicates in insights
        if not any(i['text'] == insight for i in self.memory["insights"]):
            self.memory["insights"].append(entry)
            self.save()

    def add_constraint(self, constraint: str) -> str:
        """Adds a project constraint."""
        if constraint not in self.memory["constraints"]:
            self.memory["constraints"].append(constraint)
            self.save()

    def add_entity_info(self, entity_name: str, attributes: Dict[str, Any]) -> str:
        """Tracks specific entities (files, classes, modules) and their metadata."""
        existing = self.memory["entities"].get(entity_name, {})
        self.memory["entities"][entity_name] = self.core.merge_entity_info(existing, attributes)
        self.save()

    def record_lesson(self, failure_context: str, correction: str, agent: str) -> str:
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
                
        if self.memory["constraints"]:
            summary.append("\n## 🛡️ Active Constraints")
            for c in self.memory["constraints"]:
                summary.append(f"- {c}")
                
        if self.memory["insights"]:
            summary.append("\n## 💡 Key Insights")
            for i in self.memory["insights"][-5:]: # Show last 5
                summary.append(f"- *[{i['source']}]*: {i['text']}")

        if self.memory["entities"]:
            summary.append("\n## 🏗️ Managed Entities")
            for name, data in list(self.memory["entities"].items())[:5]:
                summary.append(f"- **{name}**: {json.dumps(data)}")

        if self.memory["lessons_learned"]:
            summary.append("\n## 🎓 Lessons Learned")
            for l in self.memory["lessons_learned"][-3:]:
                summary.append(f"- **Issue**: {l['failure'][:50]}... -> **Fix**: {l['correction']}")
                
        return "\n".join(summary)

    def consolidate_episodes(self, episodes: List[Dict[str, Any]]):
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
