import io
path='src/core/base/lifecycle/base_agent.py'
with open(path,'r', encoding='utf-8') as f:
    lines=f.readlines()
line=lines[42]
print('LINE:',repr(line))
print('ORDS:', [ord(c) for c in line])
