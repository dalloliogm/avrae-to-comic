# 2020-2022 PvP Arena Mechanics And Results

- Source logs:
  - `../02-chat-logs/2020-12-24-pvp-sophie-aizza-petyr.md`
  - `../02-chat-logs/2021-01-04-pvp-crathis-leeza-sophie.md`
  - `../02-chat-logs/2021-01-08-pvp-shawn-meifaelor-petyr-luigi.md`
  - `../02-chat-logs/2021-01-12-pvp-meifaelor-petyr.md`
  - `../02-chat-logs/2021-01-14-pvp-aizza-plim.md`
  - `../02-chat-logs/2021-01-18-pvp-sophie-valen-meifaelor.md`
  - `../02-chat-logs/2021-01-21-pvp-meifaelor-willibald-aizza-stone.md`
  - `../02-chat-logs/2021-01-23-pvp-meifaelor-sophie-petyr-stone.md`
  - `../02-chat-logs/2022-09-18-pvp-meifaelor-beholdy-madam-facilier.md`
  - `../02-chat-logs/2022-12-13-pvp-plazza-zaroth-xp-and-arena-source-note.md`
- Material type: PvP arena logs and mechanics reference

## Summary

This batch is mostly PvP arena material rather than campaign plot. It preserves examples of Tortugia's Avrae PvP flow: map movement, height tracking, prone/fall handling, duck reactions, darkness/unseen-target rulings, reward commands, timeout/dropout handling, and PvP arena setup.

Several fights involve Sophie, Aizza, Petyr Quillion, Leeza Impchin, Crathis, Shawn Southwater, Meifaelor Dorlynn, Luigi, Plim, Valen, The Stone Pirate, Willibald Bramblethorn, Madam Facilier, and Beholdy. The imported source does not establish these as Giovanni's character arcs, so these entries should be treated primarily as mechanics/source archive unless later context says otherwise.

## Notable Outcomes

- 2021-01-04: Leeza dropped Crathis with Produce Flame, then Sophie later defeated Leeza with a readied pistol shot after Leeza emerged from cover.
- 2021-01-08: Shawn Southwater dropped out; Meifaelor, Luigi, and Petyr continued. Luigi later dropped Meifaelor with Hex + Eldritch Blast after darkness was removed.
- 2021-01-18: Sophie defeated Valen in PvP, then a new fight involving Meifaelor began.
- 2021-01-21: Meifaelor used Portent with Hold Person during a PvP opening against The Stone and Willibald. Willibald used Circle of the Shepherd's Bear Spirit to give temporary HP to himself and Aizza.
- 2021-01-23: Petyr broke Meifaelor's Hold Person concentration with Guiding Bolt, Sophie knocked Meifaelor out, and the remaining fight shifted toward Sophie, Petyr, and The Stone.
- 2022-12-13: Meifaelor gained 480 XP for defeating Zaroth and leveled to 13.

## Mechanics Worth Remembering

- PvP rewards commonly use `!coins + <level> gp` and `!XPgrant <5 * defeated level>`, with inspiration and movement/ammo cleanup commands.
- Dropout/timeout text instructs remaining rovers to use `!insp+`, `!mov start`, `!ammo collect`, coin reward, and `!XPgrant`.
- `!pvp quit` can fail if the character is not in the correct arena location; `!FIX` was used once to repair a stuck state.
- Height is tracked on the map for flying/climbing creatures and characters.
- Falling/prone mechanics can trigger item dropping and acrobatic landing choices.
- Ducking is a reaction involving a Dexterity save against the attack roll, with the character falling prone.
- Unseen target home rules can randomize the shot target's space if the target is not hiding but cannot be pinpointed by noise.
- Non-lethal damage has special handling for non-bludgeoning melee weapons and thunder damage.
- Heat Metal object targeting needs care: Sophie was not wearing armor, so targeting the shield was corrected.
- Portent can be used to force a failed save, but mixed targeting may require manual effect cleanup when one target rolls normally and another uses the portent result.
- Hold Person concentration loss removes paralysis and can abruptly shift a PvP fight.
- Shepherd Druid Bear Spirit grants temporary HP in a 30-foot aura and can be used tactically in PvP team-ups.
- Spike Growth can shape melee/ranged positioning and deals damage per 5 feet of movement through the area.

## Locations

- Plazza: PvP arena at The B / B's cafe.
- The B: cafe associated with a cosmopolitan crowd, outdoor tables, the Plazza, and the Large Talking Cactus notice board.

## Open Questions

- Whether Averagius, mentioned as level 7, should receive a character note.
- Whether Beholdy is a summoned/controlled creature, NPC, or player character tied to Sfollac.
