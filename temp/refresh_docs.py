import logging
import sys
import os
os.environ["PYTHONPATH"] = "."
from src.observability.reports.ReportGenerator import ReportGenerator
from pathlib import Path

logging.basicConfig(level=logging.INFO, stream=sys.stdout, format="%(levelname)s: %(message)s")

def main():
    agent_dir = Path("src")
    output_dir = Path("docs/autodoc")
    
    print(f"Refreshing autodoc: {agent_dir} -> {output_dir}")
    generator = ReportGenerator(agent_dir=agent_dir, output_dir=output_dir)
    results = generator.process_all_files()
    print(f"\nResults: {results}")

if __name__ == "__main__":
    main()

