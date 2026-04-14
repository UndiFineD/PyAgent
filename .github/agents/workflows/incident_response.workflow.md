---
title: Incident Response Workflow
description: Handle an ongoing incident
---

# Incident Response Workflow

**Description**: Handle an ongoing incident

## Orchestration Steps

1. @incident: Assess the incident, categorize severity, and log initial state in .github/agents/data/.
2. @risk: Evaluate the blast radius and potential business impact.
3. @coding: Implement a hotfix or temporary mitigation if the incident is code-related.
4. @checker: Verify the hotfix and ensure no regressions using the test suite.
5. @execution: Deploy the hotfix to the staging/production environment.
6. @documentation: Update the post-mortem logs in .github/agents/log/.

## Escalation Path
If any agent fails executing its step, it MUST invoke `@agentwriter` to document the gap or generate a new repair agent.
Errors must be logged into `.github/agents/log/error_signatures.log`.
