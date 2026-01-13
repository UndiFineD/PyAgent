#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors

import json
import time
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

class SwarmBenchmark:
    """Automated benchmark regression and tracking for the PyAgent Swarm."""

    def __init__(self, history_file: str = "data/benchmarks/history.json") -> None:
        self.history_file = Path(history_file)
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        self.history = self._load_history()

    def _load_history(self) -> List[Dict[str, Any]]:
        if self.history_file.exists():
            try:
                return json.loads(self.history_file.read_text())
            except Exception as e:
                logging.error(f"Failed to load benchmark history: {e}")
        return []

    def save_metrics(self, current_metrics: Dict[str, Any]) -> None:
        """Saves current benchmark metrics to history."""
        self.history.append({
            "timestamp": time.time(),
            "metrics": current_metrics
        })
        # Keep only last 100 runs
        if len(self.history) > 100:
            self.history = self.history[-100:]
            
        try:
            self.history_file.write_text(json.dumps(self.history, indent=2))
        except Exception as e:
            logging.error(f"Failed to save benchmark metrics: {e}")

    def check_regression(self, current_ttft: float) -> bool:
        """
        Checks if current TTFT (Time to First Token) has regressed.
        Fails if it increased by more than 10% compared to average.
        """
        if not self.history:
            logging.info("No benchmark history found. Skipping regression check.")
            return True

        # Calculate average TTFT from history
        historical_ttfts = [run['metrics'].get('ttft', 0) for run in self.history if 'ttft' in run['metrics']]
        if not historical_ttfts:
            return True

        avg_ttft = sum(historical_ttfts) / len(historical_ttfts)
        threshold = avg_ttft * 1.10 # 10% buffer
        
        if current_ttft > threshold:
            logging.error(f"PERFORMANCE REGRESSION DETECTED!")
            logging.error(f"Current TTFT: {current_ttft:.4f}s | Avg TTFT: {avg_ttft:.4f}s | Threshold: {threshold:.4f}s")
            return False
            
        logging.info(f"Performance check passed: TTFT {current_ttft:.4f}s is within 10% of history ({avg_ttft:.4f}s)")
        return True

if __name__ == "__main__":
    # Example usage
    benchmark = SwarmBenchmark()
    current_val = 0.55 # Simulated current TTFT
    if benchmark.check_regression(current_val):
        benchmark.save_metrics({"ttft": current_val, "files_processed": 10})
    else:
        print("Performance gate failed.")
