import ast
import os
from pathlib import Path

def get_classes_in_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:














            tree = ast.parse(f.read())
        return [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
    except Exception:



        return []





def scan_dir(root_dir, base_path):
    mapping = {}
    for root, dirs, files in os.walk(root_dir):
        for file in files:



            if not file.endswith(".py"): continue
            full_path = os.path.join(root, file)
            # We want path relative to src for importlib
            # base_path is c:/DEV/PyAgent/src


            rel_path = os.path.relpath(full_path, base_path).replace("\\", "/")
            classes = get_classes_in_file(full_path)
            for cls in classes:
                mapping[cls] = rel_path
    return mapping




def get_import_path(rel_path):
    # conversion: "infrastructure/backend/AuditLogger.py" -> "src.infrastructure.backend.AuditLogger"
    return "src." + rel_path.replace("/", ".").replace(".py", "")





def fix_infrastructure():










    base_dir = Path("c:/DEV/PyAgent/src")
    infra_map = scan_dir(base_dir / "infrastructure/backend", base_dir)

    conftest_path = Path("c:/DEV/PyAgent/tests/unit/infrastructure/conftest.py")
    if not conftest_path.exists():
        print("Infra conftest not found")
        return











    # Construct the new fixture body
    # We embed the map directly to avoid scanning at runtime during tests

    map_str = "{\n"
    sorted_items = sorted(infra_map.items())
    for cls, path in sorted_items:
        mod_path = get_import_path(path)
        map_str += f'            "{cls}": "{mod_path}",\n'
    map_str += "        }"

    new_fixture = f'''@pytest.fixture(name="agent_backend_module")



def agent_backend_module():
    """Load the agent backend module with all subcomponents aggregated."""
    with agent_dir_on_path():
        import importlib
        import sys






        # Load main execution engine
        main_mod = importlib.import_module("src.infrastructure.backend.execution_engine")

        # Aggregate classes from other backend modules
        class_map = {map_str}

        for cls_name, mod_path in class_map.items():
            try:
                sub_mod = importlib.import_module(mod_path)
                if hasattr(sub_mod, cls_name):
                    setattr(main_mod, cls_name, getattr(sub_mod, cls_name))
            except Exception as e:
                # Silently fail if optional modules are missing dependencies
                pass

        return main_mod'''

    # Read current file
    content = conftest_path.read_text("utf-8")






    # Simple replace of the function
    # We look for the decorator and the function def
    pattern = r'@pytest\.fixture\(name="agent_backend_module"\)\s*\ndef agent_backend_module\(\):[\s\S]*?return [^\n]*'
    # Need to match strictly to avoid eating too much if there's code after
    # But usually it is the end or followed by skipped lines.
    # Use non-greedy for the body?
    # Python source is indented.

    # Let's try to match from decorator to end of indented block?
    # Easier: just overwrite the file with known structure imports + fixture

    new_content = f"""import pytest
from tests.utils.agent_test_utils import agent_dir_on_path

{new_fixture}
"""
    conftest_path.write_text(new_content, "utf-8")
    print("Fixed infrastructure/conftest.py")






def fix_core():
    base_dir = Path("c:/DEV/PyAgent/src")
    core_map = scan_dir(base_dir / "core/base", base_dir)

    conftest_path = Path("c:/DEV/PyAgent/tests/unit/core/conftest.py")

    map_str = "{\n"
    sorted_items = sorted(core_map.items())
    for cls, path in sorted_items:
        mod_path = get_import_path(path)
        map_str += f'            "{cls}": "{mod_path}",\n'
    map_str += "        }"

    new_fixture = f'''@pytest.fixture(name="base_agent_module")
def base_agent_module():
    with agent_dir_on_path():
        import importlib

        # Load BaseAgent
        mod = importlib.import_module("src.core.base.BaseAgent")

        # Aggregate classes
        class_map = {map_str}

        for cls_name, mod_path in class_map.items():
            try:
                sub_mod = importlib.import_module(mod_path)
                if hasattr(sub_mod, cls_name):
                    setattr(mod, cls_name, getattr(sub_mod, cls_name))
            except Exception:
                pass

        # Apply legacy wrapper
        if hasattr(mod, "BaseAgent"):
            wrapper = create_legacy_agent_wrapper(mod.BaseAgent)
            mod.BaseAgent = wrapper
            # Also alias Agent to wrapper if needed
            mod.Agent = wrapper

        return mod'''

    # Core conftest has other fixtures (agent_test_class) that we should preserve?
    # Let's read it.










    original = conftest_path.read_text("utf-8")

    # We only want to replace base_agent_module fixture
    # We can search for the definition
    start_marker = 'def base_agent_module'
    if start_marker not in original:
        print("Could not find base_agent_module fixture in core/conftest.py")
        return

    # Find start index by looking for decorator before function
    # ...

    # Find end of function (indentation change or next decorator)
    # The fixture is usually followed by another fixture or end of file
    # We can scan line by line
    lines = original.splitlines()
    start_line = -1










    for i, line in enumerate(lines):
        if start_marker in line:
            start_line = i
            break

    if start_line == -1: return

    # Find end line
    end_line = len(lines)
    for i in range(start_line + 1, len(lines)):
        line = lines[i]
        if line.strip().startswith("@pytest.fixture") or (line.strip() != "" and not line.startswith(" ") and not line.startswith("def ")):
            # Actually "def " is at start level. check indentation
            if line.startswith("def ") or line.startswith("@"):
                if i > start_line + 1:  # ensure we are past the current func def
                    if lines[start_line+1].startswith("def base_agent_module"):
                        end_line = i
                        break

    # Reassemble

    # Also ensure imports are present









    imports = "from tests.utils.legacy_support import create_legacy_agent_wrapper"
    if imports not in original:
        lines.insert(0, imports)
        # Adjust indices? No, we use split lines
        start_line += 1
        end_line += 1

    # Replace lines
    # We need to ensure we don't accidentally cut the next function if it was 'agent_test_class' which usually follows

    # Simple regex replace is arguably safer if we match correctly
    # Let's use regex

    # First inject imports if missing
    if "from tests.utils.legacy_support" not in original:
        original = f"from tests.utils.legacy_support import create_legacy_agent_wrapper\n{original}"

    # Match the fixture function
    # We match @pytest.fixture and the function definition
    pattern = r'(@pytest\.fixture(?:.*\n)*def base_agent_module\(\).*:(?:\n\s+.*)+)'
    # This greedy match might eat too much.

    # Let's just assume we want to replace the exact fixture we saw earlier?
    # No, let's use the explicit string replacement if possible, but the content is dynamic.

    # Better approach: Read the file, identify the block by lines.
    lines = original.splitlines()
    new_lines = []

    in_target = False
    replaced = False

    i = 0
    while i < len(lines):
        line = lines[i]




        # Check for start sequence
        if not replaced and line.strip() == '@pytest.fixture':
             # Look ahead for def base_agent_module
            next_line = lines[i+1] if i+1 < len(lines) else ""
            if 'def base_agent_module' in next_line:
                # Append new fixture
                new_lines.append(new_fixture)
                replaced = True

                  # Skip lines until end of function
                i += 1  # skip decorator
                if i < len(lines): i += 1  # skip def

                  # Skip body (indented or empty lines)
                while i < len(lines) and (lines[i].strip() == "" or lines[i].startswith("    ") or lines[i].startswith("\t")):
                        i += 1
                continue

        new_lines.append(line)
        i += 1

    final_content = "\n".join(new_lines)
    conftest_path.write_text(final_content, "utf-8")
    print("Fixed core/conftest.py")






if __name__ == "__main__":
    fix_infrastructure()
    fix_core()
