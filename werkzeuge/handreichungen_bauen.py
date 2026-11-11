#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""
Baut alle Handreichungen und Nachschlagewerke (skills/*/*/references/*.tex mit
\\title) als PDF und legt sie nach Bereichen sortiert in handreichungen/ ab.
Der Dateiname wird aus dem \\title erzeugt, z. B.
handreichungen/informatik/Automaten-mit-TikZ-erstellen.pdf.

  python3 werkzeuge/handreichungen_bauen.py

Nach jeder Änderung an einer Handreichung oder an header.tex/newcommands.tex
ausführen, damit die PDFs im Repository zum Quelltext passen. Alte PDFs in
handreichungen/ werden vorher entfernt; README.md bleibt erhalten.
"""
import pathlib
import re
import shutil
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from alles_kompilieren import ROOT, STIL, kompiliere, vorlagen_vorbauen  # noqa: E402

ZIEL = ROOT / "handreichungen"

ERSETZE = [
    (r"\\hologo\{LaTeX\}", "LaTeX"),
    (r"Ti\\textit\{k\}Z", "TikZ"),
    (r"\\TikZ\b\s*", "TikZ "),
    (r"MusiX\\TeX\{\}", "MusiXTeX"),
    (r"\\texttt\{([^}]*)\}", r"\1"),
]


def titel(tex: pathlib.Path) -> str | None:
    m = re.search(r"\\title\{(.*)\}\s*$", tex.read_text(encoding="utf-8"), re.M)
    if not m:
        return None
    t = m.group(1)
    for muster, ersatz in ERSETZE:
        t = re.sub(muster, ersatz, t)
    return re.sub(r"\s+", " ", t).strip()


def dateiname(t: str) -> str:
    t = re.sub(r"[:,]", "", t)
    return re.sub(r"\s+", "-", t) + ".pdf"


def main():
    for alt in ZIEL.glob("*/*.pdf"):
        alt.unlink()
    fehler, liste = [], []
    for tex in sorted((ROOT / "skills").glob("*/*/references/*.tex")):
        t = titel(tex)
        if t is None:
            continue  # Beispiel-Dokument ohne Titel, keine Handreichung
        bereich = tex.relative_to(ROOT / "skills").parts[0]
        with tempfile.TemporaryDirectory() as d:
            d = pathlib.Path(d)
            # Datendateien aus assets/ desselben Skills (z. B. Karten) stehen auch zur Verfügung
            for o in (tex.parent.parent / "assets", tex.parent):
                for f in o.iterdir() if o.is_dir() else []:
                    if f.is_file():
                        shutil.copy(f, d)
            for f in ("header.tex", "newcommands.tex"):
                shutil.copy(STIL / f, d)
            vorlagen_vorbauen(d / tex.name, d)
            ok, msg = kompiliere(d / tex.name, d)
            if ok:
                ziel = ZIEL / bereich / dateiname(t)
                ziel.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(d / tex.with_suffix(".pdf").name, ziel)
                liste.append((bereich, t, ziel.relative_to(ROOT)))
        print(("ok    " if ok else "FEHLER") + "  " + str(tex.relative_to(ROOT)) + ("" if ok else "  " + msg))
        if not ok:
            fehler.append(tex)
    print(f"\n{len(liste)} PDFs in {ZIEL.relative_to(ROOT)}/")
    sys.exit(1 if fehler else 0)


if __name__ == "__main__":
    main()
