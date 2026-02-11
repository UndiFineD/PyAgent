#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""
CloudProviderAgent: System agent for managing cloud provider integrations and resource provisioning.

Supports multi-cloud, hybrid, and distributed cloud operations within the PyAgent swarm.
"""


from __future__ import annotations

from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class CloudProviderAgent(BaseAgent):
    """
    Phase 56: Multi-Cloud Infrastructure as Code.
    Manages cloud credentials, region selection, and generates IaC templates.
    """

    def __init__(self, path: str) -> None:
        super().__init__(path)
        self.supported_providers = ["aws", "azure", "gcp"]
        self.credentials: dict[str, bool] = {p: False for p in self.supported_providers}

    def configure_provider(self, provider: str, credentials_mock: dict[str, str]) -> str:  # noqa: ARG002
        """Mocks the configuration of a cloud provider."""
        if self.recorder:
            self.recorder.record_lesson("cloud_provider_config", {"provider": provider})

        if provider.lower() in self.supported_providers:
            self.credentials[provider.lower()] = True
            return f"Provider {provider} configured successfully."
        return f"Provider {provider} not supported."

    def generate_terraform_template(self, provider: str, node_count: int, region: str = "us-east-1") -> str:
        """Generates a basic Terraform template for fleet expansion."""
        if self.recorder:
            self.recorder.record_lesson("cloud_iac_generation", {"provider": provider, "nodes": node_count})

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

    def select_optimal_region(self, latency_data: dict[str, float]) -> str:
        """Selects the region with the lowest latency from a provided map."""
        if not latency_data:
            return "us-east-1"  # Default
        return min(latency_data, key=latency_data.get)
