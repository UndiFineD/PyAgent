# Extracted from: C:\DEV\PyAgent\.external\skills\skills\idanmann10\startclaw-optimizer\scripts\cost_guard.py
#!/usr/bin/env python3
"""
Cost Guard - Predict, track, and enforce budgets with graceful degradation.
"""

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Optional, Tuple

# Pricing per million tokens
PRICING = {
    "anthropic/claude-3-5-haiku-latest": {"input": 3.00, "output": 15.00},
    "anthropic/claude-3-5-haiku-latest": {"input": 0.80, "output": 4.00},
}


class CostGuard:
    def __init__(self, state_file="~/.clawdbot/skills/openclaw-optimizer/state/cost-state.json"):
        self.state_file = Path(state_file).expanduser()
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.ensure_state()

    def ensure_state(self):
        """Create state file if missing."""
        if not self.state_file.exists():
            self.save_state({"active_tasks": {}, "daily_total": 0.0, "date": self.today()})

    def today(self):
        """Get today's date in UTC."""
        return datetime.now(timezone.utc).strftime("%Y-%m-%d")

    def load_state(self):
        """Load cost state, resetting if new day."""
        with open(self.state_file) as f:
            state = json.load(f)

        # Reset if new day
        if state["date"] != self.today():
            state = {"active_tasks": {}, "daily_total": 0.0, "date": self.today()}
            self.save_state(state)

        return state

    def save_state(self, state):
        """Save cost state."""
        with open(self.state_file, "w") as f:
            json.dump(state, f, indent=2)

    def predict_cost(self, model: str, estimated_input: int, estimated_output: int) -> float:
        """
        Predict cost for a task.
        Returns estimated cost in dollars.
        """
        if model not in PRICING:
            # Default to Sonnet pricing (conservative)
            pricing = PRICING["anthropic/claude-3-5-haiku-latest"]
        else:
            pricing = PRICING[model]

        input_cost = (estimated_input / 1_000_000) * pricing["input"]
        output_cost = (estimated_output / 1_000_000) * pricing["output"]

        return input_cost + output_cost

    def start_task(
        self,
        task_id: str,
        budget_soft: float,
        budget_max: float,
        model: str,
        estimated_input: int,
        estimated_output: int,
    ) -> Tuple[bool, str, Dict]:
        """
        Start tracking a task. Returns (allowed, reason, task_state).
        """
        state = self.load_state()

        # Predict cost
        predicted = self.predict_cost(model, estimated_input, estimated_output)

        # Check if it would exceed budget
        if predicted > budget_max:
            return (
                False,
                f"Predicted cost (${predicted:.3f}) exceeds budget_max (${budget_max:.3f})",
                {},
            )

        # Warn if close to soft limit
        warning = None
        if predicted > budget_soft:
            warning = f"Predicted cost (${predicted:.3f}) exceeds budget_soft (${budget_soft:.3f})"

        # Create task state
        task_state = {
            "task_id": task_id,
            "budget_soft": budget_soft,
            "budget_max": budget_max,
            "model": model,
            "predicted_cost": round(predicted, 4),
            "actual_cost": 0.0,
            "started_at": time.time(),
            "warning": warning,
            "degraded": False,
        }

        state["active_tasks"][task_id] = task_state
        self.save_state(state)

        return True, warning or "OK", task_state

    def log_spend(self, task_id: str, input_tokens: int, output_tokens: int, model: str) -> Tuple[str, Dict]:
        """
        Log spending for a task. Returns (status, task_state).
        Status: OK | SOFT_LIMIT | HARD_LIMIT
        """
        state = self.load_state()

        if task_id not in state["active_tasks"]:
            return "ERROR", {}

        task = state["active_tasks"][task_id]

        # Calculate cost
        cost = self.predict_cost(model, input_tokens, output_tokens)
        task["actual_cost"] += cost
        state["daily_total"] += cost

        # Check limits
        if task["actual_cost"] >= task["budget_max"]:
            task["status"] = "HARD_LIMIT"
            self.save_state(state)
            return "HARD_LIMIT", task

        if task["actual_cost"] >= task["budget_soft"] and not task["degraded"]:
            task["status"] = "SOFT_LIMIT"
            task["degraded"] = True
            self.save_state(state)
            return "SOFT_LIMIT", task

        task["status"] = "OK"
        self.save_state(state)
        return "OK", task

    def degrade_task(self, task_id: str) -> Dict:
        """
        Apply degradation to task (switch to cheaper model, reduce steps, etc.).
        Returns degradation recommendations.
        """
        state = self.load_state()

        if task_id not in state["active_tasks"]:
            return {}

        task = state["active_tasks"][task_id]

        recommendations = {
            "switch_model": "anthropic/claude-3-5-haiku-latest",
            "reduce_browser_steps": True,
            "max_browser_steps": 5,
            "use_cache": True,
            "skip_browsing": task["actual_cost"] > task["budget_soft"] * 1.2,
            "reason": f"Soft limit exceeded: ${task['actual_cost']:.3f} / ${task['budget_soft']:.3f}",
        }

        return recommendations

    def finish_task(self, task_id: str) -> Dict:
        """
        Finish a task and return summary.
        """
        state = self.load_state()

        if task_id not in state["active_tasks"]:
            return {}

        task = state["active_tasks"][task_id]
        task["finished_at"] = time.time()
        task["duration"] = round(task["finished_at"] - task["started_at"], 2)

        # Remove from active tasks
        summary = task.copy()
        del state["active_tasks"][task_id]
        self.save_state(state)

        return summary

    def get_daily_total(self) -> float:
        """Get total daily spending."""
        state = self.load_state()
        return state["daily_total"]


if __name__ == "__main__":
    import sys

    guard = CostGuard()

    if len(sys.argv) < 2:
        print("Usage: cost_guard.py <action>")
        print("\nActions:")
        print("  predict <model> <input_tokens> <output_tokens>")
        print("  start <task_id> <budget_soft> <budget_max> <model> <est_input> <est_output>")
        print("  log <task_id> <input_tokens> <output_tokens> <model>")
        print("  degrade <task_id>")
        print("  finish <task_id>")
        print("  daily")
        sys.exit(1)

    action = sys.argv[1]

    if action == "predict":
        model = sys.argv[2]
        input_tokens = int(sys.argv[3])
        output_tokens = int(sys.argv[4])
        cost = guard.predict_cost(model, input_tokens, output_tokens)
        print(f"Predicted cost: ${cost:.4f}")

    elif action == "start":
        task_id = sys.argv[2]
        budget_soft = float(sys.argv[3])
        budget_max = float(sys.argv[4])
        model = sys.argv[5]
        est_input = int(sys.argv[6])
        est_output = int(sys.argv[7])

        allowed, reason, task_state = guard.start_task(task_id, budget_soft, budget_max, model, est_input, est_output)

        if allowed:
            print(f"✅ Task started")
            print(f"Predicted: ${task_state['predicted_cost']:.4f}")
            if task_state["warning"]:
                print(f"⚠️  {task_state['warning']}")
        else:
            print(f"❌ {reason}")
            sys.exit(1)

    elif action == "log":
        task_id = sys.argv[2]
        input_tokens = int(sys.argv[3])
        output_tokens = int(sys.argv[4])
        model = sys.argv[5]

        status, task = guard.log_spend(task_id, input_tokens, output_tokens, model)

        print(f"Status: {status}")
        print(f"Actual cost: ${task['actual_cost']:.4f}")
        print(f"Budget soft: ${task['budget_soft']:.4f}")
        print(f"Budget max: ${task['budget_max']:.4f}")

        if status == "SOFT_LIMIT":
            print("⚠️  Soft limit exceeded - consider degradation")
        elif status == "HARD_LIMIT":
            print("🛑 Hard limit exceeded - stop task")
            sys.exit(1)

    elif action == "degrade":
        task_id = sys.argv[2]
        recs = guard.degrade_task(task_id)

        print("Degradation recommendations:")
        print(f"  Switch model: {recs.get('switch_model', 'N/A')}")
        print(f"  Reduce browser steps: {recs.get('reduce_browser_steps', False)}")
        print(f"  Max steps: {recs.get('max_browser_steps', 'N/A')}")
        print(f"  Use cache: {recs.get('use_cache', False)}")
        print(f"  Skip browsing: {recs.get('skip_browsing', False)}")
        print(f"  Reason: {recs.get('reason', 'N/A')}")

    elif action == "finish":
        task_id = sys.argv[2]
        summary = guard.finish_task(task_id)

        print("Task finished:")
        print(f"  Duration: {summary.get('duration', 0)}s")
        print(f"  Predicted: ${summary.get('predicted_cost', 0):.4f}")
        print(f"  Actual: ${summary.get('actual_cost', 0):.4f}")
        print(f"  Status: {summary.get('status', 'UNKNOWN')}")

    elif action == "daily":
        total = guard.get_daily_total()
        print(f"Daily total: ${total:.2f}")
