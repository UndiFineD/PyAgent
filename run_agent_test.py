#!/usr/bin/env python3
"""Test script to run agent on src directory"""
import logging

from src.agent import Agent

# Set up logging before importing agent
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Initialize agent for src directory only, max 3 files, 1 loop
print("Starting agent run on src/ directory...")
print("-" * 60)

agent = Agent(
    repo_root='src',
    loop=1,
    max_files=3,
    dry_run=False,
    no_git=True  # Don't commit to git
)

# Get files to process
files = agent.find_code_files()
print(f"Found {len(files)} Python files in src/")
print("Processing first 3 files:")
for f in files[:3]:
    print(f"  - {f.name}")

print("\nRunning agent...")
print("-" * 60)
agent.run()
print("-" * 60)
print("Agent run completed!")

# Print summary
print("\nMetrics:")
print(f"  Processed: {agent.metrics.get('processed_files', 0)}")
print(f"  Improved: {agent.metrics.get('improved_files', 0)}")
print(f"  Errors: {agent.metrics.get('errors', 0)}")
