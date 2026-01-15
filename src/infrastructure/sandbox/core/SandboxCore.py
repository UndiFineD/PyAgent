
from __future__ import annotations
import typing
from dataclasses import dataclass, field




@dataclass(frozen=True)
class SandboxConfig:
    """Immutable configuration for agent sandboxing."""
    cpu_limit: float = 0.5




    memory_mb: int = 512
    network_enabled: bool = False
    read_only_paths: list[str] = field(default_factory=list)
    timeout_sec: int = 30



class SandboxCore:
    """Pure logic for containerized agent runtimes and resource isolation.
    Handles enforcement logic, quota calculations, and security constraints.
    """

    def validate_code_execution(self, code: str, config: SandboxConfig) -> dict[str, typing.Any]:
        """Validates if code execution fits within sandbox constraints."""
        issues = []
        if "os.system" in code or "subprocess" in code:
            issues.append("External process execution forbidden.")

        if not config.network_enabled and ("requests" in code or "socket" in code):
            issues.append("Network access disabled for this sandbox.")

        return {
            "allowed": len(issues) == 0,
            "issues": issues,
            "quota": {
                "cpu": f"{config.cpu_limit} cores",
                "mem": f"{config.memory_mb}MB"
            }
        }

    def calculate_resource_usage(self, start_cpu: float, end_cpu: float, duration: float) -> float:
        """Calculates normalized resource usage score."""
        if duration <= 0:
            return 0.0
        return (end_cpu - start_cpu) / duration

    def get_security_profile(self, risk_level: str) -> SandboxConfig:
        """Returns sandbox config based on risk assessment."""
        if risk_level == "high":
            return SandboxConfig(cpu_limit=0.1, memory_mb=128, network_enabled=False)
        return SandboxConfig()
