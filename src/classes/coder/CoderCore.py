#!/usr/bin/env python3

"""
Computational core for code analysis, metrics, and quality assessment.
Designed for high-performance rule checking with future Rust integration.
"""

from .CodeLanguage import CodeLanguage
from .CodeMetrics import CodeMetrics
from .CodeSmell import CodeSmell
from .QualityScore import QualityScore
from .StyleRule import StyleRule
from .StyleRuleSeverity import StyleRuleSeverity
from src.classes.base_agent.core import LogicCore
from typing import Any, Dict, List, Optional, Tuple
import ast
import hashlib
import math
import re

# Logic extracted for future Rust migration (PyO3)
# Goal: Isolate all "Computationally Expensive" or "Rule-Based" logic here.

# Default style rules for Python (Re-declared here for Core access)
DEFAULT_PYTHON_STYLE_RULES: List[StyleRule] = [
    StyleRule(
        name="line_length",
        pattern=r"^.{89,}$",
        message="Line exceeds 88 characters",
        severity=StyleRuleSeverity.WARNING,
        language=CodeLanguage.PYTHON
    ),
    StyleRule(
        name="trailing_whitespace",
        pattern=r"[ \t]+$",
        message="Trailing whitespace detected",
        severity=StyleRuleSeverity.WARNING,
        language=CodeLanguage.PYTHON
    ),
    StyleRule(
        name="multiple_blank_lines",
        pattern=r"\n{4,}",
        message="More than 2 consecutive blank lines",
        severity=StyleRuleSeverity.INFO,
        language=CodeLanguage.PYTHON
    ),
    StyleRule(
        name="missing_docstring",
        pattern=r'^def\s+\w+\([^)]*\):\s*\n\s+(?!"")',
        message="Function missing docstring",
        severity=StyleRuleSeverity.WARNING,
        language=CodeLanguage.PYTHON
    ),
]

# Common code smells patterns
CODE_SMELL_PATTERNS: Dict[str, Dict[str, Any]] = {
    "long_method": {
        "threshold": 50,
        "message": "Method is too long (>{threshold} lines)",
        "category": "complexity"
    },
    "too_many_parameters": {
        "threshold": 5,
        "message": "Function has too many parameters (>{threshold})",
        "category": "complexity"
    },
    "duplicate_code": {
        "threshold": 3,
        "message": "Duplicate code detected ({count} occurrences)",
        "category": "duplication"
    },
    "deep_nesting": {
        "threshold": 4,
        "message": "Code is too deeply nested (>{threshold} levels)",
        "category": "complexity"
    },
    "god_class": {
        "threshold": 20,
        "message": "Class has too many methods (>{threshold})",
        "category": "design"
    },
}

class CoderCore(LogicCore):
    """Core logic for CoderAgent, target for Rust conversion."""
    
    def __init__(self, language: CodeLanguage) -> None:
        self.language = language

    def calculate_metrics(self, content: str) -> CodeMetrics:
        """Analyze code structure and compute metrics."""
        lines = content.split('\n')
        metrics = CodeMetrics()
        
        # Basic line counts
        for line in lines:
            stripped = line.strip()
            if not stripped:
                metrics.blank_lines += 1
            elif stripped.startswith('#') or stripped.startswith('//'):
                metrics.lines_of_comments += 1
            else:
                metrics.lines_of_code += 1

        # Language-specific deep analysis
        if self.language == CodeLanguage.PYTHON:
            try:
                tree = ast.parse(content)
                metrics = self._analyze_python_ast(tree, metrics)
            except SyntaxError:
                pass
        
        # General Maintainability Index
        if metrics.lines_of_code > 0:
            halstead_volume = metrics.lines_of_code * math.log2(
                max(1, metrics.function_count + metrics.class_count + 1))
            cc = max(1, metrics.cyclomatic_complexity)
            loc = metrics.lines_of_code
            cm = metrics.lines_of_comments
            metrics.maintainability_index = max(0, min(100, 
                171 - 5.2 * math.log(halstead_volume + 1) - 0.23 * cc - 16.2 * math.log(loc + 1) + 50 * math.sin(math.sqrt(2.4 * (cm / (loc + cm + 1))))))
                
        return metrics

    def _analyze_python_ast(self, tree: ast.AST, metrics: CodeMetrics) -> CodeMetrics:
        """Deep AST analysis for Python."""
        function_lengths: List[int] = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                metrics.function_count += 1
                if hasattr(node, 'end_lineno') and node.end_lineno is not None:
                    length = node.end_lineno - node.lineno + 1
                    function_lengths.append(length)
                    cc = 1
                    for child in ast.walk(node):
                        if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                            cc += 1
                        elif isinstance(child, ast.BoolOp):
                            cc += len(child.values) - 1
                    metrics.cyclomatic_complexity += cc
            elif isinstance(node, ast.ClassDef):
                metrics.class_count += 1
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                metrics.import_count += 1
        
        if function_lengths:
            metrics.average_function_length = sum(function_lengths) / len(function_lengths)
            metrics.max_function_length = max(function_lengths)
            
        return metrics

    def check_style(self, content: str, rules: List[StyleRule]) -> List[Dict[str, Any]]:
        """Run regex-based style checks."""
        violations: List[Dict[str, Any]] = []
        lines = content.split('\n')
        for rule in rules:
            if not rule.enabled: continue
            if rule.language and rule.language != self.language: continue
            
            if '\n' in rule.pattern or rule.pattern.startswith('^'):
                for match in re.finditer(rule.pattern, content, re.MULTILINE):
                    line_no = content.count('\n', 0, match.start()) + 1
                    violations.append({
                        "rule": rule.name,
                        "message": rule.message,
                        "severity": rule.severity.value if hasattr(rule.severity, 'value') else str(rule.severity),
                        "line": line_no,
                        "content": match.group(0).split('\n')[0][:80]
                    })
            else:
                for i, line in enumerate(lines, 1):
                    if re.search(rule.pattern, line):
                        violations.append({
                            "rule": rule.name,
                            "message": rule.message,
                            "severity": rule.severity.value if hasattr(rule.severity, 'value') else str(rule.severity),
                            "line": i,
                            "content": line[:80]
                        })
        return violations

    def auto_fix_style(self, content: str, rules: List[StyleRule]) -> Tuple[str, int]:
        """Apply rules that have auto-fix capabilities."""
        fixed_content = content
        fix_count = 0
        for rule in rules:
            if not rule.enabled or not rule.auto_fix: continue
            if rule.language and rule.language != self.language: continue
            
            new_content = rule.auto_fix(fixed_content)
            if new_content != fixed_content:
                fix_count += 1
                fixed_content = new_content
        
        # Standard cleanup
        lines = fixed_content.split('\n')
        cleaned = [line.rstrip() for line in lines]
        if cleaned != lines:
            fix_count += 1
            fixed_content = '\n'.join(cleaned)
            
        return fixed_content, fix_count

    def detect_code_smells(self, content: str) -> List[CodeSmell]:
        """Detect common architectural code smells."""
        smells: List[CodeSmell] = []
        if self.language != CodeLanguage.PYTHON:
            return smells
            
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return smells
            
        lines = content.split('\n')
        for node in ast.walk(tree):
            # Long method detection
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if (hasattr(node, 'end_lineno') and node.end_lineno is not None):
                    length = node.end_lineno - node.lineno + 1
                    threshold = CODE_SMELL_PATTERNS["long_method"]["threshold"]
                    if length > threshold:
                        smells.append(CodeSmell(
                            name="long_method",
                            description=f"Method '{node.name}' is {length} lines (>{threshold})",
                            severity="warning",
                            line_number=node.lineno,
                            suggestion=f"Consider breaking down '{node.name}' into smaller functions",
                            category="complexity"
                        ))
                
                # Too many parameters
                param_count = len(node.args.args)
                threshold = CODE_SMELL_PATTERNS["too_many_parameters"]["threshold"]
                if param_count > threshold:
                    smells.append(CodeSmell(
                        name="too_many_parameters",
                        description=f"Function '{node.name}' has {param_count} parameters (>{threshold})",
                        severity="warning",
                        line_number=node.lineno,
                        suggestion="Consider using a data class or dictionary for parameters",
                        category="complexity"
                    ))

            # God class detection
            if isinstance(node, ast.ClassDef):
                method_count = sum(1 for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)))
                threshold = CODE_SMELL_PATTERNS["god_class"]["threshold"]
                if method_count > threshold:
                    smells.append(CodeSmell(
                        name="god_class",
                        description=f"Class '{node.name}' has {method_count} methods (>{threshold})",
                        severity="warning",
                        line_number=node.lineno,
                        suggestion="Consider splitting the class into smaller, more focused classes.",
                        category="design"
                    ))

        # Deep nesting detection
        for i, line in enumerate(lines, 1):
            indent = len(line) - len(line.lstrip())
            nesting = indent // 4
            threshold = CODE_SMELL_PATTERNS["deep_nesting"]["threshold"]
            if nesting > threshold and line.strip():
                smells.append(CodeSmell(
                    name="deep_nesting",
                    description=f"Code at line {i} has {nesting} levels of nesting (>{threshold})",
                    severity="info",
                    line_number=i,
                    suggestion="Consider early returns or extracting nested logic",
                    category="complexity"
                ))
        
        return smells

    def find_duplicate_code(self, content: str, min_lines: int = 4) -> List[Dict[str, Any]]:
        """Find duplicate code blocks using hashing."""
        lines = content.split('\n')
        duplicates: List[Dict[str, Any]] = []
        hashes: Dict[str, List[int]] = {}
        
        for i in range(len(lines) - min_lines + 1):
            block = '\n'.join(lines[i:i + min_lines])
            normalized = re.sub(r'\s+', ' ', block.strip())
            if len(normalized) < 20: continue
            
            block_hash = hashlib.md5(normalized.encode()).hexdigest()
            if block_hash not in hashes:
                hashes[block_hash] = []
            hashes[block_hash].append(i + 1)
            
        for block_hash, line_numbers in hashes.items():
            if len(line_numbers) > 1:
                duplicates.append({
                    "hash": block_hash,
                    "occurrences": len(line_numbers),
                    "lines": line_numbers,
                    "preview": '\n'.join(lines[line_numbers[0] - 1:line_numbers[0] - 1 + min_lines])[:100]
                })
        return duplicates

    def calculate_quality_score(self, metrics: CodeMetrics, violations: List[Dict[str, Any]], smells: List[CodeSmell], coverage: float) -> QualityScore:
        """Aggregate all analysis into a single QualityScore."""
        score = QualityScore()
        score.maintainability = min(100, metrics.maintainability_index)
        
        # Readability score
        readability_deductions = len(violations) * 5
        score.readability = max(0, 100 - readability_deductions)
        
        # Complexity score
        if metrics.function_count > 0:
            avg_cc = metrics.cyclomatic_complexity / metrics.function_count
            score.complexity = max(0, 100 - (avg_cc - 1) * 10)
        else:
            score.complexity = 100
            
        # Documentation score
        if metrics.lines_of_code > 0:
            comment_ratio = metrics.lines_of_comments / metrics.lines_of_code
            score.documentation = min(100, comment_ratio * 200)
            
        score.test_coverage = coverage
        
        # Overall score (weighted average)
        score.overall_score = (
            score.maintainability * 0.25 +
            score.readability * 0.25 +
            score.complexity * 0.25 +
            score.documentation * 0.15 +
            score.test_coverage * 0.10
        )
        
        # Add primary issues
        for violation in violations[:5]:
            score.issues.append(f"Style: {violation['message']} (line {violation['line']})")
        for smell in smells[:5]:
            score.issues.append(f"Smell: {smell.description}")
            
        return score
