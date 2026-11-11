#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""
Prüft, ob alles im Repository mit den universalen Stildateien kompiliert:

  1. jeder LaTeX-Codeblock in einer SKILL.md, der ein vollständiges Beispiel ist
     (enthält tikzpicture, lstlisting, mcquestion, sudoku, chessboard …),
  2. jede Vorlage assets/*.tex und jede Handreichung references/*.tex.

Dokumente mit \\input{header.tex} bekommen die universalen Dateien aus
skills/grundlagen/latex-grundstil/assets/ daneben gelegt. Dateien mit eigenem
\\documentclass werden so kompiliert, wie sie sind.

  python3 werkzeuge/alles_kompilieren.py            # alles
  python3 werkzeuge/alles_kompilieren.py schach     # nur Skills mit „schach“ im Pfad
  python3 werkzeuge/alles_kompilieren.py --pdf ziel # PDFs nach ziel/ kopieren

Benötigt pdflatex (xelatex für *_unicode.tex). Ausgabe: eine Zeile pro Datei,
am Ende die Fehlerliste. Rückgabewert 1, wenn etwas fehlschlägt.
"""
import argparse
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
STIL = ROOT / "skills" / "grundlagen" / "latex-grundstil" / "assets"
BEISPIEL = re.compile(r"\\begin\{(tikzpicture|lstlisting|mcquestion[hv]|sudoku|ausgabe|music)\}|\\chessboard|\\lehrerblase|\\koordinatensystem")
# Dateien, die Eingabedaten brauchen, die erst ein Skript erzeugt
BRAUCHT = {"vorlage_sudoku_arbeitsblatt.tex": "sudokus.tex", "vorlage_karte.tex": "karte_daten.tex",
           "vorlage_bundeslaender_bilder.tex": "deutschland_daten.tex"}


def kompiliere(tex: pathlib.Path, arbeitsordner: pathlib.Path) -> tuple[bool, str]:
    quelle = tex.read_text(encoding="utf-8")
    # xelatex nur, wenn fontspec wirklich geladen wird (nicht, wenn es nur in einem Listing steht)
    ohne_listings = re.sub(r"\\begin\{lstlisting\}.*?\\end\{lstlisting\}", "", quelle, flags=re.S)
    prog = "xelatex" if re.search(r"^[^%\n]*\\usepackage(\[[^]]*\])?\{fontspec\}", ohne_listings, re.M) else "pdflatex"
    for lauf in range(3):
        if lauf == 2 and "Rerun to get" not in (arbeitsordner / tex.with_suffix(".log").name).read_text(errors="replace"):
            break  # dritter Lauf nur, wenn LaTeX ihn verlangt (Verzeichnis, longtable)
        r = subprocess.run([prog, "-interaction=nonstopmode", "-halt-on-error", tex.name],
                           cwd=arbeitsordner, capture_output=True, text=True, errors="replace")
        mx1 = arbeitsordner / tex.with_suffix(".mx1").name
        if mx1.exists():  # MusiXTeX: Zwischenlauf musixflx für die Abstände
            subprocess.run(["musixflx", tex.stem], cwd=arbeitsordner, capture_output=True)
    log = (arbeitsordner / tex.with_suffix(".log").name).read_text(errors="replace")
    fehler = [z for z in log.splitlines() if z.startswith("!")]
    return (r.returncode == 0 and not fehler), (fehler[0] if fehler else "")


def vorlagen_vorbauen(tex: pathlib.Path, arbeitsordner: pathlib.Path) -> None:
    """Bindet eine Handreichung PDFs ein (\\includegraphics{name.pdf} außerhalb von
    Listings), werden vorher alle Vorlagen im Arbeitsordner kompiliert."""
    quelle = re.sub(r"\\begin\{lstlisting\}.*?\\end\{lstlisting\}", "", tex.read_text(encoding="utf-8"), flags=re.S)
    gesucht = set(re.findall(r"\\includegraphics(?:\[[^]]*\])?\{([^}]+?)(?:\.pdf)?\}", quelle))
    for v in sorted(arbeitsordner.glob("*.tex")):
        if v.name == tex.name or v.stem not in gesucht:
            continue
        kompiliere(v, arbeitsordner)


def bloecke(skill_md: pathlib.Path):
    text = skill_md.read_text(encoding="utf-8")
    for nr, b in enumerate(re.findall(r"```latex\n(.*?)```", text, re.S), 1):
        if not BEISPIEL.search(b) or "…" in b or "..." in b:
            continue
        if re.search(r"\\(usepackage|documentclass|input\{|usetikzlibrary)", b):
            continue
        praeambel = "\n".join(z for z in b.splitlines() if z.lstrip().startswith(("\\lstdefinestyle", "\\setchessboard")))
        koerper = b
        yield nr, praeambel, koerper


def main():
    p = argparse.ArgumentParser()
    p.add_argument("filter", nargs="?", default="")
    p.add_argument("--pdf", help="Ordner, in den die erzeugten PDFs kopiert werden")
    a = p.parse_args()
    fehlschlaege, anzahl = [], 0
    for skill in sorted((ROOT / "skills").glob("*/*/SKILL.md")):
        sdir = skill.parent
        if a.filter not in str(sdir):
            continue
        # 1. Codeblöcke
        for nr, praeambel, koerper in bloecke(skill):
            with tempfile.TemporaryDirectory() as t:
                t = pathlib.Path(t)
                for f in ("header.tex", "newcommands.tex"):
                    shutil.copy(STIL / f, t)
                for f in sdir.glob("assets/*.tex"):
                    shutil.copy(f, t)
                extra = ""
                if "\\chessboard" in koerper or "mainline" in koerper:
                    extra += "\\usepackage{xskak}\\usepackage{chessboard}\n"
                if "\\begin{music}" in koerper:
                    extra += "\\usepackage{musixtex}\n"
                if "\\begin{sudoku}" in koerper:
                    extra += "\\usepackage{sudoku}\n"
                (t / "block.tex").write_text(
                    "\\input{header.tex}\n" + extra + "\\input{newcommands.tex}\n" +
                    ("\\input{musik-befehle.tex}\n" if (sdir / "assets" / "musik-befehle.tex").exists() else "") + praeambel +
                    "\n\\begin{document}\n" + koerper + "\n\\end{document}\n", encoding="utf-8")
                ok, msg = kompiliere(t / "block.tex", t)
            anzahl += 1
            name = f"{sdir.relative_to(ROOT)}/SKILL.md Block {nr}"
            print(("ok    " if ok else "FEHLER") + "  " + name + ("" if ok else "  " + msg))
            if not ok:
                fehlschlaege.append((name, msg))
        # 2. Vorlagen und Handreichungen
        for tex in sorted(list(sdir.glob("assets/*.tex")) + list(sdir.glob("references/*.tex"))):
            q = tex.read_text(encoding="utf-8")
            if tex.name in ("header.tex", "newcommands.tex"):
                continue
            ohne_kommentare = "\n".join(z.split("%", 1)[0] for z in q.splitlines())
            if "\\documentclass" not in ohne_kommentare and "\\input{header.tex}" not in ohne_kommentare:
                continue  # Schnipsel (z. B. ka_makros.tex), keine eigenständige Datei
            with tempfile.TemporaryDirectory() as t:
                t = pathlib.Path(t)
                # Handreichungen dürfen Datendateien aus assets/ desselben Skills laden
                ordner = [sdir / "assets", tex.parent] if tex.parent.name == "references" else [tex.parent]
                for o in ordner:
                    for f in o.iterdir() if o.is_dir() else []:
                        if f.is_file():
                            shutil.copy(f, t)
                if "\\input{header.tex}" in q:
                    for f in ("header.tex", "newcommands.tex"):
                        shutil.copy(STIL / f, t)
                if tex.name == "vorlage_sudoku_arbeitsblatt.tex":
                    subprocess.run([sys.executable, str(sdir / "scripts" / "sudoku_generator.py"), "-n", "4",
                                    "--seed", "1", "-o", str(t / "sudokus.tex")], capture_output=True)
                if tex.name in BRAUCHT and not (t / BRAUCHT[tex.name]).exists():
                    print(f"skip    {tex.relative_to(ROOT)} (braucht {BRAUCHT[tex.name]})")
                    continue
                if tex.parent.name == "references":
                    vorlagen_vorbauen(t / tex.name, t)
                ok, msg = kompiliere(t / tex.name, t)
                if ok and a.pdf:
                    ziel = pathlib.Path(a.pdf)
                    ziel.mkdir(parents=True, exist_ok=True)
                    shutil.copy(t / tex.with_suffix(".pdf").name, ziel / tex.with_suffix(".pdf").name)
            anzahl += 1
            print(("ok    " if ok else "FEHLER") + "  " + str(tex.relative_to(ROOT)) + ("" if ok else "  " + msg))
            if not ok:
                fehlschlaege.append((str(tex.relative_to(ROOT)), msg))
    print(f"\n{anzahl - len(fehlschlaege)} von {anzahl} kompiliert.")
    for n, m in fehlschlaege:
        print(f"  ✗ {n}: {m}")
    sys.exit(1 if fehlschlaege else 0)


if __name__ == "__main__":
    main()
