# ideatracker-batching-verbosity - Code Artifacts

_Status: DONE_
_Coder: @6code | Updated: 2026-04-02_

## Implementation Summary

Three coordinated improvements to `scripts/IdeaTracker.py`:

1. **Scalable duplicate detection** — replaced exhaustive O(n²) `itertools.combinations` pairwise scan with a blocking strategy (`_blocking_keys` + `_build_similarity_clusters`). Records are grouped by `planned_project_id` (primary block) or first significant title token (fallback). Only intra-block pairs are evaluated and deduplicated by sorted idea-ID key. Complexity drops from O(n²) to O(k·b²) where k = block count, b = average block size.

2. **Verbose progress logging** — added `_log()` helper writing to stderr (stdout stays machine-readable). `build_tracker_payload` accepts `verbose: bool = False` and logs file-collection progress every `batch_size` files plus a similarity-blocking summary line. Nothing reaches stderr when `verbose=False`.

3. **`--batch-size` / `--verbose` CLI flags** — additive, non-breaking additions to `_build_parser`. Default `batch_size=1000`, `verbose=False`. Existing callers and the summary line contract on stdout are unchanged.

## Modules Changed
| Module | Change | Lines |
|---|---|---|
| `scripts/IdeaTracker.py` | Added `import sys`, `_STOP_WORDS`, `_log()`, `_blocking_keys()`, replaced `_build_similarity_clusters()`, extended `build_tracker_payload()` signature, added CLI flags | +80/-12 |
| `tests/test_idea_tracker.py` | Added 5 new tests covering blocking detection, cross-project exclusion, title-fallback blocking, verbose stderr, and silent non-verbose mode | +210 |

## AC Coverage
| AC | Changed module | Validating test(s) | Status |
|---|---|---|---|
| Batch-oriented processing (default 1000) | `scripts/IdeaTracker.py` | `test_build_tracker_payload_verbose_logs_to_stderr` (batch_size=1) | DONE |
| Verbose progress to stderr | `scripts/IdeaTracker.py` | `test_build_tracker_payload_verbose_logs_to_stderr`, `test_build_tracker_payload_batch_size_default_no_stderr` | DONE |
| Scalable duplicate strategy, not full O(n²) | `scripts/IdeaTracker.py` | `test_similarity_blocking_ignores_cross_project_pairs`, `test_similarity_blocking_finds_shared_project_duplicates` | DONE |
| Obvious duplicates still found | `scripts/IdeaTracker.py` | `test_similarity_blocking_finds_shared_project_duplicates`, `test_similarity_blocking_title_fallback_finds_similar_ungrouped_ideas` | DONE |
| JSON payload shape preserved | `scripts/IdeaTracker.py` | All 3 pre-existing tests still passing | DONE |
| Non-breaking CLI | `scripts/IdeaTracker.py` | Pre-existing batch-window test | DONE |

## Test Run Results
```
========== 8 passed in 8.69s ==========
tests/test_idea_tracker.py::test_build_tracker_payload_includes_active_and_archived_ideas PASSED
tests/test_idea_tracker.py::test_build_tracker_payload_adds_readiness_and_duplicate_candidates PASSED
tests/test_idea_tracker.py::test_build_tracker_payload_batch_window PASSED
tests/test_idea_tracker.py::test_similarity_blocking_finds_shared_project_duplicates PASSED
tests/test_idea_tracker.py::test_similarity_blocking_ignores_cross_project_pairs PASSED
tests/test_idea_tracker.py::test_similarity_blocking_title_fallback_finds_similar_ungrouped_ideas PASSED
tests/test_idea_tracker.py::test_build_tracker_payload_verbose_logs_to_stderr PASSED
tests/test_idea_tracker.py::test_build_tracker_payload_batch_size_default_no_stderr PASSED
```

## Deferred Items

- **Cross-block near-duplicates**: Two ideas with no shared project mapping *and* dissimilar title prefixes will not be compared. This is a known, documented tradeoff of the blocking strategy. Full LSH or shingling-based matching could catch these but is out of scope for this task.
- **Streaming record collection**: Files are still all read into memory before similarity. For extreme scales (millions), a streaming approach would be needed. `batch_size` currently controls only progress reporting, not memory windowing.
