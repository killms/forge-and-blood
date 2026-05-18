# Forge & Blood — Changelog

> Running log of every meaningful change. **Newest at the top.** A future Claude reading this should understand the current state of the project without having to read the full source.
>
> When continuing in a new chat, paste this file in and say "read this, then read `index.html`, then we'll continue."

---

## Session 18 — 2026-05-18 — Sub-classes / Specs (build depth)

### What's new
Each of the 15 classes now has **2 specialisations** that unlock at **level 15**. Pick one — permanent — to define your build. 15 × 2 = **30 specs**, and a Knight Templar plays very differently from a Knight Sentinel.

### Examples
- **Knight** → Templar (+10 Melee, +5 Life, +10% crit) **OR** Sentinel (+10 Def, +5 Life, Oath upgrades to Fortify-tier block).
- **Cleric** → Light (+5 Magic, +5 Life, regen 10/turn override) **OR** Wrath (+12 Magic, +10% crit).
- **Berserker** → Bloodlord (+12 Melee, lifesteal 15%) **OR** Undying (+10 Life, regen 6, savior).
- **Chaos Shifter** → Lord of Chaos (mutate +4) **OR** Order in Chaos (+5 to all + doubleMutate).
- … (full list in `CLASS_SPECS` const).

### How they work
Specs grant the same kinds of bonuses talents do:
- Direct stat bonuses (`atk`, `def`, `vit`, `agi`, `int`).
- Passive numeric bonuses (`critBonus`, `regen`, `dmgReduce`, `lifesteal`, `savior`, `doubleMutate`).
- Optional **`passiveOverride`** that swaps the class's base passive proc (e.g. Sentinel upgrades Oath to 25% block / 70% reduction; Light upgrades Blessing regen from 4 to 10).

All processing fits into the existing `recalculate` and `getAllPassiveBonuses` flow — no new combat code needed.

### State + migration
- `state.hero.specKey` (null until chosen).
- `migrateHero` injects `specKey: null` on older saves.

### UI
- New **Specialisation** panel at the top of the Talents tab:
  - **Locked**: shows lock icon, "Unlocks at level 15", names the two future options.
  - **Available**: both spec cards highlighted green, clickable. Pick triggers a `confirm()` (permanent choice).
  - **Picked**: chosen card gold-glowing with ✓; the other greyed and unclickable.
- The Talents-tab badge (`X to choose`) now also counts the spec as a pending pick if unlocked but not chosen.
- Hero tab Class Abilities panel shows:
  - **Spec available** (pulsing green) if unlocked but not picked.
  - **Spec chosen** (gold-bordered) describing your spec when picked.

### Notifications
- New toast when the player crosses level 15: "Specialisation available! Visit the Talents tab to choose your path."
- Picking a spec fires an "achievement" toast naming the choice.

### Files touched
- `index.html` only.

---

## Session 17 — 2026-05-18 — Visual polish pack (SVG icons, card depth, typography, tab animations)

### Inline SVG icon library
- 14 hand-drawn SVG symbols in a single `<svg>` block at the top of `<body>`: coin, heart, droplet, star, sword, magic, shield, boot, bag, skull, map, crown, flame, trophy.
- All use `currentColor` so they inherit the surrounding text colour — gold next to a gold number, blue next to MP, etc.
- New `.icon` utility class (14×14px, vertically centred). Variants: `.icon-lg` (18px), `.icon-xl` (24px).
- Icons applied:
  - **Gold display** (hero header): coin icon next to the number.
  - **HP bar text**: heart icon.
  - **MP bar text**: droplet icon.
  - **Level badge** (XP panel): star icon.
  - **Tabs** (HERO/TALENTS/BAG/SHOP/HUNT/ARENA): each tab now stacks an icon above its label (shield/star/bag/coin/map/sword).
- Active tab pulses its icon slightly and adds a gold drop shadow underneath.

### Card depth
- All `.panel` elements get:
  - Subtle vertical gradient (lighter on top, deeper on bottom).
  - Inset highlight on the top edge (gold tinge) + inset shadow on the bottom edge (black).
  - Drop shadow (`0 4px 10px rgba(0,0,0,0.45)`) — panels visibly sit above the background.
  - Bottom-edge gold sparkle line (`::after` rule) matching the existing top-edge gold line.
- Net effect: panels feel like raised wood-and-iron boards instead of flat rectangles.

### Typography hierarchy
- **Hero name** bumped 18px → 22px, weight 700, with gold text-shadow.
- **Gold display** bumped to 17px bold with gold glow.
- **Bar texts** (HP / MP) bumped to 13px / weight 700 — much more legible against the bar fill.
- Hero meta line gets a small top margin to breathe.

### Tab transitions
- When a tab becomes visible, its child panels animate `panel-slide-in` (10px translate + opacity fade) over 320ms with staggered delays per panel (40ms increments). The tab feels alive instead of snapping into place.

### Files touched
- `index.html` only.

---

## Session 16 — 2026-05-18 — Big content pass: monsters, biomes, events, sets, achievements, toasts, tooltips

### New content

**6 new monsters with abilities** (now 13 total):
- *Burning Wastes*: Fire Imp (tier 3, magical+melee), Lava Hound (tier 5, melee+dot), Salamander King (tier 8, fire mage)
- *Frozen Spires*: Frost Wolf (tier 4, melee+slow), Ice Wraith (tier 6, magical+drain), Glacial Golem (tier 9, tank+armor)
- 7 new monster abilities: ember_dart, fire_bite, molten_strike, icy_bite, frost_bolt, chilling_touch, ice_armor.

**2 new expeditions** (now 5 total):
- *The Burning Wastes* (Lv 25+, 7 nodes, boss: Salamander King) — fire biome
- *The Frozen Spires* (Lv 40+, 8 nodes, boss: Glacial Golem) — ice biome

**12 new events** (now 16 in pool):
mysterious-merchant, lone-grave, gambling-cultist, training-dummy, ambush, oasis, broken-altar, wandering-bard, ancient-statue, forgotten-cache, lost-pilgrim, plus the original 4.

**4 item sets with bonuses**:
- *Iron Guard*: Iron Helm + Ring Mail + Chain Greaves (2pc → +DEF/VIT, 3pc → +DEF/VIT/ATK)
- *Ranger's Wind*: Wolf Leathers + Wind Boots + Hunter's Dagger (AGI + ATK)
- *Arcane Mastery*: Initiate Robes + Crown of Knowledge + Pendant of Wisdom + Initiate Staff (INT-focused, scales 2→3→4 pieces)
- *Vampyric Pact*: Berserker's Axe + Necromancer's Cloak + Eye of the Beholder (ATK + VIT + INT)
- Set status shown under the Equipment grid: `Iron Guard · 2/3 — +4 Defense, +3 Life`.

### Achievements (~20)
- New `state.hero.tracking` object: monstersKilled, bossesKilled, bossesByName, expeditionsCompleted, itemsByRarity, totalGoldEarned, unlockedAchievements.
- Achievement categories: Combat (Slayer I-IV, Reaper), Bosses (Boss Hunter, Wide Hunter), Levels (Apprentice/Veteran/Champion/Legendary at L10/25/50/100), Expeditions (Explorer/Pathfinder), Loot (Lucky/Treasure Hunter/Mythbreaker for rare/epic/legendary), Wealth (Coin Stack, Wealthy), Misc (Talented).
- Rewards are **permanent stat bonuses** (applied in `recalculate` via `getAchievementBonusStats`) or **one-time gold** (`goldOnce`).
- `checkAchievements()` runs after key events (finishVictory, finishExpedition) — newly unlocked ones fire a toast.
- Migration: `ensureTracking(hero)` backfills the tracking object on load for older saves.

### Toast notification system
- Fixed top-of-screen stack with z-index 2000.
- Three flavours: `achievement` (gold glow), `levelup` (blue glow), `loot` (purple glow).
- Auto-dismisses after ~4s. Slide-in / fade-out animations.
- Fired on: level up, rare+ loot drop, achievement unlock, expedition complete.

### Tooltips
- Native `title` tooltips on the Hero attribute rows explaining what each stat does:
  - Melee dmg → "Scales melee (non-magical) ability damage. Items with +Melee boost this."
  - Magic dmg → "Scales magical ability damage. Also adds to max mana. Useless for melee classes."
  - Defense → "Reduces incoming damage. Half of your Life is added here too."
  - Life → "Max HP = Life × 5 + 20. Each point also gives +0.5 Defense."
  - Agility → "Determines turn order. Also +0.5% crit and +0.3% dodge per point."
- Future: richer custom tooltips on talent nodes / items / abilities (deferred).

### Deferred for future sessions
- **Sub-classes / specs** (rework of class system, big design work).
- **Daily quests** (needs real-time scheduling + reset logic).
- **Full sprite-animated monsters** for the new biomes (needs art acquisition).
- **Rich custom tooltips** beyond native title attribute.

### Files touched
- `index.html` only.

---

## Session 15 — 2026-05-18 — Kenney assets ingested (vistas + future 3D)

### What the user did
Dropped 3 Kenney packs at the repo root:
- **Mini Dungeon** (3D, ~4MB) — dungeon tiles + characters
- **Fantasy Town** (3D, ~12MB) — buildings, props, scenery
- **UI Pack RPG Expansion** (2D, ~434KB) — buttons, panels, icons, bars

### What was done this session
- **Cleanup**: removed orphan duplicates that ended up at the repo root from re-extractions (loose `Models/`, `PNG/`, `Spritesheet/`, `Vector/`, `Previews/`, `Overview.html`, etc.).
- **Reorganised** into clean paths:
  - `assets/town/` (from Fantasy Town)
  - `assets/dungeon/` (from Mini Dungeon)
  - `assets/ui/` (from UI pack)
- **Vistas wired in**: each pack's `Preview (Variation A).png` was copied to a simple-named `vista.png` and used as a decorative header:
  - `assets/town/vista.png` → Hero tab header
  - `assets/dungeon/vista.png` → Hunt tab (expedition list view only — not during an active expedition)
- CSS treatment on `.vista`: 130px tall, `cover` background, vignette + bottom gradient to dark, slight desaturation. Blends with the dark fantasy theme.
- Credits added in `README.md` (Kenney packs are CC0, no attribution required, but noted anyway).

### What was DEFERRED (and why)
- **UI pack integration** — the Kenney UI style is medieval-parchment / wood / earthy tones. The game's current aesthetic is dark fantasy gold/blood (closer to Diablo / Darkest Dungeon). Mixing would look incoherent. Two viable paths for later:
  - Use only specific brown-toned UI elements (buttonLong_brown, buttonSquare_brown) that match the gold accents.
  - Fully commit to the Kenney aesthetic and redo the CSS theme. Bigger work.
- **3D scenes** — the GLB models in both packs are unused. Path forward:
  - Add Three.js (~150KB) and render the town as a rotating scene on the Hero tab.
  - Render the dungeon as a 3D mini-map per expedition. ~2-3 sessions of work, ~16MB of assets actually loaded.

### Files touched
- `index.html` — vista markup + CSS
- `README.md` — credits
- New: `assets/town/`, `assets/dungeon/`, `assets/ui/` (full packs committed for future use)

### Repo size note
The new packs add ~16MB to the repo. GitHub Pages serves them on demand — the page only loads the two `vista.png` files (~1MB total). The rest sits ready for when we wire up 3D or fuller UI.

---

## Session 14 — 2026-05-18 — Visual expedition map (Slay-the-Spire style)

### What changed
The Hunt tab's active expedition no longer reveals encounters one at a time. The full path is **pre-generated and shown upfront** as a vertical map:

```
  [ ⚔ Goblin ] [ 💰 Chest ]   ← layer 1: tap one
       ▼
  [ ✦ Event ] [ ⚔ Wolf ]    ← layer 2 (locked until you finish layer 1)
       ▼
  [ ⚔ Ogre ] [ 💰 Chest ]   ← layer 3
       ▼
      [ 🔥 Boss ]            ← final
```

- Each layer has **2 options**; the boss layer has 1.
- Current layer pulses gold; future layers are dimmed and locked; past layers show ✓ on the picked node and grey out the unpicked one.
- Tap a node → that becomes your pending encounter; the resolution card appears below the map (FIGHT / OPEN / event choices).
- Once you've picked, the layer is treated as past — you can't undo or pick the alternative.

### Code
- New `generateNode(def)` and `generateExpeditionMap(def)` produce a serialisable structure (node types reference IDs like `monsterName` / `eventKey`, never functions).
- `state.expedition` schema:
  ```js
  {
    key, name, glyph, tint,
    map: [[node, node], ..., [bossNode]],
    currentLayer: 0,
    path: [],   // option index picked at each completed layer
    pending: null,
    pendingResolved, pendingResult, pendingLootRarity,
    gold, xp, monstersSlain, loot, finished, _awaitingCombat
  }
  ```
- New `expeditionPickNode(optionIdx)` snapshots the chosen node into `pending`.
- Encounter resolution uses `EXPEDITION_EVENTS.find(e => e.key === pending.eventKey)` — looks up the function at resolve time (functions never get serialised).
- Layer-state classes: `.current` (gold pulse, clickable), `.past` (✓ on picked, faded on unpicked), `.future` (locked, dimmed + grayscale).
- Boss layer styled larger with a permanent orange glow.

### Migration
- Old expedition state (no `map` field) gets cleared at load time. Existing players in mid-expedition will see the expedition list again — they didn't lose anything else (gold/loot/level all stay on the hero).

### Files touched
- `index.html` only.

---

## Session 13 — 2026-05-18 — Sell-all + damage school indicator

### Sell all (Bag)
- New `SELL ALL (N) — X ◊` banner at the top of the inventory list.
- Click → `window.confirm` with the count and total → if confirmed, all items in the bag are sold and the gold added at once.
- Equipped gear is **never** touched (only `state.hero.inventory` is cleared).
- Button hidden when bag is empty.

### Damage school indicator (Hero tab)
- New chip in the "Class Abilities" panel, just above the existing class/race passives:
  - **Magic classes** (Cleric, Druid, Shaman, Stone Priest, Chaos Shifter): blue chip — *"Spell caster — scales with Magic (INT). Active abilities cost mana."*
  - **Other classes**: red chip — *"Melee striker — scales with Melee (ATK). Some talents can still be magical."*
- Driven by the existing `MAGICAL_CLASSES` set; no data changes.

### Why this matters
The Melee/Magic split is enforced in `doDamage`:
- Magical abilities scale damage from **INT** instead of **ATK**.
- Magical abilities cost mana from the INT-driven pool.
- All other math (defense, AGI crits/dodge) is unchanged.

For a pure-melee class (Knight, Berserker, Stalker, Bear, etc.) most active abilities are non-magical → INT does almost nothing. For magic classes, INT is the primary damage stat. The new chip makes that obvious at character creation.

### Files touched
- `index.html` only.

---

## Session 12 — 2026-05-18 — Melee/Magic split + Expeditions (dynamic Hunt)

### Part A — Melee / Magic damage split (presentation)
- New `STAT_LABELS` map: `atk → Melee · int → Magic · def → Defense · vit → Life · agi → Agility`.
- `statLabel(key)` helper used in:
  - Hero **Attributes** grid: now reads `Melee dmg · Magic dmg · Defense · Life · Agility`.
  - Inventory item stat lines: `+5 Melee` / `+3 Magic` instead of `+5 ATK` / `+3 INT`.
  - Equipment slot picker + compare modal.
  - Compare deltas table — also now includes INT row.
  - Shifter mutate log entry (`Caos mutates: +2 Melee`).
- Combat math unchanged. INT keeps driving magical ability damage and the mana pool; ATK keeps driving melee damage.

### Part B — Expeditions (dynamic Hunt)
The Hunt tab is no longer a flat list of monsters. It now offers **expeditions** — multi-encounter runs with branching outcomes.

#### Three starter expeditions
- **The Whispering Woods** — Lv 1+, 5 nodes, boss: Cave Ogre. Pool: Giant Rat / Goblin Raider / Ash Wolf.
- **The Cursed Crypt** — Lv 5+, 6 nodes, boss: Awakened Lich. Pool: Skeleton Warrior / Ash Wolf / Awakened Lich.
- **The Dragon's Lair** — Lv 15+, 7 nodes, boss: Young Dragon. Pool: Skeleton Warrior / Cave Ogre / Awakened Lich.

#### Encounter types per node
- **Combat** (default) — random monster from the expedition's pool, scaled to hero level.
- **Treasure** — chance to open a chest for gold + (70%) a random item rolled with `rollLootByLevel`. Chance configurable per expedition (15-30%).
- **Event** — text-based choice with branching outcomes. Four event cards in the pool (Hooded Stranger, Wounded Traveller, Glittering Pool, Old Shrine), drawn at random. Choices have effects: gold cost / gain / heal / damage / XP, plus narrative text.
- **Boss** — always the last node. +25% atk/def, +50% vit, 2× gold, 2× XP. Defeating it completes the expedition.

#### UI
- Hunt tab opens with three **expedition cards** + a collapsible "direct hunt" `<details>` for one-off fights (original behaviour preserved).
- Active expedition shows: icon, name, "Node X of Y" progress, animated progress bar, current encounter card, and a running summary footer (gold / XP / slain / loot).
- Encounter cards have themed colours (boss = blood-red border, resolved = green tint).
- Result panels for treasures get a rarity-coloured border.

#### State + flow
- `state.expedition` holds the active run; persists in localStorage so refreshing keeps you in the run.
- `closeCombat` checks `expedition._awaitingCombat` and either advances the node (victory) or ends the expedition (defeat). Rewards earned along the way stay on the hero either way.
- Boss victory triggers a "EXPEDITION COMPLETE" screen with a single RETURN HOME button.
- "LEAVE EXPEDITION" button on any encounter lets the player exit voluntarily and keep all earned rewards.

### Migration
- `state.expedition` defaults to `null`. Loaded from `accounts[user].expedition`. Saved on every save. Cleared on logout.

### Files touched
- `index.html` only.

---

## Session 11 — 2026-05-18 — Per-action sprite swapping (attack / hurt / dead)

### What changed
- The portrait data structure now supports **multiple animation states** per character. Each portrait can carry a `sprites` object:
  ```js
  'Goblin Raider': {
    glyph: '👹', tint: '#5fa85f',
    sprites: {
      idle:   'assets/sprites/imp-sword-idle.gif',
      attack: 'assets/sprites/imp-sword-attack.gif'
      // hurt, dead optional — fall back to idle
    }
  }
  ```
- The old `sprite: 'X'` (single-string) format **still works** — treated as idle only. No data migration needed.
- During combat, sprites swap based on what's happening:
  - **Attacker → 'attack'** when they hit. Reverts to 'idle' ~480ms later.
  - **Defender → 'hurt'** when they take damage. Reverts to 'idle' ~320ms later. (Falls back to idle if no hurt sprite exists.)
  - **Defender → 'dead'** when killed. CSS death-fall takes over after.
- Multi-hit abilities (Flurry, Volley, Storm of Arrows) keep the attack pose going across hits — each new hit pushes the revert-to-idle timer forward instead of triggering a flicker.
- Each swap appends a cache-busting `?_=<timestamp>` so the GIF restarts from frame 0 cleanly.

### Code
- New `resolvePortrait(source, isHero)` extracted from `setPortrait` — reused by `buildFighter` to cache `portraitData` on the fighter object.
- New `spriteFor(portrait, state)` — picks the right URL with a fallback chain (state → idle → null).
- New `setFighterAnim(fighter, state)` — low-level swap.
- New `playAttackAnim(fighter, ms)` / `playHurtAnim(fighter, ms)` — high-level wrappers that schedule the revert and cancel previous reverts on consecutive calls.

### Wired to Goblin Raider (LPC imp)
- `imp-sword-idle.gif` for idle (already in repo from session 10).
- `imp-sword-attack.gif` now also wired — fires on each hit the goblin deals.
- LPC walk + attack packs don't include hurt or die frames, so those states fall back to idle. CSS death-fall handles dying visually.

### How to add more
For any monster (or race) you want per-action animation:
1. Drop the sprite files in `assets/sprites/`.
2. Edit the entry in `MONSTER_PORTRAITS` or `RACES.*.portrait`, replace `sprite: 'X'` with `sprites: { idle, attack, hurt?, dead? }`.
3. `git push` — live in ~1 min.

### Files touched
- `index.html`.

---

## Session 10 — 2026-05-18 — LPC imp sprite wired to Goblin Raider

### What happened
- User shared the LPC imp ZIP from OpenGameArt (`LPC%20imp_0.zip`). The pack contains 10 PNG sprite sheets (256×256, 4 directions × 4 frames each, 64×64 per frame) covering walk + attack with vanilla / pitchfork / sword / sword+shield variants.
- LPC sheets aren't animated GIFs — they're static PNGs with frames laid out in a grid. So I ran a small Python/Pillow script to extract the "facing down" row (row 2 in LPC convention: up/left/down/right) and stitch the frames into proper animated GIFs.
- Output dropped into `assets/sprites/`:
  - `imp-idle.gif` (4 frames @ 200ms — walking-down loop reused as idle for the vanilla imp)
  - `imp-sword-idle.gif` (same but holding sword + shield)
  - `imp-sword-attack.gif` (4 attack frames @ 120ms)
- **Wired** `imp-sword-idle.gif` to `MONSTER_PORTRAITS['Goblin Raider']` — small adversary slot fits the imp's vibe. Goblin keeps the same name; only the visual changed.
- Credit added in the main `README.md` pointing back to OpenGameArt's LPC imp page (CC-BY-SA 3.0 / GPL 3.0 — typical LPC licence).

### Notes
- If the "facing down" row turns out to be the wrong direction visually (some LPC packs differ), it's a one-line tweak: change `row=2` to `0/1/3` in the Python script and re-run.
- Same conversion pattern works for any LPC pack the user wants to add. Steps: drop the ZIP path on Claude, pick which monster slot, done.
- For per-class hero sprites we'd need much more art (15 classes × idle/attack/die). The infrastructure already supports it — just needs the source files.

### Files touched
- `index.html` — single line in `MONSTER_PORTRAITS`.
- `README.md` — credit line.
- `assets/sprites/` — 3 new GIFs.

---

## Session 9 — 2026-05-18 — Sprite GIF support (optional, falls back to emoji)

### Goal
- Make it trivial to swap the emoji portraits for real animated GIFs (OpenGameArt, itch.io, etc.) without touching combat code.

### Implementation
- `portrait` data (in `RACES` and `MONSTER_PORTRAITS`) now accepts an optional `sprite` path alongside the existing `glyph` + `tint`. Example:
  ```js
  'Goblin Raider': { glyph: '👹', tint: '#5fa85f', sprite: 'assets/sprites/goblin.gif' }
  ```
- `setPortrait()` checks for `sprite` first — if present, renders `<img src="...">`; otherwise renders the emoji glyph as before.
- The portrait box grew from 80×80 → 96×96 with `overflow: hidden` and inner `img { object-fit: contain; image-rendering: pixelated; }` so any sprite size shows up crisp.
- All existing animations (idle-bob, shake, lunge, slash, cast glow, death-fall, hit-flash) **still apply** because they target the parent `.fighter` / `.fighter-portrait` — they don't care whether the content is text or an `<img>`.

### New folder
- `assets/sprites/` with a `README.md` that explains:
  - How to drop a file and wire the data
  - Where to source free assets (OpenGameArt, itch.io, Kenney.nl)
  - Suggested filenames matching the data keys
  - The OpenGameArt URL gotcha: `/styles/medium/public/<file>` is a thumbnail; the real download is at `/files/<file>`
  - How to upgrade to per-class portraits later if 5 race sprites isn't enough

### What this DOESN'T do
- No sprites bundled — the user supplies them. Until that happens, every fighter keeps its emoji portrait.
- No sprite-sheet animation (LPC-style frame switching by action). GIFs animate themselves on loop; the per-action effects are still CSS on top. Sprite-sheet support would be a separate session.

### Files touched
- `index.html` (CSS + `setPortrait` rewrite)
- `assets/sprites/README.md` (new)

---

## Session 8 — 2026-05-18 — Animated emoji "bonecos" (Tier 3 lite)

### What you'll see
- **Idle bob** — both fighter portraits gently rise/fall continuously while alive.
- **Hit flash** — defender's portrait background flashes red during the shake (much more readable on emoji than the previous hue-rotate).
- **Slash overlay** — short diagonal gold streak appears across the defender on every hit, with random angle jitter so consecutive hits don't look identical. Variants: **gold** (normal), **white-gold** (crit), **blue** (magical).
- **Cast glow** — magical abilities trigger a 0.7s scale-up + blue glow on the caster *before* damage resolves (windup feels like a real spell).
- **Death animation** — when a fighter hits 0 HP, the portrait rotates left, slumps down, fades to grey. Fires on basic hits, ability hits, DoT ticks, thorns, and turret damage. Savior keeps the fighter alive at 1 HP so the animation correctly doesn't fire.
- **Lunge upgraded** — attacker now also scales up by 6% during the dash (felt flat before).
- **Hit / crit shake** — sharper, with rotation. Crits add gold drop-shadow glow.

### Implementation
- All pure CSS keyframes + tiny JS helpers. No external assets, no sprite sheets, no asset downloads.
- New helpers: `spawnSlashFx(defender, kind)`, `playDeathAnimation(fighter)`, `playCastAnimation(attacker)`.
- `startCombat` resets all per-combat animation classes (`dead`, `casting`, `shake`, etc.) so the next fight starts clean.

### Why this approach
- Sprite sheets (LPC pack we already have) would need an asset acquisition pass — base bodies for each race, classes-as-clothing layers, monster sheets, attack/death frame animations. Roughly 30-50 hours of asset work.
- Animated emoji portraits give ~70% of the "juice" feeling for 1 session of CSS.
- The combat code structure (async/await with sleep at every step) accepts proper sprite animations later with the same hook points — no refactor needed.

### Files touched
- `index.html` only.

---

## Session 7 — 2026-05-18 — Combat animations (Tier 1 + 2)

### Goal
- Make combat feel alive without needing external assets. CSS-only animations + emoji-based portraits keyed to race/monster.

### Portraits
- Each `RACES[*]` now has a `portrait: { glyph, tint }`. Tints used: human gold, elf green, orc red, dwarf stone, shifter purple.
- New `MONSTER_PORTRAITS` map: rat 🐀, goblin 👹, ash wolf 🐺, skeleton 💀, ogre 👺, lich ☠, dragon 🐉.
- `setPortrait()` paints the fighter's 80×80 box with the glyph, tinted border, and inner shadow.
- PvP opponents use their race's portrait too.

### Floating combat numbers (`spawnFloater`)
- Rises above the fighter, scales up, then fades. Coloured by type:
  - **damage** (red, large)
  - **crit** (gold, extra-large with glow)
  - **heal** (green)
  - **miss** / **dodge** (grey/blue, italic)
  - **block** (blue)
  - **dot** (orange)
- Small horizontal jitter so stacked hits don't perfectly overlap.

### Fighter shake / lunge
- `shakeFighter(fighter, kind)` — `hit` (short red shake), `crit` (longer, gold-glow shake), `heal` (green pulse on portrait).
- `lungeFighter(fighter)` — attacker briefly translates toward the opponent on every hit / miss / dodge.

### HP bar pulse
- HP fill gains `.hp-low` class when below 25% (animated pulse + drop-shadow).

### Hooks
- `doDamage`: floater + shake on defender, lunge attacker. Lifesteal / druid heal / devour heal → heal floater on attacker. Thorns → damage floater on attacker. Miss / dodge / block → their own floaters.
- `executeAbility` heal → heal floater + portrait pulse.
- `tickStartOfTurn` regen / class regen → heal floater. DoT ticks → orange damage floater + shake. Turret hits → red floater on opponent.

### Architecture note
The async/await combat loop already paced everything with `await sleep(N)`. Adding animation hooks at each step was a single line per event, no refactor needed. Tier 3+ (per-ability VFX, sprite sheets) plugs in the same way later.

### Files touched
- `index.html` only. (Still 100% CSS — no external assets required.)

---

## Session 6 — 2026-05-18 — Combat summary + slot picker + shop + sell

### Combat ends with a summary, not auto-close
- `_combatStats` tracks per-fighter metrics during the fight: damage dealt, damage taken, crits, blocks, dodges, healing, abilities used, mp spent.
- After the last action, the combat panel now shows a **summary** instead of closing automatically:
  - Verdict line (VICTORY / DEFEAT / DRAW)
  - "X vs Y · N turns" meta
  - **Performance table**: hero vs foe columns for all 7-8 metrics
  - **Rewards table**: gold, XP, level changes, talent tier unlocks, loot drop (or "No rewards" on loss/draw)
  - **CONCLUDE** button — player clicks when ready, no time limit

### Slot picker — click any equipped slot to browse compatible gear
- Old behaviour (click equipped slot → instant unequip) replaced.
- Clicking a slot in either the Hero or Bag tab now opens a modal showing:
  - The currently equipped item with an **UNEQUIP** button
  - All inventory items that fit that slot, sorted by rarity (best first) then total stat sum
- Clicking an inventory item from the picker opens the existing compare modal — for ring1/ring2 the picker forces the right slot so the user picks for exactly the ring they tapped.

### Sell gear for gold
- New **SELL FOR X ◊** button inside the compare modal. Prices by rarity:
  - common 5 · uncommon 15 · rare 40 · epic 120 · legendary 400
- The CANCEL / EQUIP / SELL trio is now a 3-row stack of buttons; the ring 3-column variant has all four.

### Shop tab
- New tab between BAG and HUNT. Single offer for now: **Sealed Crate**.
- Crate price: `50 + level * 8` gold. Opens to one random item from `rollLootByLevel(hero.level)` (same scaling as combat loot).
- Buy button disabled when gold is insufficient. After purchase, the new item is logged in a result strip below the offer.
- Loot stays generic (no per-class filtering — explicit user pref).

### Files touched
- `index.html` only.

### Known follow-ups
- Multiple shop offers (tiered crates, single-rarity boxes) would slot in cleanly — the offer container is already a list.
- Sell from inventory directly (without opening compare) is a one-liner if the user wants it; currently the only entry is via the compare modal.

---

## Session 5 — 2026-05-18 — INT items + visible rarity borders

### Caster gear (32 new items)
Added INT-bearing items across every slot and rarity tier:
- **Weapons (6)**: Apprentice Wand → Lich's Phylactery (common→legendary). High-INT weapons make Cleric/Druid/Shaman/etc. far stronger.
- **Helms (5)**: Hood of Insight → Halo of Stars.
- **Amulets (5)**: Pendant of Wisdom → Soul of the Archmage.
- **Rings (5)**: Sigil Ring → Crown of the Archon.
- **Vests (5)**: Apprentice Robes → Robes of the Archmage.
- **Pants (5)**: Mage Trousers → Pants of the Archmage.

Many carry INT + secondary stats (def/vit/atk) and effects (burn, crit, regen, dodge, lifesteal).

### Rarity colours now visible at a glance
- Items used to only show colour on the name. Now the entire **inventory card**, **equipment slot** (when filled), and **compare modal cell** all get a coloured border based on rarity:
  - Common: subtle grey
  - Uncommon: green
  - Rare: blue (+ soft glow)
  - Epic: purple (stronger glow)
  - Legendary: orange (animated pulse)
- New CSS classes `.rarity-common` / `.rarity-uncommon` / `.rarity-rare` / `.rarity-epic` / `.rarity-legendary` applied alongside existing `.r-*` name colours.

### Loot
- Drops stay **random/global** (no per-class filtering — user explicitly said "o loot nao quero por class").

### Files touched
- `index.html` only.

---

## Session 4 — 2026-05-18 — HP refill + monster scaling + enemy AI + Phase C (INT, mana, magical)

### Fixes
- **HP / MP refills to 100% after every fight** (win, lose, draw). Combat is the loop — downtime between fights doesn't exist any more.

### Monsters scale with hero level
- `MONSTERS` table reshaped: each entry has a `tier` (1-10) and base stats. `scaleMonster(template, heroLevel)` computes effective level = `max(tier, heroLevel - (10 - tier))` and applies `+18% stats per level` over the tier. Easier-tier creatures stay easier; the dragon stays the toughest; everything stays relevant past level 10.
- Gold and XP rewards scale with effective level.

### Enemy AI uses abilities (PvE + PvP)
- New `MONSTER_ABILITIES` table: per-monster ability sets (e.g. Ogre has `smash` + `roar_fear`; Lich has `arcane_bolt`, `curse`, `drain_life`; Dragon has `fire_breath`, `tail_swipe`, `dragon_roar`).
- `buildFighter` for non-heroes now installs `abilities`: from monster's template for PvE, or resolved from PvP opponent's random `talentPicks` from their class talent tree.
- PvP generation: each opponent rolls one talent per unlocked tier (random A/B); both passive bonuses (stats/regen/crit/etc.) and active abilities get applied to their fighter.
- `takeAction` now lets BOTH heroes and AI fighters use `chooseAbility`.

### Phase C — Intellect + Mana + Magical damage
- **New stat: INT (Intellect)**. Added to `hero.base.int`, scales magical damage, and grows mana pool.
- **Mana pool**: `maxMp = INT * 3 + 20`. Regen +5/turn (silent — no log spam). Magical abilities consume mana with a cost scaled to the ability's power. If MP is too low, the ability is skipped (basic attack fallback).
- **Magical detection**: `isTalentMagical(talent, attackerClass)` — explicit `school: 'magical'` / `ability.magical` / `trueDmg` / `heal` / `cleanse` count, plus everything from magical-leaning classes (Cleric, Druid, Shaman, Stone Priest, Chaos Shifter).
- **Damage formula**: magical attacks scale from INT (`baseAtk = attacker.int`); melee from ATK (Strength). Falls back to ATK if INT is 0 so non-mages aren't crippled.
- **AGI bonuses**: every point of Agility now also gives **+0.5% crit** and **+0.3% dodge** (applied at fighter build time, applies to both heroes and AI).
- **LIFE bonus**: Vitality now contributes `+0.5 DEF per point` (folded into the user-facing "Life = HP + defense" model). Existing items/talents that grant DEF still stack as raw armor.
- **Stat point allocation**: INT is the 5th option in the attribute panel (`+` button works on it).
- **Class base INT** added: Cleric 12, Shaman 11, Druid 10, Priest 10, Chaos 10 (magic-focused) · Devourer/Engineer 6 (hybrid) · Stalker/Archer/Hunter 3-4 · pure melee 2-3.

### UI
- HP and MP bars in the Hero panel header. MP bar auto-hides for heroes with no Intellect / no mana pool.
- Attribute panel relabeled: **Strength** (atk), **Agility** (agi), **Intellect** (int — new), **Life** (vit), **Defense** (def).
- Magical abilities are marked in combat log with a `✦` next to the name (`X uses Smite ✦!`).

### Migration
- Older saves get `hero.base.int` injected (uses class's `baseInt` if set, else 5).
- `maxMp` / `mp` initialised to 0 then recomputed on first `recalculate()`.
- All existing fighters, items, classes still work — no item/class data needed to change for Phase C beyond adding INT.

### Files touched
- `index.html` only.

### Known follow-ups
- Items don't roll INT in the current pool — could add a few INT-focused items (caster gear) in a follow-up.
- The Defense row is still shown on the Hero tab; if the user wants to fully hide DEF and merge into Life visually, that's a small UI tweak.
- `app.css` doesn't exist (single file) but if we ever modularise we'll move the `bar-fill.mp` style there.

---

## Session 3 (continued) — 2026-05-18 — Phase 3: talent tree rework (300 talents)

### Goal
- Replace the 6-talent-per-class system with a proper branching tree: **10 tiers × 2 mutually exclusive options = 20 talents per class × 15 classes = 300 total talents**.
- No "talent points" — choice happens automatically when a tier unlocks at a specific character level. The unchosen option is permanently locked out.

### Tier unlock levels
`TIER_UNLOCKS = [1, 3, 6, 10, 15, 22, 32, 45, 60, 80]` — front-loaded so the early game feels rich, then milestone choices later.

### Data structure
- `class.talents: [...]` (flat list) → `class.talentTree: [[opt1a, opt1b], [opt2a, opt2b], ...]` (array of tier pairs).
- `hero.talentPicks: { tier: talentKey }` replaces `hero.unlockedTalents` + `hero.talentPoints`.

### Refactor
- `getPickedTalents()` resolves picks to full talent objects via the current class's tree.
- `getActiveAbilities()`, `getAllPassiveBonuses()`, and `recalculate()` all rewritten to use the picks.
- `pickTalent(tier, key)` enforces: tier unlocked, no existing pick, valid option.
- `migrateHero()` clears legacy `unlockedTalents` / `talentPoints` fields — players keep level/stats/gear but **start fresh on talents**.
- `finishVictory()` no longer grants talent points; instead it announces "Talent tier N unlocked!" when the level matches a `TIER_UNLOCKS` entry.

### UI
- Talents tab badge: "X to choose" (green, pulsing) when there are pending picks; "X picked" (gold) otherwise.
- Each tier renders as a labelled row: `— TIER N · Lv X · [picked / choose one / unlocks at Lv X] —` followed by the two option cards side-by-side.
- Picked: gold border (existing `.unlocked` style).
- Other option once picked: dimmed `.locked`.
- Unpicked + unlocked: bright green `.available` (clickable).
- Unpicked + locked: dimmed `.locked` (waiting on level).
- Active talents show `CD N` instead of the old talent-point cost.

### Design notes per class
All 15 classes redesigned around 10-tier flow:
- T1-2 foundation (stat invest, basic ability)
- T3 power expansion
- T4 class-passive override or signature ability
- T5-7 specialization choices (offense / defense / utility)
- T8 defining choice (savior, true damage, lifesteal, etc.)
- T9 high-end stat or burst
- T10 capstone (regen + crit, or massive single-shot ability)

### Known/honest notes
- Existing accounts lose their talent allocations. Fresh start under the new system.
- Talent overflow is solved: no more wasted points.
- Some talents lean on existing effect schema (e.g. `def`, `vit`, `atk`, `agi` keys on `effect`); new combinations work because `recalculate` already iterates all numeric stat keys.
- Bug fix (also in this commit): `.hidden { display: none !important; }` — the compare modal was showing on login because `.modal-overlay { display: flex }` was declared after `.hidden` and won the cascade.

### Files touched
- `index.html` only.

---

## Session 3 — 2026-05-18 — Gear expansion + Bag redesign + compare popup

### Goals
- Add 5 new equipment slots (2 rings, amulet, vest, pants) — total 9 slots.
- On the Bag tab: show equipped gear at the top, then the inventory list.
- When clicking an inventory item, show a popup that compares **current vs new** with stat deltas; player accepts or refuses.
- For rings with both slots filled, the popup lets the player pick which ring to replace.

### Implementation
- **SLOT_LABELS** and **SLOT_ORDER** now drive a 3×3 equipment grid: weapon / helm / amulet / armor (renamed "Chestplate") / vest / pants / boots / ring I / ring II.
- `emptyEquipment()` factory used by `createHero` AND by the new `migrateHero(hero)` which backfills missing slot keys on older saves (so existing accounts don't break on first load after the schema change).
- **ITEM_POOL +28 items**: 7 rings, 7 amulets, 7 vests, 7 pants spanning common→legendary with effects in line with existing item design (lifesteal, crit, dodge, regen, thorns, burn, execute, firstStrike).
- Ring items use `slot: 'ring'` in the pool; `generateItem` maps `ring1`/`ring2` hints to the `ring` pool so loot rolls work cleanly.
- **Bag tab** has a new `#bag-equipment` panel above the inventory list. Click to unequip is mirrored from the Hero tab.
- **Compare modal** (`#compare-modal`):
  - Single-target (non-ring or one empty ring slot): two columns (current vs new) + stat deltas + EQUIP/CANCEL.
  - Both ring slots filled: three columns (Ring I / Ring II / New) + deltas vs each + three buttons (REPLACE I / REPLACE II / CANCEL).
  - Defensive: re-finds the item by reference in case the inventory shifted between open and confirm.

### Files touched
- `index.html` (everything is still in one file).

### Decisions
- Kept the equipment panel on the Hero tab too — visible in both places, no harm.
- Renamed `armor` label to "Chestplate" to distinguish it from the new "Vest" overlayer; internal slot key remains `armor` for save compatibility.

---

## 🔖 RESUME HERE — 2026-05-18 — current state

### LIVE on the internet ✅
- **Play it:** https://killms.github.io/forge-and-blood/
- **Repo:** https://github.com/killms/forge-and-blood (public)
- **GitHub Pages** serves from `master` branch root. Each `git push` triggers a rebuild that's live in ~30-60s.
- Verified: HTTP 200, Content-Type `text/html`, 99,475 bytes.

### Current state
- All Phase A (combat fix + XP bar) ✅
- All Phase B (stat points 1→100, new XP curve, level cap) ✅
- Login + localStorage persistence ✅
- Deployed to GitHub Pages ✅
- Session 3 part 1: gear expansion (9 slots) + Bag redesign + compare popup ✅
- Session 3 part 2: talent tree rework (300 talents, 10 tiers, mutual exclusion) ✅
- Session 4: HP refill, monster scaling, enemy AI (PvE + PvP), Phase C (INT, mana, magical damage) ✅

### Re-deploy workflow (already automatic)
```bash
# Make edits to index.html (or anything else)
git add -A
git commit -m "your message"
git push
# ~1 min later, https://killms.github.io/forge-and-blood/ shows the new version
```

### Hosting notes (for reference)
- **GitHub Pages** is the permanent answer. Free, auto-deploys on push, no rate limits worth worrying about for this use case.
- **Catbox** (`https://files.catbox.moe/w6x1pt.html`) was the temp URL during the previous session. It serves with `Content-Type: text/plain` now (Catbox security policy), so the browser shows source instead of rendering. **Don't use Catbox for HTML.**
- Other tried hosts that **don't work** for HTML: 0x0.st (uploads disabled), tmpfiles.org, uguu.se, qu.ax, pomf.lain.la (all reject `.html`). transfer.sh down. file.io requires auth. paste.rs wraps in viewer (no script exec).

### Known limitations / open issues
1. **Per-device accounts only.** Login on PC and on phone are separate localStorage. For cross-device sync we need a backend. **Supabase is the obvious next step** (the user is already using it for Between Lunges — same project structure could apply).
2. **Stat balance:** removed the old auto `+8 stats per level`. Players now allocate 1 point per level — 87% reduction in raw growth. Tune by changing `+1` in `finishVictory` if combat feels too weak. Suggested test: get to level ~10 and see if hunting feels under-tuned.
3. **Monster scaling:** monsters cap at level 10 (Young Dragon). At hero L20+ they're trivial. **Next progression task** = scale monsters or add new biome tiers.
4. **Talent overflow:** still +1 talent point per level, but the tree only takes 8. Levels 9+ waste talent points. Either expand the tree or give talent points only every 5-10 levels.
5. **Enemy AI:** PvE monsters and PvP opponents still only use basic attack. Original roadmap Session 3.

### Roadmap — what's next, in suggested order
1. **Deploy to GitHub Pages** (blocked on user `gh auth login`).
2. **Enemy AI** — let monsters and PvP use their class abilities. Game becomes much more interesting.
3. **Monster scaling** — match enemy levels to hero, or add tiers (lv 10-20 bestiary, lv 20-30, etc.).
4. **Shop + potions** — sink for the gold that's piling up.
5. **Talent tree expansion** so talent points stay valuable past level 8.
6. **Phase C if still wanted** — STR/AGI/INT/LIFE split + magical vs melee damage + mana system. This is a real rework (1-2 sessions of focused work), would touch races, classes, items, formulas.
7. **Modularization** — split `index.html` into the structure proposed at the bottom of `PROJECT-SUMMARY.md`. Worth doing before backend integration.
8. **Backend / cross-device sync** — Supabase. Account migration from localStorage. Cloud save.
9. **App packaging** — React Native + Expo, or Capacitor (like Between Lunges).

### How to continue tomorrow
In a fresh chat, paste this CHANGELOG and say:
> "Lê este CHANGELOG.md (`F:\Jogo\CHANGELOG.md`) e depois o `F:\Jogo\index.html`. Continuamos do que está na secção RESUME HERE."

---

## Session 2 (continued) — 2026-05-17 — Auth + localStorage persistence

### Goal
- Add a login system so the player has a persistent identity and progress is saved across refreshes.
- Came with the practical bonus of implementing the long-pending **persistence** task (was Session 2 in the original roadmap).

### What was implemented
- **Auth screen** (`#auth-screen`) that loads before `#creation` / `#game`.
  - Two-tab toggle: **Log In** / **Create Account**.
  - Username (2-24 chars) + password (≥4 chars).
  - Errors shown inline ("No account with that username", "Wrong password", etc.).
- **Session strip** in the header showing `◆ username` + LOG OUT button when logged in.
- **Account storage** in `localStorage`:
  - `forgeBlood.v1.accounts` → `{ [username]: { passwordHash, createdAt, lastSavedAt, hero } }`
  - `forgeBlood.v1.activeUser` → string username of the active session
- **Password hashing:**
  - Primary: SHA-256 via `crypto.subtle` (secure context only — HTTPS / localhost).
  - Fallback: djb2 string hash for `file://` (NOT secure, but lets the user double-click `index.html` on disk and still have working auth for local testing).
- **`saveGame()` / `loadGame()`** helpers. `saveGame` is called from:
  - `createHero` (initial save)
  - `spendStatPoint`
  - Talent unlock
  - Equip / unequip
  - `finishVictory` / `finishDefeat`
  - `logout` (one last save before clearing)
- **Init flow** (`init()` at the end of the script): if active user + account + hero → load + go to game. If account but no hero → creation. Otherwise → auth screen.

### Honest caveats (called out in the UI)
- **Per-device only.** A login created on PC ≠ a login on phone. For cross-device sync we'd need a backend (Supabase candidate, ~separate session of work).
- **Not real security.** Client-side hash, no salt, no rate-limiting. Anyone with dev tools can read the data. Good enough for a personal idle game.

### Files touched
- `index.html` only.

### Decisions
- One hero per account (simplest). If the player wants alts, they create a new account.
- LOG OUT confirms before clearing the active session (data is saved, just clears the pointer).
- Active-user pointer is checked against accounts on init; if stale, it's cleared automatically and the user lands on auth.

---

## Session 2 (continued) — 2026-05-17 — Deploy prep (rename to index.html, README)

### Goal
- Get a public URL the user can open on their phone (working remotely via remote-desktop, can't open the local file).

### Changes
- Renamed `rpg-prototype-v2.html` → `index.html` so the GitHub Pages URL is clean (`/` instead of `/rpg-prototype-v2.html`). Used `git mv` so history is preserved.
- Created `README.md` for the GitHub repo page.
- Updated `PROJECT-SUMMARY.md` and `CLAUDE-CODE-STEPS.md` references to the new filename.
- Hosting choice: **GitHub Pages** (public repo under user account `killms`, free, auto-deploys on push).
- `gh` CLI is installed (2.92.0) but not authenticated locally — the user needs to run `gh auth login` once. After that, the repo create + Pages enable is a single command.

### Deploy commands (run from `F:\Jogo`, after `gh auth login`)
```bash
gh repo create killms/forge-and-blood --public --source=. --remote=origin --push
gh api -X POST /repos/killms/forge-and-blood/pages -f source[branch]=main -f source[path]=/
```
Final URL: **https://killms.github.io/forge-and-blood/**

### Files touched
- `index.html` (renamed from `rpg-prototype-v2.html`)
- `README.md` (new)
- `PROJECT-SUMMARY.md`, `CLAUDE-CODE-STEPS.md` (filename refs)
- `CHANGELOG.md` (this entry)

---

## Session 2 (continued) — 2026-05-17 — Phase B (stat points + level 100 + XP curve)

### Goals
- Hero progresses from level 1 to level 100.
- Each level grants **1 stat point** the player allocates manually into ATK / DEF / VIT / AGI.
- Replace the old `xpNext *= 1.5` curve (which became unreachable past level ~30) with a polynomial curve that works for 100 levels.

### Implementation
- New constants:
  - `MAX_LEVEL = 100`
  - `xpForLevel(level)` → `80 * level^1.5`, rounded. L1→L2 = 80 XP, L10→L11 = 2530, L50→L51 ≈ 28k, L99→L100 ≈ 79k. Total to max ≈ 2.5M XP.
- `state.hero.statPoints` (new field, starts at 0). +1 per level.
- `spendStatPoint(stat)` increments `hero.base[stat]` by 1, decrements `statPoints`, recalculates, re-renders.
- **`finishVictory` rewritten**:
  - Auto base-stat increases per level (`+2 ATK / +2 DEF / +3 VIT / +1 AGI`) **removed** — players now choose.
  - Level-up grants `+1 statPoint` + `+1 talentPoint`.
  - XP no longer accrues once `level == MAX_LEVEL`. Level cap respected in the while loop.
  - Level-up log line updated: "+1 stat point · +1 talent point".
- `renderHero` updated:
  - Stat rows now have a `+` button next to each value when the player has unspent points.
  - "X to spend" badge in the Attributes header, green and gently pulsing (CSS `pulse-green` keyframes).
  - XP bar handles MAX level cleanly — bar fills 100% and shows "MAX" / "Max level reached" instead of `0 / 0`.
- CSS additions: `.stat-add-btn`, `.stat-val-wrap`, `.attributes-header`, `.stat-points-badge`, `@keyframes pulse-green`.

### Balance notes (important)
- The old loop auto-added **8 base stats per level** (`+2 +2 +3 +1`). The new system grants **1 point per level**. That is an 87% reduction in raw stat growth — intentional, because the player now directs the build, but worth knowing if combat starts to feel weak. Easy to tune later by changing `+1` to e.g. `+3` in `finishVictory`.
- Monsters still cap at level 10 (Young Dragon). At hero level 50+ they'll be trivial. **Monster scaling / new biome tiers should be the next progression task.**
- Talent points: still +1 per level (so up to 100 by L100). The current talent tree only has 8 points worth of nodes per class — extras will be wasted until the tree expands. Not new behaviour, just amplified.

### Files touched
- `rpg-prototype-v2.html` only.

### What this does NOT do
- No respec yet (spent points are permanent).
- No diminishing returns on stats (kept linear — the 4 stats don't lead to natural soft caps; complexity not worth it yet).
- No melee/magical damage split, no mana — those would be Phase C if the user still wants them.

---

## Session 2 — 2026-05-17 — Phase A fix (combat + XP bar)

### Bug fixed: combat continued past death
- **Symptom:** the combat log kept printing rounds even after the hero or the enemy hit 0 HP.
- **Root cause:** the `resolveCombat` `while` loop scheduled every animation up-front via `setTimeout(...)`, but HP changes were also async. So the death checks (`if (defender.hp <= 0) break;`) ran *before* damage actually applied — the loop went through all 25 rounds synchronously in milliseconds, then the timeouts fired one after another and we watched a dead fighter take more turns.
- **Fix:** converted the **entire combat pipeline** to `async`/`await`. Each step now applies state changes synchronously, paints the log, and `await sleep(N)` for pacing. The loop only advances after the previous action *truly* resolved.
- Refactored functions: `resolveCombat`, `tickStartOfTurn`, `tickMutate`, `takeAction`, `executeAbility`, `executeBasicAttack`, `doDamage`.
- Added `_combatToken` so stale awaits from an interrupted combat bail cleanly if the player starts a new fight.
- Removed dead `stateFighter` helper.

### UX: XP bar promoted to its own panel
- Was tucked under HP in the hero header. Now lives in its own panel below the hero card on the Hero tab.
- New "Lv X" badge in gold + a "Next level" label with `current / next` XP, bigger XP bar (22px).
- Visible at a glance.

### Files touched
- `rpg-prototype-v2.html` only (still single file).

### Decisions & notes
- Kept the click on the enemy card as the only "engage" click — combat itself remains zero-click.
- The auto-close timer (2.8s after victory/defeat) is unchanged.

### Commit
- `851d80e` — "Fix combat continuing past death; highlight XP bar"

---

## Session 1 — 2026-05-17 — Initial setup, English translation, idle combat, git

### What was done
- Received original prototype as `files.zip` in `F:\Jogo`.
- Initialized git (Windows, local). `.gitignore` excludes `files.zip`, node_modules, etc.
- **Translated all in-game text from Portuguese to English** (UI, races, classes, talents, items, monsters, combat log).
- Renamed internal slot keys (`arma` → `weapon`, `armadura` → `armor`, `elmo` → `helm`, `botas` → `boots`) and added a `SLOT_LABELS` map for display.
- Race/class keys also anglicised (`humano` → `human`, `cavaleiro` → `knight`, etc.). Identity checks in code (e.g. `'Fúria Sanguinária'` → `rp.key === 'orcFury'`) were updated to use stable keys instead of localised names.
- **Fully idle combat:** removed the "FECHAR" / "CLOSE" button. After victory/defeat the combat panel auto-closes after ~2.8s and returns to the previous tab. (At this point combat still had the "rounds continue past death" bug — fixed in Session 2.)
- Translated project docs: `PROJETO-SUMARIO.md` → `PROJECT-SUMMARY.md`, `PASSOS-CLAUDE-CODE.md` → `CLAUDE-CODE-STEPS.md`. Old PT files deleted.
- Committed `expansion_pack-0.04` (OpenGameArt LPC sprite pack, 6MB) that was present in the folder — intended for future combat animations.

### Files created / changed
- `rpg-prototype-v2.html` — rewritten with EN content + auto-close combat
- `PROJECT-SUMMARY.md` — new (replaces `PROJETO-SUMARIO.md`)
- `CLAUDE-CODE-STEPS.md` — new (replaces `PASSOS-CLAUDE-CODE.md`)
- `.gitignore` — new

### Commit
- `ed171fe` — "Initial commit: Forge & Blood prototype (English, idle combat)"

---

## Project baseline (Session 0, before Claude Code involvement)

This is what was in the original zip:
- Single-file HTML/CSS/JS prototype of a turn-based RPG, originally in Portuguese.
- 5 races × 3 classes = 15 classes, each with a 6-node talent tree across 3 tiers.
- ~22 items across 4 equipment slots (weapon/armor/helm/boots) and 5 rarities.
- 7 monsters (PvE) + 4 randomly generated PvP opponents per "refresh".
- Combat is semi-automatic — abilities trigger via auto-cast priorities, but the close button required a click after each fight (now auto-closed).
- See `PROJECT-SUMMARY.md` for the full design doc.
