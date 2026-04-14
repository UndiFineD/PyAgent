#!/usr/bin/env python3
"""MEGA_EXECUTION_PLAN.json - Validation & Helper Script
Provides utilities to work with the massive 52K+ idea execution plan
"""

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

PLAN_FILE = Path(__file__).parent / "MEGA_EXECUTION_PLAN.json"

def load_plan() -> Dict:
    """Load the mega execution plan."""
    print("Loading MEGA_EXECUTION_PLAN.json...")
    with open(PLAN_FILE, 'r') as f:
        plan = json.load(f)
    print(f"✅ Loaded {plan['total_ideas']:,} ideas")
    return plan

def validate_plan(plan: Dict) -> Tuple[bool, List[str]]:
    """Validate plan integrity."""
    errors = []

    # Check top-level structure
    if 'timestamp' not in plan:
        errors.append("Missing 'timestamp' field")
    if 'stats' not in plan:
        errors.append("Missing 'stats' field")
    if 'total_ideas' not in plan:
        errors.append("Missing 'total_ideas' field")
    if 'batches' not in plan:
        errors.append("Missing 'batches' field")

    # Check batch structure
    total_items = 0
    for batch_name, items in plan.get('batches', {}).items():
        if not isinstance(items, list):
            errors.append(f"Batch '{batch_name}' is not a list")
            continue

        total_items += len(items)

        # Sample check first & last items
        for idx, item in enumerate([items[0], items[-1]] if len(items) > 1 else items):
            required_fields = {'id', 'title', 'archetype', 'priority', 'effort'}
            missing = required_fields - set(item.keys())
            if missing:
                sample_idx = 0 if idx == 0 else len(items)-1
                errors.append(
                    f"Batch '{batch_name}' item {sample_idx} missing fields: {missing}"
                )

    # Verify total count
    declared_total = plan.get('total_ideas', 0)
    if total_items != declared_total:
        errors.append(
            f"Item count mismatch: {total_items} items but declared {declared_total}"
        )

    return len(errors) == 0, errors

def print_statistics(plan: Dict) -> None:
    """Print comprehensive statistics."""
    print("\n" + "="*70)
    print("MEGA EXECUTION PLAN - STATISTICS")
    print("="*70)

    stats = plan['stats']
    print("\nLoad Statistics:")
    print(f"  Loaded from source:    {stats['loaded']:>8,} ideas")
    print(f"  Extracted ideas:       {stats['extracted']:>8,} ideas")
    print(f"  After deduplication:   {stats['deduped']:>8,} unique")
    print(f"  Total batched:         {stats['batched']:>8,} ideas")

    print("\nExecution Progress:")
    print(f"  Executed:              {stats['executed']:>8,} items")
    print(f"  Succeeded:             {stats['succeeded']:>8,} items")
    print(f"  Failed:                {stats['failed']:>8,} items")

    # Batch breakdown
    print(f"\nBatch Breakdown ({len(plan['batches'])} batches):")
    batches = plan['batches']
    batch_stats = []

    for name, items in sorted(batches.items(), key=lambda x: -len(x[1])):
        count = len(items)
        if count == 0:
            continue

        # Sample stats
        efforts = [item.get('effort', 0) for item in items]
        priorities = [item.get('priority', 0) for item in items]
        archetypes = Counter(item.get('archetype', 'unknown') for item in items)

        avg_effort = sum(efforts) / len(efforts) if efforts else 0
        avg_priority = sum(priorities) / len(priorities) if priorities else 0
        top_archetype = archetypes.most_common(1)[0][0] if archetypes else 'unknown'

        pct = 100 * count / plan['total_ideas']
        batch_stats.append((name, count, pct, avg_effort, avg_priority))

    for name, count, pct, avg_effort, avg_priority in batch_stats:
        print(f"  {name:<25} {count:>6,} items ({pct:>5.1f}%) | "
              f"Effort: {avg_effort:.1f} | Priority: {avg_priority:.2f}")

    # Archetype distribution
    print("\nArchetype Distribution:")
    all_archetypes = Counter()
    for items in plan['batches'].values():
        all_archetypes.update(item.get('archetype', 'unknown') for item in items)

    for archetype, count in all_archetypes.most_common():
        pct = 100 * count / plan['total_ideas']
        bar = '█' * int(pct / 2)
        print(f"  {archetype:<20} {count:>6,} ({pct:>5.1f}%) {bar}")

def estimate_timeline(plan: Dict, team_size: int = 5) -> None:
    """Estimate execution timeline."""
    print("\n" + "="*70)
    print("EXECUTION TIMELINE ESTIMATES")
    print("="*70)

    # Velocity by effort level
    effort_to_velocity = {
        1: 20,  # items/person/week
        2: 15,  # quick wins
        3: 12,  # medium effort
        4: 8,   # high effort
    }

    # Group by effort
    effort_counts = defaultdict(int)
    for items in plan['batches'].values():
        for item in items:
            effort_counts[item.get('effort', 3)] += 1

    print(f"\nWith Team of {team_size} Engineers:\n")

    total_person_weeks = 0
    for effort in sorted(effort_counts.keys()):
        count = effort_counts[effort]
        velocity = effort_to_velocity.get(effort, 10)
        person_weeks = count / velocity
        total_weeks = person_weeks / team_size
        total_person_weeks += person_weeks

        print(f"  Effort {effort}: {count:>6,} items @ {velocity}/person/week")
        print(f"            = {person_weeks:>6.0f} person-weeks = {total_weeks:>4.1f} calendar weeks")

    total_weeks = total_person_weeks / team_size
    months = total_weeks / 4.3

    print(f"\n  TOTAL: {total_person_weeks:>6.0f} person-weeks = {total_weeks:>5.1f} calendar weeks ({months:.1f} months)")
    print("\nNote: Assumes 5-day weeks, no context switching, dependencies managed")
    print("      Actual timeline may vary by 20-30% based on scope clarity & blockers")

def list_batches(plan: Dict) -> None:
    """List all batches with sizes."""
    print("\n" + "="*70)
    print("BATCH LISTING")
    print("="*70)
    print()

    for name, items in sorted(plan['batches'].items(), key=lambda x: -len(x[1])):
        print(f"• {name:<30} {len(items):>6,} items")

def export_batch(plan: Dict, batch_name: str, output_file: Path = None) -> None:
    """Export a single batch to a file."""
    if batch_name not in plan['batches']:
        print(f"❌ Batch '{batch_name}' not found")
        print(f"   Available: {', '.join(plan['batches'].keys())}")
        return

    items = plan['batches'][batch_name]
    output_file = output_file or Path(f"/tmp/{batch_name}_export.jsonl")

    with open(output_file, 'w') as f:
        for item in items:
            f.write(json.dumps(item) + '\n')

    print(f"✅ Exported {len(items)} items to {output_file}")

def filter_items(plan: Dict, min_priority: float = None,
                 max_effort: int = None,
                 archetypes: List[str] = None) -> List[Dict]:
    """Filter items by criteria."""
    results = []

    for items in plan['batches'].values():
        for item in items:
            if min_priority is not None and item.get('priority', 0) < min_priority:
                continue
            if max_effort is not None and item.get('effort', 0) > max_effort:
                continue
            if archetypes and item.get('archetype') not in archetypes:
                continue
            results.append(item)

    return results

def main():
    """Main CLI."""
    import sys

    plan = load_plan()
    is_valid, errors = validate_plan(plan)

    if is_valid:
        print("✅ Plan is valid and complete")
    else:
        print(f"❌ Plan has {len(errors)} errors:")
        for error in errors[:10]:  # Show first 10
            print(f"  - {error}")
        return

    # Print statistics
    print_statistics(plan)

    # Timeline estimate
    estimate_timeline(plan, team_size=5)

    # Available batches
    list_batches(plan)

    print("\n" + "="*70)
    print("QUICK REFERENCE")
    print("="*70)
    print("""
Usage:
  python3 MEGA_EXECUTION_PLAN.py          # Run this analysis
  
Examples:
  # Filter high-priority quick wins
  items = filter_items(plan, min_priority=8.0, max_effort=2)
  
  # Export a batch
  export_batch(plan, 'quick_wins', Path('quick_wins.jsonl'))
  
  # Check specific batch
  plan['batches']['quick_wins'][:5]  # First 5 items
""")

if __name__ == '__main__':
    main()
