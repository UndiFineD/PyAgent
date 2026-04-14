# Private Key in Repo - Design

_Status: DESIGN_PHASE_
_Designer: @2think | Updated: 2026-04-06_

## Problem Analysis
Private cryptographic keys (`rust_core/2026-03-11-keys.priv`) are committed to the repository, creating a critical security exposure. Any repository clone leaks the secret material.

## Solution Design
Implement a multi-layered approach:

1. **Pre-commit Hook**: Local git hook that scans for common key patterns
   - Uses regex patterns to detect `.pem`, `.key`, `.priv` files
   - Blocks commits with key material
   - Runs before staging

2. **CI Validation**: Pipeline stage that ensures no key material reaches commits
   - Scans staged files before merge
   - Fails pipeline if keys detected

3. **Documentation**: Operational guidance for developers
   - How to avoid accidental commits
   - How to rotate keys if exposed
   - Configuration instructions

## Technical Approach
- Use Python script with regex pattern matching
- Implement as pre-commit hook script
- Add CI validation step to workflow
- Test with sample key patterns

## Files Affected
- `.git/hooks/pre-commit` (or setup script)
- `scripts/validate-secrets.py`
- `.github/workflows/security.yml` or similar
- Tests in `tests/test_secret_validation.py`

## Dependencies
- Python 3.6+ (already available)
- Git pre-commit support (standard)
- No external dependencies

## Success Metrics
- Hook blocks test keys on local commit
- CI catches keys in pipeline
- All tests pass
- Documentation complete
