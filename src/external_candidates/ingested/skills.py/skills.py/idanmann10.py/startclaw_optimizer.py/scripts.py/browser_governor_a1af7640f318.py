# Extracted from: C:\DEV\PyAgent\.external\skills\skills\idanmann10\startclaw-optimizer\scripts\browser_governor.py
#!/usr/bin/env python3
"""
Browser Governor - Enforce single browser usage, prevent loops, manage queue.
"""

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Optional, Tuple


class BrowserGovernor:
    def __init__(
        self, lock_file="~/.clawdbot/skills/openclaw-optimizer/state/browser-lock.json"
    ):
        self.lock_file = Path(lock_file).expanduser()
        self.lock_file.parent.mkdir(parents=True, exist_ok=True)
        self.max_steps = 20  # Hard cap on browser steps per session
        self.timeout = 300  # 5 minutes max browser session

    def acquire_lock(self, agent_id: str, task: str) -> bool:
        """
        Try to acquire browser lock. Returns True if acquired, False if locked.
        """
        if self.lock_file.exists():
            with open(self.lock_file) as f:
                lock = json.load(f)

            # Check if lock is stale (older than timeout)
            lock_age = time.time() - lock["timestamp"]
            if lock_age > self.timeout:
                print(f"Stale lock detected ({lock_age:.0f}s old). Breaking lock.")
                self.release_lock()
            else:
                # Lock is valid
                return False

        # Create lock
        lock = {
            "agent_id": agent_id,
            "task": task,
            "timestamp": time.time(),
            "iso": datetime.now(timezone.utc).isoformat(),
            "steps": 0,
        }

        with open(self.lock_file, "w") as f:
            json.dump(lock, f, indent=2)

        return True

    def release_lock(self):
        """Release browser lock."""
        if self.lock_file.exists():
            self.lock_file.unlink()

    def increment_step(self) -> bool:
        """
        Increment browser step counter. Returns False if max steps exceeded.
        """
        if not self.lock_file.exists():
            return False

        with open(self.lock_file) as f:
            lock = json.load(f)

        lock["steps"] += 1

        if lock["steps"] > self.max_steps:
            return False

        with open(self.lock_file, "w") as f:
            json.dump(lock, f, indent=2)

        return True

    def get_lock_status(self) -> Optional[Dict]:
        """Get current lock status."""
        if not self.lock_file.exists():
            return None

        with open(self.lock_file) as f:
            lock = json.load(f)

        lock_age = time.time() - lock["timestamp"]
        lock["age_seconds"] = round(lock_age, 1)
        lock["is_stale"] = lock_age > self.timeout

        return lock

    def wait_for_lock(self, agent_id: str, task: str, max_wait: int = 60) -> bool:
        """
        Wait for browser lock to become available.
        Returns True if acquired, False if timeout.
        """
        start = time.time()

        while time.time() - start < max_wait:
            if self.acquire_lock(agent_id, task):
                return True

            # Wait 5 seconds before retry
            time.sleep(5)

        return False

    def enforce_snapshot_act_pattern(self, action: str) -> Tuple[bool, str]:
        """
        Enforce snapshot → act → snapshot pattern.
        Returns (allowed, message).
        """
        if not self.lock_file.exists():
            return False, "No browser lock - acquire lock first"

        with open(self.lock_file) as f:
            lock = json.load(f)

        last_action = lock.get("last_action", None)

        # Pattern enforcement
        if action == "snapshot":
            # Snapshot always allowed
            lock["last_action"] = "snapshot"
        elif action == "act":
            # Act must follow snapshot
            if last_action != "snapshot":
                lock["last_action"] = action  # Still update
                with open(self.lock_file, "w") as f:
                    json.dump(lock, f, indent=2)
                return False, f"Act must follow snapshot (last: {last_action})"
            lock["last_action"] = "act"
        else:
            # Other actions
            lock["last_action"] = action

        with open(self.lock_file, "w") as f:
            json.dump(lock, f, indent=2)

        return True, "OK"


if __name__ == "__main__":
    import sys

    gov = BrowserGovernor()

    if len(sys.argv) < 2:
        print("Usage: browser_governor.py <action>")
        print("\nActions:")
        print("  status             - Show lock status")
        print("  acquire <id> <task> - Acquire lock")
        print("  release            - Release lock")
        print("  step               - Increment step counter")
        print("  wait <id> <task>   - Wait for lock")
        sys.exit(1)

    action = sys.argv[1]

    if action == "status":
        status = gov.get_lock_status()
        if status:
            print(f"🔒 Browser LOCKED")
            print(f"Agent: {status['agent_id']}")
            print(f"Task: {status['task']}")
            print(f"Steps: {status['steps']}/{gov.max_steps}")
            print(f"Age: {status['age_seconds']}s")
            if status["is_stale"]:
                print("⚠️  STALE LOCK (>5min)")
        else:
            print("🟢 Browser AVAILABLE")

    elif action == "acquire":
        if len(sys.argv) < 4:
            print("Usage: browser_governor.py acquire <agent_id> <task>")
            sys.exit(1)

        agent_id = sys.argv[2]
        task = " ".join(sys.argv[3:])

        if gov.acquire_lock(agent_id, task):
            print("✅ Lock acquired")
        else:
            status = gov.get_lock_status()
            print(f"❌ Browser locked by {status['agent_id']}")
            print(f"Task: {status['task']}")
            print(f"Age: {status['age_seconds']}s")
            sys.exit(1)

    elif action == "release":
        gov.release_lock()
        print("✅ Lock released")

    elif action == "step":
        if gov.increment_step():
            status = gov.get_lock_status()
            print(f"✅ Step {status['steps']}/{gov.max_steps}")
        else:
            print(f"❌ Max steps ({gov.max_steps}) exceeded")
            sys.exit(1)

    elif action == "wait":
        if len(sys.argv) < 4:
            print("Usage: browser_governor.py wait <agent_id> <task>")
            sys.exit(1)

        agent_id = sys.argv[2]
        task = " ".join(sys.argv[3:])

        print("⏳ Waiting for browser lock...")
        if gov.wait_for_lock(agent_id, task):
            print("✅ Lock acquired")
        else:
            print("❌ Timeout waiting for lock")
            sys.exit(1)
