# Async Runtime Update
> **2026-03-10:** Project migrated to Node.js-like asynchronous runtime; synchronous loops are prohibited by automated tests.

# Future Roadmap Design

This file consolidates long‑term planning tasks.  They are conceptual and do not directly modify `src` today.

## Tasks

Each of the following high‑level activities will eventually spawn its own
implementation plan or set of documents.  This section now contains a
brief motivation, candidate approaches, evaluation criteria, and risk factors
for each item.

### Define project vision and long-term goals

**Motivation:** A clear vision aligns contributors and guides every
feature decision.  Without it the project drifts range and technical debt
accumulates.

**Approaches:**

1. Interview stakeholders and synthesise a one‑pager vision statement.  
2. Run a series of working sessions with engineers and product owners, then
   publish a living wiki page.  
3. Use the "north star metric" workshop format to derive measurable goals.

**Success criteria:**

* A published document exists and is referenced in at least three PRs or
  issues during the next quarter.  
* New contributors can articulate the vision within their first week.  
* Roadmap items can be traced back to at least one long‑term goal.

**Dependencies:**

- Project management tooling (e.g., GitHub Projects, Linear).
- Access to customer/tenant feedback channels.

**Risks & Questions:**

* Vision statements often languish outdated; establish a review cadence.
* How much detail is harmful versus helpful?

---

### Create technology roadmap with milestones

**Motivation:** Translate vision into a sequence of achievable technical
milestones so the team knows what to build next and why.

**Approaches:**

1. Use a Gantt‑style timeline in `project/roadmap.md` with quarterly
   themes.  
2. Build a milestone board in GitHub Projects, grouping issues into
   releases.  
3. Maintain a living spreadsheet that tracks capabilities versus dates.

**Success criteria:**

* Roadmap is referenced during sprint planning at least once per sprint.  
* 90 % of planned milestones for a quarter are either completed or rolled
  forward with a rationale.  
* Engineers can identify which milestone their current task aligns to.

**Dependencies:**

- Executive buy‑in for timeboxing and staging work.
- Integration with issue tracker for automatic progress reporting.

**Risks & Questions:**

* Over‑commitment leading to frequent missed dates reduces trust.  
* How to handle unplanned urgent work (e.g., security fixes)?

---

### Develop feature prioritization framework

**Motivation:** With many competing ideas, we need a consistent way to
choose what to build first based on value, effort, and risk.

**Approaches:**

1. Implement RICE scoring (Reach, Impact, Confidence, Effort) for every
   feature request.  
2. Use weighted simple voting with stakeholder representatives.  
3. Adopt the "Opportunity Solution Tree" method from Teresa Torres.

**Success criteria:**

* Established framework is applied to 100 % of new feature proposals.  
* A retrospective shows that features delivered according to the framework
  had higher customer satisfaction metrics than ad‑hoc choices.  
* Prioritization meetings are shorter and more productive.

**Dependencies:**

- Data collection for reach and impact (analytics, surveys).
- Training for stakeholders on using the framework.

**Risks & Questions:**

* Risk of gaming the system—teams may inflate scores.  
* Balancing technical debt items versus new user‑facing features.

---

### Establish innovation and R&D strategy

**Motivation:** Reserve space for exploratory work without derailing the
core roadmap.  This encourages experimentation and prevents stagnation.

**Approaches:**

1. Allocate a fixed percentage of each sprint (e.g., 10 %) to "research
   spikes" with clearly defined success criteria.  
2. Create an annual hackathon and allow teams to prototype ideas that may
   feed back into the roadmap.  
3. Maintain an "incubator" label on GitHub issues for experiments and track
   their outcomes separately.

**Success criteria:**

* At least one research prototype per quarter progresses into the main
  codebase.  
* Experimentation tickets are closed with explicit `success/failure` notes.
* Team surveys indicate they feel empowered to suggest new directions.

**Dependencies:**

- Dedicated R&D budget or time allocation.  
- Mechanism for capturing and sharing learnings (wiki, internal talks).

**Risks & Questions:**

* Too many experiments without follow‑through can waste resources.  
* How to avoid innovation work competing with committed roadmap items?

---

### Plan for scalability and performance optimization

**Motivation:** As adoption grows, we must ensure the system scales without
exponential cost or latency increases.

**Approaches:**

1. Develop a set of benchmarks under `src/benchmarks/` that run automatically
   in CI.  
2. Conduct quarterly load tests against staging environments and publish
   results.  
3. Build automatic alerts on key performance indicators (KPIs) with SLOs.

**Success criteria:**

* Maintain latency <200 ms for 95 % of requests under the projected load.  
* Cost per transaction (cloud bill) does not exceed target thresholds.  
* CI benchmarks fail before a release if performance regresses.

**Dependencies:**

- Monitoring stack (Prometheus/Grafana, Datadog).  
- Load‑testing tools (k6, Locust).

**Risks & Questions:**

* Premature optimization may waste effort; focus on measured bottlenecks.  
* Performance targets may conflict with feature velocity.

---

## Classification in `src`

While roadmap activities themselves live in `project/` or `.github/roadmap`,
several code modules will emerge:

* `src/benchmarks/` for benchmark scripts and load‑test helpers.
* `src/perf/` containing profiling utilities, cost calculators, and SLO
  definitions.
* Potential small CLI under `src/roadmap/` to manipulate the roadmap files.

This design file will remain the canonical reference until the roadmap is
formalized in a more structured format.

## Notes

Treat this document as a living artifact; revisit it during quarterly
planning.  Each bullet above should eventually spawn its own design and
implementation plan when the team commits to building it.

## Classification in `src`

While roadmap items drive what gets implemented in `src/`, the planning documents themselves are kept in `project/` or `.github/roadmap`.
Specific roadmap-related code (e.g. performance benchmarks, scalability tests) will appear under `src/benchmarks/` or `src/perf/` when executed.

## Managing agent context & tooling

A cross‑cutting requirement for almost every roadmap item is the
infrastructure that supports the agents themselves.  as models grow, we
must cope with **context size**, **multipart context rewrite/windowing**,
and the dynamic **tool/skill registry** (`.agents/skills`).

**Motivation:**
The swarm and research packages depend on agents remaining coherent with
very large histories of interaction.  Without explicit support for splitting,
rewriting and caching context, models will hit token limits and degrade.
Furthermore, tools and skills evolve independently, and agents should be
able to discover and load them at runtime.

**Approaches:**

1. Implement a `ContextManager` library that fragments long chats into
   4‑kB windows (chunking & vector indexing) and rewrites earlier segments
   when new information supersedes them.  The manager would expose a simple
   interface (`push(), rewrite(), snapshot()`) used by all agents.
2. Use a modular agent architecture where each “thought” or subtask is a
   separate context document; a supervisor stitches these along with the
   current prompt, allowing partial recombination and pruning.  This
   mirrors architectures used by LangGraph and LangChain.
3. Build a centralized service (Rust in `rust_core/`) that handles context
   windowing and provides a gRPC API.  Agents then call out rather than
   carrying the logic themselves.

**Success criteria:**

* Agents are able to handle conversations exceeding 1 million tokens by
  pruning and rewriting without loss of relevant information.
* New tools placed under `.agents/skills/` are automatically registered and
  available within 30 seconds of being added; no restart required.
* Unit tests simulate context window boundary conditions and all pass.

**Dependencies:**

- Vector database or in‑memory index for context segments.
- Conventions for skill metadata (YAML or JSON in `.agents/skills/*`).
- Coordination between Python and Rust (ffi or grpc) if service approach
  is chosen.

**Risks & Questions:**

* Context rewriting might inadvertently remove facts still needed later.
  Thorough testing and explicit pinning of critical segments is necessary.
* Tools/skills versioning could cause incompatibilities; consider a
  migration mechanism or checksum validation.

---

## Notes

These tasks are guiding artifacts, meant to be revisited periodically.  Implementation of features and performance improvements will be tracked separately once the roadmap is formalized.

## Implementation Status

Several pieces of this roadmap are already live: the `src/roadmap` modules with associated tests, the benchmarking infrastructure used by roadmap and testing plans, and the context/skill/CORT tooling discussed earlier.  Future work items will spawn their own plans as originally envisioned.
