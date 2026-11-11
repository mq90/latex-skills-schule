#!/usr/bin/env python3
"""
sitzplan.py – Sitzplan aus Raumbeschreibung (.toml) und Namensliste (.csv).

    python3 sitzplan.py sitzplan_10b.toml
    pdflatex sitzplan_10b.tex

Die Namensliste bleibt auf dem eigenen Rechner – sie muss nie an eine KI.
Ohne CSV werden nummerierte Platzhalter (oder leere Plätze) gezeichnet.
Benötigt nur Python ≥ 3.11.
"""
import sys, csv, math, random, tomllib
from pathlib import Path

PLATZ_B, PLATZ_H = 2.5, 1.25      # Größe eines Platzes in cm
SEITE_B, SEITE_H = 2.4, 1.7       # Plätze an der Seitenwand (U-Form)


def tex(s):
    for a, b in [("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"),
                 ("#", r"\#"), ("_", r"\_"), ("$", r"\$")]:
        s = s.replace(a, b)
    return s


# ---------------------------------------------------------------------
#  Raum: Tische erzeugen
# ---------------------------------------------------------------------
def tische_aus_layout(lay):
    """Vorgefertigte Anordnungen. Koordinaten in cm, y=0 vorne (Tafel)."""
    typ = lay["typ"]
    gang = lay.get("gang", 1.3)
    T = []
    if typ == "reihen":
        n, k, p = lay["reihen"], lay["tische_pro_reihe"], lay.get("plaetze_pro_tisch", 2)
        abstand = lay.get("reihenabstand", 2.2)
        for r in range(n):
            for c in range(k):
                T.append(dict(x=c * (p * PLATZ_B + gang), y=2.5 + r * abstand, plaetze=p, reihen=1))
    elif typ == "gruppen":
        n, k = lay["gruppen_reihen"], lay["gruppen_pro_reihe"]
        p = lay.get("plaetze_pro_gruppe", 4)         # 4 oder 6
        breite = p // 2 * PLATZ_B
        for r in range(n):
            for c in range(k):
                T.append(dict(x=c * (breite + 2 * gang), y=2.5 + r * (2 * PLATZ_H + 2.2),
                              plaetze=p, reihen=2))
    elif typ == "u_form":
        links, hinten, rechts = lay["links"], lay["hinten"], lay["rechts"]  # Plätze je Seite
        tiefe = max(links, rechts) * SEITE_H
        breite = hinten * PLATZ_B + 2 * SEITE_B + 2 * 0.4
        for i in range(links):
            T.append(dict(x=0, y=2.5 + i * SEITE_H, plaetze=1, reihen=1, drehung=90))
        for i in range(rechts):
            T.append(dict(x=breite - SEITE_B, y=2.5 + i * SEITE_H, plaetze=1, reihen=1, drehung=-90))
        T.append(dict(x=SEITE_B + 0.4, y=2.5 + tiefe + 0.4, plaetze=hinten, reihen=1))
    else:
        raise SystemExit(f"Unbekanntes Layout: {typ}")
    return T


def plaetze_aus_tischen(tische):
    """Jeder Platz: Mittelpunkt (x,y), Tisch-Nr., Blickrichtung."""
    P = []
    for t_nr, t in enumerate(tische):
        p, r = t["plaetze"], t.get("reihen", 1)
        pro_reihe = math.ceil(p / r)
        dreh = t.get("drehung", 0)
        for i in range(p):
            reihe, spalte = divmod(i, pro_reihe)
            if dreh == 0:
                cx = t["x"] + (spalte + 0.5) * PLATZ_B
                cy = t["y"] + (reihe + 0.5) * PLATZ_H
                w, h = PLATZ_B, PLATZ_H
            else:                                    # Tisch hochkant an der Wand
                w, h = SEITE_B, SEITE_H
                cx = t["x"] + (reihe + 0.5) * w
                cy = t["y"] + (spalte + 0.5) * h
            P.append(dict(x=cx, y=cy, w=w, h=h, tisch=t_nr))
    # Platznummern: von vorne nach hinten, links nach rechts
    P.sort(key=lambda q: (round(q["y"], 1), q["x"]))
    for i, q in enumerate(P):
        q["nr"] = i + 1
    return P


def nachbarn(a, b):
    """Nachbarn = am selben Tisch direkt nebeneinander oder gegenüber."""
    if a["tisch"] != b["tisch"]:
        return False
    return math.hypot(a["x"] - b["x"], a["y"] - b["y"]) < 1.05 * max(a["w"], a["h"])


# ---------------------------------------------------------------------
#  Namen verteilen
# ---------------------------------------------------------------------
def lies_namen(datei):
    with open(datei, encoding="utf-8-sig", newline="") as f:
        probe = f.read(2048)
        f.seek(0)
        dialekt = csv.Sniffer().sniff(probe, delimiters=";,\t")
        zeilen = list(csv.DictReader(f, dialect=dialekt))
    out = []
    for z in zeilen:
        z = {k.strip().lower(): (v or "").strip() for k, v in z.items() if k}
        vor = z.get("vorname", "")
        nach = z.get("nachname", z.get("name", ""))
        if vor or nach:
            out.append(dict(vorname=vor, nachname=nach))
    return out


def schluessel(s):
    return s["vorname"] + (" " + s["nachname"] if s["nachname"] else "")


def passt(belegung, plaetze, regeln, vorne_nr):
    """Anzahl verletzter Regeln (0 = alles erfüllt)."""
    wo = {schluessel(s): p for p, s in zip(plaetze, belegung) if s}
    fehler = 0
    for a, b in regeln.get("nicht_neben", []):
        if a in wo and b in wo and nachbarn(wo[a], wo[b]):
            fehler += 1
    for a, b in regeln.get("neben", []):
        if a in wo and b in wo and not nachbarn(wo[a], wo[b]):
            fehler += 1
    for a in regeln.get("vorne", []):
        if a in wo and wo[a]["nr"] not in vorne_nr:
            fehler += 1
    for a in regeln.get("allein", []):
        if a in wo:
            for p, s in zip(plaetze, belegung):
                if s and p is not wo[a] and p["tisch"] == wo[a]["tisch"]:
                    fehler += 1
    return fehler


def verteile(schueler, plaetze, cfg):
    regeln = cfg.get("regeln", {})
    modus = cfg["namen"].get("verteilung", "liste")
    fest = {k: int(v) for k, v in regeln.get("fest", {}).items()}
    vorne_y = sorted({round(p["y"], 1) for p in plaetze})[:regeln.get("vorne_reihen", 1)]
    vorne_nr = {p["nr"] for p in plaetze if round(p["y"], 1) in vorne_y}
    n = len(plaetze)
    if len(schueler) > n:
        raise SystemExit(f"{len(schueler)} Namen, aber nur {n} Plätze.")
    # Plätze, die "allein"-Schülern zustehen, werden für den Tisch freigehalten
    rng = random.Random(cfg["namen"].get("seed"))
    beste, best_f = None, 10 ** 9
    versuche = 1 if modus == "liste" else 20000
    for _ in range(versuche):
        frei = [p for p in plaetze if p["nr"] not in fest.values()]
        rest = [s for s in schueler if schluessel(s) not in fest]
        if modus != "liste":
            rng.shuffle(rest)
            rng.shuffle(frei)
        bel = {p["nr"]: None for p in plaetze}
        for s in schueler:
            if schluessel(s) in fest:
                bel[fest[schluessel(s)]] = s
        # "allein": ganzer Tisch bleibt sonst leer
        allein = set(regeln.get("allein", []))
        gesperrt = set()
        for s in list(rest):
            if schluessel(s) in allein:
                p = next(q for q in frei if q["nr"] not in gesperrt)
                bel[p["nr"]] = s
                rest.remove(s)
                gesperrt |= {q["nr"] for q in plaetze if q["tisch"] == p["tisch"]}
        frei = [p for p in (frei if modus != "liste" else sorted(frei, key=lambda q: q["nr"]))
                if p["nr"] not in gesperrt and bel[p["nr"]] is None]
        if len(rest) > len(frei):
            raise SystemExit(f"Zu wenige Plätze: {len(rest)} Namen für {len(frei)} freie Plätze "
                             f"(die Regel 'allein' blockiert {len(gesperrt) - len(allein)} Plätze).")
        for p, s in zip(frei, rest):
            bel[p["nr"]] = s
        belegung = [bel[p["nr"]] for p in plaetze]
        f = passt(belegung, plaetze, regeln, vorne_nr)
        if f < best_f:
            beste, best_f = belegung, f
        if f == 0:
            break
    return beste, best_f


# ---------------------------------------------------------------------
#  LaTeX
# ---------------------------------------------------------------------
def latex(cfg, plaetze, belegung, tische, fehler):
    r = cfg["raum"]
    platzhalter = cfg["namen"].get("platzhalter", "nummern")
    xs = [p["x"] for p in plaetze]
    ys = [p["y"] for p in plaetze]
    xmin = min(x - p["w"] / 2 for x, p in zip(xs, plaetze)) - 1.0
    xmax = max(x + p["w"] / 2 for x, p in zip(xs, plaetze)) + 1.0
    ymax = max(y + p["h"] / 2 for y, p in zip(ys, plaetze)) + 0.8
    ymin = -0.2
    breite, hoehe = xmax - xmin, ymax - ymin
    skala = min(1.3, 25.0 / breite, 15.0 / hoehe)

    L = [r"""\documentclass[11pt]{article}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage[ngerman]{babel}
\usepackage[a4paper,landscape,margin=1.3cm]{geometry}
\usepackage{xcolor}
\usepackage{tikz}
\pagestyle{empty}
\definecolor{akzentblau}{HTML}{2563EB}
\definecolor{akzentrot}{HTML}{DC2626}
\definecolor{akzentorange}{HTML}{EA580C}
\setlength{\parindent}{0pt}
\begin{document}"""]
    a = L.append
    for ansicht in r.get("ansichten", ["lehrer"]):
        lehrer = ansicht == "lehrer"
        # Lehrersicht: Tafel unten, Raum um 180° gedreht
        def T(x, y):
            return (xmax + xmin - x, y) if lehrer else (x, ymax + ymin - y)

        a(r"\begin{center}")
        a(rf"{{\sffamily\bfseries\LARGE Sitzplan {tex(cfg['titel'])}}}\hfill"
          rf"{{\sffamily\large {tex(r.get('name', ''))} \quad Stand: {tex(cfg.get('stand', ''))}}}\par")
        a(rf"{{\sffamily\small\color{{black!55}} {'Ansicht vom Lehrertisch' if lehrer else 'Ansicht aus der Klasse (Tafel vorn)'}}}")
        a(r"\par\vfill")
        a(rf"\begin{{tikzpicture}}[scale={skala:.3f}, every node/.style={{transform shape}}]")
        # Raumumriss
        x0, y0 = T(xmin, ymin)
        x1, y1 = T(xmax, ymax)
        a(rf"\draw[black!35, line width=1pt, rounded corners=2pt] ({x0:.2f},{y0:.2f}) rectangle ({x1:.2f},{y1:.2f});")
        # Tafel, Pult, Tür, Fenster
        mitte = (xmin + xmax) / 2
        tb = r.get("tafelbreite", 8)
        tx0, ty = T(mitte - tb / 2, ymin)
        tx1, _ = T(mitte + tb / 2, ymin)
        a(rf"\fill[black!70] ({min(tx0, tx1):.2f},{ty - 0.12:.2f}) rectangle ({max(tx0, tx1):.2f},{ty + 0.12:.2f});")
        lab_y = ty - 0.45 if lehrer else ty + 0.45
        a(rf"\node[font=\sffamily\small] at ({(tx0 + tx1) / 2:.2f},{lab_y:.2f}) {{Tafel}};")
        px = r.get("pult", "rechts")
        if px:
            pxk = xmax - 3.2 if px == "rechts" else xmin + 0.6
            qx0, qy0 = T(pxk, 0.5)
            qx1, qy1 = T(pxk + 2.6, 1.6)
            a(rf"\filldraw[fill=akzentorange!15, draw=akzentorange] ({qx0:.2f},{qy0:.2f}) rectangle ({qx1:.2f},{qy1:.2f})"
              rf" node[midway, font=\sffamily\footnotesize] {{Lehrertisch}};")
        for seite, wort in ((r.get("fenster"), "Fenster"), (r.get("tuer"), "Tür")):
            if not seite:
                continue
            wx = xmin if seite == "links" else xmax
            ax, ay0 = T(wx, ymin + 1)
            _, ay1 = T(wx, ymax - 1)
            farbe = "akzentblau" if wort == "Fenster" else "akzentrot"
            if wort == "Fenster":
                a(rf"\draw[{farbe}, line width=2.5pt] ({ax:.2f},{ay0:.2f}) -- ({ax:.2f},{ay1:.2f});")
            else:
                a(rf"\draw[{farbe}, line width=2.5pt] ({ax:.2f},{ay0:.2f}) -- ++(0,{1.5 if ay0 < ay1 else -1.5});")
            innen = -0.25 if ax > (x0 + x1) / 2 else 0.25
            ly = (ay0 + ay1) / 2 if wort == "Fenster" else ay0 + (0.75 if ay0 < ay1 else -0.75)
            a(rf"\node[{farbe}, font=\sffamily\footnotesize, anchor={'east' if innen < 0 else 'west'}, "
              rf"rotate={90 if wort == 'Fenster' and innen < 0 else (-90 if wort == 'Fenster' else 0)}, "
              rf"{'anchor=south' if wort == 'Fenster' else ''}] at ({ax + innen:.2f},{ly:.2f}) {{{wort}}};")
        # Tische (Umriss) und Plätze
        for t_nr in sorted({p["tisch"] for p in plaetze}):
            ps = [p for p in plaetze if p["tisch"] == t_nr]
            bx0 = min(p["x"] - p["w"] / 2 for p in ps); bx1 = max(p["x"] + p["w"] / 2 for p in ps)
            by0 = min(p["y"] - p["h"] / 2 for p in ps); by1 = max(p["y"] + p["h"] / 2 for p in ps)
            (u0, v0), (u1, v1) = T(bx0, by0), T(bx1, by1)
            a(rf"\fill[black!6, rounded corners=3pt] ({u0:.2f},{v0:.2f}) rectangle ({u1:.2f},{v1:.2f});")
        for p, s in zip(plaetze, belegung):
            cx, cy = T(p["x"], p["y"])
            w, h = p["w"] - 0.12, p["h"] - 0.12
            a(rf"\draw[black!45, fill=white, rounded corners=2pt] ({cx - w / 2:.2f},{cy - h / 2:.2f}) "
              rf"rectangle ({cx + w / 2:.2f},{cy + h / 2:.2f});")
            a(rf"\node[font=\sffamily\tiny, black!40, anchor=north west, inner sep=1.5pt] at "
              rf"({cx - w / 2:.2f},{cy + h / 2:.2f}) {{{p['nr']}}};")
            if s:
                txt = rf"\textbf{{{tex(s['vorname'])}}}" + (rf"\\[-1pt]{{\scriptsize {tex(s['nachname'])}}}" if s["nachname"] else "")
            else:
                txt = ""
            if txt:
                a(rf"\node[font=\sffamily\footnotesize, align=center, text width={w - 0.1:.2f}cm, "
                  rf"inner sep=0pt] at ({cx:.2f},{cy - 0.05:.2f}) {{{txt}}};")
        a(r"\end{tikzpicture}")
        a(r"\par\vfill")
        if fehler:
            a(rf"{{\color{{akzentrot}}\small Achtung: {fehler} Regel(n) ließen sich nicht erfüllen.}}\par")
        a(r"\end{center}\clearpage")
    a(r"\end{document}")
    return "\n".join(L)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    datei = Path(sys.argv[1])
    cfg = tomllib.loads(datei.read_text(encoding="utf-8"))
    tische = []
    if "layout" in cfg:
        tische += tische_aus_layout(cfg["layout"])
    tische += cfg.get("tisch", [])
    plaetze = plaetze_aus_tischen(tische)

    nm = cfg.setdefault("namen", {})
    if nm.get("csv") and (datei.parent / nm["csv"]).exists():
        schueler = lies_namen(datei.parent / nm["csv"])
    else:
        if nm.get("csv"):
            print(f"Hinweis: {nm['csv']} nicht gefunden – zeichne Platzhalter.")
        schueler = []
    belegung, fehler = verteile(schueler, plaetze, cfg) if schueler else ([None] * len(plaetze), 0)
    ziel = datei.with_suffix(".tex")
    ziel.write_text(latex(cfg, plaetze, belegung, tische, fehler), encoding="utf-8")
    print(f"geschrieben: {ziel}  ({len(schueler)} Namen, {len(plaetze)} Plätze, "
          f"{fehler} Regelverstöße)")


if __name__ == "__main__":
    main()
