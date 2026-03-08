#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Documentation and Test Generator for PyAgent
Automatically generates .description.md, .improvements.md, .splice.md, and *_test.py files

Features:
- Resumption support (saves progress checkpoint)
- Enhanced error handling and reporting
- Detailed statistics with breakdowns
- Optional AI enhancement via OpenAI API
- Progress tracking and ETA
"""

import os
import ast
import json
import time
import argparse
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Any
from collections import defaultdict
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from concurrent.futures import ThreadPoolExecutor, as_completed

# Optional dependencies
AI_ENHANCED = False
ai_client = None
try:
    from openai import OpenAI
    from dotenv import load_dotenv
    load_dotenv()
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    if OPENAI_API_KEY:
        AI_ENHANCED = True
        ai_client = OpenAI(api_key=OPENAI_API_KEY)
except ImportError:
    pass

# Optional progress bar
HAS_TQDM = False
try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    # Fallback: define a no-op tqdm that returns the iterable as-is
    def tqdm(iterable, *args, **kwargs):
        return iterable

# Configuration (can be overridden by CLI args)
DRY_RUN = True
VERBOSE = True
SRC_PATH = "src"
CHECKPOINT_FILE = "data/logs/doc_gen_checkpoint.json"
ERROR_LOG = "data/logs/doc_gen_errors.json"

def safe_relative_path(file_path: Path) -> Path:
    """Safely convert a path to relative path, handling both absolute and relative paths."""
    try:
        return file_path.relative_to(Path.cwd())
    except ValueError:
        # Path is already relative or not under cwd
        return file_path

@dataclass
class ProcessingStats:
    """Track detailed processing statistics."""
    total_files: int = 0
    files_processed: int = 0
    files_skipped: int = 0
    description_created: int = 0
    improvements_created: int = 0
    splice_created: int = 0
    test_created: int = 0
    renamed: int = 0
    errors: int = 0
    start_time: float = 0.0
    
    # Detailed breakdowns
    files_by_size: Dict[str, int] = None  # type: ignore
    files_by_complexity: Dict[str, int] = None  # type: ignore
    error_types: Dict[str, int] = None  # type: ignore
    largest_files: List[Tuple[str, int]] = None  # type: ignore
    
    def __post_init__(self):
        if self.files_by_size is None:
            self.files_by_size = defaultdict(int)
        if self.files_by_complexity is None:
            self.files_by_complexity = defaultdict(int)
        if self.error_types is None:
            self.error_types = defaultdict(int)
        if self.largest_files is None:
            self.largest_files = []
    
    def elapsed_time(self) -> str:
        """Get elapsed time as formatted string."""
        if self.start_time == 0.0:
            return "0s"
        elapsed = time.time() - self.start_time
        return str(timedelta(seconds=int(elapsed)))
    
    def eta(self) -> str:
        """Calculate estimated time to completion."""
        if self.files_processed == 0 or self.start_time == 0.0:
            return "calculating..."
        elapsed = time.time() - self.start_time
        rate = self.files_processed / elapsed
        remaining = self.total_files - self.files_processed
        eta_seconds = remaining / rate if rate > 0 else 0
        return str(timedelta(seconds=int(eta_seconds)))
    
    def files_per_second(self) -> float:
        """Calculate processing rate."""
        if self.files_processed == 0 or self.start_time == 0.0:
            return 0.0
        elapsed = time.time() - self.start_time
        return self.files_processed / elapsed if elapsed > 0 else 0.0

@dataclass
class ErrorRecord:
    """Record an error with context."""
    filepath: str
    error_type: str
    error_message: str
    timestamp: str
    traceback: Optional[str] = None

class PythonFileAnalyzer:
    """Analyzes Python files to extract classes, functions, imports, etc."""
    
    def __init__(self, filepath: Path):
        self.filepath: Path = filepath
        self.content: Optional[str] = self.read_file()
        self.tree: Optional[ast.AST] = None
        self.classes: List[Dict[str, Any]] = []
        self.functions: List[Dict[str, Any]] = []
        self.imports: List[str] = []
        self.docstring: Optional[str] = None
        self.complexity_score: int = 0
        self.line_count: int = len(self.content.splitlines()) if self.content else 0
        self.parse()
    
    def read_file(self) -> Optional[str]:
        """Read file content safely."""
        try:
            with open(self.filepath, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except Exception as e:
            print(f"  [!] Cannot read {self.filepath}: {e}")
            return None
    
    def parse(self):
        """Parse the Python file using AST."""
        if not self.content:
            return
        try:
            self.tree = ast.parse(self.content, filename=str(self.filepath))
            if isinstance(self.tree, ast.Module):
                self._add_parent_refs(self.tree)
                self.extract_info()
        except SyntaxError as e:
            print(f"  [!] Syntax error in {self.filepath}: {e}")
        except Exception as e:
            print(f"  [!] Parse error in {self.filepath}: {e}")
    
    def _add_parent_refs(self, node, parent=None):
        """Add parent references to AST nodes for tracking."""
        node.parent = parent
        for child in ast.iter_child_nodes(node):
            self._add_parent_refs(child, node)
    
    def extract_info(self):
        """Extract classes, functions, imports from AST."""
        if not self.tree or not isinstance(self.tree, ast.Module):
            return
        
        # Get module docstring
        self.docstring = ast.get_docstring(self.tree)
        
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef):
                class_info = {
                    'name': node.name,
                    'docstring': ast.get_docstring(node),
                    'methods': [],
                    'bases': [self.get_base_name(base) for base in node.bases],
                    'lineno': node.lineno
                }
                # Extract methods
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        class_info['methods'].append({
                            'name': item.name,
                            'docstring': ast.get_docstring(item),
                            'args': [arg.arg for arg in item.args.args]
                        })
                self.classes.append(class_info)
                self.complexity_score += len(class_info['methods'])
            
            elif isinstance(node, ast.FunctionDef):
                # Only top-level functions
                if isinstance(getattr(node, 'parent', None), ast.Module):
                    self.functions.append({
                        'name': node.name,
                        'docstring': ast.get_docstring(node),
                        'args': [arg.arg for arg in node.args.args]
                    })
                    self.complexity_score += 1
            
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    self.imports.append(alias.name)
            
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ''
                for alias in node.names:
                    self.imports.append(f"{module}.{alias.name}")
    
    def get_base_name(self, base) -> str:
        """Extract base class name from AST node."""
        if isinstance(base, ast.Name):
            return base.id
        elif isinstance(base, ast.Attribute):
            return base.attr
        return "Unknown"
    
    def has_multiple_classes(self) -> bool:
        """Check if file has multiple classes."""
        return len(self.classes) > 1
    
    def get_summary(self) -> str:
        """Get a summary of the file."""
        return f"{len(self.classes)} classes, {len(self.functions)} functions, {len(self.imports)} imports"
    
    def get_complexity_category(self) -> str:
        """Categorize file by complexity."""
        if self.complexity_score < 5:
            return "simple"
        elif self.complexity_score < 20:
            return "moderate"
        elif self.complexity_score < 50:
            return "complex"
        else:
            return "very_complex"
    
    def get_size_category(self) -> str:
        """Categorize file by line count."""
        if self.line_count < 100:
            return "small"
        elif self.line_count < 500:
            return "medium"
        elif self.line_count < 1000:
            return "large"
        else:
            return "very_large"

def generate_description_md(file_path: Path, analyzer: PythonFileAnalyzer, use_ai: bool = False) -> str:
    """Generate .description.md content."""
    relative_path = safe_relative_path(file_path)
    
    # Try AI-enhanced description first
    if use_ai and AI_ENHANCED:
        try:
            ai_description = generate_ai_description(file_path, analyzer)
            if ai_description:
                return ai_description
        except Exception as e:
            if VERBOSE:
                print(f"  [!] AI enhancement failed, using standard generation: {e}")
    
    content = f"""# {file_path.stem}

**File**: `{relative_path}`  
**Type**: Python Module  
**Summary**: {analyzer.get_summary()}  
**Lines**: {analyzer.line_count}  
**Complexity**: {analyzer.complexity_score} ({analyzer.get_complexity_category()})

## Overview

"""
    
    if analyzer.docstring:
        content += f"{analyzer.docstring}\n\n"
    else:
        content += f"Python module containing implementation for {file_path.stem}.\n\n"
    
    # Classes section
    if analyzer.classes:
        content += f"## Classes ({len(analyzer.classes)})\n\n"
        for cls in analyzer.classes:
            content += f"### `{cls['name']}`\n\n"
            if cls['bases']:
                content += f"**Inherits from**: {', '.join(cls['bases'])}\n\n"
            if cls['docstring']:
                content += f"{cls['docstring']}\n\n"
            else:
                content += f"Class {cls['name']} implementation.\n\n"
            
            if cls['methods']:
                content += f"**Methods** ({len(cls['methods'])}):\n"
                for method in cls['methods'][:10]:  # Limit to first 10
                    args = ', '.join(method['args'])
                    content += f"- `{method['name']}({args})`\n"
                if len(cls['methods']) > 10:
                    content += f"- ... and {len(cls['methods']) - 10} more methods\n"
                content += "\n"
    
    # Functions section
    if analyzer.functions:
        content += f"## Functions ({len(analyzer.functions)})\n\n"
        for func in analyzer.functions[:10]:
            args = ', '.join(func['args'])
            content += f"### `{func['name']}({args})`\n\n"
            if func['docstring']:
                content += f"{func['docstring']}\n\n"
    
    # Imports section
    if analyzer.imports:
        content += f"## Dependencies\n\n"
        content += f"**Imports** ({len(analyzer.imports)}):\n"
        unique_imports = sorted(set(analyzer.imports))[:15]
        for imp in unique_imports:
            content += f"- `{imp}`\n"
        if len(analyzer.imports) > 15:
            content += f"- ... and {len(analyzer.imports) - 15} more\n"
        content += "\n"
    
    content += "---\n"
    content += "*Auto-generated documentation*\n"
    
    return content

def generate_improvements_md(file_path: Path, analyzer: PythonFileAnalyzer, use_ai: bool = False) -> str:
    """Generate .improvements.md content."""
    relative_path = safe_relative_path(file_path)
    
    # Try AI-enhanced improvements first
    if use_ai and AI_ENHANCED:
        try:
            ai_improvements = generate_ai_improvements(file_path, analyzer)
            if ai_improvements:
                return ai_improvements
        except Exception as e:
            if VERBOSE:
                print(f"  [!] AI enhancement failed, using standard generation: {e}")
    
    content = f"""# Improvements for {file_path.stem}

**File**: `{relative_path}`  
**Analysis Date**: {datetime.now().strftime('%Y-%m-%d %H:%M')}  
**Size**: {analyzer.line_count} lines ({analyzer.get_size_category()})  
**Complexity**: {analyzer.complexity_score} score ({analyzer.get_complexity_category()})

## Suggested Improvements

"""
    
    improvements = []
    
    # Documentation improvements
    if not analyzer.docstring:
        improvements.append("### Documentation\n- [!] **Missing module docstring** - Add comprehensive module-level documentation")
    
    undocumented_classes = [cls for cls in analyzer.classes if not cls['docstring']]
    if undocumented_classes:
        improvements.append(f"### Class Documentation\n- [!] **{len(undocumented_classes)} undocumented classes**: {', '.join([c['name'] for c in undocumented_classes[:5]])}")
    
    # Type hints
    improvements.append("### Type Annotations\n- [OK] Review and add type hints to all functions and methods for better IDE support")
    
    # Testing
    test_file = file_path.with_name(file_path.stem + '_test.py')
    if not test_file.exists():
        improvements.append(f"### Testing\n- [!] **Missing test file** - Create `{test_file.name}` with pytest tests")
    
    # Code organization
    if len(analyzer.classes) > 3:
        improvements.append(f"### Code Organization\n- [TIP] **{len(analyzer.classes)} classes in one file** - Consider splitting into separate modules")
    
    # Complexity
    if analyzer.content and len(analyzer.content.splitlines()) > 500:
        improvements.append(f"### File Complexity\n- [!] **Large file** ({len(analyzer.content.splitlines())} lines) - Consider refactoring")
    
    # Add improvements to content
    if improvements:
        content += "\n\n".join(improvements)
    else:
        content += "[OK] No major improvements identified.\n"
    
    content += "\n\n## Best Practices Checklist\n\n"
    content += "- [ ] All classes have docstrings\n"
    content += "- [ ] All public methods have docstrings\n"
    content += "- [ ] Type hints are present\n"
    content += "- [ ] pytest tests cover main functionality\n"
    content += "- [ ] Error handling is robust\n"
    content += "- [ ] Code follows PEP 8 style guide\n"
    content += "- [ ] No code duplication\n"
    content += "- [ ] Proper separation of concerns\n"
    
    content += "\n---\n"
    content += "*Auto-generated improvement suggestions*\n"
    
    return content

def generate_splice_md(file_path: Path, analyzer: PythonFileAnalyzer) -> str:
    """Generate .splice.md content for files with multiple classes."""
    relative_path = safe_relative_path(file_path)
    
    content = f"""# Class Breakdown: {file_path.stem}

**File**: `{relative_path}`  
**Classes**: {len(analyzer.classes)}

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

"""
    
    for i, cls in enumerate(analyzer.classes, 1):
        content += f"### {i}. `{cls['name']}`\n\n"
        content += f"**Line**: {cls['lineno']}  \n"
        if cls['bases']:
            content += f"**Inherits**: {', '.join(cls['bases'])}  \n"
        content += f"**Methods**: {len(cls['methods'])}\n\n"
        
        if cls['docstring']:
            content += f"{cls['docstring'][:200]}{'...' if len(cls['docstring']) > 200 else ''}\n\n"
        
        # Suggest split
        suggested_filename = f"{cls['name'].lower()}.py"
        content += f"[TIP] **Suggested split**: Move to `{suggested_filename}`\n\n"
        
        content += "---\n\n"
    
    content += "## Refactoring Strategy\n\n"
    content += "1. Create separate files for each class\n"
    content += "2. Update imports in dependent modules\n"
    content += "3. Create __init__.py to maintain backwards compatibility\n"
    content += "4. Run tests to ensure functionality is preserved\n"
    
    content += "\n---\n"
    content += "*Auto-generated class breakdown*\n"
    
    return content

def generate_test_file(file_path: Path, analyzer: PythonFileAnalyzer) -> str:
    """Generate *_test.py content."""
    module_name = file_path.stem
    relative_import = str(file_path.relative_to(Path.cwd() / "src")).replace('\\', '/').replace('/', '.')[:-3]
    
    content = f'''#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Tests for {module_name}
Auto-generated test template - expand with actual test cases
"""

import pytest
import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

try:
    from {relative_import} import *
except ImportError as e:
    pytest.skip(f"Cannot import module: {{e}}", allow_module_level=True)

'''
    
    # Generate tests for classes
    for cls in analyzer.classes:
        content += f'''
def test_{cls['name'].lower()}_exists():
    """Test that {cls['name']} class exists and is importable."""
    assert '{cls['name']}' in dir()

'''
        
        # Generate basic instantiation test if no __init__ args
        init_method = next((m for m in cls['methods'] if m['name'] == '__init__'), None)
        if init_method and len(init_method['args']) <= 1:  # Only 'self'
            content += f'''
def test_{cls['name'].lower()}_instantiation():
    """Test that {cls['name']} can be instantiated."""
    instance = {cls['name']}()
    assert instance is not None

'''
    
    # Generate tests for functions
    for func in analyzer.functions:
        if not func['name'].startswith('_'):  # Skip private functions
            content += f'''
def test_{func['name']}_exists():
    """Test that {func['name']} function exists."""
    assert callable({func['name']})

'''
    
    # Add a basic import test
    content += f'''
def test_module_imports():
    """Test that the module imports without errors."""
    assert True  # If we got here, imports worked

'''
    
    return content

def generate_ai_description(file_path: Path, analyzer: PythonFileAnalyzer) -> Optional[str]:
    """Generate AI-enhanced description using OpenAI API."""
    if not AI_ENHANCED or ai_client is None:
        return None
    
    # Prepare code snippet (truncate if too long)
    code_snippet = analyzer.content[:3000] if analyzer.content else ""
    
    prompt = f"""Analyze this Python module and provide a comprehensive, technical description.

File: {file_path.name}
Lines: {analyzer.line_count}
Classes: {len(analyzer.classes)}
Functions: {len(analyzer.functions)}

Code snippet:
```python
{code_snippet}
```

Provide a detailed markdown description including:
1. Purpose and functionality
2. Key classes and their roles
3. Important functions
4. Design patterns used
5. Dependencies and integrations

Format as markdown suitable for a .description.md file."""
    
    try:
        response = ai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert Python code analyst specializing in documenting complex codebases."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1500
        )
        return response.choices[0].message.content
    except Exception as e:
        if VERBOSE:
            print(f"  [!] AI description failed: {e}")
        return None

def generate_ai_improvements(file_path: Path, analyzer: PythonFileAnalyzer) -> Optional[str]:
    """Generate AI-enhanced improvement suggestions using OpenAI API."""
    if not AI_ENHANCED or ai_client is None:
        return None
    
    # Prepare code snippet
    code_snippet = analyzer.content[:3000] if analyzer.content else ""
    
    prompt = f"""Review this Python module and suggest specific, actionable improvements.

File: {file_path.name}
Lines: {analyzer.line_count}
Complexity: {analyzer.complexity_score}
Classes: {len(analyzer.classes)}
Functions: {len(analyzer.functions)}

Code snippet:
```python
{code_snippet}
```

Provide specific improvement suggestions covering:
1. Code quality and readability
2. Performance optimization opportunities
3. Error handling and robustness
4. Testing recommendations
5. Documentation gaps
6. Design pattern improvements
7. Type safety and validation

Format as markdown suitable for a .improvements.md file."""
    
    try:
        response = ai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert Python code reviewer specializing in code quality and best practices."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1500
        )
        return response.choices[0].message.content
    except Exception as e:
        if VERBOSE:
            print(f"  [!] AI improvements failed: {e}")
        return None

def discover_python_files(src_path: str) -> List[Path]:
    """Discover all .py files excluding *_test.py files."""
    python_files = []
    
    # Convert to absolute path
    src_abs = Path(src_path).resolve()
    
    for root, _, files in os.walk(src_abs):
        for file in files:
            if file.endswith('.py') and not file.endswith('_test.py'):
                filepath = Path(root) / file
                python_files.append(filepath)
    
    return sorted(python_files)

def load_checkpoint(checkpoint_file: str) -> set:
    """Load processed files from checkpoint."""
    checkpoint_path = Path(checkpoint_file)
    if checkpoint_path.exists():
        try:
            with open(checkpoint_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return set(data.get('processed_files', []))
        except Exception as e:
            print(f"[!] Cannot load checkpoint: {e}")
    return set()

def save_checkpoint(checkpoint_file: str, processed_files: set):
    """Save processed files to checkpoint."""
    checkpoint_path = Path(checkpoint_file)
    checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(checkpoint_path, 'w', encoding='utf-8') as f:
            json.dump({
                'processed_files': list(processed_files),
                'timestamp': datetime.now().isoformat()
            }, f, indent=2)
    except Exception as e:
        print(f"[!] Cannot save checkpoint: {e}")

def save_error_log(error_log_file: str, errors: List[ErrorRecord]):
    """Save error log to file."""
    error_log_path = Path(error_log_file)
    error_log_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(error_log_path, 'w', encoding='utf-8') as f:
            json.dump([asdict(error) for error in errors], f, indent=2)
    except Exception as e:
        print(f"[!] Cannot save error log: {e}")

def save_stats_json(stats_file: str, stats: ProcessingStats, errors: List[ErrorRecord]):
    """Save statistics to JSON file."""
    stats_path = Path(stats_file)
    stats_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        stats_dict = asdict(stats)
        stats_dict['elapsed_time'] = stats.elapsed_time()
        stats_dict['files_per_second'] = stats.files_per_second()
        stats_dict['errors_detail'] = [asdict(e) for e in errors[:20]]  # First 20 errors
        
        with open(stats_path, 'w', encoding='utf-8') as f:
            json.dump(stats_dict, f, indent=2)
        
        if VERBOSE:
            print(f"\n[STATS] Statistics saved to: {stats_file}")
    except Exception as e:
        print(f"[!] Cannot save stats JSON: {e}")

def process_single_file(
    file_path: Path,
    dry_run: bool,
    use_ai: bool,
    file_index: int,
    show_details: bool = True
) -> Tuple[Dict[str, Any], Optional[ErrorRecord]]:
    """Process a single Python file (for parallel execution)."""
    result: Dict[str, Any] = {
        'filepath': str(file_path.relative_to(Path.cwd())),
        'description_created': 0,
        'improvements_created': 0,
        'splice_created': 0,
        'test_created': 0,
        'renamed': 0,
        'line_count': 0,
        'complexity': 0,
        'size_category': 'unknown',
        'complexity_category': 'unknown'
    }
    error = None
    
    try:
        analyzer = PythonFileAnalyzer(file_path)
        
        # Track file statistics
        result['line_count'] = analyzer.line_count
        result['complexity'] = analyzer.complexity_score
        result['size_category'] = analyzer.get_size_category()
        result['complexity_category'] = analyzer.get_complexity_category()
        
        # Generate .description.md
        desc_file = file_path.with_suffix('.description.md')
        py_desc_file = Path(str(file_path) + '.description.md')
        
        if py_desc_file.exists() and not desc_file.exists():
            if not dry_run:
                py_desc_file.rename(desc_file)
            result['renamed'] += 1
            if show_details and file_index <= 20:
                print(f"  [OK] Rename: {py_desc_file.name} → {desc_file.name}")
        elif not desc_file.exists():
            desc_content = generate_description_md(file_path, analyzer, use_ai)
            if not dry_run:
                desc_file.write_text(desc_content, encoding='utf-8')
            result['description_created'] += 1
            if show_details and file_index <= 20:
                print(f"  + Create: {desc_file.name}")
        
        # Generate .improvements.md
        imp_file = file_path.with_suffix('.improvements.md')
        py_imp_file = Path(str(file_path) + '.improvements.md')
        
        if py_imp_file.exists() and not imp_file.exists():
            if not dry_run:
                py_imp_file.rename(imp_file)
            result['renamed'] += 1
            if show_details and file_index <= 20:
                print(f"  [OK] Rename: {py_imp_file.name} → {imp_file.name}")
        elif not imp_file.exists():
            imp_content = generate_improvements_md(file_path, analyzer, use_ai)
            if not dry_run:
                imp_file.write_text(imp_content, encoding='utf-8')
            result['improvements_created'] += 1
            if show_details and file_index <= 20:
                print(f"  + Create: {imp_file.name}")
        
        # Generate .splice.md if multiple classes
        if analyzer.has_multiple_classes():
            splice_file = file_path.with_suffix('.splice.md')
            if not splice_file.exists():
                splice_content = generate_splice_md(file_path, analyzer)
                if not dry_run:
                    splice_file.write_text(splice_content, encoding='utf-8')
                result['splice_created'] += 1
                if show_details and file_index <= 20:
                    print(f"  + Create: {splice_file.name} ({len(analyzer.classes)} classes)")
        
        # Generate *_test.py
        test_file = file_path.with_name(file_path.stem + '_test.py')
        if not test_file.exists():
            test_content = generate_test_file(file_path, analyzer)
            if not dry_run:
                test_file.write_text(test_content, encoding='utf-8')
            result['test_created'] += 1
            if show_details and file_index <= 20:
                print(f"  + Create: {test_file.name}")
    
    except Exception as e:
        error_type = type(e).__name__
        error = ErrorRecord(
            filepath=str(safe_relative_path(file_path)),
            error_type=error_type,
            error_message=str(e),
            timestamp=datetime.now().isoformat(),
            traceback=None
        )
        if show_details and file_index <= 20:
            print(f"  [X] Error processing {file_path.name}: {error_type} - {e}")
    
    return result, error

def analyze_and_generate(
    python_files: List[Path],
    dry_run: bool = True,
    use_ai: bool = False,
    resume: bool = False,
    checkpoint_file: str = CHECKPOINT_FILE,
    error_log_file: str = ERROR_LOG,
    workers: int = 4
) -> Tuple[ProcessingStats, List[ErrorRecord]]:
    """Analyze Python files and generate missing documentation with optional parallel processing."""
    
    stats = ProcessingStats(total_files=len(python_files), start_time=time.time())
    errors: List[ErrorRecord] = []
    
    # Load checkpoint if resuming
    processed_files = set()
    if resume:
        processed_files = load_checkpoint(checkpoint_file)
        stats.files_skipped = len(processed_files)
        if VERBOSE:
            print(f"Resuming from checkpoint: {len(processed_files)} files already processed\n")
    
    # Filter out already processed files
    files_to_process = [
        f for f in python_files 
        if str(safe_relative_path(f)) not in processed_files
    ]
    
    checkpoint_counter = 0
    CHECKPOINT_INTERVAL = 50  # Save checkpoint every 50 files
    
    # Use progress bar if available
    iterator = tqdm(files_to_process, desc="Processing files", unit="file") if HAS_TQDM else files_to_process
    
    # Parallel processing
    if workers > 1 and len(files_to_process) > 10:
        with ThreadPoolExecutor(max_workers=workers) as executor:
            # Submit all tasks
            future_to_file = {
                executor.submit(process_single_file, file_path, dry_run, use_ai, i + 1, i < 20): file_path
                for i, file_path in enumerate(files_to_process)
            }
            
            # Process completed tasks
            for future in as_completed(future_to_file):
                file_path = future_to_file[future]
                file_path_str = str(safe_relative_path(file_path))
                
                try:
                    result, error = future.result()
                    
                    # Update stats
                    stats.description_created += result['description_created']
                    stats.improvements_created += result['improvements_created']
                    stats.splice_created += result['splice_created']
                    stats.test_created += result['test_created']
                    stats.renamed += result['renamed']
                    stats.files_by_size[result['size_category']] += 1
                    stats.files_by_complexity[result['complexity_category']] += 1
                    stats.largest_files.append((result['filepath'], result['line_count']))
                    
                    if error:
                        stats.errors += 1
                        stats.error_types[error.error_type] += 1
                        errors.append(error)
                    
                    processed_files.add(file_path_str)
                    stats.files_processed += 1
                    checkpoint_counter += 1
                    
                    # Save checkpoint periodically
                    if checkpoint_counter >= CHECKPOINT_INTERVAL and not dry_run:
                        save_checkpoint(checkpoint_file, processed_files)
                        checkpoint_counter = 0
                    
                    # Update progress bar
                    if HAS_TQDM and hasattr(iterator, 'update'):
                        iterator.update(1)
                
                except Exception as e:
                    stats.errors += 1
                    error_type = type(e).__name__
                    stats.error_types[error_type] += 1
                    errors.append(ErrorRecord(
                        filepath=file_path_str,
                        error_type=error_type,
                        error_message=str(e),
                        timestamp=datetime.now().isoformat(),
                        traceback=None
                    ))
    else:
        # Sequential processing (fallback or when workers=1)
        for i, file_path in enumerate(iterator, 1):
            result, error = process_single_file(file_path, dry_run, use_ai, i, i <= 20)
            file_path_str = str(safe_relative_path(file_path))
            
            # Update stats
            stats.description_created += result['description_created']
            stats.improvements_created += result['improvements_created']
            stats.splice_created += result['splice_created']
            stats.test_created += result['test_created']
            stats.renamed += result['renamed']
            stats.files_by_size[result['size_category']] += 1
            stats.files_by_complexity[result['complexity_category']] += 1
            stats.largest_files.append((result['filepath'], result['line_count']))
            
            if error:
                stats.errors += 1
                stats.error_types[error.error_type] += 1
                errors.append(error)
            
            processed_files.add(file_path_str)
            stats.files_processed += 1
            checkpoint_counter += 1
            
            # Save checkpoint periodically
            if checkpoint_counter >= CHECKPOINT_INTERVAL and not dry_run:
                save_checkpoint(checkpoint_file, processed_files)
                checkpoint_counter = 0
            
            # Update progress bar
            if HAS_TQDM and hasattr(iterator, 'update') and callable(getattr(iterator, 'update', None)):
                iterator.update(1)
    
    # Keep only top 20 largest files
    stats.largest_files = sorted(stats.largest_files, key=lambda x: x[1], reverse=True)[:20]
    
    # Final checkpoint save
    if not dry_run:
        save_checkpoint(checkpoint_file, processed_files)
        if errors:
            save_error_log(error_log_file, errors)
    
    return stats, errors

def print_enhanced_stats(stats: ProcessingStats, errors: List[ErrorRecord]):
    """Print enhanced statistics report."""
    print("\n" + "=" * 110)
    print("  GENERATION SUMMARY".center(110))
    print("=" * 110)
    
    # Basic stats
    print(f"\nTotal Python files analyzed:     {stats.total_files:6d}")
    print(f"Files processed:                 {stats.files_processed:6d}")
    if stats.files_skipped > 0:
        print(f"Files skipped (checkpoint):      {stats.files_skipped:6d}")
    print(f"Description files created:       {stats.description_created:6d}")
    print(f"Improvement files created:       {stats.improvements_created:6d}")
    print(f"Splice files created:            {stats.splice_created:6d}")
    print(f"Test files created:              {stats.test_created:6d}")
    print(f"Files renamed:                   {stats.renamed:6d}")
    print(f"Errors encountered:              {stats.errors:6d}")
    
    # Performance stats
    print(f"\nElapsed Time:                    {stats.elapsed_time()}")
    print(f"Processing Rate:                 {stats.files_per_second():.2f} files/second")
    
    # Size distribution
    if stats.files_by_size:
        print("\n--- File Size Distribution ---")
        for size_cat in ['small', 'medium', 'large', 'very_large']:
            count = stats.files_by_size.get(size_cat, 0)
            if count > 0:
                pct = (count / stats.files_processed * 100) if stats.files_processed > 0 else 0
                print(f"  {size_cat:15s}: {count:5d} ({pct:5.1f}%)")
    
    # Complexity distribution
    if stats.files_by_complexity:
        print("\n--- Complexity Distribution ---")
        for complexity in ['simple', 'moderate', 'complex', 'very_complex']:
            count = stats.files_by_complexity.get(complexity, 0)
            if count > 0:
                pct = (count / stats.files_processed * 100) if stats.files_processed > 0 else 0
                print(f"  {complexity:15s}: {count:5d} ({pct:5.1f}%)")
    
    # Largest files
    if stats.largest_files:
        print("\n--- Top 10 Largest Files ---")
        for filepath, line_count in stats.largest_files[:10]:
            print(f"  {line_count:5d} lines: {filepath}")
    
    # Error breakdown
    if stats.error_types:
        print("\n--- Error Types ---")
        for error_type, count in sorted(stats.error_types.items(), key=lambda x: x[1], reverse=True):
            print(f"  {error_type:25s}: {count:5d}")
    
    # Error details (first 10)
    if errors:
        print("\n--- Recent Errors (first 10) ---")
        for error in errors[:10]:
            print(f"  {error.filepath}")
            print(f"    {error.error_type}: {error.error_message[:100]}")

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate documentation and tests for PyAgent Python files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Dry run (preview without creating files)
  python generate_docs_and_tests.py --dry-run

  # Execute generation
  python generate_docs_and_tests.py --execute

  # Use AI enhancement (requires OPENAI_API_KEY in .env)
  python generate_docs_and_tests.py --execute --ai

  # Resume interrupted run
  python generate_docs_and_tests.py --execute --resume

  # Process specific directory
  python generate_docs_and_tests.py --execute --path src/core
        """
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        default=True,
        help='Preview changes without creating files (default)'
    )
    parser.add_argument(
        '--execute',
        action='store_true',
        help='Execute and create files'
    )
    parser.add_argument(
        '--path',
        type=str,
        default='src',
        help='Source path to process (default: src)'
    )
    parser.add_argument(
        '--ai',
        action='store_true',
        help='Use AI enhancement for descriptions and improvements (requires OpenAI API key)'
    )
    parser.add_argument(
        '--resume',
        action='store_true',
        help='Resume from checkpoint (skip already processed files)'
    )
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Minimize output'
    )
    parser.add_argument(
        '--checkpoint',
        type=str,
        default=CHECKPOINT_FILE,
        help=f'Checkpoint file path (default: {CHECKPOINT_FILE})'
    )
    parser.add_argument(
        '--error-log',
        type=str,
        default=ERROR_LOG,
        help=f'Error log file path (default: {ERROR_LOG})'
    )
    parser.add_argument(
        '--workers',
        type=int,
        default=4,
        help='Number of parallel workers (default: 4, use 1 for sequential)'
    )
    parser.add_argument(
        '--json-export',
        type=str,
        default='',
        help='Export statistics to JSON file (e.g., data/logs/stats.json)'
    )
    
    args = parser.parse_args()
    
    # If --execute is specified, disable dry-run
    if args.execute:
        args.dry_run = False
    
    return args

def main():
    """Main entry point."""
    args = parse_arguments()
    
    global VERBOSE
    VERBOSE = not args.quiet
    
    print("=" * 110)
    print("  PyAgent Documentation & Test Generator".center(110))
    print("=" * 110)
    print()
    print(f"Mode:       {'DRY RUN (no files created)' if args.dry_run else 'EXECUTE (files will be created)'}")
    print(f"Source:     {args.path}")
    print(f"AI Enhanced: {'Yes' if args.ai and AI_ENHANCED else 'No'}")
    if args.ai and not AI_ENHANCED:
        print("  [!] AI enhancement requested but OpenAI API not available")
        print("    Install: pip install openai python-dotenv")
        print("    Set OPENAI_API_KEY in .env file")
    print(f"Resume:     {'Yes' if args.resume else 'No'}")
    print()
    
    # Discover files
    print("Discovering Python files...")
    python_files = discover_python_files(args.path)
    print(f"Found {len(python_files)} Python files (excluding *_test.py)\n")
    
    if not python_files:
        print("No Python files found!")
        return
    
    # Show sample
    if VERBOSE:
        print("Sample files (first 10):")
        for f in python_files[:10]:
            print(f"  {safe_relative_path(f)}")
        if len(python_files) > 10:
            print(f"  ... and {len(python_files) - 10} more\n")
    
    # Analyze and generate
    print("\nProcessing files...\n")
    if args.workers > 1:
        print(f"Using {args.workers} parallel workers\n")
    stats, errors = analyze_and_generate(
        python_files,
        dry_run=args.dry_run,
        use_ai=args.ai,
        resume=args.resume,
        checkpoint_file=args.checkpoint,
        error_log_file=args.error_log,
        workers=args.workers
    )
    
    # Report
    print_enhanced_stats(stats, errors)
    
    # Export JSON if requested
    if args.json_export:
        save_stats_json(args.json_export, stats, errors)
    
    if args.dry_run:
        print("\n[!] DRY RUN MODE - No files were created or modified")
        print("Run with --execute to create files")
    else:
        print("\n[OK] Files created successfully!")
        print(f"\nCheckpoint saved to: {args.checkpoint}")
        if errors:
            print(f"Error log saved to: {args.error_log}")
    
    print()

if __name__ == "__main__":
    main()
