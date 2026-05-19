"""Phase C: submit 39 chars + animations to PixelLab in parallel."""
import json, requests, time, os
from concurrent.futures import ThreadPoolExecutor, as_completed

TOKEN = 'a8343c8c-5eaf-45a7-9570-5f77dac08cad'
URL = 'https://api.pixellab.ai/mcp'
HEADERS = {'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'}

# Custom attack prompts by class (weapon-agnostic — PixelLab infers from char's weapon)
ATTACK_PROMPT = {
    'warrior': 'swings weapon forward in a powerful arc',
    'paladin': 'raises weapon overhead and brings it down with force',
    'hunter':  'draws bow back and releases arrow forward',
    'thief':   'lunges forward with a quick stab'
}

def call_mcp(method, name, args, rid=1):
    """Call MCP JSON-RPC endpoint. Returns the text from the response."""
    payload = {
        'jsonrpc': '2.0', 'method': 'tools/call',
        'params': {'name': name, 'arguments': args},
        'id': rid
    }
    r = requests.post(URL, headers=HEADERS, json=payload, timeout=60)
    # Response is SSE format: "event: message\ndata: {...}\n\n"
    for line in r.text.split('\n'):
        if line.startswith('data: '):
            data = json.loads(line[6:])
            content = data.get('result', {}).get('content', [])
            if content:
                return content[0].get('text', '')
    return None

def create_character(combo):
    """Submit char creation. Returns char_id."""
    args = {
        'description': combo['desc'],
        'name': combo['slug'],
        'size': 64, 'n_directions': 4, 'view': 'side', 'mode': 'standard',
        'body_type': 'humanoid',
        'outline': 'single color black outline',
        'shading': 'basic shading', 'detail': 'medium detail'
    }
    text = call_mcp('tools/call', 'create_character', args)
    if not text: return None
    for line in text.split('\n'):
        if line.startswith('id: '):
            return line[4:].strip()
    return None

def queue_anim(char_id, template=None, action=None, name='anim', confirm=False):
    args = {'character_id': char_id, 'directions': ['east'], 'animation_name': name}
    if template:
        args['template_animation_id'] = template
    elif action:
        args['action_description'] = action
        if confirm:
            args['confirm_cost'] = True
    return call_mcp('tools/call', 'animate_character', args)

with open(r'F:\Jogo\assets\chars\phase_c_combos.json', 'r', encoding='utf-8') as f:
    DATA = json.load(f)
COMBOS = DATA['combos']
print(f'=== Phase C: {len(COMBOS)} combos ===')

# Step 1 — 39 chars in parallel
print('\n--- Step 1: 39 char creations ---')
char_ids = {}
with ThreadPoolExecutor(max_workers=15) as pool:
    futures = {pool.submit(create_character, c): c for c in COMBOS}
    for fut in as_completed(futures):
        c = futures[fut]
        cid = fut.result()
        char_ids[c['slug']] = cid
        print(f'  {c["slug"]:24s} -> {cid}')

# Save state
state_path = r'F:\Jogo\assets\chars\phase_c_state.json'
state = {'chars': char_ids, 'submitted_anims': []}
with open(state_path, 'w') as f:
    json.dump(state, f, indent=2)

# Step 2 — Queue idle anims for ALL 39 (template, 1 gen each)
print('\n--- Step 2: 39 idle template anims ---')
def queue_idle(combo):
    cid = char_ids[combo['slug']]
    return combo['slug'], queue_anim(cid, template='fight-stance-idle-8-frames', name='idle')

with ThreadPoolExecutor(max_workers=15) as pool:
    futures = [pool.submit(queue_idle, c) for c in COMBOS]
    for fut in as_completed(futures):
        slug, _ = fut.result()
        print(f'  idle queued: {slug}')

# Step 3 — Queue attack anims
casters = [c for c in COMBOS if c['anim'] == 'caster']
melees  = [c for c in COMBOS if c['anim'] == 'melee']
print(f'\n--- Step 3: {len(casters)} caster fireballs (template) ---')
def queue_caster(combo):
    cid = char_ids[combo['slug']]
    return combo['slug'], queue_anim(cid, template='fireball', name='attack')

with ThreadPoolExecutor(max_workers=15) as pool:
    futures = [pool.submit(queue_caster, c) for c in casters]
    for fut in as_completed(futures):
        slug, _ = fut.result()
        print(f'  fireball queued: {slug}')

# Step 4 — Queue custom melee attacks (20 gens each, with confirm_cost=true)
print(f'\n--- Step 4: {len(melees)} custom melee attacks (20 gens each = {len(melees)*20} gens) ---')
def queue_melee(combo):
    cid = char_ids[combo['slug']]
    action = ATTACK_PROMPT[combo['class']]
    return combo['slug'], queue_anim(cid, action=action, name='attack', confirm=True)

with ThreadPoolExecutor(max_workers=10) as pool:
    futures = [pool.submit(queue_melee, c) for c in melees]
    for fut in as_completed(futures):
        slug, txt = fut.result()
        # Detect errors
        ok = 'animation:' in (txt or '')
        print(f'  custom melee queued: {slug}  [{"OK" if ok else "?"}]')

# Save final state
state['submitted_anims'] = [c['slug'] for c in COMBOS]
with open(state_path, 'w') as f:
    json.dump(state, f, indent=2)

print('\n=== All jobs submitted. State saved to', state_path)
print('Now poll until done with phase_c_poll.py')
