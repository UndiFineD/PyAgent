#!/usr/bin/env python3
"""Dynamic comprehensive test suite for all rust_core exports - auto-generated from Rust source."""

import rust_core
import time
import sys
import os
import re
import json
import traceback
from collections import defaultdict, Counter
from typing import Any, Tuple, List, Dict, Optional
from pathlib import Path

# Configuration
VERBOSE = True
SHOW_ALL_FUNCTIONS = False  # Set to True to see all functions
SCAN_SOURCE = True  # Scan rust_core/src/ for function signatures
TEST_ALL_FUNCTIONS = True  # Attempt to test all discovered functions
MAX_FUNCTIONS_TO_TEST = 100  # Limit tests for performance

def print_header(title: str, char: str = "=") -> None:
    """Print a formatted header."""
    width = 100
    print(f"\n{char * width}")
    print(f"{title.center(width)}")
    print(f"{char * width}\n")

def print_section(title: str) -> None:
    """Print a section header."""
    print(f"\n{'─' * 100}")
    print(f"  {title}")
    print(f"{'─' * 100}")

def _extract_functions_from_file(filepath: str, file: str, fn_pattern: Any) -> List[Dict[str, Any]]:
    """Extract function definitions from a single Rust file."""
    functions = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        matches = fn_pattern.findall(content)
        for func_name, params in matches:
            if not any(skip in func_name for skip in ['test_', 'main', '__']):
                arg_count = len([p for p in params.split(',') if p.strip() and not p.strip().startswith('&')])
                functions.append({
                    'name': func_name,
                    'params': params,
                    'arg_count': arg_count
                })
    except Exception:
        pass
    return functions

def scan_rust_files(src_path: str) -> Dict[str, List[Dict[str, Any]]]:
    """Recursively scan rust_core/src for all .rs files and extract function definitions."""
    functions_by_file: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    
    if not os.path.isdir(src_path):
        return functions_by_file
    
    # Pattern to match pub fn declarations (including async, generic params)
    fn_pattern = re.compile(r'pub\s+(?:async\s+)?fn\s+(\w+)\s*(?:<[^>]*>)?\s*\(([^)]*)\)')
    
    for root, dirs, files in os.walk(src_path):
        for file in files:
            if file.endswith('.rs'):
                filepath = os.path.join(root, file)
                functions = _extract_functions_from_file(filepath, file, fn_pattern)
                functions_by_file[file].extend(functions)
    
    return functions_by_file

def generate_test_args(func_name: str, arg_count: int = 1) -> List[Tuple[Any, ...]]:
    """Generate intelligent test arguments for functions based on name patterns."""
    test_cases: List[Tuple[Any, ...]] = []
    
    func_lower = func_name.lower()
    
    # Grammar-based argument generation
    if any(x in func_lower for x in ['json', 'validate', 'check']):
        test_cases.append(('{"test": true, "value": 42}',))
    
    if any(x in func_lower for x in ['metric', 'aggregate', 'stats']):
        test_cases.append(([1, 2, 3, 4, 5],))
    
    if any(x in func_lower for x in ['complexity', 'code', 'analyze']):
        test_cases.append(('def hello():\n    return 42',))
    
    if any(x in func_lower for x in ['import', 'parse']):
        test_cases.append(('import os\nimport sys',))
    
    if any(x in func_lower for x in ['top_k', 'rank', 'sort']):
        test_cases.append(([5.0, 4.0, 3.0, 2.0, 1.0], 2))
    
    if any(x in func_lower for x in ['mask', 'token']):
        test_cases.append(([1, 0, 1, 0, 1],))
    
    if any(x in func_lower for x in ['tensor', 'matrix', 'vector']):
        test_cases.append(([1.0, 2.0, 3.0],))
    
    if any(x in func_lower for x in ['hash', 'encode']):
        test_cases.append(('test_string_value',))
    
    if any(x in func_lower for x in ['weight', 'param', 'config']):
        test_cases.append(({'key': 'value'},))
    
    if any(x in func_lower for x in ['compute', 'calculate', 'sum']):
        test_cases.append(([1, 2, 3],))
    
    # Generic fallbacks
    if not test_cases:
        if arg_count == 0:
            test_cases.append(())
        elif arg_count == 1:
            test_cases.append(('test',))
        elif arg_count == 2:
            test_cases.append(('test', 1))
        elif arg_count == 3:
            test_cases.append(('test', 1, 2))
        else:
            test_cases.append(tuple(['arg' + str(i) for i in range(arg_count)]))
    
    return test_cases

def safe_call_function(func: Any, args: Tuple, func_name: str) -> Tuple[bool, str, Any]:
    """Safely call a function with error handling and timing."""
    try:
        start_time = time.time()
        result = func(*args)
        duration = time.time() - start_time
        return True, f"✓ Returned: {type(result).__name__} (took {duration*1000:.2f}ms)", result
    except TypeError as e:
        error_msg = str(e)
        if 'missing' in error_msg or 'required' in error_msg:
            return False, f"⚠ MissingArgs: {error_msg[:60]}", None
        return False, f"✗ TypeError: {error_msg[:70]}", None
    except ValueError as e:
        return False, f"✗ ValueError: {str(e)[:70]}", None
    except RuntimeError as e:
        return False, f"✗ RuntimeError: {str(e)[:70]}", None
    except Exception as e:
        exc_type = type(e).__name__
        return False, f"✗ {exc_type}: {str(e)[:65]}", None

print_header("RUST_CORE v0.1.0 - DYNAMIC AUTO-GENERATED TEST SUITE", "=")
print("Dynamic discovery and testing of all rust_core exports...\n")
print(f"Python: {sys.version.split()[0]} | Platform: {sys.platform}")
print(f"Test Config: Verbose={VERBOSE}, ScanSource={SCAN_SOURCE}, TestAll={TEST_ALL_FUNCTIONS}")

# ============================================================================
# STEP 0: SCAN RUST SOURCE FILES
# ============================================================================
if SCAN_SOURCE:
    print_section("STEP 0: SOURCE CODE SCANNING")
    src_path = os.path.join(os.path.dirname(__file__), 'src')
    rust_functions = scan_rust_files(src_path)
    
    total_rust_funcs = sum(len(funcs) for funcs in rust_functions.values())
    print(f"Rust source files scanned: {len(rust_functions)}")
    print(f"Public functions found in source: {total_rust_funcs}\n")
    
    if SHOW_ALL_FUNCTIONS and rust_functions:
        for file, funcs in sorted(rust_functions.items())[:5]:
            print(f"{file:30s}: {len(funcs):3d} functions")
            for func in funcs[:5]:
                print(f"  • {func['name']:30s} (args: {func['arg_count']})")

# ============================================================================
# STEP 1: ENUMERATE ALL EXPORTS
# ============================================================================
print_section("STEP 1: MODULE ENUMERATION")

all_exports = dir(rust_core)
public_exports = [x for x in all_exports if not x.startswith("_")]
private_exports = [x for x in all_exports if x.startswith("_")]

print(f"Total exports found: {len(all_exports)}")
print(f"  • Public exports:  {len(public_exports)}")
print(f"  • Private exports: {len(private_exports)}")

# Categorize exports
class_exports = []
function_exports = []
special_exports = []

for item in public_exports:
    try:
        obj = getattr(rust_core, item)
        if item[0].isupper():
            class_exports.append(item)
        elif callable(obj):
            function_exports.append(item)
        else:
            special_exports.append(item)
    except:
        pass

print(f"\nExport Categories:")
print(f"  • Classes/Types: {len(class_exports):4d} ({100*len(class_exports)/(len(public_exports)):.1f}%)")
print(f"  • Functions:     {len(function_exports):4d} ({100*len(function_exports)/(len(public_exports)):.1f}%)")
print(f"  • Other:         {len(special_exports):4d} ({100*len(special_exports)/(len(public_exports)):.1f}%)")

# ============================================================================
# STEP 2: DETAILED CLASS INVENTORY
# ============================================================================
print_section("STEP 2: CLASS/TYPE INVENTORY")

print(f"Total Classes Found: {len(class_exports)}\n")
for i, cls in enumerate(sorted(class_exports), 1):
    try:
        obj = getattr(rust_core, cls)
        doc = ""
        if hasattr(obj, '__doc__') and obj.__doc__:
            doc = obj.__doc__.strip().split('\n')[0][:60]
        print(f"  {i:2d}. {cls:30s} {f'- {doc}' if doc else ''}")
    except:
        pass

# ============================================================================
# STEP 3: FUNCTION CATEGORIZATION
# ============================================================================
print_section("STEP 3: FUNCTION CATEGORIZATION")

# Group functions by prefix
prefixes: Dict[str, List[str]] = defaultdict(list)
for func_name in function_exports:
    try:
        if '_' in func_name:
            prefix = func_name.split('_')[0]
        else:
            prefix = 'uncategorized'
        prefixes[prefix].append(func_name)
    except Exception:
        prefixes['uncategorized'].append(func_name)

print(f"Function categories identified: {len(prefixes)}")
print(f"Functions per category:\n")

sorted_prefixes = sorted(prefixes.items(), key=lambda x: len(x[1]), reverse=True)

if sorted_prefixes:
    for prefix_name, funcs in sorted_prefixes[:15]:
        print(f"  {prefix_name.upper():15s}: {len(funcs):4d} functions")
    
    if len(sorted_prefixes) > 15:
        remaining = sum(len(funcs) for _, funcs in sorted_prefixes[15:])
        print(f"  {'OTHER':15s}: {remaining:4d} functions ({len(sorted_prefixes)-15} categories)")
else:
    print("  No function categories found")

# ============================================================================
# STEP 4: DYNAMIC FUNCTION TESTING
# ============================================================================
print_section("STEP 4: DYNAMIC FUNCTION TESTING")

test_results: Dict[str, Any] = {
    'pass': 0,
    'fail': 0,
    'skip': 0,
    'errors': [],
    'timings': []
}

# Select functions to test
test_functions = sorted(function_exports)
if TEST_ALL_FUNCTIONS and len(test_functions) > MAX_FUNCTIONS_TO_TEST:
    test_functions = test_functions[:MAX_FUNCTIONS_TO_TEST]

print(f"Testing {len(test_functions)} functions from {len(function_exports)} total:\n")

for i, func_name in enumerate(test_functions, 1):
    if hasattr(rust_core, func_name):
        func = getattr(rust_core, func_name)
        
        # Generate test arguments
        test_args_list = generate_test_args(func_name, 1)
        
        success = False
        message = ""
        for test_args in test_args_list:
            success, message, result = safe_call_function(func, test_args, func_name)
            
            if success:
                test_results['pass'] += 1
                test_results['timings'].append((func_name, message.split('took ')[1].split('ms')[0] if 'took' in message else '0'))
                break
        
        if not success:
            test_results['fail'] += 1
            if not any(func_name in prev_error for prev_error, _ in test_results['errors']):
                test_results['errors'].append((func_name, message))
            # Try with no args as fallback
            success, message, result = safe_call_function(func, (), func_name)
            if success:
                test_results['pass'] += 1
                test_results['fail'] -= 1
        
        # Print progress every 10 functions
        if i % 10 == 0 or i == len(test_functions):
            pct = 100 * (test_results['pass'] + test_results['fail']) / (test_results['pass'] + test_results['fail'] + 0.001)
            pass_rate = 100 * test_results['pass'] / max(1, test_results['pass'] + test_results['fail'])
            print(f"  Progress: {i}/{len(test_functions)} ({pct:.0f}%) | Pass Rate: {pass_rate:.1f}%")
    else:
        test_results['skip'] += 1

print(f"\n" + "─" * 100)

# ============================================================================
# STEP 5: CLASS INSTANTIATION TESTS  
# ============================================================================
print_section("STEP 5: CLASS INSTANTIATION TESTS")

key_classes = ["CoderCore", "CodeQualityCore", "WebCore", "ToolDraftingCore", 
               "FlexibleNeuralNetwork", "NeuralTransformer", "KVCache"]

class_results = {'found': 0, 'missing': 0}

for cls_name in key_classes:
    if hasattr(rust_core, cls_name):
        class_results['found'] += 1
        cls_obj = getattr(rust_core, cls_name)
        print(f"  ✓ {cls_name:30s} | Type: {type(cls_obj).__name__:15s} Callable: {callable(cls_obj)}")
    else:
        class_results['missing'] += 1
        print(f"  ✗ {cls_name:30s} | NOT FOUND")

# ============================================================================
# STEP 6: DETAILED STATISTICS
# ============================================================================
print_section("STEP 6: DETAILED STATISTICS")

total_tested = test_results['pass'] + test_results['fail']
pass_rate = 100 * test_results['pass'] / max(1, total_tested)

print("Export Statistics:")
print(f"  • Total Exports:       {len(public_exports):6d}")
print(f"  • Classes/Types:       {len(class_exports):6d}")
print(f"  • Functions:           {len(function_exports):6d}")

print(f"\nFunction Test Statistics:")
print(f"  • Tested:              {total_tested:6d}")
print(f"  • Passed:              {test_results['pass']:6d} ({pass_rate:5.1f}%)")
print(f"  • Failed:              {test_results['fail']:6d} ({100-pass_rate:5.1f}%)")
print(f"  • Skipped:             {test_results['skip']:6d}")

print(f"\nClass Statistics:")
print(f"  • Key Classes Found:   {class_results['found']:6d}/{len(key_classes)}")
print(f"  • Missing Classes:     {class_results['missing']:6d}/{len(key_classes)}")

if test_results['timings']:
    timings = [float(t[1]) for t in test_results['timings'] if t[1].replace('.', '').isdigit()]
    if timings:
        print(f"\nPerformance Metrics:")
        print(f"  • Fastest Function:    {min(timings):7.3f} ms")
        print(f"  • Slowest Function:    {max(timings):7.3f} ms")
        print(f"  • Average Time:        {sum(timings)/len(timings):7.3f} ms")

if test_results['errors']:
    print(f"\nFailed Function Details (first 10):")
    for func_name, error_msg in test_results['errors'][:10]:
        print(f"  • {func_name:30s} | {error_msg}")

# ============================================================================
# STEP 7: MODULE HEALTH CHECK
# ============================================================================
print_section("STEP 7: MODULE HEALTH CHECK")

health_checks = [
    ("Core imports loadable", len(public_exports) > 0),
    ("Critical classes present", len(class_exports) >= 5),
    ("Large function suite", len(function_exports) > 300),
    ("High test pass rate", pass_rate > 40.0),
    ("Key classes present", class_results['missing'] == 0),
]

passed_checks = sum(1 for _, result in health_checks if result)

print(f"Health Status: {passed_checks}/{len(health_checks)} checks passed\n")
for check_name, result in health_checks:
    status = "✓" if result else "✗"
    print(f"  {status} {check_name}")

# ============================================================================
# FINAL SUMMARY
# ============================================================================
print_header("TEST SUITE SUMMARY", "=")

status_emoji = "✅" if passed_checks == len(health_checks) else "⚠️" if passed_checks >= 4 else "❌"
print(f"Module Status: {status_emoji}\n")

print(f"Export Inventory:")
print(f"  • Total Exports:              {len(public_exports):6d}")
print(f"  • Classes:                    {len(class_exports):6d}")
print(f"  • Functions:                  {len(function_exports):6d}")
print(f"  • Function Categories:        {len(prefixes):6d}")

print(f"\nTest Results:")
print(f"  • Functions Tested:           {total_tested:6d}")
print(f"  • Success Rate:               {pass_rate:6.1f}%")
print(f"  • Health Score:               {100*passed_checks/len(health_checks):6.1f}%")

print(f"\n{'=' * 100}")
if TEST_ALL_FUNCTIONS:
    print(f"✅ rust_core v0.1.0 - Dynamic testing complete ({len(test_functions)} functions tested)".center(100))
else:
    print(f"✅ rust_core v0.1.0 - Diagnostic testing complete ({len(function_exports)} functions discovered)".center(100))
print(f"{'=' * 100}\n")
