import os

def fix_json_reimports():
    files = [
        "src/logic/agents/cognitive/world_model_agent.py",
        "src/logic/agents/cognitive/context/engines/core_mixins/core_partition_mixin.py"
    ]
    for path in files:
        if not os.path.exists(path): continue
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        new_lines = []
        for line in lines:
            if "import json" in line and (line.startswith("        ") or line.startswith("    ")):
                continue
            new_lines.append(line)
        with open(path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

def fix_knowledge_main_v2():
    path = "src/logic/agents/cognitive/context/knowledge_main.py"
    if not os.path.exists(path): return
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    new_lines = []
    import_found = False
    for line in lines:
        if "from src.logic.agents.cognitive.knowledge_agent import KnowledgeAgent" in line:
            import_found = True
            continue
        new_lines.append(line)
    
    if import_found:
        # Insert at the top (after imports)
        for i, line in enumerate(new_lines):
            if line.startswith("from src.core.base.lifecycle.version import VERSION"):
                new_lines.insert(i + 1, "from src.logic.agents.cognitive.knowledge_agent import KnowledgeAgent\n")
                break
    
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

def fix_more_docstrings():
    # Simple fix: if function has no docstring, add an empty one
    paths = [
        "src/logic/agents/cognitive/context/engines/graph_core.py",
        "src/logic/agents/cognitive/context/utils/branch_comparer.py",
        "src/logic/agents/cognitive/context/utils/context_sharing_manager.py",
        "src/logic/agents/cognitive/context/utils/context_visualizer.py",
        "src/logic/agents/cognitive/context/utils/merge_conflict_resolver.py",
    ]
    for path in paths:
        if not os.path.exists(path): continue
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        new_lines = []
        for i, line in enumerate(lines):
            new_lines.append(line)
            if "def " in line and ":" in line and not line.strip().startswith("#"):
                # Check next non-empty line
                has_doc = False
                for j in range(i+1, min(i+5, len(lines))):
                    l_next = lines[j].strip()
                    if l_next.startswith('"""'):
                        has_doc = True
                        break
                    if l_next and not l_next.startswith("#"):
                        break
                if not has_doc:
                    indent = len(line) - len(line.lstrip())
                    new_lines.append(" " * (indent + 4) + '"""Docstring for ' + line.split("def ")[1].split("(")[0] + '."""\n')
        with open(path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

fix_json_reimports()
fix_knowledge_main_v2()
fix_more_docstrings()
