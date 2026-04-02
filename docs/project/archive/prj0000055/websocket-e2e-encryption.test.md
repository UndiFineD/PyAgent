# websocket-e2e-encryption — Test Plan
_Owner: @5test | Status: DONE_

## Unit Tests (tests/test_ws_crypto.py)

| # | Test Name | What It Verifies |
|---|---|---|
| 1 | `test_generate_keypair_returns_32_byte_keys` | Both private and public keys are exactly 32 bytes |
| 2 | `test_ecdh_shared_secret_symmetric` | Alice derives same secret from Bob as Bob from Alice |
| 3 | `test_encrypt_decrypt_roundtrip` | `decrypt_message(key, encrypt_message(key, msg)) == msg` |
| 4 | `test_decrypt_with_wrong_key_raises` | Decrypting with wrong key raises an exception |
| 5 | `test_nonce_prepended_to_ciphertext` | First 12 bytes of `encrypt_message()` output == the nonce |

## Coverage Goals
- All four public functions in `ws_crypto.py` exercised
- Happy path + failure path for decrypt

## Integration Testing (Future)
- Full WebSocket handshake test with `httpx` + `starlette.testclient.TestClient`
- Currently omitted: TestClient WebSocket support has limitations with custom early messages
