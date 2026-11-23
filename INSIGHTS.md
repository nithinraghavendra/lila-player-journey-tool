# INSIGHTS

Three things I learned about LILA BLACK using the Player Journey tool.

**Basis:** 5 days (Feb 10–14, 2026), 796 matches, 798 human journeys. Ambrose Valley has most of the data (566 matches), so insights 1 and 2 are mainly Ambrose. Cells are the tool's A1–H8 grid (letter = column, number = row from the top). Counts are for human players only. I compare **rates** (events per 1,000 position samples) rather than raw counts, because busy areas would otherwise look dangerous just for being busy.

---

## 1. Every map funnels players into one central kill zone

**What caught my eye.** With the kills heatmap on, all three maps light up in the middle, and the Humans-only traffic view shows the same shape: players spawn on the edge and converge.

**Evidence.**
- Ambrose: C4, C5, D4, D5 and E5 are 5 of 64 cells (8% of the image) but hold **34% of traffic, 61% of bot kills and 69% of deaths**.
- It is not just traffic. D3–D5 averages **103 kills per 1,000 position samples vs 37** for the rest of the map. E5 has the most traffic (10% of samples) but only 60 kills per 1,000.
- Phase of the match: minute 0–1 players are on the edge (A4, F5, B7, C7); minutes 1–6 on mid compounds (B7, E5, D7); from minute 6 on, D4 and D5 alone hold **28% of all player time**.
- Same pattern elsewhere: GrandRift D5 + D4 = 68 of 180 kills (**38%**); Lockdown's top three cells (E4, C5, E5) hold 36% of kills.

**Actionable? Yes.**
- *Proposed actions:* give mid-map compounds (B7, D7, E7, D2) a reason to stop at them (better loot or an objective), and add cover or alternate approaches into D3–D5 so the fight isn't one dense brawl.
- *Metrics affected:* share of kills in the top-5 cells (now 61%), kills per 1,000 samples in D3–D5 vs elsewhere, share of time spent in the centre after minute 6, deaths per journey.
- *Target to agree with design:* a flatter kill spread. I propose a lower share in the top-5 cells; the exact number is a design decision.

**Why a Level Designer should care.** If 60% of fights happen on 8% of the map, the other 92% of the art, loot and routes carry little of the gameplay. It also shows where to add or remove cover, and which compounds are bypassed.

---

## 2. One spawn is a trap, and edge loot is almost free

**What caught my eye.** Splitting journeys by where they start showed that C6 is not like the others, and the loot heatmap in the first minute shows safe loot around the edge.

**Evidence.** Ambrose has 7 edge spawns (F5, F2, A4, C8, B1, A7, C6), each used by about 12–15% of journeys.

| Spawn | Journeys | Died to a bot within 3 min | Median journey | Loot per journey |
|---|---|---|---|---|
| **C6** | 66 | **35%** | **243 s** | **13.1** |
| F2 | 86 | 17% | 314 s | 16.7 |
| F5 | 87 | 15% | 367 s | 19.1 |
| B1 | 77 | 13% | 362 s | 17.7 |
| A7 | 67 | 12% | 404 s | 18.6 |
| A4 | 82 | 9% | 337 s | 17.4 |
| C8 | 79 | 8% | 392 s | 19.4 |
| *All Ambrose* | *568* | *15%* | | |

- C6 sits directly beside **C5, the deadliest cell on the map** (24 deaths per 1,000 samples; 57 deaths). That is my hypothesis for the cause, not something the data proves.
- Edge loot: A4, B2 and C7 hold **14.4% of Ambrose loot but only 0.8% of kills**, picked up at a median of **60 s** into the match vs 292 s in the five central cells.

**Actionable? Yes.**
- *Proposed actions:* move or shield the C6 spawn (cover, a safer first route, or a slightly later bot activation near C5). Move some of the better loot from the safe edge towards the mid-map so risk and reward line up.
- *Metrics affected:* early-death rate by spawn (C6 35% vs 15% overall), median survival time by spawn, loot per journey by spawn, share of loot taken in low-kill cells.
- *Target to agree with design:* early-death rates within a few points of each other across spawns.

**Why a Level Designer should care.** Spawn position decides some players' first three minutes before they have made a single choice. That is a fairness and first-impression problem, and it can be fixed with level geometry alone.

**Caution.** C6 is 66 journeys (about 23 early deaths). It is strong enough to act on for a playtest, not strong enough to treat as final.

---

## 3. The storm is a late timer, not a force that shapes the map

**What caught my eye.** Storm deaths barely register on any heatmap: only 39 in the whole dataset.

**Evidence.**
- All 39 storm deaths happen between **655 s and 887 s** (median 739 s). **None happen earlier.**
- Only **4.9%** of the 798 journeys end in a storm death. The median journey is 364 s, and only about 24% last past 600 s.
- Of the 188 journeys that reach 600 s, 39 (**20.7%**) die to the storm. Almost nobody reaches it, but nearly everyone who does is under real pressure.
- It is spatially scattered: no cell has more than 3 storm deaths (Ambrose D6 and Lockdown F4 top the list).
- Per journey, it bites more on smaller maps: Lockdown 9.9% (17/171), GrandRift 8.5% (5/59), Ambrose 3.0% (17/568).

**Actionable? Yes, with a caveat.** The data has storm deaths only, not the storm's position, so I can't see its path.
- *Proposed actions:* playtest an earlier or faster first shrink (or an early warning phase) so the storm affects decisions before minute 11. Check that the storm direction pushes players through the under-used areas instead of past them.
- *Metrics affected:* share of journeys ending in storm death, share of journeys reaching 600 s, median journey length, spread of storm deaths across cells.
- *Target to agree with design:* decide what share of players the storm should reach, then tune the timing to hit it.

**Why a Level Designer should care.** A storm that only matters after minute 11 does not push anyone toward quiet areas, so those areas stay empty. It is the main lever for spreading players across the map.

---

## Limits of this analysis

- **Mostly PvE.** 779 of 780 matches with a UUID human contain exactly one human, and there are only 3 human-vs-human kills. I can't judge PvP sightlines or chokepoints from this data.
- **Bot movement is recorded in only 33 of 566 Ambrose matches**, so "no bots there" claims are weak. Bot kills and deaths are logged in the human's file and are used instead.
- **Kill position.** The data doesn't say whether a kill is logged at the killer's or the victim's position; I treat it as where the event was recorded.
- **Unknown endings.** About 44.5% of journeys have no recorded death; I can't tell whether they extracted or quit.
- **Causes are hypotheses.** The data shows what happened and where. Why it happens (for example the C6/C5 link) needs a playtest to confirm.
- **Grid.** The grid covers the whole minimap image, including black unplayable margin, so "never visited" cells in the G/H columns and top and bottom rows are not a design finding.
