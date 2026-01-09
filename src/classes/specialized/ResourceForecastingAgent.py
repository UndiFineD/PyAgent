import time
import random
from typing import Dict, List, Any
from src.classes.base_agent import BaseAgent

class ResourceForecastingAgent(BaseAgent):
    """
    Resource Forecasting Agent: Predicts future compute, storage, and 
    network requirements based on historical fleet activity trends.
    """
    def __init__(self, workspace_path: str) -> None:
        super().__init__(workspace_path)
        self.workspace_path = workspace_path
        self.usage_history = [] # List of snapshots

    def log_usage_snapshot(self, compute_units: float, storage_gb: float, network_mbps: float) -> str:
        """Logs a current snapshot of resource usage."""
        snapshot = {
            "timestamp": time.time(),
            "compute": compute_units,
            "storage": storage_gb,
            "network": network_mbps
        }
        self.usage_history.append(snapshot)
        return snapshot

    def predict_future_needs(self, horizon_hours: int = 24) -> Dict[str, Any]:
        """Predicts resource needs for the specified future horizon."""
        if len(self.usage_history) < 2:
            return {"status": "Incomplete Data", "prediction": None}

        # Simple linear trend extrapolation for simulation
        first = self.usage_history[0]
        last = self.usage_history[-1]
        t_delta = last['timestamp'] - first['timestamp']
        
        if t_delta == 0:
            return {"status": "Zero Time Delta", "prediction": None}

        def extrapolate(key) -> str:
            rate = (last[key] - first[key]) / t_delta
            return last[key] + (rate * horizon_hours * 3600)

        prediction = {
            "compute": max(0, extrapolate('compute')),
            "storage": max(0, extrapolate('storage')),
            "network": max(0, extrapolate('network')),
            "horizon_hours": horizon_hours
        }

        return {
            "status": "Success",
            "prediction": prediction,
            "confidence": 0.7 if len(self.usage_history) > 10 else 0.4
        }

    def get_scaling_recommendation(self) -> str:
        """Suggests whether to scale up or down based on forecasts."""
        forecast = self.predict_future_needs()
        if forecast['status'] != "Success":
            return "Wait for more data."
        
        pred = forecast['prediction']
        if pred['compute'] > 100 or pred['storage'] > 500:
            return "Recommend SCALE_UP: Resource exhaustion predicted."
        elif pred['compute'] < 10 and len(self.usage_history) > 5:
            return "Recommend SCALE_DOWN: Resource underutilization predicted."
        return "Maintain current scale."
