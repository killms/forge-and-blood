# Next Steps for Forge & Blood

## What you have

This folder contains a working prototype of **Forge & Blood**, a fully idle turn-based RPG.

- `rpg-prototype-v2.html` — the prototype, single file (HTML + CSS + JS)
- `PROJECT-SUMMARY.md` — full design context (races, classes, combat, roadmap)
- `CLAUDE-CODE-STEPS.md` — this file

Git is initialised in this folder. Each meaningful change should be committed.

---

## Suggested working order

Pick ONE task per session. Test in the browser before moving on.

### Session 1 — Modularise
Split `rpg-prototype-v2.html` into the file structure proposed at the bottom of `PROJECT-SUMMARY.md` (HTML shell, separate CSS, JS split per system). **Test that the game still runs identically before continuing.**

### Session 2 — Persistence (localStorage)
Auto-save / auto-load the hero state. Add a "Wipe progress" button with a confirmation prompt.

### Session 3 — Enemy AI
PvE monsters and PvP opponents should use class abilities, not just basic attacks. This is what makes combat actually interesting.

### Session 4 — Shop & potions
Basic economy: spend gold on healing potions, random items, talent respec.

### Session 5 — Image / sprite scaffolding
Add `image` fields on races, classes, monsters, and items with placeholders. Later, swap in OpenGameArt assets.

### Session 6+ — Combat animations
Once everything else is solid: bouncing sprites, floating damage numbers, screen shake.

---

## Working tips

- **One task per session.** Small change → test → next.
- **Always commit before risky refactors** so you can `git reset` if needed.
- **Test in the browser**, not just in the code. Open `rpg-prototype-v2.html` directly.
- **When the chat gets long, start a new one.** Claude Code reads the project files, so it doesn't need to remember everything — just point it at the file you're editing.

---

## When the mobile app comes

When the web prototype is solid (weeks/months from now), the migration options are:

1. **React Native + Expo** — proper native app, easier to publish in stores
2. **Capacitor** — wraps the existing web app as a native app, faster but less performant

You'll need:
- Apple Developer account (~€99/year) for iOS
- Google Play account (€25 one-time) for Android

Focus on making the game fun first. App store comes later.
