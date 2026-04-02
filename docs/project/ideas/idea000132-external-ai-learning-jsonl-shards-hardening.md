# idea000132 - external-ai-learning-jsonl-shards-hardening

Planned project mapping: none yet

## Idea summary
Consolidate duplicated shard hardening ideas into one scoped initiative for external AI learning JSONL shard artifacts.

## Problem statement
Two active ideas target the same workflow with near-identical requirements and controls, differing only by shard filename. Keeping both active creates duplicate planning and execution overhead.

## Why this matters now
The duplicated scope increases triage noise and can split implementation attention across equivalent work. Consolidation reduces operational friction and improves tracker accuracy.

## User persona and impacted systems
Primary personas: maintainers, release engineers, and quality/security reviewers.
Impacted systems: legacy shard artifact quality checks, CI validation paths, and idea-tracker governance artifacts.

## Detailed proposal
Create one consolidated idea covering hardening for the shard JSONL artifacts listed below. Keep constraints and validation expectations from both source ideas, then archive superseded idea files.

## Scope suggestion
In scope: hardening initiative for the two shard artifacts and their related tests/docs.
Out of scope: unrelated data pipelines, broad architecture redesign, or non-shard modernization initiatives.

## Non-goals
Do not introduce broad subsystem rewrites.
Do not expand this effort to unrelated legacy artifacts.

## Requirements
- Preserve behavior parity where required.
- Add deterministic validation and auditable change evidence.
- Keep rollback simple through scoped commits.
- Maintain explicit lineage to superseded ideas.

## Dependencies and constraints
- Must comply with repository coding and governance checks.
- Must keep updates limited to idea files and tracker artifacts for this merge pass.
- Must keep changes deterministic and minimal.

## Research findings
- Both superseded ideas have the same template structure, readiness, and scoring profile.
- Source targets differ only by shard file path:
  - data/logs/external_ai_learning/shard_202602_306.jsonl.gz
  - data/logs/external_ai_learning/shard_202602_693.jsonl.gz
- Prior tracker run reported no automatic merge candidates at configured thresholds, so this merge is a manual high-confidence semantic consolidation.

## Candidate implementation paths
Path A: hardening and tests first.
Path B: refactor-first then test parity.
Path C: documentation and observability uplift.

## Success metrics
- One active consolidated idea replaces the two superseded shard-specific ideas.
- Tracker summary reflects updated active/archived counts.
- Archived files are explicitly referenced by this consolidated idea.

## Validation commands
- python scripts/IdeaTracker.py --output docs/project/ideatracker.json
- python scripts/project_registry_governance.py validate

## Risks and mitigations
- Risk: accidental scope broadening during consolidation.
  Mitigation: keep cluster size to 2 and restrict to shard-specific duplicate ideas.
- Risk: lineage ambiguity after archival.
  Mitigation: explicit Merged from section with both superseded idea IDs.

## Failure handling and rollback
Rollback manifest:
- If tracker refresh or governance validation fails after move operations, restore archived files to active and remove this consolidated file in the same branch.
- Re-run tracker and governance validation after rollback to confirm baseline restoration.

## Readiness status
ready

## Priority scoring
- impact_score: 2
- confidence_score: 3
- effort_score: 2
- risk_score: 2
- alignment_score: 3
- priority_score: 4

## Merged from
- idea000123 (docs/project/ideas/idea000123-shard-202602-306-jsonl-hardening.md)
- idea000124 (docs/project/ideas/idea000124-shard-202602-693-jsonl-hardening.md)

## Source references
- docs/project/ideas/idea000123-shard-202602-306-jsonl-hardening.md
- docs/project/ideas/idea000124-shard-202602-693-jsonl-hardening.md
- docs/project/legacy_idea_merge_proposals.batch1.json
- docs/project/ideatracker.json
