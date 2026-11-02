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
    'Modeled: fixed -60% maximum targeting range; +10% stasis webifier resistance (web effectiveness reduction) '
    'and hybrid turret falloff; +5% hybrid turret damage and ship maximum velocity.',
    'Modeled: fixed +400% afterburner activation capacitor cost (5 times original cost); '
    '+10% afterburner velocity bonus and overheating benefits; +5% energy turret damage and tracking.',
)

EXPERIMENTAL_WARNING = (
    'EXPERIMENTAL PREVIEW: non-final fitting data from the Fractured Skies development reference '
    '(pages 5-13) and desktop screenshot Screenshot_20261101_214353.png. '
    'Fit at most one Synchronizer across all families and sizes. '
    'Each exact matching-faction module adds one percentage point to modeled positive bonus magnitudes '
    '(including beneficial reductions); fixed pirate penalties do not scale. '
    'Officer/deadspace affiliation alone and mutaplasmid-modified modules do not count. '
    'All Synchronizers are reported to reduce CPU output, but the amount and skill mitigation are unverified '
    'and NOT modeled. Calibration, skill prerequisites (including Synchronizer Rigging), other unverified '
    'size-specific fitting details, and build/LP costs are omitted, not verified as zero. '
    'Results therefore overstate fitting feasibility and may omit important penalties. '
)
