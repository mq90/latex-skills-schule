#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""
Wertet die Ankreuz- und Zuordnungsaufgaben ausgefüllter PDF-Formulare aus und
bereitet die Abgaben für die Korrektur am Bildschirm vor.

  python3 lk_auswerten.py Abgaben/ loesung.toml
  python3 lk_auswerten.py Abgaben/ loesung.toml --eintragen Korrektur/

Ohne Option: schreibt Abgaben/auswertung.csv (eine Zeile pro Abgabe, die
Punkte der automatisch prüfbaren Aufgaben und ihre Summe).

Mit --eintragen ORDNER entsteht zusätzlich zu jeder Abgabe eine
Korrekturfassung in ORDNER:
  - die Punkte der automatisch geprüften Aufgaben stehen in den roten
    Lehrerfeldern,
  - die Lehrerfelder (Namen mit dem Präfix aus der Lösungsdatei, Standard
    "L-") sind freigegeben, die Lehrkraft trägt dort die übrigen Punkte,
    die Summe und die Note ein,
  - die Antwortfelder der Schülerin oder des Schülers sind gesperrt.
Die Originalabgaben bleiben unverändert.

Die Lösungsdatei (TOML) liegt nur bei der Lehrkraft. Im PDF, das die Klasse
bekommt, steht davon nichts. Aufbau siehe assets/loesung_beispiel.toml.

Benötigt: Python ab 3.11, pip install pypdf
"""
import argparse
import csv
import pathlib
import sys
import tomllib

from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, NumberObject

NUR_LESEN = 1  # Bit 1 der Feldflags /Ff


def felder_lesen(pdf: pathlib.Path) -> dict[str, str]:
    """Feldname -> Antwort als Text; angekreuzte Kästchen als 'x'."""
    werte: dict[str, str] = {}
    for seite in PdfReader(pdf).pages:
        for anm in seite.get("/Annots") or []:
            o = anm.get_object()
            if o.get("/Subtype") != "/Widget" or "/T" not in o:
                continue
            name = str(o["/T"])
            wert = o.get("/V", "")
            if o.get("/FT") == "/Btn":
                wert = "x" if str(wert) not in ("", "/Off", "Off") else ""
            werte[name] = str(wert).strip()
    return werte


def gleich(antwort: str, erwartet: str) -> bool:
    """Vergleicht ohne Groß-/Kleinschreibung; mehrere richtige Antworten mit | trennen."""
    a = antwort.strip().strip(".!\"' ").casefold()
    return any(a == e.strip().casefold() for e in erwartet.split("|"))


def aufgabe_bewerten(aufgabe: dict, werte: dict[str, str]) -> float:
    je = float(aufgabe.get("je", 1))
    punkte = 0.0
    # Textfelder: [Feldname, erwartete Antwort]
    for feld, erwartet in aufgabe.get("text", []):
        if gleich(werte.get(feld, ""), erwartet):
            punkte += je
    # Kästchen: je Zeile alle Kästchen, das ERSTE ist das richtige.
    # Punkte gibt es nur, wenn genau dieses eine angekreuzt ist.
    for zeile in aufgabe.get("kreuz", []):
        an = [k for k in zeile if werte.get(k, "") == "x"]
        if an == [zeile[0]]:
            punkte += je
    # Einzelne Kästchen: [Feldname, True/False]. Ohne ein einziges Kreuz 0 Punkte,
    # sonst bekäme ein leeres Blatt Punkte für alle nicht anzukreuzenden Kästchen.
    einzeln = aufgabe.get("einzeln", [])
    if any(werte.get(feld, "") == "x" for feld, _ in einzeln):
        for feld, soll in einzeln:
            if (werte.get(feld, "") == "x") == bool(soll):
                punkte += je
    return punkte


def zahl(p: float) -> str:
    """2.0 -> '2', 1.5 -> '1,5'"""
    return f"{p:g}".replace(".", ",")


def korrekturfassung(quelle: pathlib.Path, ziel: pathlib.Path, eintraege: dict[str, str], praefix: str) -> None:
    schreiber = PdfWriter(clone_from=quelle)
    for seite in schreiber.pages:
        neu: dict[str, str] = {}
        for anm in seite.get("/Annots") or []:
            o = anm.get_object()
            if o.get("/Subtype") != "/Widget" or "/T" not in o:
                continue
            name = str(o["/T"])
            flags = int(o.get("/Ff", 0))
            if name.startswith(praefix):
                flags &= ~NUR_LESEN          # Lehrerfeld freigeben
                if name in eintraege:
                    neu[name] = eintraege[name]
            else:
                flags |= NUR_LESEN           # Schülerantwort sperren
            o[NameObject("/Ff")] = NumberObject(flags)
        if neu:
            schreiber.update_page_form_field_values(seite, neu, auto_regenerate=False)
    with open(ziel, "wb") as f:
        schreiber.write(f)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ordner", type=pathlib.Path, help="Ordner mit den abgegebenen PDF-Dateien")
    ap.add_argument("loesung", type=pathlib.Path, help="Lösungsdatei (TOML)")
    ap.add_argument("--eintragen", type=pathlib.Path, metavar="ORDNER",
                    help="Korrekturfassungen mit eingetragenen Punkten in diesen Ordner schreiben")
    a = ap.parse_args()

    with open(a.loesung, "rb") as f:
        loesung = tomllib.load(f)
    aufgaben = loesung.get("aufgabe", [])
    praefix = loesung.get("lehrer_praefix", "L-")
    if not aufgaben:
        sys.exit("Die Lösungsdatei enthält keine [[aufgabe]].")

    dateien = sorted(a.ordner.glob("*.pdf"))
    if not dateien:
        sys.exit(f"Keine PDF-Dateien in {a.ordner}")
    if a.eintragen:
        if a.eintragen.resolve() == a.ordner.resolve():
            sys.exit("--eintragen braucht einen anderen Ordner als die Abgaben.")
        a.eintragen.mkdir(parents=True, exist_ok=True)

    kopf = ["Datei", "Name"] + [f"Aufgabe {x['nr']} (max. {zahl(float(x['punkte']))})" for x in aufgaben] \
        + ["automatisch geprüft", "davon erreichbar"]
    erreichbar = sum(float(x["punkte"]) for x in aufgaben)
    zeilen = []
    for pdf in dateien:
        werte = felder_lesen(pdf)
        punkte = [aufgabe_bewerten(x, werte) for x in aufgaben]
        zeilen.append([pdf.name, werte.get("name", "")] + [zahl(p) for p in punkte]
                      + [zahl(sum(punkte)), zahl(erreichbar)])
        if a.eintragen:
            eintraege = {x["lehrerfeld"]: zahl(p) for x, p in zip(aufgaben, punkte) if "lehrerfeld" in x}
            korrekturfassung(pdf, a.eintragen / pdf.name, eintraege, praefix)

    ziel = a.ordner / "auswertung.csv"
    with open(ziel, "w", newline="", encoding="utf-8-sig") as f:   # utf-8-sig: Excel erkennt Umlaute
        w = csv.writer(f, delimiter=";")
        w.writerow(kopf)
        w.writerows(zeilen)
    print(f"{len(dateien)} Abgaben, {len(aufgaben)} Aufgaben automatisch geprüft -> {ziel}")
    if a.eintragen:
        print(f"Korrekturfassungen -> {a.eintragen}")
    gesamt = loesung.get("gesamt")
    if gesamt and erreichbar < float(gesamt):
        print(f"Noch von Hand zu bewerten: {zahl(float(gesamt) - erreichbar)} von {zahl(float(gesamt))} Punkten.")


if __name__ == "__main__":
    main()
