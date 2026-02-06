import os
import shutil
import subprocess

# specific_moves maps old_name -> new_name
MOVES = {
    # Validated from previous list and user request
    "architecturaldesign": "architectural_design",
    "attentionbuffer": "attention_buffer",
    "bayesianreasoning": "bayesian_reasoning",
    "cooperativecommunication": "cooperative_communication",
    "cplusplus": "c_plus_plus",
    "datascience": "data_science",
    "docinference": "doc_inference",
    "agentbar": "agent_bar",
    "anomalydetection": "anomaly_detection",
    "consensusconflict": "consensus_conflict",
    "empathyengine": "empathy_engine",
    "websecurityscanner": "web_security_scanner",
    "securityscanner": "security_scanner",
    "networkarchsearch": "network_arch_search",
    "hierarchicalmemory": "hierarchical_memory",
    "holographiccontext": "holographic_context",
    "interfleetidentity": "inter_fleet_identity", 
    "knowledgefusion": "knowledge_fusion",
    "latentreasoning": "latent_reasoning",
    "memoryconsolidation": "memory_consolidation",
    "metacognitivemonitor": "metacognitive_monitor",
    "multimodalcontext": "multimodal_context",
    "multimodalreasoning": "multimodal_reasoning",
    "neuralanchor": "neural_anchor",
    "neurosymbolic": "neuro_symbolic",
    "patternorchestrator": "pattern_orchestrator",
    "performanceprofiling": "performance_profiling",
    "personalitycore": "personality_core",
    "predictivescheduler": "predictive_scheduler",
    "privacyguard": "privacy_guard",
    "quantummemory": "quantum_memory",
    "quantumreasoner": "quantum_reasoner",
    "quantumscalingcoder": "quantum_scaling_coder",
    "quantumshardorchestrator": "quantum_shard_orchestrator",
    "realityanchor": "reality_anchor",
    "realitygrafting": "reality_grafting",
    "researchsynthesis": "research_synthesis",
    "resiliencemanager": "resilience_manager",
    "resourcecuration": "resource_curation",
    "resourceforecasting": "resource_forecasting",
    "resourcepredictor": "resource_predictor",
    "securityaudit": "security_audit",
    "securityguard": "security_guard",
    "selfarchiving": "self_archiving",
    "selfhealing": "self_healing",
    "selfimprovementorchestrator": "self_improvement_orchestrator",
    "selfoptimizer": "self_optimizer",
    "selfsearch": "self_search",
    "sharddeduplication": "shard_deduplication",
    "sqlcoder": "sql_coder",
    "sqlquery": "sql_query",
    "strategicplanning": "strategic_planning",
    "structuredorchestrator": "structured_orchestrator",
    "swarmdeployment": "swarm_deployment",
    "swarmdistillation": "swarm_distillation",
    "syntheticdata": "synthetic_data",
    "taskplanner": "task_planner",
    "techdebt": "tech_debt",
    "temporalpredictor": "temporal_predictor",
    "temporalshard": "temporal_shard",
    "toolevolution": "tool_evolution",
    "toolsynthesis": "tool_synthesis",
    "topologicalnavigator": "topological_navigator",
    "typesafety": "type_safety",
    "uiarchitect": "ui_architect",
    "voiceinteraction": "voice_interaction",
    "weightorchestrator": "weight_orchestrator",
    "worldmodel": "world_model",
    # Additional candidates found in data/agents
    "asynciothreadingcoder": "asyncio_threading_coder",
    "audioreasoning": "audio_reasoning",
    "byzantineconsensus": "byzantine_consensus",
    "changemonitoring": "change_monitoring",
    "cloudprovider": "cloud_provider",
    "codeformattingstandards": "code_formatting_standards",
    "codegenerator": "code_generator",
    "codequality": "code_quality",
    "codereviewer": "code_reviewer",
    "codetranslation": "code_translation",
    "cognitivesuper": "cognitive_super",
    "complianceaudit": "compliance_audit",
    "coreexpansion": "core_expansion",
    "credentialextraction": "credential_extraction",
    "dataprivacyguard": "data_privacy_guard",
    "dependencygraph": "dependency_graph",
    "docgen": "doc_gen",
    "documentationindexer": "documentation_indexer",
    "dynamicdecomposer": "dynamic_decomposer",
    "entropyguard": "entropy_guard",
    "eternalaudit": "eternal_audit",
    "ethicsguardrail": "ethics_guardrail",
    "eventcorrelation": "event_correlation",
    "evolutionaryprompt": "evolutionary_prompt",
    "experimentorchestrator": "experiment_orchestrator",
    "externalairecorder": "external_ai_recorder",
    "featurestore": "feature_store",
    "fleetdeployer": "fleet_deployer",
    "fleeteconomy": "fleet_economy",
    "genetichardening": "genetic_hardening",
    "graphmemory": "graph_memory",
    "graphrelational": "graph_relational",
    "idiomextractor": "idiom_extractor",
    "imagegeneration": "image_generation",
    "immunesystem": "immune_system",
    "infrastructuremanager": "infrastructure_manager",
    "infrastructurerepair": "infrastructure_repair",
    "legacywrapper": "legacy_wrapper",
    "legalaudit": "legal_audit",
    "memorag": "memo_rag",
    "modeloptimizer": "model_optimizer",
    "morphologicalevolution": "morphological_evolution",
    "ollamaconnector": "ollama_connector",
    "qualitygate": "quality_gate",
    "remoteproxy": "remote_proxy",
    "rewardmodel": "reward_model",
    "rlpriority": "rl_priority",
    "routermodel": "router_model",
    "spectool": "spec_tool",
    "pullrequest": "pull_request",
    # Clean up ugly auto-generated snake case
    "a_rc_hi_te_ct_ur_al_d_es_ig_n": "architectural_design",
    "c_p_lu_s_p_lu_s": "c_plus_plus",
    "s_ec_ur_it_ys_ca_nn_er": "security_scanner",
}

ROOT = os.getcwd()
AGENTS_DIR = os.path.join(ROOT, "data", "agents")

def consolidate_dirs():
    print(f"Scanning {AGENTS_DIR}...")
    if not os.path.exists(AGENTS_DIR):
        print("Agents dir not found")
        return

    # Sort checks to do longest matches first if we were matching substrings, 
    # but here we match exact directory names.
    
    for old, new in MOVES.items():
        old_path = os.path.join(AGENTS_DIR, old)
        new_path = os.path.join(AGENTS_DIR, new)
        
        if os.path.exists(old_path) and old != new:
            print(f"Processing {old} -> {new}")
            if not os.path.exists(new_path):
                os.makedirs(new_path)
            
            # recursively move contents
            for root, dirs, files in os.walk(old_path):
                # We need relative path from old_path
                rel_path = os.path.relpath(root, old_path)
                dest_root = os.path.join(new_path, rel_path)
                if not os.path.exists(dest_root):
                    os.makedirs(dest_root)
                
                for file in files:
                    src_file = os.path.join(root, file)
                    dst_file = os.path.join(dest_root, file)
                    
                    if os.path.exists(dst_file):
                         print(f"  Target {dst_file} exists. Skipping/Overwriting?")
                         # For Git compliance, we should use git mv if source is tracked
                    
                    # Try git mv first
                    # print(f"  Moving {src_file} -> {dst_file}")
                    ret = subprocess.call(["git", "mv", "-k", src_file, dst_file], shell=True, stderr=subprocess.DEVNULL)
                    if ret != 0:
                        # Fallback to shutil move (for untracked files)
                        try:
                            shutil.move(src_file, dst_file)
                            # Add to git if it was untracked? User implies "agents" so maybe important data.
                            # But data/ might be ignored. Let's strictly move.
                        except Exception as e:
                            print(f"    Error moving {src_file}: {e}")

            # Try to remove the old directory structure
            # subprocess.call(["rm", "-rf", old_path], shell=True) # Dangerous
            try:
                shutil.rmtree(old_path)
                print(f"Removed {old_path}")
            except Exception as e:
                print(f"Could not remove {old_path}: {e}")

def replace_in_files():
    print("Replacing strings in src/ and tests/...")
    extensions = ('.py', '.md', '.json', '.yaml', '.txt', '.toml')
    
    # Pre-compute replacements
    replacements = [(k, v) for k, v in MOVES.items()]

    for root, dirs, files in os.walk(ROOT):
        # exclusions
        if ".git" in root or ".venv" in root or "__pycache__" in root:
            continue
            
        for file in files:
            if not file.endswith(extensions):
                continue
                
            path = os.path.join(root, file)
            # Skip this script itself
            if path == os.path.abspath(__file__):
                continue

            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content = content
                changed = False
                
                # Careful replacement: 
                # 1. replace "data/agents/<old>" -> "data/agents/<new>"
                # 2. replace "data\\agents\\<old>" -> "data\\agents\\<new>"
                
                for old_key, new_val in replacements:
                    # Unix-style paths
                    pat1 = f"data/agents/{old_key}"
                    rep1 = f"data/agents/{new_val}"
                    if pat1 in new_content:
                        new_content = new_content.replace(pat1, rep1)
                        changed = True
                    
                    # Windows-style paths (escaped in strings)
                    pat2 = f"data\\\\agents\\\\{old_key}"
                    rep2 = f"data\\\\agents\\\\{new_val}"
                    if pat2 in new_content:
                        new_content = new_content.replace(pat2, rep2)
                        changed = True

                    # Plain Windows paths (if read raw)
                    pat3 = f"data\\agents\\{old_key}"
                    rep3 = f"data\\agents\\{new_val}"
                    if pat3 in new_content:
                        new_content = new_content.replace(pat3, rep3)
                        changed = True
                
                if changed:
                    print(f"Updating references in {path}")
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
            except Exception as e:
                # print(f"Skipping {path}: {e}")
                pass

if __name__ == "__main__":
    consolidate_dirs()
    replace_in_files()
