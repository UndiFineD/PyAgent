# 3 — Project Portfolio

This document is the stable landing page for the PyAgent project portfolio.

## Purpose

- Describe how projects are tracked, named, and stored
- Point agents and contributors to the canonical project registry

## Canonical registry

| File | Purpose |
|---|---|
| `docs/project/kanban.md` | Single source of truth for all projects across all lifecycle lanes |
| `data/projects.json` | Machine-readable project registry (mirrors kanban.md) |

Both files must be updated in sync on every lane transition.

## Project folder structure

Each project has a folder: `docs/project/prjNNNNNNN/`

```
docs/project/prjNNNNNNN/
  prjNNNNNNN.project.md   ← goal, scope, branch plan, acceptance criteria
  prjNNNNNNN.think.md     ← options exploration (@2think)
  prjNNNNNNN.design.md    ← design decisions (@3design)
  prjNNNNNNN.plan.md      ← implementation plan (@4plan)
  prjNNNNNNN.test.md      ← test strategy and results (@5test)
  prjNNNNNNN.code.md      ← code implementation notes (@6code)
  prjNNNNNNN.exec.md      ← runtime validation results (@7exec)
  prjNNNNNNN.ql.md        ← security review (@8ql)
  prjNNNNNNN.git.md       ← git workflow record (@9git)
```

## ID namespace

- `prjNNNNNNN` IDs are owned by `@0master`
- IDs are never reused
- The next available ID is recorded in `docs/agents/0master.memory.md`

## Programmatic access

```
GET /api/projects          → list all projects
GET /api/projects?lane=Xxx → filter by lane
PATCH /api/projects/{id}   → update a project record
POST /api/projects         → create a new project
```
