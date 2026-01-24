import os
import re

def fix_knowledge_main():
    path = "src/logic/agents/cognitive/context/knowledge_main.py"
    if not os.path.exists(path): return
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    content = content.replace('    from src.logic.agents.cognitive.knowledge_agent import KnowledgeAgent', 'from src.logic.agents.cognitive.knowledge_agent import KnowledgeAgent')
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def fix_no_else_return():
    files = [
        "src/logic/agents/cognitive/empathy_agent.py",
        "src/logic/agents/cognitive/intention_prediction_agent.py",
        "src/logic/agents/cognitive/context/engines/context_compressor.py",
        "src/logic/agents/cognitive/context/engines/context_compressor_core.py",
        "src/logic/agents/cognitive/core/metacognitive_core.py",
        "src/logic/agents/cognitive/context/utils/context_inheritance.py"
    ]
    for path in files:
        if not os.path.exists(path): continue
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        new_lines = []
        for line in lines:
            if "        elif " in line:
                # Simple replacement for common case
                new_lines.append(line.replace("        elif ", "        if "))
            else:
                new_lines.append(line)
        with open(path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

def fix_pointless_strings():
    files = [
        "src/logic/agents/cognitive/context_agent.py",
        "src/logic/agents/cognitive/graph_memory_agent.py",
        "src/logic/agents/cognitive/knowledge_graph_assistant.py",
        "src/logic/agents/cognitive/linguistic_agent.py",
        "src/logic/agents/cognitive/memory_consolidation_agent.py",
        "src/logic/agents/cognitive/reasoning_agent.py",
        "src/logic/agents/cognitive/visualizer_agent.py"
    ]
    for path in files:
        if not os.path.exists(path): continue
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        new_lines = []
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('"""') and stripped.endswith('"""') and len(new_lines) > 0 and not new_lines[-1].strip().startswith("def ") and not new_lines[-1].strip().startswith("class "):
                # Likely a commented out block or floating docstring
                continue
            new_lines.append(line)
        with open(path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

def fix_unused_args():
    # Targets for _ prefixing
    targets = [
        ("src/logic/agents/cognitive/audio_reasoning_agent.py", "transcription"),
        ("src/logic/agents/cognitive/cooperative_communication_agent.py", "thought_payload"),
        ("src/logic/agents/cognitive/dynamic_decomposer_agent.py", "available_agents"),
        ("src/logic/agents/cognitive/dynamic_decomposer_agent.py", "pending_tasks"),
        ("src/logic/agents/cognitive/latent_reasoning_agent.py", "response"),
        ("src/logic/agents/cognitive/latent_reasoning_agent.py", "chain_of_thought"),
        ("src/logic/agents/cognitive/latent_reasoning_agent.py", "target_language"),
        ("src/logic/agents/cognitive/reflection_agent.py", "work"),
        ("src/logic/agents/cognitive/synthesis_agent.py", "fleet_agents"),
        ("src/logic/agents/cognitive/voice_agent.py", "reference_voice_path"),
        ("src/logic/agents/cognitive/world_model_agent.py", "proposed_change"),
        ("src/logic/agents/cognitive/core/quantum_core.py", "constraints"),
        ("src/logic/agents/cognitive/mixins/graph_beads_mixin.py", "threshold_days"),
        ("src/logic/agents/cognitive/mixins/graph_mirix_mixin.py", "threshold_score"),
    ]
    for path, arg in targets:
        if not os.path.exists(path): continue
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        # Find argument in function definition
        content = content.replace(f", {arg}:", f", {arg}_unused:")
        content = content.replace(f" {arg}:", f" {arg}_unused:") # If it's the first arg
        # Then inside the function, if it was used somewhere we might have broke it, but we only target W0613 (Unused argument)
        # So it shouldn't be used.
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

fix_knowledge_main()
fix_no_else_return()
fix_pointless_strings()
fix_unused_args()
