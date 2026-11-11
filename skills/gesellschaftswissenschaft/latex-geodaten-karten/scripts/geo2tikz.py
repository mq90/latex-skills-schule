#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""
geo2tikz.py – wandelt GeoJSON-Geodaten in TikZ-Code für LaTeX um.

Mehrere Ebenen (z. B. Bundesländer, Flüsse, Seen, Städte) werden in EINEM
Aufruf umgerechnet, damit alle dieselbe Projektion und denselben Maßstab
haben und genau übereinanderpassen.

Benötigt: pip install shapely pyproj

Beispiel: Deutschland mit Bundesländern, Flüssen und Seen
---------------------------------------------------------------------
  python3 geo2tikz.py --bbox 5.8,47.2,15.1,55.1 --breite 12 --proj EPSG:3035 \\
    --ebene "name=laender; datei=ne_10m_admin_1_states_provinces.geojson; filter=iso_a2=DE; id=iso_3166_2" \\
    --ebene "name=fluesse; datei=ne_10m_rivers_lake_centerlines.geojson; id=name" \\
    --ebene "name=seen; datei=ne_10m_lakes.geojson; id=name" \\
    -o karte_daten.tex

Im Dokument:
  \\input{karte_daten}
  \\tikzset{geo laender/.style={fill=gray!15, draw=white, line width=0.4pt},
           geo laender/DE-SN/.style={fill=red!40}}
  \\begin{tikzpicture}
    \\geolaender  \\geofluesse  \\geoseen
    \\node at (laender-DE-SN) {Sachsen};
  \\end{tikzpicture}

Ebenen-Schlüssel (mit ; getrennt):
  name=   Name der Ebene → Makro \\geo<name>, Stil „geo <name>“  (nur Buchstaben)
  datei=  GeoJSON-Datei
  filter= Eigenschaft=Wert (mehrere Werte mit |, z. B. iso_a2=DE|PL|CZ)
  id=     Eigenschaft für Einzelstile und Koordinatennamen (Standard: name)

Jedes Objekt bekommt den Stil „geo <name>/<id>“ (vorher leer definiert, also
nach \\input einfach überschreiben) und einen Punkt „<name>-<id>“ im Innern
(für Beschriftungen). Linien (Flüsse, Straßen) werden nicht geschlossen,
Punkte (Städte) nur als Koordinate angelegt.
"""
import argparse
import json
import math
import re
import sys

try:
    import numpy as np
    import shapely
    from shapely.geometry import shape, box
    from shapely.validation import make_valid
except ImportError:
    sys.exit("Bitte zuerst installieren: pip install shapely pyproj")


def lies_ebene(spec):
    teile = {}
    for t in spec.split(";"):
        t = t.strip()
        if not t:
            continue
        k, _, v = t.partition("=")
        teile[k.strip()] = v.strip()
    for pflicht in ("name", "datei"):
        if pflicht not in teile:
            sys.exit(f"Ebene ohne '{pflicht}=': {spec}")
    if not re.fullmatch(r"[A-Za-z]+", teile["name"]):
        sys.exit(f"Ebenenname nur aus Buchstaben (wird zum LaTeX-Makro): {teile['name']}")
    return teile


def sicher(s):
    """macht aus einer Eigenschaft einen TikZ-tauglichen Namen"""
    s = str(s)
    for a, b in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("Ä", "Ae"), ("Ö", "Oe"), ("Ü", "Ue"), ("ß", "ss")):
        s = s.replace(a, b)
    return re.sub(r"[^A-Za-z0-9-]+", "", s.replace(" ", "-")) or "ohne-id"


def projektion(name, lon0, lat0):
    """liefert f(xy) → xy für ein (N,2)-Array aus Länge/Breite in Grad"""
    if name in ("plattkarte", "flach"):
        k = math.cos(math.radians(lat0))
        return lambda xy: np.column_stack([xy[:, 0] * k, xy[:, 1]])
    if name == "mercator":
        return lambda xy: np.column_stack([np.radians(xy[:, 0]),
                                           np.log(np.tan(np.pi / 4 + np.radians(xy[:, 1]) / 2))])
    try:
        from pyproj import Transformer
    except ImportError:
        sys.exit("Für EPSG-Projektionen: pip install pyproj")
    tr = Transformer.from_crs("EPSG:4326", name, always_xy=True)
    return lambda xy: np.column_stack(tr.transform(xy[:, 0], xy[:, 1]))


def koord(x, y, nachkomma):
    return f"({x:.{nachkomma}f},{y:.{nachkomma}f})"


def pfade(geom, nachkomma):
    """liefert Liste von (Pfadtext, geschlossen?)"""
    t = geom.geom_type
    if t == "Polygon":
        out = []
        for ring in [geom.exterior, *geom.interiors]:
            pts = list(ring.coords)[:-1]
            if len(pts) >= 3:
                out.append((" -- ".join(koord(x, y, nachkomma) for x, y in pts) + " -- cycle", True))
        return out
    if t == "LineString":
        pts = list(geom.coords)
        return [(" -- ".join(koord(x, y, nachkomma) for x, y in pts), False)] if len(pts) >= 2 else []
    if t.startswith("Multi") or t == "GeometryCollection":
        out = []
        for g in geom.geoms:
            out += pfade(g, nachkomma)
        return out
    return []


def main():
    p = argparse.ArgumentParser(description="GeoJSON → TikZ")
    p.add_argument("--ebene", action="append", required=True, help="siehe Kopf der Datei")
    p.add_argument("--bbox", required=True, help="Ausschnitt lon_min,lat_min,lon_max,lat_max (Grad)")
    p.add_argument("--breite", type=float, default=12, help="Kartenbreite in cm (Standard 12)")
    p.add_argument("--proj", default="plattkarte",
                   help="plattkarte | mercator | EPSG-Code, z. B. EPSG:3035 (Europa, flächentreu) oder EPSG:25833 (Ostdeutschland)")
    p.add_argument("--toleranz", type=float, default=0.02,
                   help="Vereinfachung in cm (Douglas-Peucker); 0 = aus. Standard 0.02")
    p.add_argument("--nachkomma", type=int, default=2, help="Nachkommastellen der Koordinaten")
    p.add_argument("-o", "--ausgabe", default="karte_daten.tex")
    a = p.parse_args()

    lon1, lat1, lon2, lat2 = map(float, a.bbox.split(","))
    rahmen = box(lon1, lat1, lon2, lat2)
    # Daten großzügig auswählen; der genaue Zuschnitt passiert nach der
    # Projektion am rechteckigen Kartenrand (sonst schräge Ränder)
    dlon, dlat = (lon2 - lon1) * 0.3, (lat2 - lat1) * 0.3
    auswahl = box(max(lon1 - dlon, -180), max(lat1 - dlat, -89.9),
                  min(lon2 + dlon, 180), min(lat2 + dlat, 89.9))
    proj = projektion(a.proj, (lon1 + lon2) / 2, (lat1 + lat2) / 2)

    # Maßstab aus dem projizierten Rahmen
    rp = shapely.transform(rahmen.segmentize(0.25), proj)
    minx, miny, maxx, maxy = rp.bounds
    s = a.breite / (maxx - minx)

    hoehe = (maxy - miny) * s
    karte = box(0, 0, a.breite, hoehe)

    def in_cm(xy):
        pxy = proj(xy)
        return np.column_stack([(pxy[:, 0] - minx) * s, (pxy[:, 1] - miny) * s])

    zeilen = ["% Erzeugt mit geo2tikz.py",
              f"% Ausschnitt {a.bbox}, Projektion {a.proj}, Breite {a.breite} cm,"
              f" Höhe {(maxy - miny) * s:.2f} cm",
              "% Quelle der Daten im Dokument angeben (siehe Datenlizenz).", "\\makeatletter"]
    statistik = []
    for spec in a.ebene:
        e = lies_ebene(spec)
        name, idfeld = e["name"], e.get("id", "name")
        filt = None
        if "filter" in e:
            fk, _, fv = e["filter"].partition("=")
            filt = (fk, set(fv.split("|")))
        with open(e["datei"], encoding="utf-8") as f:
            daten = json.load(f)
        stile = [f"geo {name}/.style={{}}"]
        befehle, punkte, ids_gesehen = [], [], {}
        anzahl = 0
        for feat in daten.get("features", []):
            props = feat.get("properties") or {}
            if filt and str(props.get(filt[0])) not in filt[1]:
                continue
            if not feat.get("geometry"):
                continue
            g = shape(feat["geometry"])
            if not g.is_valid:
                g = make_valid(g)
            g = g.intersection(auswahl)
            if g.is_empty:
                continue
            g = shapely.transform(g, in_cm)
            if not g.is_valid:  # Projektion kann Flächen verdrehen (z. B. Mercator)
                g = make_valid(g)
            g = g.intersection(karte)
            if g.is_empty:
                continue
            if a.toleranz > 0 and g.geom_type != "Point":
                g = g.simplify(a.toleranz, preserve_topology=True)
            wert = props.get(idfeld)
            fid = sicher(wert) if wert not in (None, "") else "ohne-id"
            ids_gesehen[fid] = ids_gesehen.get(fid, 0) + 1
            if ids_gesehen[fid] > 1:
                fid = f"{fid}-{ids_gesehen[fid]}"
            stile.append(f"geo {name}/{fid}/.style={{}}")
            if g.geom_type in ("Point", "MultiPoint"):
                pt = g if g.geom_type == "Point" else g.geoms[0]
                punkte.append(f"\\coordinate ({name}-{fid}) at {koord(pt.x, pt.y, a.nachkomma)};")
                anzahl += 1
                continue
            stuecke = pfade(g, a.nachkomma)
            if not stuecke:
                continue
            flaeche = any(geschl for _, geschl in stuecke)
            if flaeche:
                # alle Ringe eines Objekts in einen Pfad (even odd → Löcher bleiben frei)
                befehle.append(f"\\path[geo {name}, geo {name}/{fid}, even odd rule] "
                               + " ".join(t for t, _ in stuecke) + ";")
                rp_ = g.representative_point()
                punkte.append(f"\\coordinate ({name}-{fid}) at {koord(rp_.x, rp_.y, a.nachkomma)};")
            else:
                for t, _ in stuecke:
                    befehle.append(f"\\path[geo {name}, geo {name}/{fid}] {t};")
                mitte = g.interpolate(0.5, normalized=True)
                punkte.append(f"\\coordinate ({name}-{fid}) at {koord(mitte.x, mitte.y, a.nachkomma)};")
            anzahl += 1
        statistik.append(f"{name}: {anzahl} Objekte")
        zeilen.append(f"% ---- Ebene {name} ({e['datei']}) ----")
        zeilen.append("\\tikzset{" + ",\n  ".join(stile) + "}")
        zeilen.append(f"\\newcommand\\geo{name}{{%")
        zeilen += befehle + punkte
        zeilen.append("}")
    zeilen.append("\\makeatother")
    # Rahmen-Koordinaten für Clip/Legende
    zeilen.append(f"% Kartenrahmen: (0,0) bis ({a.breite:.2f},{(maxy - miny) * s:.2f})")
    with open(a.ausgabe, "w", encoding="utf-8") as f:
        f.write("\n".join(zeilen) + "\n")
    print(f"{a.ausgabe}: " + ", ".join(statistik)
          + f"; Karte {a.breite:.1f} × {(maxy - miny) * s:.1f} cm", file=sys.stderr)


if __name__ == "__main__":
    main()
