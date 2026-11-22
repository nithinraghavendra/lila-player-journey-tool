"""Parquet -> compact per-map JSON + web-sized minimaps.
Usage: python pipeline/build_data.py <path-to/player_data> """
import sys, os, re, json, glob
import pandas as pd, pyarrow.parquet as pq
from PIL import Image

SRC = sys.argv[1] if len(sys.argv) > 1 else "player_data"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "web")
# scale, origin_x, origin_z (from the dataset README)
CFG = {"AmbroseValley": (900, -370, -473), "GrandRift": (581, -290, -290), "Lockdown": (1000, -500, -500)}
IMG = {"AmbroseValley": "AmbroseValley_Minimap.png", "GrandRift": "GrandRift_Minimap.png", "Lockdown": "Lockdown_Minimap.jpg"}
EV = {"Kill": 0, "Killed": 1, "BotKill": 2, "BotKilled": 3, "KilledByStorm": 4, "Loot": 5}
Q = 4095  # positions stored as ints 0..4095 across the image (fraction of width/height)

frames = []
for day in sorted(glob.glob(os.path.join(SRC, "February_*"))):
    for f in sorted(os.listdir(day)):
        if re.search(r"\(\d+\)$", f):  # browser-download duplicates like "...nakama-0(1)"
            continue
        d = pq.read_table(os.path.join(day, f)).to_pandas()
        d["event"] = d["event"].apply(lambda b: b.decode("utf-8") if isinstance(b, bytes) else b)
        d["day"] = os.path.basename(day).replace("February_", "Feb ")
        frames.append(d)
df = pd.concat(frames, ignore_index=True)
# ts is typed as ms but the integer is epoch SECONDS (Feb 2026) -> take raw int, treat as seconds
df["t"] = df["ts"].astype("int64")
# bot = file contains BotPosition events (more reliable than the numeric-id filename rule)
df["bot"] = df.groupby(["match_id", "user_id"])["event"].transform(lambda s: (s == "BotPosition").any())

for m, (s, ox, oz) in CFG.items():
    dm = df[df.map_id == m]
    out = {"map": m, "days": sorted(dm.day.unique()), "matches": []}
    for mid, g in dm.groupby("match_id"):
        t0 = g.t.min()
        players, ev = [], []
        for pi, (uid, p) in enumerate(g.groupby("user_id")):
            p = p.sort_values("t")
            u = ((p.x - ox) / s).clip(0, 1); v = (1 - (p.z - oz) / s).clip(0, 1)  # v flipped: image origin top-left
            px, py = (u * Q).round().astype(int), (v * Q).round().astype(int)
            pos = p.event.isin(["Position", "BotPosition"])
            pts = []
            for t, a, b in zip(p.t[pos] - t0, px[pos], py[pos]): pts += [int(t), int(a), int(b)]
            bot = bool(p.bot.iloc[0])
            players.append({"id": uid, "bot": bot, "pts": pts})
            for t, e, a, b in zip(p.t[~pos] - t0, p.event[~pos], px[~pos], py[~pos]):
                if e in EV: ev.append([int(t), EV[e], int(a), int(b), pi, int(bot)])
        ev.sort()
        out["matches"].append({"id": mid[:8], "day": g.day.iloc[0], "dur": int(g.t.max() - t0), "players": players, "ev": ev})
    out["matches"].sort(key=lambda x: (x["day"], -len(x["players"])))
    json.dump(out, open(f"{OUT}/data/{m}.json", "w"), separators=(",", ":"))
    im = Image.open(os.path.join(SRC, "minimaps", IMG[m])).convert("RGB").resize((1600, 1600), Image.LANCZOS)
    im.save(f"{OUT}/maps/{m}.jpg", quality=82)
    print(m, len(out["matches"]), "matches", os.path.getsize(f"{OUT}/data/{m}.json") // 1024, "KB")
