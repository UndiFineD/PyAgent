# Git: prj0000049 — Dependabot Security Fixes

## Branch Plan

**Expected branch:** `prj0000049-dependabot-security-fixes`  
**Observed branch:** (to be confirmed at commit time)  
**Project match:** prj0000049 ✓  

## Branch Validation

Branch created from `main`. Single-project branch — no other workstreams.

## Scope Validation

Only dependency version files staged. No application source changes.

## Failure Disposition

If CI fails after bump, revert that specific bump, document as accepted risk in ql.md, and proceed with remaining clean bumps.

## Lessons Learned

(to be filled after merge)

## Commit Hash

`9b2012dcad4b1649deebe6c0bf7d6cc3e910db68`

## PR Link

https://github.com/UndiFineD/PyAgent/pull/187

## Files Changed

- `rust_core/p2p/Cargo.toml` — libp2p `"0.49"` → `"0.56"`, feature names updated for 0.52+ split API
- `rust_core/p2p/src/main.rs` — migrated from deprecated `Swarm::new` to `SwarmBuilder` API
- `rust_core/p2p/Cargo.lock` — regenerated; all vulnerable transitive deps replaced
- `tests/security/__init__.py` — new (empty) package init
- `tests/security/test_rust_p2p_deps.py` — 7 security tests asserting CVE-affected versions absent
- `docs/project/prj0000049/dependabot-security-fixes.project.md`
- `docs/project/prj0000049/dependabot-security-fixes.think.md`
- `docs/project/prj0000049/dependabot-security-fixes.design.md`
- `docs/project/prj0000049/dependabot-security-fixes.plan.md`
- `docs/project/prj0000049/dependabot-security-fixes.test.md`
- `docs/project/prj0000049/dependabot-security-fixes.code.md`
- `docs/project/prj0000049/dependabot-security-fixes.exec.md`
- `docs/project/prj0000049/dependabot-security-fixes.ql.md`
- `docs/project/prj0000049/dependabot-security-fixes.git.md` (this file)
