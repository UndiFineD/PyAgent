# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-guardian-cli\core\workflow.py
"""
Workflow orchestration engine
Coordinates agents and manages pentest execution flow
"""

import asyncio
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from ai.gemini_client import GeminiClient
from utils.logger import get_logger
from utils.scope_validator import ScopeValidator

from core.agent import BaseAgent
from core.memory import Finding, PentestMemory, ToolExecution
from core.planner import PlannerAgent


class WorkflowEngine:
    """Orchestrates the penetration testing workflow"""

    def __init__(self, config: Dict[str, Any], target: str):
        self.config = config
        self.target = target
        self.logger = get_logger(config)

        # Initialize components
        self.memory = PentestMemory(target)
        self.scope_validator = ScopeValidator(config)
        self.gemini_client = GeminiClient(config)

        # Initialize all agents
        from core.analyst_agent import AnalystAgent
        from core.planner import PlannerAgent
        from core.reporter_agent import ReporterAgent
        from core.tool_agent import ToolAgent

        self.planner = PlannerAgent(config, self.gemini_client, self.memory)
        self.tool_agent = ToolAgent(config, self.gemini_client, self.memory)
        self.analyst = AnalystAgent(config, self.gemini_client, self.memory)
        self.reporter = ReporterAgent(config, self.gemini_client, self.memory)

        # Workflow state
        self.is_running = False
        self.current_step = 0
        self.max_steps = config.get("workflows", {}).get("max_steps", 20)

    async def run_workflow(self, workflow_name: str) -> Dict[str, Any]:
        """
        Run a predefined workflow

        Args:
            workflow_name: Name of workflow (recon, web_pentest, network_pentest)

        Returns:
            Workflow results and findings
        """
        self.logger.info(f"Starting workflow: {workflow_name} for target: {self.target}")

        # Validate target
        is_valid, reason = self.scope_validator.validate_target(self.target)
        if not is_valid:
            self.logger.error(f"Target validation failed: {reason}")
            raise ValueError(f"Invalid target: {reason}")

        self.is_running = True
        self.memory.update_phase(f"{workflow_name}_workflow")

        try:
            # Load workflow steps
            steps = self._load_workflow(workflow_name)

            # Execute workflow steps
            for step in steps:
                if not self.is_running:
                    break

                self.logger.info(f"Executing step: {step['name']}")
                await self._execute_step(step)
                self.current_step += 1

            # Generate final analysis
            analysis = await self.planner.analyze_results()

            # Save final state
            self._save_session()

            return {
                "status": "completed",
                "findings": len(self.memory.findings),
                "analysis": analysis,
                "session_id": self.memory.session_id,
            }

        except Exception as e:
            self.logger.error(f"Workflow failed: {e}")
            self._save_session()
            raise
        finally:
            self.is_running = False

    async def run_autonomous(self) -> Dict[str, Any]:
        """
        Run autonomous pentest where AI decides each step

        Returns:
            Final results
        """
        self.logger.info(f"Starting autonomous pentest for target: {self.target}")

        # Validate target
        is_valid, reason = self.scope_validator.validate_target(self.target)
        if not is_valid:
            raise ValueError(f"Invalid target: {reason}")

        self.is_running = True
        self.memory.update_phase("reconnaissance")

        try:
            while self.is_running and self.current_step < self.max_steps:
                # Ask planner for next action
                decision = await self.planner.decide_next_action()

                self.logger.info(f"AI Decision: {decision.get('next_action')}")
                self.logger.debug(f"Reasoning: {decision.get('reasoning', 'N/A')}")

                # Check if we should stop
                if decision.get("next_action", "").lower() in [
                    "done",
                    "complete",
                    "finish",
                ]:
                    self.logger.info("Planner decided workflow is complete")
                    break

                # Execute the decided action
                await self._execute_ai_decision(decision)

                self.current_step += 1

                # Progress phase if needed
                self._maybe_advance_phase()

            # Final analysis
            analysis = await self.planner.analyze_results()

            self._save_session()

            return {
                "status": "completed",
                "findings": len(self.memory.findings),
                "analysis": analysis,
                "session_id": self.memory.session_id,
            }

        except Exception as e:
            self.logger.error(f"Autonomous workflow failed: {e}")
            self._save_session()
            raise
        finally:
            self.is_running = False

    def stop(self):
        """Stop the workflow"""
        self.logger.info("Stopping workflow")
        self.is_running = False

    async def _execute_step(self, step: Dict[str, Any]):
        """Execute a workflow step"""
        step_type = step.get("type", "tool")

        if step_type == "tool":
            # Use Tool Agent to select and execute tool
            tool_name = step["tool"]
            objective = step.get("objective", f"Execute {tool_name}")

            self.logger.info(f"Tool Agent selecting tool: {tool_name}")

            # Tool Agent executes the tool
            result = await self.tool_agent.execute_tool(
                tool_name=tool_name, target=self.target, **step.get("parameters", {})
            )

            if result.get("success"):
                # Use Analyst Agent to interpret results
                self.logger.info("Analyst Agent analyzing results...")
                analysis = await self.analyst.interpret_output(
                    tool=tool_name,
                    target=self.target,
                    command=result.get("command", ""),
                    output=result.get("raw_output", ""),
                )

                self.logger.info(f"Found {len(analysis['findings'])} findings from {tool_name}")
            else:
                self.logger.warning(f"Tool execution failed: {result.get('error')}")

        elif step_type == "analysis":
            # AI analysis step
            self.logger.info("Running correlation analysis...")
            analysis = await self.analyst.correlate_findings()
            self.logger.info("Correlation analysis complete")

        elif step_type == "report":
            # Generate report
            self.logger.info(f"Generating {step.get('format', 'markdown')} report...")
            report = await self.reporter.execute(format=step.get("format", "markdown"))

            # Save report
            output_dir = Path(self.config.get("output", {}).get("save_path", "./reports"))
            output_dir.mkdir(parents=True, exist_ok=True)

            report_file = output_dir / f"report_{self.memory.session_id}.{step.get('format', 'md')}"
            with open(report_file, "w", encoding="utf-8") as f:
                f.write(report["content"])

            self.logger.info(f"Report saved to: {report_file}")

        self.memory.mark_action_complete(step["name"])

    async def _execute_ai_decision(self, decision: Dict[str, Any]):
        """Execute an AI-decided action"""
        action = decision.get("next_action", "")

        self.logger.info(f"Executing AI decision: {action}")

        # Use Tool Agent to select appropriate tool
        try:
            tool_selection = await self.tool_agent.execute(objective=action, target=self.target)

            # Execute selected tool
            result = await self.tool_agent.execute_tool(tool_name=tool_selection["tool"], target=self.target)

            if result.get("success"):
                # Analyze with Analyst Agent
                analysis = await self.analyst.interpret_output(
                    tool=tool_selection["tool"],
                    target=self.target,
                    command=result.get("command", ""),
                    output=result.get("raw_output", ""),
                )

                self.logger.info(f"Found {len(analysis['findings'])} new findings")

        except Exception as e:
            self.logger.error(f"Failed to execute AI decision: {e}")

        self.memory.mark_action_complete(action)

    def _load_workflow(self, workflow_name: str) -> List[Dict[str, Any]]:
        """Load workflow definition"""
        # Predefined workflows
        workflows = {
            "recon": [
                {"name": "subdomain_discovery", "type": "tool", "tool": "subfinder"},
                {"name": "port_scanning", "type": "tool", "tool": "nmap"},
                {"name": "web_probing", "type": "tool", "tool": "httpx"},
                {"name": "analysis", "type": "analysis"},
            ],
            "web": [
                {"name": "web_discovery", "type": "tool", "tool": "httpx"},
                {"name": "vulnerability_scan", "type": "tool", "tool": "nuclei"},
                {"name": "analysis", "type": "analysis"},
            ],
            "network": [
                {"name": "port_scan", "type": "tool", "tool": "nmap"},
                {"name": "service_detection", "type": "tool", "tool": "nmap"},
                {"name": "vulnerability_scan", "type": "tool", "tool": "nuclei"},
                {"name": "analysis", "type": "analysis"},
            ],
        }

        return workflows.get(workflow_name, workflows["recon"])

    def _maybe_advance_phase(self):
        """Advance to next phase based on progress"""
        phases = ["reconnaissance", "scanning", "analysis", "reporting"]
        current_idx = phases.index(self.memory.current_phase) if self.memory.current_phase in phases else 0

        # Simple heuristic: advance after certain number of steps
        if self.current_step % 5 == 0 and current_idx < len(phases) - 1:
            new_phase = phases[current_idx + 1]
            self.logger.info(f"Advancing to phase: {new_phase}")
            self.memory.update_phase(new_phase)

    def _save_session(self):
        """Save session state"""
        output_dir = Path(self.config.get("output", {}).get("save_path", "./reports"))
        output_dir.mkdir(parents=True, exist_ok=True)

        state_file = output_dir / f"session_{self.memory.session_id}.json"
        self.memory.save_state(state_file)
        self.logger.info(f"Session saved to: {state_file}")
