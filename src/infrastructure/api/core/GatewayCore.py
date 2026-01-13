
from __future__ import annotations
from typing import Dict, Any, Optional

class GatewayCore:
    """
    GatewayCore implements logic for SaaS service integration and load balancing.
    It manages service routing and 'Interface Affinity'.
    """

    def __init__(self) -> None:
        # Service registry for SaaS tools
        self.saas_registry: dict[str, str] = {
            "jira": "https://api.atlassian.com/ex/jira/",
            "slack": "https://slack.com/api/",
            "trello": "https://api.trello.com/1/"
        }
        
        # Interface affinity rules: interface -> model_preference
        self.interface_affinity: dict[str, str] = {
            "web_ui": "glm-4-flash",
            "cli": "gpt-4o",
            "gui": "claude-3-haiku",
            "background": "llama-3-70b"
        }

    def get_service_endpoint(self, service_name: str) -> str | None:
        """Returns the base URL for a registered SaaS service."""
        return self.saas_registry.get(service_name.lower())

    def resolve_model_by_affinity(self, interface_type: str) -> str:
        """
        Resolves the preferred LLM model based on the calling interface.
        Prioritizes speed for UI/Frontend.
        """
        return self.interface_affinity.get(interface_type.lower(), "gpt-4o")

    def format_saas_request(self, service: str, action: str, params: dict[str, Any]) -> dict[str, Any]:
        """Constructs a standardized internal request for external SaaS consumption."""
        return {
            "service": service,
            "action": action,
            "params": params,
            "method": "POST" if action in ["create", "update"] else "GET"
        }