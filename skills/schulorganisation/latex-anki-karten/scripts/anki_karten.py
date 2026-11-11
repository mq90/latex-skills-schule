#!/usr/bin/env python3
"""
anki_karten.py – Anki-Stapel (.apkg) aus einfachen Listen bauen.

VOKABELN / BEGRIFFE  (CSV, Trennzeichen ; oder , oder Tab)
    Spalten: Vorderseite;Rückseite[;Zusatz][;Tags]
    python3 anki_karten.py vokabeln englisch.csv --deck "Englisch::Unit 3" --rueckrichtung

MULTIPLE CHOICE  (Textdatei, siehe assets/fragen_blf_mathe.txt)
    ? Frage                     + richtige Antwort     - falsche Antwort
    > Erklärung (optional)      @ tags (optional)      Leerzeile = nächste Frage
    python3 anki_karten.py mc fragen.txt --deck "BLF Mathe" --mischen --pdf --qti

Formeln:  $x^2$  und  $$\\int f(x)\\,dx$$  (werden in Anki zu MathJax)
Bilder:   [bild:sachsen.png]  – Datei liegt im Ordner von --bilder
Erneuter Import derselben Datei aktualisiert die Karten statt sie doppelt
anzulegen (die Vorderseite ist der Schlüssel).

Benötigt:  pip install genanki
"""
import argparse, csv, html, random, re, sys, zipfile, hashlib
from pathlib import Path

try:
    import genanki
except ImportError:
    sys.exit("Bitte zuerst installieren:  pip install genanki")

# Feste IDs: so erkennt Anki die Notiztypen beim nächsten Import wieder.
ID_BASIS = 1607392319
ID_BASIS_REV = 1607392320
ID_MC = 1607392321

CSS = """
.card { font-family: "Segoe UI", Helvetica, Arial, sans-serif; font-size: 22px;
        text-align: center; color: #1f2937; background: #ffffff; }
.nightMode .card, .night_mode .card { color: #e5e7eb; background: #1f2937; }
.vorne  { font-size: 26px; font-weight: 600; }
.hinten { color: #2563EB; font-size: 24px; }
.zusatz { font-size: 17px; color: #6b7280; margin-top: 14px; font-style: italic; }
hr#answer { border: 0; border-top: 2px solid #2563EB; margin: 18px 0; }
img { display: block; margin: 12px auto; max-width: 95%; max-height: 60vh; }
.frage { font-size: 21px; text-align: left; margin-bottom: 12px; }
.mehrfach { font-size: 15px; color: #EA580C; text-align: left; }
ol.optionen { list-style-type: upper-alpha; text-align: left; font-size: 19px; }
ol.optionen li { margin: 6px 0; padding: 4px 8px; border-radius: 6px; }
li.richtig { background: #16A34A22; border-left: 4px solid #16A34A; font-weight: 600; }
li.falsch  { color: #9ca3af; }
.erklaerung { font-size: 16px; text-align: left; margin-top: 14px; padding: 8px 10px;
              border-left: 4px solid #2563EB; background: #2563EB11; }
"""


# ---------------------------------------------------------------------
def deck_id(name):
    return int(hashlib.sha1(name.encode()).hexdigest()[:8], 16) | (1 << 30)


def formeln(s):
    """$$…$$ → \\[…\\] und $…$ → \\(…\\) für MathJax in Anki."""
    s = re.sub(r"\$\$(.+?)\$\$", r"\\[\1\\]", s, flags=re.S)
    return re.sub(r"(?<!\\)\$(.+?)(?<!\\)\$", r"\\(\1\\)", s)


class Medien:
    def __init__(self, ordner):
        self.ordner = Path(ordner) if ordner else None
        self.dateien = []

    def __call__(self, s):
        def ersetze(m):
            name = m.group(1).strip()
            pfad = (self.ordner / name) if self.ordner else Path(name)
            if not pfad.exists():
                print(f"  WARNUNG: Bild {pfad} nicht gefunden")
            elif str(pfad) not in self.dateien:
                self.dateien.append(str(pfad))
            return f'<img src="{html.escape(pfad.name)}">'
        return re.sub(r"\[bild:([^\]]+)\]", ersetze, s)


def feld(s, medien):
    """Text sicher als HTML-Feld: Sonderzeichen maskieren, dann Formeln/Bilder."""
    s = html.escape(s.strip(), quote=False).replace("\n", "<br>")
    return medien(formeln(s))


# ---------------------------------------------------------------------
#  Vokabeln / Begriffe
# ---------------------------------------------------------------------
def modell_basis(rueck):
    vorlagen = [{
        "name": "Vorwärts",
        "qfmt": '<div class="vorne">{{Vorderseite}}</div>',
        "afmt": '<div class="vorne">{{Vorderseite}}</div><hr id="answer">'
                '<div class="hinten">{{Rückseite}}</div>'
                '{{#Zusatz}}<div class="zusatz">{{Zusatz}}</div>{{/Zusatz}}'}]
    if rueck:
        vorlagen.append({
            "name": "Rückwärts",
            "qfmt": '<div class="vorne">{{Rückseite}}</div>',
            "afmt": '<div class="vorne">{{Rückseite}}</div><hr id="answer">'
                    '<div class="hinten">{{Vorderseite}}</div>'
                    '{{#Zusatz}}<div class="zusatz">{{Zusatz}}</div>{{/Zusatz}}'})
    return genanki.Model(
        ID_BASIS_REV if rueck else ID_BASIS,
        "MKG Karteikarte (beide Richtungen)" if rueck else "MKG Karteikarte",
        fields=[{"name": "Vorderseite"}, {"name": "Rückseite"}, {"name": "Zusatz"}],
        templates=vorlagen, css=CSS)


def lies_csv(datei):
    with open(datei, encoding="utf-8-sig", newline="") as f:
        probe = f.read(4096)
        f.seek(0)
        dialekt = csv.Sniffer().sniff(probe, delimiters=";,\t")
        zeilen = [z for z in csv.reader(f, dialekt) if any(x.strip() for x in z)]
    kopf = [k.strip().lower() for k in zeilen[0]]
    if kopf and kopf[0] in ("vorderseite", "vorne", "frage", "wort", "deutsch", "englisch", "begriff"):
        zeilen = zeilen[1:]             # Kopfzeile überspringen
    return zeilen


def baue_vokabeln(a):
    medien = Medien(a.bilder)
    modell = modell_basis(a.rueckrichtung)
    deck = genanki.Deck(deck_id(a.deck), a.deck)
    zeilen = lies_csv(a.datei)
    if a.anzahl:
        random.Random(a.seed).shuffle(zeilen)
        zeilen = zeilen[:a.anzahl]
    for z in zeilen:
        z += [""] * (4 - len(z))
        vorne, hinten, zusatz, tags = z[:4]
        deck.add_note(genanki.Note(
            model=modell, fields=[feld(vorne, medien), feld(hinten, medien), feld(zusatz, medien)],
            tags=tags.split() + a.tags, guid=genanki.guid_for(a.deck, vorne.strip())))
    return deck, medien, len(zeilen)


# ---------------------------------------------------------------------
#  Multiple Choice
# ---------------------------------------------------------------------
def lies_mc(datei):
    fragen, akt = [], None
    for zeile in Path(datei).read_text(encoding="utf-8").splitlines() + [""]:
        z = zeile.rstrip()
        if z.startswith("%"):
            continue
        if not z.strip():
            if akt:
                fragen.append(akt)
            akt = None
            continue
        kz, rest = z[:1], z[1:].strip()
        if kz == "?":
            if akt:
                fragen.append(akt)
            akt = dict(frage=rest, optionen=[], erklaerung="", tags=[])
        elif akt is None:
            raise SystemExit(f"Zeile ohne Frage davor: {z}")
        elif kz in "+-":
            akt["optionen"].append((rest, kz == "+"))
        elif kz == ">":
            akt["erklaerung"] += (" " if akt["erklaerung"] else "") + rest
        elif kz == "@":
            akt["tags"] += rest.split()
        else:                            # Fortsetzung der Frage
            akt["frage"] += "\n" + z.strip()
    for f in fragen:
        if not any(r for _, r in f["optionen"]):
            raise SystemExit(f"Frage ohne richtige Antwort (+): {f['frage'][:60]}")
    return fragen


def modell_mc():
    return genanki.Model(
        ID_MC, "MKG Multiple Choice",
        fields=[{"name": "Frage"}, {"name": "Optionen"}, {"name": "Auswertung"},
                {"name": "Erklärung"}, {"name": "Mehrfach"}],
        templates=[{
            "name": "MC",
            "qfmt": '<div class="frage">{{Frage}}</div>'
                    '{{#Mehrfach}}<div class="mehrfach">Mehrere Antworten können richtig sein.</div>{{/Mehrfach}}'
                    '{{Optionen}}',
            "afmt": '<div class="frage">{{Frage}}</div><hr id="answer">{{Auswertung}}'
                    '{{#Erklärung}}<div class="erklaerung">{{Erklärung}}</div>{{/Erklärung}}'}],
        css=CSS)


def baue_mc(a, fragen):
    medien = Medien(a.bilder)
    modell = modell_mc()
    deck = genanki.Deck(deck_id(a.deck), a.deck)
    for f in fragen:
        opt = f["optionen"]
        liste = "".join(f"<li>{feld(t, medien)}</li>" for t, _ in opt)
        ausw = "".join(f'<li class="{"richtig" if r else "falsch"}">{feld(t, medien)}'
                       f'{" ✓" if r else ""}</li>' for t, r in opt)
        mehrfach = "ja" if sum(r for _, r in opt) > 1 else ""
        deck.add_note(genanki.Note(
            model=modell,
            fields=[feld(f["frage"], medien), f'<ol class="optionen">{liste}</ol>',
                    f'<ol class="optionen">{ausw}</ol>', feld(f["erklaerung"], medien), mehrfach],
            tags=f["tags"] + a.tags, guid=genanki.guid_for(a.deck, f["frage"])))
    return deck, medien


def mc_pdf(fragen, a, ziel):
    """Test als LaTeX (Aufgaben + Lösungsteil nach den gewohnten Konventionen)."""
    def t(s):
        s = s.replace("&", r"\&").replace("%", r"\%").replace("#", r"\#")
        return re.sub(r"\[bild:([^\]]+)\]",
                      lambda m: rf"\par\includegraphics[height=3.2cm]{{{Path(a.bilder or '.') / m.group(1).strip()}}}\par", s)
    buchst = "ABCDEFGH"
    L = [r"""\documentclass[11pt]{article}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage[ngerman]{babel}
\usepackage[a4paper,margin=2cm]{geometry}
\usepackage{amsmath,amssymb,graphicx,xcolor,enumitem,multicol}
\pagestyle{empty}
\setlength{\parindent}{0pt}
\setlist[enumerate,1]{label=(\arabic*), leftmargin=2.2em, itemsep=10pt}
\newcommand\kaestchen[1]{\makebox[1.4em][l]{$\square$}\textbf{#1}\enspace}
\begin{document}""",
         rf"{{\sffamily\bfseries\Large {t(a.titel or a.deck)}}}\par\smallskip",
         r"Name: \rule{7cm}{0.4pt}\hfill Datum: \rule{3cm}{0.4pt}\par\medskip",
         r"{\small Kreuze die richtige Antwort an. Bei Aufgaben mit \textbf{(M)} können mehrere Antworten richtig sein.}",
         r"\par\medskip\hrule\medskip", r"\begin{enumerate}"]
    for f in fragen:
        mehr = sum(r for _, r in f["optionen"]) > 1
        L.append(rf"\item {t(f['frage']).replace(chr(10), ' ')}{r' \textbf{(M)}' if mehr else ''}\par\nopagebreak")
        spalten = 2 if max(len(x) for x, _ in f["optionen"]) < 38 else 1
        if spalten == 2:
            L.append(r"\begin{multicols}{2}")
        for k, (x, _) in enumerate(f["optionen"]):
            L.append(rf"\kaestchen{{{buchst[k]}}}{t(x)}\par")
        if spalten == 2:
            L.append(r"\end{multicols}")
    L.append(r"\end{enumerate}")
    # Lösungsteil
    L += [r"\clearpage\scriptsize\raggedright",
          rf"{{\sffamily\bfseries\normalsize Lösungen: {t(a.titel or a.deck)}}}\par\smallskip\hrule\medskip",
          r"\begin{multicols}{2}\begin{enumerate}"]
    for f in fragen:
        richtig = ", ".join(buchst[k] for k, (_, r) in enumerate(f["optionen"]) if r)
        erkl = rf" -- {t(f['erklaerung'])}" if f["erklaerung"] else ""
        L.append(rf"\item $\boxed{{\text{{{richtig}}}}}${erkl}")
    L += [r"\end{enumerate}\end{multicols}", r"\end{document}"]
    ziel.write_text("\n".join(L), encoding="utf-8")


def mc_qti(fragen, a, ziel):
    """IMS QTI 2.1 – ein Item je Frage, alles in einer ZIP mit Manifest.
    Formeln bleiben als LaTeX-Text stehen; Bilder werden nicht übernommen."""
    def x(s):
        s = re.sub(r"\[bild:[^\]]+\]", "[Bild]", s)
        return html.escape(s, quote=True)
    items, res = [], []
    for i, f in enumerate(fragen, 1):
        ident = f"item{i:03d}"
        richtige = [f"c{k}" for k, (_, r) in enumerate(f["optionen"]) if r]
        mehr = len(richtige) > 1
        werte = "".join(f"<value>{c}</value>" for c in richtige)
        wahl = "".join(f'<simpleChoice identifier="c{k}">{x(t)}</simpleChoice>'
                       for k, (t, _) in enumerate(f["optionen"]))
        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<assessmentItem xmlns="http://www.imsglobal.org/xsd/imsqti_v2p1"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://www.imsglobal.org/xsd/imsqti_v2p1 http://www.imsglobal.org/xsd/qti/qtiv2p1/imsqti_v2p1.xsd"
  identifier="{ident}" title="Frage {i}" adaptive="false" timeDependent="false">
  <responseDeclaration identifier="RESPONSE" cardinality="{'multiple' if mehr else 'single'}" baseType="identifier">
    <correctResponse>{werte}</correctResponse>
  </responseDeclaration>
  <outcomeDeclaration identifier="SCORE" cardinality="single" baseType="float">
    <defaultValue><value>0</value></defaultValue>
  </outcomeDeclaration>
  <itemBody>
    <p>{x(f['frage'])}</p>
    <choiceInteraction responseIdentifier="RESPONSE" shuffle="{'true' if a.mischen else 'false'}" maxChoices="{0 if mehr else 1}">
      {wahl}
    </choiceInteraction>
  </itemBody>
  <responseProcessing template="http://www.imsglobal.org/question/qti_v2p1/rptemplates/match_correct"/>
</assessmentItem>
"""
        items.append((f"{ident}.xml", xml))
        res.append(f'<resource identifier="res_{ident}" type="imsqti_item_xmlv2p1" href="{ident}.xml">'
                   f'<file href="{ident}.xml"/></resource>')
    manifest = f"""<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns="http://www.imsglobal.org/xsd/imscp_v1p1" identifier="manifest_{deck_id(a.deck)}">
  <metadata><schema>QTIv2.1 Package</schema><schemaversion>1.0.0</schemaversion></metadata>
  <organizations/>
  <resources>
    {chr(10).join(res)}
  </resources>
</manifest>
"""
    with zipfile.ZipFile(ziel, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("imsmanifest.xml", manifest)
        for name, xml in items:
            z.writestr(name, xml)


# ---------------------------------------------------------------------
def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("art", choices=["vokabeln", "mc"])
    p.add_argument("datei")
    p.add_argument("--deck", required=True, help='Stapelname, Unterstapel mit ::, z. B. "Englisch::Unit 3"')
    p.add_argument("--ausgabe", help="Name der .apkg (Standard: wie Eingabedatei)")
    p.add_argument("--bilder", help="Ordner mit Bildern für [bild:...]")
    p.add_argument("--tags", nargs="*", default=[], help="Tags für alle Karten")
    p.add_argument("--rueckrichtung", action="store_true", help="zusätzlich Rückseite → Vorderseite abfragen")
    p.add_argument("--anzahl", type=int, help="nur so viele zufällige Einträge nehmen")
    p.add_argument("--seed", type=int, default=1)
    p.add_argument("--mischen", action="store_true", help="MC: Antwortreihenfolge einmalig mischen")
    p.add_argument("--pdf", action="store_true", help="MC: zusätzlich Test als .tex (mit Lösungen)")
    p.add_argument("--qti", action="store_true", help="MC: zusätzlich QTI-2.1-Paket (.zip) z. B. für ONYX")
    p.add_argument("--titel", help="MC: Überschrift für den PDF-Test")
    a = p.parse_args()

    ziel = Path(a.ausgabe) if a.ausgabe else Path(a.datei).with_suffix(".apkg")
    if a.art == "vokabeln":
        deck, medien, n = baue_vokabeln(a)
        info = f"{n} Notizen" + (" (× 2 Richtungen)" if a.rueckrichtung else "")
    else:
        fragen = lies_mc(a.datei)
        if a.anzahl:
            random.Random(a.seed).shuffle(fragen)
            fragen = fragen[:a.anzahl]
        if a.mischen:
            rng = random.Random(a.seed)
            for f in fragen:
                rng.shuffle(f["optionen"])
        deck, medien = baue_mc(a, fragen)
        info = f"{len(fragen)} Fragen"
        if a.pdf:
            mc_pdf(fragen, a, ziel.with_suffix(".tex"))
            print(f"  Test: {ziel.with_suffix('.tex')}  (mit pdflatex übersetzen)")
        if a.qti:
            mc_qti(fragen, a, ziel.with_name(ziel.stem + "_qti21.zip"))
            print(f"  QTI:  {ziel.with_name(ziel.stem + '_qti21.zip')}")
    paket = genanki.Package(deck)
    paket.media_files = medien.dateien
    paket.write_to_file(str(ziel))
    print(f"geschrieben: {ziel}  ({info}, {len(medien.dateien)} Bilder)")


if __name__ == "__main__":
    main()
