"""Script to clean up and deduplicate entries in the IMPROVEMENT_RESEARCH.md document."""

import os

file_path = r"c:\DEV\PyAgent\docs\IMPROVEMENT_RESEARCH.md"
if not os.path.exists(file_path):
    print("File not found")
    exit(1)

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

header = "## 🚀 Recent Autonomous Findings"
if header in content:
    parts = content.split(header)
    base_info = parts[0]
    findings_area = parts[1]
    
    # We want to keep only the LAST "Latest Autonomous Scan" block and the LAST "AI Lessons" block if they exist.
    # Or just wipe it and keep a fresh summary.
    
    # Let's find the last "Latest Autonomous Scan" block
    scan_blocks = findings_area.split("### Latest Autonomous Scan")
    last_scan = ""
    if len(scan_blocks) > 1:
        last_scan = "### Latest Autonomous Scan" + scan_blocks[-1]
    
    # Find the last "AI Lessons" block
    lessons_blocks = findings_area.split("### 🧠 AI Lessons")
    last_lessons = ""
    if len(lessons_blocks) > 1:
        last_lessons = "### 🧠 AI Lessons" + lessons_blocks[-1]
    
    new_findings = "\n\n" + last_scan + "\n\n" + last_lessons
    
    new_content = base_info + header + new_findings
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Deduplicated IMPROVEMENT_RESEARCH.md")
else:
    print("Header not found")
