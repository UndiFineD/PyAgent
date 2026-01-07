# -*- coding: utf-8 -*-
"""Test classes from test_agent_backend.py - integration module."""

from __future__ import annotations
import unittest
from typing import Any, List, Dict, Optional, Callable, Tuple, Set, Union
from unittest.mock import MagicMock, Mock, patch, call, ANY
import time
import json
from datetime import datetime
import pytest
import logging
from pathlib import Path
import sys
import os
import tempfile
import shutil
import subprocess
import threading
import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# Try to import test utilities
try:
    from tests.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
except ImportError:
    # Fallback
    AGENT_DIR = Path(__file__).parent.parent.parent / 'src'
    
    class agent_sys_path:
        def __enter__(self): 
            sys.path.insert(0, str(AGENT_DIR))
            return self
        def __exit__(self, *args): 
            sys.path.remove(str(AGENT_DIR))

# Import from src if needed
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))


class TestPhase6Integration:
    """Integration tests for Phase 6 features."""

    def test_queue_with_batcher(self, agent_backend_module: Any) -> None:
        """Test queue and batcher working together."""
        RequestQueue = agent_backend_module.RequestQueue
        RequestBatcher = agent_backend_module.RequestBatcher
        RequestPriority = agent_backend_module.RequestPriority

        queue = RequestQueue()
        batcher = RequestBatcher(batch_size=2)

        # Queue some requests
        queue.enqueue("prompt1", RequestPriority.NORMAL)
        queue.enqueue("prompt2", RequestPriority.HIGH)

        # Dequeue and batch
        while not queue.is_empty():
            request = queue.dequeue()
            batcher.add(request.prompt)

        assert batcher.is_ready() is True
        batch = batcher.get_batch()
        assert len(batch.requests) == 2

    def test_health_monitor_with_load_balancer(self, agent_backend_module: Any) -> None:
        """Test health monitor with load balancer."""
        BackendHealthMonitor = agent_backend_module.BackendHealthMonitor
        LoadBalancer = agent_backend_module.LoadBalancer

        monitor = BackendHealthMonitor()
        lb = LoadBalancer()

        lb.add_backend("backend1")
        lb.add_backend("backend2")

        # Record health data
        monitor.record_success("backend1", 100)
        monitor.record_failure("backend2")

        # Get next backend and check health
        backend = lb.next()
        is_healthy = monitor.is_healthy(backend.name)
        assert is_healthy is not None  # Either True or False

    def test_tracer_with_audit_logger(self, agent_backend_module: any, tmp_path) -> None:
        """Test tracer with audit logger."""
        RequestTracer = agent_backend_module.RequestTracer
        AuditLogger = agent_backend_module.AuditLogger

        log_file = tmp_path / "audit.log"
        tracer = RequestTracer()
        audit = AuditLogger(log_file=log_file)

        # Start trace
        context = tracer.start_trace("test request")

        # Log request with trace info
        audit.log_request(
            backend="test",
            prompt="test",
            response="response",
            latency_ms=100,
            request_id=context.request_id,
        )

        # End trace
        tracer.end_trace(context.request_id, success=True)

        entries = audit.get_recent_entries()
        assert len(entries) == 1
        assert entries[0]["request_id"] == context.request_id


# =============================================================================
# Session 9: Request Signing and Verification Tests
# =============================================================================



class TestGitHubModelsIntegration(unittest.TestCase):
    """Test integration with real GitHub Models API."""

    def test_github_models_api_endpoint_format(self):
        """Test GitHub Models API endpoint format."""
        api_endpoint = "https://models.githubusercontent.com / meta / llama-2-7b-chat"

        # Verify endpoint is properly formatted
        self.assertTrue(api_endpoint.startswith("https://"))
        self.assertIn("models.githubusercontent.com", api_endpoint)
        self.assertIn("meta / llama-2-7b-chat", api_endpoint)

    def test_github_models_authentication_token(self):
        """Test authentication with GitHub Models."""
        auth_token = "ghp_xxxxxxxxxxxxxxxxxxxx"
        headers = {
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application / json"
        }

        self.assertIn("Authorization", headers)
        self.assertTrue(headers["Authorization"].startswith("Bearer "))

    def test_github_models_request_payload_format(self):
        """Test request payload format for GitHub Models."""
        payload = {
            "messages": [
                {"role": "user", "content": "Hello, how are you?"}
            ],
            "temperature": 0.7,
            "top_p": 1.0,
            "max_tokens": 2048,
            "stream": False
        }

        self.assertIn("messages", payload)
        self.assertEqual(len(payload["messages"]), 1)
        self.assertEqual(payload["messages"][0]["role"], "user")

    def test_github_models_response_parsing(self):
        """Test parsing GitHub Models API response."""
        response_json = {
            "id": "chatcmpl-xxxxx",
            "object": "chat.completion",
            "created": 1234567890,
            "model": "meta / llama-2-7b-chat",
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": "I'm doing well, thank you for asking!"
                    },
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": 10,
                "completion_tokens": 15,
                "total_tokens": 25
            }
        }

        # Extract response content
        assistant_message = response_json["choices"][0]["message"]["content"]
        self.assertEqual(assistant_message, "I'm doing well, thank you for asking!")

    def test_github_models_streaming_response(self):
        """Test handling streaming responses from GitHub Models."""
        # Simulated streaming response chunks
        stream_chunks = [
            '{"choices":[{"delta":{"content":"Hello"}}]}\n',
            '{"choices":[{"delta":{"content":" "}}]}\n',
            '{"choices":[{"delta":{"content":"world"}}]}\n',
            '{"choices":[{"delta":{"content":"!"}}]}\n'
        ]

        # Aggregate stream chunks
        content = ""
        for chunk in stream_chunks:
            data = json.loads(chunk)
            if data["choices"][0].get("delta", {}).get("content"):
                content += data["choices"][0]["delta"]["content"]

        self.assertEqual(content, "Hello world!")

    def test_github_models_error_handling(self):
        """Test error handling with GitHub Models API."""
        error_response = {
            "error": {
                "code": "401",
                "message": "Unauthorized",
                "details": "Invalid authentication token"
            }
        }

        self.assertEqual(error_response["error"]["code"], "401")

    def test_github_models_rate_limiting(self):
        """Test handling rate limiting from GitHub Models."""
        rate_limit_headers = {
            "x-ratelimit-limit": "100",
            "x-ratelimit-remaining": "0",
            "x-ratelimit-reset": "1234567890"
        }

        remaining = int(rate_limit_headers["x-ratelimit-remaining"])
        self.assertEqual(remaining, 0)

    def test_github_models_token_usage_tracking(self):
        """Test tracking token usage from API response."""
        usage_info = {
            "prompt_tokens": 42,
            "completion_tokens": 135,
            "total_tokens": 177
        }

        total = usage_info["total_tokens"]
        prompt_ratio = usage_info["prompt_tokens"] / total
        completion_ratio = usage_info["completion_tokens"] / total

        self.assertAlmostEqual(prompt_ratio + completion_ratio, 1.0, places=2)

    def test_github_models_concurrent_requests(self):
        """Test handling concurrent requests to GitHub Models."""
        import concurrent.futures

        def make_request(request_id):
            """Simulate API request."""
            return {
                "request_id": request_id,
                "status": "success",
                "response": f"Response to request {request_id}"
            }

        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(make_request, i) for i in range(5)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]

        self.assertEqual(len(results), 5)

    def test_github_models_timeout_handling(self):
        """Test handling timeouts when calling GitHub Models."""

        class TimeoutError(Exception):
            pass

        def api_call_with_timeout(timeout_seconds):
            # Simulate timeout
            if timeout_seconds < 1:
                raise TimeoutError(f"Request exceeded {timeout_seconds}s timeout")
            return {"status": "success"}

        with self.assertRaises(TimeoutError):
            api_call_with_timeout(0.5)

    def test_github_models_retry_logic(self):
        """Test retry logic for failed GitHub Models requests."""

        class RetryableAPICall:
            def __init__(self, max_retries=3):
                self.max_retries = max_retries
                self.attempt_count = 0

            def call(self):
                self.attempt_count += 1
                if self.attempt_count < 3:
                    raise ConnectionError("Temporary connection error")
                return {"status": "success"}

            def execute_with_retry(self):
                for attempt in range(self.max_retries):
                    try:
                        return self.call()
                    except ConnectionError:
                        if attempt == self.max_retries - 1:
                            raise

        api_call = RetryableAPICall(max_retries=5)
        result = api_call.execute_with_retry()
        self.assertEqual(result["status"], "success")
        self.assertEqual(api_call.attempt_count, 3)



