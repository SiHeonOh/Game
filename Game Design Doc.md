# Black Curtain: Game Design Doc

Working title. Started Nov 6, 2026 · @Glaukopis

This doc is being rebuilt one decision at a time. It replaces the prototype (`Game Architecture Design Doc.md`) once it's complete; the prototype's technical architecture (classes, the BattleSetup and BattleResult bridge, saving) will move into a separate tech doc. The lore lives in `Lore Files/` (start with its README and `Timeline.md`). Sections marked **Open** aren't decided yet.

## 1. Pitch

It's 1955, ten years after an alternate Second World War ended in nuclear, chemical and biological collapse. Run any faction of a fractured world on a HOI4-style strategy map, or enlist as a soldier and rise through the ranks, and fight its wars in first person: squads, dieselpunk walkers, planes, warships and Hesperium airships, in battles of hundreds to thousands, on maps built from the real places being fought over.

## 2. Core experience

**The two core roles are the squad leader and the general.** The squad leader is the heart of the battles: you fight in first person and lead a squad of bots. The general is the heart of the campaign: you run a faction on the strategy map. Together they are the game.

**All four ranks are meant to be full experiences**, not side modes: general, colonel, squad leader and grunt should each be deep enough to play a whole campaign as.

### Two game modes

- **General mode:** you run a faction on the strategy map, and you can drop into any battle your faction fights, as much or as little as you like. Battles you skip are auto-resolved. The campaign pauses while you fight, and you return to the map exactly as you left it. To find battles worth fighting, you get both:
  - **filtered alerts:** you choose which battles pause the game and ask you (big ones, near your capital, involving airships, a unit you follow);
  - **a list of every active battle,** which you can join at any time.
- **Soldier mode:** you're a persistent character attached to a division or a squad. The grand strategy runs itself (the AI plays your faction), and you fight where your unit is sent. If you die, you continue as another soldier in the same unit.
  - **Earned promotions:** you start as a grunt, and performance and survival earn promotion to squad leader and on into the officer ranks. Soldier mode is the path through all four ranks.
  - **Between battles** you:
    - pick your loadout from what's actually available (your squad's type, and the equipment your faction has researched and has in stock);
    - follow the war on a read-only strategy map with news of how the front is moving;
    - manage your squad once you lead one: who's in it, their roles and equipment, and replacing losses.

**Single-player only,** in both modes. Bots fill every other role; there's no co-op or PvP. Every system can assume one player, which is the biggest simplification in the project.

### How battles feel

**A battle's feel comes from the strategy map.** The same battle systems should feel different depending on the situation the campaign hands them:

- **High stakes feel high stakes.** A battle that decides a region should feel like it has real consequences at the grand-strategy level. That doesn't mean one grunt swings it: as a grunt you're one soldier, and your personal impact on the outcome is small.
- **Big battles are spectacle,** in the spirit of Battlefield 1 and Ravenfield: walkers, planes, artillery and masses of soldiers at once.
- **Desperation comes from the campaign.** Fighting on bad ground, low on supplies, outnumbered and on the back foot should feel desperate, because the strategy map put you there.
- **Tactics live at the command level:** where squads go, what they attack, who suppresses whom. Not in fine-grained mechanics: not the methodical pace of Squad or Ready or Not.
- **Never Call of Duty run-and-gun.** A lone player sprinting around and out-shooting everyone is the feel to avoid.

## 3. Pillars

1. **Every battle is part of the war.** Battles happen in real places, for reasons the campaign created, with consequences it remembers: manpower, territory, prisoners. Stakes, spectacle and desperation come from the strategy situation.
2. **One soldier in a huge war.** Battles are big and you are small in them. You matter through good orders and good soldiering, never as a super-soldier.
3. **Every rank, in first person.** From grunt to general, each rank is a full way to play, and commanding happens through maps and radio with real delays, not a god's-eye camera. (Vehicles are the one exception: they allow a third-person view.)
4. **Grounded, not run-and-gun.** Detailed soldiering, moderate lethality, suppression and morale make fire superiority and command win fights.
5. **A broken world, built as data.** Fractured factions, deterrence and poisoned land shape every campaign, and the content that defines them is data that's easy to extend and mod.

## 4. Setting

From `Lore Files/` (the details are in `World/`, `Events/` and `Places/`):

- **Divergences:** walking war machines replace the tank in 1916; Fermi recognizes fission in 1934, and his team finds Hesperium, a stable superheavy element that produces lift.
- **The war:** D-Day fails in 1944. In July 1945 the US nukes Germany and Japan with four bombs (one fails). The Allies turn on each other: a nuclear, chemical and biological hot war runs from mid-1946 to about 1948 and ends in collapse, not victory.
- **The world by about 1955:** nations broken into factions; dirty-bomb deterrence freezes borders; the Black Curtain, a poisoned dead zone through Poland, Slovakia and Hungary, splits East from West.
- **Technology:** late 1940s to 1950s.

**The campaign starts in 1955,** in the frozen world: borders are set by deterrence, the Black Curtain is in place, and only a handful of Hesperium airships exist. The player's job is to break the stalemate.

**How the story reaches the player:**

- **HOI4-style events:** pop-ups with choices, triggered by dates, focus trees and situations (Italy's lost program surfaces, a plague outbreak, a coup).
- **Lore in the world:** newspapers, radio broadcasts, intelligence reports, propaganda posters on battle maps and soldiers' chatter.
- **Mysteries to uncover:** open questions such as who fired the first nuke, or where Italy's records went, solved through intelligence, captured sites and scientists.

**The map is the whole world, built Europe first.** Europe around the Black Curtain gets its factions, focus trees and battle maps first; other continents follow.

## 5. Campaign (strategy map)

### Economy

- **Factories and manpower:** factories produce equipment into a national stockpile; regions supply recruits.
- **Strategic resources:** fuel, steel, food and rare materials such as uranium and Hesperium come from specific regions. Running short limits production and operations; walkers, planes and airships all burn fuel.
- **Trade:** resources and equipment can be bought and sold through diplomacy and trade routes, and those routes can be cut.

### Weapons of mass destruction

Nukes, dirty bombs and bioweapons are rare, decisive actions, kept rare by their costs:

- **Retaliation:** targets with WMDs of their own, or with allies who have them, may strike back. The AI judges whether you've crossed its line.
- **Home front:** stability and war support drop; your people and your army may balk, and in extreme cases revolt.
- **Lasting damage:** the target stays irradiated or plague-ridden for years, including land you may want to hold later, and plague can spread back to you.

Using a WMD doesn't by itself turn the rest of the world against you; coalitions form against strength in general, not against WMD use specifically.

### Research

**A HOI4-style research tree.** Factions spend research over time to unlock weapons, walkers, aircraft, airships and doctrines. Decisions and perks can speed research up, as in HOI4. Big capabilities such as airships and the flying carrier sit deep in the tree and also need their own facilities (an airship dock, for example).

**Research is a strategy, not a checklist.** The tree is built around choices that shape what kind of army a faction fields. For example:
- prioritize infantry equipment over walkers, or the reverse;
- research and mass-produce medium walkers;
- focus on heavy walkers, or go further into superheavy ones.

What you research decides what your factories can build, and so what your soldiers actually fight with in first person.

**Equipment trees are laid out like World of Tanks and World of Warships:** each equipment type has lines of designs, one leading to the next, with branches. Superheavy walkers, for example, are their own class but branch off a heavy walker line. The difference is the currency: you advance with research time, not battle experience.

**Choices mostly cost time, but some close doors:**
- **Opportunity cost is the main rule:** most of the tree can eventually be researched, but focusing on one path leaves the others years behind.
- **Some technologies lock out others,** where two designs or approaches can't coexist.
- **Doctrines lock each other out,** HOI4-style: picking one doctrine closes its rivals for good.

**Depth: about 8–13 steps per line or branch.** Roughly 6–7 of them are truly new models; the rest are variants of those models (a better gun, more armor, a new engine, a field conversion). Variants are cheap to make with the Blender generators, so the tree can be deep while only the new models need new art. Depth varies by country: a major arms producer has long lines with rival manufacturers, while a minor nation may have a short line of its own and buy the rest.

Real history supports this pace: in wartime, armies fielded new designs every 2–4 years and upgrades every few months, and the US Air Force went through about a dozen fighters in 1945–1965.

**The tree spans about 20 years, 1955 to 1975.** With 8–13 steps per line, a faction that focuses on one line gets a new step every 1.5–2.5 years, close to real wartime pace; lines it neglects fall years behind. The campaign is a sandbox and can run past 1975, but the tree ends there.

### Grand-strategy systems

The strategy map is no longer "HOI4-lite". It has HOI4's main systems, each simplified where HOI4 turns into busywork:

- **Diplomacy:** alliances, pacts, trade and peace deals, with AI factions that negotiate.
- **Focus trees:** a national focus tree per faction, shaping its path and bonuses.
- **Politics:** ideology, stability, war support, and internal upheaval such as coups and civil wars.
- **Supply and logistics, simpler than HOI4.** Supply must decide wars: cut supply lines and armies weaken, and the battles they fight start short of ammunition, reinforcements and equipment. But building supply shouldn't be a chore; no spending the first years of a campaign spamming railways.

### Factions

**The player can run any faction**, HOI4-style. Major factions get hand-made focus trees; minor factions share a generic tree. Factions are deliberately unequal: starting as a minor splinter state is meant to be a harder game, not a balanced one.

**Equipment is a mix of blocs and national lines,** depending on region and country: some factions field their own designs, others share a bloc's family of equipment. Which is which comes from the lore, which is still being written. Every national line multiplies art work (walkers above all), so the number of lines is a key scope lever.

**Equipment comes from manufacturers.** Within a bloc or nation, designs come from specific makers (arms companies and state design bureaus), each with its own design language, so a maker's walkers, rifles and planes look related. One manufacturer can supply many nations, the way several European countries fly the same Rafale, while some countries develop their own weapons. Which country uses which manufacturer's equipment is set in the lore. Manufacturers aren't a strategy-map mechanic: capturing a region doesn't capture a maker's designs.

**Equipment is deliberately unbalanced.** Quality varies by faction and by period: a poor or cut-off faction may fight for years with obsolete rifles and old walkers, while a rich one fields the newest designs. Weapons are tuned to be believable for their era and maker, not to be fair, and research, production, trade and capture are how a faction climbs out of a bad period.

### Winning

**The campaign is a sandbox,** like HOI4: there's no formal victory screen or end date, and players set their own goals.

### What stops a steamroll

Similar to HOI4, several brakes work together so a strong faction can't simply paint the map:

- **WMD deterrence:** factions with dirty bombs or nukes retaliate when pushed too far, so attacking them is a real gamble. This is the lore's "no one can safely conquer anyone".
- **Occupation costs:** conquered regions resist with partisans, plague, low stability and poor output; holding land is harder than taking it.
- **Coalitions:** other factions ally against whoever grows too strong.
- **Poisoned land:** dead zones and irradiated or plague-ridden regions block or bleed armies, so geography limits expansion.

## 6. Battles

### Gunplay and movement

The reference is Battlefield 1: run-and-gun doesn't work there for the same reasons it shouldn't work here.

- **Moderately lethal.** Deadlier than an arcade shooter, but not one- or two-hit kills across the board. Exact numbers live in each weapon's data row and get tuned in playtests.
- **Suppression is in, for the player too.** Heavy fire near you affects you, not just bots, so winning the firefight matters more than individual aim.
- **Grounded movement.** You feel the weight of a soldier with a rifle; no sliding or twitch strafing.
- **Detailed soldier mechanics.** References: Easy Red 2 and Battlefield, with some DayZ. The soldier is on the detailed side, even though battles aren't as slow as Squad:
  - aim down sights;
  - crouch and prone;
  - lean;
  - manual reload with limited magazines.
- **Survival detail, borrowed from DayZ:**
  - **Injuries and medical:** bleeding and wounded limbs that slow you or spoil your aim, bandages and medics, instead of a plain health bar.
  - **Inventory and weight:** a loadout with slots and weight (magazines, grenades, bandages); carrying more makes you slower and tire sooner.
  - **Scavenging:** take weapons, ammo and gear from the dead and from supply crates mid-battle.
  - **Weapon handling:** chambering rounds, partly used magazines that are kept, jams, and worn weapons.
- **Bots get the same actions.** Every action the player has, bots need to use sensibly too (going prone under fire, leaning around cover), which adds to the AI work.
- **Survival detail scales with distance.** Bots near the player use the full survival systems (wounds, bandaging, weight, scavenging, jams); bots farther away use simple versions. It's a form of AI level of detail: the player only sees the detail where it's close enough to notice, and battles keep their bot counts.

### Morale

Soldiers aren't fearless. Morale is what makes desperate battles feel desperate:

- **Retreat and rout:** squads and whole units break and flee when losses, suppression or a lost leader push them too far.
- **Surrender:** cut-off or broken soldiers can surrender. The player can surrender too, or refuse.
- **Prisoners:** captured soldiers become prisoners of war on the strategy map: manpower lost to one side, which can be exchanged, freed or used in events.
- **The player feels it:** when your unit is breaking, squadmates stop obeying, and the screen and sound reflect the panic.

### Death and respawn

- **You take over a squadmate.** When you die, you continue straight away as a living soldier of your own unit, and the unit is one man smaller. Every death costs real manpower.
- **The same goes for leaders.** A dead squad leader or commander is taken over by another soldier in the chain of command, but there's a delay before the new leader can issue orders. Losing a leader disrupts command, even when the player is the leader.
- **When your whole squad is wiped out,** you continue in a reinforcement unit drawn from the manpower pool. In soldier mode that reinforcement becomes your squad, with new names and new faces. If no reinforcements are left and everyone is dead, you pick a new unit on the strategy screen.

### Commanding

**Commanding stays in first person, but isn't tied to a table.** There's no free-flying RTS camera. The command map opens anywhere, as a map in the commander's hands, so a colonel can lead from the field instead of standing at HQ. Realism comes from how information arrives: units report by radio with a delay, so the map shows where they last reported from, not where they are now. Orders also go out by radio and take time to arrive.

### Scale

**As large as performance allows, varying with the battle.** The strategy map decides each battle's size, from a skirmish between a few squads to a major offensive. Big battles get their size from layered fidelity, the same idea as the survival systems:

- **Near the player:** fully simulated soldiers with every system (survival detail, full AI, full animation).
- **Middle distance:** real soldiers that think less often and animate cheaply.
- **Far away, in the biggest battles:** soldiers simulated in bulk with simple rules and cheap rendering (Unreal's Mass system, with animation baked into textures and played on instanced meshes), turning into full soldiers as you approach.

**Target: battles of 1,000 or more soldiers, proven by an early experiment.** Partway through step 1, once soldiers can fight and die, a time-boxed experiment puts about 1,000 simple Mass soldiers in a battle in the gray-box map and measures performance. If it works, the scale plan stands; if not, battles cap at what standard soldiers can do.

- **What makes it work:** distant soldiers only need to look right and fight plausibly. Their shots can be resolved as hit chances instead of real bullets, and they become full soldiers, with all their state carried over, when the player gets close.
- **Architecture rule from day one:** a soldier's state (health, ammo, wounds, orders, unit) lives in plain data that isn't tied to the soldier's actor, so a soldier can switch between a full actor and a Mass entity. Orders and projectiles are already data, so this extends a rule the design already follows.

The real numbers come from the experiment and the step 1 bot-count test on the target hardware, not from this doc.

**Reference games for big battles** (researched Nov 2026): Rising Front (WWI first-person shooter plus top-down command, 1,000+ units), Kingmakers (Unreal Engine 4, thousands of simulated soldiers via custom multithreaded AI and GPU-driven animation), Project Windless (Unreal Engine 5 with Mass, thousands of soldiers; an action RPG, unreleased) and On All Fronts (an Unreal Engine 5 shooter/RTS built on Mass, apparently stalled). No shipped first-person shooter was found that uses Mass for battles this size, so the far layer is the riskiest part of the scale plan.

### Battle maps

**Generated from the real place, plus hand-made maps for key places.**

- **Generated everywhere:** a battle map is built from real elevation and land-use data for the spot being fought over, plus generated towns, roads, forests, trenches and props in the game's style. Every battle happens in the actual place. The same spot always generates the same map, so a town you fought over before looks the same next time, apart from battle damage.
- **Hand-made where it matters:** capitals, major cities, the Black Curtain and other famous or key places get hand-built maps.
- **Variants are layers on top:** ruined, irradiated and entrenched versions come from the region's state on the strategy map (bombing, WMD strikes, fortification level), not from separate maps.
- This makes a map generator one of the game's main tools, built alongside the battle systems.

### Objectives

**The strategy situation picks the battle type,** and each type has its own objectives:

- **Battle types:** assault, defense, breakthrough, ambush, convoy, raid and others.
- **Capture points:** key spots (a village, a hill, a crossroads) that drain the enemy or win the sector while held.
- **Front-line pushes,** like Battlefield 1's Operations: the attacker takes a line of objectives in order, and the front moves through the map.
- **Targets:** destroy or defend specific things, such as a bridge, a factory, an artillery battery, a supply depot or a downed airship.
- **Reinforcements** come from the units' real manpower, as before.
- **Time limits are optional,** per battle. When a battle has one and it runs out, the auto-resolver carries on the fight.

### Map size

**Map size follows battle size:** about 1 km across for skirmishes, up to 4–8 km for major offensives. Planes fly over a larger, low-detail area around the playable map, so they have room to maneuver without the whole area being a full battlefield.

## 7. Vehicles

### Walkers

**Walkers are the main armor**, as in the lore. The look is dieselpunk, in the spirit of Iron Harvest: riveted steel, exhaust stacks, exposed pistons and crews in the open, fighting right alongside infantry. The designs are our own.

How they're built (a game-feel approach, not a physics simulation):

- **The body moves like a big, slow character:** speed, turn rate, step height. No physics-driven legs.
- **The legs are animation:** a walk cycle plus foot IK so feet plant on uneven ground. Early walkers can use crank-driven linkage legs (Chebyshev's mechanism from the lore), which only need the crank turned by distance travelled.
- **Weight is sold by feel:** body sway, footstep shake, dust.
- **Bots drive them along NavMesh paths**, which is easier than driving physics tanks.
- **Damage:** a shot-out leg cripples a walker or brings it down.

**Classes,** modeled on World of Tanks' roles:

| Class | Role |
| --- | --- |
| Light | Fast scouts that spot and flank |
| Medium | The main battle walker and the backbone of an armored attack |
| Heavy | Slow, heavily armored, anchors a battle |
| Superheavy | A walking fortress: huge, very slow, several turrets, rare and enormously expensive; a battle's centerpiece |
| Walker destroyer | A big gun built to kill other walkers, weaker everywhere else (like a tank destroyer) |
| Artillery | Indirect fire from behind the lines |
| Support | Troop carriers, engineering and recovery walkers |

Each class needs its own model, rig, animation set and bot behavior, and factions will want their own variants, so walker art and animation is one of the largest content costs in the game.

**Why superheavies are their own class:** they play by different rules from heavies. They need their own pathfinding size and can step over walls and trenches; they carry several turrets, which makes them closer to a land warship than a big heavy; bots use them differently (escorted centerpieces, not front-line anchors); and the strategy map limits how many a faction can field. A separate class keeps those rules clean in code, data and the UI. In the research tree they still branch off a heavy line.

**Test asset (Nov 6, 2026):** a light anti-personnel walker inspired by the BT-5, with twin side machine guns, built entirely by a Blender generator script (`Blender Files/Walkers/LightAP/build_walker_light_ap.py`). It has about 4,500 triangles, seven flat colors and 10 bones. The legs are reverse-knee with a keyed walk cycle (two-bone IK computed in the script), not linkage legs. It imported into Unreal and played in `L_GrayBox`. It took one working session, including fixing the export scale. The design was rejected, so the model was removed from the project; the script stays as the template for future walkers and rebuilds the test walker in about 30 seconds. Pipeline notes:

- Every part follows exactly one bone, so rigging is automatic.
- Unreal reads FBX values as raw centimeters and ignores the file's unit tag, so the script converts to centimeters before export.
- The walk is in place; the walker must move at 2.73 m/s for its feet not to slide.

### Airships

**Airships are battleships of the sky:** Hesperium-lifted, nuclear-powered warships. They're strategic assets, not everyday units:

- Only some factions can build and use them; many have none.
- Each one is expensive and slow to build, and its presence shapes a front on the strategy map.
- When one joins a battle, it's one of the biggest things on the field.

**Conventional air power still exists:** propeller fighters, early jets, bombers and ground-attack planes, flown by factions with or without airships.

### Planes

**Flyable, with arcade handling.** Flying should be fun first, in the spirit of Ace Combat: forgiving physics, high speed and readable dogfights, not a simulator.

- **Soldier mode has a pilot career:** you can join an air wing instead of an infantry unit, and rise through it.
- **General mode:** you can take any plane in a battle your faction fights.

### The flying carrier

**The flying aircraft carrier is a wonder-level superweapon.** In principle any faction can build one if it has the resources, the technology and a dock big enough. In practice only the strongest nations manage it, and even they field three at most.

**The player can command an airship** from its bridge: set course, altitude and targets for the bot crew, with command tools like the colonel's. Manning its turrets, an airship career and boarding actions aren't planned.

### Ships

- **Naval battles** are their own battle type: fleet-against-fleet fights at sea.
- **The player can command a warship** from its bridge: course, speed and targets for the bot crew, in the spirit of World of Warships.
- **Amphibious landings** are a ground battle with a sea edge: infantry and walkers storm a beach from landing craft while ships give fire support. The lore makes these hard for walkers, which is part of why D-Day failed.

### Camera

**Infantry play in first person; vehicles allow third person,** World of Tanks and World of Warships style. Walkers, planes, warships and airships can all be driven or commanded from a third-person view.

## 8. Art direction

**Low-poly, decided after the walker test.** Flat colors from a shared palette, clean hard-surface shapes and readable silhouettes, which suit large battles with many units.

- **Hard-surface assets are generated by script in Blender:** walkers, airships, buildings and props. Scripts keep palette, bevel size and scale consistent across the whole game, and variants (faction colors, damage states) are cheap.
- **Organic assets are bought or reused:** soldiers, faces and animals, plus character animation (Unreal's mannequins and animation samples, Mixamo, a store soldier pack).
- **The test walker's design is not final;** it proved the style and the pipeline, not the look of the game's walkers.

**Open:** walker design language (proper designs, starting from reference images).

## 9. Modding

**Data modding from the start; full mod support decided after release.**

- **Game data lives in text files** (CSV or JSON) that the game loads at startup: factions, regions, units and templates, weapons, walkers, research, focus trees and events. Mods add or override rows by stable text IDs, and bad files produce clear error messages.
- **Events and focus trees use a data format** for conditions and effects, the same one used to write the game's own content.
- **It pays off during development too:** readable diffs in Git, tuning without recompiling, and safe AI-assisted edits.
- **Full mod support** (new models, maps and Blueprints through a mod kit) is expensive and has a licensing catch, since bought store assets can't go into a public kit. It's decided after release.

## 10. Scope

**First milestone: the end of step 5.** A small European campaign with infantry and walkers, playable in both general and soldier mode, is the first version worth showing or putting in early access (about 2–3 years in).

**Release model: decided later,** once there's something worth showing. Until then, keep options open: track every asset's license as if the game will be sold, and keep graphics and battle size scalable so it isn't tied to a high-end PC.

**A long-term passion project.** The full vision (HOI4-depth strategy plus a detailed combined-arms shooter) is the goal, with no release deadline. Solo at 5–10 hours a week that's likely a decade or more, so development leans heavily on AI assistance to go faster. Scope gets cut during building, when real costs are known, not up front.

**Build order: battles lead, the strategy map runs alongside.**

- **Main track: battles.** Grunt basics first (moving, shooting, health), then the squad leader. Bot AI and performance are the riskiest work in the project, so they come first, while problems are cheap to fix.
- **Side track: the strategy map.** It's mostly C++ logic and 2D (the region map, the auto-resolver, the economy), so it can be built in separate weeks as a break from 3D work.
- **They meet in the campaign slice:** a small map whose battles launch real first-person fights. The two halves only talk through the BattleSetup and BattleResult, so each can be built and tested on its own until then.
- The colonel comes after both core roles work.

### Roadmap

Every step ends in something playable. Times are rough, at 5–10 hours a week with AI assistance; the real ones get measured as steps finish.

| Step | Done when | Includes | Rough time |
| --- | --- | --- | --- |
| 0. Setup ✅ | The project builds, opens and is safely in version control | Unreal 5.8 C++ project, Git with LFS on GitHub, Unreal MCP | Done Nov 2026 |
| 1. Infantry battle | A battle against bots over objectives on the gray-box map is fun to replay, and the Mass experiment has decided the scale plan | Pieces listed below | 5–9 months |
| 2. Squad leader and soldier depth | You lead a squad of bots through that battle, and soldiering feels detailed | Command wheel and more orders; formations, cover and suppression for squads; injuries and medics, inventory and weight, scavenging, weapon handling; survival detail scaled by distance; morale effects on the player | 3–6 months |
| 3. Campaign slice (general mode) | You conquer a few European regions, fighting battles in first person on generated maps, and the map changes | Both side tracks below come together: 5–10 regions, two or more factions, battles launched from the map, filtered alerts and a battle list, BattleResult applied, the campaign pausing during battles, a versioned save | 3–6 months |
| 4. Walkers | Light and medium walkers fight alongside infantry with bot crews, and you can drive one in first or third person | Walker movement and leg animation from the Blender generator, seats and crews, the third-person camera, bot drivers, shot-out legs, infantry anti-walker weapons; the light and medium classes | 4–7 months |
| 5. Soldier mode | You enlist, follow your unit through the slice's war and earn a promotion | A persistent character, the AI running your faction, between-battle loadout, war news and squad management, reinforcement squads, picking a new unit; serving in a walker crew | 1–3 months |
| 6. Big battles | A major offensive feels huge without losing frame rate | Mass far layer with baked animation, handoff to full soldiers near the player. Only if the step 1 experiment passed; otherwise tune standard soldiers to their limit | 2–4 months |
| 7. Colonel | You win a battle through orders alone | Command map anywhere, radio reports and fog of war, orders by radio with delay, artillery fire missions, off-map air strikes, command delay on leader death | 2–4 months |
| 8. More walkers | All seven walker classes fight, and the colonel can command them | Heavy, superheavy, walker destroyer, artillery and support walkers on the step 4 systems: mostly new models from the generator, data rows and bot behavior; superheavies also need their own pathfinding size and several turrets; artillery walkers fire the colonel's fire missions | 3–5 months |
| 9. Planes | Planes fly air support and dogfight over the battle, and you can fly any of them | Ace Combat-style flight, guns, rockets and bombs, bot pilots, airfields and off-map arrival, the pilot career | 3–6 months |
| 10. Sea and sky | Warships and airships fight, and you can command one | Naval battles, commanding a warship and an airship from the bridge, amphibious landings | 4–8 months |
| 11. Full Europe | A full campaign across Europe with every strategy system | Hundreds of regions, the research tree, diplomacy, focus trees, politics, supply, resources and trade, WMDs and their costs, events and mysteries, the steamroll brakes, and documented data formats for modding | 8–14 months |
| 12+. The world | The full game | Other continents, the flying carrier, national walker lines, hand-made key maps, polish, a release decision | Ongoing |

Steps 1–11 add up to roughly 4–7 years.

**Why walkers sit at step 4:** the campaign slice comes first because proving that battles and the campaign work together is the bigger risk. Walkers come right after it because every later step (soldier mode, big battles, the colonel) is richer with armor, and the test walker already proved the art pipeline. Light and medium are built first because two classes are enough to make the walker systems general; the other four are then mostly new models and data, so they follow in step 8, when the colonel exists to command them. Step 1 matters most: nothing else is added until a battle is fun to replay.

**Side tracks,** worked on in separate weeks as breaks from the main track:

- **A. Strategy map in 2D** (start any time; needed by step 3): the region map for a slice of Europe, factions as data, armies that move, real-time ticks with pause, the auto-resolver, a simple AI. After step 3, a small research prototype on the slice (a few equipment lines and one doctrine lock) tests that research choices change what you fight with, long before the full trees exist.
- **B. Battle map generator** (start once step 1's battle works; needed by step 3): real elevation and land-use data turned into low-poly terrain, roads, forests and towns, the same map for the same place every time, and ruined, irradiated and entrenched variants as layers.
- **C. Lore and research trees** (any time, no engine needed). Equipment, factions, walker designs and the research trees all come from the lore, so this track has deadlines:
  - **before step 3:** the campaign slice's region, its two or more factions, and which manufacturers' equipment each faction fields in 1955 (bloc or national, modern or obsolete). These are the first rungs of their research lines;
  - **before step 4:** each walker manufacturer's design language, which settles the doc's last open art question, plus the light and medium walker rungs for the slice's makers;
  - **after step 3:** the small research prototype's lines (see side track A);
  - **before step 11:** every European faction, the full research trees (all lines, branches, technology locks and doctrines), and the material for focus trees, events and mysteries;
  - **before step 12:** the other continents.

**Step 1 in pieces.** Each takes a week or a few and ends playable:

1. ✅ Walk around a gray-box map with the template's rifle.
2. **Data foundation and projectile manager:** weapons as data rows in text files with stable IDs; soldier state as plain data; `UProjectileSubsystem` replaces the template's bullets.
3. **Your own soldier:** `ASoldierCharacter` with aim down sights, crouch and prone, lean, manual reload with magazines, and grounded movement.
4. **One bot that sees you and shoots back,** using the same soldier class.
5. **Health, wounds, death and two teams,** with taking over a squadmate on death.
6. **The Mass experiment (time-boxed):** about 1,000 simple soldiers fighting in the gray-box map; measure, and decide the scale plan.
7. **Suppression and morale:** suppression for bots and the player; retreat, rout and surrender.
8. **Squads and a bot commander:** squads follow their leaders, and a commander sends them to objectives with orders as data.
9. **Objectives and reinforcements:** capture points and a front-line push; reinforcement units drawn from manpower.
10. **A hand-written BattleSetup** (a text file) decides who spawns with what, and the battle writes a BattleResult.
11. **A performance test** with the chosen scale approach, which sets the bot-count target.
12. **A packaged build** that runs outside the editor, ideally played by a friend.

**How to work through a step** (from the prototype, still true):

- **Gray box first.** Make it work and make it fun with placeholder shapes; art comes last.
- **Playtest every week.** Play the current build, write down the three biggest problems, and fix those first.
- **Keep an ideas list.** New ideas go to "Ideas for later", not into the current step.
- **Cut, don't extend.** If a step runs long, cut features until its "done when" is true, and move the rest to the ideas list.
- **Close each step properly:** a packaged build, a tagged commit, and this doc updated.

### Cut order

If the project runs long and something big has to go, or be pushed past Full Europe:

1. **National lines go first.** Factions share a few bloc equipment families with their own markings.
2. **The Mass far layer goes second.** Battles stay at what standard soldiers can do, a few hundred, even if the experiment passed.
3. **Nothing else is cut.** Flyable planes, sea and sky, and every rank are core; past this point the project slows down instead of shrinking.

## 11. Risks

| Risk | Mitigation |
| --- | --- |
| Bot AI is the biggest body of work: soldiers, squads, commanders, crews, pilots and the strategic AI | Few order types and simple behaviors first; playtest every week |
| The Mass far layer is unproven in Unreal shooters | A time-boxed experiment in step 1 before anything depends on it; soldier state as plain data from day one |
| The battle map generator might not make maps that are fun to fight on | Start it as a side track early; hand-made maps for key places; gray-box test generated maps |
| Content volume: national equipment lines, seven walker classes, focus trees for every major faction | Generator scripts for hard-surface art; blocs before national lines; generic focus trees for minors |
| Solo pace over many years: losing motivation | Every step ends playable; share builds with friends; the ideas list |
| Learning Unreal C++ | Blueprints for wiring and tuning; core systems in C++ with AI help |
| Saves breaking as the game changes | A versioned save format from day one |
| Git LFS storage and bandwidth costs as assets grow | Generated outputs stay out of Git (scripts are the source); check GitHub's LFS usage before buying asset packs |

## 12. Ideas for later

New ideas go here instead of into the current step. Each names the step it fits best.

- **Debrief screen** (step 3): after every battle, show what each side lost, which objectives fell and how the result moved the map battle.
- **A regiment that persists** (step 4 or later): your regiment keeps its name, veterans and losses from battle to battle.
- **Region features as objectives** (step 10): a region's factory, rail hub or bridge becomes a target in its battles, and whether it ends up held or wrecked changes that region on the map.

## Decision log

| # | Date | Question | Decision |
| --- | --- | --- | --- |
| 1 | 2026-11-06 | Which rank is the heart of the game? | Squad leader (battles) and general (campaign) are core; all four ranks should be full experiences |
| 2 | 2026-11-06 | Which order do the ranks get built in? | Left to architecture: battles lead (grunt basics, then squad leader), the strategy map is built alongside as a 2D side track, they meet in the campaign slice, colonel after |
| 3 | 2026-11-06 | What makes 15 minutes as squad leader great? | Situational, set by the strategy map: consequence in high-stakes fights, BF1/Ravenfield spectacle in big ones, desperation when the campaign puts you on the back foot; tactics at the command level, not Squad/RoN; no CoD run-and-gun |
| 4 | 2026-11-06 | What stops CoD-style run-and-gun? | Same reasons as BF1: moderate lethality (not 1–2 hits across the board), suppression that affects the player, grounded movement |
| 5 | 2026-11-06 | Which soldier actions are in? | All of: aim down sights, crouch and prone, lean, manual reload. Detailed side, like Easy Red 2 and Battlefield, some DayZ |
| 6 | 2026-11-06 | Which DayZ aspects? | All four: injuries and medical, inventory and weight, scavenging, weapon handling |
| 7 | 2026-11-06 | Do bots get the survival systems? | Near the player only; distant bots use simple versions |
| 8 | 2026-11-06 | Walkers or tanks? | Walkers, Iron Harvest-style dieselpunk; legs are animation with foot IK, not physics |
| 9 | 2026-11-06 | Which walker classes? | World of Tanks-style: light, medium, heavy, walker destroyer, artillery, support |
| 10 | 2026-11-06 | What are airships in gameplay? | Battleships of the sky: strategic assets only some factions can build; conventional fighters, jets and bombers still exist |
| 11 | 2026-11-06 | Where does the flying carrier fit? | Wonder-level superweapon: buildable by anyone with the resources, technology and docks; in practice only the strongest, three at most |
| 12 | 2026-11-06 | How do factions get new technology? | HOI4-style research tree, sped up by decisions and perks |
| 13 | 2026-11-06 | Which other HOI4 systems are in? | All: diplomacy, focus trees, politics, and supply (simpler than HOI4: decisive, but no railway spam) |
| 14 | 2026-11-06 | Which factions can the player run? | Any faction; majors get custom focus trees, minors share a generic one |
| 15 | 2026-11-06 | How does a campaign end? | Sandbox: no formal win |
| 16 | 2026-11-06 | What stops a steamroll? | Like HOI4, all four: WMD deterrence, occupation costs, coalitions, poisoned land |
| 17 | 2026-11-06 | What's the plan for the scope? | Long-term passion project; maximize AI-assisted development; cut scope later while building |
| 18 | 2026-11-06 | When does the campaign start? | 1955, the frozen world |
| 19 | 2026-11-06 | Which part of the world first? | Europe first; the scope is global |
| 20 | 2026-11-06 | Which art style? | Low-poly, after the scripted walker test; the test walker's design itself was rejected |
| 21 | 2026-11-06 | Which battles can the player join? | Two game modes: general (any battle your faction fights, as much as you like) and soldier (a persistent character in one unit, strategy automated, continue as another soldier in that unit on death) |
| 22 | 2026-11-06 | Does the soldier rise through the ranks? | Yes, by earned promotions, starting as a grunt |
| 23 | 2026-11-06 | What happens between battles in soldier mode? | Pick loadout from available equipment, follow the war on a read-only map, manage your squad as you rise |
| 24 | 2026-11-06 | How do you get back in after dying? | Take over a squadmate; leaders are taken over too, with a delay before the new leader can give orders |
| 25 | 2026-11-06 | What if your whole squad is wiped out? | Continue in a reinforcement unit (in soldier mode it becomes your squad, new people); with no reinforcements left, pick a new unit on the strategy screen |
| 26 | 2026-11-06 | How big are battles? | The larger the better: size varies with the battle, layered fidelity (full detail near the player, cheaper soldiers farther out, Mass only if needed); numbers set by the step 1 performance test |
| 27 | 2026-11-06 | Aim for thousands with Mass? | Yes, as a target proven by a time-boxed experiment partway through step 1 (about 1,000 Mass soldiers fighting); soldier state is plain data from day one so soldiers can switch between actor and Mass |
| 28 | 2026-11-06 | Where do battle maps come from? | Generated from real elevation and land-use data everywhere, plus hand-made maps for key places; ruined, irradiated and entrenched variants are layers driven by the strategy map |
| 29 | 2026-11-06 | What are battles fought over? | All: capture points, front-line pushes, targets, and battle types that vary with the strategy situation; time limits optional |
| 30 | 2026-11-06 | Can you fly planes? | Yes, arcade handling like Ace Combat; a pilot career in soldier mode, any plane in general mode |
| 31 | 2026-11-06 | Can you crew an airship? | Command it from the bridge only; no turret crewing, airship career or boarding |
| 32 | 2026-11-06 | What's playable at sea? | Amphibious landings, commanding a warship, and naval battles; vehicles (air, naval, walkers) allow a third-person camera, World of Tanks / World of Warships style |
| 33 | 2026-11-06 | How does the colonel command? | First person only, no RTS camera; the command map opens anywhere; radio reports and orders still lag |
| 34 | 2026-11-06 | What drives the economy? | Factories and manpower, strategic resources (fuel, steel, food, uranium, Hesperium), and trade; no salvage economy |
| 35 | 2026-11-06 | What does using a WMD cost? | Retaliation, home-front stability and war support, and lasting damage; no automatic world reaction |
| 36 | 2026-11-06 | How is the story told? | HOI4-style events, lore in the world, and mysteries to uncover; no scripted squadmate stories |
| 37 | 2026-11-06 | Should the game support mods? | Data modding from the start (text files, stable IDs, add/override); full mod support with a mod kit decided after release |
| 38 | 2026-11-06 | Who is the game for? | Decide later; meanwhile track asset licenses as if selling, keep performance scalable |
| 39 | 2026-11-06 | Still single-player only? | Yes, no co-op or PvP |
| 40 | 2026-11-06 | What happens to the war during a battle? | The campaign pauses (general mode) |
| 41 | 2026-11-06 | How do you find battles to fight? | Both: filtered alerts that pause and ask, plus a list of every active battle |
| 42 | 2026-11-06 | What happens when soldiers break? | All: retreat and rout, surrender (player too), prisoners of war on the strategy map, morale effects on the player |
| 43 | 2026-11-06 | How different is each faction's equipment? | A mix of blocs and national lines by region and country, set by the lore (in progress) |
| 44 | 2026-11-06 | Pitch and pillars? | Approved as drafted: every battle is part of the war; one soldier in a huge war; every rank in first person; grounded, not run-and-gun; a broken world, built as data |
| 45 | 2026-11-06 | How big is a battle map? | Varies with the battle: about 1 km for skirmishes up to 4–8 km for major offensives, with a larger low-detail area for planes |
| 46 | 2026-11-06 | Where do walkers go in the roadmap? | Light and medium at step 4, right after the campaign slice; heavy, walker destroyer, artillery and support in step 8, after the colonel |
| 47 | 2026-11-06 | Which step makes the first showable game? | The end of step 5: a small European campaign with infantry and walkers, in general and soldier mode |
| 48 | 2026-11-06 | What gets cut first? | National lines (blocs only) |
| 49 | 2026-11-06 | What gets cut second? | The Mass far layer (battles stay at standard-soldier size) |
| 50 | 2026-11-06 | Sea and sky or flyable planes next? | Neither: both are core; past the first two cuts, slow down instead of cutting |
| 51 | 2026-11-06 | Is equipment balanced between factions? | No: quality varies by faction and period; weapons are believable for their era and maker, not fair |
| 52 | 2026-11-06 | When does the lore get written? | Side track C, any time, with deadlines: slice region and factions before step 3, walker design traditions before step 4, all of Europe before step 11 |
| 53 | 2026-11-06 | How binding are research choices? | Mostly opportunity cost; some technologies lock out others; doctrines lock each other out |
| 54 | 2026-11-06 | Where do superheavy walkers fit? | A branch of the heavy line, in World of Tanks / World of Warships-style equipment trees advanced with research time, not battle experience |
| 55 | 2026-11-06 | Should superheavies be their own class? | Yes, a seventh class (own pathfinding size, several turrets, rarity limits); in the research tree they still branch off a heavy line. Replaces the class part of decision 54 |
| 56 | 2026-11-06 | How is shared equipment organized within a bloc? | By manufacturer: each maker has a design language and belongs to a line; one maker can supply many nations (like the Rafale); which country uses what is set in the lore; not a strategy-map capture mechanic |
| 57 | 2026-11-06 | How deep is each research line? | About 8–13 steps per line or branch: roughly 6–7 new models, the rest variants; depth varies by country |
| 58 | 2026-11-06 | How many years does the research tree span? | About 20 years, 1955 to 1975; a focused line gets a new step every 1.5–2.5 years; the sandbox can run past 1975 |
