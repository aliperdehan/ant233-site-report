#!/usr/bin/env python3
"""Sanity-check sites.csv: print coordinates, pairwise distances, and the published
distance/bearing statements the plotted points should agree with."""
import csv, math
R = 6371.0088
def hav(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    d = 2 * R * math.asin(math.sqrt(math.sin((la2-la1)/2)**2 + math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2))
    y = math.sin(lo2-lo1) * math.cos(la2)
    x = math.cos(la1)*math.sin(la2) - math.sin(la1)*math.cos(la2)*math.cos(lo2-lo1)
    return d, (math.degrees(math.atan2(y, x)) + 360) % 360
S = {r["id"]: (float(r["lat"]), float(r["lon"])) for r in csv.DictReader(open("sites.csv", encoding="utf-8"))}
print("Plotted points:"); [print(f"  {k:14s} {v[0]:.4f} N  {v[1]:.4f} E") for k, v in S.items()]
def show(a, b, claim):
    d, br = hav(S[a], S[b]); print(f"  {a} -> {b}: {d:5.1f} km, bearing {br:5.1f} deg   [{claim}]")
print("Checks against published statements:")
show("zagreb", "krapina", "Simek & Smith 1997: Krapina ~40 km NNW of Zagreb (NNW = 337.5 deg)")
show("krapina", "velika_pecina", "Univ. of Alberta site record: ~20 km NE of Krapina")
show("velika_pecina", "vindija", "Karavanic 2004: both on Ravna gora, a few km apart")
show("zagreb", "veternica", "Veternica: <9 km from Zagreb centre (tourist/park sources)")
