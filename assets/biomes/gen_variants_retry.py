"""Retry the still-missing biome layers — sequential, patient backoff."""
import json, requests, time

TOKEN='a8343c8c-5eaf-45a7-9570-5f77dac08cad'
URL='https://api.pixellab.ai/mcp'
H={'Authorization':f'Bearer {TOKEN}','Content-Type':'application/json'}

with open(r'F:\Jogo\assets\biomes\variants.json') as f:
    LAYERS = {l['slug']: l['desc'] for l in json.load(f)['layers']}
with open(r'F:\Jogo\assets\biomes\variant_ids.json') as f:
    ids = json.load(f)

def call(args):
    payload={'jsonrpc':'2.0','method':'tools/call','params':{'name':'create_object','arguments':args},'id':1}
    try:
        r=requests.post(URL,headers=H,json=payload,timeout=90)
        for line in r.text.split('\n'):
            if line.startswith('data: '):
                return json.loads(line[6:])['result']['content'][0]['text']
    except Exception as e:
        return 'ERR'
    return ''

missing = [s for s, v in ids.items() if not v]
print(f'=== Retrying {len(missing)} missing layers ===', flush=True)
for slug in missing:
    desc = LAYERS[slug]
    got = None
    for attempt in range(8):
        txt = call({'description': desc, 'size': 256, 'directions': 1,
                    'view': 'side', 'object_view': 'sidescroller'})
        oid = None
        for ln in (txt or '').split('\n'):
            if ln.startswith('id:'):
                oid = ln.split(': ')[1].strip()
        if oid:
            got = oid
            break
        # rate-limited or transient — wait and retry
        time.sleep(attempt * 6 + 6)
    ids[slug] = got
    print(f'  {slug:22s} -> {got}', flush=True)
    # Save incrementally so partial progress survives a crash
    with open(r'F:\Jogo\assets\biomes\variant_ids.json','w') as f:
        json.dump(ids, f, indent=2)

done = sum(1 for v in ids.values() if v)
print(f'\n=== {done}/{len(ids)} total submitted ===', flush=True)
