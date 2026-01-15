import re
import os

ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
log_path = r"c:\DEV\PyAgent\docs\work\flake8.txt"
clean_path = r"c:\DEV\PyAgent\docs\work\flake8_clean.txt"

if os.path.exists(log_path):
    with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    clean_content = ansi_escape.sub('', content)
    
    with open(clean_path, 'w', encoding='utf-8') as f:
        f.write(clean_content)
    print(f"Cleaned log saved to {clean_path}")
else:
    print("Log not found.")
