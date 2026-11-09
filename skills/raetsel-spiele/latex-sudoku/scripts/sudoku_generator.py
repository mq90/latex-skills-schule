#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""
sudoku_generator.py – erzeugt Sudokus mit genau einer Lösung und gibt sie
als LaTeX-Code für das Paket `sudoku` aus.

Beispiele
---------
  python3 sudoku_generator.py                       # 1 Sudoku, mittel
  python3 sudoku_generator.py -n 6 -s leicht        # 6 leichte Sudokus
  python3 sudoku_generator.py -n 4 -s schwer --seed 42 -o raetsel.tex
  python3 sudoku_generator.py --loesen "53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79"

Ausgabe: eine .tex-Datei mit den Befehlen \\SudokuAufgabeN und
\\SudokuLoesungN (N = A, B, C, ...), die man mit \\input einbindet und
an beliebiger Stelle aufruft. In der Lösung erscheinen die vorgegebenen
Ziffern fett, die ergänzten grau.

Schwierigkeit: wird über die Anzahl der vorgegebenen Ziffern gesteuert
(leicht ≈ 40, mittel ≈ 32, schwer ≈ 26). Jede Aufgabe wird nach dem
Ausdünnen geprüft: Es gibt immer genau eine Lösung.
"""
import argparse
import random
import string
import sys

ZIELE = {"leicht": 40, "mittel": 32, "schwer": 26}


def kandidaten(g, i):
    r, c = divmod(i, 9)
    br, bc = 3 * (r // 3), 3 * (c // 3)
    belegt = set(g[r * 9:(r + 1) * 9]) | {g[k * 9 + c] for k in range(9)}
    belegt |= {g[(br + a) * 9 + bc + b] for a in range(3) for b in range(3)}
    return [z for z in range(1, 10) if z not in belegt]


def zaehle_loesungen(g, grenze=2):
    """Zählt Lösungen per Backtracking (bricht bei `grenze` ab)."""
    g = list(g)
    anzahl = 0

    def suche():
        nonlocal anzahl
        # Feld mit den wenigsten Kandidaten zuerst (macht es schnell)
        best, best_k = -1, None
        for i in range(81):
            if g[i] == 0:
                k = kandidaten(g, i)
                if not k:
                    return
                if best_k is None or len(k) < len(best_k):
                    best, best_k = i, k
                    if len(k) == 1:
                        break
        if best == -1:
            anzahl += 1
            return
        for z in best_k:
            g[best] = z
            suche()
            if anzahl >= grenze:
                break
        g[best] = 0

    suche()
    return anzahl


def loese(g):
    g = list(g)

    def suche():
        try:
            i = g.index(0)
        except ValueError:
            return True
        for z in kandidaten(g, i):
            g[i] = z
            if suche():
                return True
        g[i] = 0
        return False

    return g if suche() else None


def volles_gitter(rng):
    g = [0] * 81

    def fuelle(i=0):
        if i == 81:
            return True
        k = kandidaten(g, i)
        rng.shuffle(k)
        for z in k:
            g[i] = z
            if fuelle(i + 1):
                return True
        g[i] = 0
        return False

    fuelle()
    return g


def erzeuge(stufe, rng, symmetrisch=True):
    loesung = volles_gitter(rng)
    aufgabe = list(loesung)
    ziel = ZIELE[stufe]
    felder = list(range(81))
    rng.shuffle(felder)
    for i in felder:
        if sum(1 for z in aufgabe if z) <= ziel:
            break
        paar = {i, 80 - i} if symmetrisch else {i}
        if any(aufgabe[j] == 0 for j in paar):
            continue
        alt = {j: aufgabe[j] for j in paar}
        for j in paar:
            aufgabe[j] = 0
        if zaehle_loesungen(aufgabe) != 1:
            for j, z in alt.items():
                aufgabe[j] = z
    return aufgabe, loesung


def tex_gitter(aufgabe, loesung=None):
    zeilen = []
    for r in range(9):
        zellen = []
        for c in range(9):
            i = r * 9 + c
            if loesung is None:
                zellen.append(str(aufgabe[i]) if aufgabe[i] else " ")
            elif aufgabe[i]:
                zellen.append(r"{\textbf{%d}}" % aufgabe[i])
            else:
                zellen.append(r"{\textcolor{black!45}{%d}}" % loesung[i])
        zeilen.append("|" + "|".join(zellen) + "|.")
    return "\n".join(zeilen)


def lies_zeichenkette(s):
    s = "".join(ch for ch in s if ch in "0123456789.")
    if len(s) != 81:
        sys.exit(f"Erwartet 81 Zeichen (Ziffern, 0 oder . für leer), bekommen: {len(s)}")
    return [0 if ch in "0." else int(ch) for ch in s]


def main():
    p = argparse.ArgumentParser(description="Sudokus für das LaTeX-Paket sudoku erzeugen")
    p.add_argument("-n", "--anzahl", type=int, default=1)
    p.add_argument("-s", "--stufe", choices=ZIELE, default="mittel")
    p.add_argument("--seed", type=int, help="Startwert für reproduzierbare Rätsel")
    p.add_argument("--unsymmetrisch", action="store_true",
                   help="Leerfelder nicht punktsymmetrisch verteilen")
    p.add_argument("--loesen", metavar="81ZEICHEN",
                   help="ein vorhandenes Sudoku prüfen und lösen statt neu zu erzeugen")
    p.add_argument("-o", "--ausgabe", default="-", help="Zieldatei (Standard: Bildschirm)")
    a = p.parse_args()

    rng = random.Random(a.seed)
    raetsel = []
    if a.loesen:
        aufg = lies_zeichenkette(a.loesen)
        n = zaehle_loesungen(aufg)
        if n == 0:
            sys.exit("Dieses Sudoku hat keine Lösung.")
        if n > 1:
            print("% Achtung: Dieses Sudoku hat mehr als eine Lösung!", file=sys.stderr)
        raetsel.append((aufg, loese(aufg)))
    else:
        for _ in range(a.anzahl):
            raetsel.append(erzeuge(a.stufe, rng, not a.unsymmetrisch))

    out = ["% Erzeugt mit sudoku_generator.py"
           + (f" (Stufe {a.stufe}, Seed {a.seed})" if not a.loesen else "")]
    for nr, (aufg, loes) in zip(string.ascii_uppercase, raetsel):
        vorgaben = sum(1 for z in aufg if z)
        out.append(f"% Sudoku {nr}: {vorgaben} Vorgaben")
        out.append(r"\newcommand\SudokuAufgabe%s{%%" % nr)
        out.append(r"\begin{sudoku}")
        out.append(tex_gitter(aufg))
        out.append(r"\end{sudoku}}")
        out.append(r"\newcommand\SudokuLoesung%s{%%" % nr)
        out.append(r"\begin{sudoku}")
        out.append(tex_gitter(aufg, loes))
        out.append(r"\end{sudoku}}")
        out.append("")
    text = "\n".join(out)
    if a.ausgabe == "-":
        print(text)
    else:
        with open(a.ausgabe, "w", encoding="utf-8") as f:
            f.write(text + "\n")
        print(f"{len(raetsel)} Sudoku(s) nach {a.ausgabe} geschrieben.", file=sys.stderr)


if __name__ == "__main__":
    main()
