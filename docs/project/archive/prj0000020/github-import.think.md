# github-import — Think Notes
_Status: COMPLETE_

## Problem
`github_app.py` had a single `/webhook` endpoint that returned `{"received": True}` for all events. This made it impossible to route push, pull_request, or issues events to different handlers. `downloader.py` created a placeholder empty README — not useful for code analysis.

## Decisions
1. Route events via `X-GitHub-Event` header using a dispatch dict of handlers.
2. Add `/health` endpoint for load balancer readiness checks.
3. `clone_repo()` uses `git clone --depth 1` via explicit subprocess args.
4. Keep `download_repo()` as backward-compat shim for tests.
5. HMAC webhook signature verification is deferred (requires GitHub App private key).
