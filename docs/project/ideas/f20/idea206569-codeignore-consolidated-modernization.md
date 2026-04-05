# idea206569 - codeignore consolidated modernization

Planned project mapping: none yet

## Idea summary
Consolidate four active `.codeignore` modernization ideas into one scoped initiative for the repository ignore policy file.

## Problem statement
Four active ideas target the same `.codeignore` source file with identical evidence, constraints, and validation steps, differing only by modernization angle. Keeping them separate creates duplicate planning, review, and tracker overhead for one artifact.

## Why this matters now
This duplicate cluster adds avoidable noise to the active idea backlog and makes the same source file appear as multiple parallel initiatives. Consolidation reduces triage churn and preserves one clear path for follow-on work.

## User persona and impacted systems
Primary personas: maintainers, release engineers, and quality/security reviewers.
Impacted systems: repository ignore-policy maintenance, idea-tracker governance artifacts, and any validation paths that depend on `.codeignore` behavior.

## Detailed proposal
Create one consolidated modernization idea covering hardening, performance, observability, and test-coverage improvements for `.codeignore`. Preserve the shared constraints and validation expectations from the superseded idea files, then archive those originals with explicit lineage.

## Scope suggestion
In scope: modernization of `.codeignore`, directly related validation, and idea-tracker/archive updates required for this merge pass.
Out of scope: unrelated repository configuration files, broad tooling redesign, or non-`.codeignore` cleanup.

## Non-goals
Do not expand this effort to other dotfiles in the repository.
Do not introduce unrelated workflow or architecture changes.

## Requirements
- Preserve the source-file focus on `.codeignore`.
- Keep validation deterministic and auditable.
- Maintain explicit lineage to every archived source idea.
- Keep rollback limited to this consolidated file, the archived originals, and tracker refresh output.

## Dependencies and constraints
- Must comply with repository coding and governance checks.
- Must keep file edits limited to `docs/project/ideas/**` and `docs/project/ideatracker.json` for this pass.
- Must preserve the existing pending `idea000123`/`idea000124`/`idea000132` changes without modification.

## Research findings
- `docs/project/legacy_idea_merge_proposals.batch1.json` already groups `.codeignore` as a four-member consolidation candidate.
- All four active ideas reference the same source file: `.codeignore`.
- The four ideas share the same template body, readiness status, validation commands, and nearly identical scoring, with only the objective/archetype varying.
- Manual validation confirmed the cluster is tighter and lower-risk than broader same-slug groups that span different source files.

## Candidate implementation paths
Path A: unify the work as one modernization initiative and archive the duplicate archetype-specific ideas.
Path B: keep separate ideas and accept duplicate backlog/tracker noise.
Path C: defer consolidation until implementation starts.

## Success metrics
- One active consolidated idea replaces the four superseded `.codeignore` ideas.
- Archived files are explicitly referenced by this consolidated idea.
- `docs/project/ideatracker.json` reflects the new active/archive counts and lineage.

## Validation commands
- python scripts/IdeaTracker.py --output docs/project/ideatracker.json
- python scripts/project_registry_governance.py validate

## Risks and mitigations
- Risk: scope broadening beyond `.codeignore`.
  Mitigation: keep the cluster limited to the four `.codeignore` ideas only.
- Risk: lineage ambiguity after archival.
  Mitigation: list every superseded idea in `Merged from` and `Source references`.
- Risk: tracker churn obscures the pass delta.
  Mitigation: restrict the merge to one validated cluster and report exact archived/new files.

## Failure handling and rollback
Rollback manifest:
- If tracker refresh or governance validation fails after archival, restore the four archived idea files to `docs/project/ideas/` and remove this consolidated file in the same branch.
- Re-run tracker generation and governance validation after rollback to confirm the baseline is restored.

## Readiness status
ready

## Priority scoring
- impact_score: 3
- confidence_score: 3
- effort_score: 2
- risk_score: 2
- alignment_score: 3
- priority_score: 5

## Merged from
- idea000104 (docs/project/ideas/idea000104-codeignore-hardening.md)
- idea000154 (docs/project/ideas/idea000154-codeignore-performance.md)
- idea144137 (docs/project/ideas/idea144137-codeignore-observability.md)
- idea144138 (docs/project/ideas/idea144138-codeignore-test-coverage.md)

## Source references
- docs/project/ideas/idea000104-codeignore-hardening.md
- docs/project/ideas/idea000154-codeignore-performance.md
- docs/project/ideas/idea144137-codeignore-observability.md
- docs/project/ideas/idea144138-codeignore-test-coverage.md
- docs/project/legacy_idea_merge_proposals.batch1.json
- docs/project/ideatracker.json