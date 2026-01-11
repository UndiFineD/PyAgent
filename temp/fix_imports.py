import os
import re

def replace_in_files(directory, search_text, replace_text):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if search_text in content:
                    new_content = content.replace(search_text, replace_text)
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Updated: {path}")

# Fix context references
for target in ['c:/DEV/PyAgent/src', 'c:/DEV/PyAgent/tests']:
    replace_in_files(target, 'src.logic.context', 'src.logic.agents.cognitive.context')
    replace_in_files(target, 'src.logic.agents.data', 'src.logic.agents.intelligence')
    replace_in_files(target, 'src.logic.agents.specialized', 'src.logic.agents.intelligence')
    replace_in_files(target, 'src.logic.search', 'src.logic.agents.intelligence')
