#!/usr/bin/env python3
import csv,os,shutil,datetime,fnmatch
root = os.getcwd()
csvfp = os.path.join('.tmp','dangerous_summary.csv')
if not os.path.exists(csvfp):
    print('dangerous_summary.csv not found at', csvfp); raise SystemExit(1)

with open(csvfp,'r',encoding='utf-8') as f:
    lines = f.read().splitlines()
if not lines:
    print('empty csv'); raise SystemExit(1)
# parse CSV naive (first header line may be risk,path,issues)
rows = []
for i,l in enumerate(lines[1:], start=2):
    if not l.strip(): continue
    parts = l.split(',',2)
    if len(parts)<2: continue
    path = parts[1].strip()
    rows.append(path)

# normalize windows backslashes
rows_norm = [p.replace('\\','/').lstrip('./').lstrip('/') for p in rows]
# build archive dir
ts = datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
archive_root = os.path.join('.tmp','deleted_dangerous_archive', ts)
os.makedirs(archive_root, exist_ok=True)
log = []
# walk workspace and match
for dirpath,dirnames,filenames in os.walk(root):
    # skip .git and .venv and .tmp archive dir itself
    if any(x in dirpath for x in ['\\.git', '\\.venv', '.tmp\\deleted_dangerous_archive']):
        continue
    rel_dir = os.path.relpath(dirpath, root).replace('\\','/')
    for fn in filenames:
        rel_path = os.path.join(rel_dir, fn) if rel_dir!='.' else fn
        rel_path_norm = rel_path.replace('\\','/')
        for target in rows_norm:
            # match iff endswith target (case-insensitive on Windows)
            try:
                if os.name=='nt':
                    if rel_path_norm.lower().endswith(target.lower()):
                        srcp = os.path.join(root, rel_path)
                        destp = os.path.join(archive_root, rel_path_norm)
                        os.makedirs(os.path.dirname(destp), exist_ok=True)
                        shutil.move(srcp, destp)
                        log.append((rel_path_norm, destp))
                        print('MOVED', rel_path_norm)
                else:
                    if rel_path_norm.endswith(target):
                        srcp = os.path.join(root, rel_path)
                        destp = os.path.join(archive_root, rel_path_norm)
                        os.makedirs(os.path.dirname(destp), exist_ok=True)
                        shutil.move(srcp, destp)
                        log.append((rel_path_norm, destp))
                        print('MOVED', rel_path_norm)
            except Exception as e:
                print('ERROR moving', rel_path_norm, e)

# write CSV log
out = os.path.join('.tmp','deleted_workspace_dangerous.csv')
with open(out,'w',encoding='utf-8',newline='') as f:
    import csv
    w = csv.writer(f)
    w.writerow(['rel_path','moved_to'])
    for a,b in log:
        w.writerow([a,b])

print('\nArchive root:', archive_root)
print('Deleted count:', len(log))
print('CSV log:', out)
