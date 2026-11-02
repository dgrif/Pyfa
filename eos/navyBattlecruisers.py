"""Local, explicitly experimental Fractured Skies navy battlecruiser data."""

EFFECT_ID = 100400
GROUP_ID = 1201

EXPERIMENTAL_WARNING = (
    'LOCAL EXPERIMENTAL PREVIEW — not official game data. '
    'Documented layouts, hardpoints, bonuses and observed raw-stat changes from the Fractured Skies video '
    'and Fractured-Skies-All-Stats.pdf are applied. '
    'Other raw attributes retain the T1 values; unshown navy values remain unverified fallbacks. '
    'Skill prerequisites are inherited approximations. No blanket HP or speed increase is guessed. ')

HULLS = (
    {
        'typeID': 1001100,
        'baseTypeID': 4302,
        'name': 'Oracle Navy Issue [Experimental]',
        'skill': 'Amarr Battlecruiser',
        'slots': (7, 3, 7),
        'turrets': 6,
        'launchers': 0,
        'attributes': {
            'shieldCapacity': 2000, 'armorHP': 2700, 'hp': 2500, 'powerOutput': 1200,
            'maxVelocity': 225, 'agility': 0.47, 'maxTargetRange': 70000,
            'scanResolution': 230, 'scanRadarStrength': 22,
        },
        'description': (
            'Raw-stat changes: video 02:00 and 02:30. Maximum locked targets is unshown and retains the T1 Oracle '
            'fallback. Layout: 7 high / 3 mid / 7 low; 6 turret hardpoints and 1 utility high. '
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
        'attributes': {
            'shieldCapacity': 2200, 'armorHP': 2400, 'hp': 2750, 'maxVelocity': 265,
            'agility': 0.43, 'maxTargetRange': 75000, 'maxLockedTargets': 8,
            'scanResolution': 220, 'scanMagnetometricStrength': 25,
        },
        'description': (
            'Raw-stat changes: video 04:30. Base powergrid is unshown and retains the T1 Talos fallback. '
            'Layout: 7 high / 4 mid / 6 low; 6 turret hardpoints and 1 utility high. '
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
        'attributes': {'cpuOutput': 475, 'powerOutput': 650},
        'description': (
            'CPU and powergrid: video 07:15. Unshown HP, navigation, sensors, capacitor, targeting and cargo '
            'retain T1 Naga fallbacks; the spoken 100 km lock range does not establish a base value. '
            'Layout: 7 high / 7 mid / 3 low; 6 launcher hardpoints and 1 utility high. '
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
        'attributes': {
            'shieldCapacity': 2400, 'armorHP': 2250, 'hp': 2250, 'maxVelocity': 280,
            'agility': 0.52, 'maxTargetRange': 65000, 'maxLockedTargets': 7,
            'scanResolution': 240, 'scanLadarStrength': 21, 'capacity': 600,
            # One-MWD fit totals at max skills (08:55), divided by 1.25 with display rounding.
            'cpuOutput': 375, 'powerOutput': 865,
        },
        'description': (
            'Raw-stat changes: video 09:55; cargo from 08:55. CPU 375 tf and powergrid 865 MW are inferred '
            'from the one-MWD fit totals at max skills (08:55), not directly shown base values. '
            'Layout: 7 high / 6 mid / 4 low; 6 turret hardpoints and 1 utility high. '
            'Per Minmatar Battlecruiser level: Large Projectile Turret cycle time -10%, falloff +7.5%, '
            'Microwarpdrive signature-radius penalty -15% (not base signature radius). '
            'Role: Large Projectile Turret powergrid -95%, CPU -50%.'),
    },
)
