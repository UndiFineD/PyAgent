# security_analysis_mixin

**File**: `src\logic\agents\swarm\security_analysis_mixin.py`  
**Type**: Python Module  
**Summary**: 5 classes, 0 functions, 12 imports  
**Lines**: 546  
**Complexity**: 26 (complex)

## Overview

Security analysis and threat modeling for PyAgent workflows.

## Classes (5)

### `SecurityVulnerability`

Represents a security vulnerability in an agent workflow.

### `WorkflowAnalysis`

Analysis results for an agent workflow.

### `WorkflowSecurityAnalyzer`

Security analyzer for PyAgent workflows.

Inspired by Agent-Wiz's threat modeling capabilities, this analyzer
performs static analysis of agent workflows to identify security
vulnerabilities and provide mitigation recommendations.

**Methods** (13):
- `__init__(self)`
- `_load_vulnerability_database(self)`
- `analyze_workflow_code(self, code, filename)`
- `_analyze_security_issues(self, analyzer)`
- `_has_prompt_injection_risk(self, analyzer)`
- `_has_tool_execution_risk(self, analyzer)`
- `_has_data_exposure_risk(self, analyzer)`
- `_has_infinite_loop_risk(self, analyzer)`
- `_has_untrusted_tool_risk(self, analyzer)`
- `_calculate_security_score(self, vulnerabilities)`
- ... and 3 more methods

### `WorkflowASTAnalyzer`

**Inherits from**: NodeVisitor

AST analyzer for extracting workflow components from Python code.

Based on Agent-Wiz's AST parsing approach for workflow extraction.

**Methods** (8):
- `__init__(self)`
- `visit_Import(self, node)`
- `visit_ImportFrom(self, node)`
- `visit_ClassDef(self, node)`
- `visit_FunctionDef(self, node)`
- `visit_Call(self, node)`
- `_get_docstring(self, node)`
- `_is_external_tool(self, node)`

### `SecurityAnalysisMixin`

Mixin to add security analysis capabilities to PyAgent orchestrators.

This mixin provides methods to analyze workflows for security vulnerabilities
and generate security reports, inspired by Agent-Wiz's threat modeling.

**Methods** (5):
- `__init__(self)`
- `analyze_workflow_security(self, workflow_code, workflow_name)`
- `generate_security_report(self, analysis)`
- `get_security_score(self, workflow_code)`
- `check_security_threshold(self, workflow_code, threshold)`

## Dependencies

**Imports** (12):
- `ast`
- `dataclasses.dataclass`
- `dataclasses.field`
- `datetime.datetime`
- `json`
- `logging`
- `src.logic.agents.swarm.orchestrator_work_pattern_mixin.OrchestratorWorkPatternMixin`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Set`

---
*Auto-generated documentation*
