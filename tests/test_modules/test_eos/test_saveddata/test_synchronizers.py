import os
import sys

import pytest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))
sys._called_from_test = True

import eos.db
from eos.const import FittingModuleState
from eos.gamedata import Item
from eos.saveddata.cargo import Cargo
from eos.saveddata.drone import Drone
from eos.saveddata.fit import Fit
from eos.saveddata.module import Module
from eos.saveddata.ship import Ship
from eos.synchronizers import FAMILIES, TYPE_ID_BASE


SHIP_ATTRIBUTES = (
    'hp', 'armorHP', 'shieldCapacity', 'capacitorCapacity',
    'maxVelocity', 'maxTargetRange', 'signatureRadius', 'rechargeRate',
    'warpSpeedMultiplier', 'stasisWebifierResistance',
    'shieldEmDamageResonance', 'shieldThermalDamageResonance',
    'shieldKineticDamageResonance', 'shieldExplosiveDamageResonance')


def make_fit(family, size=0):
    ship_name = ('Rifter', 'Rupture', 'Typhoon')[size]
    fit = Fit(Ship(eos.db.getItem(ship_name)), 'Experimental Synchronizer regression')
    rig = Module(eos.db.getItem(TYPE_ID_BASE + FAMILIES.index(family) * 3 + size))
    fit.modules.append(rig)
    return fit, rig


def add_module(fit, name, state=FittingModuleState.ONLINE):
    module = Module(eos.db.getItem(name))
    module.state = state
    fit.modules.append(module)
    return module


def add_faction_module(fit, family):
    # Pick a real high/mid/low-slot faction item; keeping it offline isolates
    # Synchronizer scaling from that module's own passive modifiers.
    items = eos.db.get_gamedata_session().query(Item).filter(
        Item.typeName.startswith(family + ' ')).order_by(Item.typeID).all()
    item = next(item for item in items if {'hiPower', 'medPower', 'loPower'}.intersection(item.effects))
    return add_module(fit, item.ID, FittingModuleState.OFFLINE)


def recalculate(fit):
    fit.clear()
    fit.calculateModifiedAttributes()


def ship_snapshot(fit):
    return {attr: fit.ship.getModifiedItemAttr(attr) for attr in SHIP_ATTRIBUTES}


def ship_factors(family, count):
    factors = dict.fromkeys(SHIP_ATTRIBUTES, 1)
    bonus = (5 + count) / 100
    if family == 'Federation Navy':
        factors['hp'] = 1 + bonus
    elif family == 'Imperial Navy':
        factors['armorHP'] = factors['capacitorCapacity'] = 1 + bonus
    elif family == 'Republic Fleet':
        factors['maxVelocity'] = 1 + bonus
    elif family == 'Caldari Navy':
        factors['shieldCapacity'] = factors['maxTargetRange'] = 1 + bonus
    elif family == 'Domination':
        factors['signatureRadius'] = 1 - (10 + count) / 100
        factors['hp'] = factors['armorHP'] = factors['shieldCapacity'] = 0.7
        factors['warpSpeedMultiplier'] = 1 + bonus
    elif family == 'Dark Blood':
        factors['rechargeRate'] = 3
    elif family == 'Dread Guristas':
        for damage_type in ('Em', 'Thermal', 'Kinetic', 'Explosive'):
            factors['shield{}DamageResonance'.format(damage_type)] = 1 - bonus
    elif family == 'Shadow Serpentis':
        factors['maxTargetRange'] = 0.4
        factors['maxVelocity'] = 1 + bonus
        factors['stasisWebifierResistance'] = 1 - (10 + count) / 100
    return factors


@pytest.mark.parametrize('family', FAMILIES)
@pytest.mark.parametrize('size', (0, 1, 2))
def test_ship_bonuses_scale_with_fitted_offline_modules_and_reset(family, size):
    fit, rig = make_fit(family, size)
    rig.state = FittingModuleState.OFFLINE
    recalculate(fit)
    baseline = ship_snapshot(fit)

    rig.state = FittingModuleState.ONLINE
    recalculate(fit)
    assert ship_snapshot(fit) == pytest.approx({
        attr: value * ship_factors(family, 0)[attr] for attr, value in baseline.items()})

    faction_module = add_faction_module(fit, family)
    recalculate(fit)
    assert ship_snapshot(fit) == pytest.approx({
        attr: value * ship_factors(family, 1)[attr] for attr, value in baseline.items()})

    fit.modules.remove(faction_module)
    recalculate(fit)
    assert ship_snapshot(fit) == pytest.approx({
        attr: value * ship_factors(family, 0)[attr] for attr, value in baseline.items()})

    rig.state = FittingModuleState.OFFLINE
    recalculate(fit)
    assert ship_snapshot(fit) == pytest.approx(baseline)


@pytest.mark.parametrize('family', FAMILIES[:4])
def test_empire_module_and_charge_bonuses_do_not_leak(family):
    fit, rig = make_fit(family, 2)
    hybrid = add_module(fit, '75mm Gatling Rail II')
    hybrid.charge = eos.db.getItem('Antimatter Charge S')
    energy = add_module(fit, 'Dual Light Pulse Laser II')
    projectile = add_module(fit, '125mm Gatling AutoCannon II')
    launcher = add_module(fit, 'Light Missile Launcher II')
    launcher.charge = eos.db.getItem('Scourge Light Missile')
    armor = add_module(fit, 'Small Armor Repairer II')
    ancillary_armor = add_module(fit, 'Small Ancillary Armor Repairer')
    remote_armor = add_module(fit, 'Small Remote Armor Repairer II')
    shield = add_module(fit, 'Small Shield Booster II')
    ancillary_shield = add_module(fit, 'Small Ancillary Shield Booster')
    targets = (
        (hybrid, 'damageMultiplier'), (hybrid, 'trackingSpeed'),
        (energy, 'damageMultiplier'), (energy, 'capacitorNeed'),
        (projectile, 'damageMultiplier'), (projectile, 'trackingSpeed'),
        (armor, 'armorDamageAmount'), (ancillary_armor, 'armorDamageAmount'),
        (remote_armor, 'armorDamageAmount'), (shield, 'duration'), (ancillary_shield, 'duration'),
        (hybrid, 'cpu'), (energy, 'cpu'), (projectile, 'cpu'), (launcher, 'cpu'))
    rig.state = FittingModuleState.OFFLINE
    recalculate(fit)
    baseline = [module.getModifiedItemAttr(attr) for module, attr in targets]
    charge_baseline = {attr: launcher.getModifiedChargeAttr(attr) for attr in (
        'emDamage', 'thermalDamage', 'kineticDamage', 'explosiveDamage', 'maxVelocity')}
    hybrid_charge_baseline = hybrid.getModifiedChargeAttr('kineticDamage')
    rig.state = FittingModuleState.ONLINE
    add_faction_module(fit, family)
    recalculate(fit)

    expected = {
        'Federation Navy': {0: 1.06, 1: 1.06, 6: 1.06},
        'Imperial Navy': {2: 1.06, 3: 0.94},
        'Republic Fleet': {4: 1.06, 5: 1.06, 9: 0.94},
        'Caldari Navy': {}}
    for index, (module, attr) in enumerate(targets):
        assert module.getModifiedItemAttr(attr) == pytest.approx(
            baseline[index] * expected[family].get(index, 1))
    charge_factor = 1.06 if family == 'Caldari Navy' else 1
    for attr, value in charge_baseline.items():
        assert launcher.getModifiedChargeAttr(attr) == pytest.approx(value * charge_factor)
    assert hybrid.getModifiedChargeAttr('kineticDamage') == pytest.approx(hybrid_charge_baseline)


def test_dread_guristas_drone_layers_scale_but_control_penalty_does_not():
    fit, rig = make_fit('Dread Guristas')
    drone = Drone(eos.db.getItem('Hobgoblin II'))
    drone.amount = drone.amountActive = 1
    fit.drones.append(drone)
    rig.state = FittingModuleState.OFFLINE
    recalculate(fit)
    attributes = ('damageMultiplier', 'shieldCapacity', 'armorHP', 'hp')
    baseline = {attr: drone.getModifiedItemAttr(attr) for attr in attributes}
    control_range = fit.extraAttributes['droneControlRange']
    assert control_range > 0
    rig.state = FittingModuleState.ONLINE
    for count in (0, 1):
        if count:
            add_faction_module(fit, 'Dread Guristas')
        recalculate(fit)
        for attr, value in baseline.items():
            assert drone.getModifiedItemAttr(attr) == pytest.approx(value * (1.1 + count / 100))
        assert fit.extraAttributes['droneControlRange'] == pytest.approx(control_range * 0.4)
    rig.state = FittingModuleState.OFFLINE
    recalculate(fit)
    for attr, value in baseline.items():
        assert drone.getModifiedItemAttr(attr) == pytest.approx(value)
    assert fit.extraAttributes['droneControlRange'] == pytest.approx(control_range)


def test_true_sansha_fixed_penalty_only_affects_afterburners():
    fit, rig = make_fit('True Sansha', 2)
    afterburner = add_module(fit, '1MN Afterburner II')
    microwarpdrive = add_module(fit, '5MN Microwarpdrive II')
    rig.state = FittingModuleState.OFFLINE
    recalculate(fit)
    ab_cost = afterburner.getModifiedItemAttr('capacitorNeed')
    mwd_cost = microwarpdrive.getModifiedItemAttr('capacitorNeed')
    rig.state = FittingModuleState.ONLINE
    for count in (0, 1):
        if count:
            add_faction_module(fit, 'True Sansha')
        recalculate(fit)
        assert afterburner.getModifiedItemAttr('capacitorNeed') == pytest.approx(ab_cost * 5)
        assert microwarpdrive.getModifiedItemAttr('capacitorNeed') == pytest.approx(mwd_cost)


def test_faction_ammunition_drones_cargo_and_mutations_do_not_count():
    fit, rig = make_fit('Federation Navy', 2)
    hybrid = add_module(fit, '75mm Gatling Rail II')
    hybrid.charge = eos.db.getItem('Federation Navy Antimatter Charge S')
    drone = Drone(eos.db.getItem('Federation Navy Hobgoblin'))
    drone.amount = drone.amountActive = 1
    fit.drones.append(drone)
    cargo = Cargo(eos.db.getItem('Federation Navy Stasis Webifier'))
    cargo.amount = 1
    fit.cargo.append(cargo)
    base = eos.db.getItem('Federation Navy Stasis Webifier')
    mutaplasmid = base.mutaplasmids[0]
    mutated = Module(mutaplasmid.resultingItem, base, mutaplasmid)
    mutated.state = FittingModuleState.OFFLINE
    fit.modules.append(mutated)
    rig.state = FittingModuleState.OFFLINE
    recalculate(fit)
    hull = fit.ship.getModifiedItemAttr('hp')
    rig.state = FittingModuleState.ONLINE
    recalculate(fit)
    assert fit.ship.getModifiedItemAttr('hp') == pytest.approx(hull * 1.05)
    ordinary = add_module(fit, base.ID, FittingModuleState.OFFLINE)
    recalculate(fit)
    assert fit.ship.getModifiedItemAttr('hp') == pytest.approx(hull * 1.06)
    fit.modules.remove(ordinary)
    recalculate(fit)
    assert fit.ship.getModifiedItemAttr('hp') == pytest.approx(hull * 1.05)


def test_deadspace_affiliation_does_not_count_as_faction_name():
    fit, rig = make_fit('Domination')
    add_module(fit, 'Gistii A-Type Small Shield Booster', FittingModuleState.OFFLINE)
    rig.state = FittingModuleState.OFFLINE
    recalculate(fit)
    signature = fit.ship.getModifiedItemAttr('signatureRadius')
    rig.state = FittingModuleState.ONLINE
    recalculate(fit)
    assert fit.ship.getModifiedItemAttr('signatureRadius') == pytest.approx(signature * 0.9)
    add_faction_module(fit, 'Domination')
    recalculate(fit)
    assert fit.ship.getModifiedItemAttr('signatureRadius') == pytest.approx(signature * 0.89)


@pytest.mark.parametrize('family', FAMILIES)
def test_synchronizer_does_not_project_to_another_fit(family):
    source, rig = make_fit(family)
    target = Fit(Ship(eos.db.getItem('Rifter')), 'Projection target')
    recalculate(source)
    recalculate(target)
    baseline = ship_snapshot(target)
    target.register(rig, origin=source)
    for runtime in ('early', 'normal', 'late'):
        rig.calculateModifiedAttributes(target, runtime, forceProjected=True)
    assert ship_snapshot(target) == pytest.approx(baseline)
    projected_rig = Module(rig.item)
    target.projectedModules.append(projected_rig)
    recalculate(target)
    assert ship_snapshot(target) == pytest.approx(baseline)


@pytest.mark.parametrize('size', (0, 1, 2))
def test_rig_size_and_one_per_ship_limit_apply_across_families(size):
    fit, rig = make_fit('Federation Navy', size)
    recalculate(fit)
    assert rig.fits(fit)
    wrong_size = Module(eos.db.getItem(TYPE_ID_BASE + (size + 1) % 3))
    assert not wrong_size.fits(fit)
    second_family = Module(eos.db.getItem(TYPE_ID_BASE + 3 + size))
    assert not second_family.fits(fit)
    rig.state = FittingModuleState.OFFLINE
    assert not second_family.fits(fit)
    fit.modules.remove(rig)
    assert second_family.fits(fit)


@pytest.mark.parametrize('family', FAMILIES[4:])
@pytest.mark.parametrize('rig_last', (False, True))
def test_pirate_module_traits_scale_without_leaking(family, rig_last):
    fit, rig = make_fit(family, 2)
    modules = {
        'hybrid': add_module(fit, '75mm Gatling Rail II'),
        'energy': add_module(fit, 'Dual Light Pulse Laser II'),
        'projectile': add_module(fit, '125mm Gatling AutoCannon II'),
        'neut': add_module(fit, 'Small Energy Neutralizer II'),
        'nos': add_module(fit, 'Small Energy Nosferatu II'),
        'remote_cap': add_module(fit, 'Small Remote Capacitor Transmitter II'),
        'ab': add_module(fit, '1MN Afterburner II'),
        'mwd': add_module(fit, '5MN Microwarpdrive II'),
        'ecm': add_module(fit, 'Multispectral ECM II'),
        'burst': add_module(fit, 'Burst Jammer II'),
        'web': add_module(fit, 'Stasis Webifier II')}
    targets = []
    for name in ('hybrid', 'energy', 'projectile'):
        targets.extend((name, attr) for attr in ('damageMultiplier', 'falloff', 'trackingSpeed'))
    for name, amount in (('neut', 'energyNeutralizerAmount'), ('nos', 'powerTransferAmount')):
        targets.extend((name, attr) for attr in (
            amount, 'maxRange', 'falloffEffectiveness', 'duration', 'overloadSelfDurationBonus'))
    targets.append(('remote_cap', 'powerTransferAmount'))
    for name in ('ab', 'mwd'):
        targets.extend((name, attr) for attr in (
            'capacitorNeed', 'speedFactor', 'overloadSpeedFactorBonus'))
    for name in ('ecm', 'burst'):
        targets.extend((name, 'scan{}StrengthBonus'.format(sensor)) for sensor in (
            'Radar', 'Ladar', 'Magnetometric', 'Gravimetric'))
    targets.extend((('ecm', 'maxRange'), ('web', 'speedFactor')))
    if rig_last:
        fit.modules.remove(rig)
        fit.modules.append(rig)
    rig.state = FittingModuleState.OFFLINE
    recalculate(fit)
    baseline = {key: modules[key[0]].getModifiedItemAttr(key[1]) for key in targets}
    rig.state = FittingModuleState.ONLINE
    for count in (0, 1, 2):
        if count:
            add_faction_module(fit, family)
        recalculate(fit)
        expected = {}
        small, large = 1 + (5 + count) / 100, 1 + (10 + count) / 100
        if family == 'Dark Blood':
            expected['energy', 'damageMultiplier'] = small
            for name, amount in (('neut', 'energyNeutralizerAmount'), ('nos', 'powerTransferAmount')):
                expected[name, amount] = expected[name, 'overloadSelfDurationBonus'] = large
                expected[name, 'maxRange'] = expected[name, 'falloffEffectiveness'] = small
        elif family in ('Domination', 'Shadow Serpentis'):
            weapon = 'projectile' if family == 'Domination' else 'hybrid'
            expected[weapon, 'damageMultiplier'] = small
            expected[weapon, 'falloff'] = large
        elif family == 'Dread Guristas':
            for sensor in ('Radar', 'Ladar', 'Magnetometric', 'Gravimetric'):
                expected['ecm', 'scan{}StrengthBonus'.format(sensor)] = small
            expected['ecm', 'maxRange'] = small
        elif family == 'True Sansha':
            expected['ab', 'capacitorNeed'] = 5
            expected['ab', 'speedFactor'] = expected['ab', 'overloadSpeedFactorBonus'] = large
            expected['energy', 'damageMultiplier'] = expected['energy', 'trackingSpeed'] = small
        for key, value in baseline.items():
            assert modules[key[0]].getModifiedItemAttr(key[1]) == pytest.approx(
                value * expected.get(key, 1)), key
    rig.state = FittingModuleState.OFFLINE
    recalculate(fit)
    for key, value in baseline.items():
        assert modules[key[0]].getModifiedItemAttr(key[1]) == pytest.approx(value), key


@pytest.mark.parametrize('family', ('Dark Blood', 'True Sansha'))
@pytest.mark.parametrize('rig_last', (False, True))
def test_pirate_heat_bonuses_only_change_overheated_benefits(family, rig_last):
    fit, rig = make_fit(family, 2)
    neut = add_module(fit, 'Small Energy Neutralizer II', FittingModuleState.ACTIVE)
    nos = add_module(fit, 'Small Energy Nosferatu II', FittingModuleState.ACTIVE)
    afterburner = add_module(fit, '1MN Afterburner II', FittingModuleState.ACTIVE)
    mwd = add_module(fit, '5MN Microwarpdrive II', FittingModuleState.ACTIVE)
    if rig_last:
        fit.modules.remove(rig)
        fit.modules.append(rig)
    modules = (neut, nos, afterburner, mwd)
    rig.state = FittingModuleState.OFFLINE
    recalculate(fit)
    durations = {mod: mod.getModifiedItemAttr('duration') for mod in (neut, nos)}
    speeds = {mod: mod.getModifiedItemAttr('speedFactor') for mod in (afterburner, mwd)}
    heat = {neut: neut.getModifiedItemAttr('overloadSelfDurationBonus'),
            nos: nos.getModifiedItemAttr('overloadSelfDurationBonus'),
            afterburner: afterburner.getModifiedItemAttr('overloadSpeedFactorBonus'),
            mwd: mwd.getModifiedItemAttr('overloadSpeedFactorBonus')}
    assert heat[neut] < 0 and heat[nos] < 0
    assert heat[afterburner] > 0
    for count in (0, 1):
        if count:
            add_faction_module(fit, family)
        rig.state = FittingModuleState.ONLINE
        recalculate(fit)
        factor = 1 + (10 + count) / 100
        for mod, value in durations.items():
            assert mod.getModifiedItemAttr('duration') == pytest.approx(value)
        for mod, value in speeds.items():
            speed_factor = factor if family == 'True Sansha' and mod is afterburner else 1
            assert mod.getModifiedItemAttr('speedFactor') == pytest.approx(value * speed_factor)
        for mod in modules:
            mod.state = FittingModuleState.OVERHEATED
        recalculate(fit)
        for mod, value in durations.items():
            heat_factor = factor if family == 'Dark Blood' else 1
            assert mod.getModifiedItemAttr('duration') == pytest.approx(
                value * (1 + heat[mod] * heat_factor / 100))
        for mod, value in speeds.items():
            speed_factor = factor if family == 'True Sansha' and mod is afterburner else 1
            assert mod.getModifiedItemAttr('speedFactor') == pytest.approx(
                value * speed_factor * (1 + heat[mod] * speed_factor / 100))
        rig.state = FittingModuleState.OFFLINE
        recalculate(fit)
        for mod, value in durations.items():
            assert mod.getModifiedItemAttr('duration') == pytest.approx(value * (1 + heat[mod] / 100))
        for mod, value in speeds.items():
            assert mod.getModifiedItemAttr('speedFactor') == pytest.approx(value * (1 + heat[mod] / 100))
        for mod in modules:
            mod.state = FittingModuleState.ACTIVE


@pytest.mark.parametrize('state', (FittingModuleState.ACTIVE, FittingModuleState.OVERHEATED))
@pytest.mark.parametrize('speed_modules', (False, True))
def test_sansha_propulsion_bonus_is_not_penalized_by_speed_modules(state, speed_modules):
    fit, rig = make_fit('True Sansha', 2)
    if speed_modules:
        add_module(fit, 'Nanofiber Internal Structure II')
        add_module(fit, 'Overdrive Injector System II')
    afterburner = add_module(fit, '1MN Afterburner II')
    fit.modules.remove(rig)
    fit.modules.append(rig)
    rig.state = FittingModuleState.OFFLINE
    recalculate(fit)
    unpropelled_speed = fit.ship.getModifiedItemAttr('maxVelocity')
    afterburner.state = state
    recalculate(fit)
    normal_speed = fit.ship.getModifiedItemAttr('maxVelocity')
    normal_bonus = afterburner.getModifiedItemAttr('speedFactor')
    rig.state = FittingModuleState.ONLINE
    recalculate(fit)
    enhanced_bonus = afterburner.getModifiedItemAttr('speedFactor')
    assert enhanced_bonus > normal_bonus
    assert fit.ship.getModifiedItemAttr('maxVelocity') == pytest.approx(
        unpropelled_speed + (normal_speed - unpropelled_speed) * enhanced_bonus / normal_bonus)


@pytest.mark.parametrize('count', (0, 1))
def test_shadow_resists_incoming_webs_without_strengthening_outgoing_webs(count):
    fit, rig = make_fit('Shadow Serpentis')
    for _ in range(count):
        add_faction_module(fit, 'Shadow Serpentis')
    outgoing = add_module(fit, 'Stasis Webifier II', FittingModuleState.ACTIVE)
    incoming = Module(eos.db.getItem('Stasis Webifier II'))
    incoming.state = FittingModuleState.ACTIVE
    rig.state = FittingModuleState.OFFLINE
    recalculate(fit)
    outgoing_strength = outgoing.getModifiedItemAttr('speedFactor')
    ordinary_speed = fit.ship.getModifiedItemAttr('maxVelocity')
    fit.projectedModules.append(incoming)
    recalculate(fit)
    webbed_speed = fit.ship.getModifiedItemAttr('maxVelocity')
    assert webbed_speed < ordinary_speed
    rig.state = FittingModuleState.ONLINE
    recalculate(fit)
    velocity_factor = 1 + (5 + count) / 100
    resistance_factor = 1 - (10 + count) / 100
    assert fit.ship.getModifiedItemAttr('maxVelocity') == pytest.approx(
        (ordinary_speed + (webbed_speed - ordinary_speed) * resistance_factor) * velocity_factor)
    assert outgoing.getModifiedItemAttr('speedFactor') == pytest.approx(outgoing_strength)
