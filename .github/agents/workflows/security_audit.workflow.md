---
title: Comprehensive Security Audit Workflow
description: Review codebase for vulnerabilities
---

# Comprehensive Security Audit Workflow

**Description**: Review codebase for vulnerabilities

## Orchestration Steps

1. @vulnerability_scan: Run static and dynamic vulnerability scanning tools.
2. @codeql: Perform deep CodeQL analysis to triage discovered vulnerabilities.
3. @hardening: Apply required security hardening patterns to affected files.
4. @checker: Verify the patches do not break existing functionality.
5. @documentation: Record the security audit summary in .github/agents/governance/.

## Escalation Path
If any agent fails executing its step, it MUST invoke `@agentwriter` to document the gap or generate a new repair agent.
Errors must be logged into `.github/agents/log/error_signatures.log`.
