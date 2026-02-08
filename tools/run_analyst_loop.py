#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

import asyncio
import os
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
