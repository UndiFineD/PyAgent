import os

AGENTS_DIR = os.path.join(os.getcwd(), "data", "agents")
EXCLUDE = {
    "dashboard", "firewall", "javascript", "kubernetes", "management", 
    "monitoring", "networking", "orchestrator", "performance", "powershell",
    "production", "profiling", "provisioning", "reasoning", "reflection",
    "regression", "resilience", "scheduler", "scripting", "security",
    "simulation", "strategist", "supervisor", "synthesis", "telemetry",
    "terraform", "visualizer", "workload", "workspace", "architect", "benchmark", 
    "compliance", "middleware", "classifier", "controller", "department"
}

def find_candidates():
    if not os.path.exists(AGENTS_DIR):
        print(f"Agents dir not found: {AGENTS_DIR}")
        return

    print(f"Scanning {AGENTS_DIR}")
    for name in os.listdir(AGENTS_DIR):
        path = os.path.join(AGENTS_DIR, name)
        if not os.path.isdir(path):
            continue
            
        # Heuristic: no underscores, length > 8, not in exclude list
        if "_" not in name and len(name) > 8 and name not in EXCLUDE:
            print(f"Candidate: {name}")

if __name__ == "__main__":
    find_candidates()
