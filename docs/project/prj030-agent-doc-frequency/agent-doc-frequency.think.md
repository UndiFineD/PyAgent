# agent-doc-frequency — Options

_Status: DONE — Recommended option selected for @3design_
_Analyst: @2think | Date: 2026-03-18_

---

## 1. Root Cause Analysis

### Why the current cadence is insufficient

Agents currently write to their artifact files **once, at session exit**. This creates three compounding problems:

1. **Opacity during long sessions.** A `@6code` session implementing 10 modules may run for many minutes. Until it exits, the project folder shows no evidence of work in progress. The human (and other agents) cannot tell if the agent is stuck, drifting, or making good progress.

2. **Total loss on interruption.** If a VS Code session crashes, the model hits a context limit, or the user force-stops a `runSubagent` call, all in-session findings are lost. No partial artifact is written.

3. **Blocking downstream agents.** When `@6code` calls `runSubagent @7exec`, `@7exec` needs to read `<project>.code.md` to know what was implemented and what commands to run. If that file is only written at the very end of `@6code`'s session—after the handoff call—it is never populated before `@7exec` reads it.

### Why five new artifact files are needed (@5test–@9git)

The current four files (`.project.md`, `.think.md`, `.design.md`, `.plan.md`) are owned by @1project–@4plan. Agents @5test through @9git have no designated artifact file. Their output currently lives only in `docs/agents/Nagent.memory.md` (one shared global file per agent across all projects). This means:

- You cannot look at a project folder and see what @5test discovered.
- `@7exec` cannot read a structured `<project>.exec.md` to understand what was validated.
- `@9git` has no canonical place to record what commit was created for the project.

The global memory files were designed for cross-project lifecycle tracking, not per-project deliverables.

---

## 2. Options Explored

### Option A — Step-Gated Full Overwrite (Instruction-Only Change)

**Approach:**
Add one checkpoint rule to each agent's Operating Procedure:

> "After completing each numbered step, rewrite `docs/project/<project>/<project>.<doctype>.md`
> with the full current state of your artifact."

Agents write the complete artifact content on every checkpoint. Final write at session end is just another overwrite—no special case.

New artifact file sections template:

| Artifact | Sections |
|---|---|
| `<project>.test.md` | `## Test Plan`, `## Test Cases (Red)`, `## Validation Results (Green)`, `## Unresolved Failures` |
| `<project>.code.md` | `## Implementation Summary`, `## Modules Changed`, `## Test Run Results`, `## Deferred Items` |
| `<project>.exec.md` | `## Execution Plan`, `## Run Log`, `## Pass/Fail Summary`, `## Blockers` |
| `<project>.ql.md` | `## Scan Scope`, `## Findings`, `## False Positives`, `## Cleared` |
| `<project>.git.md` | `## Branch`, `## Commit Hash`, `## Files Changed`, `## PR Link` |

**Pros:** ✅ Zero Python code changes — instruction-only. ✅ Proven pattern (existing artifacts already use full rewrite). ✅ One-sentence rule = high LLM compliance. ✅ Clean deliverable for downstream agents.

**Cons:** ⚠️ Token cost proportional to document size. ⚠️ No enforcement mechanism.

---

### Option B — Append-Log with Final Consolidation

**Approach:**
Agent appends a timestamped entry after each finding:
```
---
**Step N — 2026-03-18T14:23Z**: <one-paragraph finding>
```
Final session action adds a `## Summary` section.

**Pros:** ✅ Append-safe (no overwrite risk). ✅ Natural audit timeline.

**Cons:** ❌ Downstream agents expect structured documents, not logs. ❌ Edit tools require read→write (two calls, fragility). ❌ Summary may be skipped on crash.

---

### Option C — Structured Section-Surgical Updates

**Approach:**
Agent updates only sections relevant to each step (targeted edit).

**Pros:** ✅ Minimal rewrite per checkpoint. ✅ Fine-grained structure.

**Cons:** ❌ Complex instructions (~40 sub-rules across 8 agents). ❌ VS Code edit tools still effectively do full overwrites. ❌ High non-compliance risk.

---

### Option D — Progress-Header + Step-Body Overwrite (Hybrid)

**Approach:**
Minimal status header updated per tool call; body rewritten per step.

**Pros:** ✅ Maximum live visibility.

**Cons:** ❌ Two write patterns in one instruction = LLM compliance drops sharply. ❌ Marginal value over a `## Status` field.

---

## 3. Decision Matrix

| Criterion | Opt A (Step Overwrite) | Opt B (Append Log) | Opt C (Surgical) | Opt D (Header+Body) |
|---|---|---|---|---|
| Instruction simplicity | ✅ High | ✅ High | ❌ Low | ❌ Low |
| LLM compliance reliability | ✅ High | ✅ High | ⚠️ Medium | ❌ Low |
| Clean downstream deliverable | ✅ Yes | ❌ Log only | ✅ Yes | ✅ Yes |
| Append safety | ⚠️ Overwrite | ✅ Append-safe | ⚠️ Overwrite | ⚠️ Overwrite |
| Token cost per checkpoint | ⚠️ Full doc | ✅ Paragraph | ✅ Section | ⚠️ Full doc |
| No Python code changes required | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Matches existing pattern | ✅ Yes | ❌ No | ⚠️ Partial | ⚠️ Partial |

**Winner: Option A**

---

## 4. Recommended Option — A (Step-Gated Full Overwrite)

### Rationale

1. Zero code changes. Entire implementation is instruction text in agent configuration files.
2. Proven pattern. Existing artifacts already produced by full rewrite. Agents know how to do this.
3. Highest LLM compliance. "Rewrite the file after each step" is a one-sentence rule. Option C needs 40+ sub-rules.
4. Downstream agent compatibility. Downstream agents expect structured summaries, not append logs.
5. StorageTransaction independence. Not yet implemented; direct file writes are safe for single-machine, one-agent-at-a-time model.

### Implementation summary

1. Add to each `*.agent.md` Operating Procedure:
   > **Checkpoint rule:** At the start of Step 1, create `docs/project/<project>/<project>.<doctype>.md` with the artifact template and `Status: IN_PROGRESS`. After completing each subsequent numbered step, overwrite the file with full current content. Set `Status: DONE` on the final write.

2. Define five new artifact templates (inline in respective `*.agent.md` files):
   - `5test.agent.md` → `.test.md` template
   - `6code.agent.md` → `.code.md` template
   - `7exec.agent.md` → `.exec.md` template
   - `8ql.agent.md` → `.ql.md` template
   - `9git.agent.md` → `.git.md` template

3. Update `1project.agent.md` to list all 9 artifact files in the project folder schema.

4. Update `docs/agents/MEMORY_LIFECYCLE.md` (if it exists) to document the new artifact file types.

5. No changes to `docs/agents/Nagent.memory.md` write contract.

---

## 5. Key Risks

| Risk | Severity | Mitigation |
|---|---|---|
| LLM skips checkpoint writes mid-session | Medium | Unambiguous phrasing; verify in @7exec integration test |
| File overwrite loses a prior section due to LLM compression | Low | Template sections clearly named; agent cannot "forget" a named section |
| StorageTransaction not yet available | Low | Single-machine model makes direct writes safe; note as tech debt |
| @1project doesn't pre-create new artifact stub files | Medium | Clarify in `1project.agent.md` that all 9 stubs are created at project setup |
| New artifact templates diverge in style across agents | Medium | Define templates in shared `docs/agents/ARTIFACT_TEMPLATES.md` linked from each agent file |

---

## 6. Open Questions for @3design

1. **Template authority:** Artifact templates inline in each `*.agent.md`, or in a single `docs/agents/ARTIFACT_TEMPLATES.md`?
2. **Initialization ownership:** Does `@1project` pre-create all 9 stub files, or does each agent create its own at Step 1?
3. **Checkpoint granularity:** Is "after each numbered step" fine enough, or do large steps (e.g. @6code's implement step) need internal sub-checkpoints?
4. **Backport to existing artifacts:** Should the existing four types (`.think.md`, `.design.md`, `.plan.md`, `.project.md`) also adopt the explicit checkpoint rule?
