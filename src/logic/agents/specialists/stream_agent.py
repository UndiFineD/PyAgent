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

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""
Stream agent.py module.
"""
# StreamAgent: n8n and External Workflow Integration - Phase 319 Enhanced

from __future__ import annotations

import asyncio
import contextlib
import json
import re
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

from src.core.base.common.base_utilities import as_tool
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class WebhookStatus(Enum):
    """Possible statuses for a webhook delivery."""
    SUCCESS = "success"
    FAILED = "failed"
    TIMEOUT = "timeout"
    RETRY = "retry"
    RATE_LIMITED = "rate_limited"


@dataclass
class WebhookConfig:
    """Configuration for a webhook endpoint."""

    url: str
    name: str
    method: str = "POST"
    headers: Dict[str, str] = field(default_factory=dict)
    timeout: float = 10.0
    max_retries: int = 3
    retry_delay: float = 1.0
    schema: Optional[Dict[str, Any]] = None


@dataclass
class StreamEvent:
    """Represents an event in the data stream."""

    event_type: str
    payload: Dict[str, Any]
    timestamp: float = field(default_factory=time.time)
    source: str = "unknown"
    correlation_id: Optional[str] = None


# pylint: disable=too-many-ancestors
class StreamAgent(BaseAgent):
    """
    Agent specializing in streaming data injection and extraction.
    Interfaces with n8n, Zapier, Make, and other webhook-based automation platforms.
    """

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._webhooks: Dict[str, WebhookConfig] = {}
        self._event_buffer: List[StreamEvent] = []
        self._transformers: Dict[str, Callable] = {}
        self._delivery_log: List[Dict[str, Any]] = []
        self._system_prompt = (
            "You are the Stream Agent. You act as a bridge between PyAgent "
            "and external automation tools like n8n. You handle data transformation, "
            "schema validation, and reliable webhook delivery with retries."
        )

    @as_tool
    # pylint: disable=too-many-positional-arguments
    async def register_external_webhook(
        self,
        name: str,
        url: str,
        method: str = "POST",
        headers: Optional[Dict[str, str]] = None,
        timeout: float = 10.0,
        max_retries: int = 3,
        schema: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Registers an external automation webhook (n8n, etc.)."""
        config = WebhookConfig(
            url=url,
            name=name,
            method=method,
            headers=headers or {"Content-Type": "application/json"},
            timeout=timeout,
            max_retries=max_retries,
            schema=schema,
        )
        self._webhooks[name] = config

        return {"success": True, "webhook_name": name, "url": url, "registered_webhooks": list(self._webhooks.keys())}

    @as_tool
    async def push_to_n8n(
        self, webhook_url: str, data: Dict, webhook_name: Optional[str] = None, validate_schema: bool = True
    ) -> Dict[str, Any]:
        """Sends data to an n8n webhook with retry logic and validation."""
        from src.infrastructure.security.network.firewall import ReverseProxyFirewall

        # Get config if named webhook
        config = self._webhooks.get(webhook_name) if webhook_name else None
        if config:
            webhook_url = config.url

        firewall = ReverseProxyFirewall()

        # Schema validation
        if validate_schema and config and config.schema:
            validation = self._validate_schema(data, config.schema)
            if not validation["valid"]:
                return {"success": False, "error": "schema_validation_failed", "details": validation["errors"]}

        # Retry logic
        max_retries = config.max_retries if config else 3
        timeout = config.timeout if config else 10.0
        headers = config.headers if config else {"Content-Type": "application/json"}

        last_error = None
        for attempt in range(max_retries):
            try:
                response = firewall.post(webhook_url, json=data, headers=headers, timeout=timeout)

                status = WebhookStatus.SUCCESS if response.status_code in (200, 201, 202) else WebhookStatus.FAILED

                result = {
                    "success": status == WebhookStatus.SUCCESS,
                    "status_code": response.status_code,
                    "attempt": attempt + 1,
                    "webhook_url": webhook_url[:50] + "...",
                    "response_preview": response.text[:200] if response.text else None,
                }

                self._delivery_log.append({**result, "timestamp": time.time(), "payload_size": len(json.dumps(data))})

                if status == WebhookStatus.SUCCESS:
                    return result

            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                last_error = str(e)

            if attempt < max_retries - 1:
                await asyncio.sleep(config.retry_delay if config else 1.0)

        return {"success": False, "status": WebhookStatus.FAILED.value, "error": last_error, "attempts": max_retries}

    @as_tool
    async def extract_from_stream(self, raw_stream: str, extract_type: str = "auto") -> Dict[str, Any]:
        """Parses complex stream data into a structured schema."""
        if extract_type == "json":
            return self._extract_json(raw_stream)
        if extract_type == "csv":
            return self._extract_csv(raw_stream)
        if extract_type == "xml":
            return self._extract_xml(raw_stream)

        # Auto-detect and use LLM for complex extraction
        prompt = (
            f"Extract key entities and variables from this stream data:\n\n"
            f"{raw_stream[:2000]}\n\n"
            "Output structured JSON with:\n"
            "- 'entities': list of named entities found\n"
            "- 'variables': key-value pairs of variables\n"
            "- 'format': detected data format\n"
            "- 'schema': inferred schema"
        )
        res = await self.improve_content(prompt)

        with contextlib.suppress(ValueError, TypeError, AttributeError, json.JSONDecodeError, KeyError):
            match = re.search(r"(\{[\s\S]*\})", res)
            if match:
                return json.loads(match.group(1))

        return {"raw": res, "format": "unknown"}

    @as_tool
    async def transform_data(
        self, data: Dict[str, Any], mapping: Dict[str, str], filters: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Transforms data using a field mapping and optional filters."""
        result = {}

        for target_key, source_path in mapping.items():
            value = self._get_nested_value(data, source_path)
            if value is not None:
                result[target_key] = value

        # Apply filters
        if filters:
            for filter_expr in filters:
                self._apply_filter(result, filter_expr)

        return {"transformed": result, "original_keys": list(data.keys()), "mapped_keys": list(result.keys())}

    def _apply_filter(self, result: Dict[str, Any], filter_expr: str) -> None:
        """Helper to apply a single filter to result - reduces nesting."""
        try:
            parts = filter_expr.split()
            if len(parts) != 3:
                return
            fld, op, val = parts
            field_val = result.get(fld)
            if field_val is None:
                return

            if op == ">" and float(field_val) <= float(val):
                result["_filtered_out"] = True
            elif op == "<" and float(field_val) >= float(val):
                result["_filtered_out"] = True
            elif op == "==" and str(field_val) != val:
                result["_filtered_out"] = True
        except (ValueError, TypeError, AttributeError):
            pass

    @as_tool
    async def buffer_event(self, event_type: str, payload: Dict[str, Any], source: str = "manual") -> Dict[str, Any]:
        """Buffers an event for batch processing."""
        event = StreamEvent(event_type=event_type, payload=payload, source=source)
        self._event_buffer.append(event)

        return {"buffered": True, "buffer_size": len(self._event_buffer), "event_type": event_type}

    @as_tool
    async def flush_buffer(self, webhook_name: str) -> Dict[str, Any]:
        """Flushes buffered events to a registered webhook."""
        if webhook_name not in self._webhooks:
            return {"success": False, "error": f"Webhook '{webhook_name}' not registered"}

        events = self._event_buffer.copy()
        self._event_buffer.clear()

        if not events:
            return {"success": True, "message": "Buffer was empty", "flushed": 0}

        payload = {
            "events": [
                {"type": e.event_type, "payload": e.payload, "timestamp": e.timestamp, "source": e.source}
                for e in events
            ],
            "batch_size": len(events),
            "flush_timestamp": time.time(),
        }

        result = await self.push_to_n8n("", payload, webhook_name=webhook_name)
        result["flushed"] = len(events)
        return result

    @as_tool
    async def get_delivery_stats(self) -> Dict[str, Any]:
        """Returns delivery statistics."""
        if not self._delivery_log:
            return {"total_deliveries": 0, "success_rate": "N/A"}

        successes = sum(1 for d in self._delivery_log if d.get("success"))
        total = len(self._delivery_log)

        return {
            "total_deliveries": total,
            "successful": successes,
            "failed": total - successes,
            "success_rate": f"{successes / total:.1%}",
            "registered_webhooks": list(self._webhooks.keys()),
            "buffer_size": len(self._event_buffer),
            "recent_deliveries": self._delivery_log[-5:],
        }

    def _validate_schema(self, data: Dict, schema: Dict) -> Dict[str, Any]:
        """Simple schema validation."""
        errors = []
        for fld, rules in schema.items():
            if rules.get("required") and fld not in data:
                errors.append(f"Missing required field: {fld}")
            if fld in data and "type" in rules:
                expected_type = rules["type"]
                actual_type = type(data[fld]).__name__
                if expected_type != actual_type:
                    errors.append(f"Type mismatch for {fld}: expected {expected_type}, got {actual_type}")
        return {"valid": not errors, "errors": errors}

    def _get_nested_value(self, data: Dict, path: str) -> Any:
        """Gets a nested value using dot notation."""
        keys = path.split(".")
        value = data
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
            else:
                return None
        return value

    def _extract_json(self, raw: str) -> Dict[str, Any]:
        """Extracts JSON from raw string."""
        with contextlib.suppress(Exception):
            return {"data": json.loads(raw), "format": "json"}

        match = re.search(r"(\{[\s\S]*\}|\[[\s\S]*\])", raw)
        if match:
            with contextlib.suppress(Exception):
                return {"data": json.loads(match.group(1)), "format": "json"}

        return {"error": "json_parse_failed", "raw": raw[:500]}

    def _extract_csv(self, raw: str) -> Dict[str, Any]:
        """Extracts CSV data."""
        lines = raw.strip().split("\n")
        if len(lines) < 2:
            return {"error": "insufficient_csv_lines", "raw": raw[:500]}

        headers = [h.strip() for h in lines[0].split(",")]
        rows = []
        for line in lines[1:]:
            values = [v.strip() for v in line.split(",")]
            rows.append(dict(zip(headers, values)))

        return {"headers": headers, "rows": rows, "row_count": len(rows), "format": "csv"}

    def _extract_xml(self, raw: str) -> Dict[str, Any]:
        """Basic XML extraction using regex."""
        tags = re.findall(r"<(\w+)>([^<]+)</\1>", raw)
        return {"elements": dict(tags), "format": "xml"}
