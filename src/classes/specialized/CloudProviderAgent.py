import os
import json
from typing import Dict, List, Any, Optional
from src.classes.base_agent import BaseAgent

class CloudProviderAgent(BaseAgent):
    """
    Phase 56: Multi-Cloud Infrastructure as Code.
    Manages cloud credentials, region selection, and generates IaC templates.
    """
    
    def __init__(self, path: str) -> None:
        super().__init__(path)
        self.supported_providers = ["aws", "azure", "gcp"]
        self.credentials: Dict[str, bool] = {p: False for p in self.supported_providers}

    def configure_provider(self, provider: str, credentials_mock: Dict[str, str]) -> str:
        """Mocks the configuration of a cloud provider."""
        if provider.lower() in self.supported_providers:
            self.credentials[provider.lower()] = True
            return f"Provider {provider} configured successfully."
        return f"Provider {provider} not supported."

    def generate_terraform_template(self, provider: str, node_count: int, region: str = "us-east-1") -> str:
        """Generates a basic Terraform template for fleet expansion."""
        if not self.credentials.get(provider.lower()):
            return f"Error: Provider {provider} not configured."
            
        template = f"""
provider "{provider}" {{
  region = "{region}"
}}

resource "{provider}_instance" "pyagent_node" {{
  count         = {node_count}
  instance_type = "t3.medium"
  tags = {{
    Name = "PyAgent-Fleet-Node"
    Role = "Worker"
  }}
}}
"""
        return template.strip()

    def select_optimal_region(self, latency_data: Dict[str, float]) -> str:
        """Selects the region with the lowest latency from a provided map."""
        if not latency_data:
            return "us-east-1" # Default
        return min(latency_data, key=latency_data.get)
