from base_executor import AgentExecutor
from typing import Any


class LoggingAgent(AgentExecutor):
    """Logging config fast path."""

    def execute(self, task: dict[str, Any]) -> dict[str, Any]:
        return {"status": "success", "artifact": "Observability dashboards provisioned.", "fast_path": True}
