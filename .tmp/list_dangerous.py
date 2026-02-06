import json, itertools
m=json.load(open('src/external_candidates/ingested/batch_refactor_map.json','r',encoding='utf-8'))
# consider these issue tokens as high-risk
dangerous_tokens = [
    'forbidden_call:exec','forbidden_call:eval','forbidden_call:compile',
    'forbidden_attr_call:system','forbidden_attr_call:Popen','forbidden_attr_call:popen','forbidden_attr_call:call',
    'forbidden_module_call:subprocess.Popen','forbidden_module_call:subprocess.run','forbidden_module_call:subprocess.call',
    'forbidden_module_call:subprocess.check_output','forbidden_module_call:subprocess.getoutput','forbidden_import:subprocess'
]

def is_dangerous(issues):
    if not issues:
        return False
    for it in issues:
        for tok in dangerous_tokens:
            if tok in it:
                return True
    return False

dangerous = [(k,v['issues']) for k,v in m.items() if v.get('status')=='unsafe' and is_dangerous(v.get('issues'))]
print('DANGEROUS COUNT:', len(dangerous))
print('\nSAMPLE (first 50):')
for k,issues in itertools.islice(dangerous,50):
    print(f"{k} -> {', '.join(issues) if issues else 'no issues listed'}")
# write full CSV
import csv
with open('.tmp/dangerous_skipped.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f)
    w.writerow(['path','issues'])
    for k,issues in dangerous:
        w.writerow([k,';'.join(issues) if issues else ''])
print('\nFull CSV: .tmp/dangerous_skipped.csv')
