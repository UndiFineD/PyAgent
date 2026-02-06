import json, itertools
m=json.load(open('src/external_candidates/ingested/batch_refactor_map.json','r',encoding='utf-8'))
unsafe=[(k, v.get('issues')) for k,v in m.items() if v.get('status')=='unsafe']
print('SKIPPED COUNT:', len(unsafe))
print('\nSAMPLE (first 30):')
for k,issues in itertools.islice(unsafe,30):
    print(f"{k} -> {', '.join(issues) if issues else 'no issues listed'}")
