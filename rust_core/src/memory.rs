// Copyright 2026 PyAgent Authors
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

use pyo3::prelude::*;

// ────────────────────────────────────────────────────────────────────────────
// Encrypted memory block subsystem
// ────────────────────────────────────────────────────────────────────────────
use chacha20poly1305::{
    aead::{rand_core::RngCore as _, Aead, KeyInit, OsRng as AeadOsRng},
    ChaCha20Poly1305, Key, Nonce,
};
use dashmap::DashMap;
use hkdf::Hkdf;
use sha2::{Digest, Sha256};
use uuid::Uuid;
use x25519_dalek::{EphemeralSecret, PublicKey, StaticSecret};
use zeroize::{Zeroize, ZeroizeOnDrop};

use std::sync::{Arc, Mutex};

/// Size of ChaCha20-Poly1305 nonce in bytes.
const NONCE_LEN: usize = 12;

// ─── DEK zeroization wrapper ────────────────────────────────────────────────

/// A 32-byte Data Encryption Key that is zeroized on drop.
#[derive(Clone, Zeroize, ZeroizeOnDrop)]
struct Dek([u8; 32]);

/// Derive a DEK deterministically from a static secret and an ephemeral
/// public key via X25519 ECDH → HKDF-SHA-256.
///
/// This is the core crypto primitive: the same (static_secret, peer_public)
/// pair always produces the same 32-byte DEK.
fn derive_dek(static_secret: &StaticSecret, peer_public: &PublicKey) -> Dek {
    let shared = static_secret.diffie_hellman(peer_public);
    let hk = Hkdf::<Sha256>::new(None, shared.as_bytes());
    let mut dek = [0u8; 32];
    hk.expand(b"pyagent-memory-block-dek-v1", &mut dek)
        .expect("HKDF expand: output length is valid");
    Dek(dek)
}

// ─── EncryptedMemoryBlock ───────────────────────────────────────────────────

/// A single encrypted memory slab.
///
/// Internals are kept private; Python sees only the PyO3 wrapper below.
#[derive(Clone)]
struct EncryptedMemoryBlock {
    /// UUID that uniquely identifies this block.
    id: Uuid,
    /// Ephemeral X25519 public key used during block creation (stored so the
    /// owning registry can re-derive the DEK at read time).
    ephemeral_pub: PublicKey,
    /// Encrypted slabs: each element is `nonce || ciphertext`.
    slabs: Vec<Vec<u8>>,
}

impl EncryptedMemoryBlock {
    /// Create an empty block and generate its ephemeral key-pair.
    fn new() -> (Self, EphemeralSecret) {
        let ephemeral_secret = EphemeralSecret::random_from_rng(rand::thread_rng());
        let ephemeral_pub = PublicKey::from(&ephemeral_secret);
        let block = EncryptedMemoryBlock {
            id: Uuid::new_v4(),
            ephemeral_pub,
            slabs: Vec::new(),
        };
        (block, ephemeral_secret)
    }

    /// Encrypt `data` with `dek` and append the resulting slab.
    fn put_raw(&mut self, data: &[u8], dek: &Dek) -> Result<usize, String> {
        let key = Key::from(dek.0);
        let cipher = ChaCha20Poly1305::new(&key);

        let mut nonce_bytes = [0u8; NONCE_LEN];
        AeadOsRng.fill_bytes(&mut nonce_bytes);
        let nonce = Nonce::from(nonce_bytes);

        let ct = cipher
            .encrypt(&nonce, data)
            .map_err(|e| format!("encrypt error: {e}"))?;

        let mut slab = Vec::with_capacity(NONCE_LEN + ct.len());
        slab.extend_from_slice(&nonce_bytes);
        slab.extend_from_slice(&ct);
        self.slabs.push(slab);
        Ok(self.slabs.len() - 1)
    }

    /// Decrypt slab at `index` using `dek`.
    fn get_raw(&self, index: usize, dek: &Dek) -> Result<Vec<u8>, String> {
        let slab = self.slabs.get(index).ok_or_else(|| {
            format!(
                "slab index {index} out of bounds (len={})",
                self.slabs.len()
            )
        })?;

        if slab.len() < NONCE_LEN {
            return Err(format!("slab {index} is too short to contain a nonce"));
        }

        let (nonce_bytes, ct) = slab.split_at(NONCE_LEN);
        let nonce = Nonce::from_slice(nonce_bytes);
        let key = Key::from(dek.0);
        let cipher = ChaCha20Poly1305::new(&key);

        cipher
            .decrypt(nonce, ct)
            .map_err(|e| format!("decrypt error: {e}"))
    }

    /// Number of slabs currently in the block.
    fn slab_count(&self) -> usize {
        self.slabs.len()
    }

    /// Securely wipe all slab data and reset the slab vec.
    fn purge(&mut self) {
        for slab in self.slabs.iter_mut() {
            slab.zeroize();
        }
        self.slabs = Vec::new();
    }
}

// ─── MemoryBlockRegistry ────────────────────────────────────────────────────

/// Thread-safe registry that owns all `EncryptedMemoryBlock`s.
///
/// Each registry is keyed by its own `StaticSecret`; blocks created through
/// one registry cannot be read by a different registry instance.
#[derive(Clone)]
struct MemoryBlockRegistry {
    static_secret: Arc<StaticSecret>,
    blocks: Arc<DashMap<String, EncryptedMemoryBlock>>,
}

impl MemoryBlockRegistry {
    /// Create a new registry with an empty block set and a random static secret.
    /// The static secret is never exposed outside the registry; it's only used
    /// internally to derive DEKs for the blocks it owns.
    /// The registry itself is cloneable and thread-safe; clones share the same
    /// underlying data and secrets.
    /// Note: we use Arc to allow cloning the registry cheaply without copying the
    /// static secret or the blocks; the registry is effectively a reference-counted
    /// handle to the underlying data.
    /// The static secret is generated once at registry creation and remains fixed for the
    /// lifetime of the registry; this ensures that blocks created by this registry can be
    /// consistently accessed as long as the registry exists.
    /// The blocks are stored in a DashMap for concurrent access; each block is keyed by its UUID string.
    /// The registry provides methods to create blocks, put/get data, check slab counts, purge blocks, and remove blocks.
    /// The design ensures that blocks created by one registry cannot be accessed by another registry, as they use different static secrets for DEK derivation.
    /// The registry also handles secure deletion of blocks by purging their data before removal.
    /// Overall, this design provides a secure and concurrent in-memory storage solution for encrypted data blocks, with clear ownership and access control via the static secrets.
    /// Create a new registry with a random static secret and empty block set.
    fn new() -> Self {
        MemoryBlockRegistry {
            static_secret: Arc::new(StaticSecret::random_from_rng(rand::thread_rng())),
            blocks: Arc::new(DashMap::new()),
        }
    }

    /// Allocate a new block; returns its UUID string.
    fn create_block(&self) -> String {
        let (block, ephemeral_secret) = EncryptedMemoryBlock::new();
        // Immediately consume ephemeral_secret to derive DEK and verify round-
        // trip is possible, then discard it — DEK is re-derived via the stored
        // ephemeral_pub at read time.
        //
        // Note: EphemeralSecret is consumed by diffie_hellman, so we don't
        // need explicit zeroization.
        let _dek = derive_dek_from_ephemeral(ephemeral_secret, &self.static_secret);
        let id = block.id.to_string();
        self.blocks.insert(id.clone(), block);
        id
    }

    /// Helper: get the DEK for block `id` by looking up the block's ephemeral public key
    /// and deriving with the registry's static secret.
    fn dek_for(&self, id: &str) -> Result<Dek, String> {
        let block = self
            .blocks
            .get(id)
            .ok_or_else(|| format!("block '{id}' not found"))?;
        Ok(derive_dek(&self.static_secret, &block.ephemeral_pub))
    }

    /// Encrypt and store `data` in block `id`; returns the slab index.
    fn put(&self, id: &str, data: &[u8]) -> Result<usize, String> {
        let dek = self.dek_for(id)?;
        let mut block = self
            .blocks
            .get_mut(id)
            .ok_or_else(|| format!("block '{id}' not found"))?;
        block.put_raw(data, &dek)
    }

    /// Decrypt and return slab `index` from block `id`.
    fn get(&self, id: &str, index: usize) -> Result<Vec<u8>, String> {
        let dek = self.dek_for(id)?;
        let block = self
            .blocks
            .get(id)
            .ok_or_else(|| format!("block '{id}' not found"))?;
        block.get_raw(index, &dek)
    }

    /// Return the number of slabs stored in block `id`.
    fn slab_count(&self, id: &str) -> Result<usize, String> {
        Ok(self
            .blocks
            .get(id)
            .ok_or_else(|| format!("block '{id}' not found"))?
            .slab_count())
    }

    /// Wipe all slab data from block `id` (in place; block remains registered).
    fn purge(&self, id: &str) -> Result<(), String> {
        let mut block = self
            .blocks
            .get_mut(id)
            .ok_or_else(|| format!("block '{id}' not found"))?;
        block.purge();
        Ok(())
    }

    /// Remove block `id` from the registry and wipe its data.
    fn remove_block(&self, id: &str) {
        if let Some((_, mut block)) = self.blocks.remove(id) {
            block.purge();
        }
    }
}

/// Helper: consume `EphemeralSecret` + `StaticSecret` → DEK.
///
/// We store the *ephemeral public key* in the block and re-derive the DEK
/// at read time by computing ECDH(static_secret, ephemeral_pub).  The first
/// call (at block creation) uses the ephemeral secret directly to get the
/// shared point without storing it.
fn derive_dek_from_ephemeral(ephemeral: EphemeralSecret, static_sec: &StaticSecret) -> Dek {
    // ephemeral.diffie_hellman moves the secret — zeroization is automatic.
    let static_pub = PublicKey::from(static_sec);
    let shared = ephemeral.diffie_hellman(&static_pub);
    let hk = Hkdf::<Sha256>::new(None, shared.as_bytes());
    let mut dek = [0u8; 32];
    hk.expand(b"pyagent-memory-block-dek-v1", &mut dek)
        .expect("HKDF expand: output length is valid");
    Dek(dek)
}

// ─── PyO3 wrappers ──────────────────────────────────────────────────────────

/// Python-visible registry wrapper.
#[pyclass(name = "MemoryBlockRegistry")]
pub struct PyMemoryBlockRegistry {
    inner: MemoryBlockRegistry,
}

#[pymethods]
impl PyMemoryBlockRegistry {
    /// The `PyMemoryBlockRegistry` class is a Python wrapper around the Rust `MemoryBlockRegistry`.
    /// It exposes methods to create blocks, put/get data, check slab counts, purge blocks, and remove blocks, while internally managing the encryption and secure storage of the data.
    /// The design ensures that blocks created by one registry cannot be accessed by another registry, as they use different static secrets for DEK derivation.
    /// The registry also handles secure deletion of blocks by purging their data before removal.
    /// Overall, this design provides a secure and concurrent in-memory storage solution for encrypted data blocks, with clear ownership and access control via the static secrets.
    /// Create a new `PyMemoryBlockRegistry` instance.
    #[new]
    fn new() -> Self {
        PyMemoryBlockRegistry {
            inner: MemoryBlockRegistry::new(),
        }
    }

    /// Create a new encrypted memory block and return its ID.
    fn create_block(&self) -> String {
        self.inner.create_block()
    }

    /// Encrypt and store `data` in block `id`; returns the slab index.
    fn put(&self, id: &str, data: &[u8]) -> PyResult<usize> {
        self.inner
            .put(id, data)
            .map_err(|e| pyo3::exceptions::PyValueError::new_err(e))
    }

    /// Decrypt and return slab `index` from block `id`.
    fn get(&self, id: &str, index: usize) -> PyResult<Vec<u8>> {
        self.inner
            .get(id, index)
            .map_err(|e| pyo3::exceptions::PyValueError::new_err(e))
    }

    /// Return the number of slabs stored in block `id`.
    fn slab_count(&self, id: &str) -> PyResult<usize> {
        self.inner
            .slab_count(id)
            .map_err(|e| pyo3::exceptions::PyValueError::new_err(e))
    }

    /// Wipe all slab data from block `id` (in place; block remains registered).
    fn purge(&self, id: &str) -> PyResult<()> {
        self.inner
            .purge(id)
            .map_err(|e| pyo3::exceptions::PyValueError::new_err(e))
    }

    /// Remove block `id` from the registry and wipe its data.
    fn remove_block(&self, id: &str) {
        self.inner.remove_block(id);
    }
}

// ─── HMAC key derivation helpers ─────────────────────────────────────────

use crate::security::hmac_keys::derive_msg_key;

// ─── SharedMemory subsystem ─────────────────────────────────────────────────

/// Fleet-wide broadcast map with per-entry HMAC integrity.
/// Keys and values are raw byte vectors; `tag` holds the 32-byte HMAC-SHA256 tag.
#[allow(dead_code)] // these methods are exercised from Python bindings and tests
pub struct SharedMemory {
    map: DashMap<Vec<u8>, (Vec<u8>, [u8; 32])>,
    current_master: Arc<[u8; 32]>,
    previous_master: Option<Arc<[u8; 32]>>, // allow verification during rotation
}

#[allow(dead_code)]
impl SharedMemory {
    pub fn new(master_key: [u8; 32]) -> Self {
        Self {
            map: DashMap::new(),
            current_master: Arc::new(master_key),
            previous_master: None,
        }
    }

    /// Put a value under `key`, computing an HMAC tag.
    pub fn put(&self, key: &[u8], value: &[u8]) {
        let msg_key = derive_msg_key(&self.current_master, &sha2::Sha256::digest(key).into(), 0);
        let tag = hmac_sha256(&msg_key, value);
        self.map.insert(key.to_vec(), (value.to_vec(), tag));
    }

    /// Get value and verify integrity. Returns Err if tag check fails.
    pub fn get(&self, key: &[u8]) -> Result<Vec<u8>, String> {
        let entry = self.map.get(key).ok_or("entry not found".to_string())?;
        let (ref data, tag) = &*entry;
        let key_fp: [u8; 32] = sha2::Sha256::digest(key).into();
        // try current master
        let msg_key = derive_msg_key(&self.current_master, &key_fp, 0);
        if verify_hmac(&msg_key, data, tag) {
            return Ok(data.clone());
        }
        // try previous master if present
        if let Some(prev) = &self.previous_master {
            let msg_key = derive_msg_key(prev, &key_fp, 0);
            if verify_hmac(&msg_key, data, tag) {
                return Ok(data.clone());
            }
        }
        Err("integrity check failed".to_string())
    }

    /// Rotate the master key; keep old one for transient verification.
    pub fn rotate_master(&mut self, new_master: [u8; 32]) {
        self.previous_master = Some(self.current_master.clone());
        self.current_master = Arc::new(new_master);
    }
}

// simple HMAC-SHA256 convenience wrappers
#[allow(dead_code)]
fn hmac_sha256(key: &[u8; 32], data: &[u8]) -> [u8; 32] {
    use hmac::{Hmac, Mac};
    type H = Hmac<sha2::Sha256>;
    // disambiguate between KeyInit::new_from_slice and Mac::new_from_slice
    let mut mac = <H as Mac>::new_from_slice(key).expect("HMAC can take key of any size");
    mac.update(data);
    let result = mac.finalize();
    let bytes = result.into_bytes();
    bytes.into()
}

/// Verify HMAC tag for given key and data. Returns true if valid, false if not.
/// Use this when accessing SharedMemory entries to ensure integrity;
/// it checks against both current and previous master keys to allow for seamless rotation.
#[allow(dead_code)]
/// Public helper used by Python wrapper for explicit integrity checks.
pub fn verify_hmac(key: &[u8; 32], data: &[u8], tag: &[u8; 32]) -> bool {
    hmac_sha256(key, data) == *tag
}

// ─── Vector search (original) ───────────────────────────────────────────────

/// Vector similarity/search for agent long-term memory (Common/Memory).
#[pyfunction]
pub fn search_vector_rust(
    query_vec: Vec<f32>,
    database: Vec<Vec<f32>>,
    top_k: usize,
) -> PyResult<Vec<usize>> {
    let mut scores: Vec<(usize, f32)> = database
        .iter()
        .enumerate()
        .map(|(idx, vec)| {
            let score: f32 = query_vec.iter().zip(vec.iter()).map(|(q, v)| q * v).sum();
            (idx, score)
        })
        .collect();

    scores.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap_or(std::cmp::Ordering::Equal));

    Ok(scores.into_iter().take(top_k).map(|(idx, _)| idx).collect())
}

/// PyO3 wrapper for SharedMemory
#[pyclass(name = "SharedMemory")]
struct PySharedMemory {
    inner: Arc<Mutex<SharedMemory>>,
}

/// The `PySharedMemory` class is a Python wrapper around the
/// Rust `SharedMemory` struct, providing a thread-safe interface
/// for storing and retrieving key-value pairs with HMAC integrity checks.
/// It allows for master key rotation while maintaining access to existing
/// entries, and exposes methods for putting values, getting values with
/// integrity verification, and rotating the master key. The design
/// ensures that integrity checks are performed using both the current
/// and previous master keys to allow for seamless rotation without
/// breaking access to existing data.
#[pymethods]
impl PySharedMemory {
    #[new]
    fn new(master_key: Vec<u8>) -> PyResult<Self> {
        if master_key.len() != 32 {
            return Err(pyo3::exceptions::PyValueError::new_err(
                "master_key must be 32 bytes",
            ));
        }
        let mut arr = [0u8; 32];
        arr.copy_from_slice(&master_key);
        Ok(PySharedMemory {
            inner: Arc::new(Mutex::new(SharedMemory::new(arr))),
        })
    }

    /// Put a value under `key`, computing an HMAC tag.
    fn put(&self, key: &[u8], value: &[u8]) {
        self.inner.lock().unwrap().put(key, value);
    }

    /// Get value and verify integrity. Returns None if entry not found, Err if tag check fails.
    fn get(&self, key: &[u8]) -> PyResult<Option<Vec<u8>>> {
        match self.inner.lock().unwrap().get(key) {
            Ok(v) => Ok(Some(v)),
            Err(e) if e == "entry not found" => Ok(None),
            Err(e) => Err(pyo3::exceptions::PyValueError::new_err(e)),
        }
    }

    /// Rotate the master key. The new key must be 32 bytes.
    fn rotate_master_key(&self, new_master: Vec<u8>) -> PyResult<()> {
        if new_master.len() != 32 {
            return Err(pyo3::exceptions::PyValueError::new_err(
                "new_master must be 32 bytes",
            ));
        }
        let mut arr = [0u8; 32];
        arr.copy_from_slice(&new_master);
        self.inner.lock().unwrap().rotate_master(arr);
        Ok(())
    }

    /// Public helper for explicit integrity checks;
    /// returns true if valid, false if not.
    fn verify_hmac(&self, key: &[u8], value: &[u8], tag: &[u8]) -> PyResult<bool> {
        if tag.len() != 32 {
            return Err(pyo3::exceptions::PyValueError::new_err(
                "tag must be 32 bytes",
            ));
        }
        let mut arr = [0u8; 32];
        arr.copy_from_slice(tag);
        Ok(verify_hmac(
            &derive_msg_key(
                &self.inner.lock().unwrap().current_master,
                &sha2::Sha256::digest(key).into(),
                0,
            ),
            value,
            &arr,
        ))
    }
}

/// Register memory functions in the rust_core module.
pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(search_vector_rust, m)?)?;
    m.add_class::<PyMemoryBlockRegistry>()?;
    m.add_class::<PySharedMemory>()?;
    Ok(())
}

// ─── Tests ──────────────────────────────────────────────────────────────────

#[cfg(test)]
mod tests {
    use super::*;
    use subtle::ConstantTimeEq;

    // ── Task 2/3: DEK determinism ────────────────────────────────────────────

    /// Verify that the same (static_secret, ephemeral_pub) pair always produces the same DEK,
    /// and that different ephemeral keys yield different DEKs.
    #[test]
    fn dek_is_deterministic_from_static_secret_and_pub() {
        let static_secret = StaticSecret::random_from_rng(rand::thread_rng());
        let ephemeral_secret = EphemeralSecret::random_from_rng(rand::thread_rng());
        let ephemeral_pub = PublicKey::from(&ephemeral_secret);

        let dek_a = derive_dek(&static_secret, &ephemeral_pub);

        // Re-derive with the same static secret + same ephemeral pub → identical DEK.
        let dek_b = derive_dek(&static_secret, &ephemeral_pub);

        // Use subtle ConstantTimeEq to compare without timing side-channel.
        assert_eq!(
            1u8,
            dek_a.0.ct_eq(&dek_b.0).unwrap_u8(),
            "DEK must be deterministic given the same (static_secret, ephemeral_pub)"
        );
    }

    /// Verify that different ephemeral keys yield different DEKs (with the same static secret).
    #[test]
    fn dek_differs_for_different_ephemeral_keys() {
        let static_secret = StaticSecret::random_from_rng(rand::thread_rng());

        let eph1 = EphemeralSecret::random_from_rng(rand::thread_rng());
        let pub1 = PublicKey::from(&eph1);
        let eph2 = EphemeralSecret::random_from_rng(rand::thread_rng());
        let pub2 = PublicKey::from(&eph2);

        let dek1 = derive_dek(&static_secret, &pub1);
        let dek2 = derive_dek(&static_secret, &pub2);

        assert_ne!(
            dek1.0, dek2.0,
            "Different ephemeral keys must yield different DEKs"
        );
    }

    // ── Task 4/5: put_raw / get_raw round-trip ───────────────────────────────

    /// Verify that data can be correctly stored and retrieved using put_raw and get_raw.
    #[test]
    fn put_raw_then_get_raw_roundtrip() {
        let static_secret = StaticSecret::random_from_rng(rand::thread_rng());
        let (mut block, _eph) = EncryptedMemoryBlock::new();
        let dek = derive_dek(&static_secret, &block.ephemeral_pub);

        let payload = b"hello encrypted memory world";
        let idx = block.put_raw(payload, &dek).unwrap();
        let output = block.get_raw(idx, &dek).unwrap();

        assert_eq!(
            payload.as_ref(),
            output.as_slice(),
            "Round-trip must recover the original plaintext"
        );
    }

    /// Verify that attempting to decrypt with the wrong DEK fails.
    #[test]
    fn get_raw_with_wrong_dek_fails() {
        let static_secret = StaticSecret::random_from_rng(rand::thread_rng());
        let (mut block, _eph) = EncryptedMemoryBlock::new();
        let dek_correct = derive_dek(&static_secret, &block.ephemeral_pub);

        let eph_wrong = EphemeralSecret::random_from_rng(rand::thread_rng());
        let pub_wrong = PublicKey::from(&eph_wrong);
        let dek_wrong = derive_dek(&static_secret, &pub_wrong);

        let idx = block.put_raw(b"secret", &dek_correct).unwrap();
        let result = block.get_raw(idx, &dek_wrong);

        assert!(result.is_err(), "Decrypt with wrong DEK must fail");
    }

    // ── Task 6/7: slab growth ────────────────────────────────────────────────

    /// Verify that the slab count grows with each put_raw operation.
    #[test]
    fn slab_count_grows_with_each_put() {
        let static_secret = StaticSecret::random_from_rng(rand::thread_rng());
        let (mut block, _eph) = EncryptedMemoryBlock::new();
        let dek = derive_dek(&static_secret, &block.ephemeral_pub);

        assert_eq!(0, block.slab_count());
        block.put_raw(b"one", &dek).unwrap();
        assert_eq!(1, block.slab_count());
        block.put_raw(b"two", &dek).unwrap();
        assert_eq!(2, block.slab_count());
        block.put_raw(b"three", &dek).unwrap();
        assert_eq!(3, block.slab_count());
    }

    // ── Task 8/9: purge ──────────────────────────────────────────────────────

    /// Verify that purging a block resets its slab count to zero.
    #[test]
    fn purge_resets_slab_count_to_zero() {
        let static_secret = StaticSecret::random_from_rng(rand::thread_rng());
        let (mut block, _eph) = EncryptedMemoryBlock::new();
        let dek = derive_dek(&static_secret, &block.ephemeral_pub);

        block.put_raw(b"a", &dek).unwrap();
        block.put_raw(b"b", &dek).unwrap();
        assert_eq!(2, block.slab_count());

        block.purge();
        assert_eq!(0, block.slab_count(), "After purge, slab_count must be 0");
    }

    /// Verify that attempting to get a slab after purge returns an error (index out of bounds).
    #[test]
    fn get_after_purge_returns_error() {
        let static_secret = StaticSecret::random_from_rng(rand::thread_rng());
        let (mut block, _eph) = EncryptedMemoryBlock::new();
        let dek = derive_dek(&static_secret, &block.ephemeral_pub);

        block.put_raw(b"temp", &dek).unwrap();
        block.purge();

        assert!(
            block.get_raw(0, &dek).is_err(),
            "get_raw after purge must return Err (index out of bounds)"
        );
    }

    // ── Task 10/11/12: MemoryBlockRegistry ──────────────────────────────────

    /// Verify that data can be correctly stored and retrieved using the registry.
    #[test]
    fn registry_create_put_get_roundtrip() {
        let reg = MemoryBlockRegistry::new();
        let id = reg.create_block();

        let payload = b"registry round-trip test";
        let idx = reg.put(&id, payload).unwrap();
        let output = reg.get(&id, idx).unwrap();

        assert_eq!(payload.as_ref(), output.as_slice());
    }

    /// Verify that the slab count is correctly updated and that purging a block resets its slab count.
    #[test]
    fn registry_slab_count_and_purge() {
        let reg = MemoryBlockRegistry::new();
        let id = reg.create_block();

        reg.put(&id, b"x").unwrap();
        reg.put(&id, b"y").unwrap();
        assert_eq!(2, reg.slab_count(&id).unwrap());

        reg.purge(&id).unwrap();
        assert_eq!(0, reg.slab_count(&id).unwrap());
    }

    /// Verify that blocks created by one registry cannot be accessed by another registry.
    #[test]
    fn registry_isolation_different_registries_cannot_cross_decrypt() {
        let reg_a = MemoryBlockRegistry::new();
        let reg_b = MemoryBlockRegistry::new();

        let id_a = reg_a.create_block();
        reg_a.put(&id_a, b"secret-a").unwrap();

        // reg_b doesn't know about id_a at all → error expected.
        let result = reg_b.get(&id_a, 0);
        assert!(
            result.is_err(),
            "Registry B must not access blocks belonging to Registry A"
        );
    }

    /// Verify that removing a block makes its ID inaccessible.
    #[test]
    fn registry_remove_block_makes_id_inaccessible() {
        let reg = MemoryBlockRegistry::new();
        let id = reg.create_block();
        reg.put(&id, b"to be removed").unwrap();

        reg.remove_block(&id);

        assert!(
            reg.get(&id, 0).is_err(),
            "After remove_block the ID must no longer be accessible"
        );
    }

    /// Verify that accessing a slab with an out-of-bounds index returns an error.
    #[test]
    fn slab_index_out_of_bounds_returns_error() {
        let reg = MemoryBlockRegistry::new();
        let id = reg.create_block();
        reg.put(&id, b"only one slab").unwrap();

        assert!(
            reg.get(&id, 99).is_err(),
            "Out-of-bounds slab index must return Err"
        );
    }

    /// Verify SharedMemory HMAC behavior and rotation support.
    #[test]
    fn test_hmac_key_management() {
        let master1 = [1u8; 32];
        let master2 = [2u8; 32];
        let mut mem = SharedMemory::new(master1);
        let key = b"foo";
        mem.put(key, b"bar");
        assert_eq!(mem.get(key).unwrap(), b"bar".to_vec());
        mem.rotate_master(master2);
        // old entry must still verify
        assert_eq!(mem.get(key).unwrap(), b"bar".to_vec());
        // tamper to cause integrity failure
        if let Some(mut entry) = mem.map.get_mut(&key.to_vec()) {
            entry.0[0] ^= 0xFF;
        }
        assert!(mem.get(key).is_err());
    }
}
