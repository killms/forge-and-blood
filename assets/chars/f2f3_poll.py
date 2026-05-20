"""Poll F2+F3 chars until ready."""
import json, requests, time
TOKEN='a8343c8c-5eaf-45a7-9570-5f77dac08cad'
URL='https://api.pixellab.ai/mcp'
H={'Authorization':f'Bearer {TOKEN}','Content-Type':'application/json'}

with open(r'F:\Jogo\assets\chars\f2f3_state.json') as f:
    state = json.load(f)
ALL = {**state['monsters'], **state['pets']}
# monsters need 2 anims (idle+attack); pets need 1 (idle only)
PETS_NEED = 1
MONSTERS_NEED = 2
mon_keys = set(state['monsters'].keys())

def status(cid):
    payload={'jsonrpc':'2.0','method':'tools/call','params':{'name':'get_character','arguments':{'character_id':cid}},'id':1}
    r=requests.post(URL,headers=H,json=payload,timeout=60)
    for line in r.text.split('\n'):
        if line.startswith('data: '):
            t=json.loads(line[6:])['result']['content'][0]['text']
            return t.count('(east,'), 'pending jobs' in t
    return 0, False

for attempt in range(40):
    not_ready = []
    for slug,info in ALL.items():
        need = MONSTERS_NEED if slug in mon_keys else PETS_NEED
        a, p = status(info['id'])
        if a < need or p:
            not_ready.append((slug, a, need, p))
    ts = time.strftime('%H:%M:%S')
    if not not_ready:
        print(f'[{ts}] ALL DONE',flush=True); break
    print(f'[{ts}] attempt {attempt+1}: {len(not_ready)}/{len(ALL)} pending',flush=True)
    for slug,a,need,p in not_ready[:8]:
        print(f'  {slug:20s} anims={a}/{need} pending={p}',flush=True)
    time.sleep(30)
print('Done polling.',flush=True)
