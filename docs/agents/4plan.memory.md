# 4plan Memory

This file tracks implementation plans, task breakdowns, and progress checklists.

## Auto-handoff

Once an implementation plan is ready and validated, the next agent in the workflow is **@5test**.

To invoke the next agent, use the following command:

- `agent/runSubagent @5test`

This ensures the plan is handed off cleanly to the testing phase, where test cases are written and validated against the plan.
