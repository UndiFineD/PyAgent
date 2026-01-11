import os
import re
import sys

# Get absolute path to src
workspace_root = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(workspace_root, 'src')

print(f"Scanning: {src_path}")

mappings = [
    (r'from src\.logic\.coder\.models', 'from src.core.base.types'),
    (r'import src\.logic\.coder\.models', 'import src.core.base.types'),
    
    (r'from src\.logic\.coder\.analyzers', 'from src.logic.agents.development'),
    (r'from src\.logic\.coder\.core', 'from src.logic.agents.development'),
    
    (r'from src\.logic\.coder\.code_generator', 'from src.logic.agents.development.CodeGeneratorAgent'),
    (r'from src\.logic\.coder\.CodeReviewer', 'from src.logic.agents.development.CodeReviewerAgent'),
    (r'from src\.logic\.coder\.SecurityScanner', 'from src.logic.agents.security.SecurityScannerAgent'),
    
    (r'from src\.logic\.changes\.ChangesAgent', 'from src.logic.agents.swarm.ChangesAgent'),
    (r'from src\.logic\.changes\.ComplianceChecker', 'from src.logic.agents.security.ComplianceCheckerAgent'),
    
    # Generic logic.changes moves (mostly to types)
    (r'from src\.logic\.changes\.(?!ChangesAgent|ComplianceChecker|Changelog|Diff|Feed|Release|change_tracker|EntryReorderer|Monorepo|ReferenceLink)', 'from src.core.base.types.'),
    
    # Class renames
    (r'\bAccessibilityAnalyzer\b', 'AccessibilityAgent'),
    (r'\bConsistencyChecker\b', 'ConsistencyAgent'),
    (r'\bDependencyAnalyzer\b', 'DependencyAgent'),
    (r'\bModernizationAdvisor\b', 'ModernizationAgent'),
    (r'\bPerformanceOptimizer\b', 'PerformanceAgent'),
    (r'\bProfilingAdvisor\b', 'ProfilingAgent'),
    (r'\bTestGapAnalyzer\b', 'TestGapAgent'),
]

def fix_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {path}: {e}")
        return False
    
    new_content = content
    for pattern, replacement in mappings:
        new_content = re.sub(pattern, replacement, new_content)
    
    if new_content != content:
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
        except Exception as e:
            print(f"Error writing {path}: {e}")
            return False
    return False

count = 0
for root, dirs, files in os.walk(src_path):
    for file in files:
        if file.endswith('.py'):
            if fix_file(os.path.join(root, file)):
                count += 1

print(f"Fixed imports in {count} files.")

