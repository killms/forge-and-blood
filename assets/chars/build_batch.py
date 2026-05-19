"""Convert PixelLab character bundles to game GIFs.
Auto-detects idle (most frames) and attack (other) per character.
"""
from PIL import Image
import os, json, glob

DST = r'F:\Jogo\assets\chars'

# (race-class slug, extract folder, char folder name)
CHARS = [
    ('orc-shaman',           'orc-shaman-pixellab',          'Orc_Shaman'),
    ('dwarf-paladin',        'dwarf-paladin-pixellab',       'Dwarf_Paladin'),
    ('shifter-necromancer',  'shifter-necromancer-pixellab', 'Shifter_Necromancer'),
    ('elf-druid',            'elf-druid-pixellab',           'Elf_Druid'),
]

def build_for(slug, extract_folder, char_folder):
    base = os.path.join(DST, extract_folder, char_folder)
    anims_dir = os.path.join(base, 'animations')
    if not os.path.isdir(anims_dir):
        print(f'  {slug}: NO animations folder')
        return
    # Auto-detect: idle is the one with MORE frames, attack is the other
    candidates = []
    for sub in os.listdir(anims_dir):
        east_dir = os.path.join(anims_dir, sub, 'east')
        if not os.path.isdir(east_dir):
            continue
        frames = sorted(glob.glob(os.path.join(east_dir, 'frame_*.png')))
        candidates.append((sub, east_dir, len(frames), frames))
    if len(candidates) < 2:
        print(f'  {slug}: needs 2 animations, found {len(candidates)}')
        return
    # Sort by frame count descending — idle has more frames
    candidates.sort(key=lambda c: -c[2])
    idle_sub, idle_dir, idle_n, idle_frames = candidates[0]
    atk_sub,  atk_dir,  atk_n,  atk_frames  = candidates[1]
    # Build idle GIF — 120ms per frame, infinite loop
    idle_imgs = [Image.open(p).convert('RGBA') for p in idle_frames]
    idle_imgs[0].save(
        os.path.join(DST, f'{slug}-idle.gif'),
        save_all=True, append_images=idle_imgs[1:],
        duration=120, loop=0, disposal=2, transparency=0, optimize=True
    )
    # Build attack GIF — 60ms per frame, plays once
    atk_imgs = [Image.open(p).convert('RGBA') for p in atk_frames]
    atk_imgs[0].save(
        os.path.join(DST, f'{slug}-attack.gif'),
        save_all=True, append_images=atk_imgs[1:],
        duration=60, loop=1, disposal=2, transparency=0, optimize=True
    )
    sz = Image.open(os.path.join(DST, f'{slug}-idle.gif')).size
    print(f'  {slug}: OK idle={idle_n}f attack={atk_n}f size={sz[0]}x{sz[1]}')

print('=== Building GIFs ===')
for slug, ef, cf in CHARS:
    build_for(slug, ef, cf)
print('=== Done ===')

# Summary
import os
for slug, _, _ in CHARS:
    for suffix in ['idle', 'attack']:
        p = os.path.join(DST, f'{slug}-{suffix}.gif')
        if os.path.exists(p):
            print(f'  {os.path.basename(p)}: {os.path.getsize(p)} bytes')
