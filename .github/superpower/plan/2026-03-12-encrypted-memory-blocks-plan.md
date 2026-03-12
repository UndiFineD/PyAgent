# Encrypted Growable Memory Blocks — Implementation Plan

**Goal:** Implement `EncryptedMemoryBlock` and `MemoryBlockRegistry` as PyO3 `#[pyclass]` types in `rust_core/src/memory.rs`, giving every agent cryptographically isolated RAM via X25519 ECDH + HKDF-SHA256 → ChaCha20-Poly1305, with a growable 1 MB warm-up + 10 MB slab allocator, zeroed on release.

**Architecture:**
- Pure Rust implementation in `rust_core/src/memory.rs` — no new Python files
- DEK derived from owner X25519 pubkey; lives only in Rust heap; never returned to Python
- `DashMap<[u8;32], EncryptedMemoryBlock>` registry, keyed by `SHA-256(owner_pubkey)`
- `memory::register(m)` already wired in `lib.rs` — only `m.add_class::<T>()` calls needed

**Tech Stack:** Rust 2021 · PyO3 0.24 · `x25519-dalek 2` · `dashmap 6` · `zeroize 1` · `uuid 1` · `subtle 2` · `chacha20poly1305 0.10` · `hkdf 0.12` · `sha2 0.10` (last 3 already in Cargo.toml)

---

### Task 1 — Add 5 new dependencies to `Cargo.toml`

**Step 1: Edit `rust_core/Cargo.toml`**

In `[dependencies]`, append after the last existing entry:
```toml
x25519-dalek = { version = "2", features = ["static_secrets"] }
dashmap      = "6"
zeroize      = { version = "1", features = ["derive"] }
uuid         = { version = "1", features = ["v4"] }
subtle       = "2"
```

**Step 2: Verify it compiles (no test yet — dependency resolution only)**
```powershell
cd rust_core; cargo check 2>&1
```
Expected output (last line):
```
Finished `dev` profile [unoptimized + debuginfo] target(s) in ...
```
Any `error[E...]` here means a version conflict — fix the version string before continuing.

---

### Task 2 — Write failing test: DEK derivation from X25519 ECDH + HKDF-SHA256

**Step 1: Add `#[cfg(test)]` block to `rust_core/src/memory.rs`**

Append at the bottom of the file (below `register()`):
```rust
#[cfg(test)]
mod tests {
    use super::*;
    use x25519_dalek::{EphemeralSecret, PublicKey, StaticSecret};
    use hkdf::Hkdf;
    use sha2::Sha256;

    fn make_owner_keypair() -> (StaticSecret, PublicKey) {
        let secret = StaticSecret::random_from_rng(rand_core::OsRng);
        let public = PublicKey::from(&secret);
        (secret, public)
    }

    #[test]
    fn test_dek_derivation_deterministic() {
        // Given the same owner pubkey + eph privkey → DEK must be identical both times
        let (owner_secret, owner_pubkey) = make_owner_keypair();
        let eph_secret = EphemeralSecret::random_from_rng(rand_core::OsRng);
        let eph_pubkey = PublicKey::from(&eph_secret);

        let shared1 = eph_secret.diffie_hellman(&owner_pubkey);

        // Re-derive from owner side (owner_secret × eph_pubkey = same shared secret)
        let shared2 = owner_secret.diffie_hellman(&eph_pubkey);

        assert_eq!(shared1.as_bytes(), shared2.as_bytes(),
            "ECDH shared secrets must be equal (Diffie-Hellman property)");

        // HKDF expand to 32 bytes
        let block_id = uuid::Uuid::new_v4();
        let hk = Hkdf::<Sha256>::new(Some(block_id.as_bytes()), shared1.as_bytes());
        let mut dek1 = [0u8; 32];
        hk.expand(b"pyagent-dek/v1", &mut dek1).unwrap();

        let hk2 = Hkdf::<Sha256>::new(Some(block_id.as_bytes()), shared2.as_bytes());
        let mut dek2 = [0u8; 32];
        hk2.expand(b"pyagent-dek/v1", &mut dek2).unwrap();

        assert_eq!(dek1, dek2, "DEK must be the same from both sides");
        assert_ne!(dek1, [0u8; 32], "DEK must not be all-zeros");
    }
}
```

**Step 2: Run test — expect compile error (imports not yet in scope)**
```powershell
cd rust_core; cargo test memory::tests::test_dek_derivation_deterministic 2>&1
```
Expected failure:
```
error[E0433]: failed to resolve: use of undeclared crate or module `x25519_dalek`
```

---

### Task 3 — Make DEK derivation test pass: add imports to `memory.rs`

**Step 1: Add use declarations at the top of `rust_core/src/memory.rs` (after existing `use pyo3::prelude::*;`)**
```rust
use chacha20poly1305::{
    aead::{Aead, KeyInit, Payload},
    ChaCha20Poly1305, Key as ChaChaKey, Nonce,
};
use hkdf::Hkdf;
use sha2::Sha256;
use x25519_dalek::{EphemeralSecret, PublicKey as X25519PublicKey};
use rand_core::OsRng;
use uuid::Uuid;
use subtle::ConstantTimeEq;
use zeroize::Zeroize;
use std::collections::HashMap;
```

**Step 2: Run the test — expect it to pass**
```powershell
cd rust_core; cargo test memory::tests::test_dek_derivation_deterministic 2>&1
```
Expected output:
```
test memory::tests::test_dek_derivation_deterministic ... ok
```

---

### Task 4 — Write failing test: `EncryptedMemoryBlock` put/get roundtrip

**Step 1: Add test inside the `tests` block already opened in Task 2**
```rust
    #[test]
    fn test_encrypted_block_put_get_roundtrip() {
        let (_owner_secret, owner_pubkey) = make_owner_keypair();
        let mut block = EncryptedMemoryBlock::new(owner_pubkey.as_bytes())
            .expect("block allocation must succeed");

        let entry_id = Uuid::new_v4().to_string();
        let plaintext = b"agent private state";

        block.put_raw(&entry_id, plaintext).expect("put must succeed");
        let recovered = block.get_raw(&entry_id).expect("get must succeed");

        assert_eq!(recovered, plaintext, "roundtrip must recover exact plaintext");
    }
```

**Step 2: Run — expect compile error (struct does not exist yet)**
```powershell
cd rust_core; cargo test memory::tests::test_encrypted_block_put_get_roundtrip 2>&1
```
Expected:
```
error[E0422]: cannot find struct, variant or union type `EncryptedMemoryBlock`
```

---

### Task 5 — Implement `EncryptedMemoryBlock`: struct + `new` + `put_raw` + `get_raw`

**Step 1: Add structs and non-pyclass impl block to `rust_core/src/memory.rs`** (insert before the `register` function):

```rust
const WARM_SLAB:  usize = 1  * 1024 * 1024;  //  1 MB
const SLAB_SIZE:  usize = 10 * 1024 * 1024;  // 10 MB

#[derive(Clone)]
struct SlabPtr { slab_idx: usize, offset: usize, len: usize }

pub struct EncryptedMemoryBlock {
    block_id:          Uuid,
    owner_fingerprint: [u8; 32],      // SHA-256(owner_pubkey)
    eph_pubkey:        [u8; 32],       // stored so owner can re-derive DEK offline
    dek:               ChaChaKey,      // heap-only; zeroed on drop
    slabs:             Vec<Vec<u8>>,   // [warm(1MB), growth(10MB), …]
    directory:         HashMap<Uuid, SlabPtr>,
    write_cursor:      (usize, usize), // (slab_idx, byte_offset)
    dead_bytes:        usize,          // bytes from purge()d entries (compaction trigger)
}

impl Drop for EncryptedMemoryBlock {
    fn drop(&mut self) {
        self.dek.zeroize();
        for slab in &mut self.slabs {
            slab.zeroize();
        }
    }
}

impl EncryptedMemoryBlock {
    pub fn new(owner_pubkey_bytes: &[u8]) -> Result<Self, String> {
        if owner_pubkey_bytes.len() != 32 {
            return Err("owner_pubkey must be 32 bytes (X25519)".into());
        }
        let owner_pubkey_arr: [u8; 32] = owner_pubkey_bytes.try_into().unwrap();
        let owner_pubkey = X25519PublicKey::from(owner_pubkey_arr);

        // Ephemeral ECDH
        let eph_secret  = EphemeralSecret::random_from_rng(OsRng);
        let eph_pub     = X25519PublicKey::from(&eph_secret);
        let shared      = eph_secret.diffie_hellman(&owner_pubkey);

        // HKDF-SHA256 → 32-byte DEK
        let block_id = Uuid::new_v4();
        let hk = Hkdf::<Sha256>::new(Some(block_id.as_bytes()), shared.as_bytes());
        let mut dek_bytes = [0u8; 32];
        hk.expand(b"pyagent-dek/v1", &mut dek_bytes)
            .map_err(|e| format!("HKDF expand failed: {e}"))?;
        let dek = *ChaChaKey::from_slice(&dek_bytes);
        dek_bytes.zeroize();

        // SHA-256 fingerprint
        use sha2::Digest;
        let owner_fingerprint: [u8; 32] = sha2::Sha256::digest(owner_pubkey_bytes).into();

        let mut warm_slab = Vec::with_capacity(WARM_SLAB);
        warm_slab.resize(WARM_SLAB, 0u8);

        Ok(Self {
            block_id,
            owner_fingerprint,
            eph_pubkey: *eph_pub.as_bytes(),
            dek,
            slabs: vec![warm_slab],
            directory: HashMap::new(),
            write_cursor: (0, 0),
            dead_bytes: 0,
        })
    }

    /// Encrypt `plaintext` with DEK and append to slabs.
    pub fn put_raw(&mut self, entry_id_str: &str, plaintext: &[u8]) -> Result<(), String> {
        let entry_id = Uuid::parse_str(entry_id_str)
            .map_err(|e| format!("invalid UUID: {e}"))?;
        let cipher  = ChaCha20Poly1305::new(&self.dek);
        // 12-byte nonce from entry UUID (first 12 bytes)
        let nonce_bytes: [u8; 12] = entry_id.as_bytes()[..12].try_into().unwrap();
        let nonce = Nonce::from(nonce_bytes);
        let ciphertext = cipher.encrypt(&nonce, plaintext)
            .map_err(|e| format!("encrypt failed: {e}"))?;

        let clen = ciphertext.len();
        // Grow if needed
        let (si, off) = self.write_cursor;
        if off + clen > self.slabs[si].len() {
            let mut new_slab = Vec::with_capacity(SLAB_SIZE);
            new_slab.resize(SLAB_SIZE, 0u8);
            self.slabs.push(new_slab);
            self.write_cursor = (self.slabs.len() - 1, 0);
        }
        let (si, off) = self.write_cursor;
        self.slabs[si][off..off + clen].copy_from_slice(&ciphertext);
        self.directory.insert(entry_id, SlabPtr { slab_idx: si, offset: off, len: clen });
        self.write_cursor = (si, off + clen);
        Ok(())
    }

    /// Decrypt and return plaintext for `entry_id`.
    pub fn get_raw(&self, entry_id_str: &str) -> Result<Vec<u8>, String> {
        let entry_id = Uuid::parse_str(entry_id_str)
            .map_err(|e| format!("invalid UUID: {e}"))?;
        let ptr = self.directory.get(&entry_id)
            .ok_or_else(|| "entry not found".to_string())?;
        let ciphertext = &self.slabs[ptr.slab_idx][ptr.offset..ptr.offset + ptr.len];
        let cipher = ChaCha20Poly1305::new(&self.dek);
        let nonce_bytes: [u8; 12] = entry_id.as_bytes()[..12].try_into().unwrap();
        let nonce = Nonce::from(nonce_bytes);
        cipher.decrypt(&nonce, ciphertext)
            .map_err(|e| format!("decrypt failed: {e}"))
    }
}
```

**Step 2: Run failing test → expect it to pass**
```powershell
cd rust_core; cargo test memory::tests::test_encrypted_block_put_get_roundtrip 2>&1
```
Expected:
```
test memory::tests::test_encrypted_block_put_get_roundtrip ... ok
```

---

### Task 6 — Write failing test: warm slab used, then overflow triggers new slab

**Step 1: Add test inside `tests` block**
```rust
    #[test]
    fn test_slab_growth_on_overflow() {
        let (_owner_secret, owner_pubkey) = make_owner_keypair();
        let mut block = EncryptedMemoryBlock::new(owner_pubkey.as_bytes()).unwrap();

        assert_eq!(block.slab_count(), 1, "start with one warm slab");

        // Fill the warm slab beyond 1 MB with many entries (each ~4 KB + AEAD tag)
        let entry = vec![0xABu8; 4096];
        let entries_to_overflow = (WARM_SLAB / (4096 + 16)) + 5;  // +16 AEAD tag
        let mut ids = Vec::new();
        for _ in 0..entries_to_overflow {
            let id = Uuid::new_v4().to_string();
            block.put_raw(&id, &entry).expect("put must not error");
            ids.push(id);
        }
        assert!(block.slab_count() >= 2, "must have grown to at least 2 slabs");

        // All entries must still be recoverable
        for id in &ids {
            let recovered = block.get_raw(id).expect("get must not error");
            assert_eq!(recovered, entry);
        }
    }
```

**Step 2: Run — expect failure (compile error: `slab_count` method missing)**
```powershell
cd rust_core; cargo test memory::tests::test_slab_growth_on_overflow 2>&1
```
Expected:
```
error[E0599]: no method named `slab_count` found for struct `EncryptedMemoryBlock`
```

---

### Task 7 — Implement `slab_count` and `used_bytes` on `EncryptedMemoryBlock`

**Step 1: Add two methods inside the `impl EncryptedMemoryBlock` block (after `get_raw`)**
```rust
    pub fn slab_count(&self) -> usize {
        self.slabs.len()
    }

    pub fn used_bytes(&self) -> usize {
        self.write_cursor.0 * SLAB_SIZE + self.write_cursor.1
    }
```

**Step 2: Run both passing tests**
```powershell
cd rust_core; cargo test memory::tests 2>&1
```
Expected:
```
test memory::tests::test_dek_derivation_deterministic ... ok
test memory::tests::test_encrypted_block_put_get_roundtrip ... ok
test memory::tests::test_slab_growth_on_overflow ... ok
```

---

### Task 8 — Write failing test: `purge` zero-fills ciphertext, then `get` returns error

**Step 1: Add test**
```rust
    #[test]
    fn test_purge_removes_entry() {
        let (_owner_secret, owner_pubkey) = make_owner_keypair();
        let mut block = EncryptedMemoryBlock::new(owner_pubkey.as_bytes()).unwrap();
        let id = Uuid::new_v4().to_string();
        block.put_raw(&id, b"secret data").expect("put must succeed");
        assert!(block.get_raw(&id).is_ok(), "entry must be present before purge");
        block.purge(&id).expect("purge must succeed");
        assert!(block.get_raw(&id).is_err(), "entry must be gone after purge");
    }
```

**Step 2: Run — expect compile error**
```powershell
cd rust_core; cargo test memory::tests::test_purge_removes_entry 2>&1
```
Expected:
```
error[E0599]: no method named `purge` found for struct `EncryptedMemoryBlock`
```

---

### Task 9 — Implement `purge` on `EncryptedMemoryBlock`

**Step 1: Add method inside `impl EncryptedMemoryBlock`**
```rust
    /// Zero-fill ciphertext bytes in slab, remove from directory, track dead bytes.
    pub fn purge(&mut self, entry_id_str: &str) -> Result<(), String> {
        let entry_id = Uuid::parse_str(entry_id_str)
            .map_err(|e| format!("invalid UUID: {e}"))?;
        let ptr = self.directory.remove(&entry_id)
            .ok_or_else(|| "entry not found".to_string())?;
        // Zero-fill the ciphertext region
        self.slabs[ptr.slab_idx][ptr.offset..ptr.offset + ptr.len].zeroize();
        self.dead_bytes += ptr.len;
        Ok(())
    }
```

**Step 2: Run all memory tests**
```powershell
cd rust_core; cargo test memory::tests 2>&1
```
Expected:
```
test memory::tests::test_dek_derivation_deterministic    ... ok
test memory::tests::test_encrypted_block_put_get_roundtrip ... ok
test memory::tests::test_slab_growth_on_overflow         ... ok
test memory::tests::test_purge_removes_entry             ... ok
```

---

### Task 10 — Write failing test: `MemoryBlockRegistry` allocate / get / release

**Step 1: Add test**
```rust
    #[test]
    fn test_registry_allocate_get_release() {
        use x25519_dalek::StaticSecret;
        let secret  = StaticSecret::random_from_rng(OsRng);
        let pubkey  = X25519PublicKey::from(&secret);

        let registry = MemoryBlockRegistry::new();
        let block_id = registry.allocate(pubkey.as_bytes()).expect("allocate must succeed");
        assert!(!block_id.is_empty());

        // Can write through registry reference
        {
            let mut block = registry.get_block_mut(pubkey.as_bytes()).expect("block must exist");
            let id = Uuid::new_v4().to_string();
            block.put_raw(&id, b"test").expect("put must succeed");
        }

        // Release must succeed
        registry.release(pubkey.as_bytes()).expect("release must succeed");

        // After release, get_block must fail
        assert!(registry.get_block_mut(pubkey.as_bytes()).is_err(),
            "block must be gone after release");
    }
```

**Step 2: Run — expect compile error**
```powershell
cd rust_core; cargo test memory::tests::test_registry_allocate_get_release 2>&1
```
Expected:
```
error[E0422]: cannot find struct `MemoryBlockRegistry`
```

---

### Task 11 — Implement `MemoryBlockRegistry` (lock-free DashMap)

**Step 1: Add additional imports at the top of `memory.rs` (supplement imports from Task 3)**
```rust
use dashmap::DashMap;
use sha2::Digest as Sha2Digest;
use std::sync::Arc;
```

**Step 2: Add struct and impl below `EncryptedMemoryBlock`'s impl block**
```rust
pub struct MemoryBlockRegistry {
    pub(crate) blocks: DashMap<[u8; 32], EncryptedMemoryBlock>,
}

impl MemoryBlockRegistry {
    pub fn new() -> Self {
        Self { blocks: DashMap::new() }
    }

    fn fingerprint(owner_pubkey_bytes: &[u8]) -> Result<[u8; 32], String> {
        if owner_pubkey_bytes.len() != 32 {
            return Err("owner_pubkey must be 32 bytes".into());
        }
        let fp: [u8; 32] = sha2::Sha256::digest(owner_pubkey_bytes).into();
        Ok(fp)
    }

    pub fn allocate(&self, owner_pubkey_bytes: &[u8]) -> Result<String, String> {
        let fp    = Self::fingerprint(owner_pubkey_bytes)?;
        let block = EncryptedMemoryBlock::new(owner_pubkey_bytes)?;
        let id    = block.block_id.to_string();
        self.blocks.insert(fp, block);
        Ok(id)
    }

    pub fn get_block_mut<'a>(
        &'a self,
        owner_pubkey_bytes: &[u8],
    ) -> Result<dashmap::mapref::one::RefMut<'a, [u8; 32], EncryptedMemoryBlock>, String> {
        let fp = Self::fingerprint(owner_pubkey_bytes)?;
        self.blocks.get_mut(&fp)
            .ok_or_else(|| "block not found".to_string())
    }

    pub fn release(&self, owner_pubkey_bytes: &[u8]) -> Result<(), String> {
        let fp = Self::fingerprint(owner_pubkey_bytes)?;
        self.blocks.remove(&fp)
            .ok_or_else(|| "block not found".to_string())?;
        Ok(())
    }

    pub fn total_used_bytes(&self) -> usize {
        self.blocks.iter().map(|r| r.used_bytes()).sum()
    }
}
```

**Step 3: Run test**
```powershell
cd rust_core; cargo test memory::tests::test_registry_allocate_get_release 2>&1
```
Expected:
```
test memory::tests::test_registry_allocate_get_release ... ok
```

---

### Task 12 — Write failing test: cross-agent isolation (wrong key → different bucket)

**Step 1: Add test**
```rust
    #[test]
    fn test_cross_agent_isolation() {
        use x25519_dalek::StaticSecret;
        use sha2::Digest;
        let secret_a = StaticSecret::random_from_rng(OsRng);
        let pubkey_a = X25519PublicKey::from(&secret_a);
        let secret_b = StaticSecret::random_from_rng(OsRng);
        let pubkey_b = X25519PublicKey::from(&secret_b);

        let registry = MemoryBlockRegistry::new();
        registry.allocate(pubkey_a.as_bytes()).expect("allocate A");
        registry.allocate(pubkey_b.as_bytes()).expect("allocate B");

        // Fingerprints must be distinct
        let fp_a: [u8; 32] = sha2::Sha256::digest(pubkey_a.as_bytes()).into();
        let fp_b: [u8; 32] = sha2::Sha256::digest(pubkey_b.as_bytes()).into();
        assert_ne!(fp_a, fp_b, "different owners must have different fingerprints");

        // B's block is accessible by B's fingerprint
        assert!(registry.blocks.get(&fp_b).is_some());

        // A and B have distinct block_ids — no shared state
        let id_a = registry.blocks.get(&fp_a).unwrap().block_id;
        let id_b = registry.blocks.get(&fp_b).unwrap().block_id;
        assert_ne!(id_a, id_b, "A and B must have distinct isolated blocks");
    }
```

**Step 2: Run — expect pass (same module has `pub(crate) blocks`)**
```powershell
cd rust_core; cargo test memory::tests::test_cross_agent_isolation 2>&1
```
Expected:
```
test memory::tests::test_cross_agent_isolation ... ok
```

---

### Task 13 — Wire both types as `#[pyclass]` and expose via `memory::register`

**Step 1: Add `#[pyclass]` + `#[pymethods]` wrappers after `MemoryBlockRegistry`'s impl in `memory.rs`**

```rust
// ── PyO3 wrappers ────────────────────────────────────────────────────────────

#[pyclass(name = "EncryptedMemoryBlock")]
pub struct PyEncryptedMemoryBlock {
    inner: EncryptedMemoryBlock,
}

#[pymethods]
impl PyEncryptedMemoryBlock {
    pub fn put(&mut self, entry_id: &str, plaintext: &[u8]) -> PyResult<()> {
        self.inner.put_raw(entry_id, plaintext)
            .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(e))
    }
    pub fn get(&self, entry_id: &str) -> PyResult<Vec<u8>> {
        self.inner.get_raw(entry_id)
            .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(e))
    }
    pub fn purge(&mut self, entry_id: &str) -> PyResult<()> {
        self.inner.purge(entry_id)
            .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(e))
    }
    pub fn used_bytes(&self) -> PyResult<usize> { Ok(self.inner.used_bytes()) }
    pub fn slab_count(&self)  -> PyResult<usize> { Ok(self.inner.slab_count()) }
}

#[pyclass(name = "MemoryBlockRegistry")]
pub struct PyMemoryBlockRegistry {
    inner: Arc<MemoryBlockRegistry>,
}

#[pymethods]
impl PyMemoryBlockRegistry {
    #[new]
    pub fn py_new() -> Self {
        Self { inner: Arc::new(MemoryBlockRegistry::new()) }
    }

    pub fn allocate(&self, owner_pubkey: &[u8]) -> PyResult<String> {
        self.inner.allocate(owner_pubkey)
            .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(e))
    }

    pub fn release(&self, owner_pubkey: &[u8]) -> PyResult<()> {
        self.inner.release(owner_pubkey)
            .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(e))
    }

    pub fn total_used_bytes(&self) -> PyResult<usize> {
        Ok(self.inner.total_used_bytes())
    }
}
```

**Step 2: Replace the existing `register()` function at the bottom of `memory.rs`**
```rust
pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(search_vector_rust, m)?)?;
    m.add_class::<PyEncryptedMemoryBlock>()?;
    m.add_class::<PyMemoryBlockRegistry>()?;
    Ok(())
}
```

**Step 3: Build**
```powershell
cd rust_core; cargo build 2>&1
```
Expected: no errors.

---

### Task 14 — Run full memory test suite

```powershell
cd rust_core; cargo test memory 2>&1
```
Expected — all 6 tests pass:
```
test memory::tests::test_dek_derivation_deterministic      ... ok
test memory::tests::test_encrypted_block_put_get_roundtrip ... ok
test memory::tests::test_slab_growth_on_overflow           ... ok
test memory::tests::test_purge_removes_entry               ... ok
test memory::tests::test_registry_allocate_get_release     ... ok
test memory::tests::test_cross_agent_isolation             ... ok

test result: ok. 6 passed; 0 failed
```

---

### Task 15 — Build the Python extension with maturin

```powershell
cd rust_core; maturin develop --release 2>&1
```
Expected (last lines):
```
📦 Built wheel for CPython ...
🛠 Installed rust_core-...
```

---

### Task 16 — Python smoke test

**Step 1: Run inline**
```powershell
python -c "
from rust_core import MemoryBlockRegistry
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey

priv = X25519PrivateKey.generate()
pub  = priv.public_key().public_bytes_raw()  # 32 bytes

r = MemoryBlockRegistry()
block_id = r.allocate(pub)
print('block_id:', block_id)
print('total_used_bytes:', r.total_used_bytes())
r.release(pub)
print('released OK')
"
```
Expected:
```
block_id: <uuid-string>
total_used_bytes: 0
released OK
```
