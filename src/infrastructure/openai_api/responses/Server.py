# SPDX-License-Identifier: Apache-2.0
import asyncio
import logging
import uuid
from typing import AsyncIterator, Callable, Dict, List, Optional, Union
from .Enums import ResponseStatus
from .Models import Response, ResponseConfig, ResponseUsage
from .Store import ResponseStore, InMemoryResponseStore
from .Streaming import SSEStream, StreamingHandler

logger = logging.getLogger(__name__)

class ResponsesAPIServer:
    """
    OpenAI Responses API server implementation.
    """
    def __init__(
        self,
        model_handler: Callable[[ResponseConfig], AsyncIterator[str]],
        store: Optional[ResponseStore] = None,
        enable_store: bool = True,
    ):
        self.model_handler = model_handler
        self.store = store or InMemoryResponseStore()
        self.enable_store = enable_store
        self._background_tasks: Dict[str, asyncio.Task] = {}

    def _create_response_id(self) -> str:
        return f"resp_{uuid.uuid4().hex[:24]}"

    async def create_response(self, config: ResponseConfig) -> Union[Response, SSEStream]:
        response = Response(id=self._create_response_id(), model=config.model, status=ResponseStatus.IN_PROGRESS, metadata=config.metadata)
        if config.stream: return await self._create_streaming_response(response, config)
        return await self._create_sync_response(response, config)

    async def _create_sync_response(self, response: Response, config: ResponseConfig) -> Response:
        try:
            text_parts = []
            prompt_tokens = 0
            completion_tokens = 0
            async for chunk in self.model_handler(config):
                text_parts.append(chunk)
                completion_tokens += len(chunk.split())
            full_text = "".join(text_parts)
            response.add_text_output(full_text)
            if config.messages:
                for msg in config.messages:
                    if isinstance(msg.content, str): prompt_tokens += len(msg.content.split())
            response.complete(ResponseUsage(prompt_tokens=prompt_tokens, completion_tokens=completion_tokens, total_tokens=prompt_tokens + completion_tokens))
            if config.store and self.enable_store: await self.store.save(response)
        except Exception as e:
            logger.exception(f"Error creating response: {e}")
            response.fail(str(e))
        return response

    async def _create_streaming_response(self, response: Response, config: ResponseConfig) -> SSEStream:
        stream = SSEStream(response.id)
        handler = StreamingHandler(response, stream)
        async def generate():
            try:
                await handler.start()
                prompt_tokens = 0
                completion_tokens = 0
                if config.messages:
                    for msg in config.messages:
                        if isinstance(msg.content, str): prompt_tokens += len(msg.content.split())
                async for chunk in self.model_handler(config):
                    await handler.add_content_delta(chunk)
                    completion_tokens += len(chunk.split())
                await handler.complete(ResponseUsage(prompt_tokens=prompt_tokens, completion_tokens=completion_tokens, total_tokens=prompt_tokens + completion_tokens))
                if config.store and self.enable_store: await self.store.save(response)
            except Exception as e:
                logger.exception(f"Streaming error: {e}")
                await handler.fail(str(e))
        task = asyncio.create_task(generate())
        self._background_tasks[response.id] = task
        return stream

    async def get_response(self, response_id: str) -> Optional[Response]:
        return await self.store.get(response_id)

    async def delete_response(self, response_id: str) -> bool:
        if response_id in self._background_tasks:
            task = self._background_tasks.pop(response_id)
            task.cancel()
        return await self.store.delete(response_id)

    async def list_responses(self, limit: int = 20, after: Optional[str] = None, before: Optional[str] = None) -> List[Response]:
        return await self.store.list(limit=limit, after=after, before=before)

    async def cancel_response(self, response_id: str) -> Optional[Response]:
        if response_id in self._background_tasks:
            task = self._background_tasks.pop(response_id)
            task.cancel()
        response = await self.store.get(response_id)
        if response and response.status == ResponseStatus.IN_PROGRESS:
            response.status = ResponseStatus.CANCELLED
            await self.store.save(response)
        return response
