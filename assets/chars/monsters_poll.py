"""Poll monsters until all have 2 anims + 0 pending."""
import json, requests, time, os
TOKEN = 'a8343c8c-5eaf-45a7-9570-5f77dac08cad'
URL = 'https://api.pixellab.ai/mcp'
HEADERS = {'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'}

with open(r'F:\Jogo\assets\chars\monsters_state.json') as f:
    monsters = json.load(f)['monsters']

def call(name, args):
    payload = {'jsonrpc':'2.0','method':'tools/call','params':{'name':name,'arguments':args},'id':1}
    r = requests.post(URL, headers=HEADERS, json=payload, timeout=60)
    for line in r.text.split('\n'):
        if line.startswith('data: '):
            return json.loads(line[6:])['result']['content'][0]['text']
    return ''

def status(cid):
    t = call('get_character', {'character_id': cid})
    return t.count('(east,'), 'pending jobs' in t

print('=== Polling monsters ===', flush=True)
for attempt in range(50):
    not_ready = []
    for slug, info in monsters.items():
        a, p = status(info['id'])
        if a < 2 or p:
            not_ready.append((slug, a, p))
    ts = time.strftime('%H:%M:%S')
    if not not_ready:
        print(f'[{ts}] *** ALL {len(monsters)} MONSTERS READY ***', flush=True)
        break
    print(f'[{ts}] attempt {attempt+1}: {len(not_ready)}/{len(monsters)} pending', flush=True)
    for slug, a, p in not_ready[:6]:
        print(f'  {slug:20s} anims={a} pending={p}', flush=True)
    time.sleep(25)
print('Done polling.', flush=True)
