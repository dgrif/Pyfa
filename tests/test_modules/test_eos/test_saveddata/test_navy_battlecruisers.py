import os
import sys

import pytest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))
sys._called_from_test = True

import eos.db
from eos.const import FittingHardpoint, FittingModuleState, FittingSlot
from eos.navyBattlecruisers import HULLS
from eos.saveddata.character import Character
from eos.saveddata.fit import Fit
from eos.saveddata.module import Module
from eos.saveddata.ship import Ship


WEAPONS = (
    'Mega Pulse Laser II', 'Neutron Blaster Cannon II',
    'Cruise Missile Launcher II', '800mm Repeating Cannon II')
TURRET_CASES = (
    (0, 'Heavy Pulse Laser II', {'damageMultiplier': 15, 'maxRange': 7.5, 'capacitorNeed': -10}),
    (1, 'Heavy Neutron Blaster II', {'damageMultiplier': 15, 'falloff': 7.5}),
    (3, '425mm AutoCannon II', {'speed': -10, 'falloff': 7.5}),
)


def make_fit(index, level=0, original=False):
    hull = HULLS[index]
    fit = Fit(Ship(eos.db.getItem(hull['baseTypeID'] if original else hull['typeID'])), 'Navy hull regression')
    fit.character = Character('Navy regression skills', defaultLevel=0, initSkills=False)
    fit.character.getSkill(hull['skill']).setLevel(level, ignoreRestrict=True)
    return fit


def add_module(fit, name, state=FittingModuleState.ONLINE, charge=None):
    module = Module(eos.db.getItem(name))
    module.state = state
    if charge is not None:
        module.charge = eos.db.getItem(charge)
    fit.modules.append(module)
    return module


def recalculate(fit):
    fit.clear()
    fit.calculateModifiedAttributes()


def assert_raw_factors(module, factors):
    for attr, factor in factors.items():
        assert module.getModifiedItemAttr(attr) == pytest.approx(module.item.getAttribute(attr, 0) * factor)


@pytest.mark.parametrize('index', range(4))
def test_six_weapons_and_utility_fit_without_an_extra_weapon_hardpoint(index):
    hull = HULLS[index]
    fit = make_fit(index, 5)
    recalculate(fit)
    for slot, count in zip((FittingSlot.HIGH, FittingSlot.MED, FittingSlot.LOW), hull['slots']):
        assert fit.getNumSlots(slot) == count
    for _ in range(6):
        weapon = Module(eos.db.getItem(WEAPONS[index]))
        assert weapon.fits(fit)
        fit.modules.append(weapon)
        recalculate(fit)
    assert fit.getSlotsFree(FittingSlot.HIGH.value) == 1
    assert not Module(eos.db.getItem(WEAPONS[index])).fits(fit)
    wrong_weapon = 'Mega Pulse Laser II' if index == 2 else 'Cruise Missile Launcher II'
    assert not Module(eos.db.getItem(wrong_weapon)).fits(fit)
    utility = Module(eos.db.getItem('Small Energy Neutralizer II'))
    assert utility.fits(fit)
    fit.modules.append(utility)
    recalculate(fit)
    assert fit.getSlotsFree(FittingSlot.HIGH.value) == 0
    assert not Module(eos.db.getItem('Small Energy Neutralizer II')).fits(fit)
    assert fit.getHardpointsFree(FittingHardpoint.MISSILE if index == 2 else FittingHardpoint.TURRET) == 0
    assert fit.pgUsed <= fit.ship.getModifiedItemAttr('powerOutput')
    assert fit.cpuUsed <= fit.ship.getModifiedItemAttr('cpuOutput')
    medium_rig = Module(eos.db.getItem('Medium Ancillary Current Router I'))
    small_rig = Module(eos.db.getItem('Small Ancillary Current Router I'))
    assert medium_rig.fits(fit)
    assert not small_rig.fits(fit)


@pytest.mark.parametrize('level', (0, 5))
@pytest.mark.parametrize('index,smaller,bonuses', TURRET_CASES)
def test_documented_turret_bonuses_and_smaller_weapon_exclusion(index, smaller, bonuses, level):
    fit = make_fit(index, level)
    large = add_module(fit, WEAPONS[index])
    small = add_module(fit, smaller)
    wrong = add_module(fit, '800mm Repeating Cannon II' if index != 3 else 'Mega Pulse Laser II')
    recalculate(fit)
    factors = {attr: 1 + bonus * level / 100 for attr, bonus in bonuses.items()}
    factors.update({'power': 0.05, 'cpu': 0.5, 'trackingSpeed': 1})
    if index in (0, 1):
        factors['capacitorNeed'] = 0.5 * (1 - 0.1 * level if index == 0 else 1)
    assert_raw_factors(large, factors)
    # Neither a smaller same-family turret nor a large wrong-family turret gets
    # any navy fitting, cap, damage, range, tracking or cycle-time modifiers.
    unbonused = dict.fromkeys(('power', 'cpu', 'capacitorNeed', 'damageMultiplier',
                              'maxRange', 'falloff', 'trackingSpeed', 'speed'), 1)
    assert_raw_factors(small, unbonused)
    assert_raw_factors(wrong, unbonused)
    # Recalculate at the other level on the same real fit, exercising skill
    # modifier registration and clearing rather than immutable default values.
    other = 5 - level
    fit.character.getSkill(HULLS[index]['skill']).setLevel(other, ignoreRestrict=True)
    recalculate(fit)
    for attr, bonus in bonuses.items():
        role = 0.5 if attr == 'capacitorNeed' else 1
        assert_raw_factors(large, {attr: role * (1 + bonus * other / 100)})


@pytest.mark.parametrize('level', (0, 5))
@pytest.mark.parametrize('launcher,suffix', (
    ('Cruise Missile Launcher II', 'Cruise Missile'),
    ('Torpedo Launcher II', 'Torpedo'),
))
@pytest.mark.parametrize('flavor,damage', (
    ('Scourge', 'kineticDamage'), ('Mjolnir', 'emDamage'),
    ('Inferno', 'thermalDamage'), ('Nova', 'explosiveDamage'),
))
def test_naga_cruise_and_torpedo_damage_velocity_and_fitting_only(launcher, suffix, flavor, damage, level):
    fit = make_fit(2, level)
    module = add_module(fit, launcher, charge=f'{flavor} {suffix}')
    recalculate(fit)
    assert_raw_factors(module, {'power': 0.05, 'cpu': 0.5, 'speed': 1})
    for attr in ('kineticDamage', 'emDamage', 'thermalDamage', 'explosiveDamage', 'maxVelocity'):
        bonus = 10 if attr in ('kineticDamage', 'maxVelocity') else 5
        assert module.getModifiedChargeAttr(attr) == pytest.approx(
            module.charge.getAttribute(attr, 0) * (1 + bonus * level / 100))
    assert module.getModifiedChargeAttr(damage) > 0


@pytest.mark.parametrize('level', (0, 5))
def test_naga_does_not_apply_rapid_heavy_or_inherited_hybrid_bonuses(level):
    fit = make_fit(2, level)
    rapid = add_module(fit, 'Rapid Heavy Missile Launcher II', charge='Scourge Heavy Missile')
    # Force a hybrid into the data model solely to test effect scope; normal
    # fitting rejects it because this hull correctly has zero turret hardpoints.
    hybrid = add_module(fit, 'Neutron Blaster Cannon II')
    recalculate(fit)
    assert_raw_factors(rapid, {'power': 1, 'cpu': 1, 'speed': 1})
    for attr in ('kineticDamage', 'maxVelocity'):
        assert rapid.getModifiedChargeAttr(attr) == pytest.approx(rapid.charge.getAttribute(attr))
    assert_raw_factors(hybrid, dict.fromkeys(
        ('power', 'cpu', 'capacitorNeed', 'damageMultiplier', 'maxRange', 'trackingSpeed'), 1))


@pytest.mark.parametrize('level', (0, 5))
def test_talos_reduces_plate_added_mass_not_hull_mass_or_tracking(level):
    fit = make_fit(1, level)
    base_mass = fit.ship.item.getAttribute('mass')
    plate = add_module(fit, '1600mm Steel Plates II')
    recalculate(fit)
    addition = plate.item.getAttribute('massAddition') * (1 - 0.15 * level)
    assert plate.getModifiedItemAttr('massAddition') == pytest.approx(addition)
    assert fit.ship.getModifiedItemAttr('mass') == pytest.approx(base_mass + addition)
    fit.modules.remove(plate)
    recalculate(fit)
    assert fit.ship.getModifiedItemAttr('mass') == base_mass


@pytest.mark.parametrize('level', (0, 5))
def test_tornado_reduces_only_mwd_signature_penalty(level):
    fit = make_fit(3, level)
    base_signature = fit.ship.item.getAttribute('signatureRadius')
    mwd = add_module(fit, '50MN Microwarpdrive II')
    afterburner = add_module(fit, '10MN Afterburner II')
    recalculate(fit)
    penalty = mwd.item.getAttribute('signatureRadiusBonus') * (1 - 0.15 * level)
    assert mwd.getModifiedItemAttr('signatureRadiusBonus') == pytest.approx(penalty)
    assert fit.ship.getModifiedItemAttr('signatureRadius') == base_signature
    assert_raw_factors(afterburner, {'speedFactor': 1, 'capacitorNeed': 1})
    mwd.state = FittingModuleState.ACTIVE
    recalculate(fit)
    assert fit.ship.getModifiedItemAttr('signatureRadius') == pytest.approx(base_signature * (1 + penalty / 100))
    mwd.state = FittingModuleState.ONLINE
    recalculate(fit)
    assert fit.ship.getModifiedItemAttr('signatureRadius') == base_signature


@pytest.mark.parametrize('index,damage_factor,range_attr,range_factor', (
    (0, 1.25, 'maxRange', 1), (1, 1.25, 'trackingSpeed', 1.375),
    (2, 1.25, 'maxRange', 1.5), (3, 1, 'speed', 0.75),
))
def test_original_t1_hulls_keep_original_effect_behavior(index, damage_factor, range_attr, range_factor):
    fit = make_fit(index, 5, original=True)
    weapon = add_module(fit, 'Neutron Blaster Cannon II' if index == 2 else WEAPONS[index])
    recalculate(fit)
    assert_raw_factors(weapon, {
        'damageMultiplier': damage_factor, range_attr: range_factor,
        'power': 0.05, 'cpu': 0.5})
    if index in (0, 1, 2):
        assert_raw_factors(weapon, {'capacitorNeed': 0.25 if index == 0 else 0.5})
