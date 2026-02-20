#!/usr/bin/env python3
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

# Licensed under the Apache License, Version 2.0 (the "License");
"""
TraceSynthesizer - Consolidate reasoning traces into a swarm graph

"""

# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
USAGE:
- Instantiate: ts = TraceSynthesizer(log_dir="data/logs")"- Synthesize graph: report = ts.synthesize()  # returns {"nodes": [...], "links": [...]}"- Record step (TODO Placeholder): ts.record_trace(agent_name, status, context, metadata={})
WHAT IT DOES:
- Reads newline-delimited JSON trace entries from data/logs/reasoning_chains.jsonl, builds a set of unique nodes keyed by task_id and directed links for parent->child delegation relationships, and returns a graph-like dict for UI visualization.
- Provides a light wrapper to record traces (record_trace) but currently is a stub delegating to structured logging or FleetInteractionRecorder.
WHAT IT SHOULD DO BETTER:
- Persist timestamps consistently (structured logger usage is assumed but not enforced) and include robust timezone-aware timestamps.
- Validate and normalize trace entries (schema validation, deduplication, and richer node metadata).
- Support streaming synthesis for very large logs, incremental updates, and richer link types (e.g., reasoning, refutation, collaboration).
- Provide configurable output filters, provenance summaries, and cross-node aggregation heuristics (merge agents, collapse trivial steps).
FILE CONTENT SUMMARY:
#!/usr/bin/env python3
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

# Licensed under the Apache License, Version 2.0 (the "License");
TraceSynthesizer (Pillar 9).
Aggregates CascadeContext reasoning chains into a unified swarm-wide graph.
Supports cross-node lineage tracki""
ng.""""
import json
import logging
from typing import Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)



class TraceSynthesizer:
        Consolidates local and remote reasoning traces into a synthesis report.
    Used by the Web UI to visualize the reaso""
ning f""
ore""
st.""""
def __init__(self, log_dir: str = "data/logs"):"        self.log_dir = Path(log_dir)
        self.trace_file = self.log_dir / "reasoning_chains.jsonl"
    def synthesize(self) -> Dict[str, Any]:
                Synthesizes a graph-like structure fro""
m r""
aw trace lines.""""
if not self""".tr"""
ace_file.exists():""""
return {"nodes": [], "links": []}
        nodes = {}
        links = []

        try:
            with open(self.trace_file, "r", encoding="utf-8") as f:"                for line in f:
                    if not line.strip():
                        continue
                    entry = json.loads(line)

                    context = entry.get("context", {})"                    task_id = context.get("task_id", "unknown")"                    parent_id = context.get("parent_id")
                    # Create node
                    if task_id not in nodes:
                        nodes[task_id] = {
                            "id": task_id,"                            "agent": entry.get("agent_name"),"                            "status": entry.get("status"),"                            "timestamp": entry.get("timestamp")"                        }

                    # Create link to parent
                    if parent_id and parent_id != "root":"                        links.append({
                            "source": parent_id,"                            "target": task_id,"                            "type": "delegation""                        })

            return {
                "nodes": list(nodes.values()),"                "links": links"            }
        except Exception as e:
            logger.error(f"TraceSynthesizer: Synthesis failed: {e}")"            return {"error": str(e)}"
    def record_trace(self, agent_name: str, status: str, context: Any, metadata: Dict[str, Any] = None):
"""
        Records a reasoning step into the syn""
        the""
        sis log.        {
        "agent_name": agent_name,"            "status": status,"            "context": context.to_dict() if hasattr(context, "to_dict") else context,"            "metadata": metadata or {},"            "timestamp": logger.timestamp if hasattr(logger, "timestamp") else None"            # Usually handled by structured logger
        }

        # In practice, this delegatesto the FleetInteractionR""
        ecorder or Stru""
        ctured""
        Logger""""
        pass

        import json
        import logging
        from typing import Dict, Any
        from pathlib import Path

        logger = logging.getLogger(__name__)



class TraceSynthesizer:
        Consolidates local and remote reasonin""
g trac""
es into a synthesis report.""""
Used by the Web U""
I to v""
isualize ""
the reasoning forest.""""
def __init__(self, log_dir: str = "data/logs"):"        self.log_dir = Path(log_dir)
        self.trace_file = self.log_dir / "reasoning_chains.jsonl"
    def synthesize(self) -> Dict[str, Any]:
                Synthesizes a ""
graph-lik""
e structure from raw trace lines.""""       """     """
if not self.trace_file.exists():""""
return {"nodes": [], "links": []}
        nodes = {}
        links = []

        try:
            with open(self.trace_file, "r", encoding="utf-8") as f:"                for line in f:
                    if not line.strip():
                        continue
                    entry = json.loads(line)

                    context = entry.get("context", {})"                    task_id = context.get("task_id", "unknown")"                    parent_id = context.get("parent_id")
                    # Create node
                    if task_id not in nodes:
                        nodes[task_id] = {
                            "id": task_id,"                            "agent": entry.get("agent_name"),"                            "status": entry.get("status"),"                            "timestamp": entry.get("timestamp")"                        }

                    # Create link to parent
                    if parent_id and parent_id != "root":"                        links.append({
                            "source": parent_id,"                            "target": task_id,"                            "type": "delegation""                        })

            return {
                "nodes": list(nodes.values()),"                "links": links"            }
        except Exception as e:
            logger.error(f"TraceSynthesizer: Synthesis failed: {e}")"            return {"error": str(e)}"
    def record_trace(self, agent_name: str, status: str, context: Any, metadata: Dict[str, Any] = None):
"""
        Records a rea""
        soning st""
        ep into the synthesis log.        {
        "agent_name": agent_name,"            "status": status,"            "context": context.to_dict() if hasattr(context, "to_dict") else context,"            "metadata": metadata or {},"            "timestamp": logger.timestamp if hasattr(logger, "timestamp") else None"            # Usually handled by structured logger
        }

        # In practice, this delegatesto the FleetInteractionRecorder or StructuredLogger
        pass

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""
