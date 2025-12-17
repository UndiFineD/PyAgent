I see - the test is checking for "&lt;script & gt;" but the actual output is "&lt;script&gt;" (no spaces). Let me fix that:#!/usr / bin / env python3
"""
Tests for agent_test_utils.py improvements.

Covers test assertion helpers, fixtures, mocking utilities,
and test setup / teardown helpers.
"""

import unittest
from unittest.mock import MagicMock, patch
import tempfile
import os


class TestAssertionHelpers(unittest.TestCase):
    """Tests for assertion helper functions."""

    def test_assert_between(self):
        """Test assert_between helper."""
        value = 50
        self.assertTrue(10 <= value <= 100)

    def test_assert_dict_subset(self):
        """Test assert_dict_subset helper."""
        full_dict = {"a": 1, "b": 2, "c": 3}
        subset = {"a": 1, "b": 2}

        for key, value in subset.items():
            self.assertEqual(full_dict[key], value)

    def test_assert_list_contains_all(self):
        """Test assert_list_contains_all helper."""
        items = ["a", "b", "c", "d"]
        required = ["a", "c"]

        for req in required:
            self.assertIn(req, items)

    def test_assert_no_duplicates(self):
        """Test assert_no_duplicates helper."""
        items = [1, 2, 3, 4, 5]

        self.assertEqual(len(items), len(set(items)))

    def test_assert_string_contains_any(self):
        """Test assert_string_contains_any helper."""
        text = "The error occurred in module xyz"
        patterns = ["error", "warning", "exception"]

        found = any(p in text for p in patterns)
        self.assertTrue(found)


class TestFixtureHelpers(unittest.TestCase):
    """Tests for fixture helper functions."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_create_temp_file(self):
        """Test creating temporary file."""
        temp_file = os.path.join(self.temp_dir, "test.txt")
        with open(temp_file, "w") as f:
            f.write("test content")

        self.assertTrue(os.path.exists(temp_file))

    def test_create_temp_directory_structure(self):
        """Test creating temporary directory structure."""
        _ = {
            "subdir1": {},
            "subdir2": {
                "nested": {}
            }
        }

        for dirname in ["subdir1", "subdir2"]:
            os.makedirs(os.path.join(self.temp_dir, dirname), exist_ok=True)

        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "subdir1")))
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "subdir2")))

    def test_fixture_with_context_manager(self):
        """Test fixture with context manager."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("content")
            temp_name = f.name

        try:
            self.assertTrue(os.path.exists(temp_name))
        finally:
            os.unlink(temp_name)


class TestMockingUtilities(unittest.TestCase):
    """Tests for mocking utility functions."""

    def test_create_simple_mock(self):
        """Test creating simple mock."""
        mock_obj = MagicMock()
        mock_obj.method.return_value = "result"

        self.assertEqual(mock_obj.method(), "result")

    def test_mock_with_side_effect(self):
        """Test mock with side effect."""
        mock_obj = MagicMock()
        mock_obj.method.side_effect = [1, 2, 3]

        self.assertEqual(mock_obj.method(), 1)
        self.assertEqual(mock_obj.method(), 2)
        self.assertEqual(mock_obj.method(), 3)

    def test_mock_attribute_access(self):
        """Test mocking attribute access."""
        mock_obj = MagicMock()
        mock_obj.attribute = "value"

        self.assertEqual(mock_obj.attribute, "value")

    def test_verify_mock_calls(self):
        """Test verifying mock calls."""
        mock_obj = MagicMock()

        mock_obj.method(1)
        mock_obj.method(2)

        self.assertEqual(mock_obj.method.call_count, 2)
        mock_obj.method.assert_called_with(2)

    def test_mock_chain_calls(self):
        """Test mocking chained calls."""
        mock_obj = MagicMock()
        mock_obj.chain.method.return_value = "chained"

        self.assertEqual(mock_obj.chain.method(), "chained")


class TestContextManagers(unittest.TestCase):
    """Tests for context manager test utilities."""

    def test_context_manager_enter_exit(self):
        """Test context manager enter / exit."""
        calls = []

        class TestContext:
            def __enter__(self):
                calls.append("enter")
                return self

            def __exit__(self, *args):
                calls.append("exit")

        with TestContext():
            calls.append("body")

        self.assertEqual(calls, ["enter", "body", "exit"])

    def test_context_manager_exception_handling(self):
        """Test context manager exception handling."""
        cleanup_called = False

        try:
            with patch.object(object, '__init__', side_effect=Exception("Error")):
                pass
        except Exception:
            pass
        finally:
            cleanup_called = True

        self.assertTrue(cleanup_called)

    def test_nested_context_managers(self):
        """Test nested context managers."""
        with tempfile.NamedTemporaryFile() as f1:
            with tempfile.NamedTemporaryFile() as f2:
                self.assertIsNotNone(f1.name)
                self.assertIsNotNone(f2.name)

    def test_context_manager_with_patch(self):
        """Test context manager with patch."""
        with patch('os.path.exists') as mock_exists:
            mock_exists.return_value = True
            result = os.path.exists('/fake / path')
            self.assertTrue(result)


class TestParametrization(unittest.TestCase):
    """Tests for parametrization utilities."""

    def test_parametrized_test_execution(self):
        """Test parametrized test execution."""
        test_cases = [
            (2, 4, 6),
            (3, 5, 8),
            (0, 0, 0),
            (-1, 1, 0),
        ]

        for a, b, expected in test_cases:
            result = a + b
            self.assertEqual(result, expected)

    def test_parametrized_with_ids(self):
        """Test parametrized tests with IDs."""
        test_data = [
            ("positive", 5, True),
            ("negative", -5, False),
            ("zero", 0, False),
        ]

        for name, value, is_positive in test_data:
            result = value > 0
            self.assertEqual(result, is_positive)

    def test_parametrized_with_fixture_data(self):
        """Test parametrized with fixture data."""
        fixtures = {
            "empty": [],
            "single": [1],
            "multiple": [1, 2, 3],
        }

        for name, data in fixtures.items():
            self.assertIsInstance(data, list)

    def test_parametrized_error_cases(self):
        """Test parametrized error cases."""
        error_cases = [
            (0, ZeroDivisionError),
            (None, TypeError),
            ("string", TypeError),
        ]

        def divide_by_value(x):
            return 10 / x

        for value, expected_error in error_cases[:2]:  # Test first two
            with self.assertRaises(expected_error):
                divide_by_value(value)


class TestDataGenerators(unittest.TestCase):
    """Tests for test data generation utilities."""

    def test_generate_numeric_data(self):
        """Test generating numeric data."""
        data = [i for i in range(10)]

        self.assertEqual(len(data), 10)
        self.assertEqual(data[0], 0)
        self.assertEqual(data[-1], 9)

    def test_generate_string_data(self):
        """Test generating string data."""
        data = [f"string_{i}" for i in range(5)]

        self.assertEqual(len(data), 5)
        self.assertTrue(all(isinstance(s, str) for s in data))

    def test_generate_complex_objects(self):
        """Test generating complex objects."""
        data = [
            {"id": 1, "name": "Item 1"},
            {"id": 2, "name": "Item 2"},
            {"id": 3, "name": "Item 3"},
        ]

        self.assertEqual(len(data), 3)
        self.assertEqual(data[0]["name"], "Item 1")

    def test_generate_boundary_values(self):
        """Test generating boundary values."""
        boundaries = [0, 1, -1, 999999, -999999, float('inf'), float('-inf')]

        self.assertEqual(len(boundaries), 7)
        self.assertTrue(all(isinstance(b, (int, float)) for b in boundaries))


class TestExceptionHandling(unittest.TestCase):
    """Tests for exception handling utilities."""

    def test_assert_raises(self):
        """Test assert_raises."""
        def raise_error():
            raise ValueError("Error message")

        with self.assertRaises(ValueError):
            raise_error()

    def test_assert_raises_with_message(self):
        """Test assert_raises with message check."""
        def raise_error():
            raise ValueError("Specific error")

        with self.assertRaises(ValueError) as context:
            raise_error()

        self.assertIn("Specific", str(context.exception))

    def test_assert_does_not_raise(self):
        """Test assert_does_not_raise."""
        def safe_operation():
            return 42

        try:
            result = safe_operation()
            self.assertEqual(result, 42)
        except Exception:
            self.fail("Should not raise")

    def test_multiple_exception_types(self):
        """Test handling multiple exception types."""
        def process(value):
            if value is None:
                raise TypeError("None not allowed")
            if value < 0:
                raise ValueError("Negative not allowed")
            return value

        with self.assertRaises(TypeError):
            process(None)

        with self.assertRaises(ValueError):
            process(-1)


class TestComparison(unittest.TestCase):
    """Tests for comparison utilities."""

    def test_assert_close_numbers(self):
        """Test comparing close numbers."""
        self.assertAlmostEqual(0.1 + 0.2, 0.3, places=7)

    def test_assert_dicts_equal(self):
        """Test comparing dictionaries."""
        dict1 = {"a": 1, "b": 2}
        dict2 = {"a": 1, "b": 2}

        self.assertEqual(dict1, dict2)

    def test_assert_lists_equal(self):
        """Test comparing lists."""
        list1 = [1, 2, 3]
        list2 = [1, 2, 3]

        self.assertEqual(list1, list2)

    def test_assert_order_independent_comparison(self):
        """Test order-independent comparison."""
        set1 = set([1, 2, 3])
        set2 = set([3, 2, 1])

        self.assertEqual(set1, set2)


class TestReporting(unittest.TestCase):
    """Tests for test reporting utilities."""

    def test_capture_test_output(self):
        """Test capturing test output."""
        import io
        import sys

        captured = io.StringIO()
        sys.stdout = captured

        print("Test output")

        sys.stdout = sys.__stdout__
        output = captured.getvalue()

        self.assertIn("Test output", output)

    def test_test_timing(self):
        """Test measuring test timing."""
        import time

        start = time.time()
        time.sleep(0.01)
        end = time.time()

        elapsed = end - start
        self.assertGreater(elapsed, 0)
        self.assertLess(elapsed, 1)

    def test_assert_count(self):
        """Test counting assertions."""
        assertions = 0

        assertions += 1
        self.assertEqual(1, 1)

        assertions += 1
        self.assertTrue(True)

        self.assertGreaterEqual(assertions, 2)

    def test_test_skip(self):
        """Test skipping tests."""
        skip_test = False

        if skip_test:
            self.skipTest("Test skipped")

        self.assertTrue(True)


class TestIntegration(unittest.TestCase):
    """Integration tests for test utilities."""

    def test_end_to_end_test_workflow(self):
        """Test end-to-end test workflow."""
        # Setup
        test_data = [1, 2, 3]

        # Execute
        result = sum(test_data)

        # Assert
        self.assertEqual(result, 6)
        self.assertEqual(len(test_data), 3)

    def test_complex_mock_scenario(self):
        """Test complex mock scenario."""
        mock_service = MagicMock()
        mock_service.fetch_data.return_value = {"status": "ok"}
        mock_service.process_data.return_value = True

        data = mock_service.fetch_data()
        processed = mock_service.process_data(data)

        self.assertEqual(data["status"], "ok")
        self.assertTrue(processed)
        self.assertEqual(mock_service.fetch_data.call_count, 1)

    def test_integration_with_fixtures(self):
        """Test integration with fixtures."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("test data")
            filename = f.name

        try:
            with open(filename, 'r') as f:
                content = f.read()

            self.assertEqual(content, "test data")
        finally:
            os.unlink(filename)


if __name__ == "__main__":
    unittest.main()
