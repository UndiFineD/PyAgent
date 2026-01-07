#!/usr/bin/env python3

"""Agent specializing in Security Auditing and Vulnerability detection."""

from src.classes.base_agent import BaseAgent
from src.classes.base_agent.utilities import create_main_function
import logging

class SecurityAgent(BaseAgent):
    """Agent for security analysis of code and configuration."""
    
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._system_prompt = (
            "You are a Senior Security Auditor. "
            "Scan the provided content for vulnerabilities, hardcoded secrets, "
            "SQL injection risks, cross-site scripting (XSS), and insecure dependencies. "
            "Provide detailed remediation steps for each finding."
        )

    def _get_default_content(self) -> str:
        return "# Security Audit Report\n\n## Summary\nPending audit...\n"

if __name__ == "__main__":
    main = create_main_function(SecurityAgent, "Security Agent", "File to audit for security")
    main()
