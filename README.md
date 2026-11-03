# pyfa

## Preferred way to run this fork

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then from the terminal run the following commands from this repository's root directory. Use Python 3.14, matching `.python-version`; the project's declared minimum is Python 3.12.

```sh
uv python install 3.14
uv venv --python 3.14
uv sync --locked
uv run pyfa.py
```

`uv venv` creates a local `.venv`, and `uv sync --locked` installs the project's dependencies from `pyproject.toml` and `uv.lock` into it. No manual environment activation is needed. On Linux, the default wxPython dependency builds from source and requires the platform's compiler, Python development headers, and GTK development packages.

[![Build Status](https://github.com/pyfa-org/Pyfa/actions/workflows/build.yml/badge.svg?branch=master)](https://github.com/pyfa-org/Pyfa/actions/workflows/build.yml)

![pyfa](https://user-images.githubusercontent.com/275209/66119992-864be080-e5e2-11e9-994a-3a4368c9fad7.png)

## What is it?

Pyfa, short for **py**thon **f**itting **a**ssistant, allows you to create, experiment with, and save ship fittings without being in game. Open source and written in Python, it is available on any platform where Python 3 and wxWidgets are available, including Windows, macOS, and Linux.

## Latest Version and Changelogs
The latest version along with release notes can always be found on the project's [releases](https://github.com/pyfa-org/Pyfa/releases) page. Pyfa will notify you if you are running an outdated version.

## Installation
Windows, macOS, and Linux users are supplied self-contained builds of pyfa on the [latest releases](https://github.com/pyfa-org/Pyfa/releases/latest) page.

### Third Party Packages
Please note that these packages are maintained by third-parties and are not evaluated by the pyfa developers.

#### macOS
Apart from the official release, there is also a [Homebrew](https://formulae.brew.sh/cask/pyfa) option for installing pyfa on macOS. Simply fire up in terminal:
```
$ brew install --cask pyfa
```

#### Linux Distro-specific Packages
The following is a list of pyfa packages available for certain distributions. 

* Arch: https://aur.archlinux.org/packages/pyfa/
* Gentoo: https://github.com/ZeroPointEnergy/gentoo-pyfa-overlay

## Local Fractured Skies preview

This local build includes four **experimental navy attack battlecruisers** and 27 **experimental Synchronizer rigs**. Sources: the developer interview in `mytmpdata\evepatch.mkv` and `mytmpdata\Fractured-Skies-All-Stats.pdf` (15 pages), compared against the video's readable stats and fitting demonstrations. These local reference files are not committed. The preview is not complete, final game data.

Start the installed local build with:

```sh
./launch-local.sh
```

### Navy attack battlecruisers

The fitting browser's **Attack Battlecruiser** category includes:

| Experimental hull | High / mid / low | Weapon hardpoints | Fallback for unverified stats |
| --- | --- | --- | --- |
| Oracle Navy Issue | 7 / 3 / 7 | 6 turrets | T1 Oracle |
| Talos Navy Issue | 7 / 4 / 6 | 6 turrets | T1 Talos |
| Naga Navy Issue | 7 / 7 / 3 | 6 launchers | T1 Naga |
| Tornado Fleet Issue | 7 / 6 / 4 | 6 turrets | T1 Tornado |

Each has one utility high slot. The documented navy skill and role bonuses
replace the T1 bonuses: large lasers on Oracle, large hybrids and reduced plate
mass on Talos, cruise missiles/torpedoes on Naga, and large projectiles plus
reduced MWD signature penalty on Tornado. Naga has no hybrid or rapid-heavy
bonuses; Talos does not retain its T1 tracking bonus.

**Layouts, hardpoints, documented bonuses and observed raw-stat changes are modeled.** Oracle, Talos and Tornado use the shown navy HP, speed, agility and targeting/sensor changes; Oracle and Naga use the shown powergrid/CPU changes, and Tornado uses the shown cargo capacity. Tornado CPU (375 tf) and powergrid (865 MW) are inferred from the one-MWD fit totals at max skills, allowing display rounding.

Unshown values retain explicitly unverified T1 fallbacks: most Naga raw stats (including base lock range), Talos base powergrid, Oracle maximum locked targets, and skill prerequisites. Other unchanged raw attributes retain their T1 values. No blanket 25% HP or approximately 12% speed increase is guessed. Every hull name and description identifies it as experimental. Rebuild the database with `uv run python db_update.py` after updating these preview definitions.

### Synchronizer rigs

Search the market browser for `Synchronizer`, or browse **Rigs → Experimental
Synchronizers**. Every rig name ends in `[Experimental]`; its description lists
the modeled effects and missing attributes. Standard rig-size restrictions and
the limit of one Synchronizer across all families apply.

The four empire families implement their documented bonuses, increasing each
beneficial magnitude by one percentage point per exact matching-faction module.
Offline fitted modules count; ammunition, cargo, drones, Synchronizers and mutated
modules do not. Matching uses the English item name regardless of UI language,
not officer/deadspace faction affiliation.

Pirate traits are modeled from the video's Traits tabs, including their faction-module scaling and fixed penalties:

- **Dark Blood:** drain amount, neut/Nosferatu overheating benefits, optimal and
  falloff, and laser damage; fixed +200% capacitor recharge time (3×).
- **Domination:** signature reduction, projectile falloff/damage and warp speed;
  fixed −30% shield, armor and structure hitpoints.
- **Dread Guristas:** drone damage/all HP layers, shield resistances and ECM
  strength/optimal; fixed −60% drone control range.
- **Shadow Serpentis:** incoming-web resistance, hybrid falloff/damage and speed;
  fixed −60% targeting range.
- **True Sansha:** afterburner velocity bonus and overheating benefits, laser
  damage/tracking; fixed +400% afterburner capacitor activation cost (5×).

Heat benefits apply only when the affected module is overheated. Resistance
bonuses reduce damage/web-effectiveness multipliers, rather than adding flat
percentage points to displayed resistance.

**The shown −10% CPU-output drawback is modeled for every Synchronizer.** Synchronizer Rigging mitigation is not modeled because the skill's exact formula is unverified. Rigs have 5 m³ volume, 40 structure HP, Tech 1 and Meta 8, as shown on the four empire and True Sansha medium rigs; these metadata values are assumed for the other families and sizes.

Synchronizers now use the existing module/rig stacking pools for turret damage/tracking/falloff, missile damage/velocity, armor-repair amount, ship velocity/signature/warp speed, targeting-range bonuses, shield resistances, and ECM strength/range. HP, capacitor capacity/recharge and activation-cost modifiers, shield-booster cycle time, and heat-benefit enhancements remain unpenalized, matching their existing equivalents. Dark Blood neut/Nosferatu amount/range bonuses, Shadow Serpentis web resistance and fixed pirate drawbacks retain their unpenalized preview behavior; these interactions have not been independently established.

**Video-confirmed stacking:** Shadow Serpentis turret damage stacks with Magnetic Field Stabilizers. The complete faction Proteus fit at All 5 with Null M and five Warrior IIs reproduces 595.5 DPS (586.1 including reloads) and 1,733 turret volley; the Warrior II identification is inferred from the video's 80.4 drone DPS, not a readable drone name. True Sansha's afterburner speed bonus shares the module's stacking pool with overheating, but remains independent of nanofiber/overdrive stacking on ship velocity. The eleven-module Phantasm demo reproduces 1,494.4 m/s without the rig, 1,742.7 m/s with it, and 2,556.01 m/s overheated. Other stacking choices follow existing mechanics and remain preview assumptions, not confirmed release behavior.

**Calibration is provisionally set to 250 for every Synchronizer family and size; this value is unverified.** Skill prerequisites remain unmodeled. Local armor-repair and shield-booster bonuses currently exclude ancillary and remote repair modules; that scope is not confirmed by the video. Shadow Serpentis retains the Traits tab's −60% targeting-range penalty: the complete faction Proteus fit, including its Ionic Field Projector, reproduces 43.75 km (109.375 km with only the Synchronizer disabled). The earlier apparent halving compared different fits, not the rig alone. Fitting feasibility and combat results are therefore not authoritative.

Rigs use private type IDs `1001000`–`1001026`; hulls use `1001100`–`1001103`.
These are not official EVE IDs. Exports containing them are local-build data,
not valid in-game fittings. The additions live in `db_update.py`, `eos/effects.py`,
`eos/synchronizers.py`, `eos/pirateSynchronizers.py` and
`eos/navyBattlecruisers.py`, so rebuilding the database retains them.

The installed `.venv` uses the locked Ubuntu wxPython binary with private JPEG,
TIFF and JBIG compatibility libraries under `.venv/pyfa-compat`; no system
packages were changed. The launcher supplies their library path. A plain
`uv run`/`uv sync` uses the project's default source-build group and may replace
this environment; installing from source requires GTK development packages.
To rebuild with the installed environment:

```sh
LD_LIBRARY_PATH="$PWD/.venv/pyfa-compat/usr/lib/x86_64-linux-gnu${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" \
  .venv/bin/python db_update.py
```

### Portable Windows executable

`pyfa-Fractured-Skies-Portable.exe` is a single-file Windows x64 build containing
the customized database, Python, wxPython, and required native libraries.
It needs no Python installation or pyfa installer. The executable is unsigned;
Windows SmartScreen may warn about an unrecognized application.

Run it from a writable folder. Fits, preferences, logs and credentials are
stored in a `saveddata` folder beside the executable. Move that folder with the
executable to retain your data. An explicit `--savepath` / `-s` option overrides
the portable location. The bundled resources extract into a temporary directory
at startup; saved fittings do not live in that temporary directory.

The desktop copy is the deliverable. Rebuilding writes a new copy under
`dist/windows-portable/`; the disposable build environment and duplicate output
can be removed afterward. All experimental hull and rig limitations above still
apply. Verification used Windows Python and the packaged executable under Wine,
not a native Windows machine.

To rebuild on Windows from this customized source tree, with the Microsoft
Visual C++ x64 redistributable installed on the build machine:

```powershell
uv sync --frozen --no-default-groups --group packaging --group wx-binary
uv run --no-sync python scripts/compile_lang.py
uv run --no-sync python db_update.py
$env:PYFA_PORTABLE = '1'
uv run --no-sync python -m PyInstaller --clean --noconfirm --distpath dist/windows-portable pyfa.spec
```

Without `PYFA_PORTABLE=1`, the spec retains its normal directory-based packaging.

## Contribution
If you wish to help with development or you need to run pyfa through a Python interpreter, check out [the instructions](https://github.com/pyfa-org/Pyfa/blob/master/CONTRIBUTING.md).

## Bug Reporting
The preferred method of reporting bugs is through the project's [GitHub Issues interface](https://github.com/pyfa-org/Pyfa/issues). Alternatively, posting a report in the [pyfa thread](https://forums.eveonline.com/t/27156) on the official EVE Online forums is acceptable. Guidelines for bug reporting can be found on [this wiki page](https://github.com/pyfa-org/Pyfa/wiki/Bug-Reporting). 

## License
Pyfa is licensed under the GNU GPL v3.0, see LICENSE

## Resources
* [Development repository](https://github.com/pyfa-org/Pyfa)
* [EVE forum thread](https://forums.eveonline.com/t/27156)
* [EVE University guide using pyfa](https://wiki.eveuniversity.org/PYFA)
* [EVE Online website](http://www.eveonline.com/)

## Contacts:
* Kadesh / DarkPhoenix
    * GitHub: @DarkFenX
    * EVE: Kadesh Priestess
    * Email: phoenix@mail.ru
* Sable Blitzmann
    * GitHub: @blitzmann
    * [TweetFleet Slack](https://www.fuzzwork.co.uk/tweetfleet-slack-invites/): @blitzmann
    * [Gitter chat](https://gitter.im/pyfa-org/Pyfa): @blitzmann
    * Email: sable.blitzmann@gmail.com

## CCP Copyright Notice
EVE Online, the EVE logo, EVE and all associated logos and designs are the intellectual property of CCP hf. All artwork, screenshots, characters, vehicles, storylines, world facts or other recognizable features of the intellectual property relating to these trademarks are likewise the intellectual property of CCP hf. EVE Online and the EVE logo are the registered trademarks of CCP hf. All rights are reserved worldwide. All other trademarks are the property of their respective owners. CCP hf. has granted permission to pyfa to use EVE Online and all associated logos and designs for promotional and information purposes on its website but does not endorse, and is not in any way affiliated with, pyfa. CCP is in no way responsible for the content on or functioning of this program, nor can it be liable for any damage arising from the use of this program.
