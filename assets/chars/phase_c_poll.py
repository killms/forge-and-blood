"""Poll PixelLab until all Phase C jobs are done."""
import json, requests, time

TOKEN = 'a8343c8c-5eaf-45a7-9570-5f77dac08cad'
URL = 'https://api.pixellab.ai/mcp'
HEADERS = {'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'}

with open(r'F:\Jogo\assets\chars\phase_c_state.json') as f:
    state = json.load(f)
CHARS = state['chars']

def get_status(cid):
    payload = {'jsonrpc': '2.0', 'method': 'tools/call',
               'params': {'name': 'get_character', 'arguments': {'character_id': cid}},
               'id': 1}
    r = requests.post(URL, headers=HEADERS, json=payload, timeout=60)
    for line in r.text.split('\n'):
        if line.startswith('data: '):
            d = json.loads(line[6:])
            return d.get('result', {}).get('content', [{}])[0].get('text', '')
    return ''

def is_done(status):
    if not status: return False
    return 'pending jobs' not in status and 'creating' not in status

attempt = 0
while attempt < 50:
    attempt += 1
    t = time.strftime('%H:%M:%S')
    pending = []
    done = []
    pending_summary = {}
    for slug, cid in CHARS.items():
        if cid is None:
            pending.append(slug)
            continue
        s = get_status(cid)
        if is_done(s):
            done.append(slug)
        else:
            pending.append(slug)
            # Extract first pending job
            for line in s.split('\n'):
                if ':' in line and ('%' in line or 's' in line.split(':')[-1]):
                    if 'pending' not in line:
                        pending_summary.setdefault(slug, []).append(line.strip()[:80])
                        break
    print(f'\n=== [{t}] Attempt {attempt}: done={len(done)}/{len(CHARS)} pending={len(pending)} ===')
    if len(pending) <= 10:
        # Show pending jobs detail
        for slug in pending:
            jobs = pending_summary.get(slug, ['(no detail)'])
            print(f'  ⏳ {slug:24s} {jobs[0] if jobs else ""}')
    if not pending:
        print('\n*** ALL DONE ***')
        break
    time.sleep(45)

print('\nFinal state:')
for slug, cid in CHARS.items():
    s = get_status(cid)
    anims_count = s.count('(east,')
    print(f'  {slug:24s} anims={anims_count}')
