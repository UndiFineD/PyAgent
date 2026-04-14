from backend import PostgresBackend
from typing import Any


class RulesAgent:
    """
    Code implementation for rules.
    Streamlines fixed processes while keeping fallback flexibility via markdown rules.
    """

    def __init__(self) -> None:
        self.name: str = "rules"
        self.backend: PostgresBackend = PostgresBackend()

    def execute(self, task: dict[str, Any]) -> dict[str, Any]:
        # 1. Fetch any PostgreSQL or code-based rule overrides
        overrides: dict[str, Any] = self.backend.get_rule_overrides(self.name) or {}

        # 2. If a fixed process exists in overrides, use the fast/code path
        if overrides.get("use_fast_path"):
            return self.fast_execute(task, overrides)

        # 3. Fallback to flexible LLM rule/workflow execution
        return self.llm_execute(task)

    def fast_execute(self, task: dict[str, Any], overrides: dict[str, Any]) -> dict[str, str]:
        """Faster execution bypassing LLM, reducing context size for fixed processes."""
        print(f"[@{self.name}] Executing via CODE fast-path...")
        return {"status": "success", "mode": "fast_code"}

    def llm_execute(self, task: dict[str, Any]) -> dict[str, Any]:
        """Flexible execution using standard agent rules and workflows.

        Assemble a redacted, size-limited context before handing off to any LLM.
        """
        print(f"[@{self.name}] Executing via LLM rules fallback...")
        try:
            from context_manager import assemble_context

            ctx_result = assemble_context(self.name, task)
            # ctx_result is {"context": str, "length": int, "redacted": bool}
            return {"status": "success", "mode": "llm_rules", "context_summary": ctx_result}
        except Exception as exc:
            return {"status": "error", "mode": "llm_rules", "error": str(exc)}
