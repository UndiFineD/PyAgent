#!/usr/bin/env python3

"""Agent specializing in self-optimization and roadmap refinement."""

from src.classes.base_agent import BaseAgent
from src.classes.base_agent.utilities import create_main_function
from src.classes.stats.ResourceMonitor import ResourceMonitor
from src.classes.stats.ObservabilityEngine import ObservabilityEngine
import logging
import os
from pathlib import Path
from typing import Dict, List, Any, Optional

class SelfOptimizerAgent(BaseAgent):
    """Analyses the workspace status and suggests strategic improvements."""
    
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        workspace_root = self.file_path.parent.parent.parent
        self.resource_monitor = ResourceMonitor(str(workspace_root))
        self.telemetry = ObservabilityEngine(str(workspace_root))
        self._system_prompt = (
            "You are the Self-Optimizer Agent. "
            "Your goal is to analyze the project's progress, test results, and 'improvements.txt' "
            "to identify the most impactful next steps for development. "
            "Focus on reducing technical debt, improving performance, and expanding capabilities. "
            "Always output a structured 'Strategic Roadmap' in Markdown."
        )

    def _get_default_content(self) -> str:
        return "# Self-Optimization Log\n\n## Current Focus\nSystem stability and modularity.\n"

    def analyze_roadmap(self, improvements_path: str = "improvements.txt") -> str:
        """Reads the improvements file and prioritizes items."""
        root = self.file_path.parent.parent.parent # Resolve to workspace root
        imp_file = root / improvements_path
        
        if not imp_file.exists():
            return "No improvements file found to analyze."
            
        try:
            content = imp_file.read_text(encoding="utf-8")
            # In a real scenario, we might use an LLM here.
            # For this tool, we'll categorize based on keywords.
            lines = content.splitlines()
            
            categories = {
                "High Priority (Stability)": [],
                "Medium Priority (Features)": [],
                "Low Priority (Maintenance)": []
            }
            
            for line in lines:
                if not line.strip() or line.startswith("#"): continue
                
                low_line = line.lower()
                if any(k in low_line for k in ["fix", "bug", "error", "crash", "stable"]):
                    categories["High Priority (Stability)"].append(line)
                elif any(k in low_line for k in ["add", "new", "feature", "capability", "expand"]):
                    categories["Medium Priority (Features)"].append(line)
                else:
                    categories["Low Priority (Maintenance)"].append(line)
                    
            report = ["# Strategic Optimization Roadmap\n"]
            for cat, items in categories.items():
                if items:
                    report.append(f"## {cat}")
                    for item in items[:5]: # Take top 5 per category
                        report.append(f"- [ ] {item}")
                    report.append("")
                    
            return "\n".join(report)
        except Exception as e:
            return f"Error analyzing roadmap: {e}"

    def improve_content(self, prompt: str) -> str:
        """Analyze and optimize."""
        roadmap = self.analyze_roadmap()
        stats = self.resource_monitor.get_current_stats()
        telemetry = self.telemetry.get_summary()
        
        system_report = [
            f"\n## System Health",
            f"- **Status**: {stats.get('status', 'Unknown')}",
            f"- **CPU Usage**: {stats.get('cpu_usage_pct')}%",
            f"- **Memory Usage**: {stats.get('memory_usage_pct')}%",
            f"- **Free Disk**: {stats.get('disk_free_gb')} GB",
            f"- **Avg Latency**: {telemetry.get('avg_latency_ms', 'N/A')} ms",
            f"- **Success Rate**: {telemetry.get('success_rate', 'N/A')}%"
        ]
        
        return f"Self-Optimization Analysis for: {prompt}\n\n{roadmap}\n" + "\n".join(system_report)

if __name__ == "__main__":
    main = create_main_function(SelfOptimizerAgent, "SelfOptimizer Agent", "Query/Topic to optimize")
    main()

