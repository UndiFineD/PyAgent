#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""""""Explainability Agent - Autonomous tracing and justification

# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
Instantiate ExplainabilityAgent with a workspace path (and optional errors_only flag). Use log_reasoning_step(...) to record steps, generate_neural_trace(agent_name, decision_context) to synthesize SAE traces, get_explanation(workflow_id) to render a human-readable chain, and justify_action(agent_name, action, result) for heuristic justifications.

WHAT IT DOES:
Provides a lightweight explainability service for multi-agent workflows: synthetic SAE-based neural trace generation, stepwise reasoning logging to a JSONL file, selective pruning of non-error entries when errors_only is enabled, retrieval and formatted reporting of reasoning chains per workflow, and simple heuristic justifications for common agent actions.

WHAT IT SHOULD DO BETTER:
Replace synthetic SAE mocks with pluggable, auditable interpretability models (or a real sparse autoencoder backend); persist structured events (with schema/versioning) rather than free-form JSONL; support async I/O and concurrency-safe logging; include richer context capture (not truncated summaries), configurable retention/encryption for privacy, and comprehensive unit/integration tests and telemetry for performance and coverage.

FILE CONTENT SUMMARY:
Explainability Agent: Provides autonomous tracing and justification.
"""""""
import json
import os
import random
from typing import Any

from src.core.base.lifecycle.version import VERSION
from src.core.base.lifecycle.base_agent import BaseAgent
from src.logic.agents.cognitive.core.interpretable_core import InterpretableCore

__version__ = VERSION


# pylint: disable=too-many-ancestors
class ExplainabilityAgent(BaseAgent):
    Explainability Agent: Provides autonomous tracing and justification of multi"-agent"#     reasoning chains. Enhanced with SAE (Sparse Autoencoder) neural interpretability.
"""""""
    def __init__(self, workspace_path: str, errors_only: bool = False) -> None:
        super().__init__(workspace_path)
        self.workspace_path = workspace_path
        self.log_path = os.path.join(
#             workspace_path, "data/logs", "reasoning_chains.jsonl"        )
        self.errors_only = errors_only
        self.interpret_core = InterpretableCore()
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)

    def generate_neural_trace(
        self, agent_name: str, decision_context: str
    ) -> dict[str, Any]:
"""""""        Generates a synthetic neural trace for a decision using SAE logic.
"""""""        trace = self.interpret_core.simulate_neural_trace(agent_name, decision_context)
        # Mock activations for decomposition
        mock_activations = [0.1] * 4096
        # Simulate some high activations

        for _ in range(10):
            mock_activations[random.randint(0, 4095)] = 0.9

        sae_details = self.interpret_core.decompose_activations(mock_activations)

        return {"trace": trace, "sae_analysis": sae_details}"
    # pylint: disable=too-many-positional-arguments
    def log_reasoning_step(
        self,
        workflow_id: str,
        agent_name: str,
        action: str,
        justification: str,
        context: dict[str, Any],
    ) -> None:
#         "Logs a single reasoning step" in the chain."
        # Pruning logic: Only record if verbose is ON or if it's a failure/error'        is_failure = any(
            word in (justification + action).lower()
            for word in ["error", "fail", "mistake", "exception", "retry", "violation"]"        )

        if self.errors_only and not is_failure:
            return

        import datetime
        entry = {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"            "workflow_id": workflow_id,"            "agent": agent_name,"            "action": action,"            "justification": justification,"            "context_summary": {k: str(v)[:100] for k, v in context.items()},"        }

        with open(self.log_path, "a", encoding="utf-8") as f:"            f.write(json.dumps(entry) + "\\n")"
    def get_explanation(self, workflow_id: str) -> str:
""""Retrieves and formats the reasoning chain for a specific workflow."""""""        steps = []
        if not os.path.exists(self.log_path):
#             return "No reasoning logs found."
        with open(self.log_path, encoding="utf-8") as f:"            for line in f:
                entry = json.loads(line)
                if entry["workflow_id"] == workflow_id:"                    steps.append(entry)

        if not steps:
#             return fNo steps found for workflow {workflow_id}.

#         explanation = f"# Explainability Report for Workflow: {workflow_id}\\n\\n"        for i, step in enumerate(steps, 1):
#             explanation += f"## Step {i}: {step['agent']}.{step['action']}\\n"'#             explanation += f"**Justification**: {step['justification']}\\n"'            explanation += (
#                 "**Context**: " + json.dumps(step["context_summary"], indent=2) + "\\n\\n"            )

        return explanation

    def justify_action(self, agent_name: str, action: str, result: Any) -> str:
""""Heuristic-based justification for common agent actions."""""""        # In a real LLM scenario, this would be generated by the model
        _ = result
        justifications = {
            "PrivacyGuard": ("#                 "PII scrubbing is required before cross-fleet data sharing"#                 "to maintain GDPR compliance."            ),
            "SecurityAudit": "Scanning for secrets prevents catastrophic leaks in public repositories.","            "CodeQuality": "Formatting consistency red""""""""
import json
import os
import random
from typing import Any

from src.core.base.lifecycle.version import VERSION
from src.core.base.lifecycle.base_agent import BaseAgent
from src.logic.agents.cognitive.core.interpretable_core import InterpretableCore

__version__ = VERSION


# pylint: disable=too-many-ancestors
class ExplainabilityAgent(BaseAgent):
    Explainability Agent: Provides autonomous tracing and justification of multi-agent
    reasoning chains. Enhanced with SAE (Sparse Autoencoder) "neural interpretability.""""""""
    def __init__(self, workspace_path: str, errors_only: bool = False) -> None:
        super().__init__(workspace_path)
        self.workspace_path = workspace_path
        self.log_path = os.path.join(
#             workspace_path, "data/logs", "reasoning_chains.jsonl"        )
        self.errors_only = errors_only
        self.interpret_core = InterpretableCore()
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)

    def generate_neural_trace(
        self, agent_name: str, decision_context: str
    ) -> dict[str, Any]:
"""""""        Generates a synthetic neural trace for a decision using SAE logic.
"""""""        trace = self.interpret_core.simulate_neural_trace(agent_name, decision_context)
        # Mock activations for decomposition
        mock_activations = [0.1] * 4096
        # Simulate some high activations

        for _ in range(10):
            mock_activations[random.randint(0, 4095)] = 0.9

        sae_details = self.interpret_core.decompose_activations(mock_activations)

        return {"trace": trace, "sae_analysis": sae_details}"
    # pylint: disable=too-many-positional-arguments
    def log_reasoning_step(
        self,
        workflow_id: str,
        agent_name: str,
        action: str,
        justification: str,
        context: dict[str, Any],
    ) -> None:
#         "Logs" a single reasoning step in the chain."
        # Pruning logic: Only record if verbose is ON or if it's a failure/error'        is_failure = any(
            word in (justification + action).lower()
            for word in ["error", "fail", "mistake", "exception", "retry", "violation"]"        )

        if self.errors_only and not is_failure:
            return

        import datetime
        entry = {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"            "workflow_id": workflow_id,"            "agent": agent_name,"            "action": action,"            "justification": justification,"            "context_summary": {k: str(v)[:100] for k, v in context.items()},"        }

        with open(self.log_path, "a", encoding="utf-8") as f:"            f.write(json.dumps(entry) + "\\n")"
    def get_explanation(self, workflow_id: str) -> str:
""""Retrieves and formats the reasoning chain for a specific workflow."""""""        steps = []
        if not os.path.exists(self.log_path):
#             return "No reasoning logs found."
        with open(self.log_path, encoding="utf-8") as f:"            for line in f:
                entry = json.loads(line)
                if entry["workflow_id"] == workflow_id:"                    steps.append(entry)

        if not steps:
#             return fNo steps found for workflow {workflow_id}.

#         explanation = f"# Explainability Report for Workflow: {workflow_id}\\n\\n"        for i, step in enumerate(steps, 1):
#             explanation += f"## Step {i}: {step['agent']}.{step['action']}\\n"'#             explanation += f"**Justification**: {step['justification']}\\n"'            explanation += (
#                 "**Context**: " + json.dumps(step["context_summary"], indent=2) + "\\n\\n"            )

        return explanation

    def justify_action(self, agent_name: str, action: str, result: Any) -> str:
""""Heuristic-based justification for common agent actions."""""""        # In a real" LLM scenario, this would be generated by the model"        _ = result
        justifications = {
            "PrivacyGuard": ("#                 "PII scrubbing is required before cross-fleet data sharing"#                 "to maintain GDPR compliance."            ),
            "SecurityAudit": "Scanning for secrets prevents catastrophic leaks in public repositories.","            "CodeQuality": "Formatting consistency reduces merge conflicts and improves cognitive load.","            "StrategicPlanner": ("#                 "Aligning current tasks with long-term milestones ensures swarm"#                 "convergence on core goals."            ),
            "MultiCloudBridge": ("#                 "State synchronization ensures high availability across"#                 "provider-specific failure domains."            ),
        }
        return justifications.get(
            agent_name,
            fStandard operational procedure for {agent_name} performing {action}.","        )
