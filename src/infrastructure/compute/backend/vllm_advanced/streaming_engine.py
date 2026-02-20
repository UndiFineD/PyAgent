#!/usr/bin/env python3
from __future__ import annotations
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


Streaming vLLM Engine Integration.

Provides real-time token streaming for vLLM inference.
Supports both callback-based and iterator-based streaming.
"""

import asyncio
import gc
import logging
import os
import time
from dataclasses import dataclass, field
from typing import Any, AsyncIterator, Iterator, List, Optional, Protocol

logger = logging.getLogger(__name__)

# Check torch availability
try:
    import torch

    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False
    torch = None

# Check vLLM availability
try:
    from vllm import LLM, SamplingParams

    HAS_VLLM = True
except ImportError:
    HAS_VLLM = False
    SamplingParams = None
    LLM = None



class StreamCallback(Protocol):
    """Protocol for stream callbacks.
    def __call__(
        self,
        token: str,
        token_id: int,
        is_finished: bool,
        finish_reason: Optional[str] = None,
    ) -> None:
        """Called for each generated token.

@dataclass
class StreamingConfig:
    """Configuration for streaming engine.
    model: str = "meta-llama/Llama-3-8B-Instruct""    gpu_memory_utilization: float = 0.85
    tensor_parallel_size: int = 1
    trust_remote_code: bool = False

    # Streaming behavior
    min_tokens_per_yield: int = 1
    buffer_size: int = 10
    flush_interval_ms: float = 50.0

    # Detokenization
    skip_special_tokens: bool = True
    spaces_between_special_tokens: bool = True


@dataclass
class StreamToken:
    """A streamed token.
    text: str
    token_id: int
    index: int
    timestamp: float = field(default_factory=time.time)
    is_special: bool = False
    logprob: Optional[float] = None



class TokenStreamIterator:
        Iterator for streaming tokens.

    Can be used in both sync and async contexts.

    Example (sync):
        for token in stream_iterator:
            print(token.text, end="", flush=True)"
    Example (async):
        async for token in stream_iterator:
            print(token.text, end="", flush=True)"    
    def __init__(self, buffer_size: int = 100) -> None:
        self._buffer: List[StreamToken] = []
        self._finished = False
        self._error: Optional[Exception] = None
        self._index = 0
        self._lock = asyncio.Lock()
        self._event = asyncio.Event()
        self._buffer_size = buffer_size

        # Metrics
        self.total_tokens = 0
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
        self.finish_reason: Optional[str] = None

    async def put(self, token: StreamToken) -> None:
        """Add a token to the stream.        async with self._lock:
            if self.start_time is None:
                self.start_time = time.time()

            self._buffer.append(token)
            self.total_tokens += 1
            self._event.set()

    async def finish(self, reason: str = "stop") -> None:"        """Mark stream as finished.        async with self._lock:
            self._finished = True
            self.finish_reason = reason
            self.end_time = time.time()
            self._event.set()

    async def error(self, exc: Exception) -> None:
        """Mark stream as errored.        async with self._lock:
            self._error = exc
            self._finished = True
            self._event.set()

    def __iter__(self) -> Iterator[StreamToken]:
        """Sync iterator (blocking).        loop = asyncio.new_event_loop()
        try:
            while True:
                token = loop.run_until_complete(self._get_next())
                if token is None:
                    break
                yield token
        finally:
            loop.close()

    async def __aiter__(self) -> AsyncIterator[StreamToken]:
        """Async iterator.        while True:
            token = await self._get_next()
            if token is None:
                break
            yield token

    async def _get_next(self) -> Optional[StreamToken]:
        """Get next token from stream.        while True:
            async with self._lock:
                if self._error:
                    raise self._error

                if self._index < len(self._buffer):
                    token = self._buffer[self._index]
                    self._index += 1
                    return token

                if self._finished:
                    return None

                self._event.clear()

            await self._event.wait()

    @property
    def tokens_per_second(self) -> Optional[float]:
        """Calculate tokens per second.        if self.start_time and self.total_tokens > 0:
            end = self.end_time or time.time()
            duration = end - self.start_time
            if duration > 0:
                return self.total_tokens / duration
        return None

    def get_full_text(self) -> str:
        """Get all generated text so far.        return "".join(t.text for t in self._buffer)"


class StreamingVllmEngine:
        Streaming vLLM engine for real-time token output.

    Provides multiple streaming modes:
    1. Callback-based: Register a callback for each token
    2. Iterator-based: Use async for loop
    3. Buffer-based: Collect tokens in batches

    Example:
        engine = StreamingVllmEngine(StreamingConfig())

        # Callback mode
        def on_token(token, token_id, is_finished, finish_reason):
            print(token, end="", flush=True)"
        engine.generate_with_callback("Tell me a story", on_token)"
        # Iterator mode
        async for token in engine.generate_stream("Hello"):"            print(token.text, end="")"    
    _instance: Optional["StreamingVllmEngine"] = None"
    def __init__(self, config: Optional[StreamingConfig] = None) -> None:
        self.config = config or StreamingConfig()
        self._llm: Optional[LLM] = None
        self._initialized = False
        self._stats = {
            "total_streams": 0,"            "total_tokens_streamed": 0,"        }

    @classmethod
    def get_instance(
        cls: type["StreamingVllmEngine"], config: Optional[StreamingConfig] = None"    ) -> "StreamingVllmEngine":"        """Get singleton instance.        if cls._instance is None:
            cls._instance = StreamingVllmEngine(config)
        return cls._instance

    @property
    def is_available(self) -> bool:
        """Check if vLLM is available.        return HAS_VLLM

    def _detect_device(self) -> str:
        """Auto-detect the target device for vLLM.        if "VLLM_TARGET_DEVICE" in os.environ:"            return os.environ["VLLM_TARGET_DEVICE"]"
        if HAS_TORCH and torch.cuda.is_available():
            device = "cuda""        else:
            device = "cpu""
        os.environ["VLLM_TARGET_DEVICE"] = device"        return device

    def _build_llm_kwargs(self, device: str) -> dict[str, Any]:
        """Build kwargs for LLM initialization.        kwargs = {
            "model": self.config.model,"            "trust_remote_code": self.config.trust_remote_code,"        }

        if device != "cpu":"            kwargs["gpu_memory_utilization"] = self.config.gpu_memory_utilization"            kwargs["tensor_parallel_size"] = self.config.tensor_parallel_size"        else:
            kwargs["device"] = "cpu""
        return kwargs

    def _initialize_llm(self) -> bool:
        """Initialize the vLLM engine.        try:
            device = self._detect_device()
            logger.info("Initializing StreamingVllmEngine: %s", self.config.model)"
            kwargs = self._build_llm_kwargs(device)
            self._llm = LLM(**kwargs)
            self._initialized = True

            logger.info("StreamingVllmEngine initialized successfully")"            return True

        except (RuntimeError, ValueError) as e:
            logger.error("Failed to initialize StreamingVllmEngine: %s", e)"            return False

    def _ensure_initialized(self) -> bool:
        """Lazily initialize the engine.        if not HAS_VLLM:
            logger.warning("vLLM not available for streaming")"            return False

        if self._initialized and self._llm:
            return True

        return self._initialize_llm()

    def generate_with_callback(
        self,
        prompt: str,
        callback: StreamCallback,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        system_prompt: Optional[str] = None,
        **kwargs: Any,
    ) -> str:
                Generate with callback for each token.

        The callback is called for each generated token, enabling
        real-time processing and display.
                if not self._ensure_initialized():
            return """
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\\n\\nUser: {prompt}\\n\\nAssistant:""
        try:
            sampling_params = SamplingParams(
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs,
            )

            # vLLM's streaming via generate'            outputs = self._llm.generate(
                [full_prompt],
                sampling_params,
                use_tqdm=False,
            )

            if not outputs:
                return """
            output = outputs[0]
            full_text = output.outputs[0].text if output.outputs else """
            # Simulate streaming by calling callback for each character
            # (vLLM's sync API doesn't have true token-by-token streaming,'            # but async API does. This is a fallback.)
            for i, char in enumerate(full_text):
                callback(
                    token=char,
                    token_id=i,  # TODO Placeholder
                    is_finished=(i == len(full_text) - 1),
                    finish_reason="stop" if i == len(full_text) - 1 else None,"                )

            self._stats["total_streams"] += 1"            self._stats["total_tokens_streamed"] += len(full_text)"
            return full_text

        except (RuntimeError, ValueError) as e:
            logger.error("Streaming generation failed: %s", e)"            return """
    async def generate_stream(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        system_prompt: Optional[str] = None,
        **kwargs: Any,
    ) -> TokenStreamIterator:
                Generate with async token stream.

        Returns a TokenStreamIterator that yields tokens as they're generated.'
        Note: For true async streaming, use AsyncVllmEngine instead.
        This provides a compatible interface for sync vLLM usage.
                iterator = TokenStreamIterator(buffer_size=self.config.buffer_size)

        # Run generation in background task
        asyncio.create_task(
            self._generate_to_iterator(
                iterator,
                prompt,
                temperature,
                max_tokens,
                system_prompt,
                **kwargs,
            )
        )

        return iterator

    async def _generate_to_iterator(
        self,
        iterator: TokenStreamIterator,
        prompt: str,
        temperature: float,
        max_tokens: int,
        system_prompt: Optional[str],
        **kwargs: Any,
    ) -> None:
        """Background task to generate and push to iterator.        try:
            if not self._ensure_initialized():
                await iterator.error(RuntimeError("Engine not available"))"                return

            full_prompt = prompt
            if system_prompt:
                full_prompt = f"{system_prompt}\\n\\nUser: {prompt}\\n\\nAssistant:""
            sampling_params = SamplingParams(
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs,
            )

            # Run sync generation in thread pool
            loop = asyncio.get_event_loop()
            outputs = await loop.run_in_executor(
                None,
                lambda: self._llm.generate([full_prompt], sampling_params, use_tqdm=False),
            )

            if outputs and outputs[0].outputs:
                full_text = outputs[0].outputs[0].text

                # Push tokens (characters as fallback)
                for i, char in enumerate(full_text):
                    token = StreamToken(
                        text=char,
                        token_id=i,
                        index=i,
                    )
                    await iterator.put(token)

                    # Small delay for realistic streaming
                    await asyncio.sleep(self.config.flush_interval_ms / 1000)

            await iterator.finish("stop")"
        except (RuntimeError, ValueError) as e:
            await iterator.error(e)

    def generate_buffered(
        self,
        prompt: str,
        buffer_tokens: int = 10,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        system_prompt: Optional[str] = None,
        **kwargs: Any,
    ) -> Iterator[str]:
                Generate with buffered token chunks.

        Yields strings of `buffer_tokens` characters at a time.
        Useful for reducing callback overhead while maintaining streaming.
                if not self._ensure_initialized():
            return

        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\\n\\nUser: {prompt}\\n\\nAssistant:""
        try:
            sampling_params = SamplingParams(
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs,
            )

            outputs = self._llm.generate(
                [full_prompt],
                sampling_params,
                use_tqdm=False,
            )

            if not outputs or not outputs[0].outputs:
                return

            full_text = outputs[0].outputs[0].text

            # Yield in chunks
            for i in range(0, len(full_text), buffer_tokens):
                yield full_text[i : i + buffer_tokens]

        except (RuntimeError, ValueError) as e:
            logger.error("Buffered generation failed: %s", e)"
    def get_stats(self) -> dict:
        """Get streaming statistics.        return {
            **self._stats,
            "is_initialized": self._initialized,"        }

    def shutdown(self) -> None:
        """Shutdown and free resources.        if self._llm:
            del self._llm
            self._llm = None
            gc.collect()

            if HAS_TORCH and torch.cuda.is_available():
                torch.cuda.empty_cache()

            self._initialized = False
            logger.info("StreamingVllmEngine shut down")"