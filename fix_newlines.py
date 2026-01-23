import re

file_path = r"c:\DEV\PyAgent\src\core\base\lifecycle\base_agent.py"
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Restore newlines before hash comments
content = re.sub(r'([^ \n])#', r'\1\n#', content)
# Restore newlines before docstrings
content = re.sub(r'([^ \n])"""', r'\1\n"""', content)
# Restore newlines before from/import
content = re.sub(r'([^ \n])from ', r'\1\nfrom ', content)
content = re.sub(r'([^ \n])import ', r'\1\nimport ', content)
# Restore newlines before class/def
content = re.sub(r'([^ \n])class ', r'\1\nclass ', content)
content = re.sub(r'([^ \n])    def ', r'\1\n    def ', content)
content = re.sub(r'([^ \n])    @', r'\1\n    @', content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
