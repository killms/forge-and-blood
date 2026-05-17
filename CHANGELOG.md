# Forge & Blood — Changelog

> Running log of every meaningful change. **Newest at the top.** A future Claude reading this should understand the current state of the project without having to read the full source.
>
> When continuing in a new chat, paste this file in and say "read this, then read `index.html`, then we'll continue."

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
