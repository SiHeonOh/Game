# Black Curtain: project guidelines

Black Curtain is a single-player war game in Unreal Engine 5.8: a HOI4-style strategy map plus first-person battles with infantry, walkers, planes, ships and airships. Read `Game Design Doc.md` for what the game is and the roadmap. `Game Architecture Design Doc.md` is the older prototype doc, kept for its technical architecture. The lore is in `Lore Files/`.

This file sets how sessions start and end, and where files go and how they're named. Follow it for every new file. When something doesn't fit, extend these rules here instead of improvising.

## Session handoffs

Work spans many sessions, so each session leaves a handoff for the next one.

- **At the start of every session,** read the newest file in `Handoffs/` (file names start with the date, so it sorts last) before doing anything else. Check its claims against the repo (git status, the files it names) rather than trusting it blindly, and tell the user in a line or two where things stand.
- **When the user asks to end the session** (for example "end session", "wrap up for today", "write a handoff"), write a new handoff, then offer to commit it.

Handoffs live in `Handoffs/YYYY-MM-DD-<topic>.md` (a second one on the same day gets `-2`, `-3`). They're committed like any other doc. Each one covers:

```
# Handoff: <date>, <topic>

## Done this session
What changed, with commit hashes; decisions made, with their numbers in the design doc.

## Current state
Branch, whether everything is committed and pushed, anything uncommitted and why.
State of the Unreal editor and project if it matters (open maps, Play-in-Editor, assets mid-import).

## Next steps
The next concrete task first, then what follows it on the roadmap.

## Open questions
Decisions still waiting on the user.

## Watch out for
Gotchas found this session, unfinished experiments, things that look done but aren't verified.
```

Keep handoffs short and factual. Point to the design doc and commits instead of repeating them.

## Top level

```
Blender Files/            Blender sources: generator scripts and hand-made .blend files
Game Files/Black_Curtain/ the Unreal project
Handoffs/                 session handoffs, one file per session (see Session handoffs)
Lore Files/               the setting: one Markdown file per faction, maker, event or place (see Lore)
Game Design Doc.md        the design doc
CLAUDE.md                 this file
```

## Lore

The lore is the user's writing; it lives in `Lore Files/`, one file per thing, and `Lore Files/README.md` holds its folder, naming and format rules. Follow that README for every lore file.

- **Before designing anything that touches the setting** (factions, equipment, events, focus trees, maps), read `Lore Files/README.md` once, then search the `summary:` lines of the relevant folder and open only the files you need. `Timeline.md` is the chronology; `OPEN.md` lists what's undecided.
- **Respect `status`:** build on `canon`; treat `draft` and `idea` as unsettled and say so; ignore `cut` unless asked.
- **Don't change the user's lore wording** without asking. Adding headers, links, "In the game" sections, or splitting a file without rewording is fine.
- **Lore IDs and game-data IDs are the same IDs** (`fac_`, `mfr_`, equipment IDs), so lore maps straight onto data rows.
- **Keep the top-level files current:** add a line to `Timeline.md` for every new dated event, and remove `OPEN.md` entries once they're settled.

## The rule behind the layout: equipment belongs to manufacturers, not factions

Factions share a bloc's equipment, field obsolete gear, and capture or buy each other's weapons. So every weapon, walker, plane, ship and airship lives in exactly one place: under the **manufacturer** that makes it, inside the **line** that manufacturer belongs to.

- A **line** is a bloc or a nation with its own designs.
- A **manufacturer** is a maker within a line, such as an arms company or a state design bureau. A bloc's shared equipment comes from its manufacturers, and each manufacturer has its own design language. One manufacturer can supply many nations, the way several European countries fly the Rafale.
- Which factions can build or use an item is **data** (see Game data), never a folder.
- Folders under `Factions/` hold only what is truly a faction's own: flags, insignia, color material instances and faction-specific UI.
- Faction looks are **applied, not modeled.** One model takes each faction's colors and insignia through material parameters and decals, so captured equipment repaints itself without new art.

Line and manufacturer names are placeholders (`WestBloc`, `EastBloc`, `Italy`; `Vulcan`, `Hammer`) until the lore settles them. Rename by moving folders in the Unreal editor (see Moving and renaming).

## Unreal project (`Game Files/Black_Curtain/`)

### Content

All of our own assets go under `Content/BlackCurtain/`. Everything else in `Content/` comes from templates or store packs.

```
Content/
  BlackCurtain/
    Core/                      shared master materials, the color palette, decal masters
    Equipment/
      Weapons/<Line>/<Manufacturer>/<Item>/   meshes, materials and sounds unique to that item
      Walkers/<Line>/<Manufacturer>/<Item>/   skeletal mesh, skeleton, animations, materials
      Aircraft/<Line>/<Manufacturer>/<Item>/
      Ships/<Line>/<Manufacturer>/<Item>/
      Airships/<Line>/<Manufacturer>/<Item>/
      Manufacturers/<Manufacturer>/          logos, maker's plates, materials shared by that maker's items
    Characters/
      Soldiers/                the shared soldier rig, body and animations
      Uniforms/<Line>/         uniform and gear meshes per bloc or nation
    Factions/<FactionID>/      flag, insignia decals, faction color material instances
    Environment/               props, buildings and kits used by maps and the map generator
    Maps/
      Test/                    gray-box and experiment maps (L_GrayBox lives here)
      Key/                     hand-made maps for key places
    Gameplay/                  Blueprints: game modes, controllers, pickups and other gameplay classes
    AI/                        behavior assets: StateTrees, Behavior Trees, EQS queries
    UI/                        widgets, fonts, icons
    Audio/                     shared sounds and music (item-specific sounds stay with the item)
    VFX/                       shared Niagara systems and effects
  Data/                        game data as text files (see Game data)
  FirstPerson/, Variant_Shooter/, Characters/, Weapons/, LevelPrototyping/, Input/
                               template content: placeholders only
```

- **Template and store content stays in its own folders.** Never put our assets inside them. Template assets may be edited as temporary stand-ins (the rifle bullet speed was), but anything meant to last gets made or copied under `BlackCurtain/`.
- An item's folder holds everything unique to it. Anything shared by several items moves up to `Core/`, `Audio/` or `VFX/`.

### C++ code (`Source/Black_Curtain/`)

One game module to start, with a folder per system:

```
Source/Black_Curtain/
  Core/        data types, IDs, data loading, saving
  Campaign/    strategy map simulation, auto-resolver, factions, economy, research
  Battle/      game mode, BattleSetup and BattleResult, objectives, reinforcements
  Combat/      projectile manager, damage, wounds, suppression
  Soldiers/    the soldier class and soldier state
  Vehicles/    shared vehicle base, seats, walkers, aircraft, vessels
  AI/          bot controllers, commanders, StateTree tasks, Mass processors
  UI/          C++ widget bases
```

Split it into separate modules only if compile times start to hurt.

## Game data

Game data lives in **text files** (JSON or CSV) under `Content/Data/`. The game loads them at startup, so mods can add or override rows. Unreal's content browser ignores them. Packaging has to copy them as plain files: when packaging is first set up, add `Data` to "Additional Non-Asset Directories to Copy" in the project's packaging settings.

```
Content/Data/
  Factions/factions.json       id, name, colors, starting regions, which manufacturers' equipment it uses
  Equipment/lines.csv          id, name, bloc or nation
  Equipment/manufacturers.csv  id, name, line, design notes
  Equipment/weapons.csv        id, manufacturer, class, damage, muzzle velocity, magazine, ...
  Equipment/walkers.csv        id, manufacturer, class (light ... superheavy), asset path, ...
  Equipment/aircraft.csv, ships.csv, airships.csv
  Research/                    lines, branches, technology locks, doctrines
  Regions/                     region data for the strategy map
  Events/                      events, with conditions and effects as data
  FocusTrees/                  one file per major faction, plus the generic tree
  Battles/                     hand-written BattleSetups for testing
```

- Every row has a **stable text ID**. Code, research, saves and mods refer to IDs, never to row numbers or asset paths.
- Equipment rows name their manufacturer and their asset path; the manufacturer row names its line. Data and assets meet in one place.
- Don't use Unreal DataTable assets as the source of truth for game data: they're binary, hard to diff, and not moddable. Generate them from the text files if a system needs them.

## Blender files (`Blender Files/`)

Mirrors the equipment layout. Scripts are the source of truth.

```
Blender Files/
  _lib/                                 shared generator code: palette, rivets, rigging helpers, export to centimeters
  _lib/manufacturers/<manufacturer>.py  each maker's design language: shapes, proportions, details, colors
  Equipment/Walkers/<Line>/<Manufacturer>/<Item>/build_<item>.py
  Equipment/Weapons/<Line>/<Manufacturer>/<Item>/build_<item>.py
  Environment/<Kit>/build_<kit>.py
```

- **Generator output is not committed.** The `.fbx`, `.blend` and render files a script produces can be rebuilt in seconds; committing them only uses Git LFS space. Commit the script.
- **Hand-made `.blend` files are committed** (through Git LFS), next to any script that processes them.
- Anything two generators share (colors, bevel sizes, rivets, the export settings) goes in `_lib/`, so every asset keeps the same look.
- A manufacturer's design language lives in its `_lib/manufacturers/` module, so everything one maker builds looks related, and makers look different from each other.
- `Blender Files/Walkers/LightAP/build_walker_light_ap.py` predates these rules. Its shared parts move to `_lib/` and the script moves under `Equipment/Walkers/` when the first real walker is made.

## Naming

### IDs (data files)

Lowercase, underscores, starting with a type prefix. Equipment IDs are `<type>_<manufacturer>_<class>_<name>`; the line isn't repeated, because the manufacturer already belongs to one.

| Type | Prefix | Example |
| --- | --- | --- |
| Faction | `fac_` | `fac_italy` |
| Line | `line_` | `line_westbloc` |
| Manufacturer | `mfr_` | `mfr_vulcan` |
| Weapon | `wpn_` | `wpn_vulcan_rifle_m1` |
| Walker | `wlk_` | `wlk_vulcan_light_01` |
| Aircraft | `air_` | `air_hammer_fighter_01` |
| Ship | `shp_` | `shp_hammer_destroyer_01` |
| Airship | `ash_` | `ash_vulcan_battleship_01` |
| Region | `reg_` | `reg_rhine_north` |
| Technology | `tec_` | `tec_walker_heavy_2` |
| Event | `evt_` | `evt_italy_records_found` |

An ID never changes once something references it: saves and mods depend on it.

### Unreal assets

Standard Unreal prefixes, then the item, with the manufacturer in the name so assets are findable in search: `SK_Walker_Vulcan_Light_01`.

| Asset | Prefix |
| --- | --- |
| Static mesh | `SM_` |
| Skeletal mesh | `SK_` |
| Skeleton | `SKEL_` |
| Animation sequence | `A_` |
| Animation Blueprint | `ABP_` |
| Blueprint | `BP_` |
| Material | `M_` |
| Material instance | `MI_` |
| Texture | `T_` |
| Sound | `S_` |
| Niagara system | `NS_` |
| Widget | `WBP_` |
| Map | `L_` |
| Data asset | `DA_` |
| StateTree | `ST_` |

### C++

Unreal's usual prefixes (`A` for actors, `U` for objects and components, `F` for structs, `E` for enums), named after the system: `ASoldierCharacter`, `UProjectileSubsystem`, `FBattleSetup`.

## Moving and renaming

- **Move or rename Unreal assets only inside the editor,** never in Explorer or with Git. The editor updates references and leaves redirector files behind; run "Fix Up Redirectors" on the folder afterwards.
- **Never have two editors open on the same project.** They lock each other's files and can overwrite each other's work.
- **Don't import, save or move assets while Play-in-Editor is running.**
