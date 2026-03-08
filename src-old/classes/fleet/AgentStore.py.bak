#!/usr/bin/env python3

"""Agent Store for sharing specialized agent configurations and templates.
Allows agents to 'buy' or download new capabilities.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

class AgentStore:
    """Marketplace for agent templates and specialized configurations."""

    def __init__(self, store_path: str) -> None:
        self.store_path: Path = Path(store_path)
        self.store_path.mkdir(parents=True, exist_ok=True)
        self.templates: Dict[str, Dict[str, Any]] = {
            "SqlExpert": {
                "base": "DataAgent",
                "config": {"mode": "sql_only", "engine": "sqlite"},
                "price": 50.0
            },
            "PythonOptimizer": {
                "base": "CoderAgent",
                "config": {"lint": True, "refactor_level": "aggresive"},
                "price": 75.0
            }
        }

    def list_templates(self) -> Dict[str, Dict[str, Any]]:
        return self.templates

    def purchase_template(self, agent_id: str, template_name: str, economy: Any) -> Optional[Dict[str, Any]]:
        """Purchases a template using agent credits."""
        if template_name not in self.templates:
            return None
            
        template: Dict[str, Any] = self.templates[template_name]
        price: float = float(template["price"])
        
        if hasattr(economy, "transfer_credits") and economy.transfer_credits(agent_id, "STORE", price, f"Purchase template: {template_name}"):
            logging.info(f"{agent_id} purchased {template_name} for {price} credits.")
            return template
            
        return None

from typing import Optional
