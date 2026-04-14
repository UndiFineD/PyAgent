from base_executor import AgentExecutor
import logging
from typing import Any


class FastPathExecAgent(AgentExecutor):
    """Executes Terraform, Docker, Shell commands."""

    def execute(self, task: dict[str, Any]) -> dict[str, Any]:
        prompt = task.get("prompt", "Default echo prompt")
        # For realistic simulation, pretending to run a cloud deployment if Terraform is requested
        # Here we will write to a local log or run a real echo
        logging.info(f"Agent {self.__class__.__name__} received Infra task: {prompt}")

        # In a real environment, this translates "Deploy Edge cluster" into Terraform syntax
        # or triggers LLM context if not a deterministic fast-path.
        if "terraform" in prompt.lower() or "deploy" in prompt.lower() or "edge" in prompt.lower():
            # Example fake terraform apply (We just echo for safety here)
            command_result = self.run_command(f"echo 'Simulating terraform apply for: {prompt}' && sleep 2")
            return {
                "status": "success" if command_result["success"] else "failed",
                "infrastructure_result": command_result["stdout"],
                "exit_code": command_result["exit_code"],
            }

        elif "health check" in prompt.lower() or "latency" in prompt.lower():
            command_result = self.run_command("ping -c 3 8.8.8.8")
            return {
                "status": "success" if command_result["success"] else "failed",
                "network_health": command_result["stdout"],
            }
        else:
            command_result = self.run_command(f"echo 'Unknown execution intent: {prompt}'")
            return {"status": "success", "result": command_result["stdout"]}
