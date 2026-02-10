# Infrastructure & Swarm Services

The infrastructure layer (`src/infrastructure/`) provides the "Liquid Foundation" of the PyAgent swarm, handling distributed state, secure transport, and heavy compute offloading.

## 🌌 Voyager: Decentralized Transport
The "Voyager" layer implements a zero-broker, P2P message bus.
- **Protocol**: ZeroMQ DEALER/ROUTER for asynchronous communication.
- **Discovery**: `mDNS` (Zeroconf) allows nodes to join and leave the cluster without a central registry.
- **Security**: AES-GCM encryption for all inter-node traffic.
- **Stability**: Specialized `asyncio` loop management for graceful shutdowns on all operating systems.

## 🚢 Fleet Management
- **`FleetManager`**: Orchestrates local agent resources, assigning tasks based on availability and priority.
- **`ZeroTrustFirewall`**: Integrated into the fleet loop to verify all incoming P2P requests before they reach an agent.
- **`InterFleetBridgeOrchestrator`**: Handles task "Teleportation" between different network nodes (e.g., sending a Video task to a node with a beefy GPU).
- **Consensus**: Implements Raft for consistent shared state and a Byzantine Fault Tolerant (BFT) implementation (`FleetConsensusManager`) for safety-critical consensus.

## 🌩️ Cloud & Services
- **`CloudProviderManager`**: Abstracts interactions with Azure AI, AWS Bedrock, and GCP Vertex.
- **MCP (Model Context Protocol)**: Dynamic discovery and execution of tools. PyAgent allows agents to "boot" new MCP servers on demand.
- **Docker/Sandbox**: Secure execution environment for code toolsets, ensuring filesystem isolation and network egress rules.

## 💾 Storage & Persistence
- **State Transactions**: `AgentStateManager` ensures all file-system changes are atomic and can be rolled back on failure via `StateTransaction`.
- **Paged KV_v2 Cache**: Virtual memory management for agent reasoning, utilizing Rust offsets for high-speed block hashing and retrieval.
- **KV Transfer**: High-speed sharding of memory and experience buffers using `msgpack` and LSH indexing.
- **Distributed RAID-10**: Mirroring of part-based state snapshots across peer nodes for disaster recovery.

## 🛡️ Security Infrastructure
- **Zero-Trust mesh**: No implicit trust. All nodes must authenticate via the handshake protocol.
- **Network Isolation**: Strict egress filtering for sandboxed tools.
- **Credential Vault**: Encrypted storage for API keys and tokens, never exposed to the reasoning logs.
- **System Sanitizer**: Automated scanning of tool inputs/outputs to prevent prompt injection or exfiltration attempts.

---
*Distributed Intelligence. Secure by Default.*
