import json
p='.secrets.baseline'
with open(p,'r',encoding='utf-8') as f:
    data=json.load(f)
res=data.get('results',{})
paths=set()
for k in res.keys():
    paths.add(k.replace('\\','/'))
out='secrets_paths.txt'
with open(out,'w',encoding='utf-8') as o:
    for p in sorted(paths):
        o.write(p+'\n')
print('Wrote',out,'entries:',len(paths))
print('\nSample:')
for i,p in enumerate(sorted(paths)[:20]):
    print(p)
