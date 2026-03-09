# Development Tools & Utilities Design

This topic has been split into several focused design documents.  Each link below points at a file containing one aspect of the original monolithic spec:

- [Structure](2026-03-09-dev_tools_structure_design.md) – outlines where helper code lives, the directory layout under `src/tools` versus `scripts`, and the test/CI conventions used to keep utilities first‑class.
- [Core Capabilities](2026-03-09-dev_tools_capabilities_design.md) – enumerates the individual utilities we want to provide (git helpers, SSL rotation, network calculators, etc.), explains their purpose, and gives concrete module names and design rationale.
- [Self‑Improvement & Autonomy](2026-03-09-dev_tools_autonomy_design.md) – describes how some tools will monitor the repo, run on a schedule, or automatically repair common misconfigurations; includes autonomy patterns and failure modes.
- [Implementation Considerations](2026-03-09-dev_tools_implementation_design.md) – lists cross‑cutting concerns such as shared helper modules, documentation requirements, CLI conventions, and CI integration points.

To create an implementation plan, gather the actionable pieces from each document: the tasks sketched in "Capabilities" become individual modules, the structure doc provides the path rules, autonomy doc suggests scheduled jobs, and implementation considerations supply shared helpers and test skeletons.  The plan should sequence those pieces into test‑driven tasks, beginning with importability tests and a docs check, then scaffolding placeholder modules, and finally fleshing out each utility with real logic and CLI options.

Use this file as the central index: when you're ready to write a plan, refer back here to ensure nothing is overlooked.  The companion plan file should mirror this outline by creating task groups corresponding to each sub‑document.
