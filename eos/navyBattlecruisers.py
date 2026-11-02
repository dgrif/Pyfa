"""Local, explicitly experimental Fractured Skies navy battlecruiser data."""

EFFECT_ID = 100400
GROUP_ID = 1201

EXPERIMENTAL_WARNING = (
    'LOCAL EXPERIMENTAL PREVIEW — not official game data. '
    'Only the documented slot layout, weapon hardpoints and bonuses below are navy values. '
    'Every other raw hull attribute is copied unchanged from the T1 hull, not an actual navy stat: '
    'HP, resistances, fitting resources, capacitor, speed, mass, agility, targeting, cargo and drones. '
    'T1 rig size, rig slots, calibration and skill prerequisites are inherited approximations. '
    'No speculative HP or speed increase is applied. ')

HULLS = (
    {
        'typeID': 1001100,
        'baseTypeID': 4302,
        'name': 'Oracle Navy Issue [Experimental]',
        'skill': 'Amarr Battlecruiser',
        'slots': (7, 3, 7),
        'turrets': 6,
        'launchers': 0,
        'description': (
            'T1 fallback: Oracle. Layout: 7 high / 3 mid / 7 low; 6 turret hardpoints and 1 utility high. '
            'Per Amarr Battlecruiser level: Large Energy Turret damage +15%, optimal range +7.5%, '
            'activation capacitor cost -10%. Role: Large Energy Turret powergrid -95%, CPU -50%, '
            'activation capacitor cost -50% (multiplicative with the skill bonus).'),
    },
    {
        'typeID': 1001101,
        'baseTypeID': 4308,
        'name': 'Talos Navy Issue [Experimental]',
        'skill': 'Gallente Battlecruiser',
        'slots': (7, 4, 6),
        'turrets': 6,
        'launchers': 0,
        'description': (
            'T1 fallback: Talos. Layout: 7 high / 4 mid / 6 low; 6 turret hardpoints and 1 utility high. '
            'Per Gallente Battlecruiser level: Large Hybrid Turret damage +15%, falloff +7.5%, '
            'Armor Plate added mass -15%. Role: Large Hybrid Turret powergrid -95%, CPU -50%, '
            'activation capacitor cost -50%. No inherited T1 tracking bonus.'),
    },
    {
        'typeID': 1001102,
        'baseTypeID': 4306,
        'name': 'Naga Navy Issue [Experimental]',
        'skill': 'Caldari Battlecruiser',
        'slots': (7, 7, 3),
        'turrets': 0,
        'launchers': 6,
        'description': (
            'T1 fallback: Naga. Layout: 7 high / 7 mid / 3 low; 6 launcher hardpoints and 1 utility high. '
            'Per Caldari Battlecruiser level: Cruise Missile and Torpedo kinetic damage +10%, '
            'EM/thermal/explosive damage +5%, missile velocity +10%. Role: Cruise Missile and Torpedo '
            'launcher powergrid -95%, CPU -50%. No hybrid or rapid-heavy launcher bonuses.'),
    },
    {
        'typeID': 1001103,
        'baseTypeID': 4310,
        'name': 'Tornado Fleet Issue [Experimental]',
        'skill': 'Minmatar Battlecruiser',
        'slots': (7, 6, 4),
        'turrets': 6,
        'launchers': 0,
        'description': (
            'T1 fallback: Tornado. Layout: 7 high / 6 mid / 4 low; 6 turret hardpoints and 1 utility high. '
            'Per Minmatar Battlecruiser level: Large Projectile Turret cycle time -10%, falloff +7.5%, '
            'Microwarpdrive signature-radius penalty -15% (not base signature radius). '
            'Role: Large Projectile Turret powergrid -95%, CPU -50%.'),
    },
)
