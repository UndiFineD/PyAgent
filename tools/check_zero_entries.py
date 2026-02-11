from pathlib import Path
text = Path('lint_results.json').read_text(encoding='utf-8')
count = text.count('"exit_code": 0')
print('count_exit_code_0=', count)
# Print small context samples if any
if count:
    idx = text.find('"exit_code": 0')
    start = max(0, idx-200)
    end = min(len(text), idx+200)
    print(text[start:end])
else:
    print('none found')
