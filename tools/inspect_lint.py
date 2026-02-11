import json
p='lint_results.json'
with open(p,'r',encoding='utf-8') as f:
    d=json.load(f)
first=d[0]
print('keys:', list(first.keys()))
print('ruff present:', 'ruff' in first)
print('ruff type:', type(first['ruff']))
print('ruff exit_code repr:', repr(first['ruff'].get('exit_code')))
print('ruff stdout repr:', repr(first['ruff'].get('stdout')))
