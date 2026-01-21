import logging
from typing import Any
from src.infrastructure.services.sandbox.core.sandbox_core import SandboxCore


class SandboxRuntime:
    """Shell/Manager for containerized agent runtimes.
    Wraps the pure SandboxCore with I/O and runtime orchestration.
    """

    def __init__(self) -> None:
        self.core = SandboxCore()
        self.active_containers: dict[str, Any] = {}

    def run_isolated(
        self, agent_id: str, code: str, risk_level: str = "medium"
    ) -> dict[str, Any]:
        """Runs agent code in an isolated environment after validation."""
        config = self.core.get_security_profile(risk_level)
        validation = self.core.validate_code_execution(code, config)

        if not validation["allowed"]:
            logging.error(
                f"Sandbox: Code rejected for agent {agent_id}: {validation['issues']}"
            )
            return {"success": False, "errors": validation["issues"]}

        logging.info(
            f"Sandbox: Executing code for {agent_id} in {config.memory_mb}MB container."
        )
        # Implementation would call Docker/Podman here.
        # For now, we simulate success within the Core logic.
        return {"success": True, "quota_applied": validation["quota"]}
