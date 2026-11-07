# Lore Files

The setting of Black Curtain, kept as many small Markdown files, one per thing. There's no central index: each file carries its own one-line summary in its header, and searching those summaries gives an up-to-date overview of any folder. This README never lists individual files, so it stays the same size however much lore there is.

Works as a plain folder in Git, and as an Obsidian vault (open `Lore Files/` in Obsidian for links, graph view and search).

## Folders

| Folder | Holds | ID prefix |
| --- | --- | --- |
| `World/` | Big concepts that shape everything: divergences, Hesperium, walkers, WMDs, how the world fractured | `wld_` |
| `Events/` | Things that happened, at any scale: a battle, a strike, a coup, a discovery | `evt_` |
| `Factions/` | Each faction as it stands in 1955: the playable and AI actors of the campaign | `fac_` |
| `Nations/` | Pre-collapse countries and what became of them | `nat_` |
| `Manufacturers/` | Arms makers and design bureaus: design language, line, products, who buys from them | `mfr_` |
| `People/` | Notable people | `per_` |
| `Places/` | Zones, corridors, cities and parts of the world (strategy-map regions are game data, with `reg_` IDs) | `plc_` |

Create a folder when its first file arrives. When a folder passes about 50 files, split it by region: `Factions/Europe/`, `Factions/Asia/`.

Two files sit at the top level:

- `Timeline.md`: the master chronology. One line per event, in date order, linking to the file with the details. It's the spine you read in order.
- `OPEN.md`: open questions, contradictions and loose threads. An entry is removed once it's settled and the answer is written into the relevant file.

## Naming rules

- **The file name is the ID:** `evt_dday_fails.md`. IDs are lowercase English, ASCII only, words joined by underscores, starting with the folder's prefix.
- **IDs are unique across all folders,** so a link like `[[evt_dday_fails]]` always finds one file, wherever it moves.
- **Share IDs with the game data.** Factions, manufacturers and equipment use the same IDs the game's data files use (`fac_italy`, `mfr_vulcan`, `wlk_vulcan_light_01`), so lore maps straight onto data. See `CLAUDE.md` for the game's ID rules.
- **Name things by their common English name:** `plc_black_curtain`, `nat_italy`.
- **People are surname first:** `per_fermi_enrico`. Add a distinguishing word only if two people would collide.
- **Events are short, specific names.** Add a year only when the name alone is ambiguous: `evt_july_1945_strikes`.
- **Never rename an ID once other files or game data use it.** If a name turns out wrong, change the title instead.
- **Titles and body text are free:** the `# Title` can be anything readable, and native names belong in the text (阿南惟幾, Mussolini's OVRA).

## File format

Every file starts with this header:

```markdown
---
id: evt_dday_fails
type: event            # world | event | faction | nation | manufacturer | person | place
status: canon          # canon | draft | idea | cut
era: 1944–1945         # a year or a range; "1948–1955+" for open-ended
summary: One line, under about 150 characters, saying what this is.
related: [wld_walkers, evt_july_1945_strikes]
---

# Title

Body.

## In the game
How this shows up in play: equipment lines, focus tree branches, events, mysteries, battle maps.
```

Extra header fields are fine where they help, such as `line:` for a manufacturer or `faction:` for a person.

- **`status`** says how settled something is: `canon` is settled, `draft` is being worked out, `idea` is a possibility, `cut` was dropped. Cut files are kept, not deleted, so old ideas can be found again.
- **`summary`** is what makes the folder searchable. Keep it to one specific line.
- **"In the game"** is optional while writing lore, but it's the bridge to the design doc. Add it once a piece of lore feeds something playable.

## Writing conventions

- **`[REAL]` and `[ALT]` markers** at the start of a bullet or line separate real history from the alternate timeline.
- **Link with `[[id]]`** when another file covers something in more depth.
- **Dates:** years as `1946`, ranges as `1946–1948`, exact dates as `July 1945` or `1945-07-24`.
- **One topic per file.** If a section grows its own sub-story, split it into a new file and link to it.
