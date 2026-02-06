#!/usr/bin/env python3
import csv,collections,sys
fn = '.tmp/dangerous_skipped.csv'
rows = []
with open(fn,'r',encoding='utf-8',newline='') as f:
    r = csv.reader(f)
    header = next(r, None)
    for row in r:
        if not row: continue
        path = row[0]
        issues = (row[1] or '').split(';') if len(row)>1 else []
        issues = [i.strip() for i in issues if i.strip()]
        rows.append((path,issues))

# token counts
counter = collections.Counter()
for _,issues in rows:
    for it in issues:
        counter[it]+=1

# map tokens to risk levels
high = set([
    'forbidden_call:exec','forbidden_call:eval','forbidden_call:compile',
    'forbidden_attr_call:system','forbidden_attr_call:Popen','forbidden_attr_call:popen','forbidden_attr_call:call',
    'forbidden_module_call:subprocess.Popen','forbidden_module_call:subprocess.run','forbidden_module_call:subprocess.call',
    'forbidden_module_call:subprocess.check_output','forbidden_module_call:subprocess.getoutput','forbidden_import:subprocess'
])
medium = set([
    'forbidden_module_call:subprocess.check_call','forbidden_module_call:subprocess.check_output','forbidden_attr_call:check_output'
])

# classify rows
classified = {'high':[], 'medium':[], 'low':[]}
for path,issues in rows:
    if any(any(tok in it for tok in high) for it in issues):
        classified['high'].append((path,issues))
    elif any(any(tok in it for tok in medium) for it in issues):
        classified['medium'].append((path,issues))
    else:
        classified['low'].append((path,issues))

print('TOTAL DANGEROUS ROWS:', len(rows))
print('\nTop issue tokens:')
for tok,count in counter.most_common(20):
    print(f' - {tok}: {count}')

print('\nCounts by risk level:')
for k in ('high','medium','low'):
    print(f' - {k}: {len(classified[k])}')

print('\nSample high-risk files (first 40):')
for path,issues in classified['high'][:40]:
    print(' -', path, '->', ', '.join(issues))

# write grouped CSV by issue type
out = '.tmp/dangerous_summary.csv'
with open(out,'w',encoding='utf-8',newline='') as f:
    w = csv.writer(f)
    w.writerow(['risk','path','issues'])
    for r in ('high','medium','low'):
        for path,issues in classified[r]:
            w.writerow([r,path,';'.join(issues)])
print('\nSummary CSV written to .tmp/dangerous_summary.csv')
