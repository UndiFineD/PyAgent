# Copyright 2026 PyAgent Authors
# Phase 320: LAN Discovery & Peer Synchronization

import socket
import threading
import json
import time
import logging
import hmac
import hashlib
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from src.infrastructure.network.NetworkUtils import get_ip
from src.observability.StructuredLogger import StructuredLogger

logger = StructuredLogger(__name__)

@dataclass
class PeerInfo:
    agent_id: str
    ip: str
    port: int
    last_seen: float
    metadata: Dict[str, Any]
    trust_score: float = 1.0
    latency: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

class LANDiscovery:
    """
    Decentralized LAN Discovery for PyAgents.
    Follows an Announce -> Respond -> Register -> Sync cycle.
    """
    DISCOVERY_PORT = 31415
    BROADCAST_ADDR = "255.255.255.255"
    MAX_CLOCK_SKEW = 10.0  # Seconds
    
    def __init__(
        self, 
        agent_id: str, 
        service_port: int, 
        secret_key: Optional[str] = None,
        metadata: Optional[Dict] = None
    ):
        self.agent_id = agent_id
        self.service_port = service_port
        self.secret_key = secret_key
        self.metadata = metadata or {}
        self.registry: Dict[str, PeerInfo] = {}
        self._running = False
        self._lock = threading.Lock()
        self._nonces: Dict[str, float] = {}  # agent_id: last_timestamp
        self._ping_times: Dict[str, float] = {} # agent_id: sent_time
        
        # Local IP detection (lazy)
        self._local_ip = None

    @property
    def local_ip(self) -> str:
        if not self._local_ip:
            self._local_ip = get_ip()
        return self._local_ip

    def _sign(self, data: str) -> str:
        if not self.secret_key:
            return "unsigned"
        return hmac.new(
            self.secret_key.encode(), 
            data.encode(), 
            hashlib.sha256
        ).hexdigest()

    def _verify(self, data: str, signature: str) -> bool:
        if not self.secret_key:
            return True
        expected = self._sign(data)
        return hmac.compare_digest(expected, signature)

    def _create_message(self, msg_type: str, extra: Optional[Dict] = None) -> bytes:
        payload: Dict[str, Any] = {
            "type": msg_type,
            "agent_id": self.agent_id,
            "ip": self.local_ip,
            "port": self.service_port,
            "timestamp": time.time(),
            "metadata": self.metadata
        }
        if extra:
            payload.update(extra)
        
        data_str = json.dumps(payload, sort_keys=True)
        envelope = {
            "data": payload,
            "sig": self._sign(data_str)
        }
        return json.dumps(envelope).encode()

    def start(self):
        """Starts the discovery threads."""
        if self._running:
            return
        self._running = True
        self._listen_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self._listen_thread.start()
        self._announce_thread = threading.Thread(target=self._announce_loop, daemon=True)
        self._announce_thread.start()
        logger.info(f"LANDiscovery: Active for {self.agent_id} on {self.local_ip}:{self.service_port}")

    def stop(self):
        """Stops the discovery threads."""
        self._running = False

    def _announce_loop(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        # Initial announcement
        try:
            msg = self._create_message("ANNOUNCE")
            sock.sendto(msg, (self.BROADCAST_ADDR, self.DISCOVERY_PORT))
        except Exception as e:
            logger.error(f"LANDiscovery: Initial announcement failed: {e}")

        while self._running:
            try:
                # Periodic Heartbeat
                msg = self._create_message("HEARTBEAT")
                sock.sendto(msg, (self.BROADCAST_ADDR, self.DISCOVERY_PORT))
                
                # Registry Sync (Gossip)
                if len(self.registry) > 0:
                    self._sync_registry(sock)
                    
            except Exception as e:
                logger.debug(f"LANDiscovery: Background loop error: {e}")
            
            time.sleep(30) # Announce every 30 seconds

    def _sync_registry(self, sock: socket.socket):
        with self._lock:
            # Send top 10 most recent peers
            peers_list = sorted(
                [p.to_dict() for p in self.registry.values()],
                key=lambda x: x['last_seen'],
                reverse=True
            )[:10]
            
        msg = self._create_message("SYNC", {"peers": peers_list})
        sock.sendto(msg, (self.BROADCAST_ADDR, self.DISCOVERY_PORT))

    def _listen_loop(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            # Bind to all interfaces on DISCOVERY_PORT
            sock.bind(("", self.DISCOVERY_PORT))
        except Exception as e:
            logger.error(f"LANDiscovery: Failed to bind to port {self.DISCOVERY_PORT}: {e}")
            return

        while self._running:
            try:
                data, addr = sock.recvfrom(65535)
                self._handle_packet(data, addr)
            except Exception as e:
                if self._running:
                    logger.debug(f"LANDiscovery: Listen loop error: {e}")

    def _handle_packet(self, data: bytes, addr: tuple):
        try:
            envelope = json.loads(data.decode())
            payload = envelope.get("data")
            sig = envelope.get("sig")
            
            if not payload or not sig:
                return
            
            # 1. Validation & Security
            data_str = json.dumps(payload, sort_keys=True)
            if not self._verify(data_str, sig):
                logger.warning(f"LANDiscovery: Invalid signature from {addr}")
                return

            remote_agent_id = payload.get("agent_id")
            if remote_agent_id == self.agent_id:
                return # Self ignore

            msg_timestamp = payload.get("timestamp", 0)
            now = time.time()
            
            # Anti-Replay & Clock Skew Protection
            if abs(now - msg_timestamp) > self.MAX_CLOCK_SKEW:
                logger.debug(f"LANDiscovery: Dropping message from {remote_agent_id} (Clock skew: {now - msg_timestamp:.2f}s)")
                return
            
            if self._nonces.get(remote_agent_id, 0) >= msg_timestamp:
                return # Replay or old message
            self._nonces[remote_agent_id] = msg_timestamp

            msg_type = payload.get("type")
            
            # 2. Registration
            self._update_peer(payload)
            
            # 3. Message Handling
            if msg_type == "ANNOUNCE":
                # Direct respond to announcer
                resp = self._create_message("ACK")
                self._ping_times[remote_agent_id] = now
                socket.socket(socket.AF_INET, socket.SOCK_DGRAM).sendto(resp, (addr[0], self.DISCOVERY_PORT))
                logger.info(f"LANDiscovery: New peer announced: {remote_agent_id} at {addr[0]}")

            elif msg_type == "ACK":
                # Calculate latency if we sent the request
                if remote_agent_id in self._ping_times:
                    latency = (now - self._ping_times.pop(remote_agent_id)) * 1000 # ms
                    with self._lock:
                        if remote_agent_id in self.registry:
                            self.registry[remote_agent_id].latency = latency

            elif msg_type == "SYNC":
                for peer_data in payload.get("peers", []):
                    self._update_peer(peer_data)

        except Exception as e:
            logger.debug(f"LANDiscovery: Malformed packet from {addr}")

    def _update_peer(self, data: Dict[str, Any]):
        agent_id = data.get("agent_id")
        if not agent_id or agent_id == self.agent_id:
            return
        
        with self._lock:
            existing = self.registry.get(agent_id)
            latency = existing.latency if existing else data.get("latency", 0.0)
            
            # Update or Register
            self.registry[agent_id] = PeerInfo(
                agent_id=agent_id,
                ip=data.get("ip"),
                port=int(data.get("port")),
                last_seen=time.time(),
                metadata=data.get("metadata", {}),
                trust_score=data.get("trust_score", 1.0),
                latency=latency
            )

    def get_active_peers(self, max_age: int = 300) -> List[PeerInfo]:
        """Returns list of peers seen within max_age seconds."""
        now = time.time()
        with self._lock:
            return [p for p in self.registry.values() if now - p.last_seen < max_age]

    def clear_stale_peers(self, max_age: int = 3600):
        """Removes peers not seen for an hour."""
        now = time.time()
        with self._lock:
            stale = [k for k, v in self.registry.items() if now - v.last_seen > max_age]
            for k in stale:
                del self.registry[k]
