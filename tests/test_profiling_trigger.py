
import os
import sys

# Add src to path
sys.path.insert(0, os.getcwd())

from src.infrastructure.swarm.orchestration.intel.mixins.profiling_analysis_mixin import ProfilingAnalysisMixin
from src.infrastructure.swarm.orchestration.intel.self_improvement_analysis import SelfImprovementAnalysis

class MockAnalysis(SelfImprovementAnalysis, ProfilingAnalysisMixin):
    def __init__(self):
        # We don't call super().__init__ because it might trigger other things
        self.profiling_agent = None

def check_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    findings = []
    # Mixin will add findings if it triggers
    MockAnalysis().add_profiling_findings(findings, path, os.path.relpath(path), content)

    if findings:
        loop_count = content.count("for ") + content.count("while ")
        print(f"File: {path}")
        print(f"Loops: {loop_count}")
        for f in findings:
            print(f"  - {f['message']}")
    else:
        print(f"File: {path} - OK")

files_to_check = [
    r'src/infrastructure/engine/loading/expert_load_balancer.py',
    r'src/infrastructure/storage/cache/kv_cache_manager.py',
    r'src/infrastructure/engine/loading/sharded_state_loader.py',
    r'src/infrastructure/engine/loading/weight_loader.py',
    r'src/core/base/common/multimodal_logic.py'
]

for f in files_to_check:
    if os.path.exists(f):
        check_file(f)
    else:
        print(f"File not found: {f}")
