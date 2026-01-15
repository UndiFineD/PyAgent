import re
s = "\x1b[m43"
print(f"Original: {repr(s)}")
ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
clean = ansi_escape.sub('', s)
print(f"Clean: {repr(clean)}")
