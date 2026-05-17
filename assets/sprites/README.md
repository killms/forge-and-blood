# Sprites folder

Drop animated GIFs (or static PNGs) here, then wire them into the data in `index.html`.

## How to use

1. **Drop a file here**, e.g. `goblin.gif`.
2. **Edit `index.html`**, find the entry for that creature in `RACES` or `MONSTER_PORTRAITS`, and add a `sprite` field next to the existing `glyph`/`tint`:

   ```js
   const MONSTER_PORTRAITS = {
     'Goblin Raider': { glyph: '👹', tint: '#5fa85f', sprite: 'assets/sprites/goblin.gif' },
     ...
   };
   ```

   Same for `RACES`:

   ```js
   human: {
     ...
     portrait: { glyph: '⚔', tint: '#c9a557', sprite: 'assets/sprites/human-warrior.gif' },
     ...
   }
   ```

3. **Commit + push** — the new sprite shows up live in 30-60s.

## What works

- **Animated GIFs** — the browser plays them on loop, looks like proper idle animation.
- **Static PNGs** — work too; the CSS idle-bob still gives gentle motion.
- **Animated PNGs (APNG)** and **animated WebP** — also work.
- Any size is OK — the portrait box auto-fits with `object-fit: contain`. 64×64 or 96×96 looks best.

## Fallback behaviour

If a sprite path is set but the file is missing, the browser shows a broken-image icon. Either fix the path or remove the `sprite` field — the emoji glyph comes back automatically.

## Where to find sprites (free / CC0 / CC-BY)

- **OpenGameArt** — https://opengameart.org (filter by license CC0 or CC-BY)
  - The "animated imp" you found is at `/files/<filename>` not `/styles/medium/public/<filename>` — that path is the thumbnail.
- **itch.io** — free pixel art packs, search "free pixel art enemies" or "RPG hero pack"
- **Kenney.nl** — CC0 game assets
- **Sketchfab** (browse 2D section) — some CC0

## Crediting authors

When you use CC-BY assets, add a line at the bottom of the project `README.md` with the author and link, e.g.:

```
"Animated Imp" by [author] (CC-BY 3.0) — https://opengameart.org/content/...
```

CC0 doesn't require credit but it's polite to mention the source.

## Suggested filenames

Match the data keys roughly so they're easy to find:

```
assets/sprites/
  human.gif        → RACES.human
  elf.gif          → RACES.elf
  orc.gif          → RACES.orc
  dwarf.gif        → RACES.dwarf
  shifter.gif      → RACES.shifter

  giant-rat.gif    → MONSTER_PORTRAITS['Giant Rat']
  goblin.gif       → MONSTER_PORTRAITS['Goblin Raider']
  ash-wolf.gif     → MONSTER_PORTRAITS['Ash Wolf']
  skeleton.gif     → MONSTER_PORTRAITS['Skeleton Warrior']
  cave-ogre.gif    → MONSTER_PORTRAITS['Cave Ogre']
  lich.gif         → MONSTER_PORTRAITS['Awakened Lich']
  dragon.gif       → MONSTER_PORTRAITS['Young Dragon']
```

## A bigger plan if you want full coverage

There are 5 races but **15 classes**. If you want per-class sprites (Knight ≠ Cleric ≠ Bounty Hunter even though both are Human), the cleanest approach is to add a `portrait` field on each class in `CLASSES`, mirror the RACES structure, and have `setPortrait` prefer class portrait over race portrait. Ask Claude to wire that up.
