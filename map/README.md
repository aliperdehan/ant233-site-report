# Figure 1: locator map for the Krapina site report

Regenerates the map as **vector** files (SVG + PDF), in two variants for side-by-side comparison:

| File | What it is |
|---|---|
| `output/figure1_single.{svg,pdf}` | Variant A: one panel, northern Croatia |
| `output/figure1_inset.{svg,pdf}`  | Variant B: narrower panel + inset placing it in Europe |

## Regenerate

```bash
pip install -r requirements.txt     # matplotlib, numpy, pyproj
python fetch_data.py                # only if data/ is missing; downloads Natural Earth (public domain)
python verify_coordinates.py        # sanity-check the five points against published distances
python make_map.py                  # writes output/
```

## Files

- `config.py`  fonts, colours, size, extent, label positions. **Edit this to restyle.**
- `sites.csv`  the five points, each with two sources and label placement.
- `make_map.py`  the drawing script. `fetch_data.py` builds `data/*.json`.
- `data/`  small Natural Earth extracts (countries, rivers, lakes), so drawing works offline.

## Fonts

`FONT_FAMILY` in `config.py` is tried in order: Times New Roman, STIX Two Text, Liberation Serif,
STIXGeneral, DejaVu Serif. The first one installed is used. The files in `output/` were made on a
machine without Times New Roman, so they use **Liberation Serif** (metric-compatible with Times New
Roman). Re-run `make_map.py` locally and your own Times New Roman or STIX Two is picked up. SVG text is
converted to outlines (`TEXT_AS_PATHS`), so the SVG looks the same everywhere.

## Colour

Greyscale everywhere, with one accent (`ACCENT`, deep red `#A6192E`) used only for Krapina, so the
figure still reads in black and white.

## Coordinates (details and sources in `sites.csv`)

| Site | Lat N | Lon E | Basis |
|---|---|---|---|
| Krapina (rockshelter, Hušnjakovo) | 46.1647 | 15.8636 | Wikipedia; EGU geolocation (adjacent museum) |
| Vindija | 46.3016 | 16.0797 | Wikipedia (cadastre list); Croatian paper's HTRS96/TM grid reference, converted |
| Velika pećina (Mačkova špilja, Goranec) | 46.2847 | 16.0322 | Wikipedia (cadastre list); Karavanić 2004; Univ. of Alberta record |
| Veternica | 45.8411 | 15.8736 | Wikipedia; World Arachnida Catalog type locality |
| Zagreb | 45.8144 | 15.9780 | GeoNames 3186886 |

Velika pećina is the cave on Ravna gora near Goranec (Hrvatsko zagorje), **not** Velika pećina in
Kličevica (Dalmatia).