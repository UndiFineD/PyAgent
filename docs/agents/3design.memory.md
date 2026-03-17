# 3design Memory

This file records finalized design decisions, architecture diagrams, and key interface contracts.

## Auto-handoff (Design → Plan)

Once a design is finalized, the next agent in the workflow is **@4plan**.  The designer agent should invoke **@4plan** via `agent/runSubagent` so the planning work is started automatically and the work is correctly attributed.

When calling `agent/runSubagent`, include a clear task description and any relevant context/links to the design decisions so the planning agent can continue without having to re-derive the design intent.
