#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""
Liest die Formularfelder aller ausgefüllten PDFs in einem Ordner aus und
schreibt sie in eine Tabelle (CSV, öffnet sich in Excel, Numbers, LibreOffice).

  python3 antworten_einsammeln.py ordner_mit_abgaben/
  python3 antworten_einsammeln.py ordner_mit_abgaben/ --aufgaben

Ohne Option: eine Zeile pro Abgabe, eine Spalte pro Feld (antworten.csv).
Mit --aufgaben zusätzlich antworten_aufgabenweise.txt: alle Antworten zu
einer Aufgabe untereinander, damit man Aufgabe für Aufgabe korrigieren kann.
Angekreuzte Kästchen erscheinen als „x“, leere Felder bleiben leer.

Benötigt: pip install pypdf
"""
import argparse
import csv
import pathlib
import sys

from pypdf import PdfReader


def felder_lesen(pdf: pathlib.Path) -> dict[str, str]:
    """Feldname -> Antwort als Text, in der Reihenfolge der Felder im Dokument."""
    werte: dict[str, str] = {}
    for seite in PdfReader(pdf).pages:
        for anm in seite.get("/Annots") or []:
            o = anm.get_object()
            if o.get("/Subtype") != "/Widget" or "/T" not in o:
                continue
            name = str(o["/T"])
            if name.startswith("pbs@"):          # unsichtbarer Hilfsknopf von animate
                continue
            wert = o.get("/V", "")
            if o.get("/FT") == "/Btn":           # Kästchen oder Optionsfeld
                an = str(wert) not in ("", "/Off", "Off")
                if name in werte and not an:     # Optionsfelder: mehrere Widgets, ein Name
                    continue
                wert = str(wert).lstrip("/") if an and o.get("/Ff", 0) & 32768 else ("x" if an else "")
            werte[name] = str(wert).replace("\r\n", "\n").replace("\r", "\n")
    return werte


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ordner", type=pathlib.Path)
    ap.add_argument("--aufgaben", action="store_true", help="zusätzlich aufgabenweise Übersicht")
    a = ap.parse_args()

    dateien = sorted(p for p in a.ordner.glob("*.pdf"))
    if not dateien:
        sys.exit(f"Keine PDF-Dateien in {a.ordner}")
    alle = {p.name: felder_lesen(p) for p in dateien}
    spalten: list[str] = []
    for werte in alle.values():
        spalten += [k for k in werte if k not in spalten]

    ziel = a.ordner / "antworten.csv"
    with open(ziel, "w", newline="", encoding="utf-8-sig") as f:   # utf-8-sig: Excel erkennt Umlaute
        w = csv.writer(f, delimiter=";")
        w.writerow(["Datei"] + spalten)
        for datei, werte in alle.items():
            w.writerow([datei] + [werte.get(s, "") for s in spalten])
    print(f"{len(dateien)} Abgaben, {len(spalten)} Felder -> {ziel}")

    if a.aufgaben:
        ziel2 = a.ordner / "antworten_aufgabenweise.txt"
        with open(ziel2, "w", encoding="utf-8") as f:
            for s in spalten:
                f.write(f"===== {s} =====\n")
                for datei, werte in alle.items():
                    text = werte.get(s, "").replace("\n", "\n" + " " * 4)
                    f.write(f"{datei}:\n    {text}\n")
                f.write("\n")
        print(f"aufgabenweise -> {ziel2}")


if __name__ == "__main__":
    main()
