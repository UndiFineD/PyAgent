#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Licensed under the Apache License, Version 2.0 (the "License");

import asyncio
import json
from pathlib import Path
from src.logic.agents.analysis.analyst_agent import AnalystAgent
from src.core.base.common.models.communication_models import CascadeContext

async def main():
    print("🚀 Starting External Analyst Loop...")
    
    # Initialize the Analyst Agent
    agent = AnalystAgent(name="GlobalAnalyst")
    await agent.setup()
    
    # Target directory
    target = Path("src/external_candidates")
    
    # Create context
    context = CascadeContext(task_id="analyst_cycle_001", priority=1)
    
    # Run analysis
    print(f"🔍 Analyzing {target}...")
    results = await agent.run_analysis(str(target), context)
    
    # Output results
    print("\n📊 Analysis Results:")
    print(json.dumps(results, indent=2))
    
    # Save report
    report_path = Path("data/research/external_analysis_report.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n✅ Report saved to {report_path}")

if __name__ == "__main__":
    asyncio.run(main())
