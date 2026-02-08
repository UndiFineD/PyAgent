# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\skills.py\skills.py\idanmann10.py\startclaw_optimizer.py\scripts.py\context_pruner_b11438b81a01.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\skills\skills\idanmann10\startclaw-optimizer\scripts\context_pruner.py

#!/usr/bin/env python3

"""

Context Pruner - Aggressively reduce conversation context.

Keeps last N exchanges, summarizes older content.

"""

import json

import sys


def prune_context(messages, max_recent=10, max_tokens_estimate=15000):
    """

    Prune message history to reduce context bloat.



    Args:

        messages: List of conversation messages

        max_recent: Keep this many recent exchanges

        max_tokens_estimate: Target token count



    Returns:

        Pruned message list

    """

    if len(messages) <= max_recent:
        return messages

    # Keep system message

    system_msgs = [m for m in messages if m.get("role") == "system"]

    # Keep recent exchanges

    recent = messages[-max_recent:]

    # Summarize middle

    middle = messages[len(system_msgs) : -max_recent]

    if middle:
        summary = {
            "role": "user",
            "content": f"[Context summary: {len(middle)} earlier messages about building openclaw-optimizer skill, updating cron jobs, and publishing to ClawdHub]",
        }

        pruned = system_msgs + [summary] + recent

    else:
        pruned = system_msgs + recent

    return pruned


if __name__ == "__main__":
    # Read messages from stdin (JSON array)

    messages = json.load(sys.stdin)

    pruned = prune_context(messages)

    # Output pruned messages

    print(json.dumps(pruned, indent=2))

    # Stats to stderr

    print(f"Pruned: {len(messages)} → {len(pruned)} messages", file=sys.stderr)
