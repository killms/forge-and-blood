# Forge & Blood — Changelog

> Running log of every meaningful change. **Newest at the top.** A future Claude reading this should understand the current state of the project without having to read the full source.
>
> When continuing in a new chat, paste this file in and say "read this, then read `index.html`, then we'll continue."

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
