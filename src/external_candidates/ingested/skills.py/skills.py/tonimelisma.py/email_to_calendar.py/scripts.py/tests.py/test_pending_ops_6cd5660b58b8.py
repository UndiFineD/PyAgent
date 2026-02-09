# Extracted from: C:\DEV\PyAgent\.external\skills\skills\tonimelisma\email-to-calendar\scripts\tests\test_pending_ops.py
#!/usr/bin/env python3
"""Tests for utils/pending_ops.py"""

import io
import json
import os
import shutil
import sys
import tempfile
import unittest
from datetime import datetime
from unittest.mock import patch

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils import pending_ops


class TestListPendingJson(unittest.TestCase):
    """Tests for list_pending_json function."""

    def setUp(self):
        """Create temp directory and patch file path."""
        self.temp_dir = tempfile.mkdtemp()
        self.pending_file = os.path.join(self.temp_dir, "pending_invites.json")
        self.patcher = patch.object(pending_ops, "PENDING_FILE", self.pending_file)
        self.patcher.start()

    def tearDown(self):
        """Clean up temp directory and stop patcher."""
        self.patcher.stop()
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_empty_when_no_invites(self):
        """Test that empty list returned when no invites exist."""
        with open(self.pending_file, "w") as f:
            json.dump({"invites": []}, f)

        captured = io.StringIO()
        with patch("sys.stdout", captured):
            pending_ops.list_pending_json(today="2026-02-11")

        output = captured.getvalue()
        results = json.loads(output)
        self.assertEqual(results, [])

    def test_filters_past_dates(self):
        """Test that past events are filtered out."""
        test_data = {
            "invites": [
                {
                    "id": "inv1",
                    "email_id": "email1",
                    "email_subject": "Test",
                    "events": [
                        {
                            "title": "Past Event",
                            "date": "2026-02-01",
                            "status": "pending",
                        },
                        {
                            "title": "Future Event",
                            "date": "2026-02-15",
                            "status": "pending",
                        },
                    ],
                }
            ]
        }
        with open(self.pending_file, "w") as f:
            json.dump(test_data, f)

        captured = io.StringIO()
        with patch("sys.stdout", captured):
            pending_ops.list_pending_json(today="2026-02-11")

        output = captured.getvalue()
        results = json.loads(output)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "Future Event")

    def test_filters_non_pending_status(self):
        """Test that non-pending events are filtered out."""
        test_data = {
            "invites": [
                {
                    "id": "inv1",
                    "email_id": "email1",
                    "email_subject": "Test",
                    "events": [
                        {
                            "title": "Created Event",
                            "date": "2026-02-15",
                            "status": "created",
                        },
                        {
                            "title": "Pending Event",
                            "date": "2026-02-16",
                            "status": "pending",
                        },
                    ],
                }
            ]
        }
        with open(self.pending_file, "w") as f:
            json.dump(test_data, f)

        captured = io.StringIO()
        with patch("sys.stdout", captured):
            pending_ops.list_pending_json(today="2026-02-11")

        output = captured.getvalue()
        results = json.loads(output)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "Pending Event")

    def test_includes_day_of_week(self):
        """Test that day_of_week is included in results."""
        test_data = {
            "invites": [
                {
                    "id": "inv1",
                    "email_id": "email1",
                    "email_subject": "Test",
                    "events": [
                        {
                            "title": "Wednesday Event",
                            "date": "2026-02-11",
                            "status": "pending",
                        }
                    ],
                }
            ]
        }
        with open(self.pending_file, "w") as f:
            json.dump(test_data, f)

        captured = io.StringIO()
        with patch("sys.stdout", captured):
            pending_ops.list_pending_json(today="2026-02-11")

        output = captured.getvalue()
        results = json.loads(output)
        self.assertEqual(results[0]["day_of_week"], "Wednesday")


class TestListPendingSummary(unittest.TestCase):
    """Tests for list_pending_summary function."""

    def setUp(self):
        """Create temp directory and patch file path."""
        self.temp_dir = tempfile.mkdtemp()
        self.pending_file = os.path.join(self.temp_dir, "pending_invites.json")
        self.patcher = patch.object(pending_ops, "PENDING_FILE", self.pending_file)
        self.patcher.start()

    def tearDown(self):
        """Clean up temp directory and stop patcher."""
        self.patcher.stop()
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_shows_no_pending_message(self):
        """Test that 'No pending invites' shown when empty."""
        with open(self.pending_file, "w") as f:
            json.dump({"invites": []}, f)

        captured = io.StringIO()
        with patch("sys.stdout", captured):
            pending_ops.list_pending_summary(today="2026-02-11")

        output = captured.getvalue()
        self.assertIn("No pending invites", output)

    def test_shows_event_count(self):
        """Test that event count is shown in summary."""
        test_data = {
            "invites": [
                {
                    "id": "inv1",
                    "email_id": "email1",
                    "email_subject": "Meeting Invite",
                    "events": [
                        {"title": "Event 1", "date": "2026-02-15", "status": "pending"},
                        {"title": "Event 2", "date": "2026-02-16", "status": "pending"},
                    ],
                }
            ]
        }
        with open(self.pending_file, "w") as f:
            json.dump(test_data, f)

        captured = io.StringIO()
        with patch("sys.stdout", captured):
            pending_ops.list_pending_summary(today="2026-02-11")

        output = captured.getvalue()
        self.assertIn("2 pending calendar invite", output)


class TestAutoDismiss(unittest.TestCase):
    """Tests for auto-dismiss functionality."""

    def setUp(self):
        """Create temp directory and patch file path."""
        self.temp_dir = tempfile.mkdtemp()
        self.pending_file = os.path.join(self.temp_dir, "pending_invites.json")
        self.patcher = patch.object(pending_ops, "PENDING_FILE", self.pending_file)
        self.patcher.start()

    def tearDown(self):
        """Clean up temp directory and stop patcher."""
        self.patcher.stop()
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_auto_dismiss_after_max_reminders(self):
        """Test that events are auto-dismissed after MAX_REMINDERS."""
        test_data = {
            "invites": [
                {
                    "id": "inv1",
                    "email_id": "email1",
                    "email_subject": "Test",
                    "reminder_count": 3,  # MAX_REMINDERS
                    "events": [
                        {
                            "title": "Ignored Event",
                            "date": "2026-02-15",
                            "status": "pending",
                        }
                    ],
                }
            ]
        }
        with open(self.pending_file, "w") as f:
            json.dump(test_data, f)

        captured = io.StringIO()
        with patch("sys.stdout", captured):
            pending_ops.list_pending_json(today="2026-02-11", auto_dismiss=True)

        # Check that the file was updated with auto_dismissed status
        with open(self.pending_file, "r") as f:
            data = json.load(f)

        event = data["invites"][0]["events"][0]
        self.assertEqual(event["status"], "auto_dismissed")
        self.assertIn("auto_dismissed_at", event)

    def test_no_auto_dismiss_below_max_reminders(self):
        """Test that events are not auto-dismissed below MAX_REMINDERS."""
        test_data = {
            "invites": [
                {
                    "id": "inv1",
                    "email_id": "email1",
                    "email_subject": "Test",
                    "reminder_count": 2,  # Below MAX_REMINDERS
                    "events": [
                        {
                            "title": "Still Pending",
                            "date": "2026-02-15",
                            "status": "pending",
                        }
                    ],
                }
            ]
        }
        with open(self.pending_file, "w") as f:
            json.dump(test_data, f)

        captured = io.StringIO()
        with patch("sys.stdout", captured):
            pending_ops.list_pending_json(today="2026-02-11", auto_dismiss=True)

        output = captured.getvalue()
        results = json.loads(output)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "Still Pending")


class TestUpdateReminded(unittest.TestCase):
    """Tests for update-reminded functionality."""

    def setUp(self):
        """Create temp directory and patch file path."""
        self.temp_dir = tempfile.mkdtemp()
        self.pending_file = os.path.join(self.temp_dir, "pending_invites.json")
        self.patcher = patch.object(pending_ops, "PENDING_FILE", self.pending_file)
        self.patcher.start()

    def tearDown(self):
        """Clean up temp directory and stop patcher."""
        self.patcher.stop()
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_increments_reminder_count(self):
        """Test that update_reminded increments reminder_count."""
        test_data = {
            "invites": [
                {
                    "id": "inv1",
                    "email_id": "email1",
                    "email_subject": "Test",
                    "reminder_count": 1,
                    "events": [
                        {"title": "Event", "date": "2026-02-15", "status": "pending"}
                    ],
                }
            ]
        }
        with open(self.pending_file, "w") as f:
            json.dump(test_data, f)

        captured = io.StringIO()
        with patch("sys.stdout", captured):
            pending_ops.list_pending_json(today="2026-02-11", update_reminded=True)

        with open(self.pending_file, "r") as f:
            data = json.load(f)

        self.assertEqual(data["invites"][0]["reminder_count"], 2)
        self.assertIn("last_reminded", data["invites"][0])


if __name__ == "__main__":
    unittest.main()
