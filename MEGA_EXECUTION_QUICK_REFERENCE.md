# 🎯 MEGA EXECUTION QUICK REFERENCE

**mega-002: 200K ideas → 90M LOC in 210 hours**

---

## AGENT PIPELINE AT A GLANCE

```
@10idea (intake) → @0master (coordinate) → @1project (setup)
                                            ↓
                @2think ←→ @3design (options & design)
                            ↓
                @4plan ←→ @5test (plan & tests)
                            ↓
                @6code (implement) → @7exec (validate)
                                    ↓
                                @8ql (quality gate)
                                    ↓
                                @9git (merge)
```

---

## KEY NUMBERS

| What | Value |
|------|-------|
| Total ideas | 200,672 |
| Batches | 40 |
| Shards | 422 |
| Ideas/shard | 475 |
| Files/shard | 2,375 |
| LOC/shard | 142,500 |
| Tests/shard | 300+ |
| Coverage | 91%+ |
| Modules/shard | 5 |
| Tasks/shard | 50 |
| Serial time | 2,940h |
| Parallel time | 210h |
| Speedup | 14x |
| Workers | 14 |

---

## PER-SHARD WORKFLOW

```
@1project: Create dirs & manifests (15 min)
  ↓
@2think: Generate 3 options (1h)
  ↓
@3design: Consolidate to 1 design (1.5h)
  ↓
@4plan: Write 50 tasks + tests (1h)
  ↓
@5test: Validate test suite (1h)
  ↓
@6code: Implement 50 tasks (2.5h)
  ↓
@7exec: Run tests, Docker, smoke tests (1h)
  ↓
@8ql: Security, docs, architecture (1h)
  ↓
@9git: Commit (6 min)

TOTAL: 3h per shard (serial)
       = 2.5h per shard (with 5 parallel modules in @6code)
```

---

## BATCH WORKFLOW

```
@0master: Setup batch 0 (shards 0-13) (2h)
  ↓
[14 shards in parallel, each taking 3h]
  ↓
@0master: Wait for all 14 shards (3h = critical path)
  ↓
@9git: Create PR, merge batch 0 (1.5h)
  ↓
Total: ~6.5h per batch with optimal parallelization
```

---

## QUALITY GATES

| Gate | Stage | Block? | Criteria |
|------|-------|--------|----------|
| 1 | @5test | No | Tests runnable, >90% coverage expected |
| 2 | @6code | Yes | All tests passing, 90%+ coverage, no lint errors |
| 3 | @7exec | Yes | Docker builds, health checks pass, perf OK |
| 4 | @8ql | Yes | 0 critical security issues, docs complete, plan covered |

**If any gate fails:** Escalate to @0master, fix, retry

---

## PARALLELIZATION

### Per Shard
- 5 modules in @6code → 2.5h instead of 7h

### Per Batch
- 14 shards in parallel → 3h instead of 42h

### Across Batches
- Idea intake parallel: 100h instead of 1400h
- Batch 1 starts while batch 0 in @9git

**Total: 210h instead of 2940h (14x speedup)**

---

## FILE OUTPUTS PER SHARD

```
docs/project/batches/mega-002_batch_0/shard_0/
├─ think.options.json              (@2think)
├─ design.md                        (@3design)
├─ plan.md                          (@4plan)
├─ tests/                           (@5test)
├─ generated_code/                  (@6code)
├─ EXECUTION_REPORT.md              (@7exec)
├─ QUALITY_REPORT.md                (@8ql)
└─ .git/commits                     (@9git)

generated_projects_v2/mega_002_shard_0/
├─ infrastructure/
├─ backend/
├─ frontend/
├─ ai_ml/
├─ data/
├─ tests/
├─ Dockerfile
└─ requirements.txt
```

---

## COMMANDS TO KNOW

```bash
# Start execution
python launch_enhanced_mega_execution.py --execution-id mega-002 --batch 0

# Monitor live
python memory_system/live_monitor.py --execution-id mega-002

# Check shard status
cat docs/project/batches/mega-002_batch_0/shard_*/QUALITY_REPORT.md

# View branch
git log mega-002-batch-0 --oneline

# Git PR status
gh pr view 1234 --web
```

---

## FAILURE PATTERNS

| Problem | Solution |
|---------|----------|
| Test fails at @6code | @6code reads error, fixes implementation, retries |
| Docker build fails at @7exec | @7exec reports to @6code, fix Dockerfile/deps, rebuild |
| CodeQL issue at @8ql | Mark false positive (with evidence) or escalate to @6code |
| CI fails at @9git | Fix code, force-push to branch, re-run CI |
| Shard exceeds 4h | Reduce parallelism, retry serially |
| Batch blocked | Escalate to @0master, investigate root cause |

---

## SUCCESS CRITERIA

✅ All 200,672 ideas implemented  
✅ 1,800,000 files generated  
✅ 90,000,000 LOC written  
✅ 90%+ test coverage across all shards  
✅ 0 critical security issues  
✅ 100% docs coverage  
✅ All tests passing (4,200+ per shard)  
✅ All batches merged to main  
✅ 40 release tags created  

---

## CRITICAL TIMING CONSTRAINTS

| Phase | Max Duration |
|-------|--------------|
| @10idea (intake) | 100h |
| @0master (setup) | 2h |
| @1project (dir) | 15 min |
| @2think (options) | 1h |
| @3design (design) | 1.5h |
| @4plan (plan) | 1h |
| @5test (validate) | 1h |
| @6code (implement) | 2.5h ← **bottleneck** |
| @7exec (runtime) | 1h |
| @8ql (quality) | 1h |
| @9git (merge) | 1.5h |
| **Per shard serial** | **~8h** |
| **Per shard parallel** | **~3h** |
| **Per batch (14 shards)** | **~3h** |
| **Total (40 batches)** | **~210h** |

---

## CONFIG FILES

```yaml
# mega_execution_plan.json
execution_id: mega-002
total_ideas: 200672
batches: 40
shards: 422
workers: 14
estimated_hours_parallel: 210

# docs/project/batches/mega-002_batch_0/batch.project.md
batch_id: 0
idea_range: [0, 4999]
shards: 14

# docs/project/batches/mega-002_batch_0/shard_manifests/shard_0.manifest.json
shard_id: 0
ideas: 475
categories: {infrastructure: 95, backend: 142, ...}
languages: {python: 238, typescript: 142, rust: 95}
```

---

## ROLE ASSIGNMENTS (TYPICAL)

| Agent | Worker | Parallelization |
|-------|--------|-----------------|
| @10idea | 1 (batch) | 14-way parallel |
| @0master | 1 (singleton) | Serial |
| @1project | 14 (one per shard) | 14-way parallel |
| @2think | 14 (one per shard) | 14-way parallel |
| @3design | 14 (one per shard) | 14-way parallel |
| @4plan | 14 (one per shard) | 14-way parallel |
| @5test | 14 (one per shard) | 14-way parallel |
| @6code | 14 (one per shard) | 14-way parallel |
| @7exec | 14 (one per shard) | 14-way parallel |
| @8ql | 14 (one per shard) | 14-way parallel |
| @9git | 1 (per batch) | Serial |

---

## ASSUMPTIONS & CONSTRAINTS

✓ 14 workers available (can be reduced)  
✓ Each shard fits in memory (~500MB Docker image)  
✓ Test suite completes in <5 min per shard  
✓ No cross-shard dependencies  
✓ Git branch strategy is clean (no conflicts)  
✓ CI infrastructure stable (no flaky tests)  
✓ Security baseline established (0 critical threshold)  

---

**Check mega_execution_plan.json for full details**  
**Check MEGA_EXECUTION_GUIDE.md for complete workflows**
