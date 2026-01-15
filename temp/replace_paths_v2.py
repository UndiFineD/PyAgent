
import os

files = [
    r'c:\DEV\PyAgent\tests\unit\logic\test_coder_UNIT.py',
    r'c:\DEV\PyAgent\tests\unit\logic\test_coder_CORE_UNIT.py'
]

old_str = '"src/logic/agents/cognitive/context/utils/CodeGenerator.py"'
new_str = '"src/logic/agents/development/CoderAgent.py"'

for file_path in files:
    if os.path.exists(file_path):
        print(f"Processing {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        new_content = content.replace(old_str, new_str)

        if content != new_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {file_path}")
        else:
            print(f"No changes for {file_path}")
    else:
        print(f"File not found: {file_path}")
