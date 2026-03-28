# 7 - Security and Governance Architecture

This document captures the security posture and governance controls for PyAgent development workflows.

## Governance principles

- Enforce conduct and naming standards before handoff.
- Keep project boundaries explicit (ID, scope, branch plan).
- Use least privilege for tool and process execution.

## Security controls

- CI scanning: CodeQL, dependency scanning, and policy checks.
- Quality gates: security review required before git handoff.
- Auditability: preserve rationale and approval trails in project docs.

## Risk categories

- Supply chain risk: dependency drift and vulnerable packages.
- Prompt and tool risk: unsafe tool invocation or unbounded side effects.
- Data risk: leakage of secrets or sensitive execution data.
- Process risk: bypassing branch, scope, or review gates.

## Required mitigations

- Pin or constrain critical dependencies where needed.
- Gate high-risk operations behind explicit policy checks.
- Keep reproducible CI validations for sensitive workflows.
- Block merges on unresolved critical findings.

## Agent-level governance responsibilities

- 0master: enforce scope, branch, and policy preflight.
- 8ql: run security and quality gates; block on critical findings.
- 9git: enforce narrow staging and branch correctness.

## Compliance references

- docs/project/code_of_conduct.md
- docs/project/naming_standards.md
- SECURITY.md
