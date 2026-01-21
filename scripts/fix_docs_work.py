import os

files = [
    "FLEET_AUTO_DOC.md",
    "IMPROVEMENT_RESEARCH.md",
    "OPTIONAL_TOOLS.md",
    "PHASE_1_RUST_PROGRESS.md",
    "PHASE_2_SECURITY_HARDENING.md",
    "PHASE_3_DEEP_OPTIMIZATION.md",
    "PROGRESS_DASHBOARD.md",
    "PROGRESS_REPORT.md",
    "ROADMAP_PHASES.md",
    "RUST_Ready.md"
]

root = r"c:\DEV\PyAgent\docs\work"

for f in files:
    old = os.path.join(root, f)
    new = os.path.join(root, f.lower())
    if os.path.exists(old):
        temp = old + ".tmp"
        os.rename(old, temp)
        os.rename(temp, new)
        print(f"Renamed {f} to {f.lower()}")
