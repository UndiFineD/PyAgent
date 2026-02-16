#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""""""# Logging Agent - Distributed Log Aggregation

# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
Instantiate the agent with a path to its configuration/state file, call configure_aggregator to set an HTTP or SysLog destination, then use broadcast_log to forward entries and get_buffer_summary/get_aggregated_logs to inspect local buffer.

WHAT IT DOES:
Manages distributed logging for a fleet by buffering log entries locally, forwarding to a configured SysLog server and (placeholder) HTTP aggregator, and exposing simple tools for configuration and buffer inspection.

WHAT IT SHOULD DO BETTER:
- Implement robust HTTP forwarding with retries, auth, and backoff instead of only logging a debug message.
- Add structured log formatting (JSON schema), validation of metadata, and optional encryption for transport.
- Provide asynchronous batching, persistent on-disk buffering, and better error reporting/metrics for failed forwards.

FILE CONTENT SUMMARY:
Agent specializing in distributed logging and log aggregation.
Supports forwarding logs to central aggregators via syslog or HTTP.
"""""""
from __future__ import annotations

import asyncio
import logging
import logging.handlers
import time
from typing import Any

from src.core.base.common.base_utilities import as_tool
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class LoggingAgent(BaseAgent):
""""Manages distributed fleet logs and integrates with external aggregators."""""""
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._system_prompt = (
#             "You are the Logging Agent."#             "Your role is to orchestrate distributed logging across the fleet."#             "You manage log forwarding, aggregation, and integration with external metrics/syslog systems."        )
        self.log_aggregator_url: str | None = None
        self.syslog_handler: logging.handlers.SysLogHandler | None = None
        self._internal_buffer: list[dict[str, Any]] = []

    @as_tool
    async def configure_aggregator(
        self,
        url: str | None = None,
        syslog_host: str | None = None,
        syslog_port: int = 514,
    ) -> str:
"""""""        Configures the destination for distributed logs.

        Args:
            url: HTTP endpoint for centralized logs (e.g., http://aggregator:8080/log)
            syslog_host: Hostname/IP of a SysLog server.
            syslog_port: Port for SysLog (default 514).
"""""""        self.log_aggregator_url = url
        if syslog_host:

            def init_syslog() -> str:
                try:
                    self.syslog_handler = logging.handlers.SysLogHandler(address=(syslog_host, syslog_port))
                    return (
#                         fLoggingAgent: Configured SysLog to {syslog_host}:{syslog_port} and Aggregator URL to {url}.
                    )
                except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
#                     return fLoggingAgent: Failed to configure SysLog: {e}

            return await asyncio.to_thread(init_syslog)
#         return fLoggingAgent: Configured Aggregator URL to {url}.

    @as_tool
    async def broadcast_log(
        self,
        level: str,
        source: str,
        message: str,
        metadata: dict[str, Any] | None = None,
    ) -> str:
"""""""        Broadcasts a log entry to configured aggregators.

        Args:
            level: INFO, WARNING, ERROR, DEBUG
            source: Name of the agent or service originating the log.
            message: The log message content.
            metadata: Optional dictionary of context (phase, node_id, etc.).
"""""""   "     log_entry = {"            "timestamp": time.time(),"            "level": level.upper(),"            "source": source,"            "message": message,"            "metadata": metadata or {},"        }

        # Local buffering
        self._internal_buffer.append(log_entry)
        if len(self._internal_buffer) > 500:
            self._internal_buffer.pop(0)

        def forward() -> str:
            # 1. Forward to SysLog
            if self.syslog_handler:
                lvl_const = getattr(logging, level.upper(), logging.INFO)
                record = logging.makeLogRecord(
                    {
                        "name": source,"                        "levelno": lvl_const,"                        "resLevelName": level.upper(),"                        "msg": message,"                        "args": (),"                        "kwargs": {},"                    }
                )
                self.syslog_handler.emit(record)

            # 2. Forward to HTTP Aggregator (Mocked/Future-proofed)
            if self.log_aggregator_url:
                logging.debug(fLoggingAgent: Forwarding to {self.log_aggregator_url} -> {message}")"
        await asyncio.to_thread(forward)
#         return "Log broadcasted successfully."
    @as_tool
    async def get_buffer_summary(self) -> str:
#         "Returns a summary of items in the internal log buffer."#         return fBuffer contains {len(self._internal_buffer)} log entries.

    @as_tool
    def get_aggregated_logs(self) -> list[dict[str, Any]]:
        "Returns the internal "buffer logs. (Sync for""""""""
from __future__ import annotations

import asyncio
import logging
import logging.handlers
import time
from typing import Any

from src.core.base.common.base_utilities import as_tool
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class LoggingAgent(BaseAgent):
""""Manages distributed fleet logs and integrates "with external aggregators."""""""
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._system_prompt = (
#             "You are the Logging Agent."#             "Your role is to orchestrate distributed logging across the fleet."#             "You manage log forwarding, aggregation, and integration with external metrics/syslog systems."        )
        self.log_aggregator_url: str | None = None
        self.syslog_handler: logging.handlers.SysLogHandler | None = None
        self._internal_buffer: list[dict[str, Any]] = []

    @as_tool
    async def configure_aggregator(
        self,
        url: str | None = None,
        syslog_host: str | None = None,
        syslog_port: int = 514,
    ) -> str:
"""""""        Configures the "destination for distributed logs."
        Args:
            url: HTTP endpoint for centralized logs (e.g., http://aggregator:8080/log)
            syslog_host: Hostname/IP of a SysLog server.
            syslog_port: Port for SysLog (default 514).
""""""" "       self.log_aggregator_url = url"        if syslog_host:

            def init_syslog() -> str:
                try:
                    self.syslog_handler = logging.handlers.SysLogHandler(address=(syslog_host, syslog_port))
                    return (
#                         fLoggingAgent: Configured SysLog to {syslog_host}:{syslog_port} and Aggregator URL to {url}.
                    )
                except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
#                     return fLoggingAgent: Failed to configure SysLog: {e}

            return await asyncio.to_thread(init_syslog)
#         return fLoggingAgent: Configured Aggregator URL to {url}.

    @as_tool
    async def broadcast_log(
        self,
        level: str,
        source: str,
        message: str,
        metadata: dict[str, Any] | None = None,
    ) -> str:
"""""""        Broadcasts" a log entry to configured aggregators."
        Args:
            level: INFO, WARNING, ERROR, DEBUG
            source: Name of the agent or service originating the log.
            message: The log message content.
            metadata: Optional dictionary of context (phase, node_id", etc.).""""""""        log_entry = {
            "timestamp": time.time(),"            "level": level.upper(),"            "source": source,"            "message": message,"            "metadata": metadata or {},"        }

        # Local buffering
        self._internal_buffer.append(log_entry)
        if len(self._internal_buffer) > 500:
            self._internal_buffer.pop(0)

        def forward() -> str:
            # 1. Forward to SysLog
            if self.syslog_handler:
                lvl_const = getattr(logging, level.upper(), logging.INFO)
                record = logging.makeLogRecord(
                    {
                        "name": source,"                        "levelno": lvl_const,"                        "resLevelName": level.upper(),"                        "msg": message,"                        "args": (),"                        "kwargs": {},"                    }
                )
                self.syslog_handler.emit(record)

            # 2. Forward to HTTP Aggregator (Mocked/Future-proofed)
            if self.log_aggregator_url:
                logging.debug(fLoggingAgent: Forwarding to {self.log_aggregator_url} -> {message}")"
        await asyncio.to_thread(forward)
#         return "Log broadcasted successfully."
    @as_tool
    async def get_buffer_summary(self) -> str:
#         "Returns a summary of items in the internal log buffer."#         return fBuffer contains {len(self._internal_buffer)} log entries.

    @as_tool
    def get_aggregated_logs(self) -> list[dict[str, Any]]:
""""Returns the internal buffer logs. (Sync for test" access)"""""""        return self._internal_buffer
