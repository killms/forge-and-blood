"""S31 C5: Add a 3rd talent option to every tier of every class.
Inserts 9 classes × 10 tiers = 90 new talent objects."""
import re

PATH = r'F:\Jogo\index.html'
with open(PATH, 'r', encoding='utf-8') as f:
    s = f.read()

# Each tuple: (class_key, tier, insertion).
# `insertion` is the new talent block to add as the 3rd element of that tier.
# Format kept tight to match existing inline style.
NEW_TALENTS = [
    # ============ WARRIOR (k) — fury + bleed + sustain mid-line ============
    ('warrior', 1, "{ key: 'k1c', name: 'Berserker Edge', type: 'passive', desc: '+10% crit chance.', effect: { critBonus: 0.10 } }"),
    ('warrior', 2, "{ key: 'k2c', name: 'Quick Slash', type: 'active', desc: '120% atk · CD 2 (low cooldown).', ability: { dmgMult: 1.2, cd: 2 } }"),
    ('warrior', 3, "{ key: 'k3c', name: 'Combo Strike', type: 'passive', desc: 'Each consecutive hit on same target: +10% damage.', effect: { markOnHit: 0.10 } }"),
    ('warrior', 4, "{ key: 'k4c', name: 'Warrior\\'s Grit', type: 'passive', desc: 'Below 40% HP: +25% damage.', effect: { lowHpDmg: 0.25, lowHpThreshold: 0.40 } }"),
    ('warrior', 5, "{ key: 'k5c', name: 'Rend', type: 'active', desc: '150% atk + bleed 6/3 turns. CD 5.', ability: { dmgMult: 1.5, dot: 6, dur: 3, cd: 5 } }"),
    ('warrior', 6, "{ key: 'k6c', name: 'Battle Fury', type: 'active', desc: '+40% atk for 4 turns. CD 7.', ability: { buffAtk: 0.4, dur: 4, cd: 7 } }"),
    ('warrior', 7, "{ key: 'k7c', name: 'Critical Edge', type: 'passive', desc: 'Critical hits apply Bleed (10/3 turns).', effect: { bleedOnCrit: 10, bleedOnCritDur: 3 } }"),
    ('warrior', 8, "{ key: 'k8c', name: 'Onslaught', type: 'active', desc: '4 hits at 130%. CD 8.', ability: { multiHit: 4, dmgMult: 1.3, cd: 8 } }"),
    ('warrior', 9, "{ key: 'k9c', name: 'Warlord', type: 'passive', desc: '+20% damage vs enemies above 70% HP.', effect: { vsHighHpCrit: 0.20 } }"),
    ('warrior', 10, "{ key: 'k10c', name: 'Berserker King', type: 'passive', desc: '15% lifesteal + below 30% HP +40% damage.', effect: { lifesteal: 0.15, lowHpDmg: 0.40, lowHpThreshold: 0.30 } }"),

    # ============ PALADIN (c) — light + healing alternative builds ============
    ('paladin', 1, "{ key: 'c1c', name: 'Light\\'s Touch', type: 'passive', desc: '5% lifesteal on all hits.', effect: { lifesteal: 0.05 } }"),
    ('paladin', 2, "{ key: 'c2c', name: 'Light Strike', type: 'active', desc: '140% atk · true damage. CD 3.', ability: { dmgMult: 1.4, trueDmg: true, cd: 3 } }"),
    ('paladin', 3, "{ key: 'c3c', name: 'Righteous Path', type: 'passive', desc: '+8% crit chance.', effect: { critBonus: 0.08 } }"),
    ('paladin', 4, "{ key: 'c4c', name: 'Lay on Hands', type: 'active', desc: 'Restores 40% maxHP. CD 8.', ability: { heal: 0.4, cd: 8 } }"),
    ('paladin', 5, "{ key: 'c5c', name: 'Crusader\\'s Wrath', type: 'passive', desc: 'First strike of combat deals +40%.', effect: { firstHitBonus: 0.40 } }"),
    ('paladin', 6, "{ key: 'c6c', name: 'Holy Verdict', type: 'active', desc: '180% atk + heal 15% maxHP. CD 6.', ability: { dmgMult: 1.8, heal: 0.15, cd: 6 } }"),
    ('paladin', 7, "{ key: 'c7c', name: 'Avenging Light', type: 'passive', desc: 'Critical hits apply Bleed (8/3 turns).', effect: { bleedOnCrit: 8, bleedOnCritDur: 3 } }"),
    ('paladin', 8, "{ key: 'c8c', name: 'Crusade', type: 'active', desc: '+60% atk + heal 5%/turn for 3 turns. CD 8.', ability: { buffAtk: 0.6, regenBuff: 5, dur: 3, cd: 8 } }"),
    ('paladin', 9, "{ key: 'c9c', name: 'Light Eternal', type: 'passive', desc: 'Regen 10 HP/turn + +10% crit.', effect: { regen: 10, critBonus: 0.10 } }"),
    ('paladin', 10, "{ key: 'c10c', name: 'Avatar of Dawn', type: 'passive', desc: '+30% damage vs undead + 15% lifesteal.', effect: { holyVsUndead: 0.30, lifesteal: 0.15 } }"),

    # ============ MAGE (e) — fire/ice/arcane caster paths ============
    ('mage', 1, "{ key: 'e1c', name: 'Mana Tap', type: 'passive', desc: 'Regen 3 HP/turn.', effect: { regen: 3 } }"),
    ('mage', 2, "{ key: 'e2c', name: 'Arcane Missile', type: 'active', desc: '160% atk · true damage. CD 3.', ability: { dmgMult: 1.6, trueDmg: true, cd: 3 } }"),
    ('mage', 3, "{ key: 'e3c', name: 'Frost Bolt', type: 'active', desc: '140% atk + stun 1. CD 4.', ability: { dmgMult: 1.4, stun: 1, cd: 4 } }"),
    ('mage', 4, "{ key: 'e4c', name: 'Pyromaniac', type: 'passive', desc: 'Crits apply Burn (10/3 turns).', effect: { bleedOnCrit: 10, bleedOnCritDur: 3 } }"),
    ('mage', 5, "{ key: 'e5c', name: 'Ice Lance', type: 'active', desc: '200% atk · ignores 40% def + stun 1. CD 5.', ability: { dmgMult: 2, armorPen: 0.4, stun: 1, cd: 5 } }"),
    ('mage', 6, "{ key: 'e6c', name: 'Arcane Echo', type: 'passive', desc: 'Each consecutive hit on same target: +12% damage.', effect: { markOnHit: 0.12 } }"),
    ('mage', 7, "{ key: 'e7c', name: 'Combustion', type: 'active', desc: '260% atk + burn 12/3 turns. CD 6.', ability: { dmgMult: 2.6, dot: 12, dur: 3, cd: 6 } }"),
    ('mage', 8, "{ key: 'e8c', name: 'Mind Drain', type: 'passive', desc: '10% lifesteal on all spells.', effect: { lifesteal: 0.10 } }"),
    ('mage', 9, "{ key: 'e9c', name: 'Arcane Mastery', type: 'passive', desc: '+25% crit chance.', effect: { critBonus: 0.25 } }"),
    ('mage', 10, "{ key: 'e10c', name: 'Time Stop', type: 'active', desc: '180% atk + stun 2 + 60% atk buff 2 turns. CD 11.', ability: { dmgMult: 1.8, stun: 2, buffAtk: 0.6, dur: 2, cd: 11 } }"),

    # ============ NECROMANCER (h) — death magic, drain, dot ============
    ('necromancer', 1, "{ key: 'h1c', name: 'Soul Touch', type: 'passive', desc: 'Crits apply Wither (7/3 turns).', effect: { bleedOnCrit: 7, bleedOnCritDur: 3 } }"),
    ('necromancer', 2, "{ key: 'h2c', name: 'Drain Touch', type: 'active', desc: '130% atk + heal 30% of damage dealt. CD 3.', ability: { dmgMult: 1.3, lifestealOnce: 0.30, cd: 3 } }"),
    ('necromancer', 3, "{ key: 'h3c', name: 'Curse Mark', type: 'passive', desc: 'Each consecutive hit on same target: +15% damage.', effect: { markOnHit: 0.15 } }"),
    ('necromancer', 4, "{ key: 'h4c', name: 'Plague', type: 'active', desc: '160% atk + dot 14/4 turns. CD 5.', ability: { dmgMult: 1.6, dot: 14, dur: 4, cd: 5 } }"),
    ('necromancer', 5, "{ key: 'h5c', name: 'Death\\'s Hand', type: 'passive', desc: 'Below 25% HP: +50% damage.', effect: { lowHpDmg: 0.50, lowHpThreshold: 0.25 } }"),
    ('necromancer', 6, "{ key: 'h6c', name: 'Soul Siphon', type: 'active', desc: '200% atk + heal 50% of damage. CD 5.', ability: { dmgMult: 2, lifestealOnce: 0.50, cd: 5 } }"),
    ('necromancer', 7, "{ key: 'h7c', name: 'Reaper\\'s Mark', type: 'passive', desc: 'Executes enemies below 25% HP.', effect: {}, override: { proc: 'execute', val: 0.25 } }"),
    ('necromancer', 8, "{ key: 'h8c', name: 'Pestilence', type: 'active', desc: '3 hits at 100% atk + dot 6/3 each. CD 7.', ability: { multiHit: 3, dmgMult: 1, dot: 6, dur: 3, cd: 7 } }"),
    ('necromancer', 9, "{ key: 'h9c', name: 'Phylactery', type: 'passive', desc: 'Survive 1 killing blow at 30% HP per fight.', effect: { savior: true } }"),
    ('necromancer', 10, "{ key: 'h10c', name: 'Final Death', type: 'active', desc: '350% atk · true damage + executes <40%. CD 10.', ability: { dmgMult: 3.5, trueDmg: true, execThreshold: 0.4, cd: 10 } }"),

    # ============ HUNTER (a) — ranged precision, pet, marks ============
    ('hunter', 1, "{ key: 'a1c', name: 'Quick Shot', type: 'active', desc: '110% atk · CD 2 (rapid fire).', ability: { dmgMult: 1.1, cd: 2 } }"),
    ('hunter', 2, "{ key: 'a2c', name: 'Sniper Stance', type: 'passive', desc: '+18% crit vs enemies above 70% HP.', effect: { vsHighHpCrit: 0.18 } }"),
    ('hunter', 3, "{ key: 'a3c', name: 'Piercing Shot', type: 'active', desc: '170% atk · ignores 60% def. CD 4.', ability: { dmgMult: 1.7, armorPen: 0.6, cd: 4 } }"),
    ('hunter', 4, "{ key: 'a4c', name: 'Aim True', type: 'passive', desc: 'Critical hits apply Bleed (7/3 turns).', effect: { bleedOnCrit: 7, bleedOnCritDur: 3 } }"),
    ('hunter', 5, "{ key: 'a5c', name: 'Trap', type: 'active', desc: '130% atk + stun 1 + dot 5/2 turns. CD 5.', ability: { dmgMult: 1.3, stun: 1, dot: 5, dur: 2, cd: 5 } }"),
    ('hunter', 6, "{ key: 'a6c', name: 'Killshot', type: 'passive', desc: 'Executes enemies below 20% HP.', effect: {}, override: { proc: 'execute', val: 0.20 } }"),
    ('hunter', 7, "{ key: 'a7c', name: 'Volley', type: 'active', desc: '5 hits at 80% atk. CD 6.', ability: { multiHit: 5, dmgMult: 0.8, cd: 6 } }"),
    ('hunter', 8, "{ key: 'a8c', name: 'Master Tracker', type: 'passive', desc: 'Each hit on same target: +12% damage.', effect: { markOnHit: 0.12 } }"),
    ('hunter', 9, "{ key: 'a9c', name: 'Critical Shot', type: 'passive', desc: '+30% crit + 8% lifesteal.', effect: { critBonus: 0.30, lifesteal: 0.08 } }"),
    ('hunter', 10, "{ key: 'a10c', name: 'Headshot', type: 'active', desc: '450% atk · guaranteed crit. CD 9.', ability: { dmgMult: 4.5, guaranteedCrit: true, cd: 9 } }"),

    # ============ SHAMAN (s) — elements, totems, balance ============
    ('shaman', 1, "{ key: 's1c', name: 'Storm Touch', type: 'passive', desc: '+8% crit chance.', effect: { critBonus: 0.08 } }"),
    ('shaman', 2, "{ key: 's2c', name: 'Earth Spike', type: 'active', desc: '140% atk + stun 1. CD 4.', ability: { dmgMult: 1.4, stun: 1, cd: 4 } }"),
    ('shaman', 3, "{ key: 's3c', name: 'Healing Totem', type: 'active', desc: 'Restores 20% maxHP. CD 5.', ability: { heal: 0.2, cd: 5 } }"),
    ('shaman', 4, "{ key: 's4c', name: 'Lightning Chain', type: 'passive', desc: 'Each consecutive hit on same target: +12% damage.', effect: { markOnHit: 0.12 } }"),
    ('shaman', 5, "{ key: 's5c', name: 'Flame Shock', type: 'active', desc: '170% atk + dot 10/3 turns. CD 5.', ability: { dmgMult: 1.7, dot: 10, dur: 3, cd: 5 } }"),
    ('shaman', 6, "{ key: 's6c', name: 'Spirit Walk', type: 'passive', desc: 'Crits apply Soul Burn (9/3 turns).', effect: { bleedOnCrit: 9, bleedOnCritDur: 3 } }"),
    ('shaman', 7, "{ key: 's7c', name: 'Thunder Strike', type: 'active', desc: '230% atk + stun 1. CD 6.', ability: { dmgMult: 2.3, stun: 1, cd: 6 } }"),
    ('shaman', 8, "{ key: 's8c', name: 'Ancestral Spirit', type: 'passive', desc: 'Survive 1 killing blow at 40% HP per fight.', effect: { savior: true } }"),
    ('shaman', 9, "{ key: 's9c', name: 'Storm Master', type: 'passive', desc: 'Regen 8 HP/turn + +12% crit.', effect: { regen: 8, critBonus: 0.12 } }"),
    ('shaman', 10, "{ key: 's10c', name: 'Wrath of the Elements', type: 'active', desc: '4 hits at 130% atk + dot 8/3 each. CD 11.', ability: { multiHit: 4, dmgMult: 1.3, dot: 8, dur: 3, cd: 11 } }"),

    # ============ THIEF (l) — crit, agility, sustain alternatives ============
    ('thief', 1, "{ key: 'l1c', name: 'Sneak Attack', type: 'passive', desc: 'First strike of combat deals +40%.', effect: { firstHitBonus: 0.40 } }"),
    ('thief', 2, "{ key: 'l2c', name: 'Poison Dagger', type: 'active', desc: '120% atk + dot 8/4 turns. CD 4.', ability: { dmgMult: 1.2, dot: 8, dur: 4, cd: 4 } }"),
    ('thief', 3, "{ key: 'l3c', name: 'Quick Strike', type: 'active', desc: '125% atk · CD 2 (rapid).', ability: { dmgMult: 1.25, cd: 2 } }"),
    ('thief', 4, "{ key: 'l4c', name: 'Lethal Poison', type: 'passive', desc: '+15% damage vs enemies above 70% HP.', effect: { vsHighHpCrit: 0.15 } }"),
    ('thief', 5, "{ key: 'l5c', name: 'Ambush', type: 'active', desc: '220% atk · guaranteed crit. CD 5.', ability: { dmgMult: 2.2, guaranteedCrit: true, cd: 5 } }"),
    ('thief', 6, "{ key: 'l6c', name: 'Shadow Veil', type: 'passive', desc: 'Below 30% HP: +35% damage.', effect: { lowHpDmg: 0.35, lowHpThreshold: 0.30 } }"),
    ('thief', 7, "{ key: 'l7c', name: 'Flurry', type: 'active', desc: '4 hits at 110% atk. CD 6.', ability: { multiHit: 4, dmgMult: 1.1, cd: 6 } }"),
    ('thief', 8, "{ key: 'l8c', name: 'Killer\\'s Instinct', type: 'passive', desc: 'Executes enemies below 30% HP.', effect: {}, override: { proc: 'execute', val: 0.30 } }"),
    ('thief', 9, "{ key: 'l9c', name: 'Master Thief', type: 'passive', desc: '+25% crit + 12% lifesteal.', effect: { critBonus: 0.25, lifesteal: 0.12 } }"),
    ('thief', 10, "{ key: 'l10c', name: 'Death Mark', type: 'active', desc: '380% atk + executes <50% HP. CD 9.', ability: { dmgMult: 3.8, execThreshold: 0.5, cd: 9 } }"),

    # ============ DRUID (d) — nature, shapeshift, sustain ============
    ('druid', 1, "{ key: 'd1c', name: 'Bark Skin', type: 'passive', desc: 'Reduces all damage by 2 (flat).', effect: { dmgReduce: 2 } }"),
    ('druid', 2, "{ key: 'd2c', name: 'Wild Strike', type: 'active', desc: '140% atk + 30% lifesteal once. CD 4.', ability: { dmgMult: 1.4, lifestealOnce: 0.30, cd: 4 } }"),
    ('druid', 3, "{ key: 'd3c', name: 'Lifebloom', type: 'active', desc: 'Restores 25% maxHP + regen 4/turn 3 turns. CD 6.', ability: { heal: 0.25, regenBuff: 4, dur: 3, cd: 6 } }"),
    ('druid', 4, "{ key: 'd4c', name: 'Thorn Aura', type: 'passive', desc: 'Crits apply Thorns (6/3 turns).', effect: { bleedOnCrit: 6, bleedOnCritDur: 3 } }"),
    ('druid', 5, "{ key: 'd5c', name: 'Cat Form', type: 'active', desc: '180% atk · guaranteed crit. CD 5.', ability: { dmgMult: 1.8, guaranteedCrit: true, cd: 5 } }"),
    ('druid', 6, "{ key: 'd6c', name: 'Nature\\'s Grasp', type: 'passive', desc: 'Each consecutive hit on same target: +10% damage.', effect: { markOnHit: 0.10 } }"),
    ('druid', 7, "{ key: 'd7c', name: 'Moonfire', type: 'active', desc: '190% atk + dot 12/4 turns. CD 6.', ability: { dmgMult: 1.9, dot: 12, dur: 4, cd: 6 } }"),
    ('druid', 8, "{ key: 'd8c', name: 'Wild Resilience', type: 'passive', desc: 'Below 35% HP: +25% damage.', effect: { lowHpDmg: 0.25, lowHpThreshold: 0.35 } }"),
    ('druid', 9, "{ key: 'd9c', name: 'Ancient Wisdom', type: 'passive', desc: '+15% crit + regen 6 HP/turn.', effect: { critBonus: 0.15, regen: 6 } }"),
    ('druid', 10, "{ key: 'd10c', name: 'Tranquility', type: 'active', desc: 'Heal 60% maxHP + 300% atk. CD 12.', ability: { heal: 0.6, dmgMult: 3, cd: 12 } }"),

    # ============ WARLOCK (v) — curses, drain, demonic ============
    ('warlock', 1, "{ key: 'v1c', name: 'Demonic Pact', type: 'passive', desc: 'Crits apply Curse (8/3 turns).', effect: { bleedOnCrit: 8, bleedOnCritDur: 3 } }"),
    ('warlock', 2, "{ key: 'v2c', name: 'Shadow Bolt', type: 'active', desc: '150% atk + heal 25% of damage. CD 3.', ability: { dmgMult: 1.5, lifestealOnce: 0.25, cd: 3 } }"),
    ('warlock', 3, "{ key: 'v3c', name: 'Corruption', type: 'active', desc: '120% atk + dot 12/4 turns. CD 4.', ability: { dmgMult: 1.2, dot: 12, dur: 4, cd: 4 } }"),
    ('warlock', 4, "{ key: 'v4c', name: 'Hex Mark', type: 'passive', desc: 'Each consecutive hit on same target: +15% damage.', effect: { markOnHit: 0.15 } }"),
    ('warlock', 5, "{ key: 'v5c', name: 'Soul Burn', type: 'active', desc: '210% atk + heal 40% of damage. CD 5.', ability: { dmgMult: 2.1, lifestealOnce: 0.40, cd: 5 } }"),
    ('warlock', 6, "{ key: 'v6c', name: 'Curse of Doom', type: 'passive', desc: 'Below 30% HP: +40% damage.', effect: { lowHpDmg: 0.40, lowHpThreshold: 0.30 } }"),
    ('warlock', 7, "{ key: 'v7c', name: 'Death Coil', type: 'active', desc: '240% atk + heal 30% maxHP. CD 7.', ability: { dmgMult: 2.4, heal: 0.30, cd: 7 } }"),
    ('warlock', 8, "{ key: 'v8c', name: 'Soul Reaper', type: 'passive', desc: 'Executes enemies below 25% HP.', effect: {}, override: { proc: 'execute', val: 0.25 } }"),
    ('warlock', 9, "{ key: 'v9c', name: 'Demon Lord', type: 'passive', desc: '15% lifesteal + +18% crit.', effect: { lifesteal: 0.15, critBonus: 0.18 } }"),
    ('warlock', 10, "{ key: 'v10c', name: 'Chaos Bolt', type: 'active', desc: '500% atk · ignores 80% def. CD 10.', ability: { dmgMult: 5, armorPen: 0.8, cd: 10 } }"),
]

# Group by class for stats
print(f'=== Adding {len(NEW_TALENTS)} new talents ===')

# For each new talent, find the corresponding tier in the file and append it.
# The tier format is:
#   [ { key: '<prefix><N>a', ... },
#     { key: '<prefix><N>b', ... } ],
# We need to insert the new option before the closing ` ]`.

PREFIX = {
    'warrior': 'k', 'paladin': 'c', 'mage': 'e', 'necromancer': 'h',
    'hunter': 'a', 'shaman': 's', 'thief': 'l', 'druid': 'd', 'warlock': 'v'
}

ok = fail = 0
for cls, tier, new_talent in NEW_TALENTS:
    p = PREFIX[cls]
    key_b = f"'{p}{tier}b'"
    # The line containing the 'b' talent ends with " ] ],"  closing both the inner array
    # and ending the tier. Find that line and inject before the inner closing bracket.
    # Pattern: find the 'b' talent definition, then the next ' ] ],' or ' ] ]' (last tier)
    # Use a regex over a single tier block: '[ { key: XaY..., ... },
    #                                          { key: XbY..., ... } ],'
    # Replace with the same but with a 3rd entry inserted before ' ],'
    pattern = re.compile(
        r"(\[ \{ key: '" + p + str(tier) + r"a',[^\}]+\} \},\s*\n\s+\{ key: '" + p + str(tier) + r"b',[^\}]+\} \})\s*\](,?)",
        re.MULTILINE
    )
    m = pattern.search(s)
    if not m:
        # Try alternative pattern (some tiers have different whitespace)
        # Loosen: match across multiline with non-greedy
        pattern2 = re.compile(
            r"(\[ \{ key: '" + p + str(tier) + r"a',[\s\S]+?\} \},[\s\S]+?\{ key: '" + p + str(tier) + r"b',[\s\S]+?\} \})\s*\](,?)",
            re.MULTILINE
        )
        m = pattern2.search(s)
    if not m:
        print(f'  MISS {cls} t{tier}')
        fail += 1
        continue
    # Build replacement preserving indentation
    new_block = m.group(1) + ',\n        ' + new_talent + ' ]' + m.group(2)
    s = s[:m.start()] + new_block + s[m.end():]
    ok += 1
    print(f'  OK   {cls} t{tier}')

with open(PATH, 'w', encoding='utf-8') as f:
    f.write(s)
print(f'\n=== Done: {ok} ok, {fail} fail ===')
