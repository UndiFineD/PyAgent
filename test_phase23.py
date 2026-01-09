import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / "src"))

from classes.fleet.FleetManager import FleetManager

def test_phase23():
    print("--- Phase 23 Verification: NAS & Core Expansion ---")
    workspace_root = Path(__file__).parent
    fleet = FleetManager(str(workspace_root))
    
    # 1. Test NAS Agent
    print("\n[1/2] Testing Neural Architecture Search...")
    task = "High-speed tensor processing for financial sentiment"
    arch = fleet.nas.search_optimal_architecture(task)
    
    if "architecture_type" in arch:
        print(f"✅ NAS suggested: {arch['architecture_type']} with rank {arch.get('rank')}")
    else:
        print("❌ NAS search failed.")

    # 2. Test Core Expansion Agent
    print("\n[2/2] Testing Core Expansion (Environment Audit)...")
    env = fleet.core_expansion.audit_environment()
    
    if len(env) > 0:
        print(f"✅ Environment audit successful. Found {len(env)} packages.")
        # Check for a common package
        has_requests = any("requests" in pkg.lower() for pkg in env)
        if has_requests:
            print("   (Confirmed presence of 'requests')")
    else:
        print("❌ Environment audit returned no packages.")

if __name__ == "__main__":
    test_phase23()
