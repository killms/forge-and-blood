"""Build F2 monster GIFs (idle+attack) and F3 pet GIFs (idle only)."""
from PIL import Image
import os, glob

DST = r'F:\Jogo\assets\chars'

# (slug, char_folder, has_attack)
ENTRIES = [
    # F2 monsters — idle + attack
    ('frost-wolf',       'Frost_Wolf',       True),
    ('ice-wraith',       'Ice_Wraith',       True),
    ('glacial-golem',    'Glacial_Golem',    True),
    # F3 pets — idle only
    ('stray-cat',        'Stray_Cat',        False),
    ('carrier-pigeon',   'Carrier_Pigeon',   False),
    ('wolf-cub',         'Wolf_Cub',         False),
    ('owl',              'Owl',              False),
    ('spider',           'Spider',           False),
    ('bear-cub',         'Bear_Cub',         False),
    ('salamander',       'Salamander',       False),
    ('phantom',          'Phantom',          False),
    ('direwolf',         'Direwolf',         False),
    ('iron-golem',       'Iron_Golem',       False),
    ('arcane-eye',       'Arcane_Eye',       False),
    ('dragon-hatchling', 'Dragon_Hatchling', False),
    ('phoenix',          'Phoenix',          False),
    ('lich-familiar',    'Lich_Familiar',    False),
]

def build_for(slug, char_folder, has_attack):
    base = os.path.join(DST, f'{slug}-bundle', char_folder)
    anims_dir = os.path.join(base, 'animations')
    if not os.path.isdir(anims_dir):
        print(f'  {slug}: NO animations folder')
        return
    candidates = []
    for sub in os.listdir(anims_dir):
        east_dir = os.path.join(anims_dir, sub, 'east')
        if not os.path.isdir(east_dir):
            continue
        frames = sorted(glob.glob(os.path.join(east_dir, 'frame_*.png')))
        if frames:
            candidates.append((sub, east_dir, len(frames), frames))
    if not candidates:
        print(f'  {slug}: no anim frames')
        return
    # Sort by frame count desc — idle has more frames
    candidates.sort(key=lambda c: -c[2])
    idle = candidates[0]
    # Build idle GIF
    idle_imgs = [Image.open(p).convert('RGBA') for p in idle[3]]
    idle_imgs[0].save(
        os.path.join(DST, f'{slug}-idle.gif'),
        save_all=True, append_images=idle_imgs[1:],
        duration=120, loop=0, disposal=2, transparency=0, optimize=True
    )
    sz = idle_imgs[0].size
    # Build attack GIF if available
    if has_attack and len(candidates) >= 2:
        atk = candidates[1]
        atk_imgs = [Image.open(p).convert('RGBA') for p in atk[3]]
        atk_imgs[0].save(
            os.path.join(DST, f'{slug}-attack.gif'),
            save_all=True, append_images=atk_imgs[1:],
            duration=60, loop=1, disposal=2, transparency=0, optimize=True
        )
        print(f'  {slug}: OK idle={idle[2]}f atk={atk[2]}f size={sz[0]}x{sz[1]}')
    else:
        print(f'  {slug}: OK idle={idle[2]}f size={sz[0]}x{sz[1]}')

print('=== Building F2 + F3 GIFs ===')
for slug, folder, has_atk in ENTRIES:
    build_for(slug, folder, has_atk)
print('=== Done ===')
