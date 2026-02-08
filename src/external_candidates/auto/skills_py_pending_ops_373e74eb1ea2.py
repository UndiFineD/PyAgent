# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\skills.py\skills.py\tonimelisma.py\email_to_calendar.py\scripts.py\utils.py\pending_ops_373e74eb1ea2.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\skills\skills\tonimelisma\email-to-calendar\scripts\utils\pending_ops.py

#!/usr/bin/env python3

"""

Pending invites operations for email-to-calendar skill.

Manages pending calendar invites that need user action.

"""

import json

import os

import sys

from datetime import datetime

from typing import Any, Dict, List

# Add parent directory to path for imports

sys.path.insert(0, os.path.dirname(__file__))

from common import get_day_of_week

from json_store import load_json, save_json

PENDING_FILE = os.path.expanduser(

    "~/.openclaw/workspace/memory/email-to-calendar/pending_invites.json"

)

MAX_REMINDERS = 3

def list_pending_summary(

    today: str, update_reminded: bool = False, auto_dismiss: bool = False

) -> None:

    """Print human-readable summary of pending invites."""

    data = load_json(PENDING_FILE, {"invites": []})

    pending_events = []

    auto_dismissed_count = 0

    modified = False

    for invite in data.get("invites", []):

        email_subject = invite.get("email_subject", "Unknown source")

        email_id = invite.get("email_id", "")

        reminder_count = invite.get("reminder_count", 0)

        # Check if this invite should be auto-dismissed

        if auto_dismiss and reminder_count >= MAX_REMINDERS:

            for event in invite.get("events", []):

                if event.get("status") == "pending":

                    event["status"] = "auto_dismissed"

                    event["auto_dismissed_at"] = datetime.now().isoformat()

                    auto_dismissed_count += 1

                    modified = True

            continue

        for event in invite.get("events", []):

            event_date = event.get("date", "")

            if event.get("status") == "pending" and event_date >= today:

                day_of_week = get_day_of_week(event_date)

                pending_events.append(

                    {

                        "title": event.get("title", "Untitled"),

                        "date": event_date,

                        "day": day_of_week,

                        "time": event.get("time", ""),

                        "source": email_subject,

                        "email_id": email_id,

                        "reminder_count": reminder_count,

                    }

                )

    # Update reminder tracking if requested

    if update_reminded and pending_events:

        now_iso = datetime.now().isoformat()

        seen_invites = set()

        for invite in data.get("invites", []):

            email_id = invite.get("email_id", "")

            if (

                email_id in [e["email_id"] for e in pending_events]

                and email_id not in seen_invites

            ):

                invite["last_reminded"] = now_iso

                invite["reminder_count"] = invite.get("reminder_count", 0) + 1

                seen_invites.add(email_id)

                modified = True

    # Save if modified

    if modified:

        save_json(PENDING_FILE, data)

    if auto_dismissed_count > 0:

        print(

            f"({auto_dismissed_count} event(s) auto-dismissed after {MAX_REMINDERS} ignored reminders)\n"

        )

    if not pending_events:

        print("No pending invites found.")

    else:

        print(f"You have {len(pending_events)} pending calendar invite(s):\n")

        for i, evt in enumerate(pending_events, 1):

            time_str = f" at {evt['time']}" if evt["time"] else ""

            day_str = f" ({evt['day']})" if evt["day"] else ""

            reminder_marker = (

                f" [reminded {evt['reminder_count']}x]"

                if evt["reminder_count"] > 0

                else ""

            )

            print(

                f"{i}. {evt['title']} - {evt['date']}{day_str}{time_str}{reminder_marker}"

            )

            print(f"   From: {evt['source']}")

        print(

            "\nReply with numbers to create (e.g., '1, 2'), 'all', or 'none' to dismiss."

        )

def list_pending_json(

    today: str, update_reminded: bool = False, auto_dismiss: bool = False

) -> None:

    """Print JSON array of pending invites."""

    data = load_json(PENDING_FILE, {"invites": []})

    pending_events = []

    modified = False

    for invite in data.get("invites", []):

        invite_id = invite.get("id", "")

        email_subject = invite.get("email_subject", "")

        email_id = invite.get("email_id", "")

        reminder_count = invite.get("reminder_count", 0)

        last_reminded = invite.get("last_reminded")

        # Check if this invite should be auto-dismissed

        if auto_dismiss and reminder_count >= MAX_REMINDERS:

            for event in invite.get("events", []):

                if event.get("status") == "pending":

                    event["status"] = "auto_dismissed"

                    event["auto_dismissed_at"] = datetime.now().isoformat()

                    modified = True

            continue

        for event in invite.get("events", []):

            event_date = event.get("date", "")

            if event.get("status") == "pending" and event_date >= today:

                pending_events.append(

                    {

                        "invite_id": invite_id,

                        "email_id": email_id,

                        "email_subject": email_subject,

                        "title": event.get("title", ""),

                        "date": event_date,

                        "day_of_week": get_day_of_week(event_date),

                        "time": event.get("time", ""),

                        "reminder_count": reminder_count,

                        "last_reminded": last_reminded,

                    }

                )

    # Update reminder tracking if requested

    if update_reminded and pending_events:

        now_iso = datetime.now().isoformat()

        seen_invites = set()

        for invite in data.get("invites", []):

            email_id = invite.get("email_id", "")

            if (

                email_id in [e["email_id"] for e in pending_events]

                and email_id not in seen_invites

            ):

                invite["last_reminded"] = now_iso

                invite["reminder_count"] = invite.get("reminder_count", 0) + 1

                seen_invites.add(email_id)

                modified = True

    # Save if modified

    if modified:

        save_json(PENDING_FILE, data)

    print(json.dumps(pending_events, indent=2))

def main():

    # Parse arguments

    today = datetime.now().strftime("%Y-%m-%d")

    summary_mode = False

    update_reminded = False

    auto_dismiss = False

    i = 1

    while i < len(sys.argv):

        arg = sys.argv[i]

        if arg == "--summary":

            summary_mode = True

        elif arg == "--update-reminded":

            update_reminded = True

        elif arg == "--auto-dismiss":

            auto_dismiss = True

        elif arg == "--today" and i + 1 < len(sys.argv):

            today = sys.argv[i + 1]

            i += 1

        i += 1

    if summary_mode:

        list_pending_summary(today, update_reminded, auto_dismiss)

    else:

        list_pending_json(today, update_reminded, auto_dismiss)

if __name__ == "__main__":

    main()

