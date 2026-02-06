# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-guardian-cli\core\tool_agent.py
"""
Tool Selector Agent
Selects appropriate pentesting tools and configures them
"""

from typing import Any, Dict, Optional

from ai.prompt_templates import (
    TOOL_PARAMETERS_PROMPT,
    TOOL_SELECTION_PROMPT,
    TOOL_SELECTOR_SYSTEM_PROMPT,
)

from core.agent import BaseAgent
from tools import HttpxTool, NmapTool, NucleiTool, SubfinderTool


class ToolAgent(BaseAgent):
    """Agent that selects and configures pentesting tools"""

    def __init__(self, config, gemini_client, memory):
        super().__init__("ToolSelector", config, gemini_client, memory)

        # Initialize available tools
        from tools import (
            AmassTool,
            ArjunTool,
            CMSeekTool,
            DnsReconTool,
            FFufTool,
            GitleaksTool,
            GobusterTool,
            HttpxTool,
            MasscanTool,
            NiktoTool,
            NmapTool,
            NucleiTool,
            SQLMapTool,
            SSLyzeTool,
            SubfinderTool,
            TestSSLTool,
            Wafw00fTool,
            WhatWebTool,
            WPScanTool,
            XSStrikeTool,
        )

        self.available_tools = {
            "nmap": NmapTool(config),
            "httpx": HttpxTool(config),
            "subfinder": SubfinderTool(config),
            "nuclei": NucleiTool(config),
            "whatweb": WhatWebTool(config),
            "wafw00f": Wafw00fTool(config),
            "nikto": NiktoTool(config),
            "testssl": TestSSLTool(config),
            "gobuster": GobusterTool(config),
            "sqlmap": SQLMapTool(config),
            "ffuf": FFufTool(config),
            "amass": AmassTool(config),
            "wpscan": WPScanTool(config),
            "sslyze": SSLyzeTool(config),
            "masscan": MasscanTool(config),
            "arjun": ArjunTool(config),
            "xsstrike": XSStrikeTool(config),
            "gitleaks": GitleaksTool(config),
            "cmseek": CMSeekTool(config),
            "dnsrecon": DnsReconTool(config),
        }

    async def execute(self, objective: str, target: str, **kwargs) -> Dict[str, Any]:
        """
        Select and configure the best tool for an objective

        Args:
            objective: What we're trying to accomplish
            target: Target to scan
            **kwargs: Additional context

        Returns:
            Dict with selected tool and configuration
        """
        # Determine target type
        target_type = self._detect_target_type(target)

        # Get context from memory
        context = self.memory.get_context_for_ai()

        # Ask AI to select tool
        prompt = TOOL_SELECTION_PROMPT.format(
            objective=objective,
            target=target,
            target_type=target_type,
            phase=self.memory.current_phase,
            context=context,
        )

        result = await self.think(prompt, TOOL_SELECTOR_SYSTEM_PROMPT)

        # Parse tool selection
        tool_selection = self._parse_selection(result["response"])

        self.log_action("ToolSelected", f"{tool_selection['tool']} for {objective}")

        return {
            "tool": tool_selection["tool"],
            "arguments": tool_selection.get("arguments", ""),
            "reasoning": result["reasoning"],
            "expected_output": tool_selection.get("expected_output", ""),
        }

    async def configure_tool(
        self, tool_name: str, objective: str, target: str
    ) -> Dict[str, Any]:
        """
        Generate optimal parameters for a specific tool

        Returns:
            Dict with tool parameters and justification
        """
        safe_mode = self.config.get("pentest", {}).get("safe_mode", True)
        timeout = self.config.get("pentest", {}).get("tool_timeout", 300)

        prompt = TOOL_PARAMETERS_PROMPT.format(
            tool=tool_name,
            objective=objective,
            target=target,
            safe_mode=safe_mode,
            stealth=False,  # Could be configurable
            timeout=timeout,
        )

        result = await self.think(prompt, TOOL_SELECTOR_SYSTEM_PROMPT)

        return {"parameters": result["response"], "justification": result["reasoning"]}

    async def execute_tool(
        self, tool_name: str, target: str, **kwargs
    ) -> Dict[str, Any]:
        """
        Execute a selected tool

        Returns:
            Tool execution results
        """
        if tool_name not in self.available_tools:
            raise ValueError(f"Unknown tool: {tool_name}")

        tool = self.available_tools[tool_name]

        if not tool.is_available:
            self.logger.warning(f"Tool {tool_name} is not installed")
            return {
                "success": False,
                "error": f"Tool {tool_name} not available",
                "tool": tool_name,
            }

        try:
            # Execute tool
            result = await tool.execute(target, **kwargs)

            # Record execution in memory
            from core.memory import ToolExecution

            execution = ToolExecution(
                tool=tool_name,
                command=result["command"],
                target=target,
                timestamp=result.get("timestamp", ""),
                exit_code=result["exit_code"],
                output=result["raw_output"],
                duration=result["duration"],
            )
            self.memory.add_tool_execution(execution)

            return {
                "success": True,
                "tool": tool_name,
                "parsed": result["parsed"],
                "raw_output": result["raw_output"],
                "duration": result["duration"],
            }

        except Exception as e:
            self.logger.error(f"Tool execution failed: {e}")
            return {"success": False, "error": str(e), "tool": tool_name}

    def _detect_target_type(self, target: str) -> str:
        """Detect if target is IP, domain, or URL"""
        from utils.helpers import is_valid_domain, is_valid_ip, is_valid_url

        if is_valid_url(target):
            return "url"
        elif is_valid_ip(target):
            return "ip"
        elif is_valid_domain(target):
            return "domain"
        else:
            return "unknown"

    def _parse_selection(self, response: str) -> Dict[str, str]:
        """Parse AI tool selection response"""
        selection = {"tool": "nmap", "arguments": "", "expected_output": ""}  # Default

        # Simple parsing
        if "TOOL:" in response:
            start = response.find("TOOL:") + len("TOOL:")
            end = (
                response.find("ARGUMENTS:", start)
                if "ARGUMENTS:" in response
                else len(response)
            )
            selection["tool"] = response[start:end].strip().lower()

        if "ARGUMENTS:" in response:
            start = response.find("ARGUMENTS:") + len("ARGUMENTS:")
            end = (
                response.find("EXPECTED_OUTPUT:", start)
                if "EXPECTED_OUTPUT:" in response
                else len(response)
            )
            selection["arguments"] = response[start:end].strip()

        if "EXPECTED_OUTPUT:" in response:
            start = response.find("EXPECTED_OUTPUT:") + len("EXPECTED_OUTPUT:")
            selection["expected_output"] = response[start:].strip()

        return selection

    def get_available_tools(self) -> Dict[str, bool]:
        """Get status of all tools"""
        return {name: tool.is_available for name, tool in self.available_tools.items()}
