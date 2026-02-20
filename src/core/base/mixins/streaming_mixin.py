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

try:
    import asyncio
except ImportError:
    import asyncio

try:
    from typing import AsyncGenerator, Any, Callable, Optional
except ImportError:
    from typing import AsyncGenerator, Any, Callable, Optional




class StreamingMixin:
    """Provides asynchronous streaming capabilities to agents for real-time output processing.
    """
    async def stream_response(
        self,
        generator: AsyncGenerator[Any, None],
        callback: Optional[Callable[[Any], None]] = None
    ) -> AsyncGenerator[Any, None]:
        """Processes a stream from an LLM or process and optionally triggers a callback for each chunk.
        """
        async for chunk in generator:
            if callback:
                if asyncio.iscoroutinefunction(callback):
                    await callback(chunk)
                else:
                    callback(chunk)
            yield chunk

    def format_stream_chunk(self, chunk: Any) -> str:
        """Normalize various stream chunk formats into a string."""
        if isinstance(chunk, str):
            return chunk
        if hasattr(chunk, "content"):
            return str(chunk.content)
        return str(chunk)
