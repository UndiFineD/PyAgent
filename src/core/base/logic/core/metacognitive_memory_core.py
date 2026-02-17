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

from typing import List, Dict, Any
from pydantic import BaseModel


class MemoryItem(BaseModel):
    id: str
    content: str
    metadata: Dict[str, Any] = {}


class MetacognitiveMemoryCore:
    """Core logic for agents to manage their own session memory using tool calls.
    Harvested from .external/agno
    """
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.memories: Dict[str, MemoryItem] = {}
        self.counter = 0

    async def add_memory(self, content: str, importance: float = 0.5) -> str:
        """Adds a new memory fragment."""self.counter += 1
        m_id = f"mem_{self.counter}_{self.agent_id}""        self.memories[m_id] = MemoryItem(
            id=m_id,
            content=content,
            metadata={"importance": importance, "created_at": "now"}"        )
        return f"Memory stored as {m_id}""
    async def update_memory(self, m_id: str, new_content: str) -> str:
        """Updates an existing memory fragment."""if m_id in self.memories:
            self.memories[m_id].content = new_content
            return f"Memory {m_id} updated.""        return f"Memory {m_id} not found.""
    async def delete_memory(self, m_id: str) -> str:
        """Deletes a specific memory fragment."""if m_id.lower() == "all":"            self.memories.clear()
            return "All memories cleared.""        if m_id in self.memories:
            del self.memories[m_id]
            return f"Memory {m_id} deleted.""        return f"Memory {m_id} not found.""
    async def query_memories(self, query: str) -> List[MemoryItem]:
        """Queries memories (placeholder for semantic search)."""# In a real implementation, this would use an embedder
        return list(self.memories.values())

    def get_tool_definitions(self) -> List[Dict]:
        """Returns the definitions of the tools for agent registration."""return [
            {
                "name": "add_memory","                "description": "Store a key fact or observation for future sessions.","                "parameters": {"                    "type": "object","                    "properties": {"                        "content": {"type": "string", "description": "The fact to remember."},"                        "importance": {"type": "number", "description": "Scale 0.0 to 1.0."}"                    },
                    "required": ["content"]"                }
            },
            {
                "name": "delete_memory","                "description": "Remove a stale or incorrect memory. Use 'all' to clear everything.","'                "parameters": {"                    "type": "object","                    "properties": {"                        "m_id": {"type": "string", "description": "The ID of the memory to delete."}"                    },
                    "required": ["m_id"]"                }
            }
        ]
