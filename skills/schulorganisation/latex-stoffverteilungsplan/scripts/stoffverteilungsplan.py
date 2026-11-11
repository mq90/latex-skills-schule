#!/usr/bin/env python3
"""
stoffverteilungsplan.py – verteilt Lernbereiche auf echte Unterrichtstermine
und schreibt einen LaTeX-Stoffverteilungsplan (Teil A allgemein, Teil B je
Klasse mit Datum, dazu eine Halbjahresübersicht).

    python3 stoffverteilungsplan.py plan_informatik10.toml
    pdflatex plan_informatik10.tex

Alle Eingaben stehen in der .toml-Datei (Ferien in einer eigenen Datei).
Benötigt nur Python ≥ 3.11 (tomllib ist eingebaut), keine Zusatzpakete.
"""
import sys, math, tomllib, datetime as dt
from pathlib import Path

TAGE = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]
MONATE = ["Jan", "Feb", "Mär", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep",
          "Okt", "Nov", "Dez"]


def tex(s):
    """Sonderzeichen für LaTeX entschärfen."""
    for a, b in [("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"),
                 ("#", r"\#"), ("_", r"\_"), ("$", r"\$"), ("{", r"\{"),
                 ("}", r"\}"), ("~", r"\textasciitilde{}"), ("^", r"\^{}")]:
        s = s.replace(a, b)
    return s


def tagesliste(von, bis):
    d = von
    while d <= bis:
        yield d
        d += dt.timedelta(days=1)


def kurz(d):            # Di 18.08.
    return f"{TAGE[d.weekday()]} {d:%d.%m.}"


def montag(d):
    return d - dt.timedelta(days=d.weekday())


class Plan:
    def __init__(self, datei):
        self.datei = Path(datei)
        cfg = tomllib.loads(self.datei.read_text(encoding="utf-8"))
        self.cfg = cfg
        p = cfg["plan"]
        self.p = p
        self.beginn, self.ende = p["beginn"], p["ende"]
        self.ustd_termin = p.get("ustd_pro_termin", 2)
        self.warnungen = []

        # ---- Ferien und Feiertage ------------------------------------
        self.frei = {}               # Datum -> Name
        self.ferienbloecke = []      # (von, bis, name)
        fdatei = self.datei.parent / p["ferien"]
        for f in tomllib.loads(fdatei.read_text(encoding="utf-8"))["frei"]:
            von, bis = f["von"], f.get("bis", f["von"])
            self.ferienbloecke.append((von, bis, f["name"]))
            for d in tagesliste(von, bis):
                self.frei[d] = f["name"]

        self.sperren = cfg.get("sperre", [])
        self._ab_wochen()
        self._einheiten()
        self.gruppen = [self._verteile(g) for g in cfg["gruppe"]]

    # ---- A/B-Wochen ---------------------------------------------------
    def _ist_schulwoche(self, mo):
        return any(mo + dt.timedelta(days=i) not in self.frei for i in range(5))

    def _ab_wochen(self):
        """Ordnet jedem Montag zwischen beginn und ende A oder B zu
        (None = Ferienwoche ohne Zählung)."""
        self.woche = {}
        start = self.p.get("woche_bei_beginn", "A")
        modus = self.p.get("ab_zaehlung", "schulwochen")
        mo, i = montag(self.beginn), 0
        while mo <= self.ende:
            if modus == "schulwochen" and not self._ist_schulwoche(mo):
                self.woche[mo] = None
            else:
                gerade = (i % 2 == 0)
                self.woche[mo] = start if gerade else ("B" if start == "A" else "A")
                i += 1
            mo += dt.timedelta(days=7)

    # ---- Lernbereiche in Einheiten (Termine) zerlegen -----------------
    def _einheiten(self):
        self.lbs = self.cfg["lernbereich"]
        self.pflicht = []            # Liste von (lb, thema, note)
        self.wahl = None
        for lb in self.lbs:
            themen = [t if isinstance(t, dict) else {"thema": t}
                      for t in lb.get("themen", [])]
            lb["_themen"] = themen
            if lb.get("wahl"):
                self.wahl = lb
                continue
            n = math.ceil(lb["ustd"] / self.ustd_termin)
            lb["_termine"] = n
            if len(themen) > n:
                self.warnungen.append(
                    f"{lb['kurz']}: {len(themen)} Themen, aber nur {n} Termine "
                    f"({lb['ustd']} Ustd.) – überzählige Themen gestrichen.")
            for k in range(n):
                if k < len(themen):
                    t = themen[k]
                    self.pflicht.append((lb, t["thema"], t.get("note", False)))
                else:
                    letztes = themen[-1]["thema"] if themen else lb["name"]
                    if len(letztes) > 28:
                        letztes = letztes[:26].rstrip() + "…"
                    self.pflicht.append((lb, f"Fortsetzung: {letztes}", False))

    # ---- Termine einer Gruppe -------------------------------------------
    def _sperre(self, d, gruppe):
        for s in self.sperren:
            if s["von"] <= d <= s.get("bis", s["von"]) and \
               ("nur" not in s or gruppe in s["nur"]):
                return s
        return None

    def _verteile(self, g):
        name = g["name"]
        zeilen = []                  # dicts: datum, art, ...
        for t in g["termine"]:
            wtag = TAGE.index(t["tag"])
            for d in tagesliste(self.beginn, self.ende):
                if d.weekday() != wtag:
                    continue
                ab = self.woche.get(montag(d))
                if t["woche"] != "AB" and ab != t["woche"]:
                    continue
                if d in self.frei:   # einzelne Feiertage auf dem Termin zeigen
                    if not any(v <= d <= b and v != b for v, b, _ in self.ferienbloecke):
                        zeilen.append(dict(datum=d, art="feiertag", ab=ab,
                                           text=self.frei[d], zeit=t.get("zeit", "")))
                    continue
                s = self._sperre(d, name)
                if s and s.get("modus", "ausfall") == "ausfall":
                    zeilen.append(dict(datum=d, art="ausfall", ab=ab,
                                       text=s["grund"], zeit=t.get("zeit", "")))
                elif s:
                    zeilen.append(dict(datum=d, art="puffer", ab=ab, grund=s["grund"],
                                       text=s.get("thema", "Übung / Wiederholung"),
                                       zeit=t.get("zeit", "")))
                else:
                    zeilen.append(dict(datum=d, art="stunde", ab=ab,
                                       zeit=t.get("zeit", ""), bem=t.get("bemerkung", "")))
        # Ferienblöcke als graue Zeilen einsortieren
        for v, b, n in self.ferienbloecke:
            if v != b and b >= self.beginn and v <= self.ende:
                zeilen.append(dict(datum=v, bis=b, art="ferien", text=n))
        zeilen.sort(key=lambda z: (z["datum"], z["art"] != "ferien"))

        # Stoff verteilen
        rest = list(self.pflicht)
        nr_ustd, wahlnr, noten = 0, 0, 0
        for z in zeilen:
            if z["art"] != "stunde":
                continue
            if rest:
                lb, thema, note = rest.pop(0)
            else:
                lb = self.wahl
                th = lb["_themen"] if lb else [{"thema": "Wahlbereich"}]
                t = th[wahlnr % len(th)] if th else {"thema": "Wahlbereich"}
                thema, note = t["thema"], t.get("note", False)
                wahlnr += 1
            z.update(lb=lb, thema=thema, note=note,
                     ustd=f"{nr_ustd + 1}/{nr_ustd + self.ustd_termin}"
                     if self.ustd_termin == 2 else str(nr_ustd + 1))
            nr_ustd += self.ustd_termin
            noten += note
        stunden = [z for z in zeilen if z["art"] == "stunde"]
        return dict(name=name, g=g, zeilen=zeilen, offen=rest, noten=noten,
                    termine=len(stunden),
                    puffer=sum(z["art"] == "puffer" for z in zeilen),
                    letzte=stunden[-1] if stunden else None)

    # =================================================================
    #  LaTeX schreiben
    # =================================================================
    def latex(self):
        p = self.p
        L = []
        a = L.append
        a(r"""\documentclass[11pt]{article}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage[ngerman]{babel}
\usepackage[a4paper,margin=2cm,bottom=2.2cm]{geometry}
\usepackage{microtype}
\usepackage[table]{xcolor}
\usepackage{booktabs,longtable,array,tabularx}
\usepackage{tikz}
\usepackage{amssymb}
\usepackage[hidelinks]{hyperref}
\definecolor{akzentblau}{HTML}{2563EB}
\definecolor{akzentrot}{HTML}{DC2626}
\definecolor{akzentgruen}{HTML}{16A34A}
\definecolor{akzentlila}{HTML}{7C3AED}
\definecolor{akzentorange}{HTML}{EA580C}
\setlength{\parindent}{0pt}
\setlength{\parskip}{4pt}
\renewcommand\arraystretch{1.25}
\newcommand\note{\textcolor{akzentrot}{\,$\blacktriangleright$\,\textsf{\footnotesize Note}}}
\newcommand\lbmarke[2]{\textcolor{#1}{\rule[-0.3ex]{0.9ex}{1.9ex}}\,\textsf{\footnotesize #2}}
\newcommand\abschnitt[1]{\par\medskip{\sffamily\bfseries\Large #1}\par\smallskip}
\newcommand\unterabschnitt[1]{\par\medskip{\sffamily\bfseries\large #1}\par}
\begin{document}
""")
        # ---- Kopf ----------------------------------------------------
        a(r"\begin{center}")
        a(rf"{{\sffamily\bfseries\LARGE {tex(p['titel'])}}}\\[4pt]")
        a(rf"{{\sffamily\large Schuljahr {tex(p['schuljahr'])}}}\\[4pt]")
        a(rf"{{\small {tex(p.get('lehrkraft', ''))} \textbullet\ {tex(p.get('schule', ''))}"
          rf" \textbullet\ geplant {self.beginn:%d.%m.%Y}--{self.ende:%d.%m.%Y}}}")
        a(r"\end{center}")
        for w in self.warnungen:
            a(rf"\fcolorbox{{akzentrot}}{{akzentrot!6}}{{\parbox{{\dimexpr\linewidth-2\fboxsep}}"
              rf"{{\small\textbf{{Achtung:}} {tex(w)}}}}}\par")

        # ---- Teil A --------------------------------------------------
        pfl = sum(lb["_termine"] for lb in self.lbs if not lb.get("wahl"))
        a(r"\abschnitt{Teil A: Aufteilung der Lernbereiche}")
        a(rf"Pflichtumfang: {sum(lb['ustd'] for lb in self.lbs if not lb.get('wahl'))} Ustd."
          rf" $=$ {pfl} Termine à {self.ustd_termin} Ustd. Weitere Termine gehören zum Wahlbereich.")
        a(r"\begin{longtable}{@{}>{\raggedright\arraybackslash}p{4.4cm}cp{1.3cm}p{9cm}@{}}")
        a(r"\toprule \textsf{Lernbereich} & \textsf{Ustd.} & \textsf{Termin} & \textsf{Stundenthema}\\ \midrule \endhead")
        k = 0
        for lb in self.lbs:
            if lb.get("wahl"):
                continue
            eint = [x for x in self.pflicht if x[0] is lb]
            for i, (_, thema, note) in enumerate(eint):
                k += 1
                links = (rf"\lbmarke{{{lb['farbe']}}}{{{tex(lb['kurz'])}}}\ "
                         rf"\small {tex(lb['name'])}" if i == 0 else "")
                us = str(lb["ustd"]) if i == 0 else ""
                a(rf"{links} & {us} & {k} & {tex(thema)}{r'\note' if note else ''}\\")
            a(r"\midrule")
        if self.wahl:
            a(rf"\lbmarke{{{self.wahl['farbe']}}}{{{tex(self.wahl['kurz'])}}}\ \small "
              rf"{tex(self.wahl['name'])} & -- & ab {k + 1} & "
              + tex(", ".join(t["thema"] for t in self.wahl["_themen"])) + r"\\")
        a(r"\bottomrule\end{longtable}")

        # ---- Übersicht -----------------------------------------------
        a(r"\abschnitt{Übersicht}")
        a(self.uebersicht())
        a(r"\par\smallskip{\footnotesize Grau: Ferien \quad schraffiert: Puffer "
          r"(kein neuer Stoff) \quad $\times$: Termin entfällt \quad"
          r" \textcolor{akzentrot}{$\blacktriangleright$}: sonstige Note}")
        a(r"\par\medskip")
        ueb_am = self.p.get("uebergabe_am")
        sp = r" & \textsf{bis Übergabe}" if ueb_am else ""
        a(r"\begin{tabular}{@{}lccc" + ("c" if ueb_am else "") + r"c@{}}\toprule \textsf{Klasse} & "
          r"\textsf{Termine mit Stoff} & \textsf{Puffer} & \textsf{Noten}" + sp +
          r" & \textsf{Pflicht nicht untergebracht}\\ \midrule")
        for gr in self.gruppen:
            bis = ""
            if ueb_am:
                n = sum(z["art"] == "stunde" and z["datum"] <= ueb_am for z in gr["zeilen"])
                bis = f" & {n} Termine"
            a(rf"{tex(gr['name'])} & {gr['termine']} & {gr['puffer']} & "
              rf"{gr['noten']}{bis} & {len(gr['offen'])}\\")
        a(r"\bottomrule\end{tabular}")

        # ---- Teil B --------------------------------------------------
        a(r"\clearpage\abschnitt{Teil B: Verteilung auf die Klassen}")
        for gr in self.gruppen:
            a(self.gruppentabelle(gr))
        a(r"\end{document}")
        return "\n".join(L)

    def gruppentabelle(self, gr):
        L = []
        a = L.append
        zeiten = ", ".join(f"{t['tag']} {t['zeit']} ({t['woche']}-Woche)"
                           if t["woche"] != "AB" else f"{t['tag']} {t['zeit']} (wöchentlich)"
                           for t in gr["g"]["termine"])
        a(rf"\unterabschnitt{{Klasse {tex(gr['name'])}}}{{\small {tex(zeiten)}}}")
        a(r"\begin{longtable}{@{}p{1.75cm}p{1.25cm}cp{1.1cm}p{9.9cm}@{}}")
        a(r"\toprule \textsf{Datum} & \textsf{Ustd.} & \textsf{Wo.} & \textsf{LB} & \textsf{Thema / Bemerkung}\\"
          r" \midrule \endhead \bottomrule \endfoot")
        ueb_am = self.p.get("uebergabe_am")
        ueb_gesetzt = False
        for z in gr["zeilen"]:
            if ueb_am and not ueb_gesetzt and z["datum"] > ueb_am:
                ueb_gesetzt = True
                a(self._uebergabezeile(gr))
            d = kurz(z["datum"])
            if z["art"] == "ferien":
                a(rf"\rowcolor{{black!8}}\multicolumn{{5}}{{@{{}}l}}{{\textit{{{tex(z['text'])}}}"
                  rf" \quad {z['datum']:%d.%m.}--{z['bis']:%d.%m.%Y}}}\\")
            elif z["art"] in ("ausfall", "feiertag"):
                a(rf"\textcolor{{black!45}}{{{d}}} & & {z['ab'] or ''} & & "
                  rf"\textcolor{{black!55}}{{$\times$ entfällt: {tex(z['text'])}}}\\")
            elif z["art"] == "puffer":
                a(rf"{d} & & {z['ab']} & & \textit{{{tex(z['text'])}}}"
                  rf" {{\footnotesize\color{{black!55}}({tex(z['grund'])})}}\\")
            else:
                lb = z["lb"]
                marke = rf"\lbmarke{{{lb['farbe']}}}{{{tex(lb['kurz'])}}}" if lb else ""
                bem = rf" {{\footnotesize\color{{black!55}}({tex(z['bem'])})}}" if z.get("bem") else ""
                a(rf"{d} & {z['ustd']} & {z['ab']} & {marke} & {tex(z['thema'])}"
                  rf"{r'\note' if z['note'] else ''}{bem}\\")
        a(r"\midrule")
        if gr["offen"]:
            offen = "; ".join(f"{lb['kurz']} {thema}" for lb, thema, _ in gr["offen"])
            stand = (rf"\textcolor{{akzentrot}}{{\textbf{{Bis Schuljahresende nicht untergebracht "
                     rf"({len(gr['offen'])} Termine):}}}} {tex(offen)}")
        else:
            stand = r"\textbf{Pflichtumfang vollständig untergebracht.}"
        a(rf"\multicolumn{{5}}{{@{{}}p{{\linewidth}}@{{}}}}{{\small {stand}}}\\")
        a(r"\end{longtable}")
        return "\n".join(L)

    def _uebergabezeile(self, gr):
        """Rote Linie mit Stand zum Übergabedatum."""
        ueb_am = self.p["uebergabe_am"]
        vorher = [z for z in gr["zeilen"] if z["art"] == "stunde" and z["datum"] <= ueb_am]
        if vorher:
            z = vorher[-1]
            stand = f"zuletzt {z['lb']['kurz'] if z['lb'] else ''} „{z['thema']}“ (Ustd. {z['ustd']})"
        else:
            stand = "noch kein Stoff"
        txt = tex(f"{self.p.get('uebergabe', 'Übergabe')} am {ueb_am:%d.%m.%Y}: {stand}")
        return (r"\arrayrulecolor{akzentrot}\specialrule{1.2pt}{2pt}{0pt}\arrayrulecolor{black}"
                rf"\multicolumn{{5}}{{@{{}}l}}{{\small\color{{akzentrot}}\textbf{{{txt}}}}}\\"
                r"\arrayrulecolor{akzentrot}\specialrule{1.2pt}{0pt}{2pt}\arrayrulecolor{black}")

    def uebersicht(self):
        """Wochenraster: Spalten = Wochen, Zeilen = Klassen."""
        wochen = sorted(self.woche)
        bw = min(0.62, 15.6 / len(wochen))      # Spaltenbreite in cm
        h = 0.55
        L = [r"\begin{tikzpicture}[font=\sffamily\scriptsize, x=1cm, y=1cm]"]
        a = L.append
        # Kopf: Monat, Datum Montag, A/B
        letzter_monat = None
        for i, mo in enumerate(wochen):
            x = i * bw
            if mo.month != letzter_monat:
                a(rf"\node[anchor=south west, font=\sffamily\footnotesize\bfseries] at ({x:.3f},0.75)"
                  rf" {{{MONATE[mo.month - 1]}}};")
                a(rf"\draw[black!40] ({x:.3f},0.75) -- ({x:.3f},{-h * len(self.gruppen):.3f});")
                letzter_monat = mo.month
            a(rf"\node[rotate=90, anchor=west, font=\sffamily\tiny, black!60] at ({x + bw / 2:.3f},0.05)"
              rf" {{{mo:%d.%m.}}};")
        # Ferien grau hinterlegen (ganze Spalten oder Teilspalten pro Tag)
        tagb = bw / 5
        for i, mo in enumerate(wochen):
            for t in range(5):
                if mo + dt.timedelta(days=t) in self.frei:
                    a(rf"\fill[black!12] ({i * bw + t * tagb:.3f},0) rectangle ++({tagb:.3f},{-h * len(self.gruppen):.3f});")
        # Zeilen
        for r, gr in enumerate(self.gruppen):
            y = -r * h
            a(rf"\node[anchor=east, font=\sffamily\footnotesize\bfseries] at (-0.1,{y - h / 2:.3f}) {{{tex(gr['name'])}}};")
            for z in gr["zeilen"]:
                if z["art"] == "ferien":
                    continue
                i = wochen.index(montag(z["datum"]))
                x0, x1 = i * bw + 0.04, (i + 1) * bw - 0.04
                box = rf"({x0:.3f},{y - 0.06:.3f}) rectangle ({x1:.3f},{y - h + 0.06:.3f})"
                if z["art"] == "stunde":
                    f = z["lb"]["farbe"] if z["lb"] else "black!30"
                    a(rf"\fill[{f}!70] {box};")
                    if z["note"]:
                        a(rf"\node[akzentrot, font=\tiny] at ({(x0 + x1) / 2:.3f},{y - h / 2:.3f}) {{$\blacktriangleright$}};")
                elif z["art"] == "puffer":
                    a(rf"\fill[pattern=north east lines, pattern color=black!45] {box};")
                    a(rf"\draw[black!45] {box};")
                else:
                    a(rf"\node[black!60] at ({(x0 + x1) / 2:.3f},{y - h / 2:.3f}) {{$\times$}};")
            a(rf"\draw[black!20] (0,{y - h:.3f}) -- ({len(wochen) * bw:.3f},{y - h:.3f});")
        ueb_am = self.p.get("uebergabe_am")
        if ueb_am:
            i = wochen.index(montag(ueb_am))
            xu = i * bw + (ueb_am.weekday() + 1) * tagb
            a(rf"\draw[akzentrot, line width=1.2pt] ({xu:.3f},0.7) -- ({xu:.3f},{-h * len(self.gruppen) - 0.05:.3f});")
            a(rf"\node[akzentrot, anchor=north west, font=\sffamily\tiny\bfseries, inner sep=1pt, fill=white] "
              rf"at ({xu:.3f},0.7) {{Übergabe}};")
        # Legende Lernbereiche (ein Textknoten, damit nichts überlappt)
        leg = r" \quad ".join(rf"\textcolor{{{lb['farbe']}!70}}{{\rule{{0.8em}}{{0.8em}}}}\,"
                              rf"{tex(lb['kurz'])}: {tex(lb['name'])}" for lb in self.lbs)
        a(rf"\node[anchor=north west, inner sep=0pt, text width={len(wochen) * bw:.2f}cm] "
          rf"at (0,{-h * len(self.gruppen) - 0.25:.2f}) {{{leg}}};")
        a(r"\end{tikzpicture}")
        return "\n".join(L)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    plan = Plan(sys.argv[1])
    ziel = Path(sys.argv[1]).with_suffix(".tex")
    code = plan.latex().replace(r"\usepackage{tikz}",
                                r"\usepackage{tikz}" "\n" r"\usetikzlibrary{patterns}")
    ziel.write_text(code, encoding="utf-8")
    print(f"geschrieben: {ziel}")
    for gr in plan.gruppen:
        print(f"  {gr['name']}: {gr['termine']} Termine mit Stoff, {gr['puffer']} Puffer, "
              f"{len(gr['offen'])} Pflicht-Termine offen")
    for w in plan.warnungen:
        print("  WARNUNG:", w)


if __name__ == "__main__":
    main()
