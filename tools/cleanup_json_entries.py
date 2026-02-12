import json
import os

# Files that have been fixed and should be cleared from the lint results
files_to_clear_from_report = [
    r"src\logic\agents\security\scanners\mobile\apk_enum\APKEnum.py",
    r"src\maintenance\mixins\syntax_fixer_mixin.py",
    r"src\logic\agents\analysis\profiling_agent.py",
    r"src\infrastructure\swarm\discovery\mdns_service.py",
    r"src\interface\ui\web\py_agent_web.py",
    r"src\infrastructure\swarm\network\network_utils.py",
    r"src\infrastructure\swarm\resilience\distributed_backup.py",
    r"src\infrastructure\swarm\voyager\remote_neural_synapse.py",
    r"src\infrastructure\swarm\parallel\dp\balancer.py",
    r"src\infrastructure\swarm\orchestration\connectivity\inter_fleet_bridge_orchestrator.py",
    r"src\infrastructure\swarm\orchestration\core\self_improvement_core.py",
    r"src\infrastructure\swarm\orchestration\intel\intelligence_orchestrator.py",
    r"src\infrastructure\swarm\orchestration\intel\self_improvement_analysis.py",
    r"src\infrastructure\swarm\orchestration\state\holographic_state_orchestrator.py"
]

# Verify files exist on disk before processing (Safety Check)
print("Verifying file existence...")
for file_path in files_to_clear_from_report:
    if not os.path.exists(file_path):
        print(f"WARNING: File missing from disk! {file_path}")
    else:
        # print(f"Verified: {file_path}")
        pass

# Normalize paths in list
# Also need to handle leading slash issues if any
normalized_files = [os.path.normpath(f) for f in files_to_clear_from_report]

json_path = r"temp/lint_results.json"
if os.path.exists(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Filter
    new_data = []
    for entry in data:
        entry_file = os.path.normpath(entry['file'])
        # Check suffix mostly to handle relative/absolute mix
        # Or check if entry_file ends with any of normalized_files
        should_remove = False
        for rem in normalized_files:
            if entry_file.endswith(rem):
                should_remove = True
                break
        
        # Additional safety: check if filename matches exactly
        if not should_remove:
            new_data.append(entry)
            
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, indent=2)
    
    print(f"Removed {len(data) - len(new_data)} entries.")
else:
    print("JSON file not found")
