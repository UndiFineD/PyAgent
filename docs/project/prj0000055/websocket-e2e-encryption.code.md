# websocket-e2e-encryption — Code Notes
_Owner: @6code | Status: DONE_

## backend/ws_crypto.py

New module implementing four primitive functions:

```
generate_keypair()           -> (private_bytes, public_bytes)
derive_shared_secret(priv, pub) -> shared_bytes
encrypt_message(key, plain)  -> nonce[12] + ciphertext
decrypt_message(key, cipher) -> plaintext  (raises on bad tag)
```

Uses `cryptography.hazmat.primitives.asymmetric.x25519.X25519PrivateKey` and
`cryptography.hazmat.primitives.ciphers.aead.AESGCM`.

## backend/app.py — WebSocket Handler Change

After `websocket_auth` passes, the handler now:
1. Generates ephemeral server keypair via `generate_keypair()`
2. Sends server public key as base64-encoded text frame
3. Receives client public key (base64 text frame)
4. Derives `session_key` via `derive_shared_secret()`
5. Wraps `receive_text` / `send_text` with decrypt/encrypt helpers
6. On `InvalidTag` or `ValueError` during decrypt → closes with code 1011

## Key Design Decisions
- Nonce is 12 random bytes per message (AESGCM standard)
- GCM tag is appended by `AESGCM.encrypt()` automatically (16 bytes included)
- `AESGCM.decrypt()` raises `cryptography.exceptions.InvalidTag` on tampering
- Base64 used for wire encoding (WebSocket text frames, no binary frames needed)
- Session key stays in local variable only — never logged, never serialized
