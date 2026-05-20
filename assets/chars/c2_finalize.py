"""Poll + download C2 — 2 biome scenes + 8 monsters — then build monster GIFs."""
import json, requests, time, os, glob, zipfile, io
from PIL import Image

TOKEN='a8343c8c-5eaf-45a7-9570-5f77dac08cad'
URL='https://api.pixellab.ai/mcp'
H={'Authorization':f'Bearer {TOKEN}','Content-Type':'application/json'}
CHARS=r'F:\Jogo\assets\chars'
BIOMES=r'F:\Jogo\assets\biomes'

MAPS = {
    'temple-25d': 'ca34a4c3-8406-4f87-872d-d55a8e478783',
    'peaks-25d':  '7893d9bc-b33d-4496-9e2a-b089fc2d1a5f',
}
MONSTERS = {
    'drowned-acolyte': '7e943f20-45db-4925-a95e-0a32b98a7f24',
    'reef-serpent':    'e417798d-249d-4ee2-bf13-055b7b4d4ef1',
    'coral-golem':     '559e7573-ddae-4c27-8375-8b390ed03ee3',
    'tide-priest':     '371f8484-4182-4747-88e7-c367fa0b50fa',
    'harpy':           'c60629a3-4e2c-4fb2-8ff5-32d5541aeccd',
    'cloud-giant':     'bf48da25-4e3a-4ce7-9aa3-7a359b16a24d',
    'storm-eagle':     '6e4505ec-1e71-4ace-87d3-18c6cf2b3615',
    'thunder-roc':     '93080e5c-fe4b-4c6e-8d82-d893168574cc',
}

def call(name, args):
    p={'jsonrpc':'2.0','method':'tools/call','params':{'name':name,'arguments':args},'id':1}
    for _ in range(5):
        try:
            r=requests.post(URL,headers=H,json=p,timeout=90)
            for line in r.text.split('\n'):
                if line.startswith('data: '):
                    return json.loads(line[6:])['result']['content'][0]['text']
        except Exception:
            pass
        time.sleep(5)
    return ''

# --- Poll maps ---
print('=== Polling 2 biome scenes ===', flush=True)
for attempt in range(40):
    pend=[s for s,o in MAPS.items() if 'status: completed' not in call('get_map_object',{'object_id':o})]
    if not pend: print('  maps done', flush=True); break
    print(f'  {len(pend)} pending', flush=True); time.sleep(20)
for slug,oid in MAPS.items():
    t=call('get_map_object',{'object_id':oid})
    url=next((l.split(': ',1)[1].strip() for l in t.split('\n') if 'http' in l), None)
    if url:
        r=requests.get(url,timeout=60)
        open(os.path.join(BIOMES,slug+'.png'),'wb').write(r.content)
        print(f'  {slug}.png ({len(r.content)} b)', flush=True)

# --- Poll monsters (need 2 anims each) ---
print('\n=== Polling 8 monsters ===', flush=True)
for attempt in range(50):
    pend=[]
    for s,o in MONSTERS.items():
        t=call('get_character',{'character_id':o})
        if t.count('(east,')<2 or 'pending jobs' in t:
            pend.append(s)
    if not pend: print('  monsters done', flush=True); break
    print(f'  attempt {attempt+1}: {len(pend)} pending', flush=True); time.sleep(25)

# --- Download monster bundles ---
print('\n=== Downloading monster bundles ===', flush=True)
for slug,oid in MONSTERS.items():
    for r in range(8):
        resp=requests.get(f'{URL}/characters/{oid}/download',headers=H,timeout=90)
        if resp.status_code==200:
            zf=zipfile.ZipFile(io.BytesIO(resp.content))
            zf.extractall(os.path.join(CHARS,slug+'-c2'))
            print(f'  {slug} OK', flush=True)
            break
        time.sleep(r*8+8)
    else:
        print(f'  {slug} FAIL', flush=True)

# --- Build GIFs ---
print('\n=== Building monster GIFs ===', flush=True)
for slug in MONSTERS:
    base=os.path.join(CHARS,slug+'-c2')
    # find the char folder (skip metadata.json)
    sub=[d for d in os.listdir(base) if os.path.isdir(os.path.join(base,d))]
    if not sub: print(f'  {slug}: no folder'); continue
    anims_dir=os.path.join(base,sub[0],'animations')
    if not os.path.isdir(anims_dir): print(f'  {slug}: no anims'); continue
    cands=[]
    for a in os.listdir(anims_dir):
        ed=os.path.join(anims_dir,a,'east')
        if os.path.isdir(ed):
            fr=sorted(glob.glob(os.path.join(ed,'frame_*.png')))
            if fr: cands.append((len(fr),fr))
    if not cands: print(f'  {slug}: no frames'); continue
    cands.sort(key=lambda c:-c[0])
    idle=cands[0]; atk=cands[1] if len(cands)>1 else cands[0]
    ii=[Image.open(p).convert('RGBA') for p in idle[1]]
    ii[0].save(os.path.join(CHARS,slug+'-idle.gif'),save_all=True,append_images=ii[1:],
               duration=120,loop=0,disposal=2,transparency=0,optimize=True)
    ai=[Image.open(p).convert('RGBA') for p in atk[1]]
    ai[0].save(os.path.join(CHARS,slug+'-attack.gif'),save_all=True,append_images=ai[1:],
               duration=60,loop=1,disposal=2,transparency=0,optimize=True)
    print(f'  {slug}: idle={idle[0]}f atk={atk[0]}f', flush=True)
print('\n=== C2 finalize done ===', flush=True)
