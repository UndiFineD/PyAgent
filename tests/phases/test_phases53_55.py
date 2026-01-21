import unittest
import asyncio
from unittest import IsolatedAsyncioTestCase
from pathlib import Path
from src.infrastructure.fleet.fleet_manager import FleetManager


class TestPhases53_55(IsolatedAsyncioTestCase):
    def setUp(self):
        self.workspace = str(Path(__file__).resolve().parents[2])
        self.fleet = FleetManager(self.workspace)

    async def test_resource_prediction(self) -> None:
        print("\nTesting Phase 53: Predictive Resource Forecasting...")
        # Mock some metrics
        from src.observability.stats.metrics import AgentMetric

        metrics = [
            AgentMetric("AgentA", "task", 100.0, token_count=1000),
            AgentMetric("AgentA", "task", 110.0, token_count=1500),
            AgentMetric("AgentA", "task", 120.0, token_count=2000),
            AgentMetric("AgentA", "task", 130.0, token_count=3000),
            AgentMetric("AgentA", "task", 140.0, token_count=4000),
        ]
        res = self.fleet.resource_predictor.ingest_metrics(metrics)
        if asyncio.iscoroutine(res):
            await res

        forecast = self.fleet.resource_predictor.forecast_usage()
        if asyncio.iscoroutine(forecast):
            forecast = await forecast
        print(f"Forecast: {forecast}")
        self.assertGreater(forecast["forecasted_tokens"], 2000)

        scaling = self.fleet.resource_predictor.evaluate_scaling_needs(2)
        if asyncio.iscoroutine(scaling):
            scaling = await scaling
        print(f"Scaling Recommendation: {scaling}")
        self.assertTrue(scaling["trigger_scaling"])

    async def test_ui_architecture(self) -> None:
        print("\nTesting Phase 54: Generative UI Architecture...")
        layout = self.fleet.ui_architect.design_dashboard_layout(
            "Code Refactor",
            ["AgentA", "AgentB", "AgentC", "AgentD", "AgentE", "AgentF"],
        )
        if asyncio.iscoroutine(layout):
            layout = await layout
        print(f"Layout Panels: {len(layout['panels'])}")
        # Should have 'Agent Heatmap' because list > 5
        panel_titles = [p["title"] for p in layout["panels"]]
        self.assertIn("Agent Heatmap", panel_titles)

        manifest = self.fleet.ui_architect.generate_ui_manifest(
            "Let's run some SQL queries and plot the results."
        )
        if asyncio.iscoroutine(manifest):
            manifest = await manifest
        print(f"UI Manifest Plugins: {manifest['requested_plugins']}")

        self.assertIn("SQL_Explorer", manifest["requested_plugins"])
        self.assertIn("Data_Visualizer", manifest["requested_plugins"])

    async def test_dbft_consensus(self) -> None:
        print("\nTesting Phase 55: DBFT Consensus...")

        # Testing verify_state_block directly
        # This will also trigger the inter-fleet bridge broadcast
        res = self.fleet.consensus_orchestrator.verify_state_block(
            "Refactor UI", "Change button color to blue"
        )
        if asyncio.iscoroutine(res):
            await res

        # Check if the signal was 'broadcast' (simulated in InterFleetBridge shared_state_cache)
        bridge = self.fleet.inter_fleet_bridge
        self.assertIn("SIGNAL_CONSENSUS_CRYPTO_VERIFIED", bridge.shared_state_cache)
        print("DBFT Signal successfully broadcast to bridge.")


if __name__ == "__main__":
    unittest.main()
