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

"""
Phase 164: Zero-Latency Agent Communication Bus.
Uses ZeroMQ for high-performance inter-process messaging.
"""

from __future__ import annotations

import asyncio
import inspect
import logging
from typing import Any, Callable

import orjson
import zmq
import zmq.asyncio


class AgentCommunicationBus:
    """Zero-latency messaging bus for swarm orchestration."""

    def __init__(self, pub_port: int = 5555, sub_port: int = 5556) -> None:
        self.context = zmq.asyncio.Context()
        self.pub_port = pub_port
        self.sub_port = sub_port

        # PUB socket for broadcasting
        self.publisher = self.context.socket(zmq.PUB)
        self.publisher.setsockopt(zmq.LINGER, 0)
        self.publisher.bind(f"tcp://*:{self.pub_port}")

        # SUB socket for receiving
        self.subscriber = self.context.socket(zmq.SUB)
        self.subscriber.setsockopt(zmq.LINGER, 0)
        self.subscriber.connect(f"tcp://localhost:{self.pub_port}")

        self.handlers: dict[str, list[Callable]] = {}
        self._running = False

    async def broadcast(self, topic: str, message: dict[str, Any]) -> None:
        """Broadcasts a message to all agents subscribed to a topic."""
        payload = orjson.dumps({"topic": topic, "data": message})
        await self.publisher.send_multipart([topic.encode(), payload])

    def subscribe(self, topic: str, handler: Callable[[dict[str, Any]], None]) -> None:
        """Subscribes a handler to a specific topic."""
        if topic not in self.handlers:
            self.handlers[topic] = []
            self.subscriber.setsockopt_string(zmq.SUBSCRIBE, topic)
        self.handlers[topic].append(handler)

    async def start(self) -> None:
        """Starts the listening loop."""
        self._running = True
        try:
            while self._running:
                try:
                    result = await self.subscriber.recv_multipart()
                    if not result:
                        break

                    topic_bytes, payload_bytes = result
                    topic = topic_bytes.decode()
                    data = orjson.loads(payload_bytes)["data"]

                    if topic in self.handlers:
                        for handler in self.handlers[topic]:
                            if inspect.iscoroutinefunction(handler):
                                await handler(data)

                            else:
                                handler(data)
                except (zmq.ContextTerminated, zmq.ZMQError, asyncio.CancelledError):
                    self._running = False
                    break
                except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                    if self._running:
                        logging.error(f"AgentBus Error: {e}")
                        await asyncio.sleep(0.1)
        finally:
            self.stop()

    def stop(self) -> None:
        """Stops the bus and cleans up sockets."""

        self._running = False
        if hasattr(self, "publisher") and not self.publisher.closed:
            self.publisher.close(linger=0)
        if hasattr(self, "subscriber") and not self.subscriber.closed:
            self.subscriber.close(linger=0)
        if hasattr(self, "context"):
            self.context.term()


if __name__ == "__main__":
    import signal
    import sys

    # ZeroMQ on Windows requires SelectorEventLoop
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    async def run_example() -> None:
        bus = AgentCommunicationBus()

        def on_msg(data: dict[str, Any]) -> None:
            print(f"Received: {data}")

        bus.subscribe("telemetry", on_msg)

        # Setup graceful shutdown via signals (non-Windows)
        loop = asyncio.get_running_loop()
        stop_event = asyncio.Event()

        def handle_stop() -> None:
            print("\nShutting down AgentBus...")
            bus.stop()
            stop_event.set()

        try:
            for sig in (signal.SIGINT, signal.SIGTERM):
                loop.add_signal_handler(sig, handle_stop)
        except NotImplementedError:
            pass

        print("AgentBus running. Press Ctrl+C to stop.")

        try:
            listener = asyncio.create_task(bus.start())
            await bus.broadcast("telemetry", {"status": "online"})
            await asyncio.wait([listener, stop_event.wait()], return_when=asyncio.FIRST_COMPLETED)
        except (KeyboardInterrupt, asyncio.CancelledError):
            handle_stop()
        finally:
            bus.stop()
            print("AgentBus stopped.")

    try:
        asyncio.run(run_example())
    except KeyboardInterrupt:
        pass
