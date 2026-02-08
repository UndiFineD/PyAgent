# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-guardian-cli\utils\logger.py
"""
Audit logging system for Guardian
Tracks all AI decisions and security-relevant actions
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from rich.logging import RichHandler


class AuditLogger:
    """Specialized logger for security audit trails"""

    def __init__(self, log_path: str = "./logs/guardian.log", level: str = "INFO"):
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

        # Create logger
        self.logger = logging.getLogger("guardian")
        self.logger.setLevel(getattr(logging, level.upper()))

        # File handler for audit trail
        file_handler = logging.FileHandler(self.log_path)
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(file_formatter)

        # Rich console handler for beautiful output
        console_handler = RichHandler(rich_tracebacks=True, markup=True)
        console_handler.setLevel(getattr(logging, level.upper()))

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def log_ai_decision(self, agent: str, decision: str, reasoning: str, context: Dict[str, Any]):
        """Log AI agent decisions for audit trail"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "ai_decision",
            "agent": agent,
            "decision": decision,
            "reasoning": reasoning,
            "context": context,
        }
        self.logger.info(f"AI Decision [{agent}]: {decision}")
        self.logger.debug(f"AI Reasoning: {json.dumps(entry, indent=2)}")

    def log_tool_execution(self, tool: str, args: Dict[str, Any], result: Optional[str] = None):
        """Log tool execution for audit trail"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "tool_execution",
            "tool": tool,
            "arguments": args,
            "result_preview": result[:200] if result else None,
        }
        self.logger.info(f"Tool Executed: {tool}")
        self.logger.debug(f"Tool Details: {json.dumps(entry, indent=2)}")

    def log_security_event(self, event_type: str, severity: str, details: str):
        """Log security-relevant events"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "security_event",
            "event_type": event_type,
            "severity": severity,
            "details": details,
        }

        if severity == "CRITICAL":
            self.logger.critical(f"Security Event [{event_type}]: {details}")
        elif severity == "HIGH":
            self.logger.error(f"Security Event [{event_type}]: {details}")
        elif severity == "MEDIUM":
            self.logger.warning(f"Security Event [{event_type}]: {details}")
        else:
            self.logger.info(f"Security Event [{event_type}]: {details}")

    def info(self, message: str):
        """Standard info logging"""
        self.logger.info(message)

    def warning(self, message: str):
        """Standard warning logging"""
        self.logger.warning(message)

    def error(self, message: str):
        """Standard error logging"""
        self.logger.error(message)

    def debug(self, message: str):
        """Standard debug logging"""
        self.logger.debug(message)


# Global logger instance
_logger: Optional[AuditLogger] = None


def get_logger(config: Optional[Dict[str, Any]] = None) -> AuditLogger:
    """Get or create the global logger instance"""
    global _logger

    if _logger is None:
        if config and "logging" in config:
            log_config = config["logging"]
            _logger = AuditLogger(
                log_path=log_config.get("path", "./logs/guardian.log"),
                level=log_config.get("level", "INFO"),
            )
        else:
            _logger = AuditLogger()

    return _logger
