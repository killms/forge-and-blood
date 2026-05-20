"""S29 talent revamp: replace 46 boring +stat passives with class-themed effects."""
PATH = r'F:\Jogo\index.html'
with open(PATH, 'r', encoding='utf-8') as f:
    s = f.read()

# Format: (old talent block, new talent block, label)
# All replacements are exact-match strings already verified to exist in the file.
REPLACEMENTS = [
    # ===== WARRIOR (5) =====
    ("{ key: 'k1a', name: 'Defensive Training', type: 'passive', desc: '+5 Defense.', effect: { def: 5 } }",
     "{ key: 'k1a', name: 'Pain Tolerance', type: 'passive', desc: 'Below 50% HP: +30% damage dealt.', effect: { lowHpDmg: 0.30, lowHpThreshold: 0.50 } }",
     "warrior k1a → Pain Tolerance"),
    ("{ key: 'k1b', name: 'Sword Training', type: 'passive', desc: '+5 Attack.', effect: { atk: 5 } }",
     "{ key: 'k1b', name: 'Whetstone', type: 'passive', desc: 'First strike of combat deals +30%.', effect: { firstHitBonus: 0.30 } }",
     "warrior k1b → Whetstone"),
    ("{ key: 'k2b', name: 'Iron Will', type: 'passive', desc: '+8 Vitality.', effect: { vit: 8 } }",
     "{ key: 'k2b', name: 'Battle Reflex', type: 'passive', desc: '+12% critical chance.', effect: { critBonus: 0.12 } }",
     "warrior k2b → Battle Reflex"),
    ("{ key: 'k3a', name: 'Steel Vigour', type: 'passive', desc: '+8 Vitality.', effect: { vit: 8 } }",
     "{ key: 'k3a', name: 'Bloodthirst', type: 'passive', desc: '10% lifesteal on all hits.', effect: { lifesteal: 0.10 } }",
     "warrior k3a → Bloodthirst"),
    ("{ key: 'k5a', name: 'Bulwark', type: 'passive', desc: '+10 Defense.', effect: { def: 10 } }",
     "{ key: 'k5a', name: 'Indomitable', type: 'passive', desc: 'Reduces all damage taken by 4 (flat).', effect: { dmgReduce: 4 } }",
     "warrior k5a → Indomitable"),

    # ===== PALADIN (6) =====
    ("{ key: 'c1a', name: 'Devotion', type: 'passive', desc: '+6 Vitality.', effect: { vit: 6 } }",
     "{ key: 'c1a', name: 'Aura of Light', type: 'passive', desc: 'Regenerates 3 HP per turn.', effect: { regen: 3 } }",
     "paladin c1a → Aura of Light"),
    ("{ key: 'c1b', name: 'Punishment', type: 'passive', desc: '+5 Attack.', effect: { atk: 5 } }",
     "{ key: 'c1b', name: 'Holy Bond', type: 'passive', desc: '+25% damage vs Lich/Skeleton/Necromancer (undead).', effect: { holyVsUndead: 0.25 } }",
     "paladin c1b → Holy Bond"),
    ("{ key: 'c2b', name: 'Wisdom', type: 'passive', desc: '+6 Vitality.', effect: { vit: 6 } }",
     "{ key: 'c2b', name: 'Inner Faith', type: 'passive', desc: '+10% critical chance.', effect: { critBonus: 0.10 } }",
     "paladin c2b → Inner Faith"),
    ("{ key: 'c3a', name: 'Sanctified Strikes', type: 'passive', desc: '+4 Attack.', effect: { atk: 4 } }",
     "{ key: 'c3a', name: 'Smite', type: 'passive', desc: '8% lifesteal on all hits.', effect: { lifesteal: 0.08 } }",
     "paladin c3a → Smite"),
    ("{ key: 'c5a', name: 'Greater Devotion', type: 'passive', desc: '+10 Vitality.', effect: { vit: 10 } }",
     "{ key: 'c5a', name: 'Templar Vigil', type: 'passive', desc: 'Regenerates 6 HP per turn.', effect: { regen: 6 } }",
     "paladin c5a → Templar Vigil"),
    ("{ key: 'c7a', name: 'Protector', type: 'passive', desc: '+8 Defense.', effect: { def: 8 } }",
     "{ key: 'c7a', name: 'Holy Shield', type: 'passive', desc: 'Reduces all damage taken by 3 (flat).', effect: { dmgReduce: 3 } }",
     "paladin c7a → Holy Shield"),

    # ===== HUNTER (4) =====
    ("{ key: 'a1a', name: 'Bowstring Tension', type: 'passive', desc: '+6 Attack.', effect: { atk: 6 } }",
     "{ key: 'a1a', name: 'Eagle Eye', type: 'passive', desc: '+15% critical chance vs enemies above 70% HP.', effect: { vsHighHpCrit: 0.15 } }",
     "hunter a1a → Eagle Eye"),
    ("{ key: 'a1b', name: 'Light Step', type: 'passive', desc: '+6 Agility.', effect: { agi: 6 } }",
     "{ key: 'a1b', name: 'Pathfinder', type: 'passive', desc: 'First shot of combat deals +25%.', effect: { firstHitBonus: 0.25 } }",
     "hunter a1b → Pathfinder"),
    ("{ key: 'a2b', name: 'Tough Sinew', type: 'passive', desc: '+5 Vitality.', effect: { vit: 5 } }",
     "{ key: 'a2b', name: 'Steady Hands', type: 'passive', desc: '+10% critical chance.', effect: { critBonus: 0.10 } }",
     "hunter a2b → Steady Hands"),
    ("{ key: 'a5a', name: 'Wind Walker', type: 'passive', desc: '+8 Agility.', effect: { agi: 8 } }",
     "{ key: 'a5a', name: 'Marked Target', type: 'passive', desc: 'Each consecutive hit on the same target: +15% damage.', effect: { markOnHit: 0.15 } }",
     "hunter a5a → Marked Target"),

    # ===== THIEF (6) =====
    ("{ key: 'l1a', name: 'Wind Step', type: 'passive', desc: '+7 Agility.', effect: { agi: 7 } }",
     "{ key: 'l1a', name: 'Backstab', type: 'passive', desc: 'First strike of combat deals +35%.', effect: { firstHitBonus: 0.35 } }",
     "thief l1a → Backstab"),
    ("{ key: 'l1b', name: 'Honed Blades', type: 'passive', desc: '+5 Attack.', effect: { atk: 5 } }",
     "{ key: 'l1b', name: 'Bleed', type: 'passive', desc: 'Critical hits apply Bleed (5 dmg / 3 turns).', effect: { bleedOnCrit: 5, bleedOnCritDur: 3 } }",
     "thief l1b → Bleed"),
    ("{ key: 'l2b', name: 'Toughness', type: 'passive', desc: '+5 Vitality.', effect: { vit: 5 } }",
     "{ key: 'l2b', name: 'Combat Reflex', type: 'passive', desc: '+12% critical chance.', effect: { critBonus: 0.12 } }",
     "thief l2b → Combat Reflex"),
    ("{ key: 'l3a', name: 'Light as Air', type: 'passive', desc: '+10 Agility.', effect: { agi: 10 } }",
     "{ key: 'l3a', name: 'Lethal Mark', type: 'passive', desc: 'Each consecutive hit on same target: +12% damage.', effect: { markOnHit: 0.12 } }",
     "thief l3a → Lethal Mark"),
    ("{ key: 'l5a', name: 'Sharpened Edge', type: 'passive', desc: '+8 Attack.', effect: { atk: 8 } }",
     "{ key: 'l5a', name: 'Vital Strike', type: 'passive', desc: 'Critical hits apply Deep Wound (8 dmg / 3 turns).', effect: { bleedOnCrit: 8, bleedOnCritDur: 3 } }",
     "thief l5a → Vital Strike"),
    ("{ key: 'l6a', name: 'Untouchable', type: 'passive', desc: '+10 Agility.', effect: { agi: 10 } }",
     "{ key: 'l6a', name: 'Shadow Step', type: 'passive', desc: '10% lifesteal on all hits.', effect: { lifesteal: 0.10 } }",
     "thief l6a → Shadow Step"),

    # ===== DRUID (5) =====
    ("{ key: 'd1a', name: 'Deep Roots', type: 'passive', desc: '+8 Vitality.', effect: { vit: 8 } }",
     "{ key: 'd1a', name: 'Renewal', type: 'passive', desc: 'Regenerates 4 HP per turn.', effect: { regen: 4 } }",
     "druid d1a → Renewal"),
    ("{ key: 'd1b', name: 'Wild Fury', type: 'passive', desc: '+5 Attack.', effect: { atk: 5 } }",
     "{ key: 'd1b', name: 'Wild Form', type: 'passive', desc: 'Below 35% HP: +30% damage dealt.', effect: { lowHpDmg: 0.30, lowHpThreshold: 0.35 } }",
     "druid d1b → Wild Form"),
    ("{ key: 'd2b', name: 'Tough Bark', type: 'passive', desc: '+5 Defense.', effect: { def: 5 } }",
     "{ key: 'd2b', name: 'Thick Hide', type: 'passive', desc: 'Reduces all damage taken by 3 (flat).', effect: { dmgReduce: 3 } }",
     "druid d2b → Thick Hide"),
    ("{ key: 'd5a', name: 'Heart of the Forest', type: 'passive', desc: '+10 Vitality.', effect: { vit: 10 } }",
     "{ key: 'd5a', name: 'Mother Tree', type: 'passive', desc: 'Regenerates 7 HP per turn.', effect: { regen: 7 } }",
     "druid d5a → Mother Tree"),
    ("{ key: 'd9b', name: 'Primal Strikes', type: 'passive', desc: '+15 Attack.', effect: { atk: 15 } }",
     "{ key: 'd9b', name: 'Predator', type: 'passive', desc: 'First strike of combat deals +50%.', effect: { firstHitBonus: 0.50 } }",
     "druid d9b → Predator"),

    # ===== SHAMAN (6) =====
    ("{ key: 's1a', name: 'Hot Blood', type: 'passive', desc: '+5 Attack.', effect: { atk: 5 } }",
     "{ key: 's1a', name: 'Spirit Bond', type: 'passive', desc: '8% lifesteal on all hits.', effect: { lifesteal: 0.08 } }",
     "shaman s1a → Spirit Bond"),
    ("{ key: 's1b', name: 'Vital Pulse', type: 'passive', desc: '+6 Vitality.', effect: { vit: 6 } }",
     "{ key: 's1b', name: 'Spirit Heal', type: 'passive', desc: 'Regenerates 4 HP per turn.', effect: { regen: 4 } }",
     "shaman s1b → Spirit Heal"),
    ("{ key: 's2b', name: 'Iron Veins', type: 'passive', desc: '+6 Vitality.', effect: { vit: 6 } }",
     "{ key: 's2b', name: 'Stone Skin', type: 'passive', desc: 'Reduces all damage taken by 3 (flat).', effect: { dmgReduce: 3 } }",
     "shaman s2b → Stone Skin"),
    ("{ key: 's3a', name: 'Blood Surge', type: 'passive', desc: '+5 Attack.', effect: { atk: 5 } }",
     "{ key: 's3a', name: 'Lightning Strike', type: 'passive', desc: 'First strike of combat deals +30%.', effect: { firstHitBonus: 0.30 } }",
     "shaman s3a → Lightning Strike"),
    ("{ key: 's5a', name: 'Crimson Mastery', type: 'passive', desc: '+10 Vitality.', effect: { vit: 10 } }",
     "{ key: 's5a', name: 'Ancestral Vigour', type: 'passive', desc: 'Regenerates 6 HP per turn.', effect: { regen: 6 } }",
     "shaman s5a → Ancestral Vigour"),
    ("{ key: 's6a', name: 'Bloodlust', type: 'passive', desc: '+8 Attack.', effect: { atk: 8 } }",
     "{ key: 's6a', name: 'Battle Trance', type: 'passive', desc: 'Below 40% HP: +30% damage dealt.', effect: { lowHpDmg: 0.30, lowHpThreshold: 0.40 } }",
     "shaman s6a → Battle Trance"),

    # ===== WARLOCK (7) =====
    ("{ key: 'v1a', name: 'Maw', type: 'passive', desc: '+6 Attack.', effect: { atk: 6 } }",
     "{ key: 'v1a', name: 'Doomed', type: 'passive', desc: 'Each consecutive hit on same target: +15% damage.', effect: { markOnHit: 0.15 } }",
     "warlock v1a → Doomed"),
    ("{ key: 'v1b', name: 'Tough Hide', type: 'passive', desc: '+6 Vitality.', effect: { vit: 6 } }",
     "{ key: 'v1b', name: 'Dark Pact', type: 'passive', desc: '10% lifesteal on all hits.', effect: { lifesteal: 0.10 } }",
     "warlock v1b → Dark Pact"),
    ("{ key: 'v2b', name: 'Hunger', type: 'passive', desc: '+5 Attack.', effect: { atk: 5 } }",
     "{ key: 'v2b', name: 'Curse', type: 'passive', desc: 'Critical hits apply Curse (6 dmg / 3 turns).', effect: { bleedOnCrit: 6, bleedOnCritDur: 3 } }",
     "warlock v2b → Curse"),
    ("{ key: 'v3a', name: 'Endless Stomach', type: 'passive', desc: '+7 Vitality.', effect: { vit: 7 } }",
     "{ key: 'v3a', name: 'Drain Soul', type: 'passive', desc: 'Regenerates 4 HP per turn.', effect: { regen: 4 } }",
     "warlock v3a → Drain Soul"),
    ("{ key: 'v5a', name: 'Glutton', type: 'passive', desc: '+10 Vitality.', effect: { vit: 10 } }",
     "{ key: 'v5a', name: \"Death's Grip\", type: 'passive', desc: 'Below 35% HP: +35% damage dealt.', effect: { lowHpDmg: 0.35, lowHpThreshold: 0.35 } }",
     "warlock v5a → Death's Grip"),
    ("{ key: 'v6a', name: 'Bloodthirst', type: 'passive', desc: '+10 Attack.', effect: { atk: 10 } }",
     "{ key: 'v6a', name: 'Soul Reaver', type: 'passive', desc: '12% lifesteal on all hits.', effect: { lifesteal: 0.12 } }",
     "warlock v6a → Soul Reaver"),

    # ===== MAGE (5) =====
    ("{ key: 'e1a', name: 'Calibration', type: 'passive', desc: '+6 Attack.', effect: { atk: 6 } }",
     "{ key: 'e1a', name: 'Arcane Focus', type: 'passive', desc: '+12% critical chance.', effect: { critBonus: 0.12 } }",
     "mage e1a → Arcane Focus"),
    ("{ key: 'e1b', name: 'Sturdy Frame', type: 'passive', desc: '+6 Vitality.', effect: { vit: 6 } }",
     "{ key: 'e1b', name: 'Mana Shield', type: 'passive', desc: 'Regenerates 4 HP per turn.', effect: { regen: 4 } }",
     "mage e1b → Mana Shield"),
    ("{ key: 'e2b', name: 'Heavy Tools', type: 'passive', desc: '+5 Defense.', effect: { def: 5 } }",
     "{ key: 'e2b', name: 'Arcane Barrier', type: 'passive', desc: 'Reduces all damage taken by 3 (flat).', effect: { dmgReduce: 3 } }",
     "mage e2b → Arcane Barrier"),
    ("{ key: 'e3a', name: 'Anvil Chest', type: 'passive', desc: '+6 Vitality.', effect: { vit: 6 } }",
     "{ key: 'e3a', name: 'Soul Burn', type: 'passive', desc: '8% lifesteal on all hits.', effect: { lifesteal: 0.08 } }",
     "mage e3a → Soul Burn"),
    ("{ key: 'e6a', name: 'Master Smith', type: 'passive', desc: '+10 Attack.', effect: { atk: 10 } }",
     "{ key: 'e6a', name: 'Archmage', type: 'passive', desc: 'First spell of combat deals +35%.', effect: { firstHitBonus: 0.35 } }",
     "mage e6a → Archmage"),

    # ===== NECROMANCER (2) =====
    ("{ key: 'h1b', name: 'Wild Mutation', type: 'passive', desc: '+5 Attack.', effect: { atk: 5 } }",
     "{ key: 'h1b', name: 'Blood Pact', type: 'passive', desc: '10% lifesteal on all hits.', effect: { lifesteal: 0.10 } }",
     "necromancer h1b → Blood Pact"),
    ("{ key: 'h2b', name: 'Unstable', type: 'passive', desc: '+5 Vitality.', effect: { vit: 5 } }",
     "{ key: 'h2b', name: \"Death's Embrace\", type: 'passive', desc: 'Below 30% HP: +30% damage dealt.', effect: { lowHpDmg: 0.30, lowHpThreshold: 0.30 } }",
     "necromancer h2b → Death's Embrace"),
]

print(f'=== Applying {len(REPLACEMENTS)} talent revamps ===')
ok = fail = 0
for old, new, label in REPLACEMENTS:
    if old in s:
        s = s.replace(old, new)
        ok += 1
        print(f'  OK  {label}')
    else:
        fail += 1
        print(f'  MISS  {label}')

with open(PATH, 'w', encoding='utf-8') as f:
    f.write(s)

print(f'\n=== Done: {ok} ok, {fail} miss ===')
