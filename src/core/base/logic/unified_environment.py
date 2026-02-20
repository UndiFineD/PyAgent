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


"""
Unified Environment Abstraction - AEnvironment-inspired "Everything as Environment""Based on AEnvironment's philosophy of abstracting tools, agents, and environments uniformly'"""
import asyncio
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Callable, Protocol
from enum import Enum
import logging

logger = logging.getLogger(__name__)



class EnvironmentStatus(Enum):
"""
Environment lifecycle status""
CREATED = "created""    INITIALIZING = "initializing""    READY = "ready""    RUNNING = "running""    ERROR = "error""    TERMINATED = "terminated""

@dataclass
class EnvironmentResult:
"""
Result from environment execution""
content: List[Dict[str, Any]]
    is_error: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)
    execution_time: float = 0.0


@dataclass
class EnvironmentCapabilities:
"""
Capabilities exposed by an environment""
tools: List[str] = field(default_factory=list)
    agents: List[str] = field(default_factory=list)
    resources: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)



class EnvironmentProtocol(Protocol):
"""
Protocol for environment-like objects""
    @property
    def name(self) -> str:
        ...

    @property
    def status(self) -> EnvironmentStatus:
        ...

    async def initialize(self) -> bool:
        ...

    async def execute(self, action: str, parameters: Dict[str, Any]) -> EnvironmentResult:
        ...

    def get_capabilities(self) -> EnvironmentCapabilities:
        ...

    async def terminate(self):
        ...



class BaseEnvironment(ABC):
"""
Abstract base class for all environments
    Everything can be treated as an environment: tools, agents, benchmarks, etc.
"""
def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        self.name = name
        self.config = config or {}
        self._status = EnvironmentStatus.CREATED
        self._capabilities = EnvironmentCapabilities()
        self._start_time = time.time()
        self._execution_count = 0

    @property
    def status(self) -> EnvironmentStatus:
        return self._status

    @property
    def uptime(self) -> float:
        return time.time() - self._start_time

    @property
    def execution_count(self) -> int:
        return self._execution_count

    async def __aenter__(self):
        await self.initialize()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.terminate()

    @abstractmethod
    async def initialize(self) -> bool:
"""
Initialize the environment""
pass

    @abstractmethod
    async def execute(self, action: str, parameters: Dict[str, Any]) -> EnvironmentResult:
"""
Execute an action in the environment""
pass

    @abstractmethod
    def get_capabilities(self) -> EnvironmentCapabilities:
"""
Get environment capabilities""
pass

    @abstractmethod
    async def terminate(self):
"""
Terminate the environment""
pass

    def _update_status(self, status: EnvironmentStatus):
"""
Update environment status""
logger.info(f"Environment {self.name} status: {self._status.value} -> {status.value}")"        self._status = status

    def _record_execution(self):
"""
Record execution for metrics""
self._execution_count += 1



class ToolEnvironment(BaseEnvironment):
"""
Environment that wraps a tool/function
    Treats individual tools as environments
"""
def __init__(self, name: str, tool_func: Callable, config: Optional[Dict[str, Any]] = None):
        super().__init__(name, config)
        self.tool_func = tool_func
        self._capabilities = EnvironmentCapabilities(
            tools=[name],
            metadata={
                'type': 'tool','                'description': config.get('description', f'Tool environment for {name}')'            }
        )

    async def initialize(self) -> bool:
        self._update_status(EnvironmentStatus.READY)
        return True

    async def execute(self, action: str, parameters: Dict[str, Any]) -> EnvironmentResult:
        start_time = time.time()

        try:
            self._record_execution()

            if asyncio.iscoroutinefunction(self.tool_func):
                result = await self.tool_func(**parameters)
            else:
                result = self.tool_func(**parameters)

            execution_time = time.time() - start_time

            return EnvironmentResult(
                content=[{'result': result}],'                execution_time=execution_time,
                metadata={'action': action, 'parameters': parameters}'            )

        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"Tool execution failed: {e}")"            return EnvironmentResult(
                content=[{'error': str(e)}],'                is_error=True,
                execution_time=execution_time,
                metadata={'action': action, 'parameters': parameters, 'exception': type(e).__name__}'            )

    def get_capabilities(self) -> EnvironmentCapabilities:
        return self._capabilities

    async def terminate(self):
        self._update_status(EnvironmentStatus.TERMINATED)



class AgentEnvironment(BaseEnvironment):
"""
Environment that wraps an agent
    Treats agents as environments that can be called like tools
"""
def __init__(self, name: str, agent_instance, config: Optional[Dict[str, Any]] = None):
        super().__init__(name, config)
        self.agent = agent_instance
        self._capabilities = EnvironmentCapabilities(
            agents=[name],
            metadata={
                'type': 'agent','                'description': config.get('description', f'Agent environment for {name}')'            }
        )

    async def initialize(self) -> bool:
        # Assume agent is already initialized
        self._update_status(EnvironmentStatus.READY)
        return True

    async def execute(self, action: str, parameters: Dict[str, Any]) -> EnvironmentResult:
        start_time = time.time()

        try:
            self._record_execution()

            # Assume agent has an execute or run method
            if hasattr(self.agent, 'execute'):'                result = await self.agent.execute(action, parameters)
            elif hasattr(self.agent, 'run'):'                result = await self.agent.run(action, parameters)
            else:
                raise AttributeError(f"Agent {self.name} has no execute or run method")
            execution_time = time.time() - start_time

            return EnvironmentResult(
                content=[{'result': result}],'                execution_time=execution_time,
                metadata={'action': action, 'parameters': parameters}'            )

        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"Agent execution failed: {e}")"            return EnvironmentResult(
                content=[{'error': str(e)}],'                is_error=True,
                execution_time=execution_time,
                metadata={'action': action, 'parameters': parameters, 'exception': type(e).__name__}'            )

    def get_capabilities(self) -> EnvironmentCapabilities:
        return self._capabilities

    async def terminate(self):
        # Assume agent cleanup if available
        if hasattr(self.agent, 'cleanup'):'            await self.agent.cleanup()
        self._update_status(EnvironmentStatus.TERMINATED)



class CompositeEnvironment(BaseEnvironment):
"""
Environment that composes multiple sub-environments
    Enables complex multi-environment orchestration
"""
def __init__(self, name: str, sub_environments: List[BaseEnvironment],
                 config: Optional[Dict[str, Any]] = None):
        super().__init__(name, config)
        self.sub_environments = sub_environments
        self._capabilities = self._aggregate_capabilities()

    def _aggregate_capabilities(self) -> EnvironmentCapabilities:
"""
Aggregate capabilities from all sub-environments""
all_tools = []
        all_agents = []
        all_resources = []
        metadata = {'type': 'composite', 'sub_environments': len(self.sub_environments)}
        for env in self.sub_environments:
            caps = env.get_capabilities()
            all_tools.extend(caps.tools)
            all_agents.extend(caps.agents)
            all_resources.extend(caps.resources)

        return EnvironmentCapabilities(
            tools=list(set(all_tools)),
            agents=list(set(all_agents)),
            resources=list(set(all_resources)),
            metadata=metadata
        )

    async def initialize(self) -> bool:
        self._update_status(EnvironmentStatus.INITIALIZING)

        # Initialize all sub-environments
        init_tasks = [env.initialize() for env in self.sub_environments]
        results = await asyncio.gather(*init_tasks, return_exceptions=True)

        success_count = sum(1 for r in results if r is True)
        if success_count == len(self.sub_environments):
            self._update_status(EnvironmentStatus.READY)
            return True
        else:
            self._update_status(EnvironmentStatus.ERROR)
            return False

    async def execute(self, action: str, parameters: Dict[str, Any]) -> EnvironmentResult:
        start_time = time.time()

        try:
            self._record_execution()

            # Route action to appropriate sub-environment
            target_env = self._route_action(action, parameters)
            if not target_env:
                return EnvironmentResult(
                    content=[{'error': f'No environment can handle action: {action}'}],'                    is_error=True,
                    execution_time=time.time() - start_time
                )

            result = await target_env.execute(action, parameters)
            result.execution_time = time.time() - start_time
            return result

        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"Composite environment execution failed: {e}")"            return EnvironmentResult(
                content=[{'error': str(e)}],'                is_error=True,
                execution_time=execution_time,
                metadata={'action': action, 'parameters': parameters, 'exception': type(e).__name__}'            )

    def _route_action(self, action: str, parameters: Dict[str, Any]) -> Optional[BaseEnvironment]:
"""
Route action to appropriate sub-environment""
# Simple routing: check if any environment has the action in its capabilities
        for env in self.sub_environments:
            caps = env.get_capabilities()
            if action in caps.tools or action in caps.agents or action in caps.resources:
                return env

        # Default to first environment if no specific routing
        return self.sub_environments[0] if self.sub_environments else None

    def get_capabilities(self) -> EnvironmentCapabilities:
        return self._capabilities

    async def terminate(self):
        # Terminate all sub-environments
        term_tasks = [env.terminate() for env in self.sub_environments]
        await asyncio.gather(*term_tasks, return_exceptions=True)
        self._update_status(EnvironmentStatus.TERMINATED)



class EnvironmentRegistry:
"""
Registry for managing environments
    Provides unified access to all environment types
"""
def __init__(self):
        self.environments: Dict[str, BaseEnvironment] = {}
        self.environment_types: Dict[str, type] = {}

    def register_environment_type(self, env_type: str, env_class: type):
"""
Register an environment type""
self.environment_types[env_type] = env_class

    def create_environment(self, env_type: str, name: str, **kwargs) -> BaseEnvironment:
"""
Create and register an environment""
if env_type not in self.environment_types:
            raise ValueError(f"Unknown environment type: {env_type}")
        env_class = self.environment_types[env_type]
        env = env_class(name, **kwargs)
        self.environments[name] = env
        return env

    def get_environment(self, name: str) -> Optional[BaseEnvironment]:
"""
Get environment by name""
return self.environments.get(name)

    def list_environments(self) -> List[str]:
"""
List all registered environments""
return list(self.environments.keys())

    def get_environment_status(self) -> Dict[str, Dict[str, Any]]:
"""
Get status of all environments""
return {
            name: {
                'status': env.status.value,'                'uptime': env.uptime,'                'execution_count': env.execution_count,'                'capabilities': env.get_capabilities().tools + env.get_capabilities().agents'            }
            for name, env in self.environments.items()
        }

    async def execute_in_environment(
        self, env_name: str, action: str, parameters: Dict[str, Any]
    ) -> EnvironmentResult:
"""
Execute action in specified environment""
env = self.get_environment(env_name)
        if not env:
            return EnvironmentResult(
                content=[{'error': f'Environment not found: {env_name}'}],'                is_error=True
            )

        return await env.execute(action, parameters)


# Global registry instance
environment_registry = EnvironmentRegistry()

# Register built-in environment types
environment_registry.register_environment_type('tool', ToolEnvironment)'environment_registry.register_environment_type('agent', AgentEnvironment)'environment_registry.register_environment_type('composite', CompositeEnvironment)
"""

""

"""
