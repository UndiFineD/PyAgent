# Async Runtime Rollout
> **2026-03-10:** All synchronous loops have been eliminated; Node.js-like async infrastructure in place.
> See 2026-03-10-async-runtime-plan.md for details.

# Hybrid LLM Security Core Implementation Plan

**Goal:**
Build a security‑first rewrite of the `rust_core` library, driven by Python integration tests.
The new core will provide inline encryption/decryption, transactional file operations 
and monthly key rotation (zero‑trust/allow‑list model) with full memory‑safe Rust implementation.

**Architecture:**
- **Rust FFI bridge** (`rust_core/` crate) compiled as `cdylib` with `pyo3` bindings.
- New `security/crypto.rs` module housing encryption, transaction and key‑management routines.
- Python test layer in `rust_core/tests/` exercising every security API, 
  failing first then guiding the Rust implementation.
- Existing dynamic test generator remains, but focused tests live alongside it.

**Tech Stack:**
- Python 3.14, `pytest` for test harness
- Rust 2021 edition, `cargo build`/`cargo test` for native code
- `pyo3` for Python bindings
- CLI tools: `python -m pytest`, `cargo test`

---

### Task 1: add failing Python encryption round‑trip test

**Step 1: Write the failing test**
- File: `rust_core/tests/test_security_core.py`
- Code:
  ```python
  import pytest
  import rust_core

  def test_encrypt_decrypt_roundtrip():
      plaintext = b"sensitive data"
      # these attributes don't exist yet, so the import should raise
      assert hasattr(rust_core, "encrypt_data"), "encrypt_data missing"
      assert hasattr(rust_core, "decrypt_data"), "decrypt_data missing"

      encrypted = rust_core.encrypt_data(plaintext)
      assert isinstance(encrypted, (bytes, bytearray))
      decrypted = rust_core.decrypt_data(encrypted)
      assert decrypted == plaintext
  ```

**Step 2: run the new test and verify it fails**
- Command: `python -m pytest -q rust_core/tests/test_security_core.py::test_encrypt_decrypt_roundtrip`
- Expected output:
  ```
  E   AttributeError: module 'rust_core' has no attribute 'encrypt_data'
  ```

### Task 2: expose stub functions from Rust

**Step 1: create new Rust module with stubs**
- File: `rust_core/src/security/crypto.rs`
- Code:
  ```rust
  use pyo3::prelude::*;

  #[pyfunction]
  fn encrypt_data(data: &[u8]) -> PyResult<Vec<u8>> {
      // stub: return input unchanged
      Ok(data.to_vec())
  }

  #[pyfunction]
  fn decrypt_data(data: &[u8]) -> PyResult<Vec<u8>> {
      // stub: return input unchanged
      Ok(data.to_vec())
  }

  #[pymodule]
  fn crypto(_py: Python, m: &PyModule) -> PyResult<()> {
      m.add_function(wrap_pyfunction!(encrypt_data, m)?)?;
      m.add_function(wrap_pyfunction!(decrypt_data, m)?)?;
      Ok(())
  }
  ```

**Step 2: register module in `security.rs`**
- Locate `rust_core/src/security.rs` and add `mod crypto;` 
  plus call to `crypto::crypto(py, m)?;` inside the `#[pymodule]` initializer.

**Step 3: build the crate to ensure Rust compiles**
- Command: `cd rust_core && cargo build`
- Expected: `Finished dev [unoptimized + debuginfo] target(s) in …s` with no errors.

**Step 4: run the Python test again**
- Command: same as Task 1 Step 2
- Expected failure changes to assertion failure 
  (encrypted == plaintext but the stub satisfies the roundtrip):
  test passes, since stub returns input (so no assertion error anymore).
  If the attribute assertions still exist they pass.

### Task 3: implement minimal encryption logic in Rust

**Step 1: modify `encrypt_data`/`decrypt_data` to perform XOR with a fixed key**
- Replace stub bodies with simple reversible transformation:
  ```rust
  const KEY: u8 = 0xAA;
  let mut out = data.to_vec();
  for byte in &mut out { *byte ^= KEY; }
  Ok(out)
  ```
  and reverse the same operation in `decrypt_data`.

**Step 2: rebuild and run the Python test**
- Commands:
  ```powershell
  cd rust_core; cargo build
  cd ..; python -m pytest -q rust_core/tests/test_security_core.py::test_encrypt_decrypt_roundtrip
  ```
- Expected output: test passes (`✓`).

### Task 4: add Python test for transactional file operations

**Step 1: extend `test_security_core.py`** with new test below the previous one:
  ```python
  def test_transaction_rollback(tmp_path, monkeypatch):
      # begin_transaction/commit/rollback not yet implemented
      assert hasattr(rust_core, "begin_transaction")
      assert hasattr(rust_core, "commit_transaction")
      assert hasattr(rust_core, "rollback_transaction")

      test_file = tmp_path / "foo.txt"
      rust_core.begin_transaction(str(tmp_path))
      with pytest.raises(RuntimeError):
          # force an error inside the transaction; stub should trigger rollback
          raise RuntimeError("oops")
      rust_core.rollback_transaction()
      assert not test_file.exists(), "transaction should have rolled back"
  ```

**Step 2: run only this test**
- Command: `python -m pytest -q rust_core/tests/test_security_core.py::test_transaction_rollback`
- Expected failure: missing attributes (AttributeError) 
  or assertion error because stub unimplemented.

### Task 5: add transaction APIs in Rust

**Step 1: in `crypto.rs` add full function skeletons**
  ```rust
  use std::sync::Mutex;
  static TRANSACTION_ACTIVE: Mutex<bool> = Mutex::new(false);

  #[pyfunction]
  fn begin_transaction(path: &str) -> PyResult<()> {
      let mut flag = TRANSACTION_ACTIVE.lock().unwrap();
      *flag = true;
      // no real work yet
      Ok(())
  }

  #[pyfunction]
  fn commit_transaction() -> PyResult<()> {
      let mut flag = TRANSACTION_ACTIVE.lock().unwrap();
      if !*flag {
          return Err(pyo3::exceptions::PyRuntimeError::new_err("no active transaction"));
      }
      *flag = false;
      Ok(())
  }

  #[pyfunction]
  fn rollback_transaction() -> PyResult<()> {
      let mut flag = TRANSACTION_ACTIVE.lock().unwrap();
      *flag = false;
      // delete any temp files if we had created them
      Ok(())
  }
  ```

**Step 2: rebuild crate** and run the transaction test again
- Expect failure now from our Python error raise held inside the test, not from missing attribute.
  The assertion `not test_file.exists()` should still fail 
  because we have not created/rolled back any file yet – 
  adjust the test to create a file while transaction is active.

### Task 6: update transaction test to exercise file creation

**Step 1: modify `test_transaction_rollback`**:
  ```python
      # inside the transaction create a file
      rust_core.begin_transaction(str(tmp_path))
      f = open(tmp_path / "foo.txt", "w")
      f.write("hello")
      f.close()
      rust_core.rollback_transaction()
      assert not (tmp_path / "foo.txt").exists()
  ```

**Step 2: rerun test; verify it now fails because rollback is a no‑op.**

### Task 7: implement rollback logic in Rust

**Step 1: enhance `crypto.rs` to track created files and delete them on rollback**.
- Use a `Mutex<Vec<String>>` to record paths when `begin_transaction` is called.

**Step 2: rebuild and rerun both encryption and transaction tests; they should pass.**

### Task 8: add Python test for key rotation

**Step 1: append to `test_security_core.py`:
  ```python
  def test_key_rotation():
      assert hasattr(rust_core, "current_key_version")
      assert hasattr(rust_core, "rotate_keys")

      version1 = rust_core.current_key_version()
      rust_core.rotate_keys()
      version2 = rust_core.current_key_version()
      assert version2 != version1

      # old data should still decrypt using version1 (or raise if not supported)
      data = b"abc"
      enc = rust_core.encrypt_data(data)
      rust_core.rotate_keys()
      dec = rust_core.decrypt_data(enc)
      assert dec == data
  ```

**Step 2: run this test and observe failure from missing attrs or wrong behavior.**

### Task 9: implement key‑rotation skeleton in Rust

**Step 1: add functions `current_key_version` and `rotate_keys` to `crypto.rs`.**
- Maintain a simple `Mutex<u64>` version counter and a fixed `Vec<u8>` key for each version.

**Step 2: rebuild crate and run the key rotation test; adjust until it passes.

### Task 10: add Rust unit tests for the new functionality

**Step 1: create `rust_core/src/security/crypto_tests.rs` with `#[cfg(test)]` functions mirroring the Python tests.**
- Write Rust tests for: encryption roundtrip, transaction rollback, key rotation version increment.

**Step 2: `cd rust_core && cargo test --test crypto_tests` should initially fail; implement missing logic until they pass.

### Task 11: run full test suites

**Step 1: run Python integration tests**
- Command: `python -m pytest -q rust_core/tests/test_security_core.py`
- Expect all three tests (`encrypt_decrypt_roundtrip`, `test_transaction_rollback`, `test_key_rotation`) to pass.

**Step 2: run Rust unit tests**
- Command: `cd rust_core && cargo test`
- Expect the new `crypto_tests` plus any existing tests to pass.

### Task 12: update dynamic test generator (optional)

- Modify `rust_core/test_rust_core.py` to look for the new `encrypt_data`, `decrypt_data`, etc., ensuring they are exercised by the automatic scan.  Add explicit patterns if necessary.
- Run `python -m pytest rust_core/test_rust_core.py -q` to verify nothing regresses.

### Task 13: document new security API

- Add docstrings to the Python bindings in `crypto.rs` and update `docs/` or `README.md` with a brief description of the new security methods.
- Add entry to `Rust Security Core` section of `docs/architecture/hybrid-llm-security.md` if present.

### Task 14: integrate into CI

- Ensure the root `pytest` invocation covers `rust_core/tests/*` (it already does because of `pytest src/` configuration). Add a step in the repository’s GitHub Actions workflow (if one exists) to run `cd rust_core && cargo test` after Python tests.

### Task 15: place a safety net

- Add a `rust_core/security/atomic.rs` or similar for future transactional file operations; note in comments that the implementation must remain memory‑safe and use `StorageTransaction` support as described in design.

---

## Implementation Completeness Register (2026-03-08)

This section records current completion status against Tasks 1–15 in this plan.

### Task-by-task status

| Task | Status | Notes |
|---|---|---|
| 1 | ✅ Completed | Python roundtrip coverage exists in `rust_core/tests/security_core_test.py`. |
| 2 | ✅ Completed | Rust crypto APIs are exposed and registered in `rust_core/src/security.rs`. |
| 3 | ✅ Completed | Encryption/decryption implementation is present in `rust_core/src/security/crypto.rs` (AEAD + nonce prefix). |
| 4 | ✅ Completed | Transaction rollback test exists in `rust_core/tests/security_core_test.py`. |
| 5 | ✅ Completed | Transaction API functions implemented: `begin_transaction`, `commit_transaction`, `rollback_transaction`. |
| 6 | ✅ Completed | Transaction test exercises on-disk file creation and rollback behavior. |
| 7 | ✅ Completed | Rollback cleanup logic implemented and validated by tests. |
| 8 | ✅ Completed | Python key-rotation test exists in `rust_core/tests/security_core_test.py`. |
| 9 | ✅ Completed | Key versioning and rotation APIs implemented (`current_key_version`, `rotate_keys`). |
| 10 | ✅ Completed | Rust unit tests added at `rust_core/src/security/crypto/crypto_tests.rs` (module form). |
| 11 | ✅ Completed | Fresh verification run completed on 2026-03-08 (see evidence below). |
| 12 | ◑ Partially completed (optional) | `rust_core/test_rust_core.py` was updated, but no explicit hardcoded pattern additions for security APIs were registered. |
| 13 | ✅ Completed | Security API documented in `README.md`; Rust doc comments added for selected helpers. |
| 14 | ✅ Completed | CI includes Rust tests in `.github/workflows/ci.yml` (`cargo test`). |
| 15 | ⏳ Not completed | No `atomic.rs` (or equivalent explicit safety-net module) is present yet. |

### Verification evidence (fresh)

- Python integration tests: `python -m pytest -q tests/security_core_test.py` from `rust_core/` → **8 passed**.
- Rust unit tests: `cargo test -- --test-threads=1` from `rust_core/` → **3 passed, 0 failed**.

### Known caveats

- Test workflow can create dated key backup files (`YYYY-MM-DD-keys.pub/.priv`) when key rotation runs; cleanup is not centralized for all paths.
- Design roadmap items in the brainstorm document (e.g., AES-GCM fallback, external cryptography audit, broader benchmarking) remain roadmap work and are not marked complete by this register.

---

**Notes:**
- Every Rust implementation step is preceded by a failing Python (or Rust) test, 
  fulfilling TDD discipline.
- The plan leaves room for later substitution of the simple XOR cipher 
  with a proper AES‑GCM implementation and for expanding the transaction mechanism 
  with actual file‑system staging logic.

Once you approve this plan I'll save it to the canonical `.github/agent/plan` 
file and hand off to `agent/runSubagent` to start implementation.