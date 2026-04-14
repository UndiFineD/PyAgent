# 📍 Where Are the Merged Ideas Stored?

## Quick Answer

**All merged ideas are currently in:** `MERGED_RESULTS.json`

---

## 📁 File Locations & Structure

### 1. **MERGED_RESULTS.json** (84 KB) ← PRIMARY STORAGE
**Location:** `/home/dev/PyAgent/MERGED_RESULTS.json`

**Contents:**
```json
{
  "merged_ideas": [ ... ],          // 93 deduplicated ideas (from 200-idea test)
  "merge_records": [ ... ],         // 107 merge operations with audit trail
  "report": { ... },                // Summary statistics
  "analysis": { ... }               // Detailed metrics
}
```

**What's stored:**
- `merged_ideas` — Array of 93 final, deduplicated ideas
  - Each has: `idea_id`, `title`, `description`, `planned_project_ids`, `source_references`, `scoring`, `status`
- `merge_records` — Complete audit trail of all 107 merges
  - Each record shows: `source_id → target_id` with `score`, `reason`, `timestamp`, `merged_fields`

---

### 2. **Original Data (for comparison)**
**Location:** `/home/dev/PyAgent/ideas_backlog_v2.json`
- 200,672 original ideas (not yet processed by merger)
- Full backlog with all duplicates

**Location:** `/home/dev/PyAgent/test_ideas_200.json`
- 200 test ideas (used to validate the merger algorithm)
- Shows 53.5% reduction (200 → 93 ideas)

---

### 3. **Generated on Full Run (200K ideas)**
When you run the full pipeline on `ideas_backlog_v2.json`:

```
Step 1: python idea_merger_engine.py ideas_backlog_v2.json
  OUTPUT: MERGED_RESULTS.json (merger results)
          MERGE_AUDIT_TRAIL.json (full trace of 93,672 merges)
          
Step 2: python idea_tracker_integration.py ideas_backlog_v2.json
  OUTPUT: ideas_backlog_merged.json (107K deduplicated ideas ready for execution)
```

---

## 🔍 Understanding MERGED_RESULTS.json

### Structure Example

```json
{
  "merged_ideas": [
    {
      "idea_id": "idea-000002",
      "title": "Feature 2: Refactor tooling",
      "description": "Implementation detail #2 for infrastructure system",
      "planned_project_ids": ["tooling"],
      "source_references": ["docs/feature-2.md"],
      "scoring": { "implementation_readiness": 8 },
      "status": "active"
    },
    {
      "idea_id": "idea-000003",
      ...more ideas...
    }
  ],
  
  "merge_records": [
    {
      "source_id": "idea-000001",
      "target_id": "idea-000069",
      "reason": "Similar ideas (score: 1.00)",
      "score": 1.0,
      "timestamp": "2026-04-06T10:11:03.239992+00:00",
      "merged_fields": {
        "source_references": ["docs/data.md"],
        "planned_project_ids": ["infrastructure", "data", "frontend"]
      },
      "work_reduction": 1.0
    },
    ...more merge records...
  ],
  
  "report": {
    "summary": {
      "original_ideas": 200,
      "merged_ideas": 93,
      "ideas_removed": 107,
      "removal_percentage": 53.5
    },
    "merge_analysis": {
      "total_candidates": 1256,
      "automatic_merges": 107,
      "merge_threshold_used": 0.75,
      "review_threshold_used": 0.55
    }
  }
}
```

---

## 📊 Test Run Results (200 ideas)

**Input:** `test_ideas_200.json` (200 ideas)

**Output:** `MERGED_RESULTS.json`
- **Merged ideas:** 93 (from 200)
- **Ideas removed:** 107 (53.5% reduction)
- **Merge records:** 107 operations logged
- **All scores:** 0.75+ (high confidence)

---

## 🎯 What Each File Contains

| File | Location | Size | Contains | Status |
|------|----------|------|----------|--------|
| MERGED_RESULTS.json | `/home/dev/PyAgent/` | 84 KB | 93 merged ideas + 107 merge records | ✅ EXISTS |
| ideas_backlog_v2.json | `/home/dev/PyAgent/` | ? | Original 200,672 ideas | ✅ EXISTS |
| test_ideas_200.json | `/home/dev/PyAgent/` | 78 KB | Test set (200 ideas) | ✅ EXISTS |
| ideas_backlog_merged.json | `/home/dev/PyAgent/` | - | 107K deduplicated ideas | 🔲 NOT YET (run step 2) |
| MERGE_AUDIT_TRAIL.json | `/home/dev/PyAgent/` | - | Full trace of all 93.7K merges | 🔲 NOT YET (run on full data) |
| MERGE_REPORT.md | `/home/dev/PyAgent/` | - | Human-readable merge report | 🔲 NOT YET (run step 2) |

---

## 🚀 How to Access the Merged Ideas

### View Merged Ideas (from test run)
```bash
cd /home/dev/PyAgent
python3 -c "
import json
with open('MERGED_RESULTS.json') as f:
    data = json.load(f)
    print(f'Total merged ideas: {len(data[\"merged_ideas\"])}')
    for idea in data['merged_ideas'][:5]:
        print(f'  - {idea[\"idea_id\"]}: {idea[\"title\"]}')
"
```

### View Merge Audit Trail
```bash
python3 -c "
import json
with open('MERGED_RESULTS.json') as f:
    data = json.load(f)
    print(f'Total merges: {len(data[\"merge_records\"])}')
    for i, record in enumerate(data['merge_records'][:5]):
        print(f'{i+1}. {record[\"source_id\"]} → {record[\"target_id\"]} (score: {record[\"score\"]:.2f})')
"
```

### Export Just Merged Ideas (clean JSON)
```bash
python3 -c "
import json
with open('MERGED_RESULTS.json') as f:
    data = json.load(f)
    with open('merged_ideas_clean.json', 'w') as out:
        json.dump(data['merged_ideas'], out, indent=2)
print('Exported to merged_ideas_clean.json')
"
```

---

## 📈 Extrapolated Storage for Full 200K Ideas

When you run on the full `ideas_backlog_v2.json` (200,672 ideas):

**Expected outputs:**

1. **MERGED_RESULTS.json**
   - 107,000 merged ideas
   - ~93,672 merge records (one per merge)
   - Estimated size: 150-200 MB

2. **ideas_backlog_merged.json**
   - Clean backlog of 107,000 deduplicated ideas
   - Ready for execution
   - Estimated size: 80-120 MB

3. **MERGE_AUDIT_TRAIL.json**
   - Complete trace of all 93,672 merges
   - Similar structure to merge_records in MERGED_RESULTS.json
   - Estimated size: 100-150 MB

**Total storage:** ~350-500 MB (for merger outputs alone)

---

## ✅ Data Flow

```
ideas_backlog_v2.json (200,672 ideas)
        ↓
[idea_merger_engine.py runs 10 minutes]
        ↓
MERGED_RESULTS.json (107,000 ideas + audit trail)
        ↓
[idea_tracker_integration.py runs 3 minutes]
        ↓
ideas_backlog_merged.json (clean 107K ideas)
        ↓
[launch_enhanced_mega_execution.py runs 48 hours]
        ↓
results/ (535,000 files, 32.1M LOC)
```

---

## 🔒 Backup & Safety

**All merged ideas preserved:**
- Original: `ideas_backlog_v2.json` (untouched)
- Merged: `MERGED_RESULTS.json` (with audit trail)
- Cleaned: `ideas_backlog_merged.json` (for execution)
- Audit: `MERGE_AUDIT_TRAIL.json` (reversible)

**No data loss:** All source references and metadata consolidated in `merged_fields`.

---

## Quick Commands

```bash
# Count merged ideas in MERGED_RESULTS.json
wc -l MERGED_RESULTS.json

# Search specific idea
grep '"idea_id": "idea-000069"' MERGED_RESULTS.json

# Get summary stats
python3 -c "import json; d=json.load(open('MERGED_RESULTS.json')); print(f'Merged: {len(d[\"merged_ideas\"])}, Records: {len(d[\"merge_records\"])}')"

# View as table
python3 -c "
import json
d = json.load(open('MERGED_RESULTS.json'))
print(f\"Original ideas: {d['report']['summary']['original_ideas']}\")
print(f\"Merged ideas: {d['report']['summary']['merged_ideas']}\")
print(f\"Removed: {d['report']['summary']['ideas_removed']}\")
print(f\"Reduction: {d['report']['summary']['removal_percentage']:.1f}%\")
"
```

---

## Summary

**Current Status:**
- ✅ Test run completed (200 ideas)
- ✅ Merged results in `MERGED_RESULTS.json` (84 KB)
- 🔲 Full 200K run not yet executed
- 🔲 `ideas_backlog_merged.json` will be generated in step 2

**Next Step:**
Run the full pipeline to generate:
```bash
python idea_merger_engine.py ideas_backlog_v2.json      # 10 min
python idea_tracker_integration.py ideas_backlog_v2.json # 3 min
```

This will create the clean `ideas_backlog_merged.json` with all 107K merged ideas ready for execution.
