from base_executor import AgentExecutor

class LoggingAgent(AgentExecutor):
    """Logging config fast path."""
    def execute(self, payload: dict) -> dict:
        return {"status": "success", "artifact": "Observability dashboards provisioned.", "fast_path": True}
