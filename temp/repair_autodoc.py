#!/usr/bin/env python3
import sys
from pathlib import Path

# Add src to sys.path
src_path = Path("c:/DEV/PyAgent/src").resolve()
sys.path.append(str(src_path))
sys.path.append(str(src_path.parent))

from src.observability.reports.ReportGenerator import ReportGenerator




def run_repair():
    agent_dir = Path("c:/DEV/PyAgent/src").resolve()
    output_dir = Path("c:/DEV/PyAgent/docs/autodoc").resolve()

    print("Starting autodoc repair...")










    print(f"Source: {agent_dir}")
    print(f"Output: {output_dir}")

    # Ensure output dir exists




    output_dir.mkdir(parents=True, exist_ok=True)

    generator = ReportGenerator(agent_dir=agent_dir, output_dir=output_dir)
    results = generator.process_all_files()




    print("Autodoc repair completed.")
    print(f"Files Processed: {results.get('count', 0)}")
    print(f"Files Skipped: {results.get('skipped', 0)}")
    print(f"Errors: {results.get('errors', 0)}")




    # Generate the dashboard too
    dashboard = generator.generate_full_report()
    (output_dir / "AUTODOC_DASHBOARD.md").write_text(dashboard, encoding='utf-8')
    print(f"Dashboard generated at {output_dir / 'AUTODOC_DASHBOARD.md'}")






if __name__ == "__main__":
    run_repair()
