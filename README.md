# LILA BLACK · Player Journey Tool (prototype)

Static web tool for Level Designers: journeys, events, playback and heatmaps on the real minimaps.

## Tech stack
Python (pandas/pyarrow/Pillow) pipeline -> compact JSON -> plain HTML/JS + Canvas. No server, no build step, no env vars.

## Run locally
    pip install pandas pyarrow pillow
    python pipeline/build_data.py /path/to/player_data   # writes web/data/*.json and web/maps/*.jpg
    cd web && python -m http.server 8000                  # open http://localhost:8000

## Deploy
Any static host. Vercel: import the repo, set **Root Directory = `web`**, framework "Other", deploy.
(The generated `web/data` and `web/maps` are committed so the host needs no build.)

## Key data facts (see ARCHITECTURE.md once written)
- `ts` is stored typed as ms but the integers are epoch *seconds*; match time = ts - match start.
- Bot = file contains `BotPosition` events (17 numeric-ID files carry human events, so filename alone is wrong).
- 3 `...nakama-0(1)` files are download duplicates and are skipped.
- Minimaps are NOT 1024px as the dataset README says (4320, 2160x2158, 9000); pipeline uses normalized UV coordinates.
