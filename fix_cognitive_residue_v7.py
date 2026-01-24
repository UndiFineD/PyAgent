#!/usr/bin/env python3
import os
import re

root = "src/logic/agents/cognitive"

def fix_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return
    
    # 1. Fix the sys.path indent bug in context/ files
    if "if str(root / \"src\") not in sys.path:" in content:
        # We look for the pattern where from follows the sys.path.append indented
        content = re.sub(
            r'if str\(root / "src"\) not in sys.path:\s*sys.path.append\(str\(root / "src"\)\)\s+from',
            r'if str(root / "src") not in sys.path:\n    sys.path.append(str(root / "src"))\n\nfrom',
            content,
            flags=re.MULTILINE
        )

    # 2. Fix KnowledgeAgent missing import in knowledge_main.py
    if "agent = KnowledgeAgent(args.dir)" in content and "KnowledgeAgent" not in content[:500]:
        content = content.replace("from __future__ import annotations", "from __future__ import annotations\nfrom src.logic.agents.cognitive.knowledge_agent import KnowledgeAgent")
    
    # 3. Fix TheoryOfMindCore and MemoryConsolidatorCore imports
    content = content.replace(
        "from src.logic.agents.cognitive.TheoryOfMindCore import TheoryOfMindCore",
        "from .core.theory_of_mind_core import TheoryOfMindCore"
    )
    content = content.replace(
        "from src.logic.agents.cognitive.MemoryConsolidatorCore import MemoryConsolidatorCore",
        "from .core.memory_consolidator_core import MemoryConsolidatorCore"
    )

    # 4. Fix create_main_function argument count
    content = re.sub(
        r'create_main_function\((\w+)\)',
        r'create_main_function(\1, "\1: Specialist Agent", "Context for analysis")',
        content
    )

    # 5. Fix self-assigning variable in speciation_agent.py
    if "rel_import = rel_import" in content:
        content = content.replace("rel_import = rel_import", "pass")

    # 6. Fix unreachable code in knowledge_graph_assistant.py
    # return items\n        """Deduplicate..."""
    if 'return items\n        """' in content:
        content = content.replace('return items\n        """', 'return items')

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

for dirpath, _, filenames in os.walk(root):
    for filename in filenames:
        if filename.endswith(".py"):
            fix_file(os.path.join(dirpath, filename))
