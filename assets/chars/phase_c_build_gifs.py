"""Build all 39 Phase C character GIFs from downloaded bundles.
Auto-detect idle (most frames) and attack (other) per character.
Then patch index.html CLASS_SPRITES with all entries."""
from PIL import Image
import os, glob, json, re

DST = r'F:\Jogo\assets\chars'

with open(os.path.join(DST, 'phase_c_state.json')) as f:
    CHARS = json.load(f)['chars']

def find_char_folder(slug):
    """The extracted bundle has a folder named after the character (with underscores)."""
    extract_root = os.path.join(DST, f'{slug}-pixellab')
    if not os.path.isdir(extract_root):
        return None
    # Look for the char folder inside (PixelLab uses underscore form of the name)
    for entry in os.listdir(extract_root):
        if entry == 'metadata.json':
            continue
        full = os.path.join(extract_root, entry)
        if os.path.isdir(full):
            return full
    return None

def build_for(slug):
    base = find_char_folder(slug)
    if not base:
        return slug, False, 'no folder'
    anims_dir = os.path.join(base, 'animations')
    if not os.path.isdir(anims_dir):
        return slug, False, 'no animations folder'
    candidates = []
    for sub in os.listdir(anims_dir):
        east_dir = os.path.join(anims_dir, sub, 'east')
        if not os.path.isdir(east_dir): continue
        frames = sorted(glob.glob(os.path.join(east_dir, 'frame_*.png')))
        if frames:
            candidates.append((sub, east_dir, len(frames), frames))
    if len(candidates) == 0:
        return slug, False, 'no animations'
    # Sort: idle has more frames (8 frames vs 3-6 for attack)
    candidates.sort(key=lambda c: -c[2])
    idle = candidates[0]
    # Fallback: if only 1 anim, use it for both idle AND attack
    atk = candidates[1] if len(candidates) >= 2 else candidates[0]
    # Build idle (120ms/frame, infinite loop)
    idle_imgs = [Image.open(p).convert('RGBA') for p in idle[3]]
    idle_imgs[0].save(
        os.path.join(DST, f'{slug}-idle.gif'),
        save_all=True, append_images=idle_imgs[1:],
        duration=120, loop=0, disposal=2, transparency=0, optimize=True
    )
    # Build attack (60ms/frame, plays once)
    atk_imgs = [Image.open(p).convert('RGBA') for p in atk[3]]
    atk_imgs[0].save(
        os.path.join(DST, f'{slug}-attack.gif'),
        save_all=True, append_images=atk_imgs[1:],
        duration=60, loop=1, disposal=2, transparency=0, optimize=True
    )
    return slug, True, f'idle={idle[2]}f atk={atk[2]}f'

print('=== Building GIFs for all Phase C chars ===', flush=True)
results = {}
ok_count = 0; fail_count = 0
for slug in sorted(CHARS.keys()):
    s, ok, msg = build_for(slug)
    results[s] = (ok, msg)
    if ok:
        ok_count += 1
        print(f'  OK   {s:24s} {msg}', flush=True)
    else:
        fail_count += 1
        print(f'  FAIL {s:24s} {msg}', flush=True)

print(f'\nBuilt: {ok_count} ok, {fail_count} failed', flush=True)

# ─── Patch index.html CLASS_SPRITES table ────────────────────────────
print('\n=== Patching CLASS_SPRITES in index.html ===', flush=True)

# Read current index.html
idx_path = r'F:\Jogo\index.html'
with open(idx_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Build full CLASS_SPRITES table from all known sprites
# Existing combos already in file: keep them
existing_keys = ['human-warrior', 'elf-warrior', 'dwarf-paladin', 'orc-shaman', 'shifter-necromancer', 'elf-druid']
new_entries = []
all_keys = []
# Start with already-mapped ones
mapping = {
    'human-warrior':   ('assets/chars/human-warrior-idle.gif',  'assets/chars/human-warrior-attack.gif'),
    'elf-warrior':     ('assets/chars/elf-knight-idle.gif',     'assets/chars/elf-knight-attack.gif'),
    'dwarf-paladin':   ('assets/chars/dwarf-paladin-idle.gif',  'assets/chars/dwarf-paladin-attack.gif'),
    'orc-shaman':      ('assets/chars/orc-shaman-idle.gif',     'assets/chars/orc-shaman-attack.gif'),
    'shifter-necromancer': ('assets/chars/shifter-necromancer-idle.gif', 'assets/chars/shifter-necromancer-attack.gif'),
    'elf-druid':       ('assets/chars/elf-druid-idle.gif',      'assets/chars/elf-druid-attack.gif'),
}
# Add all successful Phase C builds
for slug, (ok, _) in results.items():
    if ok:
        mapping[slug] = (f'assets/chars/{slug}-idle.gif', f'assets/chars/{slug}-attack.gif')

# Order: alphabetical for cleanness
lines = []
for slug in sorted(mapping.keys()):
    idle, atk = mapping[slug]
    lines.append(f"  '{slug}': {{ idle: '{idle}', attack: '{atk}' }}")
new_block = ",\n".join(lines)

# Replace CLASS_SPRITES block. Match from `const CLASS_SPRITES = {` to matching `};`
pattern = re.compile(r'const CLASS_SPRITES = \{[\s\S]*?\n\};', re.MULTILINE)
new_text = (
    'const CLASS_SPRITES = {\n'
    '  // ============================================================\n'
    f'  // {len(mapping)} of 45 combos generated via PixelLab Tier 2 (S25-S27)\n'
    '  // ============================================================\n'
    + new_block + '\n};'
)
html2 = pattern.sub(new_text, html, count=1)
if html2 == html:
    print('  WARNING: CLASS_SPRITES block not replaced')
else:
    with open(idx_path, 'w', encoding='utf-8') as f:
        f.write(html2)
    print(f'  Patched: {len(mapping)} entries in CLASS_SPRITES')
