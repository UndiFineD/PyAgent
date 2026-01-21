
import os
import shutil
import subprocess
from pathlib import Path

# Paths
BASE_DIR = Path("c:/DEV/PyAgent/src/logic/agents")
DEV_DIR = BASE_DIR / "development"

# Target Folders
ANALYSIS = BASE_DIR / "analysis"
MULTIMODAL = BASE_DIR / "multimodal"
SECURITY = BASE_DIR / "security"
INFRA = BASE_DIR / "infrastructure"
SYSTEM = BASE_DIR / "system"
SPECIALISTS = BASE_DIR / "specialists"

MAPPING = {
    # Analysis
    "benchmark_agent.py": ANALYSIS,
    "code_quality_agent.py": ANALYSIS,
    "code_reviewer_agent.py": ANALYSIS,
    "consistency_agent.py": ANALYSIS,
    "dependency_agent.py": ANALYSIS,
    "dependency_graph_agent.py": ANALYSIS,
    "linting_agent.py": ANALYSIS,
    "performance_agent.py": ANALYSIS,
    "profiling_agent.py": ANALYSIS,
    "quality_gate_agent.py": ANALYSIS,
    "tech_debt_agent.py": ANALYSIS,
    "test_agent.py": ANALYSIS,
    "test_gap_agent.py": ANALYSIS,
    "type_safety_agent.py": ANALYSIS,
    "code_quality_core.py": ANALYSIS, # Direct move for now
    "tech_debt_core.py": ANALYSIS,
    "dependency_core.py": ANALYSIS,

    # Multimodal
    "android_agent.py": MULTIMODAL,
    "ui_architect_agent.py": MULTIMODAL,
    "svg_agent.py": MULTIMODAL,

    # Security
    "ethics_guardrail_agent.py": SECURITY,
    "security_agent.py": SECURITY,
    "security_guard_agent.py": SECURITY,
    "security_audit_manager.py": SECURITY,
    "security_core.py": SECURITY,

    # Infrastructure
    "infrastructure_manager_agent.py": INFRA,
    "infrastructure_repair_agent.py": INFRA,
    "network_arch_search_agent.py": INFRA,

    # System
    "dashboard_agent.py": SYSTEM,
    "process_synthesizer_agent.py": SYSTEM,
    "sandbox_agent.py": SYSTEM,
    "self_healing_agent.py": SYSTEM,
    "self_optimizer_agent.py": SYSTEM,

    # Specialists
    "handy_agent.py": SPECIALISTS,
    "accessibility_agent.py": SPECIALISTS,
}

# Sub-Mapping for core/ and mixins/ if they exist
CORE_MAPPING = {
    "benchmark_core.py": ANALYSIS / "core",
    "android_core.py": MULTIMODAL / "core",
}

MIXIN_MAPPING = {
    "security_auditor_mixin.py": SECURITY / "mixins",
    "security_reporter_mixin.py": SECURITY / "mixins",
    "security_scanner_mixin.py": SECURITY / "mixins",
    "accessibility_core_mixin.py": SPECIALISTS / "mixins",
    "accessibility_logic_mixin.py": SPECIALISTS / "mixins",
    "accessibility_report_mixin.py": SPECIALISTS / "mixins",
    "handy_core_mixin.py": SPECIALISTS / "mixins",
    "handy_file_system_mixin.py": SPECIALISTS / "mixins",
    "handy_terminal_mixin.py": SPECIALISTS / "mixins",
}

def move_files():
    print("Moving files...")
    # Create necessary subdirs
    for target in [ANALYSIS, MULTIMODAL, SECURITY, INFRA, SYSTEM, SPECIALISTS]:
        (target / "core").mkdir(parents=True, exist_ok=True)
        (target / "mixins").mkdir(parents=True, exist_ok=True)

    # Move root agents
    for filename, target in MAPPING.items():
        src = DEV_DIR / filename
        if src.exists():
            dest = target / filename
            print(f"Moving {src} to {dest}")
            shutil.move(str(src), str(dest))
        else:
            print(f"Warning: {src} not found")

    # Move cores
    for filename, target in CORE_MAPPING.items():
        src = DEV_DIR / "core" / filename
        if src.exists():
            dest = target / filename
            print(f"Moving {src} to {dest}")
            shutil.move(str(src), str(dest))

    # Move mixins
    for filename, target in MIXIN_MAPPING.items():
        src = DEV_DIR / "mixins" / filename
        if src.exists():
            dest = target / filename
            print(f"Moving {src} to {dest}")
            shutil.move(str(src), str(dest))

def update_imports():
    print("Updating imports...")
    # Build list of all moved files for replacement
    all_moved = {}
    for filename, target in MAPPING.items():
        old_path = f"src.logic.agents.development.{filename[:-3]}"
        new_path = f"src.logic.agents.{target.name}.{filename[:-3]}"
        all_moved[old_path] = new_path

    for filename, target in CORE_MAPPING.items():
        old_path = f"src.logic.agents.development.core.{filename[:-3]}"
        new_path = f"src.logic.agents.{target.parent.name}.core.{filename[:-3]}"
        all_moved[old_path] = new_path

    for filename, target in MIXIN_MAPPING.items():
        old_path = f"src.logic.agents.development.mixins.{filename[:-3]}"
        new_path = f"src.logic.agents.{target.parent.name}.mixins.{filename[:-3]}"
        all_moved[old_path] = new_path

    # Sort by length descending to avoid partial replacements
    sorted_items = sorted(all_moved.items(), key=lambda x: len(x[0]), reverse=True)

    # Use ripgrep to find files containing any of the old paths
    # We'll batch them to avoid too many shell calls
    batch_size = 10
    for i in range(0, len(sorted_items), batch_size):
        batch = sorted_items[i:i+batch_size]
        pattern = "|".join([old.replace(".", "\\.") for old, _ in batch])

        # Find files using powershell Select-String since rg might not be in path
        print(f"Batch {i//batch_size}: Replacing {pattern}")
        for old_import, new_import in batch:
            cmd = f'powershell -Command "Get-ChildItem -Path c:/DEV/PyAgent/src -Recurse -File -Include *.py | ForEach-Object {{ (Get-Content $_.FullName) -replace \'{old_import}\', \'{new_import}\' | Set-Content $_.FullName }}"'
            subprocess.run(cmd, shell=True)
            # Also update tests
            cmd_tests = f'powershell -Command "Get-ChildItem -Path c:/DEV/PyAgent/tests -Recurse -File -Include *.py | ForEach-Object {{ (Get-Content $_.FullName) -replace \'{old_import}\', \'{new_import}\' | Set-Content $_.FullName }}"'
            subprocess.run(cmd_tests, shell=True)

if __name__ == "__main__":
    move_files()
    update_imports()
    print("Done!")
