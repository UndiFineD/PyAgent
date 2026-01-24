import os

dirs = [
    "src/logic/agents/cognitive/context",
    "src/logic/agents/cognitive/context/engines",
    "src/logic/agents/cognitive/context/engines/core_mixins",
    "src/logic/agents/cognitive/context/engines/knowledge_mixins",
    "src/logic/agents/cognitive/context/engines/memory_mixins",
    "src/logic/agents/cognitive/context/engines/mixins",
    "src/logic/agents/cognitive/context/utils",
    "src/logic/agents/cognitive/core",
    "src/logic/agents/cognitive/mixins",
]

for d in dirs:
    init_path = os.path.join(d, "__init__.py")
    if not os.path.exists(init_path):
        print(f"Creating {init_path}")
        with open(init_path, "w", encoding="utf-8") as f:
            f.write("# Generated __init__.py\n")
    else:
        print(f"{init_path} already exists")
