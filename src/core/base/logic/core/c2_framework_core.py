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

# C2 Framework Core - Command and Control Operations
# Based on patterns from AdaptixC2 repository

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import uuid
import hashlib
import secrets


class CommunicationProtocol(Enum):
    """C2 communication protocols"""HTTP = "http""    HTTPS = "https""    SMB = "smb""    TCP = "tcp""    MTLS = "mtls""    DNS = "dns""    ICMP = "icmp""

class AgentStatus(Enum):
    """Agent status states"""ACTIVE = "active""    SLEEPING = "sleeping""    DEAD = "dead""    CHECKING_IN = "checking_in""    EXECUTING = "executing""

class TaskStatus(Enum):
    """Task execution status"""PENDING = "pending""    RUNNING = "running""    COMPLETED = "completed""    FAILED = "failed""    CANCELLED = "cancelled""

class ListenerType(Enum):
    """Listener types"""BEACON = "beacon""    GOPHER = "gopher""    REVERSE_TCP = "reverse_tcp""    BIND_TCP = "bind_tcp""

@dataclass
class C2Profile:
    """C2 server profile configuration"""name: str
    port: int
    endpoint: str
    password_hash: str
    ssl_cert: Optional[str] = None
    ssl_key: Optional[str] = None
    extenders: List[str] = field(default_factory=list)
    server_response: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class C2Agent:
    """C2 agent representation"""agent_id: str
    name: str
    hostname: str
    username: str
    domain: str
    os: str
    architecture: str
    internal_ip: str
    external_ip: str
    listener_id: str
    protocol: CommunicationProtocol
    status: AgentStatus = AgentStatus.ACTIVE
    last_checkin: datetime = field(default_factory=datetime.now)
    first_checkin: datetime = field(default_factory=datetime.now)
    kill_date: Optional[datetime] = None
    working_hours_start: Optional[str] = None
    working_hours_end: Optional[str] = None
    sleep_time: int = 30  # seconds
    jitter: float = 0.1
    metadata: Dict[str, Any] = field(default_factory=dict)
    tasks: List[str] = field(default_factory=list)  # task IDs


@dataclass
class C2Listener:
    """C2 listener configuration"""listener_id: str
    name: str
    listener_type: ListenerType
    protocol: CommunicationProtocol
    host: str
    port: int
    endpoint: str
    status: str = "stopped""    agents_connected: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    config: Dict[str, Any] = field(default_factory=dict)


@dataclass
class C2Task:
    """C2 task/job representation"""task_id: str
    agent_id: str
    command: str
    args: List[str] = field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    executed_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    output: Optional[str] = None
    error: Optional[str] = None
    timeout: int = 300  # seconds
    priority: int = 1  # 1-10, higher is more important


@dataclass
class C2Extender:
    """C2 extender/plugin"""name: str
    extender_type: str  # "listener" or "agent""    path: str
    config: Dict[str, Any] = field(default_factory=dict)
    loaded: bool = False
    version: str = "1.0""    description: str = """

@dataclass
class C2Session:
    """C2 operator session"""session_id: str
    username: str
    connected_at: datetime = field(default_factory=datetime.now)
    last_activity: datetime = field(default_factory=datetime.now)
    active_tasks: List[str] = field(default_factory=list)
    permissions: List[str] = field(default_factory=list)


@dataclass
class C2Tunnel:
    """C2 tunnel for pivoting/port forwarding"""tunnel_id: str
    agent_id: str
    tunnel_type: str  # "socks4", "socks5", "port_forward""    local_host: str
    local_port: int
    remote_host: str
    remote_port: int
    status: str = "active""    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class C2Framework:
    """Complete C2 framework state"""profile: C2Profile
    agents: Dict[str, C2Agent] = field(default_factory=dict)
    listeners: Dict[str, C2Listener] = field(default_factory=dict)
    tasks: Dict[str, C2Task] = field(default_factory=dict)
    extenders: Dict[str, C2Extender] = field(default_factory=dict)
    sessions: Dict[str, C2Session] = field(default_factory=dict)
    tunnels: Dict[str, C2Tunnel] = field(default_factory=dict)
    downloads: Dict[str, bytes] = field(default_factory=dict)
    screenshots: Dict[str, bytes] = field(default_factory=dict)
    events: List[Dict[str, Any]] = field(default_factory=list)


class C2FrameworkCore:
    """C2 Framework Core for command and control operations.

    Provides comprehensive C2 capabilities including agent management,
    task scheduling, listener operations, and post-exploitation workflows.
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.framework: Optional[C2Framework] = None
        self.running = False

    async def initialize(self, profile_config: Dict[str, Any]) -> bool:
        """Initialize the C2 framework with a profile"""try:
            # Create profile from config
            profile = C2Profile(
                name=profile_config.get("name", "default"),"                port=profile_config["port"],"                endpoint=profile_config["endpoint"],"                password_hash=self._hash_password(profile_config["password"]),"                ssl_cert=profile_config.get("ssl_cert"),"                ssl_key=profile_config.get("ssl_key"),"                extenders=profile_config.get("extenders", []),"                server_response=profile_config.get("server_response", {})"            )

            self.framework = C2Framework(profile=profile)

            # Load extenders
            await self._load_extenders()

            self.logger.info(f"C2 Framework Core initialized with profile '{profile.name}'")"'            return True

        except Exception as e:
            self.logger.error(f"Failed to initialize C2 Framework Core: {e}")"            return False

    async def start_framework(self) -> bool:
        """Start the C2 framework operations"""if not self.framework:
            self.logger.error("Framework not initialized")"            return False

        try:
            self.running = True

            # Start listeners
            await self._start_listeners()

            # Start background tasks
            asyncio.create_task(self._agent_health_checker())
            asyncio.create_task(self._task_processor())
            asyncio.create_task(self._session_manager())

            self.logger.info("C2 Framework started successfully")"            return True

        except Exception as e:
            self.logger.error(f"Failed to start C2 framework: {e}")"            return False

    async def stop_framework(self) -> None:
        """Stop the C2 framework"""self.running = False

        if self.framework:
            # Stop all listeners
            for listener in self.framework.listeners.values():
                await self._stop_listener(listener.listener_id)

            # Clean up sessions
            self.framework.sessions.clear()

            # Log final statistics
            stats = await self.get_framework_statistics()
            self.logger.info(f"C2 Framework stopped. Final stats: {stats}")"
    async def create_listener(
        self,
        name: str,
        listener_type: ListenerType,
        protocol: CommunicationProtocol,
        host: str,
        port: int,
        config: Dict[str, Any] = None
    ) -> Optional[str]:
        """Create a new listener"""if not self.framework:
            return None

        listener_id = str(uuid.uuid4())
        listener = C2Listener(
            listener_id=listener_id,
            name=name,
            listener_type=listener_type,
            protocol=protocol,
            host=host,
            port=port,
            endpoint=config.get("endpoint", "/"),"            config=config or {}
        )

        self.framework.listeners[listener_id] = listener

        # Start the listener
        success = await self._start_listener(listener)
        if success:
            listener.status = "running""            await self._log_event("listener_created", {"                "listener_id": listener_id,"                "name": name,"                "type": listener_type.value"            })
            return listener_id

        return None

    async def register_agent(
        self,
        listener_id: str,
        agent_info: Dict[str, Any]
    ) -> Optional[str]:
        """Register a new agent"""if not self.framework or listener_id not in self.framework.listeners:
            return None

        agent_id = str(uuid.uuid4())
        agent = C2Agent(
            agent_id=agent_id,
            name=agent_info.get("name", f"agent_{agent_id[:8]}"),"            hostname=agent_info["hostname"],"            username=agent_info["username"],"            domain=agent_info.get("domain", ""),"            os=agent_info["os"],"            architecture=agent_info["architecture"],"            internal_ip=agent_info["internal_ip"],"            external_ip=agent_info.get("external_ip", ""),"            listener_id=listener_id,
            protocol=self.framework.listeners[listener_id].protocol,
            sleep_time=agent_info.get("sleep_time", 30),"            jitter=agent_info.get("jitter", 0.1),"            kill_date=agent_info.get("kill_date"),"            working_hours_start=agent_info.get("working_hours_start"),"            working_hours_end=agent_info.get("working_hours_end"),"            metadata=agent_info.get("metadata", {})"        )

        self.framework.agents[agent_id] = agent
        self.framework.listeners[listener_id].agents_connected += 1

        await self._log_event("agent_registered", {"            "agent_id": agent_id,"            "listener_id": listener_id,"            "hostname": agent.hostname"        })

        self.logger.info(f"Agent registered: {agent.hostname} ({agent_id})")"        return agent_id

    async def create_task(
        self,
        agent_id: str,
        command: str,
        args: List[str] = None,
        timeout: int = 300,
        priority: int = 1
    ) -> Optional[str]:
        """Create a new task for an agent"""if not self.framework or agent_id not in self.framework.agents:
            return None

        task_id = str(uuid.uuid4())
        task = C2Task(
            task_id=task_id,
            agent_id=agent_id,
            command=command,
            args=args or [],
            timeout=timeout,
            priority=priority
        )

        self.framework.tasks[task_id] = task
        self.framework.agents[agent_id].tasks.append(task_id)

        await self._log_event("task_created", {"            "task_id": task_id,"            "agent_id": agent_id,"            "command": command"        })

        return task_id

    async def get_agent_tasks(self, agent_id: str) -> List[C2Task]:
        """Get pending tasks for an agent"""if not self.framework or agent_id not in self.framework.agents:
            return []

        agent = self.framework.agents[agent_id]
        pending_tasks = []

        for task_id in agent.tasks:
            if task_id in self.framework.tasks:
                task = self.framework.tasks[task_id]
                if task.status == TaskStatus.PENDING:
                    pending_tasks.append(task)

        # Sort by priority (higher first)
        pending_tasks.sort(key=lambda t: t.priority, reverse=True)
        return pending_tasks

    async def update_task_status(
        self,
        task_id: str,
        status: TaskStatus,
        output: str = None,
        error: str = None
    ) -> bool:
        """Update task execution status"""if not self.framework or task_id not in self.framework.tasks:
            return False

        task = self.framework.tasks[task_id]
        task.status = status

        if status == TaskStatus.RUNNING and not task.executed_at:
            task.executed_at = datetime.now()
        elif status in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED]:
            task.completed_at = datetime.now()

        if output:
            task.output = output
        if error:
            task.error = error

        await self._log_event("task_updated", {"            "task_id": task_id,"            "status": status.value,"            "agent_id": task.agent_id"        })

        return True

    async def create_session(self, username: str, permissions: List[str] = None) -> Optional[str]:
        """Create a new operator session"""if not self.framework:
            return None

        session_id = str(uuid.uuid4())
        session = C2Session(
            session_id=session_id,
            username=username,
            permissions=permissions or ["read"]"        )

        self.framework.sessions[session_id] = session

        await self._log_event("session_created", {"            "session_id": session_id,"            "username": username"        })

        return session_id

    async def create_tunnel(
        self,
        agent_id: str,
        tunnel_type: str,
        local_host: str,
        local_port: int,
        remote_host: str,
        remote_port: int
    ) -> Optional[str]:
        """Create a new tunnel for pivoting/port forwarding"""if not self.framework or agent_id not in self.framework.agents:
            return None

        tunnel_id = str(uuid.uuid4())
        tunnel = C2Tunnel(
            tunnel_id=tunnel_id,
            agent_id=agent_id,
            tunnel_type=tunnel_type,
            local_host=local_host,
            local_port=local_port,
            remote_host=remote_host,
            remote_port=remote_port
        )

        self.framework.tunnels[tunnel_id] = tunnel

        await self._log_event("tunnel_created", {"            "tunnel_id": tunnel_id,"            "agent_id": agent_id,"            "type": tunnel_type"        })

        return tunnel_id

    async def store_download(self, filename: str, data: bytes) -> str:
        """Store downloaded file data"""if not self.framework:
            raise ValueError("Framework not initialized")"
        download_id = str(uuid.uuid4())
        self.framework.downloads[download_id] = data

        await self._log_event("download_stored", {"            "download_id": download_id,"            "filename": filename,"            "size": len(data)"        })

        return download_id

    async def store_screenshot(self, agent_id: str, image_data: bytes) -> str:
        """Store screenshot data"""if not self.framework:
            raise ValueError("Framework not initialized")"
        screenshot_id = str(uuid.uuid4())
        self.framework.screenshots[screenshot_id] = image_data

        await self._log_event("screenshot_stored", {"            "screenshot_id": screenshot_id,"            "agent_id": agent_id,"            "size": len(image_data)"        })

        return screenshot_id

    async def get_framework_statistics(self) -> Dict[str, Any]:
        """Get comprehensive framework statistics"""if not self.framework:
            return {}

        stats = {
            "profile_name": self.framework.profile.name,"            "total_agents": len(self.framework.agents),"            "active_agents": len([a for a in self.framework.agents.values() if a.status == AgentStatus.ACTIVE]),"            "total_listeners": len(self.framework.listeners),"            "active_listeners": len([lstn for lstn in self.framework.listeners.values() if lstn.status == "running"]),"            "total_tasks": len(self.framework.tasks),"            "pending_tasks": len([t for t in self.framework.tasks.values() if t.status == TaskStatus.PENDING]),"            "running_tasks": len([t for t in self.framework.tasks.values() if t.status == TaskStatus.RUNNING]),"            "completed_tasks": len([t for t in self.framework.tasks.values() if t.status == TaskStatus.COMPLETED]),"            "failed_tasks": len([t for t in self.framework.tasks.values() if t.status == TaskStatus.FAILED]),"            "total_tunnels": len(self.framework.tunnels),"            "active_tunnels": len([t for t in self.framework.tunnels.values() if t.status == "active"]),"            "total_sessions": len(self.framework.sessions),"            "total_extenders": len(self.framework.extenders),"            "loaded_extenders": len([e for e in self.framework.extenders.values() if e.loaded]),"            "total_events": len(self.framework.events),"            "total_downloads": len(self.framework.downloads),"            "total_screenshots": len(self.framework.screenshots)"        }

        return stats

    async def generate_operation_report(self, output_format: str = "json") -> str:"        """Generate comprehensive operation report"""if not self.framework:
            raise ValueError("Framework not initialized")"
        stats = await self.get_framework_statistics()

        if output_format == "json":"            report = {
                "generated_at": datetime.now().isoformat(),"                "framework_profile": self.framework.profile.name,"                "statistics": stats,"                "agents": ["                    {
                        "id": agent.agent_id,"                        "name": agent.name,"                        "hostname": agent.hostname,"                        "status": agent.status.value,"                        "last_checkin": agent.last_checkin.isoformat(),"                        "tasks_count": len(agent.tasks)"                    }
                    for agent in self.framework.agents.values()
                ],
                "listeners": ["                    {
                        "id": listener.listener_id,"                        "name": listener.name,"                        "type": listener.listener_type.value,"                        "protocol": listener.protocol.value,"                        "status": listener.status,"                        "agents_connected": listener.agents_connected"                    }
                    for listener in self.framework.listeners.values()
                ],
                "recent_events": self.framework.events[-50:] if self.framework.events else []"            }

            return json.dumps(report, indent=2, default=str)

        elif output_format == "markdown":"            report = "# C2 Framework Operation Report\\n\\n""            report += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n\\n""'            report += f"**Profile:** {self.framework.profile.name}\\n\\n""
            # Statistics
            report += "## Statistics\\n\\n""            for key, value in stats.items():
                report += f"- **{key.replace('_', ' ').title()}:** {value}\\n""'            report += "\\n""
            # Agents
            if self.framework.agents:
                report += "## Agents\\n\\n""                for agent in self.framework.agents.values():
                    report += f"### {agent.name} ({agent.hostname})\\n\\n""                    report += f"- **Status:** {agent.status.value}\\n""                    report += f"- **OS:** {agent.os}\\n""                    report += f"- **Last Check-in:** {agent.last_checkin.strftime('%Y-%m-%d %H:%M:%S')}\\n""'                    report += f"- **Tasks:** {len(agent.tasks)}\\n\\n""
            # Listeners
            if self.framework.listeners:
                report += "## Listeners\\n\\n""                for listener in self.framework.listeners.values():
                    listener_str = (
                        f"- **{listener.name}:** {listener.protocol.value}://""                        f"{listener.host}:{listener.port} ({listener.status}) - ""                        f"{listener.agents_connected} agents\\n""                    )
                    report += listener_str
                report += "\\n""
            return report

        else:
            raise ValueError(f"Unsupported format: {output_format}")"
    async def _load_extenders(self) -> None:
        """Load configured extenders/plugins"""if not self.framework:
            return

        for extender_path in self.framework.profile.extenders:
            try:
                # Mock extender loading - in real implementation would load actual plugins
                extender_name = extender_path.split("/")[-2]  # Extract name from path"                extender = C2Extender(
                    name=extender_name,
                    extender_type="listener" if "listener" in extender_path else "agent","                    path=extender_path,
                    loaded=True
                )
                self.framework.extenders[extender_name] = extender
                self.logger.info(f"Loaded extender: {extender_name}")"
            except Exception as e:
                self.logger.error(f"Failed to load extender {extender_path}: {e}")"
    async def _start_listeners(self) -> None:
        """Start all configured listeners"""if not self.framework:
            return

        for listener in self.framework.listeners.values():
            await self._start_listener(listener)

    async def _start_listener(self, listener: C2Listener) -> bool:
        """Start a specific listener (mock implementation)"""try:
            # Mock listener startup
            listener.status = "running""            self.logger.info(f"Started listener: {listener.name} ({listener.listener_id})")"            return True
        except Exception as e:
            self.logger.error(f"Failed to start listener {listener.name}: {e}")"            return False

    async def _stop_listener(self, listener_id: str) -> None:
        """Stop a specific listener"""if not self.framework or listener_id not in self.framework.listeners:
            return

        listener = self.framework.listeners[listener_id]
        listener.status = "stopped""        self.logger.info(f"Stopped listener: {listener.name}")"
    async def _agent_health_checker(self) -> None:
        """Background task to check agent health"""while self.running:
            try:
                await asyncio.sleep(60)  # Check every minute

                if not self.framework:
                    continue

                current_time = datetime.now()
                dead_agents = []

                for agent in self.framework.agents.values():
                    if agent.status == AgentStatus.ACTIVE:
                        # Check if agent missed check-in
                        time_since_checkin = (current_time - agent.last_checkin).total_seconds()
                        expected_checkin = agent.sleep_time * (1 + agent.jitter)

                        if time_since_checkin > expected_checkin * 3:  # 3x expected time
                            agent.status = AgentStatus.DEAD
                            dead_agents.append(agent.agent_id)
                            await self._log_event("agent_dead", {"agent_id": agent.agent_id})"
                if dead_agents:
                    self.logger.warning(f"Marked {len(dead_agents)} agents as dead")"
            except Exception as e:
                self.logger.error(f"Agent health check error: {e}")"
    async def _task_processor(self) -> None:
        """Background task to process and timeout tasks"""while self.running:
            try:
                await asyncio.sleep(30)  # Check every 30 seconds

                if not self.framework:
                    continue

                current_time = datetime.now()
                timed_out_tasks = []

                for task in self.framework.tasks.values():
                    if task.status == TaskStatus.RUNNING:
                        if task.executed_at:
                            runtime = (current_time - task.executed_at).total_seconds()
                            if runtime > task.timeout:
                                task.status = TaskStatus.FAILED
                                task.error = "Task timed out""                                task.completed_at = current_time
                                timed_out_tasks.append(task.task_id)
                                await self._log_event("task_timeout", {"task_id": task.task_id})"
                if timed_out_tasks:
                    self.logger.warning(f"Timed out {len(timed_out_tasks)} tasks")"
            except Exception as e:
                self.logger.error(f"Task processor error: {e}")"
    async def _session_manager(self) -> None:
        """Background task to manage operator sessions"""while self.running:
            try:
                await asyncio.sleep(300)  # Check every 5 minutes

                if not self.framework:
                    continue

                current_time = datetime.now()
                expired_sessions = []

                for session in self.framework.sessions.values():
                    # Expire sessions after 24 hours of inactivity
                    if (current_time - session.last_activity).total_seconds() > 86400:
                        expired_sessions.append(session.session_id)

                for session_id in expired_sessions:
                    del self.framework.sessions[session_id]
                    await self._log_event("session_expired", {"session_id": session_id})"
                if expired_sessions:
                    self.logger.info(f"Expired {len(expired_sessions)} inactive sessions")"
            except Exception as e:
                self.logger.error(f"Session manager error: {e}")"
    async def _log_event(self, event_type: str, data: Dict[str, Any]) -> None:
        """Log a framework event"""if not self.framework:
            return

        event = {
            "timestamp": datetime.now().isoformat(),"            "type": event_type,"            "data": data"        }

        self.framework.events.append(event)

        # Keep only last 1000 events
        if len(self.framework.events) > 1000:
            self.framework.events = self.framework.events[-1000:]

    def _hash_password(self, password: str) -> str:
        """Hash password for storage"""salt = secrets.token_hex(16)
        hash_obj = hashlib.sha256((password + salt).encode())
        return f"{salt}:{hash_obj.hexdigest()}""
    def _verify_password(self, password: str, hash_string: str) -> bool:
        """Verify password against hash"""try:
            salt, hash_value = hash_string.split(":")"            hash_obj = hashlib.sha256((password + salt).encode())
            return hash_obj.hexdigest() == hash_value
        except Exception:
            return False

    async def cleanup(self) -> None:
        """Cleanup resources"""await self.stop_framework()
        if self.framework:
            self.framework.agents.clear()
            self.framework.listeners.clear()
            self.framework.tasks.clear()
            self.framework.extenders.clear()
            self.framework.sessions.clear()
            self.framework.tunnels.clear()
            self.framework.downloads.clear()
            self.framework.screenshots.clear()
            self.framework.events.clear()
        self.logger.info("C2 Framework Core cleaned up")"