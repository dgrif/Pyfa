"""Private identifiers and verified preview data for experimental Synchronizer rigs."""

FAMILIES = (
    'Federation Navy',
    'Imperial Navy',
    'Republic Fleet',
    'Caldari Navy',
    'Dark Blood',
    'Domination',
    'Dread Guristas',
    'Shadow Serpentis',
    'True Sansha',
)
TYPE_ID_BASE = 1001000
GROUP_ID = 1001000
EFFECT_ID = 100300

# Descriptions deliberately distinguish verified effects from unavailable preview data.
FAMILY_DESCRIPTIONS = (
    'Modeled: +5% hybrid weapon damage and tracking, armor repairer amount, and structure hitpoints.',
    'Modeled: +5% energy turret damage, maximum capacitor amount and armor hitpoints; '
    '-5% energy turret activation capacitor cost.',
    'Modeled: +5% projectile turret damage and tracking and ship maximum velocity; -5% shield booster cycle time.',
    'Modeled: +5% missile damage and maximum velocity, shield hitpoints, and maximum targeting range.',
    'Modeled: fixed +200% capacitor recharge time (3 times original time); +10% neutralizer and Nosferatu '
    'drain amount and overheating benefits; +5% neutralizer and Nosferatu optimal range and effectiveness '
    'falloff; +5% energy turret damage.',
    'Modeled: fixed -30% shield, armor and structure hitpoints; -10% signature radius; '
    '+10% projectile turret falloff; +5% projectile turret damage and warp speed.',
    'Modeled: fixed -60% drone control range; +10% drone damage and all drone hitpoint layers; '
    '+5% shield resistances (damage resonance reduction), ECM strength and ECM optimal range.',
    'Modeled: fixed -60% maximum targeting range (reproduces 43.75 km on the complete video Proteus fit); '
    '+10% stasis webifier resistance (web effectiveness reduction) '
    'and hybrid turret falloff; +5% hybrid turret damage and ship maximum velocity.',
    'Modeled: fixed +400% afterburner activation capacitor cost (5 times original cost); '
    '+10% afterburner velocity bonus and overheating benefits; +5% energy turret damage and tracking.',
)

EXPERIMENTAL_WARNING = (
    'EXPERIMENTAL PREVIEW: non-final fitting data from the Fractured Skies video and '
    'Fractured-Skies-All-Stats.pdf (pages 6-15). '
    'Fit at most one Synchronizer across all families and sizes. '
    'Each exact matching-faction module adds one percentage point to modeled positive bonus magnitudes '
    '(including beneficial reductions); fixed pirate penalties do not scale. '
    'Officer/deadspace affiliation alone and mutaplasmid-modified modules do not count. '
    'The shown -10% CPU output drawback is modeled without Synchronizer Rigging mitigation, whose exact '
    'formula is unverified and NOT modeled. Volume 5 m3, structure 40 HP, Tech 1 and Meta 8 are shown on '
    'the four empire and True Sansha medium rigs; these values are assumed for the other families and sizes. '
    'Calibration cost is provisionally set to 250 for every family and size; this value is unverified. '
    'Bonuses follow existing module/rig stacking conventions where equivalent effects exist. '
    'Shadow Serpentis damage stacking and True Sansha afterburner heat stacking reproduce the video; '
    'other stacking interactions are inferred, not confirmed preview data. '
    'Skill prerequisites (including Synchronizer Rigging), other unverified '
    'size-specific fitting details, and build/LP costs are omitted, not verified as zero. '
    'Results are not authoritative and may omit important fitting restrictions. '
)
