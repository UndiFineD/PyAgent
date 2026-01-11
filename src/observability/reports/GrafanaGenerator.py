#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, Any, List


































from src.core.base.version import VERSION
__version__ = VERSION

class GrafanaDashboardGenerator:
    """
    Generates Grafana JSON dashboard configurations for PyAgent swarm observability.
    Supports monitoring fleet metrics, agent health, and shard performance.
    """
    
    def __init__(self, output_dir: str = "deploy/grafana/dashboards") -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_fleet_summary(self) -> str:
        """Generates a summary dashboard for the entire fleet."""
        dashboard = {
            "title": "PyAgent Fleet Summary",
            "panels": [
                {
                    "title": "Agent Count",
                    "type": "stat",
                    "targets": [{"expr": "count(agent_up)"}]
                },
                {
                    "title": "Fleet Latency",
                    "type": "timeseries",
                    "targets": [{"expr": "rate(fleet_request_duration_seconds_sum[5m])"}]
                }
            ],
            "schemaVersion": 36,
            "uid": "pyagent-fleet-summary"
        }
        
        output_path = self.output_dir / "fleet_summary.json"
        output_path.write_text(json.dumps(dashboard, indent=2))
        return str(output_path)

    def generate_shard_obs(self, shard_name: str) -> str:
        """Generates a dashboard for a specific swarm shard."""
        dashboard = {
            "title": f"PyAgent Shard: {shard_name}",
            "panels": [
                {
                    "title": "Shard Load",
                    "type": "gauge",
                    "targets": [{"expr": f"shard_load{{shard='{shard_name}'}} "}]
                }
            ],
            "schemaVersion": 36,
            "uid": f"shard-{shard_name}"
        }
        
        output_path = self.output_dir / f"shard_{shard_name}.json"
        output_path.write_text(json.dumps(dashboard, indent=2))
        return str(output_path)
