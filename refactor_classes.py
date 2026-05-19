"""S27 Class refactor: 15 classes → 9 universal classes (WoW-style).

Renames keys, deletes deprecated, updates RACES + MAGICAL_CLASSES,
bumps storage key version to wipe old saves.
"""
import re

PATH = r'F:\Jogo\index.html'
with open(PATH, 'r', encoding='utf-8') as f:
    s = f.read()

# ─── 1. Class key renames (class CLASSES + CLASS_SPECS object keys) ───
# Order matters: do longer keys first to avoid partial matches
KEY_RENAMES = [
    ('bladeDancer', 'thief'),
    ('devourer',    'warlock'),
    ('engineer',    'mage'),
    ('chaos',       'necromancer'),
    ('archer',      'hunter'),
    ('cleric',      'paladin'),
    ('knight',      'warrior'),
    # shaman + druid stay (already canonical names)
]

# 2. Display name updates (the .name field of each class)
NAME_RENAMES = [
    ('name: \'Knight\'',         'name: \'Warrior\''),
    ('name: \'Cleric\'',         'name: \'Paladin\''),
    ('name: \'War Engineer\'',   'name: \'Mage\''),
    ('name: \'Chaos Shifter\'',  'name: \'Necromancer\''),
    ('name: \'Archer\'',         'name: \'Hunter\''),
    ('name: \'Blade Dancer\'',   'name: \'Thief\''),
    ('name: \'Devourer\'',       'name: \'Warlock\''),
]

# 3. Descriptions — quick freshening for renamed classes
DESC_RENAMES = [
    ("desc: 'Honoured defender, shield and faith.'",   "desc: 'Honoured defender, sword and shield.'"),
    ("desc: 'Devoted to the light. Heals and punishes.'", "desc: 'Holy warrior who heals and smites.'"),
    ("desc: 'Gunpowder, gears, and death.'",           "desc: 'Master of arcane forces and elemental magic.'"),
    ("desc: 'Their very flesh is unstable magic.'",    "desc: 'Wielder of death magic, raiser of fallen flesh.'"),
    ("desc: 'Born to hunt. Bow before everything.'",   "desc: 'Tracker and marksman, deadly at range.'"),
    ("desc: 'Light steps. Bleeding edges.'",           "desc: 'Cunning blades, swift strikes, deadly precision.'"),
    ("desc: 'They feed on the weak. Hunger grows.'",   "desc: 'Caster of curses and dark contracts.'"),
]

# 4. Class blocks to DELETE entirely from CLASSES and CLASS_SPECS
DELETE_CLASSES = ['bountyHunter', 'berserker', 'guardian', 'priest', 'stalker', 'bearForm']

# ─── Apply renames ───────────────────────────────────────────────────
# Note: simple string replace because the keys are unique tokens in this file
# (no false positives expected — `knight` only appears as class key/quoted)
for old, new in KEY_RENAMES:
    # Match as standalone identifiers/strings (quoted in arrays, bare in object keys)
    # Replace: 'knight' → 'warrior'  (quoted form in classes arrays, etc.)
    s = s.replace(f"'{old}'", f"'{new}'")
    # Replace: knight: { → warrior: {  (object key with colon)
    s = s.replace(f"  {old}: {{", f"  {new}: {{")
    # Replace: knight: [ → warrior: [  (CLASS_SPECS uses arrays)
    s = s.replace(f"  {old}: [", f"  {new}: [")

# Display names
for old, new in NAME_RENAMES:
    s = s.replace(old, new)

# Descriptions
for old, new in DESC_RENAMES:
    if old in s:
        s = s.replace(old, new)

# ─── Delete class blocks ─────────────────────────────────────────────
def remove_class_block(content, class_key, table_name='CLASSES'):
    """Remove a class block from CLASSES (2-space indent, multi-line `{ ... }`)."""
    # Find `^  classKey: {` line
    pat = re.compile(rf'^  {re.escape(class_key)}: \{{', re.MULTILINE)
    m = pat.search(content)
    if not m:
        return content, False
    start = m.start()
    # Scan from start, count braces to find matching close
    depth = 0
    i = m.end()  # we've consumed the opening {
    depth = 1
    while i < len(content) and depth > 0:
        c = content[i]
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
        i += 1
    # Now i is just after the matching '}'. Skip optional comma + newline
    if i < len(content) and content[i] == ',':
        i += 1
    if i < len(content) and content[i] == '\n':
        i += 1
    return content[:start] + content[i:], True

def remove_class_specs_block(content, class_key):
    """Remove a CLASS_SPECS entry like `  className: [ ... ],` (square-bracket array)."""
    pat = re.compile(rf'^  {re.escape(class_key)}: \[', re.MULTILINE)
    m = pat.search(content)
    if not m:
        return content, False
    start = m.start()
    # Count brackets
    i = m.end()
    depth = 1
    while i < len(content) and depth > 0:
        c = content[i]
        if c == '[':
            depth += 1
        elif c == ']':
            depth -= 1
        i += 1
    if i < len(content) and content[i] == ',':
        i += 1
    if i < len(content) and content[i] == '\n':
        i += 1
    return content[:start] + content[i:], True

for cls in DELETE_CLASSES:
    s, ok1 = remove_class_block(s, cls)
    s, ok2 = remove_class_specs_block(s, cls)
    print(f"  delete {cls:14s}  CLASSES={ok1}  CLASS_SPECS={ok2}")

# ─── 5. Update RACES.X.classes arrays — every race gets all 9 ───────
ALL_NINE = "['warrior', 'paladin', 'mage', 'necromancer', 'hunter', 'shaman', 'thief', 'druid', 'warlock']"
# Replace any existing classes: [...] array inside a race
# Match: classes: ['anything', ...]
s = re.sub(r"classes: \[[^\]]*\]", f"classes: {ALL_NINE}", s)

# ─── 6. Update MAGICAL_CLASSES set ───────────────────────────────────
# Old: ['cleric', 'druid', 'shaman', 'priest', 'chaos']
# New: paladin, mage, necromancer, shaman, druid, warlock (all casters/hybrids)
s = re.sub(
    r"const MAGICAL_CLASSES = new Set\(\[[^\]]*\]\);",
    "const MAGICAL_CLASSES = new Set(['paladin', 'mage', 'necromancer', 'shaman', 'druid', 'warlock']);",
    s
)

# ─── 7. Bump storage key version to wipe old saves ─────────────────
# v1 → v2 effectively orphans all old saves
s = s.replace("'forgeBlood.v1.accounts'", "'forgeBlood.v2.accounts'")
s = s.replace("'forgeBlood.v1.activeUser'", "'forgeBlood.v2.activeUser'")
# Tutorial + audio flags can stay (cosmetic, no hero data)

# ─── Write back ───────────────────────────────────────────────────────
with open(PATH, 'w', encoding='utf-8') as f:
    f.write(s)

print()
print("=== Done ===")
print("Verify: grep -c '  warrior:\\|  paladin:\\|  mage:\\|  necromancer:\\|  hunter:\\|  shaman:\\|  thief:\\|  druid:\\|  warlock:' index.html")
