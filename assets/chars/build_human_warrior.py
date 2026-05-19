"""Convert PixelLab Human Warrior export into game GIFs."""
from PIL import Image
import os

SRC = r'F:\Jogo\assets\chars\human-warrior-pixellab\Human_Warrior'
DST = r'F:\Jogo\assets\chars'

# Idle (8 frames @ 120ms = smooth combat-ready breathing)
IDLE = 'animations/animating-c68c5fc5/east'
idle_frames = [Image.open(os.path.join(SRC, IDLE, f'frame_{i:03d}.png')).convert('RGBA') for i in range(8)]
idle_frames[0].save(
    os.path.join(DST, 'human-warrior-idle.gif'),
    save_all=True,
    append_images=idle_frames[1:],
    duration=120,
    loop=0,
    disposal=2,
    transparency=0,
    optimize=True
)

# Attack (3 frames @ 60ms = 180ms snappy, plays once)
ATTACK = 'animations/jab_attack-234ceb13/east'
atk_frames = [Image.open(os.path.join(SRC, ATTACK, f'frame_{i:03d}.png')).convert('RGBA') for i in range(3)]
atk_frames[0].save(
    os.path.join(DST, 'human-warrior-attack.gif'),
    save_all=True,
    append_images=atk_frames[1:],
    duration=60,
    loop=1,
    disposal=2,
    transparency=0,
    optimize=True
)

# Report sizes
for name in ['human-warrior-idle.gif', 'human-warrior-attack.gif']:
    p = os.path.join(DST, name)
    size = os.path.getsize(p)
    im = Image.open(p)
    print(f'{name}: {im.size[0]}x{im.size[1]}, {size} bytes')
