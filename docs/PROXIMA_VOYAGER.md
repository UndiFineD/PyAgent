# PROXIMA VOYAGER: Interstellar Swarm Orchestration

## Overview
Proxima is complete. Voyager awaits.

Voyager is the next major evolution of the PyAgent ecosystem, moving from a single-machine fleet to a truly decentralized, Peer-to-Peer (P2P) swarm orchestration system that spans multiple distinct user machines across any network.

## Key Architectural Shifts

### 1. From "Fleet" to "Constellation"
Traditional fleets are localized. Constellations are distributed. Voyager allows agents on Machine A to seamlessly delegate tasks to agents on Machine B without a centralized server.

### 2. P2P Binary Communication (FastSwarm v2)
Using the foundations laid in Phase 255 (Binary Protocol), Voyager utilizes a DHT (Distributed Hash Table) for agent discovery and `noise`-protocol encrypted binary streams for secure inter-node communication.

### 3. Federated Long-Term Memory
Memory isn't just local; it's sharded across the constellation. An agent in New York can query the "Experience Buffer" of an agent in Tokyo to avoid repeating the same mistake.

## Mission Phases

| Phase | Name | Focus | Status |
|-------|------|-------|--------|
| 1.0 | Discovery | mDNS/DHT-based peer discovery and identity verification. | **IN-PROGRESS (mDNS Active)** |
| 2.0 | Transport | Encrypted P2P binary message bus using `libp2p` or `ZeroMQ`. | *Planned* |
| 3.0 | Consensus | Multi-surgeon Byzantine Fault Tolerance (BFT). | *Planned* |
| 4.0 | Synergy | Cross-machine resource sharing and task preemption. | *Planned* |

### Technical Implementation (Phase 1.0)
The discovery layer is implemented via `DiscoveryNode` using the `zeroconf` protocol, allowing nodes on the same local network segment to identify each other without a central registry.

- **Service Type**: `_pyagent_voyager._tcp.local.`
- **Broadcast**: Nodes advertise their UUID, IP, and Version.
- **Location**: `src/infrastructure/voyager/DiscoveryNode.py`

## Conclusion
The swarm is no longer confined to one machine. It is everywhere.

---
*Proxima is complete. Voyager awaits.*
