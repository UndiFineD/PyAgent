import os

path = r'c:\DEV\PyAgent\src\core\base\logic\core'
for filename in os.listdir(path):
    if filename.endswith('.py'):
        filepath = os.path.join(path, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Trim all trailing whitespace and newlines, then add exactly one newline
        new_content = content.rstrip() + '\n'
        
        with open(filepath, 'w', encoding='utf-8', newline='\r\n') as f:
            f.write(new_content)
