"""Generate 17 item icons via PixelLab create_object — submit, poll, download."""
import json, requests, time, os

TOKEN='a8343c8c-5eaf-45a7-9570-5f77dac08cad'
URL='https://api.pixellab.ai/mcp'
H={'Authorization':f'Bearer {TOKEN}','Content-Type':'application/json'}
DST=r'F:\Jogo\assets\items'

ICONS = [
    ('weapon-sword',  'a fantasy steel longsword weapon, single game item icon, centered on transparent background'),
    ('weapon-axe',    'a fantasy battle axe weapon, single game item icon, centered on transparent background'),
    ('weapon-dagger', 'a fantasy curved dagger weapon, single game item icon, centered on transparent background'),
    ('weapon-hammer', 'a fantasy heavy war hammer weapon, single game item icon, centered on transparent background'),
    ('weapon-spear',  'a fantasy spear weapon, single game item icon, centered on transparent background'),
    ('weapon-mace',   'a fantasy spiked mace weapon, single game item icon, centered on transparent background'),
    ('weapon-bow',    'a fantasy wooden longbow weapon, single game item icon, centered on transparent background'),
    ('weapon-staff',  'a fantasy magic staff with a crystal top, single game item icon, centered on transparent background'),
    ('weapon-wand',   'a fantasy magic wand, single game item icon, centered on transparent background'),
    ('weapon-scythe', 'a fantasy scythe weapon, single game item icon, centered on transparent background'),
    ('slot-helm',     'a fantasy knight helmet, single armor game item icon, centered on transparent background'),
    ('slot-amulet',   'a fantasy magic amulet pendant necklace, single jewelry game item icon, centered on transparent background'),
    ('slot-armor',    'a fantasy steel chestplate breastplate armor, single armor game item icon, centered on transparent background'),
    ('slot-vest',     'a fantasy leather vest, single armor game item icon, centered on transparent background'),
    ('slot-pants',    'fantasy armored leggings, single armor game item icon, centered on transparent background'),
    ('slot-boots',    'a pair of fantasy leather boots, single armor game item icon, centered on transparent background'),
    ('slot-ring',     'a fantasy gold magic ring with a gem, single jewelry game item icon, centered on transparent background'),
]

def call(name, args):
    p={'jsonrpc':'2.0','method':'tools/call','params':{'name':name,'arguments':args},'id':1}
    for _ in range(6):
        try:
            r=requests.post(URL,headers=H,json=p,timeout=90)
            for line in r.text.split('\n'):
                if line.startswith('data: '):
                    return json.loads(line[6:])['result']['content'][0]['text']
        except Exception:
            pass
        time.sleep(6)
    return ''

# Submit (sequential with small gap to dodge rate-limit)
print('=== Submitting 17 item icons ===', flush=True)
ids = {}
for slug, desc in ICONS:
    oid = None
    for attempt in range(8):
        t = call('create_object', {'description': desc, 'size': 64, 'directions': 1,
                                    'view': 'side'})
        for ln in (t or '').split('\n'):
            if ln.strip().startswith('id:'):
                oid = ln.split(': ')[1].strip()
        if oid: break
        time.sleep(attempt*5+5)
    ids[slug] = oid
    print(f'  {slug:16s} -> {oid}', flush=True)

# Poll
print('\n=== Polling ===', flush=True)
for attempt in range(40):
    pending = [s for s,o in ids.items() if o and 'status: completed' not in call('get_object', {'object_id': o, 'include_preview': False})]
    if not pending:
        print('  all completed', flush=True); break
    print(f'  attempt {attempt+1}: {len(pending)} pending', flush=True)
    time.sleep(20)

# Download
print('\n=== Downloading ===', flush=True)
ok = 0
for slug, oid in ids.items():
    if not oid: continue
    t = call('get_object', {'object_id': oid, 'include_preview': False})
    url = None
    for ln in t.split('\n'):
        if 'unknown:' in ln and 'http' in ln:
            url = ln.split(': ',1)[1].strip()
    if not url:
        print(f'  {slug}: no url'); continue
    try:
        r = requests.get(url, timeout=60)
        open(os.path.join(DST, slug+'.png'),'wb').write(r.content)
        ok += 1
        print(f'  {slug}.png ({len(r.content)} b)', flush=True)
    except Exception as e:
        print(f'  {slug}: {e}', flush=True)
print(f'\n=== {ok}/17 downloaded ===', flush=True)
