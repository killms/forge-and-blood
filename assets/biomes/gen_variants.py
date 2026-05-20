"""Generate 40 biome layer variants via PixelLab create_object."""
import json, requests, time
from concurrent.futures import ThreadPoolExecutor, as_completed

TOKEN='a8343c8c-5eaf-45a7-9570-5f77dac08cad'
URL='https://api.pixellab.ai/mcp'
H={'Authorization':f'Bearer {TOKEN}','Content-Type':'application/json'}

with open(r'F:\Jogo\assets\biomes\variants.json') as f:
    LAYERS = json.load(f)['layers']

def call(name, args):
    payload={'jsonrpc':'2.0','method':'tools/call','params':{'name':name,'arguments':args},'id':1}
    for attempt in range(6):
        try:
            r=requests.post(URL,headers=H,json=payload,timeout=90)
            for line in r.text.split('\n'):
                if line.startswith('data: '):
                    return json.loads(line[6:])['result']['content'][0]['text']
        except Exception:
            pass
        time.sleep(attempt*5+3)
    return ''

def submit(layer):
    txt = call('create_object', {
        'description': layer['desc'], 'size': 256, 'directions': 1,
        'view': 'side', 'object_view': 'sidescroller'
    })
    for ln in (txt or '').split('\n'):
        if ln.startswith('id:'):
            return layer['slug'], ln.split(': ')[1].strip()
    # retry once on miss (rate-limit)
    time.sleep(8)
    txt = call('create_object', {
        'description': layer['desc'], 'size': 256, 'directions': 1,
        'view': 'side', 'object_view': 'sidescroller'
    })
    for ln in (txt or '').split('\n'):
        if ln.startswith('id:'):
            return layer['slug'], ln.split(': ')[1].strip()
    return layer['slug'], None

print(f'=== Submitting {len(LAYERS)} biome layers ===', flush=True)
ids = {}
with ThreadPoolExecutor(max_workers=8) as pool:
    futures = [pool.submit(submit, l) for l in LAYERS]
    for fut in as_completed(futures):
        slug, oid = fut.result()
        ids[slug] = oid
        print(f'  {slug:22s} -> {oid}', flush=True)

with open(r'F:\Jogo\assets\biomes\variant_ids.json','w') as f:
    json.dump(ids, f, indent=2)
done = sum(1 for v in ids.values() if v)
print(f'\n=== {done}/{len(LAYERS)} submitted. IDs saved. ===', flush=True)
