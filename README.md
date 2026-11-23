# LILA BLACK · Player Journey Visualization Tool

A browser tool for Level Designers to see how players move, fight, loot and die on the three LILA BLACK maps, built from 5 days of production telemetry (Feb 10–14, 2026).

**Live tool:** https://lila-player-journey-tool-web.vercel.app

**Docs:** [ARCHITECTURE.md](ARCHITECTURE.md) · [INSIGHTS.md](INSIGHTS.md)

## What you can do
- Pick a map (Ambrose Valley, Grand Rift, Lockdown), then filter by day and by match.
- See each journey on the correct minimap: humans as solid cyan lines, bots as dashed amber lines.
- See kills, deaths (by player or bot), storm deaths and loot as distinct markers; hover a marker for details.
- Play back a single match over time, with speed control and a scrubber.
- Turn on heatmaps for traffic, kill zones and death zones, scoped to the current filter or to all matches on the map.
- Read the in-view stats panel for the current filter.

## Tech stack
Python (pandas, pyarrow, Pillow) for the data pipeline → compact JSON → plain HTML/JS + Canvas for the front end. No server, no build step. Why this stack is in [ARCHITECTURE.md](ARCHITECTURE.md).

## Environment variables
None.

## Run locally
You need Python 3 and the dataset folder (`player_data/`).

```
pip install pandas pyarrow pillow
python pipeline/build_data.py /path/to/player_data   # writes web/data/*.json and web/maps/*.jpg
cd web
python -m http.server 8000                           # then open http://localhost:8000
```

The generated `web/data` and `web/maps` are already committed, so you can skip the pipeline step and only run the last two lines.

## Deploy
Any static host. On Vercel: import the repo, set **Root Directory** to `web`, framework preset "Other", deploy.

## Repo layout
```
web/index.html      the whole front end (UI, canvas drawing, playback, heatmaps)
web/data/*.json     one compact file per map, made by the pipeline
web/maps/*.jpg      minimaps resized to 1600 px
pipeline/build_data.py   parquet → JSON + minimaps
ARCHITECTURE.md     stack, data flow, coordinate mapping, assumptions, trade-offs
INSIGHTS.md         three findings about the game
```

## Data notes (details in ARCHITECTURE.md)
- `ts` is typed as milliseconds but holds epoch **seconds**; match time = `ts` minus match start.
- Bot = the file contains `BotPosition` events (the numeric-ID filename rule alone is wrong).
- 3 download-duplicate files ending `(1)` are skipped.
- The minimaps are not 1024 px, so positions are stored as normalised coordinates.

## Known limits
No zoom or pan; mobile layout is a basic fallback; the storm ring is not drawn because the data only records storm deaths.
