# ARCHITECTURE

## What I built with, and why
A **static site**: a Python pipeline (pandas, pyarrow, Pillow) turns the parquet files into one compact JSON per map; a single `web/index.html` (plain JS + Canvas) draws everything. No server, no build step, no env vars, hosted on Vercel with Root Directory = `web`.
Why: the dataset is small (89k rows), so the browser can do all filtering, playback and heatmaps itself. That means instant interaction, free hosting, and a Level Designer opens a link and it just works. The whole app is one readable file, which also keeps it easy for me to explain.

## Data flow: parquet to screen
1. `pipeline/build_data.py` reads every file in `player_data/February_*` (decoding the `event` bytes to text) and skips 3 download duplicates named `...nakama-0(1)`.
2. It works out time, bot vs human, and map position (below), then writes `web/data/<Map>.json`: `{map, days, matches:[{id, day, dur, players:[{id, bot, pts:[t,x,y,...]}], ev:[[t,type,x,y,playerIdx,isBot]]}]}`. Positions are integers 0–4095 (fraction of image width/height), which keeps Ambrose to about 1 MB. Event types are numeric codes (Kill, Killed, BotKill, BotKilled, KilledByStorm, Loot).
3. It also saves each minimap as a 1600 px JPG in `web/maps/`.
4. In the browser, picking a map fetches that map's JSON and image once, then filters (day, match) run in memory. `draw()` paints the minimap, optional heatmap, paths (human solid cyan, bot dashed amber) and event markers; playback is a `requestAnimationFrame` clock that draws paths and markers up to the current match time.
5. Heatmaps: each point stamps a soft blob onto an offscreen canvas, the alpha is normalised to the busiest pixel and mapped through a colour ramp. They can be scoped to the current filter or all matches on the map.

## Coordinate mapping (the tricky part)
The dataset README gives, per map, a scale and an origin: `u = (x - origin_x) / scale`, `v = (z - origin_z) / scale`, then `px = u · size`, `py = (1 - v) · size`. The y column is elevation, so it is unused. The vertical flip is needed because the image origin is top-left but world z grows upward.
**The README says the minimaps are 1024 px. They are not**: 4320×4320, 2160×2158 and 9000×9000. So the pipeline never uses pixel sizes; it stores normalised `u, v` and the browser multiplies by whatever size the canvas is. Values are clamped to 0–1 so a stray point can't land off the image.
**How I checked it:** every point falls inside the image, paths follow the roads, and kills cluster at buildings. I confirmed this again by overlaying all human positions on Ambrose.

## Assumptions where the data was ambiguous
| Issue | What I found | What I did |
|---|---|---|
| Timestamps | `ts` is typed milliseconds but the integers are epoch **seconds** (Feb 2026). The README's "time within match" is wrong. | Match time = `ts` minus the match's first timestamp. Durations range 13–890 s (median about 382 s); positions are sampled every 5 s. |
| Bot detection | 17 numeric-ID files contain human events, so the filename rule fails. | Bot = the file contains `BotPosition` events. |
| Bot events | `BotKill`/`BotKilled` under a bot's own ID are unclear in the README. | Treated as that bot's own kills and deaths. Stats count "bots killed by humans" and "humans killed by bots" from human files only. |
| Duplicates | 3 files end in `(1)`. | Skipped, leaving 1,243 files, 89,104 rows, 339 players, 796 matches. |
| Who plays | 779 of 780 matches with a UUID human contain exactly one human. Only 3 human-vs-human kills exist. Bot movement is recorded in only 52 matches (bot kills/deaths show up in many more). | Playback defaults to a match with bot movement. The tool says when none was recorded. |
| Grid | The A1–H8 grid covers the whole image, including black unplayable margin. | Documented; "never visited" cells in the margin are not findings. |
| Kill position | Not stated whether it is the killer's or victim's position. | Plotted exactly where it was logged. |
| Storm | The data has storm **deaths** only, not the ring. | Show the deaths; no ring is drawn, since it would be invented. |

## Trade-offs
| Decision | Alternatives considered | Why this |
|---|---|---|
| Static site, pre-processed JSON | Streamlit / a server querying parquet in real time | Zero hosting cost, instant UI, nothing to keep running; data is small and fixed. |
| Plain HTML/JS + Canvas | React, D3, Leaflet, WebGL | No build step, one file, fast to draw 10k+ points; a framework adds weight without adding features. |
| Compact integer coordinates (0–4095) | Raw float32 world coordinates | Much smaller files; precision is far finer than one pixel at 1600 px. |
| 1600 px JPG minimaps | Original 4320–9000 px PNGs | Original files are many MB; 1600 px is sharp enough for the canvas and loads quickly. |
| Generated data committed to the repo | Build in the host at deploy time | The host needs no Python or raw data; the pipeline is still included and documented to regenerate it. |
| Heatmaps computed in the browser | Pre-rendered heatmap images | They react to the day, match and scope filters, which is what a Level Designer needs. |
| No zoom/pan, basic mobile layout | Full pan/zoom and a touch UI | Chose a few features done well; both are listed as known limits. |
