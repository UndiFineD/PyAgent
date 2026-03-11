r"""LLM_CONTEXT_START

## Source: src-old/classes/specialized/CloudProviderAgent.description.md

# CloudProviderAgent

**File**: `src\classes\specialized\CloudProviderAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 49  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for CloudProviderAgent.

## Classes (1)

### `CloudProviderAgent`

**Inherits from**: BaseAgent

Phase 56: Multi-Cloud Infrastructure as Code.
Manages cloud credentials, region selection, and generates IaC templates.

**Methods** (4):
- `__init__(self, path)`
- `configure_provider(self, provider, credentials_mock)`
- `generate_terraform_template(self, provider, node_count, region)`
- `select_optimal_region(self, latency_data)`

## Dependencies

**Imports** (7):
- `json`
- `os`
- `src.classes.base_agent.BaseAgent`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/classes/specialized/CloudProviderAgent.improvements.md

# Improvements for CloudProviderAgent

**File**: `src\classes\specialized\CloudProviderAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 49 lines (small)  
**Complexity**: 4 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `CloudProviderAgent_test.py` with pytest tests

## Best Practices Checklist

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

from typing import Dict

from src.classes.base_agent import BaseAgent


class CloudProviderAgent(BaseAgent):
    """Phase 56: Multi-Cloud Infrastructure as Code.
    Manages cloud credentials, region selection, and generates IaC templates.
    """

    def __init__(self, path: str) -> None:
        super().__init__(path)
        self.supported_providers = ["aws", "azure", "gcp"]
        self.credentials: Dict[str, bool] = {p: False for p in self.supported_providers}

    def configure_provider(
        self, provider: str, credentials_mock: Dict[str, str]
    ) -> str:
        """Mocks the configuration of a cloud provider."""
        if provider.lower() in self.supported_providers:
            self.credentials[provider.lower()] = True
            return f"Provider {provider} configured successfully."
        return f"Provider {provider} not supported."

    def generate_terraform_template(
        self, provider: str, node_count: int, region: str = "us-east-1"
    ) -> str:
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
            return "us-east-1"  # Default
        return min(latency_data, key=latency_data.get)
