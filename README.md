# Forge & Blood

A fully idle, turn-based dark-fantasy RPG. Single-file HTML/CSS/JavaScript prototype.

**Play it:** open [`index.html`](./index.html) in a browser, or visit the live build via GitHub Pages once deployed.

## What is it

- 5 races × 3 unique classes each = **15 classes**, every one with its own talent tree (3 tiers, 6 nodes).
- **Zero clicks during combat** — abilities trigger via auto-cast priorities; the player makes decisions *between* fights (allocate stat points, spend talent points, equip gear).
- Hero progresses **level 1 → 100**, gaining **1 stat point** and **1 talent point** per level.
- PvE (7 monsters) + PvP (4 randomly generated opponents).
- 22+ items across 4 slots and 5 rarities with special effects (lifesteal, crit, thorns, burn, execute, etc.).

## Project files

| File | Purpose |
|---|---|
| [`index.html`](./index.html) | The whole game in a single file (~1.9k lines) |
| [`CHANGELOG.md`](./CHANGELOG.md) | Running log of every change — paste into a new chat to resume |
| [`PROJECT-SUMMARY.md`](./PROJECT-SUMMARY.md) | Full design doc (races, classes, combat, roadmap) |
| [`CLAUDE-CODE-STEPS.md`](./CLAUDE-CODE-STEPS.md) | Suggested working order for future sessions |
| `expansion_pack-0.04/` | LPC sprite pack (OpenGameArt, CC-BY-SA) for future combat animations |

## Status

Active prototype. Built iteratively with Claude Code.

## Credits

- Sprite assets in `expansion_pack-0.04/` from the Liberated Pixel Cup expansion by Johannes Sjölund ("wulax"), via [OpenGameArt](https://opengameart.org/).
