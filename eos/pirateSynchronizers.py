def applyPirateBonuses(fit, module, family, count, **kwargs):
    """Apply local pirate traits after the caller validates the fitted rig.

    Run during the early effect pass so normal overheat effects consume the
    enhanced overload attributes regardless of fitted-module order.
    """
    bonus = 5 + count
    majorBonus = 10 + count
    if family == 'Dark Blood':
        fit.ship.boostItemAttr('rechargeRate', 200, **kwargs)
        for group, amount in (('Energy Neutralizer', 'energyNeutralizerAmount'),
                              ('Energy Nosferatu', 'powerTransferAmount')):
            matching = lambda mod, group=group: mod.item.group.name == group
            fit.modules.filteredItemBoost(matching, amount, majorBonus, **kwargs)
            fit.modules.filteredItemBoost(matching, 'overloadSelfDurationBonus', majorBonus, **kwargs)
            for attr in ('maxRange', 'falloffEffectiveness'):
                fit.modules.filteredItemBoost(matching, attr, bonus, **kwargs)
        fit.modules.filteredItemBoost(
            lambda mod: mod.item.group.name == 'Energy Weapon',
            'damageMultiplier', bonus, **kwargs)
    elif family == 'Domination':
        for attr in ('shieldCapacity', 'armorHP', 'hp'):
            fit.ship.boostItemAttr(attr, -30, **kwargs)
        fit.ship.boostItemAttr('signatureRadius', -majorBonus, **kwargs)
        fit.ship.boostItemAttr('warpSpeedMultiplier', bonus, **kwargs)
        for attr, amount in (('falloff', majorBonus), ('damageMultiplier', bonus)):
            fit.modules.filteredItemBoost(
                lambda mod: mod.item.group.name == 'Projectile Weapon', attr, amount, **kwargs)
    elif family == 'Dread Guristas':
        fit.extraAttributes.boost('droneControlRange', -60, **kwargs)
        for attr in ('damageMultiplier', 'shieldCapacity', 'armorHP', 'hp'):
            fit.drones.filteredItemBoost(
                lambda drone: drone.item.requiresSkill('Drones'), attr, majorBonus, **kwargs)
        for damageType in ('Em', 'Thermal', 'Kinetic', 'Explosive'):
            fit.ship.boostItemAttr('shield{}DamageResonance'.format(damageType), -bonus, **kwargs)
        for attr in ('maxRange', 'scanRadarStrengthBonus', 'scanLadarStrengthBonus',
                     'scanMagnetometricStrengthBonus', 'scanGravimetricStrengthBonus'):
            fit.modules.filteredItemBoost(
                lambda mod: mod.item.group.name == 'ECM', attr, bonus, **kwargs)
    elif family == 'Shadow Serpentis':
        fit.ship.boostItemAttr('maxTargetRange', -60, **kwargs)
        fit.ship.boostItemAttr('stasisWebifierResistance', -majorBonus, **kwargs)
        fit.ship.boostItemAttr('maxVelocity', bonus, **kwargs)
        for attr, amount in (('falloff', majorBonus), ('damageMultiplier', bonus)):
            fit.modules.filteredItemBoost(
                lambda mod: mod.item.group.name == 'Hybrid Weapon', attr, amount, **kwargs)
    elif family == 'True Sansha':
        afterburners = lambda mod: mod.item.requiresSkill('Afterburner')
        fit.modules.filteredItemBoost(afterburners, 'capacitorNeed', 400, **kwargs)
        # Shares module speedFactor stacking with overload, not the ship velocity
        # pool used by nanofibers/overdrives (Phantasm demo, video 26:35).
        fit.modules.filteredItemBoost(
            afterburners, 'speedFactor', majorBonus, stackingPenalties=True, **kwargs)
        fit.modules.filteredItemBoost(afterburners, 'overloadSpeedFactorBonus', majorBonus, **kwargs)
        for attr in ('damageMultiplier', 'trackingSpeed'):
            fit.modules.filteredItemBoost(
                lambda mod: mod.item.group.name == 'Energy Weapon', attr, bonus, **kwargs)
