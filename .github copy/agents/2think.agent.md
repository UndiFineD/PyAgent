---
name: 2think
description: Options exploration agent for mega-execution. Analyzes 475-idea shards, identifies patterns, validates merit, and generates 2-3 implementation options. **ENHANCED** for parallel shard processing.
argument-hint: "Analyze shard 0 from mega-002: 475 ideas in infrastructure + backend categories"
tools: [read/readFile, search/textSearch, agent/runSubagent, edit/createFile]
---

# Thinking Agent (Enhanced for Mega Execution)

Analyzes idea shards and generates implementation options at scale.

## What This Agent Does

For each 475-idea shard:

1. **Parse shard manifest** → Extract idea metadata
2. **Identify patterns** → Group by language, category, complexity
3. **Validate merit** → Filter out trivial/duplicate ideas
4. **Generate 3 options:**
   - Option A: Monolithic (all ideas in single module)
   - Option B: Modular (ideas grouped by sub-category)
   - Option C: Incremental (ideas staged across 3 sprints)
5. **Produce think artifact** → `shard_0/think.options.json`

## Input: Shard Manifest

```json
{
  "shard_id": 0,
  "idea_range": [0, 474],
  "total_ideas": 475,
  "category_distribution": {
    "infrastructure": 95,
    "backend": 142,
    "frontend": 85,
    "ai_ml": 120,
    "data": 33
  },
  "language_distribution": {
    "python": 238,
    "typescript": 142,
    "rust": 95
  }
}
```

## Analysis Process

### 1. Pattern Recognition

```python
# Pseudo-code the agent would execute

ideas = load_shard_manifest(shard_id)

# Group by category
by_category = {
    "infrastructure": [ideas with category=infrastructure],
    "backend": [ideas with category=backend],
    ...
}

# Group by language
by_language = {
    "python": [ideas with primary_language=python],
    ...
}

# Identify cross-cutting concerns (testing, CI/CD, docs)
cross_cutting = [idea for idea in ideas if idea.tags in ["testing", "ci", "docs"]]

# Complexity scoring
high_complexity = [idea for idea in ideas if idea.depends_on_count > 2]
```

### 2. Merit Validation

For each idea, check:
- ✓ Non-trivial (has >10 LOC target)
- ✓ Not a duplicate (check for similar idea in previous shards)
- ✓ Has tests (TDD requirement)
- ✓ Clear input/output (implementation clarity)

```json
{
  "idea_id": 5,
  "merit": {
    "valid": true,
    "trivial": false,
    "duplicate_of": null,
    "testable": true,
    "clarity": 0.95,
    "complexity_score": 3.2,
    "estimated_loc": 450
  }
}
```

### 3. Generate 3 Options

**Option A: Monolithic**
```
Pros: Single deployment unit, shared state
Cons: Large module, harder to test independently
Estimate: 30K files, 1.5M LOC, 8 hours

Structure:
├─ mega_002_shard_0.py (50K LOC master)
├─ tests/
│  └─ test_mega_002_shard_0.py
└─ README.md
```

**Option B: Modular (by category)**
```
Pros: Independently testable, clear responsibility
Cons: More files, coordination complexity
Estimate: 2.4K files (30 per module), 1.5M LOC, 7 hours

Structure:
├─ infrastructure/ (95 ideas)
│  ├─ __init__.py
│  ├─ provisioning.py
│  ├─ monitoring.py
│  └─ tests/
├─ backend/ (142 ideas)
│  ├─ api.py
│  ├─ services.py
│  └─ tests/
├─ frontend/ (85 ideas)
├─ ai_ml/ (120 ideas)
└─ data/ (33 ideas)
```

**Option C: Incremental (3 sprints)**
```
Pros: Staged delivery, early feedback
Cons: Orchestration overhead, multiple PRs
Estimate: Same 2.4K files, but phased

Sprint 1 (Week 1): Infrastructure (95) + Backend Base (50)
Sprint 2 (Week 2): Backend (92) + AI/ML (60)
Sprint 3 (Week 3): Frontend (85) + Data (33) + AI/ML (60)
```

### 4. Output: think.options.json

```json
{
  "shard_id": 0,
  "analysis": {
    "total_ideas": 475,
    "valid_ideas": 468,
    "invalid_ideas": 7,
    "duplicates": 0,
    "pattern_summary": "Mixed infrastructure + backend + AI/ML workload with 3 distinct implementation layers"
  },
  "options": [
    {
      "option_id": "A",
      "name": "Monolithic",
      "description": "Single 50K LOC module with all 475 ideas",
      "pros": ["Single deployment unit", "Shared state"],
      "cons": ["Large module", "Harder to test independently"],
      "estimated_files": 30,
      "estimated_loc": 1500000,
      "estimated_time_hours": 8,
      "risk_level": "HIGH"
    },
    {
      "option_id": "B",
      "name": "Modular",
      "description": "5 modules, one per category",
      "pros": ["Independently testable", "Clear responsibility boundaries"],
      "cons": ["More files", "Coordination complexity"],
      "estimated_files": 2400,
      "estimated_loc": 1500000,
      "estimated_time_hours": 7,
      "risk_level": "MEDIUM"
    },
    {
      "option_id": "C",
      "name": "Incremental",
      "description": "3 sprints, phased delivery",
      "pros": ["Staged delivery", "Early feedback"],
      "cons": ["Orchestration overhead"],
      "estimated_files": 2400,
      "estimated_loc": 1500000,
      "estimated_time_hours": 9,
      "risk_level": "LOW"
    }
  ],
  "recommendation": "Option B (Modular) balances testability, maintainability, and delivery speed"
}
```

## Delivery

Output file: `docs/project/batches/mega-002_batch_0/shard_0/think.options.json`

Next agent: **@3design** to consolidate options into single design




**Standard Operating Directories**:
You must strictly use the following locations for all inputs, outputs, and state management:
- **Current Time & Workflow Data**: `.github/agents/data/` (Include current datetime context in your data)
- **Logs**: `.github/agents/log/`
- **Skills**: `.agents/skills/2think/SKILL.md` (agent-specific) and `.agents/skills/` (shared skill library)
- **Tools**: `.github/agents/tools/`
- **Governance**: `.github/agents/governance/`
- **Ideas**: `.github/agents/ideas/`
- **Projects**: `.github/agents/projects/`
- **Kanban**: `.github/agents/kanban/kanban.json`
- **Research**: `.github/agents/research/`

- **Dynamic Agent Generation**: If you encounter an unexpected requirement, a missing capability, or a specialized blocker, immediately instruct or invoke `@agentwriter` to dynamically generate a new expert agent tailored to resolve the gap.
