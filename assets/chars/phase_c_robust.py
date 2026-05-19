"""Robust Phase C re-queue: detect missing anims accurately, queue with proper retry."""
import json, requests, time, os
import sys

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

def call_mcp(name, args, timeout=60):
    payload = {'jsonrpc': '2.0', 'method': 'tools/call',
               'params': {'name': name, 'arguments': args}, 'id': 1}
    try:
        r = requests.post(URL, headers=HEADERS, json=payload, timeout=timeout)
        for line in r.text.split('\n'):
            if line.startswith('data: '):
                d = json.loads(line[6:])
                content = d.get('result', {}).get('content', [{}])
                if content:
                    return content[0].get('text', '')
    except Exception as e:
        return f'EXC: {e}'
    return ''

def char_anim_status(cid):
    """Return (anim_names_set, pending_count) for a char."""
    text = call_mcp('get_character', {'character_id': cid})
    anim_names = set()
    pending = 0
    in_anims = False
    for line in text.split('\n'):
        ls = line.strip()
        if ls.startswith('animations'):
            in_anims = 'none' not in ls
            continue
        if ls.startswith('pending jobs'):
            in_anims = False
            try:
                pending = int(ls.split('(')[1].split(')')[0])
            except: pass
            continue
        if ls.startswith('actions') or ls.startswith('hint') or ls.startswith('available'):
            in_anims = False
        if in_anims and '(east' in ls:
            anim_names.add(ls.split(' ')[0])
    return anim_names, pending

def submit_anim(cid, kind, combo):
    """Submit a single anim. Returns (ok, response_text)."""
    if kind == 'idle':
        args = {'character_id': cid, 'template_animation_id': 'fight-stance-idle-8-frames',
                'directions': ['east'], 'animation_name': 'combat-idle'}
    elif combo['anim'] == 'caster':
        args = {'character_id': cid, 'template_animation_id': 'fireball',
                'directions': ['east'], 'animation_name': 'combat-attack'}
    else:
        action = ATTACK_PROMPT[combo['class']]
        args = {'character_id': cid, 'action_description': action,
                'directions': ['east'], 'animation_name': 'combat-attack', 'confirm_cost': True}
    text = call_mcp('animate_character', args)
    # STRICT success markers:
    # - "directions: east (N jobs)" - jobs were queued
    # - "eta: ~" - eta given
    # NOT in success: error messages saying "need N job slots"
    if 'eta: ~' in text or '(east (' in text or 'animation:' in text and 'jobs)' in text:
        # Double-check NOT an error
        if 'error:' in text.lower() or 'need ' in text and 'job slots' in text:
            return False, text[:120]
        return True, 'queued'
    return False, text[:120]

# ─── Main: identify missing anims, queue them with retry ──────────────
print('=== Round 1: identify what each char needs ===', flush=True)
needs_idle = []
needs_atk = []
for c in COMBOS:
    cid = CHARS[c['slug']]
    if not cid:
        print(f'  SKIP {c["slug"]} no cid', flush=True); continue
    anims, pending = char_anim_status(cid)
    has_idle = 'fight-stance-idle-8-frames' in anims
    has_atk = 'fireball' in anims or any('animating' in a or 'jab' in a.lower() for a in anims)
    if not has_idle:
        needs_idle.append(c)
    if not has_atk:
        needs_atk.append(c)
print(f'  needs idle: {len(needs_idle)}', flush=True)
print(f'  needs attack: {len(needs_atk)}', flush=True)

def queue_serial_with_retry(items, kind):
    """Queue items one at a time with retry on rate-limit/queue-full."""
    successes = 0; fails = 0
    for c in items:
        cid = CHARS[c['slug']]
        for attempt in range(8):
            ok, msg = submit_anim(cid, kind, c)
            if ok:
                successes += 1
                print(f'  OK {kind} {c["slug"]}', flush=True)
                break
            if 'job slots' in msg or 'queue' in msg.lower():
                # Queue full - wait
                wait_s = 25 + attempt * 5
                print(f'  WAIT {wait_s}s for queue (attempt {attempt+1}) {c["slug"]}', flush=True)
                time.sleep(wait_s)
                continue
            if 'rate' in msg.lower() or 'EXC:' in msg:
                time.sleep(20)
                continue
            # Unknown error - bail
            fails += 1
            print(f'  FAIL {kind} {c["slug"]}: {msg}', flush=True)
            break
        else:
            fails += 1
            print(f'  GIVE-UP {kind} {c["slug"]}', flush=True)
        # Small pause between calls to prevent rate limit
        time.sleep(0.5)
    return successes, fails

print('\n=== Round 2: queue all missing idle anims ===', flush=True)
ok, fail = queue_serial_with_retry(needs_idle, 'idle')
print(f'  Result: {ok} ok, {fail} fail', flush=True)

print('\n=== Round 3: queue all missing attack anims ===', flush=True)
ok, fail = queue_serial_with_retry(needs_atk, 'attack')
print(f'  Result: {ok} ok, {fail} fail', flush=True)

# ─── Poll until ALL chars have ≥2 anims with no pending ──────────────
print('\n=== Round 4: poll until all anims done ===', flush=True)
for attempt in range(60):  # 60 * 30s = 30 min max
    not_ready = []
    for c in COMBOS:
        cid = CHARS[c['slug']]
        anims, pending = char_anim_status(cid)
        if len(anims) < 2 or pending > 0:
            not_ready.append((c['slug'], len(anims), pending))
    t = time.strftime('%H:%M:%S')
    if not not_ready:
        print(f'[{t}] *** ALL ANIMS COMPLETE ***', flush=True)
        break
    print(f'[{t}] attempt {attempt+1}: {len(not_ready)}/{len(COMBOS)} still working', flush=True)
    if len(not_ready) <= 8:
        for slug, ac, pc in not_ready[:8]:
            print(f'  ⏳ {slug:24s} anims={ac} pending={pc}', flush=True)
    time.sleep(30)
else:
    print('Poll exhausted', flush=True)

print('\nDone.', flush=True)
