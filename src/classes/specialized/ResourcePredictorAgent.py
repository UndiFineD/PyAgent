import time
import logging
from typing import Dict, List, Any, Optional
from src.classes.base_agent import BaseAgent

class ResourcePredictorAgent(BaseAgent):
    """
    Phase 53: Predictive Resource Forecasting.
    Uses historical telemetry to forecast future token usage and compute needs.
    """
    
    def __init__(self, path: str) -> None:
        super().__init__(path)
        self.usage_history: List[Dict[str, Any]] = []
        self.prediction_window = 10 # Number of steps to look ahead

    def ingest_metrics(self, metrics: List[Any]):
        """Ingests recent agent metrics for analysis."""
        for m in metrics:
            # We assume 'm' is an AgentMetric-like object or dict
            self.usage_history.append({
                "timestamp": getattr(m, 'timestamp', time.time()),
                "tokens": getattr(m, 'token_count', 0),
                "agent": getattr(m, 'agent_name', "unknown")
            })
            
        # Keep history manageable
        if len(self.usage_history) > 1000:
            self.usage_history = self.usage_history[-1000:]

    def forecast_usage(self) -> Dict[str, Any]:
        """
        Forecasts usage for the next cycle.
        Uses simple linear extrapolation of the last N events.
        """
        if len(self.usage_history) < 5:
            return {"forecasted_tokens": 0, "confidence": 0.1, "action": "collect_more_data"}
            
        # Calculate moving average of token usage
        recent_usage = [h["tokens"] for h in self.usage_history[-5:]]
        avg_usage = sum(recent_usage) / len(recent_usage)
        
        # Trend analysis
        trend = recent_usage[-1] - recent_usage[0] # Very simple trend
        
        forecast = max(0, avg_usage + (trend * 0.5))
        
        return {
            "forecasted_tokens": forecast,
            "confidence": 0.8 if len(self.usage_history) > 20 else 0.4,
            "provisioning_recommendation": "scale_up" if forecast > 1000 else "stable"
        }

    def evaluate_scaling_needs(self, current_nodes: int) -> Dict[str, Any]:
        """Recommends scaling actions based on predicted load."""
        forecast = self.forecast_usage()
        needed_nodes = current_nodes
        
        if forecast["forecasted_tokens"] > 5000:
            needed_nodes += 2
        elif forecast["forecasted_tokens"] > 2000:
            needed_nodes += 1
            
        return {
            "current_nodes": current_nodes,
            "recommended_nodes": needed_nodes,
            "trigger_scaling": needed_nodes > current_nodes
        }
