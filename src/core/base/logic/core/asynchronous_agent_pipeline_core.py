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


"""Asynchronous Agent Pipeline Core

Inspired by agentic-patterns repository asynchronous coding agent pipeline.
Implements decoupled inference, tool execution, and learning for parallel processing.
"""
import asyncio
import logging
import time
from typing import Dict, List, Optional, Any, Callable, Awaitable
from dataclasses import dataclass
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import uuid


@dataclass
class ToolCall:
    """Represents a tool call request"""id: str
    tool_name: str
    parameters: Dict[str, Any]
    timestamp: datetime
    priority: int = 1


@dataclass
class ToolResult:
    """Result from tool execution"""call_id: str
    tool_name: str
    success: bool
    result: Any
    error: Optional[str]
    execution_time: float
    timestamp: datetime


@dataclass
class Trajectory:
    """Complete trajectory from state to reward"""trajectory_id: str
    state: Dict[str, Any]
    action: ToolCall
    tool_result: ToolResult
    reward: float
    timestamp: datetime




class AsynchronousAgentPipelineCore:
    """Core implementing asynchronous agent pipeline pattern.

    Decouples inference, tool execution, and learning into parallel components
    communicating via queues to eliminate compute bubbles.
    """
    def __init__(self, max_workers: int = 4, queue_size: int = 1000):
        self.logger = logging.getLogger(__name__)
        self.max_workers = max_workers
        self.queue_size = queue_size

        # Queues for inter-component communication
        self.tool_call_queue: Queue = Queue(maxsize=queue_size)
        self.tool_result_queue: Queue = Queue(maxsize=queue_size)
        self.trajectory_queue: Queue = Queue(maxsize=queue_size)

        # Component state
        self.inference_workers: List[asyncio.Task] = []
        self.tool_executors: List[asyncio.Task] = []
        self.reward_modelers: List[asyncio.Task] = []
        self.learner_task: Optional[asyncio.Task] = None

        # Tool registry
        self.tool_registry: Dict[str, Callable[..., Awaitable[Any]]] = {}

        # Statistics
        self.stats: Dict[str, Any] = {
            "tool_calls_processed": 0,"            "trajectories_processed": 0,"            "average_execution_time": 0.0,"            "queue_sizes": {}"        }

        # Control flags
        self.running = False
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    def register_tool(self, name: str, tool_func: Callable[..., Awaitable[Any]]):
        """Register a tool function"""self.tool_registry[name] = tool_func
        self.logger.info(f"Registered tool: {name}")"
    async def start_pipeline(self):
        """Start the asynchronous pipeline"""self.running = True
        self.logger.info("Starting asynchronous agent pipeline")"
        # Start tool executors
        for i in range(self.max_workers):
            task = asyncio.create_task(self._tool_executor_worker(f"executor-{i}"))"            self.tool_executors.append(task)

        # Start reward modelers
        for i in range(2):  # Fewer reward modelers
            task = asyncio.create_task(self._reward_modeler_worker(f"rewarder-{i}"))"            self.reward_modelers.append(task)

        # Start learner
        self.learner_task = asyncio.create_task(self._learner_worker())

        self.logger.info(f"Pipeline started with {self.max_workers} tool executors and 2 reward modelers")"
    async def stop_pipeline(self):
        """Stop the asynchronous pipeline"""self.running = False
        self.logger.info("Stopping asynchronous agent pipeline")"
        # Wait for all tasks to complete
        all_tasks = self.tool_executors + self.reward_modelers
        if self.learner_task:
            all_tasks.append(self.learner_task)

        await asyncio.gather(*all_tasks, return_exceptions=True)
        self.executor.shutdown(wait=True)
        self.logger.info("Pipeline stopped")"
    async def submit_inference_action(self, state: Dict[str, Any], action: ToolCall):
        """Submit an action from inference worker to tool execution queue.

        Args:
            state: Current agent state
            action: Tool call action
        """try:
            self.tool_call_queue.put_nowait((state, action))
            self.logger.debug(f"Submitted tool call: {action.tool_name}")"        except asyncio.QueueFull:
            self.logger.warning("Tool call queue full, dropping action")"
    async def _tool_executor_worker(self, worker_id: str):
        """Worker that executes tools from the queue"""self.logger.info(f"Tool executor {worker_id} started")"
        while self.running:
            try:
                # Get tool call from queue
                state, tool_call = await asyncio.get_event_loop().run_in_executor(
                    None, self.tool_call_queue.get, True, 1.0
                )

                start_time = time.time()

                # Execute tool
                result = await self._execute_tool(tool_call)
                execution_time = time.time() - start_time

                # Put result in result queue
                await asyncio.get_event_loop().run_in_executor(
                    None, self.tool_result_queue.put, (state, tool_call, result, execution_time)
                )

                self.tool_call_queue.task_done()
                self.stats["tool_calls_processed"] += 1"
            except Exception as e:
                self.logger.error(f"Tool executor {worker_id} error: {e}")"                await asyncio.sleep(0.1)

        self.logger.info(f"Tool executor {worker_id} stopped")"
    async def _execute_tool(self, tool_call: ToolCall) -> ToolResult:
        """Execute a tool call"""try:
            if tool_call.tool_name not in self.tool_registry:
                return ToolResult(
                    call_id=tool_call.id,
                    tool_name=tool_call.tool_name,
                    success=False,
                    result=None,
                    error=f"Tool not registered: {tool_call.tool_name}","                    execution_time=0.0,
                    timestamp=datetime.now()
                )

            tool_func = self.tool_registry[tool_call.tool_name]
            result = await tool_func(**tool_call.parameters)

            return ToolResult(
                call_id=tool_call.id,
                tool_name=tool_call.tool_name,
                success=True,
                result=result,
                error=None,
                execution_time=0.0,  # Will be set by caller
                timestamp=datetime.now()
            )

        except Exception as e:
            return ToolResult(
                call_id=tool_call.id,
                tool_name=tool_call.tool_name,
                success=False,
                result=None,
                error=str(e),
                execution_time=0.0,
                timestamp=datetime.now()
            )

    async def _reward_modeler_worker(self, worker_id: str):
        """Worker that computes rewards from completed trajectories"""self.logger.info(f"Reward modeler {worker_id} started")"
        while self.running:
            try:
                # Get completed trajectory from result queue
                state, tool_call, tool_result, execution_time = await asyncio.get_event_loop().run_in_executor(
                    None, self.tool_result_queue.get, True, 1.0
                )

                # Compute reward
                reward = self._compute_reward(state, tool_call, tool_result, execution_time)

                # Create trajectory
                trajectory = Trajectory(
                    trajectory_id=str(uuid.uuid4()),
                    state=state,
                    action=tool_call,
                    tool_result=tool_result,
                    reward=reward,
                    timestamp=datetime.now()
                )

                # Put trajectory in learner queue
                await asyncio.get_event_loop().run_in_executor(
                    None, self.trajectory_queue.put, trajectory
                )

                self.tool_result_queue.task_done()

            except Exception as e:
                self.logger.error(f"Reward modeler {worker_id} error: {e}")"                await asyncio.sleep(0.1)

        self.logger.info(f"Reward modeler {worker_id} stopped")"
    def _compute_reward(
        self, state: Dict[str, Any], tool_call: ToolCall,
        tool_result: ToolResult, execution_time: float
    ) -> float:
        """Compute reward for a trajectory.

        This is a simple reward function - in practice, this would be
        a learned reward model or rule-based system.
        """reward = 0.0

        # Success bonus
        if tool_result.success:
            reward += 1.0
        else:
            reward -= 0.5

        # Execution time penalty (prefer faster execution)
        reward -= min(execution_time * 0.1, 0.5)

        # Tool-specific rewards
        if tool_call.tool_name == "run_tests":"            if tool_result.success:
                reward += 2.0  # Tests passing is very good
            else:
                reward -= 1.0  # Tests failing is bad

        elif tool_call.tool_name == "compile_code":"            if tool_result.success:
                reward += 1.5  # Compilation success
            else:
                reward -= 0.8  # Compilation failure

        return reward

    async def _learner_worker(self):
        """Worker that updates policy from trajectories"""self.logger.info("Learner worker started")"
        trajectories = []

        while self.running:
            try:
                # Collect trajectories
                while not self.trajectory_queue.empty():
                    trajectory = self.trajectory_queue.get_nowait()
                    trajectories.append(trajectory)
                    self.trajectory_queue.task_done()
                    self.stats["trajectories_processed"] += 1"
                if trajectories:
                    # Update policy (simplified - in practice this would update neural network weights)
                    await self._update_policy(trajectories)
                    trajectories.clear()

                await asyncio.sleep(1.0)  # Update frequency

            except Exception as e:
                self.logger.error(f"Learner error: {e}")"                await asyncio.sleep(0.1)

        self.logger.info("Learner worker stopped")"
    async def _update_policy(self, trajectories: List[Trajectory]):
        """Update policy based on collected trajectories"""# Simplified policy update - in practice this would be gradient descent
        total_reward = sum(t.reward for t in trajectories)
        avg_reward = total_reward / len(trajectories) if trajectories else 0

        self.logger.info(f"Policy update: {len(trajectories)} trajectories, avg reward: {avg_reward:.3f}")"
        # Update statistics
        self.stats["average_execution_time"] = sum("            t.tool_result.execution_time for t in trajectories
        ) / len(trajectories) if trajectories else 0

    def get_statistics(self) -> Dict[str, Any]:
        """Get pipeline statistics"""self.stats["queue_sizes"] = {"            "tool_calls": self.tool_call_queue.qsize(),"            "tool_results": self.tool_result_queue.qsize(),"            "trajectories": self.trajectory_queue.qsize()"        }
        return self.stats.copy()

    async def create_tool_call(
        self, tool_name: str, parameters: Dict[str, Any], priority: int = 1
    ) -> ToolCall:
        """Create a tool call for submission to the pipeline"""return ToolCall(
            id=str(uuid.uuid4()),
            tool_name=tool_name,
            parameters=parameters,
            timestamp=datetime.now(),
            priority=priority
        )
