# Private Key Remediation Runbook

## Incident Metadata

- Incident ID: INC-20260328-001
- Project: prj0000090-private-key-remediation
- Scope: Active-tree containment and guardrail hardening

## Containment Evidence

| Evidence Item | Location | Notes |
|---|---|---|
| Key artifact removed from active tree | rust_core/2026-03-11-keys.priv | File deleted in containment phase |
| Rotation checkpoint gate prerequisite | docs/architecture/adr/0002-secret-remediation-control-plane.md | Rewrite remains blocked until rotation gate COMPLETE |
| Active-tree verification script | scripts/security/verify_no_key_material.py | Deterministic cleanup check for known leak path |

## Execution Steps

1. Remove leaked key artifact from active tree paths.
2. Record rotation evidence URIs for each dependent system.
3. Run local verifier before opening pull request.
4. Ensure pre-commit and CI secret scanning are fail-closed.

## Validation Commands

```powershell
& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1
python scripts/security/verify_no_key_material.py
python scripts/security/run_secret_scan.py --profile tree --fail-on-severity HIGH
```
