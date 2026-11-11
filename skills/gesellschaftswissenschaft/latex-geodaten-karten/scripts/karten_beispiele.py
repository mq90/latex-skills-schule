#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# ===================================================================
#  karten_beispiele.py  –  erzeugt die Datendateien der Beispielkarten
#  (assets/*_daten.tex) aus Geodaten. Für eigene Karten mit beliebigem
#  Ausschnitt ist geo2tikz.py gedacht; dieses Skript ist der „Atlas“ mit
#  festen Einstellungen für Deutschland, USA, Europa, Welt, Rom und Geschichte.
#
#  latex-skills-schule von Martin Quandt
#
#  Benötigt:  pip install shapely pyproj h5py contourpy scipy
#             (für GeoTIFF-Höhenmodelle zusätzlich: pip install rasterio)
#
#  Daten:     python3 karten_beispiele.py download   lädt alle benötigten Dateien
#             in den Ordner geodaten/ des Skills (ca. 170 MB, einmalig,
#             nicht im Repository)
#
#  Aufruf:    python3 karten_beispiele.py deutschland   -> deutschland_daten.tex
#             python3 karten_beispiele.py usa           -> usa_daten.tex
#             python3 karten_beispiele.py sachsen       -> sachsen_stufen.tex
#             python3 karten_beispiele.py europa        -> europa_daten.tex
#             python3 karten_beispiele.py welt          -> welt_*_daten.tex (3 Projektionen)
#             python3 karten_beispiele.py rom           -> rom_daten.tex
#             python3 karten_beispiele.py historisch    -> historisch_daten.tex
#             python3 karten_beispiele.py               -> alles
#
#  Quellen:   Natural Earth (gemeinfrei), naturalearthdata.com
#             ETOPO1 (NOAA, gemeinfrei) über github.com/fatiando-data
#             Ancient World Mapping Center (ODbL), github.com/AWMC/geodata
#             historical-basemaps (GPL-3.0), github.com/aourednik/historical-basemaps
#
#  Ablauf (für jedes Gebiet):
#    1. Längen-/Breitengrade einlesen        (GeoJSON, WGS84)
#    2. in die Ebene projizieren              (pyproj, z. B. UTM 32N)
#    3. auf Zielbreite in cm skalieren        (z. B. 12 cm)
#    4. Polygonzug vereinfachen               (Douglas-Peucker, Toleranz in cm)
#    5. als TikZ-Pfad "(x,y) -- (x,y) -- ... -- cycle" schreiben
# ===================================================================

import json
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import sys
from pathlib import Path

import shapely
from shapely.geometry import shape, box, MultiPolygon, Polygon, LineString, MultiLineString
from shapely.ops import transform, unary_union, linemerge, polylabel
from pyproj import Transformer

DATEN = Path(__file__).resolve().parent.parent / "geodaten"


# ------------------------------------------------------------------
#  Hilfsfunktionen
# ------------------------------------------------------------------
def lade(datei):
    with open(DATEN / datei, encoding="utf-8") as f:
        return json.load(f)["features"]


def projektor(epsg):
    t = Transformer.from_crs("EPSG:4326", epsg, always_xy=True)
    return lambda geom: transform(t.transform, geom)


def zahl(v):
    s = f"{v:.2f}"
    return "0.00" if s == "-0.00" else s


def punkte(coords):
    """Koordinaten runden; doppelte Nachbarpunkte entfallen."""
    out = []
    for x, y in coords:
        p = f"({zahl(x)},{zahl(y)})"
        if not out or out[-1] != p:
            out.append(p)
    return out


def ring_zu_tikz(ring):
    pkte = punkte(ring.coords)
    if len(pkte) > 1 and pkte[0] == pkte[-1]:
        pkte = pkte[:-1]                    # letzter Punkt = erster Punkt
    return " -- ".join(pkte) + " -- cycle"


def flaeche_zu_tikz(geom, min_flaeche):
    """(Multi-)Polygon -> TikZ-Pfad; Löcher werden mitgezeichnet (even odd rule)."""
    polys = geom.geoms if isinstance(geom, MultiPolygon) else [geom]
    teile = []
    for p in polys:
        if p.is_empty or p.area < min_flaeche:
            continue
        teile.append(ring_zu_tikz(p.exterior))
        for loch in p.interiors:
            if Polygon(loch).area >= min_flaeche:
                teile.append(ring_zu_tikz(loch))
    return "\n  ".join(teile)


def linie_zu_tikz(geom, min_laenge):
    linien = geom.geoms if isinstance(geom, MultiLineString) else [geom]
    teile = []
    for l in linien:
        if l.length < min_laenge:
            continue
        teile.append(" -- ".join(punkte(l.coords)))
    return "\n  ".join(teile)


def mitte(g):
    """Guter Platz für eine Beschriftung: der Punkt im größten Teilpolygon,
    der am weitesten vom Rand entfernt ist (Pol der Unzugänglichkeit)."""
    groesstes = max(getattr(g, "geoms", [g]), key=lambda p: p.area)
    return polylabel(groesstes, tolerance=0.01)


class Karte:
    """Sammelt Gebiete, Flüsse, Seen, Orte – alles schon in cm."""

    def __init__(self, epsg, bbox_grad, breite_cm, toleranz_cm):
        self.proj = projektor(epsg)
        # Rahmen (in Grad) projizieren und Maßstab festlegen
        rahmen = self.proj(box(*bbox_grad).segmentize(0.1))
        x0, y0, x1, y1 = rahmen.bounds
        rahmen = box(x0, y0, x1, y1)              # achsenparalleles Rechteck
        self.m = breite_cm / (x1 - x0)            # cm pro Meter
        self.x0, self.y0 = x0, y0
        self.rahmen = self.cm(rahmen)
        self.tol = toleranz_cm
        self.gebiete, self.mitten, self.fluesse, self.seen, self.orte = {}, {}, {}, {}, {}
        self.ebenen = {}       # weitere Ebenen: {Befehlsname: {Name: Geometrie in cm}}
        self.info = {}         # weitere Zahlenwerte als Makros
        self.massstab = 1 / (self.m / 100)        # 1 cm Karte = ... cm Natur

    def cm(self, geom):
        return transform(lambda x, y, z=None: ((x - self.x0) * self.m, (y - self.y0) * self.m), geom)

    def geo(self, geom_grad):
        return self.cm(self.proj(geom_grad))

    def gebiete_hinzu(self, eintraege):
        """eintraege: {schluessel: geometrie in Grad}. Gemeinsame Grenzen
        werden gemeinsam vereinfacht (coverage_simplify) -> keine Lücken."""
        keys = list(eintraege)
        geoms = [shapely.make_valid(self.geo(eintraege[k]).intersection(self.rahmen)) for k in keys]
        geoms = [g if g.geom_type in ("Polygon", "MultiPolygon") else
                 unary_union([p for p in getattr(g, "geoms", []) if p.geom_type in ("Polygon", "MultiPolygon")])
                 for g in geoms]
        einfach = shapely.coverage_simplify(geoms, tolerance=self.tol)
        for k, g in zip(keys, einfach):
            if not k:                            # Gebiet ohne Kennung
                continue
            if g.is_empty:                       # liegt ganz außerhalb des Rahmens
                continue
            self.gebiete[k] = g
            self.mitten[k] = mitte(g)

    def fluss_hinzu(self, name, geoms_grad, clip=None):
        g = unary_union([self.geo(x) for x in geoms_grad])
        if g.geom_type == "MultiLineString":
            g = linemerge(g)
        g = g.intersection(clip if clip is not None else self.rahmen)
        self.fluesse[name] = g.simplify(self.tol)

    def see_hinzu(self, name, geom_grad):
        self.seen[name] = self.geo(geom_grad).intersection(self.rahmen).simplify(self.tol)

    def ort_hinzu(self, name, lon, lat):
        self.orte[name] = self.geo(shapely.Point(lon, lat))

    def ebene_hinzu(self, befehl, name, geom, in_grad=True, clip=None, toleranz=None):
        """Beliebige weitere Ebene (Fläche oder Linie), z. B. befehl="Gebirge".
        Im Dokument steht dann \\Gebirge{Harz}; \\GebirgeListe enthält alle Namen."""
        g = self.geo(geom) if in_grad else geom
        if g.geom_type in ("MultiLineString", "GeometryCollection"):
            linien = [l for l in getattr(g, "geoms", [g]) if l.geom_type == "LineString"]
            if linien:
                g = linemerge(MultiLineString(linien)) if len(linien) > 1 else linien[0]
        g = shapely.make_valid(g).intersection(clip if clip is not None else self.rahmen)
        g = g.simplify(self.tol if toleranz is None else toleranz)
        if not g.is_empty:
            self.ebenen.setdefault(befehl, {})[name] = g
        return g

    def info_hinzu(self, befehl, wert):
        self.info[befehl] = wert

    # --------------------------------------------------------------
    def schreibe(self, datei, titel, quelle, min_flaeche=0.004, min_laenge=0.1):
        z = []
        w = z.append
        w(f"% {'=' * 66}")
        w(f"%  {titel}")
        w(f"%  automatisch erzeugt mit karten_beispiele.py – bitte nicht von Hand ändern")
        w(f"%  Quelle: {quelle}")
        w(f"%  Kartengröße: {zahl(self.rahmen.bounds[2])} cm x {zahl(self.rahmen.bounds[3])} cm,"
          f" Maßstab ca. 1 : {self.massstab:,.0f}".replace(",", "."))
        w(f"%  Vereinfachungstoleranz: {self.tol} cm")
        w(f"% {'=' * 66}")
        w("%  Verwendung im tikzpicture:")
        w("%    \\draw[fill=...] \\Gebiet{DE-SN};     Fläche (Polygonzug)")
        w("%    \\GeoKoordinaten                     legt benannte Punkte an:")
        w("%    \\node at (DE-SN) {SN};             Punkt im Inneren des Gebiets")
        w("%    \\fill (Leipzig) circle (1pt);      Ort")
        w("%    \\draw \\Fluss{Elbe};                 Linienzug")
        w("%    \\fill \\See{Bodensee};               Fläche")
        w("%    \\foreach \\g in \\GebietListe {...}   alle Gebiete der Datei")
        w(f"% {'=' * 66}")
        w("\\providecommand\\Gebiet[1]{\\csname geo:gebiet:#1\\endcsname}")
        w("\\providecommand\\Fluss[1]{\\csname geo:fluss:#1\\endcsname}")
        w("\\providecommand\\See[1]{\\csname geo:see:#1\\endcsname}")
        bx = self.rahmen.bounds
        w(f"\\def\\HundertKm{{{self.m * 100000:.4f}}}  % so viele cm entsprechen 100 km")
        w("\\providecommand\\Rahmen{\\csname geo:rahmen\\endcsname}")
        w(f"\\expandafter\\def\\csname geo:rahmen\\endcsname{{({zahl(bx[0])},{zahl(bx[1])}) rectangle ({zahl(bx[2])},{zahl(bx[3])})}}")
        w("")
        punkte = 0
        for k, g in self.gebiete.items():
            pfad = flaeche_zu_tikz(g, min_flaeche)
            punkte += pfad.count("(")
            p = self.mitten[k]
            w(f"% --- Gebiet {k}")
            w(f"\\expandafter\\def\\csname geo:gebiet:{k}\\endcsname{{\n  {pfad}}}")
        w(f"\\def\\GebietListe{{{','.join(self.gebiete)}}}")
        w("")
        for k, g in self.fluesse.items():
            pfad = linie_zu_tikz(g, min_laenge)
            punkte += pfad.count("(")
            w(f"% --- Fluss {k}")
            w(f"\\expandafter\\def\\csname geo:fluss:{k}\\endcsname{{\n  {pfad}}}")
        w("")
        for k, g in self.seen.items():
            pfad = flaeche_zu_tikz(g, min_flaeche / 4)
            punkte += pfad.count("(")
            w(f"% --- See {k}")
            w(f"\\expandafter\\def\\csname geo:see:{k}\\endcsname{{\n  {pfad}}}")
        w("")
        for befehl, eintraege in self.ebenen.items():
            w(f"% --- Ebene \\{befehl}")
            w(f"\\providecommand\\{befehl}[1]{{\\csname geo:{befehl}:#1\\endcsname}}")
            w(f"\\def\\{befehl}Liste{{{','.join(eintraege)}}}")
            for k, g in eintraege.items():
                if g.geom_type in ("Polygon", "MultiPolygon"):
                    pfad = flaeche_zu_tikz(g, min_flaeche / 4)
                elif g.geom_type in ("LineString", "MultiLineString"):
                    pfad = linie_zu_tikz(g, min_laenge / 2)
                else:   # gemischt: nur Flächen bzw. Linien übernehmen
                    fl = [x for x in g.geoms if x.geom_type in ("Polygon", "MultiPolygon")]
                    pfad = flaeche_zu_tikz(unary_union(fl), min_flaeche / 4) if fl else \
                        linie_zu_tikz(linemerge([x for x in g.geoms if x.geom_type == "LineString"]), min_laenge / 2)
                punkte += pfad.count("(")
                w(f"\\expandafter\\def\\csname geo:{befehl}:{k}\\endcsname{{\n  {pfad}}}")
            w("")
        for befehl, wert in self.info.items():
            w(f"\\def\\{befehl}{{{wert}}}")
        # benannte Koordinaten: Mittelpunkte der Gebiete und Orte
        w("\\def\\GeoKoordinaten{%")
        for k, p in self.mitten.items():
            if k in self.gebiete:
                w(f"  \\coordinate ({k}) at ({zahl(p.x)},{zahl(p.y)});%")
        for k, p in self.orte.items():
            w(f"  \\coordinate ({k}) at ({zahl(p.x)},{zahl(p.y)});%")
        w("}")
        Path(datei).write_text("\n".join(z) + "\n", encoding="utf-8")
        print(f"{datei}: {len(self.gebiete)} Gebiete, {len(self.fluesse)} Flüsse, "
              f"{len(self.seen)} Seen, {len(self.orte)} Orte, {punkte} Punkte, "
              f"Maßstab 1:{self.massstab:,.0f}")


# ------------------------------------------------------------------
#  Hilfen zum Herausfiltern aus Natural Earth
# ------------------------------------------------------------------
def nach_name(features, namen):
    out = {}
    for f in features:
        n = f["properties"].get("name")
        if n in namen:
            out.setdefault(namen[n], []).append(shape(f["geometry"]))
    return out


# ------------------------------------------------------------------
#  Deutschland
# ------------------------------------------------------------------
def deutschland():
    bbox = (5.4, 47.1, 15.6, 55.15)                      # Rahmen in Grad
    k = Karte("EPSG:25832", bbox, breite_cm=12, toleranz_cm=0.025)   # UTM 32N

    admin = lade("ne_10m_admin_1.geojson")
    rahmen_grad = box(*bbox).buffer(1)
    gebiete = {}
    for f in admin:
        p = f["properties"]
        g = shape(f["geometry"])
        if p["adm0_a3"] == "DEU":
            gebiete[p["iso_3166_2"]] = g
        elif p["adm0_a3"] and g.intersects(rahmen_grad):
            gebiete.setdefault(p["adm0_a3"], []).append(g)    # Nachbarstaaten
    for key, v in list(gebiete.items()):
        if isinstance(v, list):
            gebiete[key] = unary_union(v)
    gebiete["DEU"] = unary_union([g for key, g in gebiete.items() if key.startswith("DE-")])
    k.gebiete_hinzu(gebiete)

    # Flüsse: Natural Earth benennt manche Abschnitte uneinheitlich
    fluesse = {"Rhein": "Rhein", "Rhine": "Rhein", "Rhin": "Rhein", "Elbe": "Elbe",
               "Donau": "Donau", "Weser": "Weser", "Main": "Main", "Oder": "Oder",
               "Mosel": "Mosel", "Ems": "Ems", "Inn": "Inn"}
    europa = {"Neckar": "Neckar", "Saale": "Saale", "Spree": "Spree", "Isar": "Isar",
              "Fulda": "Fulda", "Weisse Elster": "WeisseElster", "Zwickauer Mulde": "Mulde",
              "Havel": "Havel", "Lahn": "Lahn", "Ruhr": "Ruhr", "Lech": "Lech",
              "Werra": "Werra", "Aller": "Aller", "Neisse": "Neisse", "Luzicka Nisa": "Neisse"}
    gefunden = nach_name(lade("ne_10m_rivers_lake_centerlines.geojson"), fluesse)
    for n, g in nach_name(lade("ne_10m_rivers_europe.geojson"), europa).items():
        gefunden.setdefault(n, []).extend(g)
    for n, g in gefunden.items():
        k.fluss_hinzu(n, g)

    seen = {"Bodensee": "Bodensee", "Müritz": "Mueritz", "Schweriner See": "SchwerinerSee",
            "CHIEMSEE": "Chiemsee", "Starnberger See": "StarnbergerSee", "Ammersee": "Ammersee",
            "Steinhuder Meer": "SteinhuderMeer", "Plauer See": "PlauerSee",
            "Kummerower See": "KummerowerSee"}
    s = nach_name(lade("ne_10m_lakes.geojson"), seen)
    for n, g in nach_name(lade("ne_10m_lakes_europe.geojson"), seen).items():
        s.setdefault(n, []).extend(g)
    for n, g in s.items():
        k.see_hinzu(n, unary_union(g))

    # Landeshauptstädte (Längengrad, Breitengrad)
    for name, lon, lat in [
        ("Kiel", 10.1228, 54.3233), ("Hamburg", 9.9937, 53.5511), ("Schwerin", 11.4148, 53.6355),
        ("Bremen", 8.8017, 53.0793), ("Hannover", 9.7320, 52.3759), ("Berlin", 13.4050, 52.5200),
        ("Potsdam", 13.0645, 52.3906), ("Magdeburg", 11.6276, 52.1205), ("Duesseldorf", 6.7735, 51.2277),
        ("Erfurt", 11.0299, 50.9848), ("Dresden", 13.7373, 51.0504), ("Wiesbaden", 8.2398, 50.0782),
        ("Mainz", 8.2473, 49.9929), ("Saarbruecken", 6.9969, 49.2402), ("Stuttgart", 9.1829, 48.7758),
        ("Muenchen", 11.5820, 48.1351), ("Leipzig", 12.3731, 51.3397),
        ("Chemnitz", 12.9214, 50.8278)]:
        k.ort_hinzu(name, lon, lat)

    deu_grad = unary_union([g for key, g in gebiete.items() if key.startswith("DE-")])

    # --- Gebirge (Natural Earth "geography regions", Flächen) ----------
    for f in lade("ne_10m_geography_regions_polys.geojson"):
        p = f["properties"]
        if p["FEATURECLA"] == "Range/mtn" and shape(f["geometry"]).intersects(box(*bbox)):
            name = ascii_name(p["NAME_DE"] or p["NAME"])
            g = k.ebene_hinzu("Gebirge", name, shape(f["geometry"]))
            k.orte[f"Gebirge-{name}"] = mitte(g) if g.geom_type != "GeometryCollection" else g.centroid

    # --- Gipfel: Lage aus Natural Earth, Höhen amtlich gerundet --------
    hoehen = {"Zugspitze": 2962, "Feldberg": 1493, "Brocken": 1141, "Hohe Acht": 747}
    for f in lade("ne_10m_geography_regions_elevation_points.geojson"):
        p = f["properties"]
        if p.get("name") in hoehen:
            k.ort_hinzu(ascii_name(p["name"]), *shape(f["geometry"]).coords[0])
    k.ort_hinzu("Fichtelberg", 12.9544, 50.4292)       # ergänzt (fehlt in Natural Earth)
    hoehen["Fichtelberg"] = 1215
    k.info_hinzu("GipfelListe", ",".join(f"{ascii_name(n)}/{n}/{h}" for n, h in hoehen.items()))

    # --- Höhenschichten aus einem Höhenmodell ---------------------------
    lon, lat, z = lade_hoehenmodell("earth_topo_10min.nc", (5, 46.5, 16, 55.5))
    for stufe, g in hoehenschichten(lon, lat, z, [100, 200, 300, 500, 750, 1000, 1500, 2000],
                                    deu_grad).items():
        k.ebene_hinzu("Hoehe", str(stufe), g)

    # --- Autobahnen und Bahnstrecken (nur innerhalb Deutschlands) -------
    deu_cm = k.geo(deu_grad.buffer(0.01))
    autobahnen = {}
    for f in lade("ne_10m_roads.geojson"):
        nr = str(f["properties"].get("local") or "")
        if f["properties"]["type"] != "Ferry Route" and nr.startswith("A") and nr[1:].isdigit():
            autobahnen.setdefault(nr, []).append(shape(f["geometry"]))
    for nr in sorted(autobahnen, key=lambda n: int(n[1:])):
        g = k.ebene_hinzu("Autobahn", nr, unary_union(autobahnen[nr]), clip=deu_cm)
        if not g.is_empty and g.length > 1.0:          # Beschriftung nur bei langen Autobahnen
            laengste = max(getattr(g, "geoms", [g]), key=lambda l: l.length)
            k.orte[nr] = laengste.interpolate(0.5, normalized=True)
    bahn = [shape(f["geometry"]) for f in lade("ne_10m_railroads.geojson")
            if shape(f["geometry"]).intersects(deu_grad)]
    k.ebene_hinzu("Bahn", "alle", unary_union(bahn), clip=deu_cm, toleranz=0.04)

    k.schreibe("deutschland_daten.tex", "Deutschland mit Bundesländern, Flüssen, Seen, Gebirgen, Verkehr",
               "Natural Earth 1:10m (gemeinfrei); Höhen: ETOPO1 (NOAA) 10', fatiando-data; "
               "Projektion ETRS89/UTM 32N (EPSG:25832)")


# ------------------------------------------------------------------
#  Hilfen: Namen ohne Umlaute, Höhenmodell, Höhenschichten
# ------------------------------------------------------------------
def ascii_name(n):
    for a, b in [("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("Ä", "Ae"), ("Ö", "Oe"), ("Ü", "Ue"),
                 ("ß", "ss"), (" ", ""), ("-", ""), (".", "")]:
        n = n.replace(a, b)
    return n


def lade_hoehenmodell(datei, bbox_grad):
    """Höhenmodell als (lon, lat, z) im Ausschnitt bbox_grad.
    .nc  -> NetCDF wie earth-topography-10arcmin (h5py)
    .tif -> GeoTIFF, z. B. Copernicus DEM oder SRTM (rasterio)"""
    import numpy as np
    x0, y0, x1, y1 = bbox_grad
    if str(datei).endswith(".nc"):
        import h5py
        with h5py.File(DATEN / datei, "r") as h:
            lon, lat = h["longitude"][:], h["latitude"][:]
            i = (lon >= x0) & (lon <= x1)
            j = (lat >= y0) & (lat <= y1)
            z = h["topography"][np.where(j)[0][0]:np.where(j)[0][-1] + 1,
                                np.where(i)[0][0]:np.where(i)[0][-1] + 1]
        return lon[i], lat[j], z.astype(float)
    import rasterio
    from rasterio.windows import from_bounds
    with rasterio.open(DATEN / datei) as r:
        fenster = from_bounds(x0, y0, x1, y1, r.transform)
        z = r.read(1, window=fenster).astype(float)
        t = r.window_transform(fenster)
    lon = t.c + t.a * (np.arange(z.shape[1]) + 0.5)
    lat = t.f + t.e * (np.arange(z.shape[0]) + 0.5)
    if lat[0] > lat[-1]:                     # GeoTIFFs beginnen meist oben (Norden)
        lat, z = lat[::-1], z[::-1]
    return lon, lat, z


def hoehenschichten(lon, lat, z, stufen, gebiet_grad=None, glaetten=4):
    """Für jede Stufe h die Fläche 'höher als h' als (Multi-)Polygon in Grad.
    Die Flächen sind ineinander geschachtelt: erst die tiefste Stufe füllen,
    darüber die nächsthöhere usw. (wie Höhenschichten im Atlas)."""
    import numpy as np
    import contourpy
    from scipy.ndimage import zoom
    if glaetten > 1:                         # feineres Gitter -> rundere Linien
        z = zoom(z, glaetten, order=3)
        lon = np.linspace(lon[0], lon[-1], z.shape[1])
        lat = np.linspace(lat[0], lat[-1], z.shape[0])
    gen = contourpy.contour_generator(lon, lat, z, fill_type=contourpy.FillType.OuterOffset)
    ergebnis = {}
    for h in stufen:
        polys = []
        for pts, offs in zip(*gen.filled(h, 1e5)):
            ringe = [pts[offs[i]:offs[i + 1]] for i in range(len(offs) - 1)]
            if len(ringe[0]) >= 4:
                polys.append(Polygon(ringe[0], [r for r in ringe[1:] if len(r) >= 4]))
        if not polys:
            continue
        g = shapely.make_valid(unary_union(polys))
        if gebiet_grad is not None:
            g = g.intersection(gebiet_grad)
        if not g.is_empty:
            ergebnis[h] = g
    return ergebnis


# ------------------------------------------------------------------
#  USA (48 zusammenhängende Staaten + Alaska und Hawaii als Einschub)
# ------------------------------------------------------------------
def usa():
    feats = [f for f in lade("ne_50m_admin_1_states_provinces_lakes.geojson")
             if f["properties"]["adm0_a3"] == "USA"]
    bbox = (-124.9, 24.3, -66.8, 49.5)
    k = Karte("EPSG:5070", bbox, breite_cm=16, toleranz_cm=0.03)     # Albers flächentreu
    # Rahmen etwas nach unten erweitern, damit die Einschübe Platz haben
    k.rahmen = box(-0.3, -2.6, k.rahmen.bounds[2] + 0.2, k.rahmen.bounds[3] + 0.2)

    gebiete = {f["properties"]["postal"]: shape(f["geometry"]) for f in feats
               if f["properties"]["postal"] not in ("AK", "HI")}
    k.gebiete_hinzu(gebiete)

    # Einschübe: eigene Projektion, eigener Maßstab, verschoben
    def einschub(postal, epsg, laenge_cm, ziel_xy, clip_grad=None):
        g = next(shape(f["geometry"]) for f in feats if f["properties"]["postal"] == postal)
        if clip_grad:
            g = g.intersection(box(*clip_grad))
        g = projektor(epsg)(g)
        x0, y0, x1, y1 = g.bounds
        m = laenge_cm / max(x1 - x0, y1 - y0)
        g = transform(lambda x, y, z=None: ((x - x0) * m + ziel_xy[0], (y - y0) * m + ziel_xy[1]), g)
        k.gebiete[postal] = g.simplify(k.tol)
        k.mitten[postal] = mitte(k.gebiete[postal])

    einschub("AK", "EPSG:3338", 3.6, (0.0, -2.4), clip_grad=(-180, 50, -129, 72))
    einschub("HI", "ESRI:102007", 2.6, (4.0, -2.3), clip_grad=(-161, 18, -154, 23))

    usa48 = unary_union(list(gebiete.values()))
    fluesse = {"Mississippi": "Mississippi", "Missouri": "Missouri", "Ohio": "Ohio",
               "Colorado": "Colorado", "Rio Grande": "RioGrande", "Columbia": "Columbia",
               "Arkansas": "Arkansas", "Tennessee": "Tennessee", "Snake": "Snake"}
    for n, g in nach_name(lade("ne_50m_rivers_lake_centerlines.geojson"), fluesse).items():
        k.fluss_hinzu(n, g, clip=k.geo(usa48.buffer(0.05)))
    seen = {"Lake Superior": "Superior", "Lake Michigan": "Michigan", "Lake Huron": "Huron",
            "Lake Erie": "Erie", "Lake Ontario": "Ontario", "Great Salt Lake": "GreatSaltLake"}
    for n, g in nach_name(lade("ne_50m_lakes.geojson"), seen).items():
        k.see_hinzu(n, unary_union(g))

    for name, lon, lat in [("Washington", -77.0369, 38.9072), ("NewYork", -74.0060, 40.7128),
                           ("LosAngeles", -118.2437, 34.0522), ("Chicago", -87.6298, 41.8781)]:
        k.ort_hinzu(name, lon, lat)

    k.schreibe("usa_daten.tex", "USA mit Bundesstaaten, Flüssen, Großen Seen",
               "Natural Earth 1:50m (gemeinfrei), Projektion Albers (EPSG:5070); AK/HI als Einschub, nicht maßstabsgetreu")


# ------------------------------------------------------------------
#  Sachsen in mehreren Vereinfachungsstufen (Douglas-Peucker)
#  -> zeigt, wie Toleranz, Punktzahl und Flächeninhalt zusammenhängen
# ------------------------------------------------------------------
def sachsen():
    sn = next(shape(f["geometry"]) for f in lade("ne_10m_admin_1.geojson")
              if f["properties"]["iso_3166_2"] == "DE-SN")
    sn = max(getattr(sn, "geoms", [sn]), key=lambda p: p.area)     # Hauptfläche
    flaechentreu = projektor("EPSG:3035")(sn)                           # LAEA Europa
    x0, y0, x1, y1 = flaechentreu.bounds
    m = 5.0 / (x1 - x0)                                                 # 5 cm breit
    sn_cm = transform(lambda x, y, z=None: ((x - x0) * m, (y - y0) * m), flaechentreu)

    z = ["% Sachsen in Vereinfachungsstufen – erzeugt mit karten_beispiele.py",
         "% Flächen berechnet mit der Gaußschen Trapezformel (flächentreue Projektion EPSG:3035)"]
    print("Stufe  Toleranz  Punkte  Fläche (km²)")
    for name, tol in [("Original", 0), ("Fein", 0.02), ("Mittel", 0.1), ("Grob", 0.4)]:
        g = sn_cm.simplify(tol) if tol else sn_cm
        n = len(g.exterior.coords) - 1
        km2 = g.area / m**2 / 1e6
        print(f"{name:7s} {tol:6.2f}   {n:5d}   {km2:9.0f}")
        z.append(f"\\expandafter\\def\\csname geo:gebiet:SN-{name}\\endcsname{{{ring_zu_tikz(g.exterior)}}}")
        z.append(f"\\expandafter\\def\\csname geo:info:SN-{name}\\endcsname{{{n}/{f"{km2:,.0f}".replace(",", "\\,")}}}")
        z.append(f"\\expandafter\\def\\csname geo:punkte:SN-{name}\\endcsname{{{','.join(punkte(g.exterior.coords)[:-1])}}}")
    Path("sachsen_stufen.tex").write_text("\n".join(z) + "\n", encoding="utf-8")


# ------------------------------------------------------------------
#  Graphfärbung (DSatur): Nachbarländer bekommen verschiedene Farben
# ------------------------------------------------------------------
def faerbe(gebiete, schluessel, farben=5):
    """gebiete: {key: Geometrie in cm}. Zwei Gebiete sind benachbart, wenn sie
    sich (fast) berühren. DSatur färbt immer zuerst das Gebiet, dessen Nachbarn
    schon die meisten verschiedenen Farben haben."""
    nachbarn = {a: {b for b in schluessel if b != a and
                    gebiete[a].buffer(0.02).intersects(gebiete[b])} for a in schluessel}
    farbe = {}
    while len(farbe) < len(schluessel):
        offen = [a for a in schluessel if a not in farbe]
        a = max(offen, key=lambda x: (len({farbe[n] for n in nachbarn[x] if n in farbe}),
                                      len(nachbarn[x])))
        belegt = {farbe[n] for n in nachbarn[a] if n in farbe}
        farbe[a] = min(c for c in range(farben + 10) if c not in belegt)
    return farbe


# ------------------------------------------------------------------
#  Europa mit allen Staaten
# ------------------------------------------------------------------
def europa():
    bbox = (-12, 35, 42, 70)
    k = Karte("EPSG:3035", bbox, breite_cm=14, toleranz_cm=0.03)     # flächentreu (LAEA)
    feats = lade("ne_50m_admin_0_countries.geojson")
    gebiete, kontinent, iso = {}, {}, {}
    for f in feats:
        p = f["properties"]
        g = shape(f["geometry"])
        if g.intersects(box(-40, 20, 80, 85)):
            gebiete[p["ADM0_A3"]] = g
            kontinent[p["ADM0_A3"]] = p["CONTINENT"]
            iso[p["ADM0_A3"]] = p["ISO_A2_EH"]
    k.gebiete_hinzu(gebiete)
    eu = [a for a in k.gebiete if kontinent[a] == "Europe"]
    farbe = faerbe(k.gebiete, eu)
    print("Europa: benötigte Farben:", max(farbe.values()) + 1)
    k.info_hinzu("EuropaFarben", ",".join(f"{a}/{farbe[a]}" for a in eu))
    k.info_hinzu("AndereLaender", ",".join(a for a in k.gebiete if a not in eu))
    k.info_hinzu("EuropaKuerzel", ",".join(f"{a}/{iso[a]}" for a in eu
                                           if k.gebiete[a].area > 0.25 and iso[a] != "-99"))
    k.schreibe("europa_daten.tex", "Europa mit allen Staaten",
               "Natural Earth 1:50m (gemeinfrei), Projektion Lambert flächentreu (EPSG:3035)")


# ------------------------------------------------------------------
#  Weltkarte in drei Projektionen (+ Tissot-Kreise)
# ------------------------------------------------------------------
def welt():
    from pyproj import Geod
    feats = lade("ne_110m_admin_0_countries.geojson")
    geod = Geod(ellps="WGS84")
    for name, crs, bbox, antarktis in [("mercator", "EPSG:3395", (-180, -60, 180, 84), False),
                                       ("robinson", "ESRI:54030", (-180, -90, 180, 90), True),
                                       ("equalearth", "EPSG:8857", (-180, -90, 180, 90), True)]:
        k = Karte(crs, bbox, breite_cm=12, toleranz_cm=0.02)
        clip = box(*bbox)
        gebiete, afrika = {}, []
        for f in feats:
            p = f["properties"]
            if p["CONTINENT"] == "Antarctica" and not antarktis:
                continue
            gebiete[p["ADM0_A3"]] = shape(f["geometry"]).intersection(clip)
            if p["CONTINENT"] == "Africa":
                afrika.append(p["ADM0_A3"])
        k.gebiete_hinzu(gebiete)
        # Kreise mit 800 km Radius auf der Erdkugel ("Tissot-Indikatrix")
        n = 0
        for lat in (-45, -15, 15, 45, 75):
            for lon in range(-150, 181, 60):
                if not (bbox[1] < lat < bbox[3]):
                    continue
                lons, lats, _ = geod.fwd([lon] * 73, [lat] * 73, list(range(0, 365, 5)), [800e3] * 73)
                n += 1
                k.ebene_hinzu("Tissot", f"k{n}", Polygon(zip(lons, lats)))
        k.info_hinzu("AfrikaListe", ",".join(a for a in afrika if a in k.gebiete))
        a_afr = sum(k.gebiete[a].area for a in afrika if a in k.gebiete)
        a_grl = k.gebiete["GRL"].area
        k.info_hinzu("AfrikaDurchGroenland", f"{a_afr / a_grl:.1f}".replace(".", "{,}"))
        print(f"{name}: Afrika/Grönland auf der Karte = {a_afr / a_grl:.1f}")
        k.schreibe(f"welt_{name}_daten.tex", f"Welt in der Projektion {name}",
                   f"Natural Earth 1:110m (gemeinfrei), Projektion {crs}")


# ------------------------------------------------------------------
#  Römisches Reich um 200 n. Chr.
# ------------------------------------------------------------------
def rom():
    lcc = "+proj=lcc +lat_0=40 +lon_0=16 +lat_1=33 +lat_2=47 +ellps=WGS84 +units=m"
    bbox = (-11, 24, 46, 56)
    k = Karte(lcc, bbox, breite_cm=15, toleranz_cm=0.03)
    rahmen_grad = box(-30, 15, 65, 65)
    land = unary_union([shape(f["geometry"]) for f in lade("ne_50m_land.geojson")]).intersection(rahmen_grad)
    k.ebene_hinzu("Land", "heute", land)
    awmc = DATEN / "awmc"
    reich = unary_union([shapely.make_valid(shape(f["geometry"])) for f in
                         json.load(open(awmc / "roman_empire_ce_200_extent.geojson"))["features"]])
    k.ebene_hinzu("Reich", "200", reich.intersection(land.buffer(0.02)))
    grenzen = unary_union([shapely.make_valid(shape(f["geometry"])).boundary for f in
                           json.load(open(awmc / "roman_empire_ce_200_provinces.geojson"))["features"]])
    k.ebene_hinzu("Provinzgrenzen", "200", grenzen.intersection(reich.buffer(-0.05)))
    strassen = json.load(open(awmc / "roads.geojson"))["features"]
    for art, wert in (("haupt", "1"), ("neben", "0")):    # Feld "Major_or_M": Hauptstraße ja/nein
        k.ebene_hinzu("Strasse", art, unary_union([shape(f["geometry"]) for f in strassen
                      if f["geometry"] and f["properties"].get("Major_or_M") == wert]), toleranz=0.04)
    fluesse = [shape(f["geometry"]) for f in lade("ne_50m_rivers_lake_centerlines.geojson")
               if f["properties"].get("scalerank", 9) <= 4]
    k.ebene_hinzu("Gewaesser", "alle", unary_union(fluesse).intersection(land))
    for name, lon, lat in [("Roma", 12.4964, 41.9028), ("Londinium", -0.0918, 51.5136),
                           ("ColoniaAgrippina", 6.9583, 50.9375), ("AugustaTreverorum", 6.6414, 49.7499),
                           ("Carthago", 10.3233, 36.8528), ("Alexandria", 29.9187, 31.2001),
                           ("Athenae", 23.7275, 37.9838), ("Antiochia", 36.1612, 36.2021),
                           ("Byzantium", 28.9784, 41.0082), ("Lugdunum", 4.8357, 45.7640),
                           ("Hierosolyma", 35.2137, 31.7683), ("Augusta", 10.8978, 48.3705)]:
        k.ort_hinzu(name, lon, lat)
    k.schreibe("rom_daten.tex", "Römisches Reich um 200 n. Chr.",
               "Ancient World Mapping Center (ODbL), Natural Earth (gemeinfrei); "
               "Projektion Lambert konform, lon_0=16°")


# ------------------------------------------------------------------
#  Deutschland 1938, 1945 und 1949-1990
# ------------------------------------------------------------------
def deutschland_historisch():
    bbox = (4.5, 45.6, 23.6, 56.2)
    k = Karte("EPSG:25833", bbox, breite_cm=12, toleranz_cm=0.03)     # UTM 33N
    rahmen_grad = box(*bbox).buffer(3)
    for jahr in (1938, 1945):
        gebiete = {}
        for f in lade(f"hist_world_{jahr}.geojson"):
            name = f["properties"].get("NAME")
            if not f["geometry"] or not name:
                continue
            g = shapely.make_valid(shape(f["geometry"]))
            if g.intersects(rahmen_grad):
                key = {"Germany": "Reich", "Germany (USA)": "USA", "Germany (UK)": "UK",
                       "Germany (France)": "FRA", "Germany (Soviet)": "SOV"}.get(name, ascii_name(name))
                gebiete[f"{jahr}-{key}"] = unary_union([gebiete[f"{jahr}-{key}"], g]) \
                    if f"{jahr}-{key}" in gebiete else g
        k.gebiete_hinzu(gebiete)
    # heutige Grenzen zum Vergleich
    heute = {}
    for f in lade("ne_10m_admin_1.geojson"):
        p = f["properties"]
        if p["adm0_a3"] == "DEU":
            heute[p["iso_3166_2"][3:]] = shape(f["geometry"])
    k.ebene_hinzu("Heute", "DEU", unary_union(list(heute.values())))
    ost = unary_union([heute[x] for x in ("MV", "BB", "BE", "ST", "SN", "TH")])
    k.ebene_hinzu("Heute", "Ost", ost)
    k.ebene_hinzu("Heute", "West", unary_union(list(heute.values())).difference(ost))
    k.ebene_hinzu("Heute", "Grenze", k.geo(ost).boundary.intersection(k.geo(unary_union(
        [heute[x] for x in heute if x not in ("MV", "BB", "BE", "ST", "SN", "TH")]).buffer(0.01))),
        in_grad=False)
    nachbarn = {}
    for f in lade("ne_10m_admin_0_countries.geojson"):
        g = shape(f["geometry"])
        if f["properties"]["ADM0_A3"] != "DEU" and g.intersects(rahmen_grad):
            nachbarn[f"heute-{f['properties']['ADM0_A3']}"] = g
    k.gebiete_hinzu(nachbarn)
    k.info_hinzu("NachbarnHeute", ",".join(a for a in k.gebiete if a.startswith("heute-")))
    k.info_hinzu("NachbarnReich", ",".join(a for a in k.gebiete if a.startswith("1938-") and a != "1938-Reich"))
    k.info_hinzu("NachbarnZonen", ",".join(a for a in k.gebiete if a.startswith("1945-")
                                         and a[5:] not in ("USA", "UK", "FRA", "SOV")))
    for name, lon, lat in [("Berlin", 13.405, 52.52), ("Leipzig", 12.3731, 51.3397),
                           ("Wien", 16.3738, 48.2082), ("Koenigsberg", 20.5103, 54.7104),
                           ("Bonn", 7.0982, 50.7374), ("Prag", 14.4378, 50.0755)]:
        k.ort_hinzu(name, lon, lat)
    k.schreibe("historisch_daten.tex", "Deutschland 1938, 1945, 1949–1990",
               "historical-basemaps (A. Ourednik, GPL-3.0), Natural Earth (gemeinfrei); UTM 33N")


# ------------------------------------------------------------------
#  Alle benötigten Rohdaten herunterladen (einmalig)
# ------------------------------------------------------------------
NE = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/"
HB = "https://raw.githubusercontent.com/aourednik/historical-basemaps/master/geojson/"
AW = "https://raw.githubusercontent.com/AWMC/geodata/master/Cultural-Data/"
DOWNLOADS = {
    "ne_10m_admin_1.geojson": NE + "ne_10m_admin_1_states_provinces.geojson",
    **{f: NE + f for f in [
        "ne_10m_admin_0_countries.geojson", "ne_50m_admin_0_countries.geojson",
        "ne_110m_admin_0_countries.geojson", "ne_50m_land.geojson",
        "ne_10m_rivers_lake_centerlines.geojson", "ne_10m_rivers_europe.geojson",
        "ne_10m_lakes.geojson", "ne_10m_lakes_europe.geojson",
        "ne_10m_geography_regions_polys.geojson",
        "ne_10m_geography_regions_elevation_points.geojson",
        "ne_10m_roads.geojson", "ne_10m_railroads.geojson",
        "ne_50m_admin_1_states_provinces_lakes.geojson",
        "ne_50m_rivers_lake_centerlines.geojson", "ne_50m_lakes.geojson"]},
    "hist_world_1938.geojson": HB + "world_1938.geojson",
    "hist_world_1945.geojson": HB + "world_1945.geojson",
    "hist_world_200.geojson": HB + "world_200.geojson",
    "earth_topo_10min.nc": "https://github.com/fatiando-data/earth-topography-10arcmin/"
                           "releases/download/v1/earth-topography-10arcmin.nc",
    "awmc/roman_empire_ce_200_provinces.geojson":
        AW + "political_shading/roman_empire_ce_200_provinces/roman_empire_ce_200_provinces.geojson",
    "awmc/roman_empire_ce_200_extent.geojson":
        AW + "political_shading/roman_empire_ce_200_extent/roman_empire_ce_200_extent.geojson",
    "awmc/roads.geojson": AW + "roads/roads.geojson",
}


def download():
    import urllib.request
    for datei, url in DOWNLOADS.items():
        ziel = DATEN / datei
        if ziel.exists():
            print(f"vorhanden: {datei}")
            continue
        ziel.parent.mkdir(parents=True, exist_ok=True)
        print(f"lade {datei} ...", flush=True)
        urllib.request.urlretrieve(url, ziel)


if __name__ == "__main__":
    if sys.argv[1:] == ["download"]:
        download()
        sys.exit()
    alle = {"deutschland": deutschland, "usa": usa, "sachsen": sachsen, "europa": europa,
            "welt": welt, "rom": rom, "historisch": deutschland_historisch}
    for w in sys.argv[1:] or alle:
        alle[w]()
