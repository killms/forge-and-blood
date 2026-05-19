"""Build monster GIFs (idle + attack) from PixelLab bundles."""
from PIL import Image
import os, glob, json

DST = r'F:\Jogo\assets\chars'

# Folder names inside each zip (PixelLab converts spaces to underscores)
MONSTERS = [
    ('giant-rat',        'Giant_Rat'),
    ('ash-wolf',         'Ash_Wolf'),
    ('lava-hound',       'Lava_Hound'),
    ('salamander-king',  'Salamander_King'),
    ('young-dragon',     'Young_Dragon'),
    ('goblin-raider',    'Goblin_Raider'),
    ('skeleton-warrior', 'Skeleton_Warrior'),
    ('cave-ogre',        'Cave_Ogre'),
    ('awakened-lich',    'Awakened_Lich'),
    ('fire-imp',         'Fire_Imp')
]

def build_for(slug, char_folder):
    base = os.path.join(DST, f'{slug}-monster', char_folder)
    anims_dir = os.path.join(base, 'animations')
    if not os.path.isdir(anims_dir):
        print(f'  {slug}: NO animations folder')
        return False
    candidates = []
    for sub in os.listdir(anims_dir):
        east_dir = os.path.join(anims_dir, sub, 'east')
        if not os.path.isdir(east_dir):
            continue
        frames = sorted(glob.glob(os.path.join(east_dir, 'frame_*.png')))
        if frames:
            candidates.append((sub, east_dir, len(frames), frames))
    if len(candidates) < 1:
        print(f'  {slug}: no animation frames')
        return False
    # Sort by frame count desc: idle (more frames) first
    candidates.sort(key=lambda c: -c[2])
    if len(candidates) >= 2:
        idle = candidates[0]
        atk  = candidates[1]
    else:
        # Only one anim — use it as both idle and attack
        idle = candidates[0]
        atk  = candidates[0]
    # idle: 120ms per frame, loop infinite
    idle_imgs = [Image.open(p).convert('RGBA') for p in idle[3]]
    idle_imgs[0].save(
        os.path.join(DST, f'{slug}-idle.gif'),
        save_all=True, append_images=idle_imgs[1:],
        duration=120, loop=0, disposal=2, transparency=0, optimize=True
    )
    # attack: 60ms per frame, plays once
    atk_imgs = [Image.open(p).convert('RGBA') for p in atk[3]]
    atk_imgs[0].save(
        os.path.join(DST, f'{slug}-attack.gif'),
        save_all=True, append_images=atk_imgs[1:],
        duration=60, loop=1, disposal=2, transparency=0, optimize=True
    )
    print(f'  {slug}: OK idle={idle[2]}f atk={atk[2]}f')
    return True

print('=== Building monster GIFs ===')
ok = fail = 0
for slug, folder in MONSTERS:
    if build_for(slug, folder):
        ok += 1
    else:
        fail += 1
print(f'\nBuilt {ok} ok, {fail} failed')

# Show file sizes
print('\n=== GIF files ===')
for slug, _ in MONSTERS:
    for suffix in ['idle', 'attack']:
        p = os.path.join(DST, f'{slug}-{suffix}.gif')
        if os.path.exists(p):
            size = os.path.getsize(p)
            im = Image.open(p)
            print(f'  {slug}-{suffix}.gif: {im.size[0]}x{im.size[1]} {size}b')
