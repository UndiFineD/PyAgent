# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\skills.py\skills.py\robbyczgw_cla.py\agent_protocol.py\examples.py\handler_example_7a9d86fc8781.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\skills\skills\robbyczgw-cla\agent-protocol\examples\handler-example.py

#!/usr/bin/env python3

"""

Example event handler.

Reads event JSON from stdin and processes it.

"""

import json

import sys


def main():
    # Read event from stdin

    event_json = sys.stdin.read()

    event = json.loads(event_json)

    # Process event

    print(f"Received event: {event['event_type']}")

    print(f"From: {event['source_agent']}")

    print(f"Payload: {json.dumps(event['payload'], indent=2)}")

    # Your processing logic here

    # ...

    # Output result (optional)

    result = {"status": "success", "processed_at": event["timestamp"]}

    print(json.dumps(result))


if __name__ == "__main__":
    main()
