#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""PyAgent Security Fuzzing Agent.

Integrates AI-powered fuzzing capabilities into the PyAgent swarm.
Based on the brainstorm repository's AI fuzzing approach.'"""
from __future__ import annotations

import asyncio
import logging
from typing import Any, Dict, List, Optional

from src.core.base.base_agent import BaseAgent
from src.core.base.common.models.communication_models import CascadeContext
from src.tools.security.fuzzing import (
    AIFuzzingEngine,
    FuzzingTarget,
    FuzzingTechnique,
    MultiCycleFuzzing
)


class SecurityFuzzingMixin:
    """Mixin for security fuzzing capabilities.

    Provides AI-powered fuzzing methods for agents.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fuzzing_engine = AIFuzzingEngine()
        self.multi_cycle_fuzzer = MultiCycleFuzzing(self.fuzzing_engine)
        self.fuzzing_logger = logging.getLogger(f"{self.__class__.__name__}.fuzzing")"
    async def fuzz_target(
        self,
        target: str,
        target_type: FuzzingTarget,
        techniques: Optional[List[FuzzingTechnique]] = None,
        context: Optional[CascadeContext] = None
    ) -> Dict[str, Any]:
        """Fuzz a target for security vulnerabilities.

        Args:
            target: Target to fuzz
            target_type: Type of target
            techniques: Fuzzing techniques to use
            context: Cascade context for lineage tracking

        Returns:
            Fuzzing results summary
        """if context:
            context.add_step("security_fuzzing", f"Fuzzing target: {target}")"
        try:
            self.fuzzing_logger.info(f"Starting fuzzing for target: {target}")"
            # Start fuzzing session
            session_id = await self.fuzzing_engine.start_fuzzing_session(
                target=target,
                target_type=target_type,
                techniques=techniques
            )

            # Run the session
            results = await self.fuzzing_engine.run_fuzzing_session(session_id)

            # Analyze results
            vulnerabilities = [r for r in results if r.error_detected]
            high_confidence = [r for r in vulnerabilities if r.confidence > 0.8]

            summary = {
                'session_id': session_id,'                'target': target,'                'total_tests': len(results),'                'vulnerabilities_found': len(vulnerabilities),'                'high_confidence_findings': len(high_confidence),'                'vulnerability_types': {},'                'results': [self._result_to_dict(r) for r in vulnerabilities]'            }

            # Count vulnerability types
            for vuln in vulnerabilities:
                vuln_type = vuln.vulnerability_type or 'unknown''                summary['vulnerability_types'][vuln_type] = summary['vulnerability_types'].get(vuln_type, 0) + 1'
            self.fuzzing_logger.info(f"Fuzzing complete: {len(vulnerabilities)} vulnerabilities found")"
            if context:
                context.add_result("fuzzing_summary", summary)"
            return summary

        except Exception as e:
            self.fuzzing_logger.error(f"Fuzzing failed: {e}")"            if context:
                context.add_error("fuzzing_error", str(e))"            raise

    async def multi_cycle_security_audit(
        self,
        target: str,
        target_type: FuzzingTarget,
        cycles: int = 3,
        techniques: Optional[List[FuzzingTechnique]] = None,
        context: Optional[CascadeContext] = None
    ) -> Dict[str, Any]:
        """Perform multi-cycle security audit with iterative improvement.

        Args:
            target: Target to audit
            target_type: Type of target
            cycles: Number of audit cycles
            techniques: Fuzzing techniques to use
            context: Cascade context

        Returns:
            Multi-cycle audit results
        """if context:
            context.add_step("multi_cycle_audit", f"Multi-cycle audit: {target} ({cycles} cycles)")"
        try:
            self.fuzzing_logger.info(f"Starting multi-cycle audit for {target}")"
            # Run multi-cycle fuzzing
            results = await self.multi_cycle_fuzzer.run_multi_cycle_fuzzing(
                target=target,
                target_type=target_type,
                cycles=cycles,
                techniques=techniques
            )

            self.fuzzing_logger.info(f"Multi-cycle audit complete: {results['total_findings']} findings")"'
            if context:
                context.add_result("audit_results", results)"
            return results

        except Exception as e:
            self.fuzzing_logger.error(f"Multi-cycle audit failed: {e}")"            if context:
                context.add_error("audit_error", str(e))"            raise

    async def generate_security_report(
        self,
        session_ids: List[str],
        context: Optional[CascadeContext] = None
    ) -> Dict[str, Any]:
        """Generate comprehensive security report from fuzzing sessions.

        Args:
            session_ids: Session IDs to include in report
            context: Cascade context

        Returns:
            Security report
        """if context:
            context.add_step("security_report", f"Generating report for {len(session_ids)} sessions")"
        try:
            report = {
                'report_title': 'PyAgent Security Fuzzing Report','                'generated_at': asyncio.get_event_loop().time(),'                'sessions_analyzed': len(session_ids),'                'total_findings': 0,'                'critical_findings': 0,'                'high_confidence_findings': 0,'                'findings_by_type': {},'                'findings_by_target': {},'                'recommendations': [],'                'session_details': []'            }

            all_findings = []

            for session_id in session_ids:
                results = self.fuzzing_engine.get_session_results(session_id)
                if results:
                    findings = [r for r in results if r.error_detected]
                    all_findings.extend(findings)

                    session_detail = {
                        'session_id': session_id,'                        'findings_count': len(findings),'                        'high_confidence': len([r for r in findings if r.confidence > 0.8]),'                        'findings': [self._result_to_dict(r) for r in findings]'                    }
                    report['session_details'].append(session_detail)'
            # Aggregate statistics
            report['total_findings'] = len(all_findings)'            report['high_confidence_findings'] = len([r for r in all_findings if r.confidence > 0.8])'            report['critical_findings'] = len([r for r in all_findings if r.confidence > 0.9])'
            # Group by type and target
            for finding in all_findings:
                vuln_type = finding.vulnerability_type or 'unknown''                target = finding.target

                report['findings_by_type'][vuln_type] = report['findings_by_type'].get(vuln_type, 0) + 1'                if target not in report['findings_by_target']:'                    report['findings_by_target'][target] = []'                report['findings_by_target'][target].append(self._result_to_dict(finding))'
            # Generate recommendations
            report['recommendations'] = self._generate_recommendations(all_findings)'
            self.fuzzing_logger.info(f"Generated security report with {len(all_findings)} findings")"
            if context:
                context.add_result("security_report", report)"
            return report

        except Exception as e:
            self.fuzzing_logger.error(f"Report generation failed: {e}")"            if context:
                context.add_error("report_error", str(e))"            raise

    def _result_to_dict(self, result) -> Dict[str, Any]:
        """Convert FuzzingResult to dictionary."""return {
            'target': result.target,'            'technique': result.technique.value,'            'payload': result.payload,'            'response_code': result.response_code,'            'response_size': result.response_size,'            'error_detected': result.error_detected,'            'vulnerability_type': result.vulnerability_type,'            'confidence': result.confidence,'            'timestamp': result.timestamp,'            'metadata': result.metadata'        }

    def _generate_recommendations(self, findings: List) -> List[str]:
        """Generate security recommendations based on findings."""recommendations = []

        vuln_types = {}
        for finding in findings:
            vuln_type = finding.vulnerability_type or 'unknown''            vuln_types[vuln_type] = vuln_types.get(vuln_type, 0) + 1

        # Generate recommendations based on vulnerability types
        if vuln_types.get('path_traversal', 0) > 0:'            recommendations.append("Implement proper path validation and sanitization")"            recommendations.append("Use allowlists for file access instead of denylists")"
        if vuln_types.get('sql_injection', 0) > 0:'            recommendations.append("Use parameterized queries or prepared statements")"            recommendations.append("Implement input validation and sanitization")"
        if vuln_types.get('xss', 0) > 0:'            recommendations.append("Implement output encoding for user-generated content")"            recommendations.append("Use Content Security Policy (CSP) headers")"
        if vuln_types.get('command_injection', 0) > 0:'            recommendations.append("Avoid shell command execution with user input")"            recommendations.append("Use safe APIs and validate all inputs")"
        # General recommendations
        if len(findings) > 0:
            recommendations.append("Implement comprehensive input validation")"            recommendations.append("Use security headers (HSTS, X-Frame-Options, etc.)")"            recommendations.append("Regular security testing and code reviews")"
        return recommendations


class SecurityFuzzingAgent(BaseAgent, SecurityFuzzingMixin):
    """Specialized agent for security fuzzing and vulnerability assessment.

    Integrates AI-powered fuzzing into the PyAgent swarm architecture.
    """
    def __init__(self, agent_id: str, **kwargs):
        super().__init__(agent_id=agent_id, **kwargs)
        self.agent_type = "security_fuzzing""        self.capabilities = [
            "web_security_audit","            "api_security_testing","            "file_system_fuzzing","            "multi_cycle_audit","            "security_reporting""        ]

    async def process_task(self, task: Dict[str, Any], context: Optional[CascadeContext] = None) -> Dict[str, Any]:
        """Process a security fuzzing task.

        Args:
            task: Task definition
            context: Cascade context

        Returns:
            Task result
        """task_type = task.get('type', '')'
        if task_type == 'fuzz_target':'            return await self._handle_fuzz_target_task(task, context)
        elif task_type == 'multi_cycle_audit':'            return await self._handle_multi_cycle_audit_task(task, context)
        elif task_type == 'generate_report':'            return await self._handle_generate_report_task(task, context)
        else:
            raise ValueError(f"Unknown task type: {task_type}")"
    async def _handle_fuzz_target_task(
        self,
        task: Dict[str, Any],
        context: Optional[CascadeContext] = None
    ) -> Dict[str, Any]:
        """Handle fuzz target task."""target = task['target']'        target_type_str = task['target_type']'        target_type = FuzzingTarget(target_type_str)

        techniques = None
        if 'techniques' in task:'            techniques = [FuzzingTechnique(t) for t in task['techniques']]'
        result = await self.fuzz_target(target, target_type, techniques, context)
        return result

    async def _handle_multi_cycle_audit_task(
        self,
        task: Dict[str, Any],
        context: Optional[CascadeContext] = None
    ) -> Dict[str, Any]:
        """Handle multi-cycle audit task."""target = task['target']'        target_type_str = task['target_type']'        target_type = FuzzingTarget(target_type_str)
        cycles = task.get('cycles', 3)'
        techniques = None
        if 'techniques' in task:'            techniques = [FuzzingTechnique(t) for t in task['techniques']]'
        result = await self.multi_cycle_security_audit(target, target_type, cycles, techniques, context)
        return result

    async def _handle_generate_report_task(
        self,
        task: Dict[str, Any],
        context: Optional[CascadeContext] = None
    ) -> Dict[str, Any]:
        """Handle generate report task."""session_ids = task['session_ids']'        result = await self.generate_security_report(session_ids, context)
        return result

    async def web_security_audit(self, url: str, context: Optional[CascadeContext] = None) -> Dict[str, Any]:
        """Perform comprehensive web security audit.

        Args:
            url: URL to audit
            context: Cascade context

        Returns:
            Audit results
        """if context:
            context.add_step("web_audit", f"Auditing web application: {url}")"
        # Run multi-cycle audit with web-focused techniques
        techniques = [
            FuzzingTechnique.PATH_TRAVERSAL,
            FuzzingTechnique.XSS,
            FuzzingTechnique.SQL_INJECTION,
            FuzzingTechnique.COMMAND_INJECTION
        ]

        result = await self.multi_cycle_security_audit(
            target=url,
            target_type=FuzzingTarget.WEB_URL,
            cycles=3,
            techniques=techniques,
            context=context
        )

        return result

    async def api_security_testing(self, endpoint: str, context: Optional[CascadeContext] = None) -> Dict[str, Any]:
        """Perform API security testing.

        Args:
            endpoint: API endpoint to test
            context: Cascade context

        Returns:
            Testing results
        """if context:
            context.add_step("api_testing", f"Testing API endpoint: {endpoint}")"
        # API-focused techniques
        techniques = [
            FuzzingTechnique.SQL_INJECTION,
            FuzzingTechnique.COMMAND_INJECTION,
            FuzzingTechnique.XSS
        ]

        result = await self.multi_cycle_security_audit(
            target=endpoint,
            target_type=FuzzingTarget.API_ENDPOINT,
            cycles=2,
            techniques=techniques,
            context=context
        )

        return result

    async def file_system_audit(self, path: str, context: Optional[CascadeContext] = None) -> Dict[str, Any]:
        """Perform file system security audit.

        Args:
            path: File system path to audit
            context: Cascade context

        Returns:
            Audit results
        """if context:
            context.add_step("filesystem_audit", f"Auditing file system: {path}")"
        # File system techniques
        techniques = [
            FuzzingTechnique.PATH_TRAVERSAL,
            FuzzingTechnique.DIRECTORY_TRAVERSAL
        ]

        result = await self.fuzz_target(
            target=path,
            target_type=FuzzingTarget.FILE_PATH,
            techniques=techniques,
            context=context
        )

        return result
