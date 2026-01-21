from src.core.base.agent_plugin_base import AgentPluginBase
from pathlib import Path
from typing import Dict, Any


class testsandbox(AgentPluginBase):
    def __init__(self):
        super().__init__("testsandbox")

    def run(self, file_path: Path, context: Dict[str, Any]) -> bool:
        self.logger.info(f"TestSandbox running on {file_path}")
        return True

    def shutdown(self):
        pass
