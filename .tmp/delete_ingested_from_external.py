#!/usr/bin/env python3
import os,json,shutil,datetime,csv
root = os.getcwd()
map_fp = os.path.join('src','external_candidates','ingested','batch_refactor_map.json')
if not os.path.exists(map_fp):
    print('mapping not found', map_fp); raise SystemExit(1)
with open(map_fp,'r',encoding='utf-8') as f:
    m=json.load(f)
# collect copied entries
copied = [k for k,v in m.items() if v.get('status')=='copied']
if not copied:
    print('no copied entries found'); raise SystemExit(0)
# normalize keys
keys_norm = [k.replace('\\','/').lstrip('./').lstrip('/') for k in copied]
# archive
ts = datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
archive_root = os.path.join('.tmp','deleted_ingested_originals_archive', ts)
os.makedirs(archive_root, exist_ok=True)
log = []
# walk .external only
for dirpath,dirnames,filenames in os.walk(os.path.join(root, '.external')):
    rel_dir = os.path.relpath(dirpath, root).replace('\\','/')
    for fn in filenames:
        rel_path = os.path.join(rel_dir, fn).replace('\\','/')
        for key in keys_norm:
            if rel_path.lower().endswith(key.lower()):
                srcp = os.path.join(root, rel_path)
                destp = os.path.join(archive_root, rel_path)
                os.makedirs(os.path.dirname(destp), exist_ok=True)
                try:
                    shutil.move(srcp, destp)
                    log.append((rel_path, destp))
                    print('MOVED', rel_path)
                except Exception as e:
                    print('ERROR', rel_path, e)
# write csv log
out = os.path.join('.tmp','deleted_ingested_originals.csv')
with open(out,'w',encoding='utf-8',newline='') as f:
    w = csv.writer(f)
    w.writerow(['rel_path','moved_to'])
    for a,b in log:
        w.writerow([a,b])
print('\nArchive root:', archive_root)
print('Moved count:', len(log))
print('CSV log:', out)
