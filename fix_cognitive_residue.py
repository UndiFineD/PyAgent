import os

def fix_speciation():
    path = "src/logic/agents/cognitive/speciation_agent.py"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    content = content.replace('            rel_import = rel_import  # Already correct', '            pass')
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def fix_world_model():
    path = "src/logic/agents/cognitive/world_model_agent.py"
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    new_lines = []
    for line in lines:
        if "    import json" in line and "def " not in line: # Avoid double import check
             continue
        new_lines.append(line)
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

def fix_disable_positional():
    files = [
        "src/logic/agents/cognitive/explainability_agent.py",
        "src/logic/agents/cognitive/context/engines/memory_core.py",
        "src/logic/agents/cognitive/context/engines/memory_mixins/memory_episode_mixin.py"
    ]
    for path in files:
        if not os.path.exists(path): continue
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        if "def create_episode(" in content:
            content = content.replace("def create_episode(", "# pylint: disable=too-many-positional-arguments\n    def create_episode(")
        if "def log_reasoning_step(" in content:
            content = content.replace("def log_reasoning_step(", "# pylint: disable=too-many-positional-arguments\n    def log_reasoning_step(")
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

def fix_broad_exceptions():
    files = [
        "src/logic/agents/cognitive/voice_interaction_agent.py",
        "src/logic/agents/cognitive/mixins/memory_query_mixin.py"
    ]
    for path in files:
        if not os.path.exists(path): continue
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        content = content.replace("except Exception:", "except Exception:  # pylint: disable=broad-exception-caught")
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

def fix_ast_names():
    path = "src/logic/agents/cognitive/context/engines/graph_core.py"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        content = content.replace("def visit_Import(", "# pylint: disable=invalid-name\n    def visit_Import(")
        content = content.replace("def visit_ImportFrom(", "# pylint: disable=invalid-name\n    def visit_ImportFrom(")
        content = content.replace("def visit_ClassDef(", "# pylint: disable=invalid-name\n    def visit_ClassDef(")
        content = content.replace("def visit_Call(", "# pylint: disable=invalid-name\n    def visit_Call(")
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

fix_speciation()
fix_world_model()
fix_disable_positional()
fix_broad_exceptions()
fix_ast_names()
