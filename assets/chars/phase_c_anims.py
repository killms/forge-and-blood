"""Queue all missing animations for Phase C chars.
Handles job-slot-full errors with retries."""
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
COMBO_BY_SLUG = {c['slug']: c for c in COMBOS}

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
                if content:
                    return content[0].get('text', '')
    except Exception:
        return ''
    return ''

def char_state(cid):
    text = call_mcp('get_character', {'character_id': cid})
    # Count distinct animations by their template/action name lines
    anim_names = []
    in_anims = False
    pending_count = 0
    for line in text.split('\n'):
        ls = line.strip()
        if ls.startswith('animations'):
            if 'none' in ls:
                in_anims = False
            else:
                in_anims = True
            continue
        if ls.startswith('pending jobs'):
            in_anims = False
            try:
                pending_count = int(ls.split('(')[1].split(')')[0])
            except Exception: pass
            continue
        if in_anims and ls and not ls.startswith('actions') and not ls.startswith('hint') and not ls.startswith('available'):
            if '(east' in ls:
                anim_names.append(ls.split(' ')[0])
        if ls.startswith('actions') or ls.startswith('hint') or ls.startswith('available'):
            in_anims = False
    return anim_names, pending_count

def queue_with_retry(cid, args, max_retries=10):
    for attempt in range(max_retries):
        text = call_mcp('animate_character', args)
        if 'jobs)' in text or 'jobs ' in text or 'animation:' in text:
            return True, text
        if 'job slots' in text or 'queue' in text.lower():
            time.sleep(20)
            continue
        if 'rate' in text.lower() or 'too many' in text.lower():
            time.sleep(30)
            continue
        return False, text[:150]
    return False, 'max retries'

def queue_idle(combo):
    cid = CHARS[combo['slug']]
    names, _ = char_state(cid)
    if 'fight-stance-idle-8-frames' in names:
        return combo['slug'], True, 'already-done'
    ok, msg = queue_with_retry(cid, {
        'character_id': cid,
        'template_animation_id': 'fight-stance-idle-8-frames',
        'directions': ['east'], 'animation_name': 'combat-idle'
    })
    return combo['slug'], ok, msg if not ok else 'queued'

def queue_attack(combo):
    cid = CHARS[combo['slug']]
    names, _ = char_state(cid)
    # Skip if already has attack template fireball or any custom
    if 'fireball' in names or any('jab' in n or 'attack' in n.lower() for n in names):
        return combo['slug'], True, 'already-done'
    if combo['anim'] == 'caster':
        ok, msg = queue_with_retry(cid, {
            'character_id': cid,
            'template_animation_id': 'fireball',
            'directions': ['east'], 'animation_name': 'combat-attack'
        })
    else:
        action = ATTACK_PROMPT[combo['class']]
        ok, msg = queue_with_retry(cid, {
            'character_id': cid,
            'action_description': action,
            'directions': ['east'], 'animation_name': 'combat-attack',
            'confirm_cost': True
        })
    return combo['slug'], ok, msg if not ok else 'queued'

print(f'=== Queue idles for {len(COMBOS)} combos (skipping done) ===')
with ThreadPoolExecutor(max_workers=4) as pool:
    futures = [pool.submit(queue_idle, c) for c in COMBOS]
    success = 0
    skipped = 0
    failed = 0
    for fut in as_completed(futures):
        slug, ok, msg = fut.result()
        if ok and msg == 'already-done':
            skipped += 1
        elif ok:
            success += 1
        else:
            failed += 1
            print(f'  FAIL {slug}: {msg}')
    print(f'  idle: success={success} skipped={skipped} failed={failed}')

print(f'\n=== Queue attacks ===')
with ThreadPoolExecutor(max_workers=4) as pool:
    futures = [pool.submit(queue_attack, c) for c in COMBOS]
    success = 0
    skipped = 0
    failed = 0
    for fut in as_completed(futures):
        slug, ok, msg = fut.result()
        if ok and msg == 'already-done':
            skipped += 1
        elif ok:
            success += 1
        else:
            failed += 1
            print(f'  FAIL {slug}: {msg}')
    print(f'  attack: success={success} skipped={skipped} failed={failed}')

print('\nDone queuing.')
