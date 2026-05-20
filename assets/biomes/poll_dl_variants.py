"""Poll the 40 biome objects, then download each completed PNG."""
import json, requests, time, os

TOKEN='a8343c8c-5eaf-45a7-9570-5f77dac08cad'
URL='https://api.pixellab.ai/mcp'
H={'Authorization':f'Bearer {TOKEN}','Content-Type':'application/json'}
DST=r'F:\Jogo\assets\biomes'

with open(os.path.join(DST,'variant_ids.json')) as f:
    ids = json.load(f)

def get_obj(oid):
    payload={'jsonrpc':'2.0','method':'tools/call','params':{'name':'get_object','arguments':{'object_id':oid,'include_preview':False}},'id':1}
    try:
        r=requests.post(URL,headers=H,json=payload,timeout=60)
        for line in r.text.split('\n'):
            if line.startswith('data: '):
                return json.loads(line[6:])['result']['content'][0]['text']
    except Exception:
        pass
    return ''

# Poll until all completed
print('=== Polling 40 biome objects ===', flush=True)
for attempt in range(50):
    pending = []
    for slug, oid in ids.items():
        if not oid: continue
        t = get_obj(oid)
        if 'status: completed' not in t:
            pending.append(slug)
    ts = time.strftime('%H:%M:%S')
    if not pending:
        print(f'[{ts}] ALL 40 COMPLETED', flush=True)
        break
    print(f'[{ts}] attempt {attempt+1}: {len(pending)} pending', flush=True)
    time.sleep(25)

# Download each
print('\n=== Downloading PNGs ===', flush=True)
ok = 0
for slug, oid in ids.items():
    if not oid:
        print(f'  {slug}: NO ID'); continue
    t = get_obj(oid)
    url = None
    for ln in t.split('\n'):
        if 'unknown:' in ln and 'http' in ln:
            url = ln.split(': ', 1)[1].strip()
            break
    if not url:
        print(f'  {slug}: no URL'); continue
    try:
        r = requests.get(url, timeout=60)
        with open(os.path.join(DST, slug + '.png'), 'wb') as f:
            f.write(r.content)
        ok += 1
        print(f'  {slug}.png ({len(r.content)} b)', flush=True)
    except Exception as e:
        print(f'  {slug}: download fail {e}', flush=True)

print(f'\n=== {ok}/40 downloaded ===', flush=True)
