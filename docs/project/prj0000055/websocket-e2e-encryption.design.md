# websocket-e2e-encryption — Design
_Owner: @3design | Status: DONE_

## Chosen Architecture: X25519 ECDH + AES-256-GCM

### Cryptographic Primitives
- **Key Exchange:** X25519 Elliptic Curve Diffie-Hellman (RFC 7748)
  - 32-byte private key, 32-byte public key
  - 32-byte shared secret from ECDH
- **Symmetric Encryption:** AES-256-GCM (AEAD)
  - 256-bit key (directly from shared secret)
  - 12-byte random nonce per message (prepended)
  - 16-byte GCM authentication tag (appended by `cryptography` library)

### Handshake Protocol
```
Client                     Server
  |                           |
  |  <-- WS Accept           |
  |  <-- Auth (4401 if fail) |
  |  <-- server pubkey (b64) |
  |  -- client pubkey (b64) -->|
  |  [both derive shared key]  |
  |  == encrypted messages ==  |
```

### Message Wire Format
Each encrypted WebSocket text frame:
```
base64( nonce[12] || ciphertext[n] || gcm_tag[16] )
```

### Module Layout
```
backend/
  ws_crypto.py   — cryptographic primitives
  app.py         — WebSocket handler (MODIFIED)
```

### Error Handling
- Decryption failure (bad tag, corrupt nonce) → close WebSocket with code 1011 (internal error)
- Client sends invalid base64 → treated as decryption failure → close 1011

### Dependencies
- `cryptography>=41.0.0` — already in backend/requirements.txt after prj0000049
