#!/usr/bin/env python3

import logging
import json
import time
from typing import Dict, List, Any, Optional
from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import as_tool

class AttentionBufferAgent(BaseAgent):
    """
    Agent that maintains a shared attention buffer between humans and agents.
Maintain a high-resolution stream of state changes, user interactions, and agent thoughts.
    """
    
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.buffer: List[Dict[str, Any]] = []
        self.max_buffer_size = 100
        self._system_prompt = (
            "You are the Attention Buffer Agent. "
            "Your role is to maintain a 'shared consciousness' between the user and the agent swarm. "
            "You track the current locus of attention, recent important events, and pending human questions."
        )

    @as_tool
    def push_attention_point(self, source: str, content: str, priority: int = 5) -> str:
        """
        Adds a new point of interest to the shared attention buffer.
        Source can be 'Human' or any Agent name.
        """
        point = {
            "timestamp": time.time(),
            "source": source,
            "content": content,
            "priority": priority
        }
        self.buffer.append(point)
        
        # Maintain size limit
        if len(self.buffer) > self.max_buffer_size:
            self.buffer.pop(0)
            
        logging.info(f"Attention point added from {source}: {content[:50]}...")
        return f"Attention point registered. Buffer size: {len(self.buffer)}"

    @as_tool
    def get_attention_summary(self) -> Dict[str, Any]:
        """
        Returns the current state of the attention buffer, sorted by priority and recency.
        """
        sorted_buffer = sorted(self.buffer, key=lambda x: (x['priority'], x['timestamp']), reverse=True)
        return {
            "current_focus": sorted_buffer[0] if sorted_buffer else None,
            "recent_context": sorted_buffer[:10],
            "total_points": len(self.buffer)
        }

    @as_tool
    def clear_stale_attention(self, age_seconds: int = 3600) -> str:
        """
        Removes attention points older than a certain duration.
        """
        now = time.time()
        initial_count = len(self.buffer)
        self.buffer = [p for p in self.buffer if now - p['timestamp'] < age_seconds]
        removed = initial_count - len(self.buffer)
        return f"Cleared {removed} stale attention points."
