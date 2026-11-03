# Game Architecture Design Doc

Nov 3, 2026 · @Glaukopis

A single-player, low-poly war game in two halves: a HOI4-style strategy map of a shattered post-nuclear world, and first-person battles you can drop into, fought on land, in the air, at sea and with airships. Working title TBD.

## Overview

A single-player war game with two layers:

- **Strategy map (HOI4-style):** run one faction in a shattered, post-nuclear world on the real-world map: territory, armies, production and war.
- **Battles (Ravenfield-style, first person):** drop into any battle your faction fights, as a colonel, a squad leader or a grunt, alongside bots, with infantry, ground vehicles, planes, ships and airships.

The macro game decides most of a battle's outcome. Inside a battle you matter through your orders (as an officer) and otherwise only as much as one soldier.

**Pillars**

1. **Macro decides, micro matters.** The strategy map sets up the battlefield; battles reward good orders, not super-soldiers.
2. **First person at every rank.** Even commanding happens through a map table, binoculars and a radio.
3. **One combined-arms sandbox.** Infantry, ground vehicles, planes, ships and airships share one world and one set of systems.
4. **Built to finish.** Every build step ends in something playable.

**Constraints and non-goals**

- Single-player only, with bots on both sides. No online multiplayer.
- Arcade physics: flying and driving should be fun, and damage is health-based. No armor-penetration simulation.
- HOI4-lite: regions, armies, factories and manpower first. Diplomacy, research trees and detailed supply come later, if ever.
- No guided missiles in battles; every weapon fires an unguided projectile.
- One consistent low-poly art style, mostly from store assets.
- Unreal Engine 5, with C++ for core systems and Blueprints for wiring up content and tuning.
- Hobby pace (about 5–10 hours a week): a rough but complete version in 2–4 years, polished within 10.

## Setting

Only the parts the systems depend on. Detailed lore can be written any time and slotted in later.

- **Alternate history:** the US ends WWII by nuking Germany and Japan. The Allies then turn on each other. By the 1950s more nations have nukes, and those without them use bioweapons. Civilization collapses.
- **When:** some time after the collapse ("the future"), but technology is stuck around late-1940s to 1950s level: bolt-action and early automatic rifles, post-war tanks, propeller planes and early jets, gun-armed warships, plus armored airships.
- **Political map:** almost every country is divided, gone or in civil war, so there are many factions and they are deliberately unequal. Balancing factions against each other is not a goal.
- **Geography:** the real-world map, edited wherever the apocalypse justifies it (flooded coasts, dead zones, new borders).
- **WMDs:** only a few strong survivors may still have nukes or ICBMs; bioweapons are more widespread. Both are rare actions on the strategy map, not weapons inside battles.
- **Airships:** armored flying warships, not blimps.
- **Superweapon:** the flying aircraft carrier, on the same tier as nukes, buildable only by the strongest factions.

## At a glance

&#91;embedded content: game architecture · 2 halves, 1 interface\]

The campaign hands each battle a BattleSetup and gets a BattleResult back. Nothing else crosses between the two halves, so each one can be built and tested on its own.

## Strategy layer

**Time.** Real time with pause, like HOI4. The campaign advances in hourly ticks at an adjustable speed. It pauses automatically when the player is offered a battle and while a battle is being played.

**Map and regions**

- Regions come from free public-domain map data (Natural Earth's states and provinces), merged or split into a few hundred regions. Build one continent first.
- Each region has an owner, a terrain type (plains, forest, hills, mountains, urban, coast), neighbors, manpower, factories, a fortification level, and status effects (irradiated, plague, ruined).
- Sea zones connect coasts for fleets. Planes and airships operate over both regions and sea zones.
- The map is drawn from a region ID image: every region is a unique color. The same image is used to work out which region was clicked and to color regions by owner.

**Factions.** Each faction is a data row: name, color, flag, capital, starting regions and units, industry, manpower, AI personality, and capability flags (has nukes, can build superweapons). Diplomacy starts as just "at war" or "at peace".

**Units on the map**

- Types: army (made of regiments), fleet, air wing, airship group and superweapon.
- Each unit tracks owner, location, manpower, equipment by type (rifles, trucks, tanks, planes, ships and so on), organization (readiness and morale), supply and experience.
- Units are built from templates, a simplified version of HOI4's division designer.

**Economy.** Factories produce equipment into a national stockpile over time. Manpower is recruited from regions. Units draw men and equipment from these to reinforce. More resources (fuel, steel) are a later expansion.

**Combat on the map.** When a unit attacks into an enemy-held region, a map battle starts. It is split into sectors and resolved tick by tick from strength, equipment, terrain, fortification, organization and support. When the player's faction is involved, the player can choose to fight one sector in first person (see The bridge).

**WMDs and superweapons**

- **Nuke:** available to a few factions only, expensive, with a long cooldown. It destroys manpower and factories in the target region and leaves it Irradiated for a long time: attrition, lower production, and a ruined or irradiated battle map variant.
- **Bioweapon:** puts Plague on a region, draining manpower over time, with a chance to spread to neighbors.
- **Flying carrier:** a unit with a huge cost and build time. It projects air power over nearby regions and appears in battles as a centerpiece and mobile spawn point.

**Strategic AI.** One AI runs every faction except the player's, steered by faction data (aggression, priorities). It has three jobs: deciding what to build, where to send armies (attack weak neighbors, defend threatened regions), and when to use strategic weapons (rarely, past clear thresholds). It scores its options instead of following a script written for each faction.

## Battle layer

**Flow**

1. Load a battle level and read the BattleSetup.
2. Pick the map variant, objectives and entry edges.
3. Deploy each side's forces, HQs and support.
4. The player picks a rank slot: colonel, squad leader or grunt.
5. Fight until an end condition is met.
6. Write the BattleResult and return to the strategy map.

**Maps**

- A library of hand-made maps per terrain type (plains, forest, hills, urban, coast), each with variants: ruined, irradiated, and entrenched (trenches and bunkers for a dug-in defender).
- Each map defines objectives (capture points), entry zones on each edge so the attack direction matches the strategy map, HQ positions, and where relevant airfields, shorelines and airship approaches.
- Size: about 2–4 km across, enough room for combined arms.

**Objectives and end conditions**

- A battle is a sector fight: the attacker must take a set number of objectives before running out of reinforcements, and the defender must hold.
- Reinforcements come from the manpower of the units in the BattleSetup. Every soldier who dies draws from that pool. Vehicles are limited to the equipment those units actually have.
- The battle ends when one side runs out of reinforcements, the objectives fall, or a time limit runs out. After a time limit, the auto-resolver on the strategy map carries on the fight.

**Scale.** Start with 60–150 bots and a handful of vehicles per side, and raise the counts after performance testing. A battle represents one sector of a larger map battle, roughly the colonel's regiment's share of the front.

## Chain of command

Every rank in a battle is a slot that either a bot or the player fills. The ranks above the player are bots giving orders, and the ranks below are bots carrying them out.

| Rank | Where it's played | Controls | Gives orders with |
| --- | --- | --- | --- |
| General | Strategy map | Armies, fronts, production | The strategy map |
| Colonel | Battle, first person | Several companies (each a few bot squads), plus artillery, tanks and air support | HQ map table, field map, binoculars, radio |
| Squad leader | Battle, first person | About 8 soldiers | Command wheel: look at a spot and pick an order |
| Grunt | Battle, first person | Themselves | Follows the squad leader's orders |

**Orders are data.** An order is a small struct: type (move, attack, defend, hold, fall back, follow, fire mission, air strike), target (a location, objective or enemy unit), recipient, issuer and time issued. Bot officers and the player's UI create the same order objects, so a unit can't tell whether a bot or the player gave it an order. Orders can arrive after a radio delay.

**Information comes by radio.** Units report their position, status and contacts at intervals and when something happens (enemy spotted, heavy losses, objective taken). The colonel's map shows where units last reported from, not where they are now, plus a log of reports. That gives fog of war for free.

**Command tools**

- **HQ map table:** a physical map in the command post with markers for units. Full overview and precise orders, but far from the fighting.
- **Field kit:** a handheld map, binoculars and a radio operator who follows the player. Look through the binoculars at a spot to order an attack or call artillery on it. Less overview, more personal risk.
- **Squad command wheel:** follow me, move here, attack there, hold, take cover, suppress, regroup.

**Officer death.** When the player's colonel dies, a bot second-in-command takes over after a short gap with no new orders; units keep following their last orders. The player then respawns at HQ as the replacement officer after a delay. The exact rules are an open question.

**Picking a rank.** The player picks a slot at the start of a battle and can switch to any free slot when respawning.

## Bot AI

The AI mirrors the chain of command. Each level only talks to the level directly above and below it.

- **Battle commander (colonel):** assigns companies to objectives by scoring them (objective value, distance, known enemy strength) and spends support such as artillery and air sorties.
- **Company and platoon leaders:** turn an objective into squad tasks, such as approach routes and one squad giving covering fire while another moves.
- **Squad leader:** moves the squad in formation, picks cover positions, assigns targets, and decides when to suppress or assault.
- **Soldier:** sees and hears enemies, picks targets, shoots with an accuracy model (distance, movement, suppression), uses cover, and has morale states (suppressed, pinned, falling back).
- **Vehicle crews:** drivers follow paths with steering, gunners pick and lead targets, pilots fly waypoints and attack runs (simple dogfighting later), and captains of ships and airships keep their range and their turrets on target.

**Unreal tools:** Behavior Trees (or StateTree) for decisions, the Environment Query System (EQS) for finding cover and firing positions, NavMesh for pathfinding (separate settings for infantry and vehicles), and AI Perception for sight and hearing.

**Performance**

- Bots far from the player think less often (AI level of detail).
- Expensive decisions are spread over several frames, and line-of-sight checks get a fixed budget per frame.
- If battles ever need many hundreds of bots, Unreal's Mass system (built for large crowds) is the upgrade path.

## Combat and vehicles

**Projectiles.** One system handles every weapon: rifles, machine guns, tank shells, artillery, bombs, rockets and airship cannons. A projectile is a position, a velocity, gravity and drag, plus a damage profile. A single manager moves every projectile each frame and checks each step for hits with a ray-cast, instead of spawning a separate actor per bullet, so hundreds of shots in flight stay cheap.

**Damage**

- Soldiers have health; hit locations can come later.
- Vehicles have hull health plus a few parts that can be knocked out: a destroyed engine means it can't move, a destroyed turret means it can't fire.
- Armor tiers act as damage multipliers by weapon class, so rifles can't hurt a tank but a tank shell can.
- Near misses raise a soldier's suppression, which lowers their accuracy and pushes them into cover.

**Weapons as data.** Each weapon is a data row: damage, muzzle velocity, rate of fire, magazine size, spread, projectile type, effective range, and its sounds and effects.

**Seats.** Every vehicle is a set of seats (driver or pilot, gunners, passengers). Any seat can be taken by the player or a bot, with entering, leaving and switching seats. A seat can carry a weapon mount with limits on how far it turns and elevates.

**Ground vehicles.** Unreal's Chaos Vehicles handles wheeled vehicles. Tanks use wheeled physics hidden under track visuals, a common trick. Turrets rotate at a set speed.

**Planes.** A custom arcade flight model: thrust, turn rates that depend on speed, and a forgiving stall. Guns, unguided rockets and bombs. Planes take off from airfields on the battle map or arrive from off-map.

**Big vessels: ships, airships and the flying carrier.** One Vessel class covers all three: a hull split into damage sections, several turret seats, propulsion and steering. It has two movement modes:

- **Water:** buoyancy and flat movement, using Unreal's Water plugin or a simple custom buoyancy.
- **Air:** altitude control, hovering and slow turns.

The flying carrier is a large air vessel with launch points for planes and a spawn point for troops.

## The bridge: BattleSetup and BattleResult

The two halves only talk through these two structs, so each half can be built and tested on its own. A test BattleSetup can be written by hand long before the strategy map exists.

**BattleSetup (strategy map → battle)**

- Battle and sector ids, region id, terrain type, map variant (ruined, irradiated, entrenched), time of day and weather.
- Attacker and defender faction ids, and which map edge each side enters from.
- Order of battle for each side: a list of units, each with type, manpower, equipment counts by type, organization, experience and supply.
- Support for each side: artillery fire missions, air sorties by plane type, airships present, flying carrier present.
- Reinforcement pools (worked out from manpower) and the victory conditions.
- Which rank slots the player may take.

**BattleResult (battle → strategy map)**

- Winner (or draw) and the objectives each side holds at the end.
- Per unit: manpower lost, equipment lost by type, change in organization, experience gained.
- How long the battle lasted.

**How one sector feeds the map battle.** The map battle keeps resolving every sector automatically. The sector the player fought replaces its automatic result with the real one, and its winner gets a temporary bonus in the overall battle. Playing a battle should matter, but it shouldn't be an exploit.

An example BattleSetup, written as data:

```
BattleSetup {
  region: "Rhine_North", terrain: Forest, variant: Entrenched,
  attacker: {
    faction: "WestRepublic", entersFrom: West,
    units: [
      { type: InfantryRegiment, manpower: 2400, equipment: { Rifle: 2100, MachineGun: 90 } },
      { type: ArmorBattalion,   manpower: 400,  equipment: { MediumTank: 22 } }
    ],
    support: { fireMissions: 6, sorties: { Fighter: 4, Bomber: 2 }, airships: 1 }
  },
  defender: { ... },
  playerSlots: [ Colonel, SquadLeader, Grunt ]
}
```

## Data, saving and Unreal project structure

**Content is data.** Factions, regions, terrain types, unit templates, weapons, vehicles and the battle map library live in Unreal DataTables (which import from CSV or JSON) or Data Assets. Adding a faction or a weapon means adding a row, not writing code.

**Campaign state** is plain C++ structs owned by one object that survives level loads (a Game Instance Subsystem). It's saved with Unreal's SaveGame system whenever the player saves on the strategy map. Battle state is temporary; only the BattleResult is kept. Save files carry a version number from day one, so old saves can be upgraded as the game changes.

**C++ vs. Blueprints**

- **C++:** data types, the campaign simulation and auto-resolver, the projectile manager, damage, seats and vehicle logic, AI tasks, the order system, saving and loading.
- **Blueprints:** assigning meshes, sounds and effects, tuning numbers, UI layout (UMG) and level scripting.

**Key classes**

| Class | Job |
| --- | --- |
| `UCampaignSubsystem` (Game Instance Subsystem) | Owns campaign state across level loads; hands out the BattleSetup and takes back the BattleResult |
| `AStrategyGameMode` | Runs the strategy map level: ticks, map rendering, strategy UI |
| `ABattleGameMode` | Reads the BattleSetup, spawns forces, runs objectives and reinforcements, writes the BattleResult |
| `ASoldierCharacter` | One soldier class shared by the player and bots |
| `ABotController` and a custom player controller | Bot brains and player input, driving the same soldiers and vehicles |
| `UProjectileSubsystem` (World Subsystem) | Moves every projectile and resolves hits |
| `UCommandSubsystem` (World Subsystem) | Carries orders down and reports up the chain of command |
| `AVehicleBase` + `USeatComponent` | Shared vehicle base with seats; subclasses for ground vehicles, aircraft and vessels |

**Code layout.** One C++ game module to start, with a folder per system: Core, Campaign, Battle, Combat, Vehicles, AI, UI. Split it into separate modules only if compile times start to hurt.

**Tools.** Visual Studio with the "Game development with C++" workload (or JetBrains Rider). Version control from day one: Git with Git LFS for the big binary asset files, or a game-focused option like Perforce, plus an off-site backup.

## Art and assets

- **One style.** Low-poly, from one or two creators whose packs match, for example Synty's POLYGON military, war and post-apocalyptic packs. Free CC0 packs (Kenney, Quaternius) only where they fit that style.
- **Characters and animation:** Unreal's built-in mannequins and animation samples, plus Mixamo for extra animations.
- **Gray boxes first.** Battles are built with the mannequin, the template gun and blockout shapes until they're fun. Buy assets once you know what you need.
- **Custom pieces** (airships, the flying carrier): kitbash them from pack parts, use Unreal's built-in Modeling Mode, learn basic Blender, or hire a freelancer.
- **Faction identity** comes from color, insignia and flags on shared models. Scavenged, mixed equipment fits the setting.
- **Mood** comes from lighting, fog and color grading, not texture detail.
- **Style checkpoint:** after step 1, build one small test scene in low-poly and one in realistic (a soldier, a tank, a patch of ground) and commit to one.
- **Licenses:** keep a sheet listing every asset's source and license. CC0 is free to use, CC-BY needs a credit, and store licenses forbid reselling the assets. Never use models ripped from other games or mods.

## Roadmap

Every step ends in something playable. Times assume about 5–10 hours a week.

The order follows a common rule in game development: build the riskiest parts first, so problems show up early, while they are still cheap to fix. Here that means three things, in this order:

1. **The infantry battle**, because bot AI and performance are the hardest engineering in the project, and it's where Unreal gets learned.
2. **Both halves working together**, as a tiny campaign that launches real battles, because the combination is what makes the game different.
3. **The colonel**, because commanding in first person is a pillar and needs only infantry and orders.

Everything after that (vehicles, the full strategy map, WMDs) adds content to a loop that is already known to work.

| Step | Done when | Includes | Rough time |
| --- | --- | --- | --- |
| 0. Setup | An empty C++ project builds, opens and is safely in version control | Install UE5 and Visual Studio or Rider, set up Git with LFS and an off-site backup, create a C++ project from the First Person template with a neutral name (renaming later is painful), do one Blueprint beginner tutorial | 2–4 weeks |
| 1. Infantry battle | A 15-minute battle against bots over capture points is fun to replay | Soldier, rifle, projectile manager, health and teams, capture points and reinforcements, basic orders as data, a simple chain of command (bot commander → squads), one gray-box map, a hand-written BattleSetup, a bot-count performance test, a packaged build | 3–6 months |
| 2. Squad leader | You can lead a squad of bots through that battle | Command wheel, more order types, better squad AI (formations, cover, suppression) | 1–2 months |
| 3. Campaign slice | You can conquer a tiny map, fight its battles in first person, and see the results change the map | A hand-painted region ID image with 5–10 regions, two factions, armies that move, real-time ticks with pause, the auto-resolver, a simple AI (attack the weakest neighbor), BattleSetup from campaign data, BattleResult applied, level loading, a versioned save | 1–3 months |
| 4. Colonel | You can win a battle through orders alone, from the HQ map table or the field kit | HQ map table, field kit, radio reports and fog of war, artillery fire missions, off-map air strikes, officer death | 2–4 months |
| 5. Ground vehicles | Bot crews drive and fight alongside infantry, and the colonel can order them | Seats, Chaos Vehicles, armor tiers, knocked-out parts, bot drivers and gunners. Decide walkers vs. tanks first (see Open questions) | 3–6 months |
| 6. Planes | Planes fly air support and dogfight over the battle | Arcade flight model, guns, rockets and bombs, bot pilots, airfields or off-map arrival. Real planes replace step 4's off-map air strikes | 3–6 months |
| 7. Airships and ships | Airships fight over the land maps, and ships fight on a coastal map | The Vessel class in air mode first (it needs no water or new maps), then water mode, turret seats, crews, one coastal map | 3–6 months |
| 8. Full strategy map | A full campaign on one continent, with any battle playable in first person | Grow the slice: a few hundred regions from Natural Earth, faction data, unit templates, the economy, fleets, air wings and sea zones, the strategic AI, sectors, full saving | 6–12 months |
| 9+. Expand | The full game | WMDs, the flying carrier, more maps, factions and continents, polish | Ongoing |

Steps 0–8 add up to roughly 2–4 years. Step 1 matters most: nothing else gets added until it is fun to replay. The style checkpoint (see Art and assets) comes right after it. The strategy map is mostly C++ logic and 2D, so parts of it, like the region map or the auto-resolver, can be worked on any time as a break from 3D work.

### Step 1 in small pieces

Step 1 is long, so it is split into pieces that each take a week or two and each end playable:

1. Walk around a gray-box map with the First Person template's rifle.
2. Swap the template's bullets for the projectile manager (the first real C++).
3. One bot that sees the player and shoots back (AI Perception, plus a Behavior Tree or StateTree).
4. Health, death, respawning and two teams.
5. Capture points and reinforcement pools.
6. Bot squads that follow a squad leader, and a bot commander that sends them to capture points with orders.
7. A hand-written BattleSetup decides who spawns and with what.
8. A performance test: raise the bot count until the frame rate drops, then set the target.
9. A packaged build that runs outside the editor, ideally played by a friend.

### How to work through a step

- **Gray box first.** Make it work and make it fun with placeholder shapes; art comes last.
- **Playtest every week.** Play the current build, write down the three biggest problems, and fix those first.
- **Keep an "ideas for later" list.** New ideas go on the list, not into the current step. This is the main defense against scope creep.
- **Cut, don't extend.** If a step runs long, cut features from it until its "done when" is true, and move the rest to the list.
- **Close each step properly:** a packaged build, a tagged commit, and this doc updated with anything that changed.

## Risks and open questions

**Risks**

| Risk | Mitigation |
| --- | --- |
| AI is the biggest chunk of work: soldiers, crews, pilots, officers and the strategic AI | Few order types, simple behaviors first, playtest every week |
| Scope creep: factions, continents, vehicle types | One continent first, a few vehicle types per domain, everything data-driven, an "ideas for later" list |
| Losing motivation over years | Every step ends playable; share builds with friends |
| Performance with many bots and vehicles | Projectile manager, AI level of detail, low-poly art, a bot-count target set in step 1 |
| Playing a battle becomes pointless, or an exploit | Sector results have a capped effect; the macro game decides most of the outcome; tested early in the campaign slice (step 3) |
| Learning Unreal's C++ (classes, inheritance, Unreal's macros) | Learn the editor with Blueprints first; write core systems in C++ with help |
| Saves breaking as the game changes | A versioned save format from day one |

**Open questions**

- [ ] Working title
- [ ] Start year, and which continent to build first
- [ ] The faction list for that continent
- [ ] What happens when the player dies as colonel
- [ ] Bot count per battle (set after performance tests in step 1)
- [ ] Final art style (after the step 1 test scenes)
- [ ] Airship types (gunship, transport, carrier) and how they stay up in the lore
- [ ] How planes reach battles: airfields on the battle map, or arriving from off-map
- [ ] Walkers or tanks as the main armored vehicle: the lore has walkers replacing tanks, which needs a different movement system than Chaos Vehicles (decide before step 5)
