path='src/core/base/lifecycle/base_agent.py'
with open(path,'rb') as f:
    lines=f.readlines()
for idx in range(38,46):
    print(idx+1, lines[idx])
