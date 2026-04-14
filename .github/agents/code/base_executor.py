import subprocess
import logging
from pathlib import Path

class AgentExecutor:
    """Base class for all fast-path Python agents running on distributed nodes."""
    
    def __init__(self):
        self.workspace = Path("/tmp/agent_workspaces")
        self.workspace.mkdir(parents=True, exist_ok=True)
        
    def execute(self, payload: dict) -> dict:
        """Override this in specific agents. Returns a result dictionary."""
        return {"status": "success", "message": "Default executor finished."}

    def run_command(self, cmd: str, timeout: int = 300) -> dict:
        """Securely run a shell command on the host node and return structured stdout/stderr."""
        logging.info(f"Running command: {cmd}")
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                cwd=str(self.workspace),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=timeout
            )
            return {
                "exit_code": result.returncode,
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip(),
                "success": result.returncode == 0
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Command timed out", "exit_code": 124}
        except Exception as e:
            return {"success": False, "error": str(e), "exit_code": -1}
