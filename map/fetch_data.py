#!/usr/bin/env python3
"""Download Natural Earth vector data (public domain) and write small extracts to data/.

Source: https://github.com/nvkelso/natural-earth-vector  (geojson/ folder, master branch)
Run once; make_map.py then works offline from the extracts in data/.
"""
import json, pathlib, urllib.request

BASE = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/"
RAW = pathlib.Path("data/raw"); RAW.mkdir(parents=True, exist_ok=True)
OUT = pathlib.Path("data")

# name -> (bbox lon_min, lat_min, lon_max, lat_max) of features to keep, output file, properties to keep
JOBS = [
    ("ne_10m_admin_0_countries", (12.0, 43.0, 20.5, 48.5), "countries_regional.json", ["NAME", "ISO_A3"]),  # filtered to neighbours below
    ("ne_10m_rivers_lake_centerlines", (13.5, 44.0, 18.5, 47.5), "rivers_regional.json", ["name", "scalerank"]),
    ("ne_10m_lakes", (13.5, 44.0, 18.5, 47.5), "lakes_regional.json", ["name"]),
    ("ne_50m_admin_0_countries", (-15.0, 30.0, 45.0, 65.0), "countries_europe.json", ["NAME", "ISO_A3"]),
]

def coords_iter(g):
    t = g["type"]
    if t == "Point": yield g["coordinates"]
    elif t in ("MultiPoint", "LineString"): yield from g["coordinates"]
    elif t in ("MultiLineString", "Polygon"):
        for part in g["coordinates"]: yield from part
    elif t == "MultiPolygon":
        for poly in g["coordinates"]:
            for ring in poly: yield from ring

def rnd(o, nd=3):
    if isinstance(o, float): return round(o, nd)
    if isinstance(o, list): return [rnd(x, nd) for x in o]
    return o

for name, (x0, y0, x1, y1), out, keep in JOBS:
    f = RAW / f"{name}.geojson"
    if not f.exists():
        print("downloading", name); urllib.request.urlretrieve(BASE + name + ".geojson", f)
    data = json.load(open(f, encoding="utf-8"))
    feats = []
    NEIGHBOURS = {"HRV", "SVN", "HUN", "AUT", "ITA", "BIH", "SRB", "MNE", "SVK", "ROU"}
    for ft in data["features"]:
        if name == "ne_10m_admin_0_countries" and ft["properties"].get("ISO_A3") not in NEIGHBOURS: continue
        g = ft.get("geometry")
        if not g: continue
        pts = list(coords_iter(g))
        if not pts: continue
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        if max(xs) < x0 or min(xs) > x1 or max(ys) < y0 or min(ys) > y1: continue
        feats.append({"properties": {k: ft["properties"].get(k) for k in keep},
                      "geometry": {"type": g["type"], "coordinates": rnd(g["coordinates"])}})
    json.dump({"features": feats}, open(OUT / out, "w", encoding="utf-8"), separators=(",", ":"))
    print(f"{name}: kept {len(feats)} features -> data/{out} ({(OUT/out).stat().st_size/1e3:.0f} kB)")
