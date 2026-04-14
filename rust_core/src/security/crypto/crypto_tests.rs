// Unit tests for the security/crypto module.
// These tests roughly mirror the Python integration tests added earlier.

use super::*; // bring crypto functions into scope
use std::fs;
use tempfile::tempdir;

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn encrypt_decrypt_roundtrip() {
        // ensure Python interpreter is initialized for any pyo3 types we return
        pyo3::prepare_freethreaded_python();

        let data = b"sensitive data";
        // ensure deterministic behavior for this test by resetting global state
        *KEY_VERSION.lock().unwrap() = 0;
        *KEYS.lock().unwrap() = None;

        let enc = encrypt_data(data).expect("encrypt should succeed");
        let dec = decrypt_data(&enc).expect("decrypt failed");
        assert_eq!(dec, data);
    }

    #[test]
    fn transaction_rollback_removes_files() {
        pyo3::prepare_freethreaded_python();

        let tmp = tempdir().unwrap();
        let base = tmp.path().to_str().unwrap();

        // start transaction
        begin_transaction(base).unwrap();
        let file_path = tmp.path().join("foo.txt");
        fs::write(&file_path, b"hello").unwrap();
        assert!(file_path.exists(), "file should exist inside tx");

        // simulate error and rollback
        rollback_transaction().unwrap();
        assert!(!file_path.exists(), "file should be removed after rollback");
    }

    #[test]
    fn key_rotation_increments_version_and_preserves_data() {
        pyo3::prepare_freethreaded_python();

        let v1 = current_key_version().unwrap();
        rotate_keys().unwrap();
        let v2 = current_key_version().unwrap();
        assert_ne!(v1, v2);

        let data = b"abc";
        let enc = encrypt_data(data).unwrap();
        rotate_keys().unwrap();
        let dec = decrypt_data(&enc).expect("decrypt after rotation");
        assert_eq!(dec, data);
    }
}
