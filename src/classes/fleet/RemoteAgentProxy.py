#!/usr/bin/env python3

"""Proxy for agents running on remote nodes.
Allows FleetManager to transparently call tools on other machines.
"""

import requests
import json
import logging
import os
import time
from typing import Dict, List, Any, Optional
from src.classes.base_agent import BaseAgent

class RemoteAgentProxy(BaseAgent):
    """Encapsulates a remote agent accessible via HTTP/JSON-RPC.
    
    Resilience (Phase 108): Implements a 15-minute TTL status cache for remote nodes.
    Intelligence (Phase 108): Records remote interactions to local shards.
    """
    
    STATUS_CACHE_FILE = "remote_node_status.json"
    CACHE_TTL_SECONDS = 900  # 15 minutes

    def __init__(self, file_path: str, node_url: str, agent_name: str) -> None:
        super().__init__(file_path)
        self.node_url = node_url.rstrip("/")
        self.agent_name = agent_name
        self._system_prompt = f"Proxy for remote agent '{agent_name}' at {node_url}"
        
        # Determine paths for caching (Phase 108)
        self.workspace_root = os.getcwd()
        self.cache_path = os.path.join(self.workspace_root, "agent_store", self.STATUS_CACHE_FILE)
        os.makedirs(os.path.dirname(self.cache_path), exist_ok=True)

    def _is_node_working(self) -> bool:
        """Checks if the remote node is known to be working via cache (Phase 108)."""
        if not os.path.exists(self.cache_path):
            return True
            
        try:
            with open(self.cache_path, "r") as f:
                cache = json.load(f)
                
            status = cache.get(self.node_url)
            if status and status["state"] == "down":
                if time.time() - status["timestamp"] < self.CACHE_TTL_SECONDS:
                    logging.warning(f"Remote node {self.node_url} is marked DOWN in cache. Skipping call.")
                    return False
        except Exception as e:
            logging.debug(f"Error reading node status cache: {e}")
            
        return True

    def _update_node_status(self, is_up: bool) -> None:
        """Updates the node status in the persistent cache (Phase 108)."""
        try:
            cache = {}
            if os.path.exists(self.cache_path):
                with open(self.cache_path, "r") as f:
                    cache = json.load(f)
            
            cache[self.node_url] = {
                "state": "up" if is_up else "down",
                "timestamp": time.time()
            }
            
            with open(self.cache_path, "w") as f:
                json.dump(cache, f, indent=2)
        except Exception as e:
            logging.error(f"Error updating node status cache: {e}")

    def call_remote_tool(self, tool_name: str, **kwargs) -> str:
        """Calls a tool on the remote node with resilience and intelligence (Phase 108)."""
        if not self._is_node_working():
            return f"Skipping call: Remote node {self.node_url} is currently unreachable (cached)."

        endpoint = f"{self.node_url}/call"
        payload = {
            "agent": self.agent_name,
            "tool": tool_name,
            "args": kwargs
        }
        
        try:
            logging.info(f"Calling remote tool {tool_name} on {self.node_url}")
            response = requests.post(endpoint, json=payload, timeout=60)
            response.raise_for_status()
            
            result = response.json().get("result", "No result returned.")
            self._update_node_status(True)
            self._record_interaction(tool_name, payload, result)
            return result
        except Exception as e:
            logging.error(f"Error calling remote agent: {e}")
            self._update_node_status(False)
            return f"Error calling remote agent: {e}"

    def _record_interaction(self, tool_name: str, payload: Dict[str, Any], response: str) -> None:
        """Records the interaction to a local shard for later intelligence harvesting (Phase 108)."""
        try:
            from src.classes.backend.LocalContextRecorder import LocalContextRecorder
            recorder = LocalContextRecorder()
            recorder.record_interaction(
                agent_name=f"remote_{self.agent_name}",
                tool_name=tool_name,
                payload=payload,
                response=response
            )
        except Exception as e:
            logging.debug(f"Failed to record remote interaction: {e}")

    def improve_content(self, prompt: str) -> str:
        """Proxies the improvement request to the remote agent."""
        return self.call_remote_tool("improve_content", prompt=prompt)
