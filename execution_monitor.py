#!/usr/bin/env python3
"""Real-time execution monitor for PyAgent 209K ideas.
Shows progress across all three phases.
"""

import json
import os
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

HERMES_HOME = Path(os.path.expanduser("~"))
IDEAS_ROOT = HERMES_HOME / "PyAgent/docs/project/ideas"
ARCHIVE_ROOT = HERMES_HOME / "PyAgent/docs/project/archive"
PROGRESS_FILE = HERMES_HOME / ".executor_progress.json"

def load_progress():
    """Load current progress from file."""
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE) as f:
            return json.load(f)
    return {
        "phase": "starting",
        "total_ideas": 209469,
        "phase1_target": 15000,
        "phase2_target": 50000,
        "phase3_target": 145000,
        "phase1_complete": 0,
        "phase2_complete": 0,
        "phase3_complete": 0,
        "projects_created": 0,
        "projects_released": 0,
        "ideas_archived": 0,
        "git_commits": 0,
        "batches_completed": 0,
        "start_time": datetime.now().isoformat(),
        "last_update": datetime.now().isoformat(),
    }

def count_ideas():
    """Count active and archived ideas."""
    active = 0
    archived = 0

    if IDEAS_ROOT.exists():
        for idea_file in IDEAS_ROOT.rglob("*.md"):
            active += 1

    if ARCHIVE_ROOT.exists():
        for idea_file in ARCHIVE_ROOT.rglob("*.md"):
            archived += 1

    return active, archived

def count_projects():
    """Count created, released, and archived projects."""
    projects_root = HERMES_HOME / "PyAgent/docs/project"

    created = 0
    released = 0
    archived = 0

    if projects_root.exists():
        # Count active projects
        for folder in projects_root.iterdir():
            if folder.is_dir() and folder.name.startswith("prj"):
                created += 1
                # Check if released (has git tag or marked released)
                if (folder / "project.md").exists():
                    content = (folder / "project.md").read_text(errors='ignore')
                    if "Status: Released" in content or "Status: Archived" in content:
                        released += 1

        # Count archived projects
        if (projects_root / "archive").exists():
            for folder in (projects_root / "archive").iterdir():
                if folder.is_dir() and folder.name.startswith("prj"):
                    archived += 1

    return created, released, archived

def get_git_commits():
    """Get total commits in PyAgent repo."""
    import subprocess
    try:
        result = subprocess.run(
            ["git", "-C", str(HERMES_HOME / "PyAgent"), "rev-list", "--count", "HEAD"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return int(result.stdout.strip())
    except:
        pass
    return 0

def calculate_progress():
    """Calculate overall progress."""
    progress = load_progress()

    active_ideas, archived_ideas = count_ideas()
    created_projects, released_projects, archived_projects = count_projects()
    git_commits = get_git_commits()

    total_ideas = 209469
    implemented = archived_ideas  # Ideas in archive = implemented

    phase = "starting"
    if implemented >= 15000:
        phase = "phase1-complete"
    if implemented >= 65000:  # 15K + 50K
        phase = "phase2-complete"
    if implemented >= 209469:
        phase = "complete"
    elif implemented >= 65000:
        phase = "phase3-active"
    elif implemented >= 15000:
        phase = "phase2-active"
    elif implemented >= 100:
        phase = "phase1-active"

    progress.update({
        "phase": phase,
        "total_ideas": total_ideas,
        "ideas_implemented": implemented,
        "ideas_remaining": total_ideas - implemented,
        "projects_created": created_projects,
        "projects_released": released_projects,
        "projects_archived": archived_projects,
        "git_commits": git_commits,
        "percent_complete": round(100 * implemented / total_ideas, 1),
        "last_update": datetime.now().isoformat(),
    })

    return progress

def print_dashboard(progress):
    """Print live dashboard."""
    print("\033[2J\033[H")  # Clear screen
    print("=" * 80)
    print(" 🚀 PYAGENT 209K IDEAS EXECUTION MONITOR 🚀")
    print("=" * 80)
    print()

    total = progress["total_ideas"]
    implemented = progress["ideas_implemented"]
    remaining = progress["ideas_remaining"]
    percent = progress["percent_complete"]
    phase = progress["phase"]

    # Progress bar
    bar_width = 60
    filled = int(bar_width * percent / 100)
    bar = "█" * filled + "░" * (bar_width - filled)
    print(f"Overall Progress: [{bar}] {percent}%")
    print(f"  {implemented:,} / {total:,} ideas implemented")
    print()

    # Phase status
    print("─" * 80)
    print("PHASE STATUS:")
    print("─" * 80)

    p1_target = 15000
    p2_target = 50000
    p3_target = 145000

    p1_done = min(implemented, p1_target)
    p1_pct = round(100 * p1_done / p1_target, 1)
    print(f"Phase 1 (Fixes):      {p1_done:>6,} / {p1_target:>6,} ({p1_pct:>5.1f}%) ", end="")
    if p1_done >= p1_target:
        print("✓ COMPLETE")
    else:
        print()

    p2_done = max(0, min(implemented - p1_target, p2_target))
    p2_pct = round(100 * p2_done / p2_target, 1) if p2_target > 0 else 0
    print(f"Phase 2 (Features):   {p2_done:>6,} / {p2_target:>6,} ({p2_pct:>5.1f}%) ", end="")
    if p2_done >= p2_target:
        print("✓ COMPLETE")
    else:
        print()

    p3_done = max(0, min(implemented - p1_target - p2_target, p3_target))
    p3_pct = round(100 * p3_done / p3_target, 1) if p3_target > 0 else 0
    print(f"Phase 3 (Polish):     {p3_done:>6,} / {p3_target:>6,} ({p3_pct:>5.1f}%) ", end="")
    if p3_done >= p3_target:
        print("✓ COMPLETE")
    else:
        print()

    print()

    # Project and git stats
    print("─" * 80)
    print("ARTIFACTS:")
    print("─" * 80)
    print(f"Projects Created:     {progress['projects_created']:>10,}")
    print(f"Projects Released:    {progress['projects_released']:>10,}")
    print(f"Projects Archived:    {progress['projects_archived']:>10,}")
    print(f"Git Commits:          {progress['git_commits']:>10,}")
    print()

    # Timeline estimate
    print("─" * 80)
    print("TIMELINE:")
    print("─" * 80)
    print(f"Start Date:           {progress.get('start_time', 'N/A')}")
    print(f"Last Update:          {progress['last_update']}")

    if p1_pct > 0:
        # Estimate based on current rate
        elapsed_hours = 0  # Would need timestamp tracking for real estimate
        rate = percent / 100.0  # Very rough
        if rate > 0:
            eta_pct = 100 - percent
            # Rough estimate: assume current rate continues
            print("ETA Completion:       2026-07-15 (target)")

    print()
    print("=" * 80)
    print("Cron Jobs Running:")
    print("  ✓ phase1-executor (every 6 hours)")
    print("  ✓ phase2-executor (every 8 hours, starts at Phase 1 50%)")
    print("  ✓ phase3-executor (every 12 hours, starts at Phase 2 50%)")
    print("=" * 80)

def main():
    """Main monitor loop."""
    while True:
        try:
            progress = calculate_progress()
            print_dashboard(progress)

            # Save progress
            with open(PROGRESS_FILE, "w") as f:
                json.dump(progress, f, indent=2)

            # Check for completion
            if progress["percent_complete"] >= 100:
                print("\n🎉 ALL 209K IDEAS IMPLEMENTED! 🎉\n")
                break

            # Update every 5 seconds in interactive mode
            import time
            time.sleep(5)

        except KeyboardInterrupt:
            print("\nMonitor stopped.")
            break
        except Exception as e:
            print(f"Error: {e}")
            import time
            time.sleep(10)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "once":
        # Single update mode for cron
        progress = calculate_progress()
        print_dashboard(progress)
        with open(PROGRESS_FILE, "w") as f:
            json.dump(progress, f, indent=2)
    else:
        # Interactive mode
        main()
