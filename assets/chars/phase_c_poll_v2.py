"""Clean poll: wait until all 39 chars have >=2 anims and 0 pending."""
import json, requests, time, sys

TOKEN = 'a8343c8c-5eaf-45a7-9570-5f77dac08cad'
URL = 'https://api.pixellab.ai/mcp'
HEADERS = {'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'}

with open(r'F:\Jogo\assets\chars\phase_c_state.json') as f:
    CHARS = json.load(f)['chars']

def call(name, args):
    payload = {'jsonrpc':'2.0','method':'tools/call','params':{'name':name,'arguments':args},'id':1}
    r = requests.post(URL, headers=HEADERS, json=payload, timeout=60)
    for line in r.text.split('\n'):
        if line.startswith('data: '):
            return json.loads(line[6:])['result']['content'][0]['text']
    return ''

def status(cid):
    text = call('get_character', {'character_id': cid})
    anims = text.count('(east,')
    pending_match = 'pending jobs' in text
    pct = 0
    eta = ''
    if pending_match:
        for ln in text.split('\n'):
            if '%' in ln and ('east' in ln or 'attack' in ln or 'idle' in ln):
                eta = ln.strip()[:60]
                break
    return anims, pending_match, eta

print('=== Polling all chars ===', flush=True)
for attempt in range(60):
    not_ready = []
    for slug, cid in CHARS.items():
        a, p, eta = status(cid)
        if a < 2 or p:
            not_ready.append((slug, a, p, eta))
    t = time.strftime('%H:%M:%S')
    if not not_ready:
        print(f'[{t}] *** ALL 39 READY ***', flush=True)
        break
    print(f'[{t}] attempt {attempt+1}: {len(not_ready)}/{len(CHARS)} still working', flush=True)
    if len(not_ready) <= 12:
        for slug, a, p, eta in not_ready[:12]:
            print(f'  {slug:24s} anims={a} {("pending: "+eta) if p else "no pending"}', flush=True)
    time.sleep(30)

print('Done polling.', flush=True)
