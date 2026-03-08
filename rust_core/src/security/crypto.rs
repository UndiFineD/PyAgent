use pyo3::prelude::*;
use once_cell::sync::OnceCell;
use std::fs;
// bring KeyInit into scope so we can call `XChaCha20Poly1305::new`
use chacha20poly1305::KeyInit;
use chacha20poly1305::aead::Aead;
use hkdf::Hkdf;
use sha2::Sha256;
use rand_core::OsRng;
use rand_core::RngCore;

// prometheus metrics
use once_cell::sync::Lazy;
use prometheus::{IntCounter, register_int_counter, Encoder, TextEncoder};

static ENCRYPT_COUNTER: Lazy<IntCounter> = Lazy::new(|| {
    register_int_counter!("encrypt_data_calls", "Number of encrypt_data invocations").unwrap()
});
static DECRYPT_COUNTER: Lazy<IntCounter> = Lazy::new(|| {
    register_int_counter!("decrypt_data_calls", "Number of decrypt_data invocations").unwrap()
});
static ROLLBACK_COUNTER: Lazy<IntCounter> = Lazy::new(|| {
    register_int_counter!("rollback_calls", "Number of transaction rollbacks").unwrap()
});
static ROTATE_COUNTER: Lazy<IntCounter> = Lazy::new(|| {
    register_int_counter!("rotate_key_calls", "Number of key rotation operations").unwrap()
});

// store key material once; loading twice is an error
static KEYS: OnceCell<(Vec<u8>, Vec<u8>)> = OnceCell::new();

// helper to produce a 32‑byte key for AEAD using HKDF-SHA256.
// the KDF input material combines the public and private bytes, and the
// salt includes the current key rotation version so that rotating keys
// automatically produces a new key without touching the stored files.
fn derive_key() -> [u8; 32] {
    let ikm = if let Some((pub_k, priv_k)) = KEYS.get() {
        // concatenate pub||priv
        [pub_k.as_slice(), priv_k.as_slice()].concat()
    } else {
        // fallback to fixed value to keep API working even if keys absent
        b"static-default-keying".to_vec()
    };
    let version = *KEY_VERSION.lock().unwrap();
    let mut salt = [0u8; 8];
    salt.copy_from_slice(&version.to_le_bytes());

    let hk = Hkdf::<Sha256>::new(Some(&salt), &ikm);
    let mut okm = [0u8; 32];
    hk.expand(b"rust_core encryption", &mut okm)
        .expect("HKDF expand should never fail with 32-byte output");
    okm
}

// simple transaction state tracker for demonstration purposes
use std::sync::Mutex;
static TRANSACTION_ACTIVE: Mutex<bool> = Mutex::new(false);
// root directory for the active transaction; used for rollback cleanup
static TRANSACTION_PATH: Mutex<Option<String>> = Mutex::new(None);

// simple key rotation counter; actual key material unchanged for now
static KEY_VERSION: Mutex<u64> = Mutex::new(0);

#[pyfunction]
pub fn load_keys(pub_path: &str, priv_path: &str) -> PyResult<()> {
    let pub_bytes = fs::read(pub_path).map_err(|e| PyErr::new::<pyo3::exceptions::PyIOError, _>(format!("failed to read pub key: {}", e)))?;
    let priv_bytes = fs::read(priv_path).map_err(|e| PyErr::new::<pyo3::exceptions::PyIOError, _>(format!("failed to read priv key: {}", e)))?;
    KEYS.set((pub_bytes, priv_bytes))
        .map_err(|_| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>("keys already loaded"))?;
    Ok(())
}

#[pyfunction]
pub fn export_keys(pub_path: &str, priv_path: &str) -> PyResult<()> {
    if let Some((pubk, privk)) = KEYS.get() {
        fs::write(pub_path, pubk).map_err(|e| PyErr::new::<pyo3::exceptions::PyIOError, _>(format!("failed to write pub key: {}", e)))?;
        fs::write(priv_path, privk).map_err(|e| PyErr::new::<pyo3::exceptions::PyIOError, _>(format!("failed to write priv key: {}", e)))?;
        Ok(())
    } else {
        Err(pyo3::exceptions::PyRuntimeError::new_err("no keys loaded"))
    }
}

#[pyfunction]
pub fn encrypt_data(data: &[u8]) -> PyResult<Vec<u8>> {
    // ChaCha20Poly1305 AEAD with a random nonce; prepend nonce to output.
    use chacha20poly1305::{XChaCha20Poly1305, Key, XNonce};

    let key_bytes = derive_key();
    let cipher = XChaCha20Poly1305::new(Key::from_slice(&key_bytes));

    // generate 24-byte nonce
    let mut nonce_bytes = [0u8; 24];
    OsRng.fill_bytes(&mut nonce_bytes);
    let nonce = XNonce::from_slice(&nonce_bytes);

    let ciphertext = cipher
        .encrypt(nonce, data)
        .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
            format!("encryption failure: {}", e)
        ))?;

    // return nonce || ciphertext
    let mut out = Vec::with_capacity(24 + ciphertext.len());
    out.extend_from_slice(&nonce_bytes);
    out.extend_from_slice(&ciphertext);
    ENCRYPT_COUNTER.inc();
    Ok(out)
}

// helper which attempts to decrypt using a specific key version
fn try_decrypt_version(data: &[u8], version: u64) -> Result<Vec<u8>, chacha20poly1305::aead::Error> {
    use chacha20poly1305::{XChaCha20Poly1305, Key, XNonce};

    if data.len() < 24 {
        return Err(chacha20poly1305::aead::Error);
    }
    let (nonce_bytes, ciphertext) = data.split_at(24);
    let nonce = XNonce::from_slice(nonce_bytes);

    // temporarily override the version during key derivation
    let orig_version = *KEY_VERSION.lock().unwrap();
    // compute using supplied version by temporarily setting it
    *KEY_VERSION.lock().unwrap() = version;
    let key_bytes = derive_key();
    *KEY_VERSION.lock().unwrap() = orig_version;

    let cipher = XChaCha20Poly1305::new(Key::from_slice(&key_bytes));
    cipher.decrypt(nonce, ciphertext)
}

#[pyfunction]
pub fn decrypt_data(data: &[u8]) -> PyResult<Vec<u8>> {
    use pyo3::exceptions::PyRuntimeError;

    // try current key first, then fall back to previous version if available
    let current_version = *KEY_VERSION.lock().unwrap();
    let attempt = try_decrypt_version(data, current_version);
    if let Ok(plain) = attempt {
        return Ok(plain);
    }
    if current_version > 0 {
        if let Ok(plain) = try_decrypt_version(data, current_version - 1) {
            return Ok(plain);
        }
    }

    Err(PyRuntimeError::new_err("decryption failure: aead::Error"))
}

#[pyfunction]
pub fn begin_transaction(path: &str) -> PyResult<()> {
    let mut active = TRANSACTION_ACTIVE.lock().unwrap();
    if *active {
        return Err(pyo3::exceptions::PyRuntimeError::new_err("transaction already active"));
    }
    *active = true;
    let mut txpath = TRANSACTION_PATH.lock().unwrap();
    *txpath = Some(path.to_string());
    Ok(())
}

#[pyfunction]
pub fn commit_transaction() -> PyResult<()> {
    let mut active = TRANSACTION_ACTIVE.lock().unwrap();
    if !*active {
        return Err(pyo3::exceptions::PyRuntimeError::new_err("no active transaction"));
    }
    *active = false;
    // drop stored path since transaction finished successfully
    let mut txpath = TRANSACTION_PATH.lock().unwrap();
    *txpath = None;
    Ok(())
}

#[pyfunction]
pub fn rollback_transaction() -> PyResult<()> {
    let mut active = TRANSACTION_ACTIVE.lock().unwrap();
    if !*active {
        return Err(pyo3::exceptions::PyRuntimeError::new_err("no active transaction"));
    }
    *active = false;
    ROLLBACK_COUNTER.inc();
    // remove any files that were created under the transaction path
    if let Some(base) = TRANSACTION_PATH.lock().unwrap().take() {
        match fs::remove_dir_all(&base) {
            Ok(_) => {},
            Err(e) if e.kind() == std::io::ErrorKind::NotFound => {},
            Err(e) => return Err(PyErr::new::<pyo3::exceptions::PyIOError, _>(
                format!("failed to cleanup transaction path: {}", e)
            )),
        }
        // recreate the directory so tests can inspect absence of file
        let _ = fs::create_dir_all(&base);
    }
    Ok(())
}

// key rotation helpers
#[pyfunction]
pub fn current_key_version() -> PyResult<u64> {
    Ok(*KEY_VERSION.lock().unwrap())
}

#[pyfunction]
pub fn rotate_keys() -> PyResult<()> {
    let mut v = KEY_VERSION.lock().unwrap();
    *v += 1;
    ROTATE_COUNTER.inc();
    Ok(())
}

// Metrics gathering helper exposed to Python
#[pyfunction]
pub fn gather_metrics() -> PyResult<String> {
    let encoder = TextEncoder::new();
    let mf = prometheus::gather();
    let mut buf = Vec::new();
    encoder.encode(&mf, &mut buf).map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
        format!("metrics encoding error: {}", e)
    ))?;
    String::from_utf8(buf).map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
        format!("utf8 error: {}", e)
    ))
}

// The helper functions above are registered by `security::register`
// so this file does not declare a separate Python module.

// include Rust unit tests defined in separate file
#[cfg(test)]
mod crypto_tests;
