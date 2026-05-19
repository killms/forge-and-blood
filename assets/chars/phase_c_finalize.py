"""Final stage: poll until all anims ready, download all zips, build GIFs."""
import json, requests, time, os, subprocess, zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys

TOKEN = 'a8343c8c-5eaf-45a7-9570-5f77dac08cad'
URL = 'https://api.pixellab.ai/mcp'
HEADERS = {'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'}
DST = r'F:\Jogo\assets\chars'

with open(os.path.join(DST, 'phase_c_state.json')) as f:
    CHARS = json.load(f)['chars']

def flush(*a, **k):
    print(*a, **k, flush=True)

def call_mcp(name, args):
    payload = {'jsonrpc': '2.0', 'method': 'tools/call',
               'params': {'name': name, 'arguments': args}, 'id': 1}
    try:
        r = requests.post(URL, headers=HEADERS, json=payload, timeout=90)
        for line in r.text.split('\n'):
            if line.startswith('data: '):
                d = json.loads(line[6:])
                content = d.get('result', {}).get('content', [{}])
                if content:
                    return content[0].get('text', '')
    except Exception as e:
        return f'EXCEPTION: {e}'
    return ''

# ─── Poll until all 39 chars are fully done ─────────────────────────
flush('=== Poll until anims complete ===')
for attempt in range(80):  # 80 * 30s = 40 mins max
    pending = []
    summary = []
    for slug, cid in CHARS.items():
        text = call_mcp('get_character', {'character_id': cid})
        if 'pending jobs' in text or 'creating' in text:
            pending.append(slug)
            for line in text.split('\n'):
                if '%' in line or '~' in line:
                    if 'pending' not in line and slug not in [s.split(':')[0] for s in summary]:
                        summary.append(f'{slug}: {line.strip()[:60]}')
                        break
    t = time.strftime('%H:%M:%S')
    if not pending:
        flush(f'[{t}] *** ALL ANIMS DONE ***')
        break
    flush(f'[{t}] attempt {attempt+1}: {len(pending)}/{len(CHARS)} pending')
    if len(pending) <= 8:
        for s in summary[:8]:
            flush(f'  ⏳ {s}')
    time.sleep(30)
else:
    flush('Poll exhausted — proceeding with what we have')

# ─── Download zips in parallel ──────────────────────────────────────
flush('\n=== Download character bundles ===')
def download_one(slug, cid):
    url = f'{URL}/characters/{cid}/download'
    folder = f'{slug}-pixellab'
    zip_path = os.path.join(DST, folder + '.zip')
    extract_path = os.path.join(DST, folder)
    try:
        r = requests.get(url, headers=HEADERS, timeout=120, stream=True)
        if r.status_code != 200:
            return slug, False, f'HTTP {r.status_code}'
        with open(zip_path, 'wb') as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)
        # Extract
        os.makedirs(extract_path, exist_ok=True)
        with zipfile.ZipFile(zip_path, 'r') as z:
            z.extractall(extract_path)
        return slug, True, f'{os.path.getsize(zip_path)} bytes'
    except Exception as e:
        return slug, False, str(e)

with ThreadPoolExecutor(max_workers=8) as pool:
    futures = {pool.submit(download_one, slug, cid): slug for slug, cid in CHARS.items()}
    ok_count = 0; fail_count = 0
    for fut in as_completed(futures):
        slug, ok, msg = fut.result()
        if ok:
            ok_count += 1
        else:
            fail_count += 1
            flush(f'  FAIL {slug}: {msg}')
    flush(f'  Downloads: OK={ok_count} FAIL={fail_count}')

flush('\nDone. Run phase_c_build_gifs.py next to convert into GIFs.')
