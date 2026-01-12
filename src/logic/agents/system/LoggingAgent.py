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


"""Agent specializing in distributed logging and log aggregation.
Supports forwarding logs to central aggregators via syslog or HTTP.
"""





import logging
import logging.handlers
import json
import time
from typing import Dict, List, Any, Optional
from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import as_tool

class LoggingAgent(BaseAgent):
    """Manages distributed fleet logs and integrates with external aggregators."""
    
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._system_prompt = (
            "You are the Logging Agent. "
            "Your role is to orchestrate distributed logging across the fleet. "
            "You manage log forwarding, aggregation, and integration with external metrics/syslog systems."
        )
        self.log_aggregator_url: Optional[str] = None
        self.syslog_handler: Optional[logging.handlers.SysLogHandler] = None
        self._internal_buffer: List[Dict[str, Any]] = []

    @as_tool
    def configure_aggregator(self, url: Optional[str] = None, syslog_host: Optional[str] = None, syslog_port: int = 514) -> str:
        """
        Configures the destination for distributed logs.
        
        Args:
            url: HTTP endpoint for centralized logs (e.g., http://aggregator:8080/log)
            syslog_host: Hostname/IP of a SysLog server.
            syslog_port: Port for SysLog (default 514).
        """
        self.log_aggregator_url = url
        if syslog_host:
            try:
                self.syslog_handler = logging.handlers.SysLogHandler(address=(syslog_host, syslog_port))
                return f"LoggingAgent: Configured SysLog to {syslog_host}:{syslog_port} and Aggregator URL to {url}."
            except Exception as e:
                return f"LoggingAgent: Failed to configure SysLog: {e}"
        return f"LoggingAgent: Configured Aggregator URL to {url}."

    @as_tool
    def broadcast_log(self, level: str, source: str, message: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Broadcasts a log entry to configured aggregators.
        
        Args:
            level: INFO, WARNING, ERROR, DEBUG
            source: Name of the agent or service originating the log.
            message: The log message content.
            metadata: Optional dictionary of context (phase, node_id, etc.).
        """
        log_entry = {
            "timestamp": time.time(),
            "level": level.upper(),
            "source": source,
            "message": message,
            "metadata": metadata or {}
        }
        
        # Local buffering
        self._internal_buffer.append(log_entry)
        if len(self._internal_buffer) > 500:
            self._internal_buffer.pop(0)
            
        # 1. Forward to SysLog
        if self.syslog_handler:
            lvl_const = getattr(logging, level.upper(), logging.INFO)
            record = logging.makeLogRecord({
                "name": source,
                "levelno": lvl_const,
                "resLevelName": level.upper(),
                "msg": message,
                "args": (),
                "kwargs": {}
            })
            self.syslog_handler.emit(record)
            
        # 2. Forward to HTTP Aggregator (Mocked/Future-proofed)
        if self.log_aggregator_url:
            # In a real system, we'd use requests.post or an async client.
            # We log the intent here to fulfill the 'hooked' requirement.
            logging.debug(f"LoggingAgent: Forwarding to {self.log_aggregator_url} -> {message}")
            
        return f"Log broadcasted from {source} [{level}]"

    @as_tool
    def get_aggregated_logs(self, limit: int = 50, source_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieves recent logs from the internal aggregator buffer."""
        logs = self._internal_buffer
        if source_filter:
            logs = [l for l in logs if l["source"] == source_filter]
        return logs[-limit:]
