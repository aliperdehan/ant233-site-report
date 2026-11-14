"""Stratigraphic panel for the inset variant of Figure 1.

Vertical proportions are read off Gorjanovic-Kramberger's hand-drawn profile of the
Hušnjakovo section ("Brieg Hušnjakovo u Krapini"), as reproduced in Fig. 1 of
Radovčić et al. (2016), C. R. Palevol (sources/newest/radovcic2016.pdf, p. 2).

HOW THE NUMBERS WERE OBTAINED (all heights are on the drawing's own scale, whose unit
is not stated in the text I could read; it is taken to be metres because the fluvial
package comes out at ~1.2 on it and Miracle 2011, p. 88 gives "the lowermost metre"):
  * profile rendered at 600 dpi; the axis ticks give ~130 px per unit;
  * each position is the pixel row of the numeral / dashed line next to the feature,
    converted with a piecewise-linear fit to the tick rows. Uncertainty ~ +-0.1 unit.

WHAT THE NUMERALS ARE: Gorjanovic's numerals 2-8 label the dark cultural BANDS on the
section face (Miracle 2011, p. 88: "8 visible cultural layers that in section appear as
darker bands"), so they are drawn as bands at their heights, not as stacked boxes.

READINGS NOT ON THE DRAWING (agreed choices):
  * band 4: not marked on the edge; placed at the dashed "Homo sapiens" line;
  * band 9: placed at the top dashed "Zona sa Ursus spelaeus" line (top of the fill);
  * rockfall: ~1 m sterile rockfall over level 4 (Trinkaus 1985, p. 204); its extent here
    is schematic, set between band 4 and band 5 where the drawing shows the block "x";
  * Lower/Upper Unit boundary: lies between bands 5 and 6 (Simek & Smith 1997, p. 566:
    Lower = K through 5, Upper = 6 through 9); the line is drawn midway between them.
Other sources used for the labels: Simek & Smith 1997, pp. 562, 565 (hominin zone in 3-4);
Radovčić et al. 2015, pp. 3, 11 (Ursus spelaeus zone = layers 8/9); Rink et al. 1995, p. 24
(ESR 130 +- 10 ka for layers 1-8).
"""
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import config as C

# --- readings on the drawing's scale -------------------------------------------------
BASE = 24.03            # base of the basal gravels
FLUVIAL_TOP = 25.18     # top of the fluvial package (clays under the cave fill)
TOP = 32.11             # top of the fill = "Zona sa Ursus spelaeus" line
BANDS = {2: 26.86, 3: 28.15, 4: 28.39, 5: 29.47, 6: 30.04, 7: 31.17, 8: 31.46, 9: 32.11}
ROCKFALL = (28.45, 29.45)
UNIT_SPLIT = (BANDS[5] + BANDS[6]) / 2
ESR_RANGE = (BASE, BANDS[8])          # Rink et al. 1995: layers 1-8, 130 +- 10 ka

# --- layout, in cm inside the panel --------------------------------------------------
K = 0.588               # cm per scale unit (about per metre); sized so the column spans the panel
COL = (1.05, 1.95)      # column x-range
NUM_X = 2.32            # numerals
TAG_X = 2.78            # right-hand tags
ESR_X = 0.62
GAP = 0.27              # minimum distance between numerals


def panel_height_cm():
    return (TOP - BASE) * K + 0.45


def _spread(desired, gap):
    """Move labels apart (keeping their order) until none is closer than `gap`."""
    items = sorted(desired.items(), key=lambda kv: kv[1])
    changed = True
    clusters = [[i] for i in range(len(items))]
    while changed:
        changed = False
        for a in range(len(clusters) - 1):
            lo, hi = clusters[a], clusters[a + 1]
            top_lo = _centre(clusters[a], items, gap)[-1]
            bot_hi = _centre(clusters[a + 1], items, gap)[0]
            if bot_hi - top_lo < gap - 1e-9:
                clusters[a:a + 2] = [lo + hi]
                changed = True
                break
    out = {}
    for cl in clusters:
        for i, y in zip(cl, _centre(cl, items, gap)):
            out[items[i][0]] = y
    return out


def _centre(cl, items, gap):
    mean = sum(items[i][1] for i in cl) / len(cl)
    n = len(cl)
    return [mean + (j - (n - 1) / 2) * gap for j in range(n)]


def draw_strat(fig, x_cm, y_cm, w_cm, W, H):
    """Draw the panel with its lower-left corner at (x_cm, y_cm) of the figure."""
    ph = panel_height_cm()
    ax = fig.add_axes([x_cm / W, y_cm / H, w_cm / W, ph / H])
    ax.set_xlim(0, w_cm); ax.set_ylim(0, ph); ax.axis("off")
    y0 = 0.03               # column base sits on the main panel's bottom edge
    Y = lambda u: y0 + (u - BASE) * K
    fs = C.FONT_SIZE_SMALL_PT
    ink = C.SITE

    # column body, fluvial block, rockfall
    ax.add_patch(Rectangle((COL[0], Y(BASE)), COL[1] - COL[0], Y(TOP) - Y(BASE), facecolor="#F0F0F0", edgecolor=ink, linewidth=0.6, zorder=2))
    ax.add_patch(Rectangle((COL[0], Y(BASE)), COL[1] - COL[0], Y(FLUVIAL_TOP) - Y(BASE), facecolor="#CFCFCF", edgecolor=ink, linewidth=0.6, hatch="....", zorder=3))
    ax.add_patch(Rectangle((COL[0], Y(ROCKFALL[0])), COL[1] - COL[0], Y(ROCKFALL[1]) - Y(ROCKFALL[0]), facecolor="white", edgecolor="#555555", linewidth=0.4, hatch="////", zorder=3))
    for n, u in BANDS.items():
        ax.plot(COL, [Y(u)] * 2, color=ink, linewidth=0.9 if n < 9 else 0.0, solid_capstyle="butt", zorder=5)
    ax.plot(COL, [Y(UNIT_SPLIT)] * 2, color=ink, linewidth=0.6, linestyle=(0, (2, 1.5)), zorder=5)

    # numerals with leaders
    want = {n: Y(u) for n, u in BANDS.items()}
    placed = _spread(want, GAP)
    for n, yy in placed.items():
        ax.plot([COL[1], COL[1] + 0.12, NUM_X - 0.1], [want[n], want[n], yy], color=ink, linewidth=0.4, zorder=4, solid_capstyle="butt")
        ax.text(NUM_X, yy, str(n), ha="left", va="center", fontsize=fs, color=ink, zorder=6)

    # right-hand tags (brackets)
    def tag(lo, hi, text, x=TAG_X):
        ax.plot([x - 0.1, x - 0.1], [Y(lo), Y(hi)], color=ink, linewidth=0.5, zorder=4)
        ax.text(x, (Y(lo) + Y(hi)) / 2, text, ha="left", va="center", fontsize=fs, color=ink, zorder=6, linespacing=0.95)

    tag(BANDS[8], BANDS[9], "Ursus zone")
    tag(BANDS[3], BANDS[4], "hominin zone")
    tag(*ROCKFALL, "rockfall")
    tag(UNIT_SPLIT - 0.12, UNIT_SPLIT + 0.12, "Lower/Upper Unit")
    tag(BASE, FLUVIAL_TOP, "fluvial base")

    # ESR bracket (left), layers 1-8
    lo, hi = ESR_RANGE
    ax.plot([ESR_X + 0.1, ESR_X, ESR_X, ESR_X + 0.1], [Y(lo), Y(lo), Y(hi), Y(hi)], color=ink, linewidth=0.5, zorder=4)
    ax.text(ESR_X - 0.14, (Y(lo) + Y(hi)) / 2, "ESR 130 ± 10 ka, layers 1–8", rotation=90, ha="center", va="center", fontsize=fs, color=ink, zorder=6)

    # 1 m bar (label above the bar so it clears the "fluvial base" tag)
    bx = w_cm - 0.28
    ax.plot([bx, bx], [Y(BASE), Y(BASE) + K], color=ink, linewidth=1.2, solid_capstyle="butt", zorder=4)
    ax.text(bx, Y(BASE) + K + 0.06, "1 m", ha="center", va="bottom", fontsize=fs, color=ink, zorder=6)

    ax.text(0.0, Y(TOP) + 0.28, "B", ha="left", va="bottom", fontsize=C.FONT_SIZE_PT + 2, weight="bold", color=ink, zorder=6)
    ax.text(0.42, Y(TOP) + 0.28, "Stratigraphic profile", ha="left", va="bottom", fontsize=C.FONT_SIZE_LEGEND_PT, color=ink, zorder=6)
    return ax
