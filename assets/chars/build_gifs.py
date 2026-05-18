"""Convert PixelLab export into game-ready GIFs.

Takes the elf-knight east-facing frames and produces:
  - elf-knight-idle.gif    : 1-frame loop (PNG works too, but GIF for consistency)
  - elf-knight-attack.gif  : 9-frame animation, ~80ms per frame
"""
from PIL import Image
import os

SRC = r'F:\Jogo\assets\chars\test-elf-knight\I_want_a_elf_knight'
DST = r'F:\Jogo\assets\chars'

# Idle = single static frame (east-facing rotation)
idle = Image.open(os.path.join(SRC, 'rotations', 'east.png')).convert('RGBA')
idle.save(os.path.join(DST, 'elf-knight-idle.gif'),
          save_all=True, disposal=2, transparency=0, optimize=True)

# Attack = 9 frames "wind up arm" loop
ANIM = 'animations/The_character_pulls_their_right_arm_back_to_wind_u-e827c969/east'
frames = []
for i in range(9):
    fp = os.path.join(SRC, ANIM, f'frame_{i:03d}.png')
    im = Image.open(fp).convert('RGBA')
    frames.append(im)

# Save as animated GIF, ~50ms per frame (snappier — full anim ~450ms)
# Plays once and then holds last frame; setFighterAnim reverts to idle anyway.
frames[0].save(os.path.join(DST, 'elf-knight-attack.gif'),
               save_all=True,
               append_images=frames[1:],
               duration=50,
               loop=1,
               disposal=2,
               transparency=0,
               optimize=True)

# Also produce a 2x-upscaled version for crispness on larger displays
def upscale_gif(in_path, out_path, factor=2):
    src = Image.open(in_path)
    out_frames = []
    try:
        while True:
            frame = src.convert('RGBA')
            w, h = frame.size
            out_frames.append(frame.resize((w * factor, h * factor), Image.NEAREST))
            src.seek(src.tell() + 1)
    except EOFError:
        pass
    if not out_frames:
        return
    out_frames[0].save(out_path,
                       save_all=True,
                       append_images=out_frames[1:],
                       duration=src.info.get('duration', 80),
                       loop=0,
                       disposal=2,
                       transparency=0,
                       optimize=True)

print('Idle GIF:', os.path.join(DST, 'elf-knight-idle.gif'))
print('Attack GIF:', os.path.join(DST, 'elf-knight-attack.gif'))
print('Size: 68x68 (PixelLab default)')
print('Done.')
