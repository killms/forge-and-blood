"""Poll all 20 biome layers until ready, then download PNGs."""
import json, requests, time, os
from urllib.request import urlretrieve

TOKEN = 'a8343c8c-5eaf-45a7-9570-5f77dac08cad'
URL = 'https://api.pixellab.ai/mcp'
HEADERS = {'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'}
DST = r'F:\Jogo\assets\biomes'

with open(os.path.join(DST, 'biome_ids.json')) as f:
    BIOMES = json.load(f)

# Flat list of (slug, id)
ALL = []
for biome, layers in BIOMES.items():
    for layer, oid in layers.items():
        ALL.append((f'{biome}-{layer}', oid))

def call(name, args):
    payload = {'jsonrpc':'2.0','method':'tools/call','params':{'name':name,'arguments':args},'id':1}
    r = requests.post(URL, headers=HEADERS, json=payload, timeout=60)
    for line in r.text.split('\n'):
        if line.startswith('data: '):
            return json.loads(line[6:])['result']['content'][0]['text']
    return ''

def get_obj(oid):
    return call('get_object', {'object_id': oid, 'include_preview': False})

print(f'=== Polling {len(ALL)} biome layers ===', flush=True)
for attempt in range(40):
    pending = []
    urls = {}
    for slug, oid in ALL:
        t = get_obj(oid)
        first = t.split('\n')[0] if t else ''
        if 'completed' in first:
            for ln in t.split('\n'):
                if 'unknown:' in ln and 'http' in ln:
                    urls[slug] = ln.strip().split(': ',1)[1]
                    break
        else:
            pending.append((slug, first))
    ts = time.strftime('%H:%M:%S')
    print(f'[{ts}] attempt {attempt+1}: {len(urls)}/{len(ALL)} done, {len(pending)} pending', flush=True)
    if pending and len(pending) <= 8:
        for s, st in pending:
            print(f'  {s}: {st}', flush=True)
    if not pending:
        print('*** ALL DONE ***', flush=True)
        break
    time.sleep(25)

print(f'\n=== Downloading {len(urls)} PNGs ===', flush=True)
for slug, url in urls.items():
    path = os.path.join(DST, f'{slug}.png')
    try:
        urlretrieve(url, path)
        sz = os.path.getsize(path)
        print(f'  {slug}.png: {sz} bytes', flush=True)
    except Exception as e:
        print(f'  {slug}.png: ERR {e}', flush=True)

print('\nAll biome layers downloaded.', flush=True)
