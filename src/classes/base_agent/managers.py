#!/usr/bin/env python3
# Copyright (c) 2025 DebVisor contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

"""Manager and utility classes for BaseAgent."""

import hashlib
import json
import logging
import random
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, cast, TYPE_CHECKING

if TYPE_CHECKING:
    from .agent import BaseAgent

from .models import (
    AuthConfig, AuthMethod, BatchResult, ConfigProfile,
    FilePriority, FilePriorityConfig, InputType, MessageRole, ModelConfig,
    MultimodalInput, PromptTemplate, SerializationConfig,
    SerializationFormat, _empty_dict_str_any, _empty_dict_str_int,
    _empty_dict_str_str, _empty_list_str, _empty_agent_event_handlers,
    _empty_list_float, _empty_dict_str_health_checks, _empty_dict_str_configprofile,
    AgentEvent
)


# ========== Prompt Management ==========

class PromptTemplateManager:
    """Manages a collection of prompt templates."""

    def __init__(self) -> None:
        """Initialize the template manager."""
        self.templates: Dict[str, PromptTemplate] = {}

    def register(self, template: PromptTemplate) -> None:
        """Register a prompt template.

        Args:
            template: PromptTemplate to register.
        """
        self.templates[template.name] = template

    def render(self, template_name: str, **kwargs: Any) -> str:
        """Render a template by name.

        Args:
            template_name: Name of the template to render.
            **kwargs: Variables to substitute in the template.

        Returns:
            Rendered template string.

        Raises:
            KeyError: If template not found.
        """
        template = self.templates[template_name]
        return template.render(**kwargs)


class ConversationHistory:
    """Manages a conversation history with message storage and retrieval."""

    def __init__(self, max_messages: int = 100) -> None:
        """Initialize conversation history.

        Args:
            max_messages: Maximum number of messages to keep.
        """
        self.messages: List[Any] = []
        self.max_messages = max_messages

    def add(self, role: MessageRole, content: str) -> None:
        """Add a message to the history.

        Args:
            role: Message role (user, assistant, system).
            content: Message content.
        """
        from .models import ConversationMessage
        msg = ConversationMessage(role=role, content=content)
        self.messages.append(msg)

        # Keep only the last max_messages
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]

    def get_context(self) -> List[Any]:
        """Get conversation context (all messages).

        Returns:
            List of conversation messages.
        """
        return self.messages.copy()

    def clear(self) -> None:
        """Clear all messages from history."""
        self.messages.clear()


class ResponsePostProcessor:
    """Manages post-processing hooks for agent responses."""

    def __init__(self) -> None:
        """Initialize the post-processor."""
        self.hooks: List[tuple[Callable[[str], str], int]] = []

    def register(self, hook: Callable[[str], str], priority: int = 0) -> None:
        """Register a post-processing hook.

        Args:
            hook: Function that takes text and returns processed text.
            priority: Priority level (higher = executed first).
        """
        self.hooks.append((hook, priority))

    def process(self, text: str) -> str:
        """Process text through all registered hooks in priority order.

        Args:
            text: Text to process.

        Returns:
            Processed text.
        """
        # Sort by priority (descending), then execute in order
        sorted_hooks = sorted(self.hooks, key=lambda x: x[1], reverse=True)
        for hook, _ in sorted_hooks:
            text = hook(text)
        return text


# ========== Batch Processing ==========

class BatchRequest:
    """Request in a batch processing queue.

    Supports both generic batching (with items) and file-based batching.

    Attributes:
        file_path: Path to the file to process (optional).
        prompt: Improvement prompt (optional).
        priority: Processing priority.
        callback: Optional callback on completion.
        max_size: Maximum batch size (for generic batching).
        items: Items in the batch (for generic batching).
    """

    def __init__(
        self,
        file_path: Optional[Path] = None,
        prompt: Optional[str] = None,
        priority: FilePriority = FilePriority.NORMAL,
        callback: Optional[Callable[[str], None]] = None,
        max_size: Optional[int] = None
    ) -> None:
        """Initialize batch request.

        Supports both old file-based API and new generic batching API.

        Args:
            file_path: Path to file (old API).
            prompt: Prompt text (old API).
            priority: Processing priority (old API).
            callback: Completion callback (old API).
            max_size: Max items before flush (new API).
        """
        # Old API fields
        self.file_path = file_path
        self.prompt = prompt or ""
        self.priority = priority
        self.callback = callback

        # New API fields
        self.max_size = max_size
        self.items: List[Any] = []

    def add(self, item: Any) -> None:
        """Add item to batch (new API).

        Args:
            item: Item to add.
        """
        # If at max size, don't add
        if self.max_size is not None and len(self.items) >= self.max_size:
            return
        self.items.append(item)

    @property
    def size(self) -> int:
        """Get batch size (new API)."""
        return len(self.items)

    def execute(self, processor: Callable[[List[Any]], List[Any]]) -> List[Any]:
        """Execute batch with processor (new API).

        Args:
            processor: Function to process batch items.

        Returns:
            Processed results.
        """
        return processor(self.items)


class RequestBatcher:
    """Batch processor for multiple file requests.

    Handles efficient processing of multiple files in batches
    with priority-based ordering and parallel execution.

    Attributes:
        batch_size: Maximum requests per batch.
        max_concurrent: Maximum concurrent requests.
        queue: Pending batch requests.
        results: Completed batch results.

    Example:
        batcher = RequestBatcher(batch_size=10)
        batcher.add_request(BatchRequest(Path("file.py"), "Improve"))
        results = batcher.process_all(agent_factory)
    """

    def __init__(
        self,
        batch_size: int = 10,
        max_concurrent: int = 4
    ) -> None:
        """Initialize the request batcher.

        Args:
            batch_size: Maximum requests per batch.
            max_concurrent: Maximum concurrent requests.
        """
        self.batch_size = batch_size
        self.max_concurrent = max_concurrent
        self.queue: List[BatchRequest] = []
        self.results: List[BatchResult] = []
        logging.debug(f"RequestBatcher initialized with batch_size={batch_size}")

    def add_request(self, request: BatchRequest) -> None:
        """Add a request to the queue.

        Args:
            request: The batch request to add.
        """
        self.queue.append(request)
        logging.debug(f"Added request for {request.file_path}")

    def add_requests(self, requests: List[BatchRequest]) -> None:
        """Add multiple requests to the queue.

        Args:
            requests: List of batch requests to add.
        """
        self.queue.extend(requests)
        logging.debug(f"Added {len(requests)} requests to queue")

    def get_queue_size(self) -> int:
        """Get the current queue size.

        Returns:
            Number of pending requests.
        """
        return len(self.queue)

    def clear_queue(self) -> None:
        """Clear all pending requests."""
        self.queue.clear()
        logging.debug("Request queue cleared")

    def _sort_by_priority(self) -> List[BatchRequest]:
        """Sort requests by priority (highest first).

        Returns:
            Sorted list of requests.
        """
        return sorted(self.queue, key=lambda r: r.priority.value, reverse=True)

    def process_batch(
        self,
        agent_factory: Callable[[str], 'BaseAgent']
    ) -> List[BatchResult]:
        """Process a single batch of requests.

        Args:
            agent_factory: Factory function to create agents.

        Returns:
            List of batch results.
        """
        sorted_requests = self._sort_by_priority()
        batch = sorted_requests[:self.batch_size]
        results: List[BatchResult] = []

        for request in batch:
            start_time = time.time()
            try:
                agent = agent_factory(str(request.file_path))
                agent.read_previous_content()
                content = agent.improve_content(request.prompt)

                result = BatchResult(
                    file_path=request.file_path,
                    success=True,
                    content=content,
                    processing_time=time.time() - start_time
                )

                if request.callback:
                    request.callback(content)

            except Exception as e:
                result = BatchResult(
                    file_path=request.file_path,
                    success=False,
                    error=str(e),
                    processing_time=time.time() - start_time
                )

            results.append(result)
            self.queue.remove(request)

        self.results.extend(results)
        return results

    def process_all(
        self,
        agent_factory: Callable[[str], 'BaseAgent']
    ) -> List[BatchResult]:
        """Process all queued requests.

        Args:
            agent_factory: Factory function to create agents.

        Returns:
            List of all batch results.
        """
        all_results: List[BatchResult] = []
        while self.queue:
            batch_results = self.process_batch(agent_factory)
            all_results.extend(batch_results)
        return all_results

    def get_stats(self) -> Dict[str, Any]:
        """Get batch processing statistics.

        Returns:
            Dictionary with processing stats.
        """
        if not self.results:
            return {"processed": 0, "success_rate": 0.0, "avg_time": 0.0}

        successful = sum(1 for r in self.results if r.success)
        total_time = sum(r.processing_time for r in self.results)

        return {
            "processed": len(self.results),
            "successful": successful,
            "failed": len(self.results) - successful,
            "success_rate": successful / len(self.results),
            "avg_time": total_time / len(self.results),
            "total_time": total_time,
        }


# ========== Authentication & Authorization ==========

class AuthenticationManager:
    """Manager for authentication methods.

    Handles various authentication methods for AI backends
    including API keys, bearer tokens, OAuth2, and custom auth.

    Attributes:
        config: Authentication configuration.
        token_cache: Cached authentication tokens.

    Example:
        auth = AuthenticationManager(AuthConfig(method=AuthMethod.BEARER_TOKEN, token="xxx"))
        headers = auth.get_headers()
    """

    def __init__(self, config: Optional[AuthConfig] = None) -> None:
        """Initialize authentication manager.

        Args:
            config: Authentication configuration.
        """
        self.config = config or AuthConfig()
        self.token_cache: Dict[str, str] = {}
        logging.debug(f"AuthenticationManager initialized with method={self.config.method.value}")

    def get_headers(self) -> Dict[str, str]:
        """Get authentication headers.

        Returns:
            Dictionary of HTTP headers for authentication.
        """
        headers: Dict[str, str] = {}

        if self.config.method == AuthMethod.API_KEY:
            headers["X-API-Key"] = self.config.api_key
        elif self.config.method == AuthMethod.BEARER_TOKEN:
            headers["Authorization"] = f"Bearer {self.config.token}"
        elif self.config.method == AuthMethod.BASIC_AUTH:
            import base64
            credentials = f"{self.config.username}:{self.config.password}"
            encoded = base64.b64encode(credentials.encode()).decode()
            headers["Authorization"] = f"Basic {encoded}"
        elif self.config.method == AuthMethod.OAUTH2:
            token = self._get_oauth_token()
            headers["Authorization"] = f"Bearer {token}"

        # Add custom headers
        headers.update(self.config.custom_headers)

        return headers

    def _get_oauth_token(self) -> str:
        """Get OAuth2 token (with caching).

        Returns:
            OAuth2 access token.
        """
        cache_key = f"oauth_{self.config.oauth_client_id}"
        if cache_key in self.token_cache:
            return self.token_cache[cache_key]

        # In production, would exchange credentials for token
        # For now, return placeholder
        token = self.config.token or "oauth_token_placeholder"
        self.token_cache[cache_key] = token
        return token

    def refresh_token(self) -> None:
        """Refresh authentication token."""
        self.token_cache.clear()
        logging.debug("Authentication tokens refreshed")

    def set_custom_header(self, key: str, value: str) -> None:
        """Set a custom header.

        Args:
            key: Header name.
            value: Header value.
        """
        self.config.custom_headers[key] = value

    def validate(self) -> bool:
        """Validate authentication configuration.

        Returns:
            True if configuration is valid.
        """
        if self.config.method == AuthMethod.NONE:
            return True
        if self.config.method == AuthMethod.API_KEY:
            return bool(self.config.api_key)
        if self.config.method == AuthMethod.BEARER_TOKEN:
            return bool(self.config.token)
        if self.config.method == AuthMethod.BASIC_AUTH:
            return bool(self.config.username and self.config.password)
        if self.config.method == AuthMethod.OAUTH2:
            return bool(self.config.oauth_client_id and self.config.oauth_client_secret)
        return True


@dataclass
class AuthManager:
    """Manages authentication."""
    method: AuthMethod | str | None = None
    credentials: Dict[str, str] = field(default_factory=_empty_dict_str_str)
    custom_headers: Dict[str, str] = field(default_factory=_empty_dict_str_str)

    def set_method(self, method: str, **kwargs: str) -> None:
        """Set authentication method."""
        self.method = method
        self.credentials = kwargs

    def add_custom_header(self, header: str, value: str) -> None:
        """Add custom header."""
        self.custom_headers[header] = value

    def get_headers(self) -> Dict[str, str]:
        """Get authentication headers."""
        headers = dict(self.custom_headers)

        # Convert enum to string if needed
        method = self.method
        if isinstance(method, AuthMethod):
            method = method.value

        if method == "api_key" and "api_key" in self.credentials:
            headers["X-API-Key"] = self.credentials["api_key"]
        elif method == "token" and "token" in self.credentials:
            headers["Authorization"] = f"Bearer {self.credentials['token']}"
        elif method == "bearer_token" and "token" in self.credentials:
            headers["Authorization"] = f"Bearer {self.credentials['token']}"

        return headers


# ========== Prompt Versioning & A/B Testing ==========

class PromptVersion:
    """Versioned prompt for A/B testing.

    Supports both simple and advanced versioning APIs.

    Attributes:
        version: Version identifier.
        content: The prompt content.
        description: Prompt description.
        active: Whether this version is active.
        created_at: Creation timestamp.
        metrics: Performance metrics.
        version_id: Alias for version (compatibility).
        template_id: Template identifier (compatibility).
        variant: Variant name (compatibility).
        prompt_text: Alias for content (compatibility).
        weight: Selection weight (compatibility).
    """

    def __init__(
        self,
        version: Optional[str] = None,
        content: Optional[str] = None,
        description: str = "",
        active: bool = True,
        version_id: Optional[str] = None,
        template_id: Optional[str] = None,
        variant: Optional[str] = None,
        prompt_text: Optional[str] = None,
        weight: float = 1.0
    ) -> None:
        """Initialize prompt version.

        Supports both new and old parameter names for compatibility.

        Args:
            version: Version string (new API).
            content: Prompt content (new API).
            description: Optional description.
            active: Whether version is active.
            version_id: Version ID (old API, used if version is None).
            template_id: Template ID (old API).
            variant: Variant name (old API).
            prompt_text: Prompt text (old API, used if content is None).
            weight: Selection weight (old API).
        """
        # Support both APIs
        self.version = version or version_id or ""
        self.content = content or prompt_text or ""
        self.description = description
        self.active = active
        self.created_at = datetime.now()
        self.metrics: Dict[str, float] = {}

        # Old API compatibility
        self.version_id = self.version
        self.template_id = template_id or ""
        self.variant = variant or ""
        self.prompt_text = self.content
        self.weight = weight


class PromptVersionManager:
    """Manager for prompt versioning and A/B testing.

    Supports both simple and advanced version management APIs.

    Attributes:
        versions: Registered prompt versions.
        active_version: Currently active version.
        metrics: Collected metrics per version.
    """

    def __init__(self) -> None:
        """Initialize the prompt version manager."""
        self.versions: Dict[str, PromptVersion] = {}
        self.active_version: Optional[str] = None
        self.metrics: Dict[str, Dict[str, float]] = {}
        self._old_api_versions: Dict[str, List[PromptVersion]] = {}  # For old API
        self.selection_history: List[Dict[str, Any]] = []
        logging.debug("PromptVersionManager initialized")

    def register_version(self, version: PromptVersion) -> None:
        """Register a prompt version (old API).

        Args:
            version: The prompt version to register.
        """
        # Old API: organize by template_id
        template_id = version.template_id
        if template_id not in self._old_api_versions:
            self._old_api_versions[template_id] = []
        self._old_api_versions[template_id].append(version)

        # Also store in new API format
        self.versions[version.version_id] = version
        if self.active_version is None:
            self.active_version = version.version_id
        logging.debug(f"Registered version {version.version_id} for {template_id}")

    def add_version(self, version: PromptVersion) -> None:
        """Add a prompt version (new API).

        Args:
            version: The prompt version to add.
        """
        self.versions[version.version] = version
        if self.active_version is None:
            self.active_version = version.version
        logging.debug(f"Added version {version.version}")

    def set_active(self, version: str) -> None:
        """Set the active version (new API).

        Args:
            version: Version identifier.
        """
        if version in self.versions:
            self.active_version = version
            self.versions[version].active = True
            logging.debug(f"Set active version to {version}")

    def get_active(self) -> Optional[PromptVersion]:
        """Get the active version (new API).

        Returns:
            The active prompt version.
        """
        if self.active_version and self.active_version in self.versions:
            return self.versions[self.active_version]
        return None

    def get_versions(self, template_id: str = "") -> List[PromptVersion]:
        """Get all versions (old API).

        Args:
            template_id: The template ID.

        Returns:
            List of prompt versions.
        """
        if template_id:
            return self._old_api_versions.get(template_id, [])
        return list(self.versions.values())

    def select_version(self, template_id: str = "") -> Optional[PromptVersion]:
        """Select a version using weighted random selection (old API).

        Args:
            template_id: The template ID.

        Returns:
            Selected prompt version.
        """
        versions = self.get_versions(template_id)
        if not versions:
            return None

        # Weighted selection
        total_weight = sum(v.weight for v in versions)
        if total_weight <= 0:
            return versions[0]

        r = random.uniform(0, total_weight)
        cumulative = 0.0
        for version in versions:
            cumulative += version.weight
            if r <= cumulative:
                self.selection_history.append({
                    "template_id": template_id,
                    "version_id": version.version_id,
                    "variant": version.variant,
                    "timestamp": time.time()
                })
                return version

        return versions[-1]

    def record_metric(
        self,
        version_id: str,
        metric_name: str,
        value: float
    ) -> None:
        """Record a metric for a version.

        Args:
            version_id: The version ID.
            metric_name: Name of the metric.
            value: Metric value.
        """
        if version_id not in self.metrics:
            self.metrics[version_id] = {}

        # Rolling average for old API
        if metric_name in self.metrics[version_id]:
            current = self.metrics[version_id][metric_name]
            self.metrics[version_id][metric_name] = (current + value) / 2
        else:
            self.metrics[version_id][metric_name] = value

        # Also update in version if it exists
        if version_id in self.versions:
            self.versions[version_id].metrics[metric_name] = value

    def get_best_version(
            self,
            template_id: str = "",
            metric: str = "quality") -> Optional[PromptVersion]:
        """Get the best performing version.

        Args:
            template_id: Optional template ID.
            metric: Metric to use for comparison.

        Returns:
            Best performing version.
        """
        versions = self.get_versions(template_id) if template_id else list(self.versions.values())
        if not versions:
            return None

        best: Optional[PromptVersion] = None
        best_score = -float('inf')

        for version in versions:
            score = version.metrics.get(metric, 0)
            if score > best_score:
                best_score = score
                best = version

        return best

    def generate_report(self, template_id: str = "") -> Dict[str, Any]:
        """Generate a report about versions.

        Args:
            template_id: Optional template ID.

        Returns:
            Report with version statistics.
        """
        report: Dict[str, Any] = {
            "total_versions": len(self.versions),
            "versions": {}
        }

        for version_id, version in self.versions.items():
            report["versions"][version_id] = {
                "content": version.content,
                "active": version.active,
                "metrics": version.metrics
            }

        return report

    def get_ab_report(self, template_id: str) -> Dict[str, Any]:
        """Get A/B testing report for a template (old API).

        Args:
            template_id: The template ID.

        Returns:
            Report with version statistics.
        """
        versions = self.get_versions(template_id)
        selections = [s for s in self.selection_history if s["template_id"] == template_id]

        report: Dict[str, Any] = {
            "template_id": template_id,
            "total_selections": len(selections),
            "versions": {}
        }

        for version in versions:
            version_selections = [s for s in selections if s["version_id"] == version.version_id]
            report["versions"][version.version_id] = {
                "variant": version.variant,
                "selections": len(version_selections),
                "metrics": self.metrics.get(version.version_id, {})
            }

        return report


# ========== Multimodal Processing ==========

class MultimodalProcessor:
    """Processor for multimodal inputs.

    Handles processing of various input types including
    text, images, diagrams, and code for AI backends.

    Attributes:
        inputs: List of multimodal inputs.
        processed: Processed content ready for AI.

    Example:
        processor = MultimodalProcessor()
        processor.add_input(MultimodalInput(InputType.TEXT, "Hello"))
        processor.add_input(MultimodalInput(InputType.IMAGE, base64_data))
        prompt = processor.build_prompt()
    """

    def __init__(self) -> None:
        """Initialize the multimodal processor."""
        self.inputs: List[MultimodalInput] = []
        self.processed: str = ""
        logging.debug("MultimodalProcessor initialized")

    def add_input(self, input_data: MultimodalInput) -> None:
        """Add a multimodal input.

        Args:
            input_data: The input to add.
        """
        self.inputs.append(input_data)
        logging.debug(f"Added {input_data.input_type.value} input")

    def add_text(self, text: str) -> None:
        """Add text input.

        Args:
            text: Text content.
        """
        self.add_input(MultimodalInput(InputType.TEXT, text))

    def add_image(self, data: str, mime_type: str = "image / png") -> None:
        """Add image input (base64 encoded).

        Args:
            data: Base64 encoded image data.
            mime_type: Image MIME type.
        """
        self.add_input(MultimodalInput(InputType.IMAGE, data, mime_type))

    def add_code(self, code: str, language: str = "python") -> None:
        """Add code input.

        Args:
            code: Source code.
            language: Programming language.
        """
        self.add_input(MultimodalInput(
            InputType.CODE,
            code,
            metadata={"language": language}
        ))

    def build_prompt(self) -> str:
        """Build combined prompt from all inputs.

        Returns:
            Combined prompt string.
        """
        parts: List[str] = []

        for inp in self.inputs:
            if inp.input_type == InputType.TEXT:
                parts.append(inp.content)
            elif inp.input_type == InputType.CODE:
                lang = inp.metadata.get("language", "")
                parts.append(f"```{lang}\n{inp.content}\n```")
            elif inp.input_type == InputType.IMAGE:
                parts.append(f"[Image: {inp.mime_type}]")
            elif inp.input_type == InputType.DIAGRAM:
                parts.append(f"[Diagram: {inp.metadata.get('type', 'unknown')}]")

        self.processed = "\n\n".join(parts)
        return self.processed

    def get_api_messages(self) -> List[Dict[str, Any]]:
        """Get messages formatted for multimodal API.

        Returns:
            List of message dictionaries.
        """
        messages: List[Dict[str, Any]] = []

        for inp in self.inputs:
            if inp.input_type == InputType.TEXT:
                messages.append({"type": "text", "text": inp.content})
            elif inp.input_type == InputType.IMAGE:
                messages.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{inp.mime_type};base64,{inp.content}"
                    }
                })
            elif inp.input_type == InputType.CODE:
                messages.append({
                    "type": "text",
                    "text": f"```{inp.metadata.get('language', '')}\n{inp.content}\n```"
                })

        return messages

    def clear(self) -> None:
        """Clear all inputs."""
        self.inputs.clear()
        self.processed = ""


# ========== Agent Composition ==========

class AgentComposer:
    """Composer for multi-agent workflows.

    Orchestrates multiple agents working together on a task,
    handling dependencies and result aggregation.

    Attributes:
        agents: Configured agents for composition.
        results: Results from each agent.
        execution_order: Calculated execution order.

    Example:
        composer = AgentComposer()
        composer.add_agent(ComposedAgent("coder", order=1))
        composer.add_agent(ComposedAgent("tests", order=2, depends_on=["coder"]))
        result = composer.execute(file_path, prompt)
    """

    def __init__(self) -> None:
        """Initialize the agent composer."""
        from .models import ComposedAgent
        self.agents: List[ComposedAgent] = []
        self.results: Dict[str, str] = {}
        self.execution_order: List[str] = []
        logging.debug("AgentComposer initialized")

    def add_agent(self, agent: ComposedAgent) -> None:
        """Add an agent to the composition.

        Args:
            agent: The agent configuration to add.
        """
        self.agents.append(agent)
        self._calculate_execution_order()
        logging.debug(f"Added agent: {agent.agent_type}")

    def _calculate_execution_order(self) -> None:
        """Calculate execution order based on dependencies."""
        # Topological sort
        sorted_agents: List[str] = []
        visited: set[str] = set()
        temp: set[str] = set()

        def visit(agent_type: str) -> None:
            if agent_type in temp:
                raise ValueError(f"Circular dependency detected for {agent_type}")
            if agent_type in visited:
                return

            temp.add(agent_type)
            agent = next((a for a in self.agents if a.agent_type == agent_type), None)
            if agent:
                for dep in agent.depends_on:
                    visit(dep)
            temp.remove(agent_type)
            visited.add(agent_type)
            sorted_agents.append(agent_type)

        for agent in sorted(self.agents, key=lambda a: a.order):
            if agent.agent_type not in visited:
                visit(agent.agent_type)

        self.execution_order = sorted_agents

    def execute(
        self,
        file_path: str,
        prompt: str,
        agent_factory: Callable[[str, str], 'BaseAgent']
    ) -> Dict[str, str]:
        """Execute the composed agents.

        Args:
            file_path: Path to the file to process.
            prompt: Base prompt for agents.
            agent_factory: Factory to create agents (type, path).

        Returns:
            Dictionary of results from each agent.
        """
        self.results.clear()
        current_content = ""

        for agent_type in self.execution_order:
            agent_config = next((a for a in self.agents if a.agent_type == agent_type), None)
            if not agent_config:
                continue

            # Create agent
            agent = agent_factory(agent_type, file_path)

            # Build prompt with context from previous agents
            enhanced_prompt = prompt
            for dep in agent_config.depends_on:
                if dep in self.results:
                    enhanced_prompt += f"\n\nPrevious {dep} result:\n{self.results[dep][:500]}"

            # Process
            if current_content:
                agent.previous_content = current_content

            result = agent.improve_content(enhanced_prompt)
            self.results[agent_type] = result
            current_content = result

        return self.results

    def get_final_result(self) -> str:
        """Get the final aggregated result.

        Returns:
            Content from the last executed agent.
        """
        if not self.execution_order:
            return ""
        return self.results.get(self.execution_order[-1], "")


# ========== Serialization ==========

class SerializationManager:
    """Manager for custom serialization formats.

    Handles serialization and deserialization of agent data
    in various formats with optional compression and encryption.

    Attributes:
        config: Serialization configuration.

    Example:
        manager = SerializationManager(SerializationConfig(format=SerializationFormat.JSON))
        data = manager.serialize({"key": "value"})
        obj = manager.deserialize(data)
    """

    def __init__(self, config: Optional[SerializationConfig] = None) -> None:
        """Initialize serialization manager.

        Args:
            config: Serialization configuration.
        """
        self.config = config or SerializationConfig()
        logging.debug(f"SerializationManager initialized with format={self.config.format.value}")

    def serialize(self, data: Any) -> bytes:
        """Serialize data to bytes.

        Args:
            data: Data to serialize.

        Returns:
            Serialized bytes.
        """
        if self.config.format == SerializationFormat.JSON:
            result = json.dumps(data, indent=2).encode("utf-8")
        elif self.config.format == SerializationFormat.PICKLE:
            import pickle
            result = pickle.dumps(data)
        else:
            # Default to JSON
            result = json.dumps(data).encode("utf-8")

        if self.config.compression:
            import zlib
            result = zlib.compress(result)

        return result

    def deserialize(self, data: bytes) -> Any:
        """Deserialize bytes to data.

        Args:
            data: Serialized bytes.

        Returns:
            Deserialized data.
        """
        if self.config.compression:
            import zlib
            data = zlib.decompress(data)

        if self.config.format == SerializationFormat.JSON:
            return json.loads(data.decode("utf-8"))
        elif self.config.format == SerializationFormat.PICKLE:
            import pickle
            return pickle.loads(data)
        else:
            return json.loads(data.decode("utf-8"))

    def save_to_file(self, data: Any, path: Path) -> None:
        """Save serialized data to file.

        Args:
            data: Data to save.
            path: File path.
        """
        serialized = self.serialize(data)
        path.write_bytes(serialized)
        logging.debug(f"Saved {len(serialized)} bytes to {path}")

    def load_from_file(self, path: Path) -> Any:
        """Load data from file.

        Args:
            path: File path.

        Returns:
            Deserialized data.
        """
        data = path.read_bytes()
        return self.deserialize(data)


# ========== File Priority Management ==========

class FilePriorityManager:
    """Manager for file priority and request ordering.

    Determines file priority based on patterns, extensions,
    and custom rules for request prioritization.

    Attributes:
        config: Priority configuration.

    Example:
        manager = FilePriorityManager()
        manager.set_pattern_priority("*.py", FilePriority.HIGH)
        priority = manager.get_priority(Path("main.py"))
    """

    def __init__(self, config: Optional[FilePriorityConfig] = None) -> None:
        """Initialize priority manager.

        Args:
            config: Priority configuration.
        """
        self.config = config or FilePriorityConfig()
        # Default extension priorities
        self._default_extensions = {
            ".py": FilePriority.HIGH,
            ".js": FilePriority.HIGH,
            ".ts": FilePriority.HIGH,
            ".md": FilePriority.NORMAL,
            ".json": FilePriority.LOW,
            ".txt": FilePriority.LOW,
        }
        logging.debug("FilePriorityManager initialized")

    def set_pattern_priority(self, pattern: str, priority: FilePriority) -> None:
        """Set priority for a path pattern.

        Args:
            pattern: Glob pattern.
            priority: Priority level.
        """
        self.config.path_patterns[pattern] = priority

    def set_extension_priority(self, extension: str, priority: FilePriority) -> None:
        """Set priority for a file extension.

        Args:
            extension: File extension (with dot).
            priority: Priority level.
        """
        self.config.extension_priorities[extension] = priority

    def get_priority(self, path: Path) -> FilePriority:
        """Get priority for a file.

        Args:
            path: File path.

        Returns:
            Priority level.
        """
        # Check path patterns first
        import fnmatch
        path_str = str(path)
        for pattern, priority in self.config.path_patterns.items():
            if fnmatch.fnmatch(path_str, pattern):
                return priority

        # Check extension
        ext = path.suffix.lower()
        if ext in self.config.extension_priorities:
            return self.config.extension_priorities[ext]
        if ext in self._default_extensions:
            return self._default_extensions[ext]

        return self.config.default_priority

    def sort_by_priority(self, paths: List[Path]) -> List[Path]:
        """Sort paths by priority (highest first).

        Args:
            paths: List of file paths.

        Returns:
            Sorted list of paths.
        """
        return sorted(paths, key=lambda p: self.get_priority(p).value, reverse=True)

    def filter_by_priority(
        self,
        paths: List[Path],
        min_priority: FilePriority = FilePriority.LOW
    ) -> List[Path]:
        """Filter paths by minimum priority.

        Args:
            paths: List of file paths.
            min_priority: Minimum priority to include.

        Returns:
            Filtered list of paths.
        """
        return [p for p in paths if self.get_priority(p).value >= min_priority.value]


# ========== Response Caching ==========

@dataclass
class ResponseCache:
    """Caches responses based on prompts."""
    cache_dir: Path
    cache_data: Dict[str, str] = field(default_factory=_empty_dict_str_str)

    def __post_init__(self) -> None:
        """Initialize cache directory."""
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_cache_key(self, prompt: str) -> str:
        """Generate cache key from prompt."""
        return hashlib.md5(prompt.encode()).hexdigest()

    def set(self, prompt: str, response: str) -> None:
        """Cache a response."""
        key = self._get_cache_key(prompt)
        self.cache_data[key] = response

        # Also write to disk
        cache_file = self.cache_dir / f"{key}.json"
        cache_file.write_text(json.dumps({"prompt": prompt, "response": response}))

    def get(self, prompt: str) -> Optional[str]:
        """Get cached response."""
        key = self._get_cache_key(prompt)
        if key in self.cache_data:
            return self.cache_data[key]

        # Try to load from disk
        cache_file = self.cache_dir / f"{key}.json"
        if cache_file.exists():
            data = json.loads(cache_file.read_text())
            self.cache_data[key] = data["response"]
            return data["response"]

        return None

    def invalidate(self, prompt: str) -> None:
        """Invalidate cached response."""
        key = self._get_cache_key(prompt)
        self.cache_data.pop(key, None)

        cache_file = self.cache_dir / f"{key}.json"
        if cache_file.exists():
            cache_file.unlink()


# ========== State Persistence ==========

@dataclass
class StatePersistence:
    """Persists agent state to disk."""
    state_file: Path
    backup: bool = False
    backup_count: int = 0

    def save(self, state: Dict[str, Any]) -> None:
        """Save state to file."""
        if self.backup and self.state_file.exists():
            backup_file = self.state_file.parent / f"{self.state_file.stem}.{self.backup_count}.bak"
            self.state_file.rename(backup_file)
            self.backup_count += 1

        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.state_file.write_text(json.dumps(state))

    def load(self, default: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Load state from file."""
        if self.state_file.exists():
            return json.loads(self.state_file.read_text())

        return default or {}


# ========== Model Selection ==========

@dataclass
class ModelSelector:
    """Selects models for different agent types."""
    models: Dict[str, ModelConfig] = field(default_factory=lambda: {"default": ModelConfig(model_id="gpt-3.5-turbo")})

    def __post_init__(self) -> None:
        """Initialize with default model."""
        if "default" not in self.models:
            self.models["default"] = ModelConfig(model_id="gpt-3.5-turbo")

    def select(self, agent_type: str) -> ModelConfig:
        """Select model for agent type."""
        selected = self.models.get(agent_type)
        if selected is not None:
            return selected
        return self.models["default"]

    def set_model(self, agent_type: str, config: ModelConfig) -> None:
        """Set model for agent type."""
        self.models[agent_type] = config


# ========== Quality Scoring ==========

@dataclass
class QualityScorer:
    """Scores response quality."""
    criteria: Dict[str, tuple[Callable[[str], float], float]] = field(default_factory=lambda: {})

    def add_criterion(self, name: str, func: Callable[[str], float], weight: float = 1.0) -> None:
        """Add scoring criterion."""
        self.criteria[name] = (func, weight)

    def score(self, text: str) -> float:
        """Score response quality."""
        if not self.criteria:
            # Default: score based on length
            length_score = min(1.0, len(text) / 200.0)
            return length_score

        total_weight = 0.0
        total_score = 0.0

        for func, weight in self.criteria.values():
            score = func(text)
            total_score += score * weight
            total_weight += weight

        return total_score / total_weight if total_weight > 0 else 0.0


# ========== A/B Testing ==========

@dataclass
class ABTest:
    """A/B test for variants."""
    name: str
    variants: List[str]
    weights: List[float] = field(default_factory=_empty_list_float)
    variant_counts: Dict[str, int] = field(default_factory=_empty_dict_str_int)

    def __post_init__(self) -> None:
        """Initialize variant counts."""
        for variant in self.variants:
            self.variant_counts[variant] = 0

        # Normalize weights if not provided
        if not self.weights:
            self.weights = [1.0 / len(self.variants)] * len(self.variants)

    def select_variant(self) -> str:
        """Select a variant based on weights."""
        return random.choices(self.variants, weights=self.weights, k=1)[0]


# ========== Event Management ==========

@dataclass
class EventManager:
    """Manages agent events."""
    handlers: Dict[AgentEvent, List[Callable[..., None]]] = field(default_factory=_empty_agent_event_handlers)

    def on(self, event: AgentEvent, handler: Callable[..., None]) -> None:
        """Register event handler."""
        if event not in self.handlers:
            self.handlers[event] = []
        self.handlers[event].append(handler)

    def emit(self, event: AgentEvent, data: Any = None) -> None:
        """Emit event."""
        if event in self.handlers:
            for handler in self.handlers[event]:
                if data is not None:
                    handler(data)
                else:
                    handler()


# ========== Plugin Management ==========

@dataclass
class PluginManager:
    """Manages agent plugins."""
    plugins: Dict[str, Any] = field(default_factory=_empty_dict_str_any)

    def register(self, plugin: Any) -> None:
        """Register a plugin."""
        self.plugins[plugin.name] = plugin

    def activate_all(self) -> None:
        """Activate all plugins."""
        for plugin in self.plugins.values():
            if hasattr(plugin, 'activate'):
                plugin.activate()

    def deactivate(self, name: str) -> None:
        """Deactivate a plugin."""
        if name in self.plugins:
            plugin = self.plugins[name]
            if hasattr(plugin, 'deactivate'):
                plugin.deactivate()


# ========== Health Checking ==========

@dataclass
class HealthChecker:
    """Checks agent health status."""
    checks: Dict[str, Callable[[], Dict[str, Any]]] = field(default_factory=_empty_dict_str_health_checks)
    request_count: int = 0
    error_count: int = 0
    total_latency: int = 0

    def add_check(self, name: str, check_func: Callable[[], Dict[str, Any]]) -> None:
        """Add a health check."""
        self.checks[name] = check_func

    def check(self) -> Dict[str, Any]:
        """Run health check."""
        components: dict[str, Any] = {}
        result: dict[str, Any] = {"status": "healthy", "components": components}

        for name, check_func in self.checks.items():
            components[name] = check_func()

        return result

    def record_request(self, success: bool, latency_ms: int) -> None:
        """Record a request."""
        self.request_count += 1
        self.total_latency += latency_ms
        if not success:
            self.error_count += 1

    def get_metrics(self) -> Dict[str, Any]:
        """Get health metrics."""
        error_rate = self.error_count / self.request_count if self.request_count > 0 else 0
        avg_latency = self.total_latency / self.request_count if self.request_count > 0 else 0

        return {
            "total_requests": self.request_count,
            "error_count": self.error_count,
            "error_rate": error_rate,
            "avg_latency_ms": avg_latency
        }


# ========== Configuration Profiles ==========

@dataclass
class ProfileManager:
    """Manages configuration profiles."""
    profiles: Dict[str, ConfigProfile] = field(default_factory=_empty_dict_str_configprofile)
    active_name: Optional[str] = None

    @property
    def active(self) -> Optional[ConfigProfile]:
        """Get active profile."""
        if self.active_name and self.active_name in self.profiles:
            return self.profiles[self.active_name]
        return None

    def add_profile(self, profile: ConfigProfile) -> None:
        """Add a profile."""
        self.profiles[profile.name] = profile

    def set_active(self, name: str) -> None:
        """Set active profile."""
        if name in self.profiles:
            self.active_name = name

    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get setting from active profile with inheritance."""
        if not self.active:
            return default

        # Check active profile
        if key in self.active.settings:
            return self.active.settings[key]

        # Check parent
        if self.active.parent and self.active.parent in self.profiles:
            parent = self.profiles[self.active.parent]
            if key in parent.settings:
                return parent.settings[key]

        return default
