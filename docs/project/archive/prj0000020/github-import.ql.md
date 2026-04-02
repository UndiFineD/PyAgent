# github-import — Security / CodeQL Review

## Known Security Gaps

- **HMAC webhook signature verification is NOT implemented.**  
  GitHub sends an `X-Hub-Signature-256` header (HMAC-SHA256 of the request body using the configured webhook secret).  
  The current `src/github_app.py` does not verify this header, so any caller can spoof a webhook event.

## Required Remediation (future sprint)

1. Read `WEBHOOK_SECRET` from env/config.
2. Compute `hmac.new(secret, body, sha256).hexdigest()`.
3. Compare with `X-Hub-Signature-256` using `hmac.compare_digest` to avoid timing attacks.
4. Return `403` on mismatch before dispatching to any handler.

## Other Notes
- `subprocess` in `clone_repo` uses explicit arg list (no `shell=True`) — injection-safe.
- No user-supplied data is interpolated into shell strings.
