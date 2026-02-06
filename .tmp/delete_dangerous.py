#!/usr/bin/env python3
import json,os,sys,datetime,csv
root = os.getcwd()
map_fp = os.path.join('src','external_candidates','ingested','batch_refactor_map.json')
if not os.path.exists(map_fp):
    print('Mapping file not found:', map_fp); sys.exit(1)
with open(map_fp,'r',encoding='utf-8') as f:
    m = json.load(f)

# tokens considered dangerous
dangerous_tokens = [
    'forbidden_call:exec','forbidden_call:eval','forbidden_call:compile',
    'forbidden_attr_call:system','forbidden_attr_call:Popen','forbidden_attr_call:popen','forbidden_attr_call:call',
    'forbidden_module_call:subprocess.Popen','forbidden_module_call:subprocess.run','forbidden_module_call:subprocess.call',
    'forbidden_module_call:subprocess.check_output','forbidden_module_call:subprocess.getoutput','forbidden_import:subprocess','forbidden_importfrom:subprocess'
]

deleted = []
for src,info in list(m.items()):
    status = info.get('status')
    issues = info.get('issues') or []
    if status=='copied' and issues:
        # if any dangerous token matches any issue substring
        if any(any(tok in it for tok in dangerous_tokens) for it in issues):
            dest = info.get('dest')
            if dest:
                # resolve dest relative to repo root
                dest_path = os.path.normpath(os.path.join(root, dest))
                if os.path.exists(dest_path):
                    try:
                        os.remove(dest_path)
                        info['status']='deleted'
                        info['deleted_at']=datetime.datetime.utcnow().isoformat()+'Z'
                        info['deleted_reason']='dangerous_tokens'
                        deleted.append((src,dest,issues))
                        print('DELETED', dest_path)
                    except Exception as e:
                        print('FAILED to delete', dest_path, str(e))
                else:
                    # already absent
                    info['status']='missing'
                    info['deleted_reason']='dest_missing'
                    print('MISSING', dest_path)
            else:
                print('NO dest for', src)

# write updated mapping backup
bak = map_fp + '.bak'
with open(bak,'w',encoding='utf-8') as f:
    json.dump(m,f,indent=2,ensure_ascii=False)
with open(map_fp,'w',encoding='utf-8') as f:
    json.dump(m,f,indent=2,ensure_ascii=False)

# write CSV log
out = '.tmp/deleted_dangerous.csv'
os.makedirs('.tmp', exist_ok=True)
with open(out,'w',encoding='utf-8',newline='') as f:
    w = csv.writer(f)
    w.writerow(['src','dest','issues'])
    for src,dest,issues in deleted:
        w.writerow([src,dest,';'.join(issues)])

print('\nSUMMARY:')
print(' - mapping:', map_fp)
print(' - backup:', bak)
print(' - deleted count:', len(deleted))
print(' - csv log:', out)
