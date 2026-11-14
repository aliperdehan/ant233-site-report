"""Everything you are likely to want to tweak lives here.

Edit a value, re-run `python make_map.py`, done. A local Claude Code session
can change this file on request (e.g. 'use STIX Two', 'make the accent blue').
"""

# ---------------------------------------------------------------- typography
# First installed family in the list wins. Times New Roman is first (matches the
# report body text); Liberation Serif is a metric-compatible clone of it, and
# STIXGeneral ships inside matplotlib, so the script always finds something.
# To use STIX Two Text, put "STIX Two Text" first (family name as installed).
FONT_FAMILY = ["Times New Roman", "STIX Two Text", "Liberation Serif", "STIXGeneral", "DejaVu Serif"]
FONT_SIZE_PT = 8.0          # site labels
FONT_SIZE_SMALL_PT = 6.5    # ticks, scale bar, river and country names
FONT_SIZE_LEGEND_PT = 7.0
TEXT_AS_PATHS = True        # SVG: convert text to outlines (no font needed on the viewer's machine)

# ------------------------------------------------------------------- colours
# Greyscale-safe: every colour below is distinguishable by lightness alone.
ACCENT = "#A6192E"          # deep red; prints as dark grey. Used only for Krapina.
CROATIA_FILL = "#DCDCDC"
OTHER_FILL = "#F4F4F4"
BORDER = "#8A8A8A"          # thin, light: international borders
RIVER = "#4A4A4A"           # darker and thicker than borders so rivers never read as borders
LAKE = "#BEBEBE"
GRID = "#B8B8B8"
SITE = "#111111"
TEXT = "#111111"
COUNTRY_LABEL = "#8A8A8A"

# -------------------------------------------------------------------- layout
FIG_WIDTH_CM = 15.9         # A4 text width with 2.54 cm (1 in) margins
FIG_HEIGHT_CM = 8.8
FIG_HEIGHT_INSET_CM = 11.5   # inset variant is taller: the stratigraphic panel sits under the legend
LAT_RANGE = (45.70, 46.45)  # main-panel latitude range; longitude range is derived from the aspect
# the inset variant is taller, so its latitude range grows by the same factor: the ground scale and
# the longitude range stay the same (computed in make_map.py, centred on LAT_RANGE)
LON_CENTER = 15.95
SCALE_BAR_KM = 20           # total length, drawn in two halves
GRATICULE_STEP_DEG = 0.25

# Where the country names go (lon, lat). The script checks each point really lies in that country.
COUNTRY_LABELS = [                 # variant A (single wide panel)
    ("CROATIA", 16.45, 46.07),
    ("SLOVENIA", 15.35, 46.30),
]
COUNTRY_LABELS_INSET = [           # variant B (narrower panel)
    ("CROATIA", 16.30, 45.76),
    ("SLOVENIA", 15.50, 46.33),
]
# Natural Earth name -> label shown (NE uses the German name "Drau" for the Drava)
RIVER_LABELS = {"Sava": "Sava", "Drau": "Drava"}

# Inset (variant B): Croatia in Europe, LAEA (EPSG:3035)
INSET_LONLAT_BOX = (4.5, 34.0, 29.5, 53.5)   # lon_min, lat_min, lon_max, lat_max of the inset view
INSET_SIZE_CM = (4.5, 3.6)

# ------------------------------------------------------------------- outputs
OUTPUT_DIR = "output"
FORMATS = ["svg", "pdf"]    # add "png" if you ever need a raster preview
