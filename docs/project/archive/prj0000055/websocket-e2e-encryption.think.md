# websocket-e2e-encryption — Think / Analysis
_Owner: @2think | Status: DONE_

## Existing WebSocket Endpoint Analysis

The existing `/ws` endpoint in `backend/app.py`:
1. Accepts the connection with `await websocket.accept()`
2. Runs `websocket_auth()` — closes with code 4401 if auth fails
3. Registers session in `SessionManager`
4. Enters a `while True` receive loop, dispatching to `handle_message()`

## Encryption Options Considered

| Option | Pros | Cons |
|---|---|---|
| TLS at transport layer | Transparent to app | Requires cert management, not per-session |
| X25519 ECDH + AES-256-GCM | Per-session keys, forward secrecy, Python stdlib via `cryptography` | Requires handshake before first message |
| Noise_XX (full handshake) | Industry grade, mutual auth | Complex, requires Noise lib |
| RSA key wrapping | Widely understood | Slow, no forward secrecy |

## Decision: X25519 ECDH + AES-256-GCM

- X25519 is the modern DH curve (RFC 7748), same as WireGuard and Signal
- AES-256-GCM provides authenticated encryption (AEAD) — integrity + confidentiality
- The `cryptography` package (already used for JWT) provides both
- Simple 2-message handshake: server sends pub key, client sends pub key
- Shared secret derived independently by both sides (no secret transmitted)

## Security Properties
- **Forward secrecy:** Per-session ephemeral key pairs; compromise of one session does not expose others
- **Authentication:** Auth check happens before key exchange (no anon sessions)
- **Integrity:** GCM tag authenticates each message; tampering → decryption failure → 1011 close
- **Nonce:** 12-byte random nonce per message, prepended to ciphertext — replay/reorder detection
