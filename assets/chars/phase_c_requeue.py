"""Re-queue all Phase C animations now that chars are ready.
Validates responses to detect failures."""
import json, requests, time
from concurrent.futures import ThreadPoolExecutor, as_completed

TOKEN = 'a8343c8c-5eaf-45a7-9570-5f77dac08cad'
URL = 'https://api.pixellab.ai/mcp'
HEADERS = {'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'}

ATTACK_PROMPT = {
    'warrior': 'swings weapon forward in a powerful arc',
    'paladin': 'raises weapon overhead and brings it down with force',
    'hunter':  'draws bow back and releases arrow forward',
    'thief':   'lunges forward with a quick stab'
}

with open(r'F:\Jogo\assets\chars\phase_c_combos.json') as f:
    COMBOS = json.load(f)['combos']
with open(r'F:\Jogo\assets\chars\phase_c_state.json') as f:
    CHARS = json.load(f)['chars']

def call_mcp(name, args):
    payload = {'jsonrpc': '2.0', 'method': 'tools/call',
               'params': {'name': name, 'arguments': args}, 'id': 1}
    try:
        r = requests.post(URL, headers=HEADERS, json=payload, timeout=60)
        for line in r.text.split('\n'):
            if line.startswith('data: '):
                d = json.loads(line[6:])
                content = d.get('result', {}).get('content', [{}])
                return content[0].get('text', '') if content else ''
    except Exception as e:
        return f'ERROR: {e}'
    return ''

def queue_idle(combo):
    cid = CHARS[combo['slug']]
    txt = call_mcp('animate_character', {
        'character_id': cid,
        'template_animation_id': 'fight-stance-idle-8-frames',
        'directions': ['east'], 'animation_name': 'combat-idle'
    })
    ok = 'fight-stance-idle' in txt or 'jobs)' in txt
    return combo['slug'], ok, txt[:120] if not ok else 'OK'

def queue_caster(combo):
    cid = CHARS[combo['slug']]
    txt = call_mcp('animate_character', {
        'character_id': cid,
        'template_animation_id': 'fireball',
        'directions': ['east'], 'animation_name': 'combat-attack'
    })
    ok = 'fireball' in txt or 'jobs)' in txt
    return combo['slug'], ok, txt[:120] if not ok else 'OK'

def queue_melee(combo):
    cid = CHARS[combo['slug']]
    action = ATTACK_PROMPT[combo['class']]
    txt = call_mcp('animate_character', {
        'character_id': cid,
        'action_description': action,
        'directions': ['east'], 'animation_name': 'combat-attack',
        'confirm_cost': True
    })
    ok = 'animation:' in txt or 'jobs)' in txt
    return combo['slug'], ok, txt[:120] if not ok else 'OK'

# Check which already have animations (skip them)
def has_anims(cid):
    txt = call_mcp('get_character', {'character_id': cid})
    return '(east,' in txt

print('=== Checking existing anims (skip ones already animated) ===')
to_idle = []
to_caster = []
to_melee = []
already_done = []
for c in COMBOS:
    cid = CHARS[c['slug']]
    if has_anims(cid):
        already_done.append(c['slug'])
        continue
    to_idle.append(c)
    if c['anim'] == 'caster':
        to_caster.append(c)
    else:
        to_melee.append(c)

print(f'Already with anims: {len(already_done)}')
print(f'Need idle anim: {len(to_idle)}')
print(f'Need caster fireball: {len(to_caster)}')
print(f'Need custom melee: {len(to_melee)} (cost={len(to_melee)*20} gens)')

# Run with low concurrency to be safe
print('\n--- Queueing idles ---')
with ThreadPoolExecutor(max_workers=4) as pool:
    futures = [pool.submit(queue_idle, c) for c in to_idle]
    for fut in as_completed(futures):
        slug, ok, msg = fut.result()
        print(f'  {"OK" if ok else "FAIL"} {slug}: {msg if not ok else ""}')
        time.sleep(0.05)

print('\n--- Queueing caster fireballs ---')
with ThreadPoolExecutor(max_workers=4) as pool:
    futures = [pool.submit(queue_caster, c) for c in to_caster]
    for fut in as_completed(futures):
        slug, ok, msg = fut.result()
        print(f'  {"OK" if ok else "FAIL"} {slug}: {msg if not ok else ""}')

print('\n--- Queueing custom melee attacks ---')
with ThreadPoolExecutor(max_workers=4) as pool:
    futures = [pool.submit(queue_melee, c) for c in to_melee]
    for fut in as_completed(futures):
        slug, ok, msg = fut.result()
        print(f'  {"OK" if ok else "FAIL"} {slug}: {msg if not ok else ""}')

print('\nDone re-queueing.')
