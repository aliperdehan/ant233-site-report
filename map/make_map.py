#!/usr/bin/env python3
"""Draw Figure 1 (locator map for the Krapina site report) as vector files.

    python make_map.py            # writes output/figure1_single.* and output/figure1_inset.*

Variant A  figure1_single : one panel (northern Croatia).
Variant B  figure1_inset  : the same panel, narrower, plus an inset placing it in Europe.

All styling is in config.py, all coordinates (with their sources) in sites.csv,
all base data (Natural Earth, public domain) in data/ (re-create with fetch_data.py).
"""
import csv, json, math, pathlib, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.patches import Polygon, Rectangle
from matplotlib.path import Path
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter, MultipleLocator
from pyproj import Transformer
import config as C
import strat

CM = 1 / 2.54
HERE = pathlib.Path(__file__).parent

matplotlib.rcParams.update({
    "font.family": "serif",
    "font.serif": C.FONT_FAMILY,
    "font.size": C.FONT_SIZE_PT,
    "svg.fonttype": "path" if C.TEXT_AS_PATHS else "none",
    "pdf.fonttype": 42,
    "axes.linewidth": 0.6,
    "mathtext.default": "regular",
})

# ------------------------------------------------------------------ data
def load(name):
    return json.load(open(HERE / "data" / name, encoding="utf-8"))["features"]

def rings(geom):
    """Exterior rings of a (Multi)Polygon as Nx2 arrays."""
    if geom["type"] == "Polygon":
        return [np.array(geom["coordinates"][0])]
    if geom["type"] == "MultiPolygon":
        return [np.array(p[0]) for p in geom["coordinates"]]
    return []

def lines(geom):
    if geom["type"] == "LineString":
        return [np.array(geom["coordinates"])]
    if geom["type"] == "MultiLineString":
        return [np.array(c) for c in geom["coordinates"]]
    return []

SITES = list(csv.DictReader(open(HERE / "sites.csv", encoding="utf-8")))
for s in SITES:
    s["lat"], s["lon"] = float(s["lat"]), float(s["lon"])
    s["dx"], s["dy"] = float(s["label_dx_pt"]), float(s["label_dy_pt"])

COUNTRIES = load("countries_regional.json")
RIVERS = load("rivers_regional.json")
LAKES = load("lakes_regional.json")
EUROPE = load("countries_europe.json")

def fmt_lon(v, _=None):
    d = int(math.floor(v)); m = int(round((v - d) * 60)); 
    if m == 60: d, m = d + 1, 0
    return f"{d}°{m:02d}′E" if m else f"{d}°E"

def fmt_lat(v, _=None):
    d = int(math.floor(v)); m = int(round((v - d) * 60))
    if m == 60: d, m = d + 1, 0
    return f"{d}°{m:02d}′N" if m else f"{d}°N"

HALO = [pe.withStroke(linewidth=2.2, foreground="white")]

# ------------------------------------------------------------ main panel
def draw_main(ax, w_cm, h_cm, show_legend, country_labels, lat_range=None):
    lat0, lat1 = lat_range or C.LAT_RANGE
    latc = (lat0 + lat1) / 2
    half = (w_cm / h_cm) * (lat1 - lat0) / math.cos(math.radians(latc)) / 2
    lon0, lon1 = C.LON_CENTER - half, C.LON_CENTER + half
    ax.set_xlim(lon0, lon1); ax.set_ylim(lat0, lat1)
    ax.set_aspect(1 / math.cos(math.radians(latc)))   # equal ground distance in x and y

    # land
    for f in COUNTRIES:
        fill = C.CROATIA_FILL if f["properties"]["NAME"] == "Croatia" else C.OTHER_FILL
        for r in rings(f["geometry"]):
            ax.add_patch(Polygon(r, closed=True, facecolor=fill, edgecolor=C.BORDER, linewidth=0.45, zorder=1))
    for f in LAKES:
        for r in rings(f["geometry"]):
            ax.add_patch(Polygon(r, closed=True, facecolor=C.LAKE, edgecolor=C.RIVER, linewidth=0.3, zorder=2))
    # rivers
    for f in RIVERS:
        for ln in lines(f["geometry"]):
            ax.plot(ln[:, 0], ln[:, 1], color=C.RIVER, linewidth=1.0, solid_capstyle="round", zorder=3)

    # graticule + frame ticks
    ax.xaxis.set_major_locator(MultipleLocator(C.GRATICULE_STEP_DEG)); ax.yaxis.set_major_locator(MultipleLocator(C.GRATICULE_STEP_DEG))
    ax.xaxis.set_major_formatter(FuncFormatter(fmt_lon)); ax.yaxis.set_major_formatter(FuncFormatter(fmt_lat))
    ax.grid(True, color=C.GRID, linewidth=0.3, linestyle=(0, (1, 2)), zorder=0.5)
    ax.tick_params(labelsize=C.FONT_SIZE_SMALL_PT, length=2.5, width=0.5, pad=2)
    ax.set_axisbelow(False)

    # river names, placed on the longest visible stretch with the local angle
    for ne_name, label in C.RIVER_LABELS.items():
        best = None
        for f in RIVERS:
            if f["properties"]["name"] != ne_name: continue
            for ln in lines(f["geometry"]):
                for a, b in zip(ln[:-1], ln[1:]):
                    mid = (a + b) / 2
                    if not (lon0 + .04 * (lon1-lon0) < mid[0] < lon1 - .04 * (lon1-lon0) and lat0 + .05*(lat1-lat0) < mid[1] < lat1 - .05*(lat1-lat0)): continue
                    if any(math.hypot((mid[0]-s["lon"]) * math.cos(math.radians(latc)), mid[1]-s["lat"]) < 0.16 for s in SITES): continue
                    seg = math.hypot((b[0]-a[0]) * math.cos(math.radians(latc)), b[1]-a[1])
                    if best is None or seg > best[0]: best = (seg, mid, a, b)
        if best:
            _, mid, a, b = best
            ang = math.degrees(math.atan2((b[1]-a[1]), (b[0]-a[0]) * math.cos(math.radians(latc))))
            if ang > 90: ang -= 180
            if ang < -90: ang += 180
            ax.text(mid[0], mid[1], label, rotation=ang, rotation_mode="anchor", ha="center", va="bottom",
                    fontsize=C.FONT_SIZE_SMALL_PT, style="italic", color=C.RIVER, path_effects=HALO, zorder=4)
        else:
            print(f"note: river '{label}' has no visible stretch in this panel; label skipped")

    # country names (checked to lie inside the right polygon)
    for name, lo, la in country_labels:
        ok = any(Path(r).contains_point((lo, la)) for f in COUNTRIES if f["properties"]["NAME"].upper() == name for r in rings(f["geometry"]))
        if not (lon0 < lo < lon1 and lat0 < la < lat1):
            continue                                   # label point is outside this panel: skip silently
        if not ok: print(f"WARNING: label point for {name} ({lo}, {la}) is not inside {name}; move it in config.py")
        ax.text(lo, la, " ".join(name), ha="center", va="center", fontsize=C.FONT_SIZE_SMALL_PT, color=C.COUNTRY_LABEL, zorder=2.5)

    # sites
    for s in SITES:
        if s["role"] == "focus":
            ax.plot(s["lon"], s["lat"], marker="*", markersize=11, markerfacecolor=C.ACCENT, markeredgecolor="white", markeredgewidth=0.6, zorder=6, linestyle="none")
        elif s["role"] == "cave":
            ax.plot(s["lon"], s["lat"], marker="o", markersize=4.2, markerfacecolor=C.SITE, markeredgecolor="white", markeredgewidth=0.5, zorder=6, linestyle="none")
        else:
            ax.plot(s["lon"], s["lat"], marker="s", markersize=4.2, markerfacecolor="white", markeredgecolor=C.SITE, markeredgewidth=0.9, zorder=6, linestyle="none")
        txt = dict(fontsize=C.FONT_SIZE_PT, color=C.ACCENT if s["role"] == "focus" else C.TEXT,
                   weight="bold" if s["role"] == "focus" else "normal",
                   style="normal", path_effects=HALO, zorder=7)
        kw = dict(xy=(s["lon"], s["lat"]), xytext=(s["dx"], s["dy"]), textcoords="offset points", ha=s["ha"], va=s["va"], **txt)
        if s["leader"] == "1":
            kw["arrowprops"] = dict(arrowstyle="-", lw=0.45, color="#444444", shrinkA=1.5, shrinkB=2.5)
        ax.annotate(s["label"], **kw)

    # scale bar (two halves, alternating black/white)
    km_deg = C.SCALE_BAR_KM / (111.32 * math.cos(math.radians(latc)))
    x0 = lon0 + 0.035 * (lon1 - lon0); y0 = lat0 + 0.06 * (lat1 - lat0); bh = 0.012 * (lat1 - lat0) / 0.75 * 0.75
    ax.add_patch(Rectangle((x0, y0), km_deg / 2, bh, facecolor="black", edgecolor="black", linewidth=0.4, zorder=8))
    ax.add_patch(Rectangle((x0 + km_deg / 2, y0), km_deg / 2, bh, facecolor="white", edgecolor="black", linewidth=0.4, zorder=8))
    for frac, lab in ((0, "0"), (0.5, f"{C.SCALE_BAR_KM // 2}"), (1, f"{C.SCALE_BAR_KM} km")):
        ax.text(x0 + frac * km_deg, y0 + bh + 0.006 * (lat1 - lat0), lab, ha="center", va="bottom", fontsize=C.FONT_SIZE_SMALL_PT, zorder=8, path_effects=HALO)

    # north arrow
    nx, ny = lon1 - 0.04 * (lon1 - lon0), lat1 - 0.07 * (lat1 - lat0)
    ax.annotate("", xy=(nx, ny), xytext=(nx, ny - 0.11 * (lat1 - lat0)), arrowprops=dict(arrowstyle="-|>", lw=0.8, color="black", mutation_scale=7), zorder=8)
    ax.text(nx, ny + 0.012 * (lat1 - lat0), "N", ha="center", va="bottom", fontsize=C.FONT_SIZE_SMALL_PT + 0.5, weight="bold", zorder=8, path_effects=HALO)

    if show_legend:
        h = [Line2D([], [], marker="*", markersize=10, markerfacecolor=C.ACCENT, markeredgecolor="white", linestyle="none", label="Krapina (this report)"),
             Line2D([], [], marker="o", markersize=4.2, markerfacecolor=C.SITE, markeredgecolor="white", linestyle="none", label="Other Middle Palaeolithic cave sites"),
             Line2D([], [], marker="s", markersize=4.2, markerfacecolor="white", markeredgecolor=C.SITE, markeredgewidth=0.9, linestyle="none", label="City (reference)")]
        return h, (lon0, lon1, lat0, lat1)
    return None, (lon0, lon1, lat0, lat1)

# ------------------------------------------------------------------ inset
def draw_inset(ax, extent):
    tr = Transformer.from_crs(4326, 3035, always_xy=True)
    lo0, la0, lo1, la1 = C.INSET_LONLAT_BOX
    # projected bounds from a dense sample of the lon/lat box edges
    xs, ys = [], []
    for lo in np.linspace(lo0, lo1, 25):
        for la in (la0, la1): x, y = tr.transform(lo, la); xs.append(x); ys.append(y)
    for la in np.linspace(la0, la1, 25):
        for lo in (lo0, lo1): x, y = tr.transform(lo, la); xs.append(x); ys.append(y)
    w_cm, h_cm = C.INSET_SIZE_CM
    xmin, xmax, ymin, ymax = min(xs), max(xs), min(ys), max(ys)
    cx, cy = (xmin + xmax) / 2, (ymin + ymax) / 2
    span = max((xmax - xmin) / w_cm, (ymax - ymin) / h_cm)       # metres per cm so the box fits
    ax.set_xlim(cx - span * w_cm / 2, cx + span * w_cm / 2); ax.set_ylim(cy - span * h_cm / 2, cy + span * h_cm / 2)
    ax.set_aspect("equal")
    for f in EUROPE:
        is_hr = f["properties"]["NAME"] == "Croatia"
        for r in rings(f["geometry"]):
            X, Y = tr.transform(r[:, 0], r[:, 1])
            ax.add_patch(Polygon(np.column_stack([X, Y]), closed=True, facecolor="#8C8C8C" if is_hr else "#EFEFEF",
                                 edgecolor=C.BORDER, linewidth=0.25, zorder=1))
    lon0, lon1, lat0, lat1 = extent
    box = [tr.transform(lo, la) for lo, la in ((lon0, lat0), (lon1, lat0), (lon1, lat1), (lon0, lat1))]
    ax.add_patch(Polygon(box, closed=True, facecolor="none", edgecolor=C.ACCENT, linewidth=0.9, zorder=5))
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values(): sp.set_linewidth(0.6)
    hx, hy = tr.transform(16.2, 45.1)
    ax.text(hx, hy - 30000, "CROATIA", ha="center", va="top", fontsize=C.FONT_SIZE_SMALL_PT - 0.5, color="#333333", zorder=6, path_effects=HALO)

# ------------------------------------------------------------------ figures
def fig_single():
    W, H = C.FIG_WIDTH_CM, C.FIG_HEIGHT_CM
    fig = plt.figure(figsize=(W * CM, H * CM))
    l, b, r, t = 1.15, 0.65, 0.15, 0.15
    ax = fig.add_axes([l / W, b / H, (W - l - r) / W, (H - b - t) / H])
    handles, _ = draw_main(ax, W - l - r, H - b - t, True, C.COUNTRY_LABELS)
    leg = ax.legend(handles=handles, loc="lower right", fontsize=C.FONT_SIZE_LEGEND_PT, frameon=True, fancybox=False,
                    edgecolor="black", framealpha=0.95, borderpad=0.5, labelspacing=0.45, handletextpad=0.5, borderaxespad=0.5)
    leg.get_frame().set_linewidth(0.5); leg.set_zorder(20)
    return fig

def fig_inset():
    W, H = C.FIG_WIDTH_CM, C.FIG_HEIGHT_INSET_CM
    iw, ih = C.INSET_SIZE_CM
    fig = plt.figure(figsize=(W * CM, H * CM))
    l, b, r, t, gap = 1.15, 0.65, 0.15, 0.15, 0.35
    main_w = W - l - r - iw - gap
    # same ground scale as the single variant: stretch the latitude range with the height
    la0, la1 = C.LAT_RANGE
    stretch = (H - b - t) / (C.FIG_HEIGHT_CM - b - t)
    lac = (la0 + la1) / 2
    lat_range = (lac - (la1 - la0) * stretch / 2, lac + (la1 - la0) * stretch / 2)
    ax = fig.add_axes([l / W, b / H, main_w / W, (H - b - t) / H])
    handles, extent = draw_main(ax, main_w, H - b - t, True, C.COUNTRY_LABELS_INSET, lat_range)
    ax.text(0.025, 0.975, "A", transform=ax.transAxes, ha="left", va="top", fontsize=C.FONT_SIZE_PT + 2, weight="bold", path_effects=HALO, zorder=20)
    iax = fig.add_axes([(W - r - iw) / W, (H - t - ih) / H, iw / W, ih / H])
    draw_inset(iax, extent)
    leg = fig.legend(handles=handles, loc="upper left", bbox_to_anchor=((W - r - iw - 0.05) / W, (H - t - ih - 0.3) / H),
                     fontsize=C.FONT_SIZE_LEGEND_PT, frameon=False, labelspacing=0.55, handletextpad=0.4, borderpad=0, borderaxespad=0)
    strat.draw_strat(fig, W - r - iw, b, iw, W, H)
    return fig

if __name__ == "__main__":
    out = HERE / C.OUTPUT_DIR; out.mkdir(exist_ok=True)
    for name, fn in (("figure1_single", fig_single), ("figure1_inset", fig_inset)):
        fig = fn()
        for ext in C.FORMATS:
            fig.savefig(out / f"{name}.{ext}", dpi=300)
            print("wrote", (out / f"{name}.{ext}").relative_to(HERE))
        plt.close(fig)
