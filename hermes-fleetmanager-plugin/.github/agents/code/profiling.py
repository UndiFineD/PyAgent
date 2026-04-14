from backend import PostgresBackend
from typing import Any


class ProfilingAgent:
    """
    Code implementation for profiling.
    Streamlines fixed processes while keeping fallback flexibility via markdown rules.
    """

    def __init__(self) -> None:
        self.name = "profiling"
        self.backend = PostgresBackend()

    def execute(self, task: dict[str, Any]) -> dict[str, Any]:
        # 1. Fetch any PostgreSQL or code-based rule overrides
        overrides = self.backend.get_rule_overrides(self.name)

        # 2. If a fixed process exists in overrides, use the fast/code path
        if overrides.get("use_fast_path"):
            return self.fast_execute(task, overrides)

        # 3. Fallback to flexible LLM rule/workflow execution
        return self.llm_execute(task)

    def fast_execute(self, task: dict[str, Any], overrides: dict[str, Any]) -> dict[str, Any]:
        """Faster execution bypassing LLM, reducing context size for fixed processes."""
        print(f"[@{self.name}] Executing via CODE fast-path...")
        return {"status": "success", "mode": "fast_code"}

    def llm_execute(self, task: dict[str, Any]) -> dict[str, Any]:
        """Flexible execution using standard agent rules and workflows."""
        print(f"[@{self.name}] Executing via LLM rules fallback...")
        return {"status": "success", "mode": "llm_rules"}
