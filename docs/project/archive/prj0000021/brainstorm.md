# Async Runtime Update
> **2026-03-10:** Project migrated to Node.js-like asynchronous runtime; synchronous loops are prohibited by automated tests.

# Project Management & Governance Design

This file captures high‑level management items; implementation details generally live outside `src` but are referenced by project metadata.

## Tasks

- Establish project governance structure
- Create project milestone and timeline plan
- Develop project budget and resource allocation plan
- Implement project communication plan
- Create project risk assessment and mitigation plan
- Develop project success criteria and KPIs

## Governance Structure

Define clear roles such as **Engineering Lead**, **Product Manager**, **QA Lead**, and **Security Officer**.  A lightweight RACI matrix (Responsible, Accountable, Consulted, Informed) should be stored in `project/governance.md`.  Governance meetings occur at the start of each milestone and on major architectural decisions.  Developers who produce artifacts for the project (e.g. plans, reports, dashboards) are considered *stakeholders* and have edit access.

## Classification in `src`

These tasks do not correspond to code in `src/` — the actual application lives under the normal Python package tree.  The `project/` directory is a *metadata area* for planning, not the repository root; most source files will continue to reside in `src/` as usual.  (Think of `project/` like a docs/ directory specifically for project‑management artefacts.)

However, templates or helpers (e.g. KPI calculators) could be added to `src/tools/` or `src/analytics/` if necessary.

## Milestones & Timeline

A `project/milestones.md` file outlines major deliverables (MVP, beta, production) with target dates and cross‑team dependencies.  Each milestone includes a short description, acceptance criteria, and a list of related GitHub issues.  The timeline is reviewed weekly during the status email digest.

## Budget & Resource Allocation

Although this is a loose open‑source effort, an annual budget document (`project/budget.xlsx` or markdown) tracks expenditures for cloud services, third‑party tools, and contractor hours.  Resource allocation notes which team members are assigned to which modules or tasks, updated at the beginning of every quarter.

## Success Criteria

Beyond KPIs, success is defined by meeting milestone acceptance criteria, maintaining <50% technical debt ratio (per automated analysis), and achieving <24 hrs average issue turnaround in the issue tracker.  These criteria feed into quarterly reviews and are surfaced to the governance board.


## Notes

The intent is to maintain these documents in `project/` or `.github/` where they can be versioned alongside design artifacts.  None of the items involve programming changes, but developers may be asked to update scripts that generate reports or dashboards.

To support automation we will build a small `src/tools/pm` package containing helper scripts and CLI entrypoints.  Example modules include:

* `kpi.py` – functions to compute throughput, defect density, cycle time, and deployment frequency from CI logs and issue tracker exports.
* `risk.py` – simple editor/serializer for the risk matrix (`project/risk.md`) with YAML/markdown interchange.
* `email.py` – templates and a renderer for weekly status emails.

Each tool will have unit tests under `tests/tools/test_pm_*.py` ensuring sample input produces expected output.  The implementation plan will flesh out those tests as the first TDD step.

A companion `scripts/` directory may house simple utilities invoked by folder watchers or GitHub Actions (e.g. `scripts/generate_governance_templates.py`).  Templates for status emails, incident reports, and meeting agendas should reside under `project/templates/` and the script will copy them when a new milestone is created.

CI workflows (`.github/workflows/pm.yml`) will run the PM tools daily or on demand to regenerate the dashboard, validate report formatting, and dispatch status emails (dry‑run mode).  A test will verify that the workflow file contains the expected steps.

Wherever code is added, a corresponding test in the appropriate `tests/` subfolder will be written, following the pattern established by the earlier infrastructure tasks.

## Key Performance Indicators (KPIs)

To measure progress and value we will track a small set of quantifiable KPIs, e.g.:

* **Feature throughput** – number of stories completed per sprint
* **Defect density** – bugs per thousand lines of code or per release
* **Cycle time** – average lead time from ticket creation to deployment
* **Test coverage** – percentage of code exercised by automated tests
* **Deployment frequency** – how often we ship to staging/production

A lightweight dashboard may be generated from CI logs and the issue tracker; templates for those reports can live under `project/metrics/`.

## Risk Assessment & Mitigation

A simple risk matrix will be maintained in `project/risk.md` with columns:

1. **Risk** – e.g. dependency upgrades, key-person departures, security vulnerabilities
2. **Likelihood** – low/medium/high
3. **Impact** – low/medium/high
4. **Mitigation** – planned actions or contingencies

Periodic reviews (at the start of each milestone) will update the matrix.  High‑impact/high‑likelihood items must surface to the governance board and have assigned owners.

## Communication Workflows

Clear, documented communication channels are essential:

* **Daily standups** – team sync via chat or short video call; notes stored in `project/standups/`.
* **Weekly status emails** – automated summary of completed work, blockers, upcoming milestones.
* **Incident notifications** – Slack/Teams alerting for production outages with post‑mortems archived in `project/incidents/`.
* **Documentation updates** – any design or plan change triggers a pull request; reviewers include engineering lead and at least one product manager.

Templates for status emails, incident reports, and meeting agendas should be placed alongside the governance documents so they can be easily reused.

## Implementation Considerations

Even though the governance framework centers around documentation, an implementation plan will require several concrete deliverables:

1. **PM tool package** (`src/tools/pm`) with CLI wrappers and core logic for computing KPIs, editing risk matrices, and rendering templates.  Tests are mandatory and will drive development.
2. **Template directory** (`project/templates/`) containing boilerplate email/text documents; a generator script to instantiate them for new milestones.
3. **CI workflow** (`.github/workflows/pm.yml`) with steps to execute the PM tools and validate their output; accompanied by a structure test similar to `tests/structure/*` used earlier.
4. **Metadata files** (`project/milestones.md`, `project/risk.md`, etc.) initial stubs and specifications.
5. **Sample dashboards** generated via scripts and optionally stored under `project/metrics/` with a README describing how to refresh them.

These implementation notes will map directly to tasks in the upcoming plan, ensuring each code artifact is test‑driven and versioned.

## Implementation Status

Several components have been bootstrapped according to this design: a `src/tools/pm` package, generator scripts, metadata stubs in `project/`, and accompanying unit tests.  The governance CI workflow (`.github/workflows/pm.yml`) is in place and exercised by tests.

## 5W1H Summary

To keep the high‑level purpose explicit:

* **Who**: Core team roles (Engineering Lead, Product Manager, QA, etc.) plus stakeholders across engineering, product, and operations.
* **What**: A lightweight governance framework that governs planning, execution, risk, and communication for the PyAgent project.
* **Where**: Documentation lives in `project/` and `.github/`; operational activities occur in the repository, chat channels, and the CI system.
* **When**: Governance meetings at milestone start, weekly status emails, quarterly reviews for budget/resource updates, and incident notifications in real time.
* **Why**: To ensure transparency, accountability, and measurable progress; reduce risk; and align the distributed team toward shared goals.
* **How**: Through documented templates, automated reports, regular syncs, and version‑controlled artefacts that anyone can inspect.

This 5W1H section can serve as an introduction for new contributors or external reviewers.
