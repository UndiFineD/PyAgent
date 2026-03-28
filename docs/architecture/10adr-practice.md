# 10 - ADR Authoring and Lifecycle

This document standardizes how architecture decisions are proposed, approved, and maintained.

## Canonical template

Use this template for all new ADRs:

- docs/architecture/adr/0001-architecture-decision-record-template.md

## When to create an ADR

Create an ADR when a change affects one or more of the following:

- system architecture boundaries or layering
- runtime model, transaction semantics, or safety model
- API/interface compatibility strategy
- security posture or governance controls
- testing or quality gate requirements

## ADR ownership by workflow phase

- 2think: identify candidate decisions and alternatives.
- 3design: author initial ADR draft with rationale.
- 4plan: map implementation and validation implications.
- 8ql: verify security and compliance implications.
- 9git: ensure ADR is included in narrow staging when required.

## ADR status model

- Proposed: draft under review.
- Accepted: approved and active.
- Deprecated: no longer preferred for new work.
- Superseded: replaced by another ADR.

## Linking requirements

Each ADR must link to:

- related project docs under docs/project/prjNNNNNNN/
- affected architecture docs under docs/architecture/
- implementation or validation artifacts, when applicable

## Update discipline

- Never silently rewrite accepted ADR intent.
- Use superseding ADRs for major direction changes.
- Keep consequences and tradeoffs explicit and current.
