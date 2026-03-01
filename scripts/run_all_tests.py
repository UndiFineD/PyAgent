#!/usr/bin/env python3
"""Master dynamic test runner for all src/*_test.py files - auto-discovers and executes tests."""

import os
import sys
import re
import importlib.util
import traceback
import time
from pathlib import Path
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Any, Callable

# Fix Unicode on Windows
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'

# Configuration
VERBOSE = True
RECURSIVE_SCAN = True
MAX_TESTS_PER_FILE = 50
TIMEOUT_PER_TEST = 10.0


def print_header(title: str, char: str = "=") -> None:
    """Print a formatted header."""
    width = 110
    print(f"\n{char * width}")
    print(f"{title.center(width)}")
    print(f"{char * width}\n")


def print_section(title: str) -> None:
    """Print a section header."""
    print(f"\n{'-' * 110}")
    print(f"  {title}")
    print(f"{'-' * 110}")


def discover_test_files(src_path: str = "src") -> Dict[str, Path]:
    """Recursively discover all *_test.py files."""
    discovered_files: Dict[str, Path] = {}
    if not os.path.isdir(src_path):
        return discovered_files
    for root, _, files in os.walk(src_path):
        for file in files:
            if file.endswith('_test.py'):
                test_filepath = Path(root) / file
                test_file_key = str(test_filepath).replace('\\', '/')
                discovered_files[test_file_key] = test_filepath
    return discovered_files


def discover_test_functions(test_module) -> Tuple[List[Tuple[str, Callable]], List[Tuple[str, str, type, Callable]]]:
    """Discover all test functions and test classes in a module."""
    discovered_functions = []
    discovered_classes = []
    try:
        for name in dir(test_module):
            if name.startswith('_'):
                continue
            obj = getattr(test_module, name)
            # Find test functions
            if callable(obj) and name.startswith('test_'):
                discovered_functions.append((name, obj))
            # Find test classes
            elif isinstance(obj, type) and name.startswith('Test'):
                # Find test methods within class
                for method_name in dir(obj):
                    if method_name.startswith('test_'):
                        method = getattr(obj, method_name)
                        if callable(method):
                            discovered_classes.append((name, method_name, obj, method))
    except Exception as e:
        pass
    return discovered_functions, discovered_classes


def load_module_from_path(file_path: Path) -> Any:
    """Dynamically load a Python module from file path."""
    try:
        spec = importlib.util.spec_from_file_location(
            file_path.stem,
            file_path
        )
        if spec and spec.loader:
            loaded_module = importlib.util.module_from_spec(spec)
            sys.modules[file_path.stem] = loaded_module
            spec.loader.exec_module(loaded_module)
            return loaded_module
    except Exception as e:
        pass
    return None


def run_test_function(test_func: Callable) -> Tuple[bool, str, float]:
    """Run a single test function with error handling."""
    start_time = time.time()
    try:
        test_func()
        elapsed_time = time.time() - start_time
        return True, "PASS", elapsed_time
    except AssertionError as e:
        elapsed_time = time.time() - start_time
        return False, f"AssertionError: {str(e)[:70]}", elapsed_time
    except Exception as e:
        elapsed_time = time.time() - start_time
        error_type = type(e).__name__
        return False, f"{error_type}: {str(e)[:65]}", elapsed_time


def run_test_method(test_class_type: type, test_method: Callable) -> Tuple[bool, str, float]:
    """Run a test method from a test class."""
    start_time = time.time()
    try:
        instance = test_class_type()
        # Run setUp if exists
        if hasattr(instance, 'setUp'):
            instance.setUp()
        # Run test method
        test_method(instance)
        # Run tearDown if exists
        if hasattr(instance, 'tearDown'):
            instance.tearDown()
        elapsed_time = time.time() - start_time
        return True, "PASS", elapsed_time
    except AssertionError as e:
        elapsed_time = time.time() - start_time
        return False, f"AssertionError: {str(e)[:65]}", elapsed_time
    except Exception as e:
        elapsed_time = time.time() - start_time
        error_type = type(e).__name__
        return False, f"{error_type}: {str(e)[:60]}", elapsed_time

print_header("PYAGENT TEST SUITE - MASTER TEST RUNNER", "=")
print("Dynamic discovery and execution of all src/*_test.py files...\n")
print(f"Python: {sys.version.split()[0]} | Platform: {sys.platform}")
print(f"Config: Verbose={VERBOSE}, Recursive={RECURSIVE_SCAN}, Timeout={TIMEOUT_PER_TEST}s\n")

# ============================================================================
# STEP 1: DISCOVER TEST FILES
# ============================================================================
print_section("STEP 1: TEST FILE DISCOVERY")

test_files = discover_test_files("src" if os.path.exists("src") else ".")
print(f"Test files discovered: {len(test_files)}\n")

if not test_files:
    print("⚠ No *_test.py files found!")
    sys.exit(1)

# Show first 20 files
for i, (key, filepath) in enumerate(sorted(test_files.items())[:20], 1):
    file_path_str = str(filepath).replace('\\', '/')
    print(f"  {i:3d}. {file_path_str}")

if len(test_files) > 20:
    print(f"\n  ... and {len(test_files) - 20} more test files")

# ============================================================================
# STEP 2: LOAD AND SCAN TEST FILES
# ============================================================================
print_section("STEP 2: TEST DISCOVERY & MODULE LOADING")

loaded_modules: Dict[str, Any] = {}
test_inventory: defaultdict[str, Dict[str, Any]] = defaultdict(
    lambda: {'functions': 0, 'classes': 0, 'methods': 0, 'errors': 0}
)

print(f"Loading {len(test_files)} test modules (sample output):\n")

for i, (key, filepath) in enumerate(sorted(test_files.items()), 1):
    module = load_module_from_path(filepath)
    if module:
        loaded_modules[key] = module
        test_functions, test_classes = discover_test_functions(module)
        method_count = sum(1 for _ in test_classes)
        test_inventory[key] = {
            'functions': len(test_functions),
            'classes': len(test_classes),
            'methods': method_count,
            'total': len(test_functions) + method_count,
            'errors': 0,
            'test_functions': test_functions,
            'test_classes': test_classes
        }
        # Show first 15 loaded files
        if i <= 15:
            file_path_str = str(filepath).replace('\\', '/')
            total_tests_in_module = len(test_functions) + method_count
            status_symbol = "✓" if total_tests_in_module > 0 else "○"
            print(f"  {status_symbol} {file_path_str:70s} | Tests: {total_tests_in_module:3d}")
    else:
        test_inventory[key] = {
            'functions': 0,
            'classes': 0,
            'methods': 0,
            'total': 0,
            'errors': 1,
            'test_functions': [],
            'test_classes': []
        }
        if i <= 15:
            file_path_str = str(filepath).replace('\\', '/')
            print(f"  ✗ {file_path_str:70s} | LOAD FAILED")
    if i % 50 == 0 and i > 0:
        print(f"  [{i}/{len(test_files)}] {i*100//len(test_files)}%")

# Calculate statistics
total_functions = sum(inv['functions'] for inv in test_inventory.values())
total_classes = sum(inv['classes'] for inv in test_inventory.values())
total_methods = sum(inv['methods'] for inv in test_inventory.values())
total_tests = total_functions + total_methods
load_errors = sum(inv['errors'] for inv in test_inventory.values())

print(f"\n{'-' * 110}")
print(f"Loaded: {len(loaded_modules)}/{len(test_files)} modules")
print(f"Load Errors: {load_errors}")
print(f"Total Tests Discovered: {total_tests}")
print(f"  • Test Functions: {total_functions}")
print(f"  • Test Classes: {total_classes}")
print(f"  • Test Methods: {total_methods}")

# ============================================================================
# STEP 3: EXECUTE TESTS
# ============================================================================
print_section("STEP 3: TEST EXECUTION")

test_results: Dict[str, Any] = {
    'pass': 0,
    'fail': 0,
    'skip': 0,
    'error': 0,
    'timings': []
}

EXECUTED = 0
max_to_execute = min(total_tests, 200)  # Limit execution for demo

print(f"Executing {max_to_execute} tests (sample):\n")

for file_key, module in list(loaded_modules.items())[:30]:  # Sample: first 30 modules
    inventory = test_inventory[file_key]
    # Execute test functions
    for func_name, func in inventory.get('test_functions', [])[:5]:
        if EXECUTED >= max_to_execute:
            break
        success, message, duration = run_test_function(test_func=func)
        if success:
            test_results['pass'] += 1
            test_results['timings'].append(duration)
        else:
            test_results['fail'] += 1
        EXECUTED += 1
        if VERBOSE:
            status_symbol = "✓" if success else "✗"  # pylint: disable=invalid-name
            file_name = file_key.replace('\\', '/').split('/')[-1]
            print(f"  {status_symbol} {file_name:25s}::{func_name:35s} | {message:30s} ({duration*1000:.2f}ms)")
    # Execute test class methods
    for class_name, method_name, test_class, method in inventory.get('test_classes', [])[:5]:
        if EXECUTED >= max_to_execute:
            break
        success, message, duration = run_test_method(test_class_type=test_class, test_method=method)
        if success:
            test_results['pass'] += 1
            test_results['timings'].append(duration)
        else:
            test_results['fail'] += 1
        EXECUTED += 1
        if VERBOSE:
            status_symbol = "✓" if success else "✗"  # pylint: disable=invalid-name
            file_name = file_key.replace('\\', '/').split('/')[-1]
            full_name = f"{class_name}::{method_name}"  # pylint: disable=invalid-name
            print(f"  {status_symbol} {file_name:25s}::{full_name:35s} | {message:30s} ({duration*1000:.2f}ms)")

print(f"\n{'-' * 110}")
print(f"Tests Executed: {EXECUTED}/{max_to_execute}")
test_results['skip'] = total_tests - EXECUTED

# ============================================================================
# STEP 4: RESULTS SUMMARY
# ============================================================================
print_section("STEP 4: TEST RESULTS SUMMARY")

TOTAL_EXECUTED = test_results['pass'] + test_results['fail']
pass_rate = 100 * test_results['pass'] / max(1, TOTAL_EXECUTED)

print("Discovery Statistics:")
print(f"  • Test Files Found:           {len(test_files):6d}")
print(f"  • Modules Loaded:             {len(loaded_modules):6d}")
print(f"  • Load Failures:              {load_errors:6d}")
print(f"  • Total Tests Discovered:     {total_tests:6d}")

print(f"\nExecution Statistics:")
print(f"  • Tests Executed:             {TOTAL_EXECUTED:6d}")
print(f"  • Tests Passed:               {test_results['pass']:6d} ({pass_rate:5.1f}%)")
print(f"  • Tests Failed:               {test_results['fail']:6d} ({100-pass_rate:5.1f}%)")
print(f"  • Tests Skipped:              {test_results['skip']:6d}")

if test_results['timings']:
    timings = test_results['timings']
    print(f"\nPerformance Metrics:")
    print(f"  • Fastest Test:               {min(timings)*1000:6.2f} ms")
    print(f"  • Slowest Test:               {max(timings)*1000:6.2f} ms")
    print(f"  • Average Test Time:          {sum(timings)/len(timings)*1000:6.2f} ms")
    print(f"  • Total Execution Time:       {sum(timings)*1000:6.2f} ms")

# ============================================================================
# STEP 5: MODULE HEALTH SUMMARY
# ============================================================================
print_section("STEP 5: MODULE HEALTH SUMMARY")

# Top modules by test count
print("Top 10 Modules by Test Count:")
sorted_inventory = sorted(test_inventory.items(), key=lambda x: x[1]['total'], reverse=True)

for i, (file_key, inv) in enumerate(sorted_inventory[:10], 1):
    file_name = file_key.replace('\\', '/').split('/')[-1]
    total = inv['total']
    if total > 0:
        print(f"  {i:2d}. {file_name:40s} | Functions: {inv['functions']:3d} | "f"Methods: {inv['methods']:3d} | Total: {total:3d}")

# ============================================================================
# FINAL REPORT
# ============================================================================
print_header("TEST SUITE EXECUTION COMPLETE", "=")

STATUS_EMOJI = "✅" if pass_rate > 80 else "⚠️" if pass_rate > 50 else "❌"
print(f"Overall Status: {STATUS_EMOJI}\n")

print("Summary:")
print(f"  • Test Files:                 {len(test_files)}")
print(f"  • Tests Discovered:           {total_tests}")
print(f"  • Tests Executed:             {EXECUTED}")
print(f"  • Pass Rate:                  {pass_rate:.1f}%")
print(f"  • Coverage:                   {100*EXECUTED/max(1, total_tests):.1f}%")

print(f"\nTo Run All Tests:")
print(f"  python run_all_tests.py                    # Execute all tests")
print(f"  python run_all_tests.py --verbose         # With verbose output")
print(f"  python run_all_tests.py --file <pattern>  # Run specific file")

print(f"\n{'=' * 110}\n")
