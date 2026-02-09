# Extracted from: C:\DEV\PyAgent\.external\skills\skills\idanmann10\startclaw-optimizer\scripts\telemetry.py
#!/usr/bin/env python3
"""
Telemetry - Log runs, learn from history, recommend safe budgets.
"""

import json
import statistics
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional


class Telemetry:
    def __init__(
        self,
        history_file="~/.clawdbot/skills/openclaw-optimizer/state/task-history.jsonl",
    ):
        self.history_file = Path(history_file).expanduser()
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        self.history_file.touch()

    def log_run(
        self,
        task_type: str,
        model: str,
        browser_steps: int,
        input_tokens: int,
        output_tokens: int,
        cost: float,
        duration: float,
        success: bool,
        metadata: Optional[Dict] = None,
    ):
        """
        Log a completed run to history.
        """
        entry = {
            "timestamp": time.time(),
            "iso": datetime.now(timezone.utc).isoformat(),
            "task_type": task_type,
            "model": model,
            "browser_steps": browser_steps,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cost": round(cost, 4),
            "duration": round(duration, 2),
            "success": success,
            "metadata": metadata or {},
        }

        with open(self.history_file, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def get_history(
        self, task_type: Optional[str] = None, limit: int = 100
    ) -> List[Dict]:
        """
        Get recent history, optionally filtered by task_type.
        """
        history = []

        with open(self.history_file) as f:
            for line in f:
                if not line.strip():
                    continue
                entry = json.loads(line)
                if task_type is None or entry["task_type"] == task_type:
                    history.append(entry)

        # Return most recent N
        return history[-limit:]

    def get_stats(self, task_type: str) -> Dict:
        """
        Get statistics for a task type.
        """
        runs = self.get_history(task_type)

        if not runs:
            return {"task_type": task_type, "runs": 0, "error": "No history"}

        costs = [r["cost"] for r in runs]
        durations = [r["duration"] for r in runs]
        browser_steps = [r["browser_steps"] for r in runs]
        input_tokens = [r["input_tokens"] for r in runs]
        output_tokens = [r["output_tokens"] for r in runs]
        success_rate = sum(1 for r in runs if r["success"]) / len(runs)

        return {
            "task_type": task_type,
            "runs": len(runs),
            "success_rate": round(success_rate, 2),
            "cost": {
                "mean": round(statistics.mean(costs), 4),
                "p50": round(statistics.median(costs), 4),
                "p90": round(self._percentile(costs, 0.9), 4),
                "max": round(max(costs), 4),
            },
            "duration": {
                "mean": round(statistics.mean(durations), 2),
                "p50": round(statistics.median(durations), 2),
                "p90": round(self._percentile(durations, 0.9), 2),
            },
            "browser_steps": {
                "mean": round(statistics.mean(browser_steps), 1),
                "p90": round(self._percentile(browser_steps, 0.9), 1),
            },
            "tokens": {
                "input_mean": int(statistics.mean(input_tokens)),
                "output_mean": int(statistics.mean(output_tokens)),
            },
        }

    def recommend_budget(self, task_type: str) -> Dict:
        """
        Recommend safe budget_soft and budget_max based on history.
        """
        stats = self.get_stats(task_type)

        if "error" in stats:
            # No history - use defaults
            return {
                "budget_soft": 0.10,  # $0.10
                "budget_max": 0.20,  # $0.20
                "confidence": "low",
                "reason": "No historical data - using defaults",
            }

        # budget_soft = p50 + 20% buffer
        # budget_max = p90 + 50% buffer
        budget_soft = stats["cost"]["p50"] * 1.2
        budget_max = stats["cost"]["p90"] * 1.5

        # Enforce minimum budgets
        budget_soft = max(budget_soft, 0.05)
        budget_max = max(budget_max, 0.10)

        confidence = (
            "high" if stats["runs"] >= 10 else "medium" if stats["runs"] >= 5 else "low"
        )

        return {
            "budget_soft": round(budget_soft, 3),
            "budget_max": round(budget_max, 3),
            "confidence": confidence,
            "based_on_runs": stats["runs"],
            "stats": stats,
        }

    def _percentile(self, data: List[float], p: float) -> float:
        """Calculate percentile."""
        sorted_data = sorted(data)
        index = int(len(sorted_data) * p)
        return sorted_data[min(index, len(sorted_data) - 1)]


if __name__ == "__main__":
    import sys

    telem = Telemetry()

    if len(sys.argv) < 2:
        print("Usage: telemetry.py <action>")
        print("\nActions:")
        print(
            "  log <task_type> <model> <steps> <in_tok> <out_tok> <cost> <dur> <success>"
        )
        print("  stats <task_type>")
        print("  recommend <task_type>")
        print("  history [task_type] [limit]")
        sys.exit(1)

    action = sys.argv[1]

    if action == "log":
        task_type = sys.argv[2]
        model = sys.argv[3]
        browser_steps = int(sys.argv[4])
        input_tokens = int(sys.argv[5])
        output_tokens = int(sys.argv[6])
        cost = float(sys.argv[7])
        duration = float(sys.argv[8])
        success = sys.argv[9].lower() in ["true", "1", "yes"]

        telem.log_run(
            task_type,
            model,
            browser_steps,
            input_tokens,
            output_tokens,
            cost,
            duration,
            success,
        )
        print("✅ Run logged")

    elif action == "stats":
        task_type = sys.argv[2]
        stats = telem.get_stats(task_type)

        if "error" in stats:
            print(f"❌ {stats['error']}")
            sys.exit(1)

        print(f"📊 Stats for '{task_type}' ({stats['runs']} runs)")
        print(f"\nSuccess rate: {stats['success_rate']*100:.0f}%")
        print(f"\nCost:")
        print(f"  Mean: ${stats['cost']['mean']:.4f}")
        print(f"  P50:  ${stats['cost']['p50']:.4f}")
        print(f"  P90:  ${stats['cost']['p90']:.4f}")
        print(f"  Max:  ${stats['cost']['max']:.4f}")
        print(f"\nDuration:")
        print(f"  Mean: {stats['duration']['mean']}s")
        print(f"  P90:  {stats['duration']['p90']}s")
        print(f"\nBrowser steps:")
        print(f"  Mean: {stats['browser_steps']['mean']}")
        print(f"  P90:  {stats['browser_steps']['p90']}")
        print(f"\nTokens:")
        print(f"  Input:  {stats['tokens']['input_mean']:,}")
        print(f"  Output: {stats['tokens']['output_mean']:,}")

    elif action == "recommend":
        task_type = sys.argv[2]
        rec = telem.recommend_budget(task_type)

        print(f"💡 Budget recommendation for '{task_type}'")
        print(f"\nBudget soft: ${rec['budget_soft']:.3f}")
        print(f"Budget max:  ${rec['budget_max']:.3f}")
        print(f"\nConfidence: {rec['confidence']}")
        if "based_on_runs" in rec:
            print(f"Based on: {rec['based_on_runs']} runs")
        print(f"Reason: {rec.get('reason', 'Historical data')}")

    elif action == "history":
        task_type = sys.argv[2] if len(sys.argv) > 2 else None
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 10

        history = telem.get_history(task_type, limit)

        print(f"📜 Recent runs ({len(history)}):")
        for entry in history[-10:]:
            success_icon = "✅" if entry["success"] else "❌"
            print(
                f"{success_icon} {entry['iso']} | {entry['task_type']} | "
                f"{entry['model'][:20]:<20} | ${entry['cost']:.3f} | {entry['duration']}s"
            )
