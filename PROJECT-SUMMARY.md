# Forge & Blood — Project Summary

## Vision

A turn-based RPG with **fully idle** combat, focused on deep hero customisation through races, classes, talents, and equipment.

**Combat philosophy:** the player does NOT control combat in real time and never clicks during a fight. All decisions are made OUTSIDE combat (pick a class, equip gear, spend talent points). Inside combat, abilities trigger automatically through smart auto-cast priorities, the fight resolves with animated log entries, and the combat panel auto-closes when the fight ends.

**Game modes:**
- **PvE** — hunt monsters of increasing level
- **PvP** — duels against "other heroes" (currently bots with random builds)

## Current stack

- HTML/CSS/JavaScript vanilla (single file)
- No external dependencies except Google Fonts (Cinzel + EB Garamond)
- Dark fantasy aesthetic, gold/blood palette over deep brown
- Mobile-first (max-width 480px), intended to ship as a native app later

## Next architectural step

When the prototype grows, the goal is to:
1. Split into multiple files (data/, components/, combat/, etc.)
2. Migrate to React Native + Expo, or Capacitor, to package as a mobile app
3. Add persistence (localStorage in the prototype; AsyncStorage/SQLite in the app)

## Race system (5 races)

Each race has stat modifiers, a racial passive, and 3 exclusive classes.

| Race | Modifiers | Passive | Classes |
|------|-----------|---------|---------|
| Human | +2 to all | Resilience: +10% XP | Knight, Cleric, Bounty Hunter |
| Elf | +6 AGI, +1 ATK | Ancient Gaze: +5% crit | Wild Archer, Druid, Blade Dancer |
| Orc | +5 ATK, +3 DEF, +2 VIT, -3 AGI | Blood Fury: +30% ATK when <50% HP | Berserker, Blood Shaman, Soul Devourer |
| Dwarf | +6 DEF, +5 VIT, +2 ATK, -2 AGI | Granite Skin: -2 damage taken | Forge Guardian, Stone Priest, War Engineer |
| Shifter | +3 ATK, +3 VIT, +3 AGI, +1 DEF | Adaptation: +1 random stat/turn in combat | Stalker, Bear Form, Chaos Shifter |

## Class system (15 unique, 3 per race)

Each class has:
- **4 base stats** (ATK, DEF, VIT, AGI)
- **1 unique passive** always active in combat (block, regen, first strike, etc.)
- **Talent tree** with 6 nodes across 3 tiers

### Talent tree structure per class

- **Tier 1** (2 talents, 1 point each): basic investments
- **Tier 2** (2 talents, 1 point each, require 1 talent from Tier 1): expansions
- **Tier 3** (2 talents, 2 points each): powerful capstone talents

### Talent types

- **Passive** (◈): permanent effect — stat bonuses, extra regen, upgrade to class passive
- **Active** (⚔): combat ability with a cooldown
- **Override**: replaces/upgrades the base class passive

### Talent progression

- Start with 1 talent point
- Gain +1 per level
- Spent points are not refundable (definitive choice — may add respec later)

## Combat system

### Flow
1. Determine who attacks first (agility > comparison, several effects can grant "first strike")
2. Each turn: start-of-turn effects (regen, DoTs, turret) → attacker action → defender action → mutation (shifters) → buff/cooldown decay
3. Ends when someone hits 0 HP, or after 25 turns (draw)

### Base damage formula
```
damage = max(1, ATK - DEF/2) * (0.9 + random()*0.2)
```

### Damage modifiers (rough order)
- Ability multiplier (e.g. Smite deals 1.5x)
- Armor penetration
- True damage (ignores defense) — e.g. Smite
- Crit (base 5% + bonus): 2x damage
- Class procs (engineer burst, stalker first crit, etc.)
- Execute (kills if HP < threshold)
- Block (defender reduces damage)
- Flat damage reduction (dwarf, bear, etc.)

### Supported effects
- DoTs: burn, curse, hex
- Buffs: +ATK, +DEF, extra regen, dodge, thorns, automatic turret
- Debuffs: -ATK, -AGI, stun
- Lifesteal — base, per ability, per equipment
- Heal (% of max HP)
- Mimicry (copies % of enemy stats)
- Cleanse (removes debuffs and DoTs)
- Savior (1x per fight, survives a killing blow with 1 HP)
- Continuous mutation (shifter)

### Auto-cast AI (hero)
Ability priority:
1. Heal if HP < 50%
2. Execute if enemy below ability's threshold
3. Random damaging ability (from available pool)
4. Otherwise, any ability not on cooldown
5. If nothing available, basic attack

Enemies: currently only use basic attack (don't use class abilities). **To improve.**

### Idle UX
- Zero clicks during combat — abilities trigger automatically.
- Combat panel auto-closes ~2.8s after the fight ends and returns the player to the previous tab.
- The only click to engage a fight is on the enemy card itself.

## Equipment system

- **4 slots:** Weapon, Armor, Helm, Boots
- **5 rarities:** Common (grey), Uncommon (green), Rare (blue), Epic (purple), Legendary (orange)
- Items give stats and may have **special effects:**
  - lifesteal, crit, dodge, regen, thorns, burn, firstStrike, execute

### Loot
- Drop probability per rarity scales with monster level
- Drop rate ~60% per victory

## Items currently implemented

~22 items across the 4 slots and 5 rarities. **Needs much more.**

## Monsters (PvE)

7 monsters, from Giant Rat (lvl 1) to Young Dragon (lvl 10).
Yield gold, XP, and may drop loot.

## PvP

4 randomly generated opponents:
- Random class + race (any of the 15 classes)
- Level ±1 of the hero
- Stats scale by level
- Regenerate after a victory

**Current limitation:** PvP opponents don't use class abilities, only basic attack. **To improve.**

## What's implemented and works

- ✅ Character creation (3 steps: race → class → name)
- ✅ Talent tree with prerequisites and point cost
- ✅ Turn-based combat with animated log
- ✅ Equipment and inventory (click to equip/unequip)
- ✅ PvE with 7 monsters
- ✅ PvP with 4 random opponents
- ✅ Level / XP / gold system
- ✅ Loot by rarity
- ✅ 5 races + 15 unique classes
- ✅ ~30 different talents
- ✅ 20+ distinct combat effects
- ✅ Fully idle combat: zero clicks during fights, auto-close on end

## What's missing / logical next steps

### Short term
- **Persistence** (localStorage): losing progress on reload is frustrating
- **Shop**: spend gold on potions, items, talent respec
- **Potions**: consumables usable in combat or outside
- **More items** (especially T2+ legendaries for each slot)
- **Enemies with abilities**: monsters and PvP should use their class abilities
- **Balance pass**: some talents are too strong, others too weak

### Medium term
- **Image/sprite system**: fields are already in place. Assets likely from OpenGameArt.org (preference for CC0 and CC-BY licenses)
- **Combat animations**: sprites bouncing, floating damage numbers, screen shake
- **More zones/biomes**: forest, desert, dungeons
- **Bosses**: unique monsters with their own mechanics
- **Crafting**: combine items
- **Quests / narrative progression**

### Long term
- **Native app** (React Native + Expo, or Capacitor)
- **Backend for real PvP** (Supabase is a strong candidate)
- **Async multiplayer** (raid another player's hero, in-game messages)
- **Guilds / clans**
- **Seasons / ladder**

## Design notes / key decisions

- **Language:** ALL in-game text is in English
- **Tone:** dark fantasy, grim but not edgy. Think "Berserk" meets "Diablo"
- **Idle combat:** the player never clicks during a fight. Decisions happen between fights. Combat resolves itself and the panel auto-closes when it's done.
- **Balance:** a fight should typically last 5-15 turns. More than 20 is too long, under 4 is too short.
- **Progression:** the player should feel stronger every level, but equipment should be the main long-term progression vector.

## Recommended structure when modularising

```
forge-and-blood/
├── index.html              ← minimal HTML shell
├── styles/
│   └── main.css            ← all styles
├── data/
│   ├── races.js            ← 5 race definitions
│   ├── classes.js          ← 15 class definitions and talent trees
│   ├── items.js            ← item pool
│   ├── monsters.js         ← PvE monsters
│   └── pvp.js              ← PvP opponent generation
├── systems/
│   ├── combat.js           ← combat engine
│   ├── damage.js           ← damage calculation
│   ├── abilities.js        ← active ability execution
│   ├── passives.js         ← race/class passives
│   ├── effects.js          ← DoTs, buffs, debuffs, mutation, etc.
│   └── ai.js               ← auto-cast logic
├── ui/
│   ├── creation.js         ← character creation screen
│   ├── hero.js             ← hero tab
│   ├── talents.js          ← talent tree
│   ├── inventory.js        ← bag
│   ├── pve.js              ← monster list
│   ├── pvp.js              ← arena
│   └── combat-view.js      ← combat UI (auto-close, no clicks)
├── core/
│   ├── state.js            ← global state
│   ├── persistence.js      ← localStorage (save/load)
│   └── leveling.js         ← XP and level-ups
└── assets/                 ← images (from OpenGameArt)
    ├── races/
    ├── monsters/
    ├── items/
    └── ui/
```

## How to continue from the current code

The `index.html` file has EVERYTHING in a single file. The first step on Claude Code will be to split it into modules following the structure above.

All the logic is already there — it just needs to be reorganised and expanded.
