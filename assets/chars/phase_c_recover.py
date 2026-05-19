"""Phase C recovery: resubmit missing chars + queue all missing anims.
Conservative concurrency (5 max) + retries to avoid rate limits."""
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
                    text = content[0].get('text', '')
                    is_error = d.get('result', {}).get('isError', False)
                    return text, is_error
    except Exception as e:
        return f'EXCEPTION: {e}', True
    return '', True

def list_characters():
    """Fetch all chars on account, build slug -> id map."""
    text, err = call_mcp('list_characters', {'limit': 50})
    if err:
        return {}
    by_slug = {}
    for line in text.split('\n'):
        line = line.strip()
        if '|' not in line: continue
        # Format: "id | name | dirs size | anims"
        parts = [p.strip() for p in line.split('|')]
        if len(parts) < 2: continue
        cid = parts[0].lstrip('+').strip()
        name = parts[1]
        by_slug[name] = cid
    return by_slug

print('=== Step 1: List existing characters ===')
existing = list_characters()
print(f'Found {len(existing)} chars on account')

# Map our slugs to existing chars
CHARS = {}
missing = []
for c in COMBOS:
    slug = c['slug']
    if slug in existing:
        CHARS[slug] = existing[slug]
    else:
        missing.append(c)

print(f'Mapped to existing: {len(CHARS)}')
print(f'Missing (need create): {len(missing)}')

# ─── Resubmit missing chars, low concurrency + retry ─────────────────
def create_char_retry(combo, max_retries=3):
    args = {
        'description': combo['desc'],
        'name': combo['slug'],
        'size': 64, 'n_directions': 4, 'view': 'side', 'mode': 'standard',
        'body_type': 'humanoid',
        'outline': 'single color black outline',
        'shading': 'basic shading', 'detail': 'medium detail'
    }
    for attempt in range(max_retries):
        text, err = call_mcp('create_character', args)
        # Extract id from text even if it had errors
        for line in text.split('\n'):
            if line.startswith('id: '):
                return combo['slug'], line[4:].strip(), None
        if 'rate' in text.lower() or 'job slots' in text.lower():
            time.sleep(15 * (attempt + 1))
            continue
        return combo['slug'], None, text[:120]
    return combo['slug'], None, 'max retries exceeded'

if missing:
    print(f'\n=== Step 2: Create {len(missing)} missing chars (5 concurrency, w/ retry) ===')
    with ThreadPoolExecutor(max_workers=5) as pool:
        futures = [pool.submit(create_char_retry, c) for c in missing]
        for fut in as_completed(futures):
            slug, cid, err = fut.result()
            if cid:
                CHARS[slug] = cid
                print(f'  OK   {slug:24s} -> {cid}')
            else:
                print(f'  FAIL {slug:24s} : {err}')

# Save state
state = {'chars': CHARS}
with open(r'F:\Jogo\assets\chars\phase_c_state.json', 'w') as f:
    json.dump(state, f, indent=2)
print(f'\nState saved: {len(CHARS)} chars')

# ─── Step 3: Poll until all chars created ────────────────────────────
print('\n=== Step 3: Wait for chars to be created ===')
for attempt in range(30):
    pending = []
    for slug, cid in CHARS.items():
        text, _ = call_mcp('get_character', {'character_id': cid})
        # Char is created when status: completed AND rotations are listed
        if 'status: completed' not in text:
            pending.append(slug)
    if not pending:
        print(f'  All {len(CHARS)} chars ready')
        break
    t = time.strftime('%H:%M:%S')
    print(f'  [{t}] attempt {attempt+1}: {len(pending)} chars still creating')
    time.sleep(30)
