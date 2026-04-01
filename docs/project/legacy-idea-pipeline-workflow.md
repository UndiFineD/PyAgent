# Legacy Idea Pipeline Workflow

This workflow turns large legacy code/document snapshots into prioritized, merge-ready idea artifacts.

## Goals

- Generate high-volume, template-filled ideas from legacy files.
- Cluster near-duplicate ideas and propose merges.
- Promote only top-ranked ideas into `docs/project/ideas/`.
- Keep operations idempotent and resumable.

## Inputs

- Legacy source root (for example: `C:/Dev/PyAgent.3.7.0`).
- Generated ideas JSONL from the legacy generator.

## Step 1: Generate Ideas

Run the generator in batches for controllable throughput:

```powershell
python scripts/GenerateLegacyIdeas.py --legacy-root C:\Dev\PyAgent.3.7.0 --output docs/project/legacy_ideas_3_7_0.batch1.jsonl --manifest docs/project/legacy_ideas_3_7_0.batch1.manifest.json --max-ideas-per-file 10 --offset 0 --limit 500
```

Notes:

- Excludes files under dot-directories automatically.
- Generates up to 10 ideas per file with filled template sections.
- Manifests make reruns auditable and resumable.

## Step 2: Propose Dedupe Merges

Produce merge candidates grouped by source-file overlap:

```powershell
python scripts/ProposeLegacyIdeaMerges.py --input docs/project/legacy_ideas_3_7_0.batch1.jsonl --output-json docs/project/legacy_idea_merge_proposals.batch1.json --output-markdown docs/project/legacy_idea_merge_proposals.batch1.md --min-group-size 2 --max-group-size 4 --min-priority 2
```

Outputs:

- JSON proposal set for automation.
- Markdown proposal report for review.

## Step 3: Promote Top Ideas

Promote only the best ideas into active project idea files:

```powershell
python scripts/PromoteLegacyIdeas.py --input docs/project/legacy_ideas_3_7_0.batch1.jsonl --ideas-dir docs/project/ideas --archive-dir docs/project/ideas/archive --state-file docs/project/legacy_ideas_promoted_state.json --manifest docs/project/legacy_ideas_promotion.batch1.json --top-n 100 --min-priority 2 --max-per-source 1
```

Promotion behavior:

- Allocates next available `ideaNNNNNN` ID.
- Converts generated template into markdown idea files.
- Uses state file to prevent duplicate promotions on rerun.

## Operational Guidelines

- Use batch windows (`offset`, `limit`) to avoid huge one-shot runs.
- Keep generated JSONL as artifact data unless repository policy explicitly requires check-in.
- Commit scripts, tests, manifests, and promoted idea markdowns separately from massive raw outputs.

## Suggested Cadence

1. Generate next batch.
2. Run dedupe proposals.
3. Promote top-N candidates.
4. Review and hand off selected ideas to `@10idea` merge or to project planning.

## Validation

Run focused checks before PR:

```powershell
pytest -q tests/test_generate_legacy_ideas.py tests/test_promote_legacy_ideas.py tests/test_propose_legacy_idea_merges.py
```
