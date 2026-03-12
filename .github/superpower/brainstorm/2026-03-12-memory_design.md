> **2026-03-10 Async Runtime Note**: Project migrated to async-first runtime. All memory I/O, disk access, and cross-agent reads/writes **must** use `async`/`await`. Synchronous loops calling memory APIs are blocked by the automated test suite.

---

# Memory Subsystem Design

## Status

> **Architecture rule**: All memory and disk operations are implemented in Rust (`rust_core/`). Python code calls into the subsystem exclusively via `from rust_core import <Class>` — PyO3 `#[pyclass]` and `#[pymodule]` exports defined in Rust. No Python intermediary files, no delegation wrappers.

| Layer | Rust module | Python import | Status |
|---|---|---|---|
| Core KV store | `rust_core/src/memory.rs` | `from rust_core import MemoryStore` | ⚠️ `src/core/memory.py` has Python logic — delete; implement `MemoryStore` in Rust |
| Swarm shared & agent memory | `rust_core/src/memory.rs` | `from rust_core import SharedMemory, AgentMemory` | ⚠️ `src/swarm/memory.py` has Python logic — delete; implement in Rust |
| Vector search | `rust_core/src/memory.rs` → `search_vector_rust` | `from rust_core import search_vector` | ✅ Rust implemented |
| Episode / utility scoring | `rust_core/src/agents/memory.rs` | `from rust_core import EpisodeStore` | ✅ Rust functions exist; `EpisodeStore` struct planned |
| KV-cache / GPU pressure | `rust_core/src/inference/memory.rs` | `from rust_core import MemoryPressure` | ✅ Rust implemented |
| Semantic `store`/`query` API | `rust_core/src/memory.rs` | `from rust_core import MemoryStore` | 🔲 Planned |
| `MemoryTransactionManager` | `rust_core/src/memory.rs` | `from rust_core import MemoryTransaction` | 🔲 Planned |
| Encrypted disk tier | `rust_core/src/memory.rs` | internal to Rust — no Python surface | 🔲 Planned |
| Encrypted growable RAM blocks | `rust_core/src/memory.rs` | `from rust_core import MemoryBlockRegistry, EncryptedMemoryBlock` | 🔲 Planned |

---

## Five-Layer Architecture

All five layers are implemented entirely in Rust (`rust_core/`). Python code imports the types directly from `rust_core` — there are no intermediary Python files. Rust defines each type with `#[pyclass]` and registers it in `#[pymodule]`; maturin builds and installs the extension so `from rust_core import X` works like any other Python import.

```
┌───────────────────────────────────────────────────────────────────┐
│  Layer 5 – Archived / Disk tier                                   │
│  Encrypted WAL-backed storage, owner-key-signed                   │
│  rust_core/src/memory.rs  (#[pyclass] DiskTier — planned)         │
├───────────────────────────────────────────────────────────────────┤
│  Layer 4 – Episodic / Long-term memory                            │
│  create_episode_struct · calculate_new_utility ·                  │
│  filter_relevant_memories · EpisodeStore                          │
│  rust_core/src/agents/memory.rs  (#[pyclass] EpisodeStore)        │
├───────────────────────────────────────────────────────────────────┤
│  Layer 3 – Semantic / Vector memory                               │
│  search_vector_rust · store() · query()                           │
│  rust_core/src/memory.rs  (search_vector_rust ✅; store/query 🔲) │
├───────────────────────────────────────────────────────────────────┤
│  Layer 2 – Swarm shared + agent-private memory                    │
│  SharedMemory (DashMap) · AgentMemory (HashMap)                   │
│  rust_core/src/memory.rs  (#[pyclass] — planned)                  │
├───────────────────────────────────────────────────────────────────┤
│  Layer 1 – Core KV store                                          │
│  MemoryStore  HashMap<Uuid, MemoryEntry>                          │
│  rust_core/src/memory.rs  (#[pyclass] — planned)                  │
└───────────────────────────────────────────────────────────────────┘
         ↑ all writes gated behind MemoryTransactionManager
           (#[pyclass] MemoryTransaction — planned)

  Python call site:                   Rust (rust_core/)
  from rust_core import MemoryStore   #[pyclass]
  from rust_core import SharedMemory  #[pyclass]
  from rust_core import MemoryTransaction  #[pyclass]
  ──────────────────────────────────────────────────
  No Python files between caller and Rust implementation.
  src/core/memory.py and src/swarm/memory.py are deleted
  once their Rust replacements are shipped.
```

---

## Layer Details

### Layer 1 – Core KV Store

- **Implementation**: `#[pyclass] MemoryStore` backed by `HashMap<Uuid, MemoryEntry>` in `rust_core/src/memory.rs`.
- **Python usage**: `from rust_core import MemoryStore` — no Python file in between.
- `src/core/memory.py` currently contains a Python dict implementation; it is **deleted** when `MemoryStore` ships from Rust.
- Supports O(1) direct lookup, lazy initialisation via `OnceCell`, and concurrent async access without GIL contention (`#[pyclass(frozen)]` where applicable).

### Layer 2 – Swarm Memory

Two scopes, both `#[pyclass]` types in `rust_core/src/memory.rs`:

| Scope | Rust type | Python import |
|---|---|---|
| `SharedMemory` – fleet-wide broadcast | `DashMap<K, V>` (lock-free concurrent) | `from rust_core import SharedMemory` |
| `AgentMemory` – per-agent private | `HashMap<K, V>` (single-owner) | `from rust_core import AgentMemory` |

- `src/swarm/memory.py` is **deleted** when these ship from Rust.
- Conflict resolution implemented in Rust: last-write-wins for scratch data; CRDT merge for structured knowledge entries.
- `async put`/`async get` are `async fn` exposed to Python via `pyo3-asyncio`.

### Layer 3 – Semantic / Vector Memory

- `search_vector_rust` (cosine dot-product, returns top-k indices) is already implemented in `rust_core/src/memory.rs` and exported via `#[pyfunction]`.
- `store(content, metadata, tags)` / `query(query_text, n_results, filter_tags)` are the **next implementation targets** in `rust_core/src/memory.rs`, also exported as `#[pymethods]` on `MemoryStore`.
- `src/memory/__init__.py` is **deleted** when these are shipped; call sites use `from rust_core import MemoryStore`.
- Index structures:

| Index | Rust type | Purpose |
|---|---|---|
| KV hash | `HashMap<Uuid, MemoryEntry>` | O(1) direct lookup |
| BTree | `BTreeMap<timestamp, Uuid>` | Range queries, ordered recall |
| Graph | petgraph `DiGraph` | Relationship + pattern queries |

- Lazy access tracking: each read updates an `accessed_at` timestamp; entries not accessed within a configurable TTL are candidates for tier promotion to Layer 4/5.

### Layer 4 – Episodic / Long-term Memory (`rust_core/src/agents/memory.rs`)

Three Rust functions are already implemented:

| Function | Purpose |
|---|---|
| `create_episode_struct` | Build a timestamped episode dict with success/failure and baseline utility |
| `calculate_new_utility` | Clamp-normalised score increment (`±0.2 / ±0.3`) |
| `filter_relevant_memories` | Filter a list of episode dicts by `min_utility` threshold |

- **Next target**: implement `#[pyclass] EpisodeStore` in `rust_core/src/agents/memory.rs` that owns the three existing functions and persists episodes directly to Layer 5 disk tier.
- Python usage: `from rust_core import EpisodeStore` — no Python file between caller and Rust.
- Synaptic pruning: a Rust background task (`tokio::spawn`) demotes episodes below `utility_floor` after `prune_after_days` to Layer 5 or deletes them; Python never manages this lifecycle.

### Layer 5 – Encrypted Disk / Archive Tier

> ⚠️ **Security constraint (CVE – Dependabot #31):** DiskCache ≤ 5.6.3 uses Python pickle by default. Any attacker with write access to the cache directory can achieve arbitrary code execution. **Python's DiskCache library must not be used.** All disk I/O is handled entirely in Rust.

Design (all Rust, `rust_core/src/memory.rs`):
- **Serialisation**: `bincode` or `rmp-serde` (MessagePack) — no pickle, no Python serialisation libraries.
- **Encryption**: `ring` crate — entries encrypted with owner's Ed25519/X25519 public key before any write syscall.
- **Storage backend**: `rusqlite` (SQLite WAL mode) or `lmdb-rs` — opened and managed entirely from Rust.
- Each entry carries: `uuid`, `encrypted_blob`, `pubkey_fingerprint`, `written_at`, `accessed_at`, `ttl`.
- Reads: Rust decrypts into a `Vec<u8>` held in Rust heap memory; decrypted bytes are never written back to disk.
- Python never touches the raw file handles, encryption keys, or serialised bytes.

---

## Transaction Layer – `MemoryTransactionManager` (Planned)

All writes to any layer must go through a `MemoryTransaction`. Implemented as `#[pyclass] MemoryTransaction` in `rust_core/src/memory.rs`.

```rust
// rust_core/src/memory.rs  — to be implemented
#[pyclass]
pub struct MemoryTransaction {
    tid: Uuid,
    journal: WalJournal,   // rusqlite WAL
    ops: Vec<MemoryOp>,
}

#[pymethods]
impl MemoryTransaction {
    pub fn __aenter__<'py>(slf: PyRef<'py, Self>) -> PyResult<Bound<'py, PyAny>> { ... }
    pub fn __aexit__<'py>(&mut self, exc: Option<&Bound<'py, PyAny>>) -> PyResult<Bound<'py, PyAny>> { ... }
    pub fn set<'py>(&mut self, layer: u8, key: &str, value: Bound<'py, PyAny>) -> PyResult<Bound<'py, PyAny>> { ... }
    pub fn store<'py>(&mut self, content: &str, metadata: Bound<'py, PyAny>, tags: Vec<String>) -> PyResult<Bound<'py, PyAny>> { ... }
}
```

```python
# Call site — no wrapper, no intermediary file
from rust_core import MemoryTransaction

async with MemoryTransaction(tid=uuid4()) as tx:
    await tx.set(layer=1, key="agent::state", value=state)
    await tx.store(content=text, metadata=meta, tags=tags)
    # __aexit__ commits; exception triggers WAL rollback — both in Rust
```

- WAL journal managed by `rusqlite` WAL, opened and flushed entirely from Rust.
- Two-phase commit: journal write then apply — both in Rust.
- `ContextTransaction` lineage (`tid`, `parent_tid`) threaded through to prevent recursive memory writes.

---

## Indexing Strategy

| Workload | Primary index | Secondary index |
|---|---|---|
| Direct key lookup | KV (HashMap) | — |
| Time-range recall | BTree (timestamp) | KV for payload |
| Semantic / RAG | Vector (dot-product top-k) | BTree for recency filter |
| Relationship traversal | Graph (petgraph) | KV for payload |
| Episode filtering | Utility score scan | BTree for recency |

---

## Encrypted Growable Memory Blocks

### Goal

Each agent/user owns exclusive, encrypted memory that no other agent can read — even when agents share the same Rust process. Isolation is enforced cryptographically, not by access-control policy alone.

---

### Key Encapsulation — Hybrid Encryption

The owner supplies an **X25519 public key** (32 bytes) at block allocation. Rust derives a per-block **data encryption key (DEK)** using ECDH + HKDF, then uses it for all entry-level ChaCha20-Poly1305 encryption.

```
Owner supplies:  owner_pubkey  (X25519, 32 bytes)

At block allocation — inside Rust only:
  1. Gen ephemeral X25519 keypair  →  (eph_privkey, eph_pubkey)
  2. ECDH:   shared_secret = x25519(eph_privkey, owner_pubkey)
  3. HKDF-SHA256(ikm=shared_secret, salt=block_uuid, info="pyagent-dek/v1")
             → DEK  (32 bytes — ChaCha20Poly1305 key)
  4. Stored alongside block:  eph_pubkey (32 bytes)
                               owner_fingerprint = SHA-256(owner_pubkey)
  5. DEK lives only in Rust heap — never serialised, never returned to Python

At disk flush / block hand-off:
  Owner presents owner_privkey  →  Rust re-derives DEK  →  decrypts entries
```

- **DEK is a private Rust field** — never appears in any `#[pymethods]` return value.
- `eph_privkey` is dropped immediately after DEK derivation; `eph_pubkey` is kept so the owner can re-derive DEK later with their private key.
- On `release()` / teardown: slabs zero-filled with `zeroize` crate before `Vec` drop; DEK memory overwritten.

---

### `EncryptedMemoryBlock` — Rust Structure

```rust
// rust_core/src/memory.rs  —  to be implemented

const WARM_SLAB:  usize = 1  * 1024 * 1024;  //  1 MB  initial warm-up slab
const SLAB_SIZE:  usize = 10 * 1024 * 1024;  // 10 MB  growth increment

struct SlabPtr { slab_idx: u32, offset: u32, len: u32 }

#[pyclass]
pub struct EncryptedMemoryBlock {
    block_id:          uuid::Uuid,                      // immutable identity
    owner_fingerprint: [u8; 32],                        // SHA-256(owner_pubkey) — registry key
    eph_pubkey:        [u8; 32],                        // stored so owner can re-derive DEK
    dek:               chacha20poly1305::Key,            // heap-only, never serialised
    slabs:             Vec<Vec<u8>>,                    // growable: [warm(1MB), slab(10MB), …]
    directory:         HashMap<uuid::Uuid, SlabPtr>,    // entry_id → location
    write_cursor:      (usize, usize),                  // (slab_idx, byte_offset)
}

#[pymethods]
impl EncryptedMemoryBlock {
    /// Encrypt `plaintext` with DEK (ChaCha20-Poly1305) and append to slabs.
    pub fn put(&mut self, entry_id: &str, plaintext: &[u8]) -> PyResult<()> { … }
    /// Decrypt and return plaintext for `entry_id`; DEK stays in Rust.
    pub fn get(&self,     entry_id: &str) -> PyResult<Vec<u8>> { … }
    /// Zero-fill ciphertext in slab, remove from directory.
    pub fn purge(&mut self, entry_id: &str) -> PyResult<()> { … }
    /// Total committed bytes across all slabs.
    pub fn used_bytes(&self) -> PyResult<usize> { … }
    /// Number of slabs currently allocated.
    pub fn slab_count(&self) -> PyResult<usize> { … }
}
```

---

### Slab Growth Policy

| Event | Action |
|---|---|
| First `put()` | Use 1 MB warm-up slab — keeps idle agents cheap |
| `put()` would overflow current slab | `Vec::with_capacity(SLAB_SIZE)` — push one new 10 MB slab |
| `purge()` marks entry dead | Free space tracked; compaction deferred until slab ≥ 70 % dead |
| Compaction trigger | Live entries rewritten to fresh slab; old slab zero-filled and dropped |
| `release()` / agent teardown | Every slab zero-filled (`zeroize`); DEK overwritten; block removed from registry |

Growth is pay-as-you-go: an agent writing 500 KB holds one 1 MB warm slab. An agent writing 25 MB holds one 1 MB slab + two 10 MB slabs (warm + 2 × growth).

---

### Block Registry — `MemoryBlockRegistry`

```rust
// rust_core/src/memory.rs  —  to be implemented

#[pyclass]
pub struct MemoryBlockRegistry {
    // DashMap shards across CPU cores — concurrent agents never contend on a single lock
    blocks: DashMap<[u8; 32], EncryptedMemoryBlock>,  // SHA-256(owner_pubkey) → block
}

#[pymethods]
impl MemoryBlockRegistry {
    /// Allocate a new encrypted block for `owner_pubkey`.  Returns block_id (UUID string).
    pub fn allocate(&self,   owner_pubkey: &[u8]) -> PyResult<String> { … }
    /// Return a reference to the block.  Returns PyRuntimeError if fingerprint mismatches.
    pub fn get_block(&self,  owner_pubkey: &[u8]) -> PyResult<Py<EncryptedMemoryBlock>> { … }
    /// Zero-fill all slabs and remove block from registry.
    pub fn release(&self,    owner_pubkey: &[u8]) -> PyResult<()> { … }
    /// Bytes committed across all blocks (fleet-level telemetry).
    pub fn total_used_bytes(&self) -> PyResult<usize> { … }
}
```

`get_block()` fingerprints the supplied `owner_pubkey` via SHA-256 and looks it up in the DashMap. A caller supplying the wrong key gets a different fingerprint → missed lookup → `PyRuntimeError("block not found")`. There is no bypass path.

---

### Python Interface

```python
from rust_core import MemoryBlockRegistry
from uuid import uuid4

registry = MemoryBlockRegistry()          # one per process / swarm node

# ── Agent A owns its block ──────────────────────────────────────────
block_id_a = registry.allocate(owner_pubkey=agent_a_x25519_pubkey_bytes)
block_a    = registry.get_block(owner_pubkey=agent_a_x25519_pubkey_bytes)
block_a.put(entry_id=str(uuid4()), plaintext=b"Agent A private state")

# ── Agent B allocates its own block — separate DEK ──────────────────
block_id_b = registry.allocate(owner_pubkey=agent_b_x25519_pubkey_bytes)
block_b    = registry.get_block(owner_pubkey=agent_b_x25519_pubkey_bytes)

# ── Cross-agent access attempt — blocked by fingerprint mismatch ─────
# registry.get_block(owner_pubkey=agent_a_x25519_pubkey_bytes)
#   → PyRuntimeError("block not found")   ← returned to Agent B

# ── Teardown — zero-fills all slabs ─────────────────────────────────
registry.release(owner_pubkey=agent_a_x25519_pubkey_bytes)
```

---

### New `Cargo.toml` Dependencies

```toml
# Add to rust_core/Cargo.toml
x25519-dalek = { version = "2", features = ["static_secrets"] }  # ECDH — DEK derivation
dashmap      = "6"                                                 # concurrent block registry
zeroize      = { version = "1", features = ["derive"] }           # secure slab wipe on drop
uuid         = { version = "1", features = ["v4", "serde"] }      # block_id + entry_id
subtle       = "2"                                                 # constant-time fingerprint compare
```

`chacha20poly1305`, `hkdf`, `sha2`, `rand_core` — already in `Cargo.toml`. No removals.

---

### Security Properties

| Property | How achieved |
|---|---|
| Agent A cannot read Agent B's memory | `get_block()` fingerprints pubkey via SHA-256 — wrong key → missed DashMap lookup → error |
| DEK never exposed to Python | Private Rust field; no `#[pymethods]` getter; not in any serialised form |
| Memory zeroed on release | `zeroize` crate overwrites all slab `Vec<u8>` bytes before drop |
| Forward secrecy per block | Fresh ephemeral X25519 keypair per block; `eph_privkey` dropped after DEK derivation |
| No timing oracle on cross-agent probing | Constant-time SHA-256 fingerprint compare via `subtle` crate; `DashMap` hash lookup |
| Disk tier re-uses block encryption | Ciphertext already encrypted with DEK — no second layer needed; `eph_pubkey` stored in metadata |

---

### Integration with Five-Layer Architecture

- **Layers 1–4 (RAM)**: `MemoryBlockRegistry` is the gatekeeper. `MemoryStore`, `AgentMemory`, `SharedMemory`, and `EpisodeStore` all write entries through `EncryptedMemoryBlock.put()` — they never hold raw plaintext beyond the duration of a single call.
- **Layer 5 (disk)**: slab ciphertext is written verbatim (already encrypted with DEK). `eph_pubkey` and `owner_fingerprint` are stored in block metadata so the owner can re-derive DEK offline with their private key.
- **`MemoryTransaction`**: each `tx.set()` / `tx.store()` resolves the calling agent's `owner_fingerprint`, routes to that owner's `EncryptedMemoryBlock`, and never touches another agent's block.

---

## Memory Pressure & Swapping (`rust_core/src/inference/memory.rs`)

Already implemented in Rust:

| Function | Purpose |
|---|---|
| `calculate_memory_pressure_rust` | Score 0–1 based on used/total blocks and reserved ratio |
| `blocks_to_free_rust` | Determine how many blocks to evict given pressure score |
| `chunk_boundaries_rust` | Compute prefill chunk boundaries shrunk under pressure |

Promotion / demotion policy:

```
RAM (L1–L3)  ──── pressure > 0.7 ───►  Disk (L5)
Disk (L5)    ──── accessed recently ──►  RAM (L3/L4)
```

---

## Security Requirements

1. **No pickle serialisation** anywhere in the memory stack.
2. All disk-tier data encrypted with owner public key (Ed25519/X25519) before write.
3. `MemoryTransaction` journal entries encrypted at rest.
4. `SharedMemory` entries accessible to fleet agents are integrity-checked with HMAC before use.

   #### HMAC key management

   * **Derivation** – each swarm is provisioned with a master symmetric key (`K_master`).
     Use a hierarchical KDF (HKDF‑SHA256) to derive per‑message keys:
     `K_msg = HKDF(K_master, context=agent_id||sequence)` so that every entry has
     a unique key.  The Rust implementation in `rust_core/src/memory.rs` already
     calls `aead::hmac_sha256` with a supplied key; modify `SharedMemory` helpers to
     derive `K_msg` before signing/verifying.
   * **Distribution** – `K_master` is generated by the fleet CA and distributed
     to each agent via sealed‑secret provisioning (e.g. Kubernetes `Secret` or
     Vault wrapped key).  Agents cache the master key in memory only; never write
     it to disk.  When a new agent joins the swarm it requests the current
     master key over the cluster’s mTLS channel, authenticated by its client
     certificate.
   * **Rotation policy** – rotate `K_master` periodically (e.g. 30‑day interval)
     or on compromise.  The rotation controller in `rust_core/src/security/crypto.rs`
     should emit a new key and propagate it via the same CA distribution channel.
     Agents keep the previous and current master key and attempt verification with
     both, falling back to the old key until reprovisioned with new entries.  New
     `SharedMemory` writes always use the latest derived keys; a migration job may
     re‑HMAC older entries offline if long‑term integrity is required.
   * **Rust verification** – when loading a `SharedMemory` entry, call
     `verify_hmac(&entry.data, &derive_msg_key(&agent_id, &entry.seq), &entry.tag)`
     using whichever master key(s) are active.  The loader should surface a
     `IntegrityError` if neither key verifies.

5. Sensitive entries (PII, credentials) support explicit `purge()` and `anonymize()` operations.
6. **Per-agent RAM isolation**: each agent's in-memory entries are encrypted with a per-block DEK derived from the owner's X25519 public key. No agent can access another's block. See [Encrypted Growable Memory Blocks](#encrypted-growable-memory-blocks).

---

## Design Principles Summary

1. **Rust-only memory and disk ops** – all memory management, indexing, serialisation, encryption, and disk I/O is implemented in Rust. Python code reaches the subsystem via `from rust_core import X` — no intermediary Python files, no wrappers, no fallbacks.
2. **Async-first** – memory `async fn` in Rust, surfaced to Python via `pyo3-asyncio`. No synchronous blocking memory I/O anywhere.
3. **Delete Python logic files when replaced** – `src/core/memory.py`, `src/swarm/memory.py`, and `src/memory/__init__.py` are removed from the repo as each Rust `#[pyclass]` ships. They are not kept as "stubs".
4. **Layered promotion/demotion** – data moves between RAM and disk tiers based on utility score and access recency; all movement logic is in Rust.
5. **Transaction integrity** – every write is gated behind `MemoryTransactionManager` (Rust WAL).
6. **Security by default** – disk tier encrypted in Rust (`ring` crate); no Python serialisation; no pickle; HMAC on shared entries computed in Rust.

---

## Open Questions / Future Work

### Implementation work (priority order)
- [ ] Implement `#[pyclass] MemoryStore` with `get`/`set`/`store`/`query` in `rust_core/src/memory.rs`; delete `src/core/memory.py` and `src/memory/__init__.py`
- [ ] Implement `#[pyclass] SharedMemory` (`DashMap`) and `#[pyclass] AgentMemory` (`HashMap`) in `rust_core/src/memory.rs`; delete `src/swarm/memory.py`
- [ ] Implement `#[pyclass] MemoryTransaction` with `__aenter__`/`__aexit__`, WAL journal via `rusqlite`
- [ ] Implement `#[pyclass] EncryptedMemoryBlock` with `put`/`get`/`purge`/`used_bytes`/`slab_count` in `rust_core/src/memory.rs` (ECDH X25519 + HKDF-SHA256 → DEK, ChaCha20-Poly1305 per entry, growable 1 MB warm + 10 MB slabs)
- [ ] Implement `#[pyclass] MemoryBlockRegistry` with `allocate`/`get_block`/`release`/`total_used_bytes` — `DashMap` keyed by SHA-256(owner_pubkey); constant-time fingerprint compare via `subtle` crate
- [ ] Add `x25519-dalek`, `dashmap`, `zeroize`, `uuid`, `subtle` to `rust_core/Cargo.toml`
- [ ] Route `MemoryStore`, `AgentMemory`, `EpisodeStore` writes through `EncryptedMemoryBlock.put()` — no raw plaintext held outside a single call
- [ ] Implement encrypted disk tier in Rust (`bincode` + `ring` Ed25519/X25519 + `rusqlite` WAL); no Python surface; disk tier writes slab ciphertext verbatim (DEK handles encryption)
- [ ] Implement `#[pyclass] EpisodeStore` in `rust_core/src/agents/memory.rs`; wire persistence to disk tier
- [ ] Wire `pyo3-asyncio` for all `async fn` methods across all `#[pyclass]` types
- [ ] Expose Graph index via `petgraph` `DiGraph` in Rust; add `#[pymethods]` for relationship queries
- [ ] Synaptic pruning background task (`tokio::spawn`) in Rust — configurable TTL + `utility_floor`
- [ ] Memory compression for archived entries (`zstd` crate, pure Rust)
- [ ] Horizontal sharding for fleet-scale `SharedMemory`
- [ ] ML-based prefetch prediction (access pattern learning)

---

*Sources: `rust_core/src/memory.rs`, `rust_core/src/agents/memory.rs`, `rust_core/src/inference/memory.rs`, `src/core/memory.py` (stub), `src/swarm/memory.py` (stub), Dependabot advisory #31 (DiskCache CVE).*