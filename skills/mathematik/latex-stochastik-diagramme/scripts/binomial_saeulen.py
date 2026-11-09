#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""
binomial_saeulen.py – erzeugt TikZ-Code für ein Säulendiagramm (Histogramm)
einer Binomialverteilung B(n; p) im Arbeitsblatt-Stil (reines TikZ, kein pgfplots).

Die Wahrscheinlichkeiten werden hier exakt berechnet und als feste Zahlen in den
TikZ-Code geschrieben – pgfmath kann Fakultäten nur bis etwa 7! sicher.

  python3 binomial_saeulen.py 10 0.3                  # B(10; 0,3)
  python3 binomial_saeulen.py 20 0.5 --markiere 0-8   # Säulen 0 bis 8 hervorheben
  python3 binomial_saeulen.py 10 0.3 --hoehe 6 --breite 11 --tabelle

Ausgabe: eine tikzpicture auf dem Bildschirm (zum Einfügen in das Dokument).
"""
import argparse
from math import comb


def main():
    ap = argparse.ArgumentParser(description="Säulendiagramm einer Binomialverteilung als TikZ-Code")
    ap.add_argument("n", type=int)
    ap.add_argument("p", type=float)
    ap.add_argument("--markiere", help="Bereich hervorheben, z. B. 0-3 oder 5-10")
    ap.add_argument("--hoehe", type=float, default=5.0, help="Höhe der y-Achse in cm (Standard 5)")
    ap.add_argument("--breite", type=float, default=11.0, help="Breite der x-Achse in cm (Standard 11)")
    ap.add_argument("--tabelle", action="store_true", help="zusätzlich die Wertetabelle als Kommentar")
    a = ap.parse_args()

    n, p = a.n, a.p
    werte = [comb(n, k) * p**k * (1 - p)**(n - k) for k in range(n + 1)]
    pmax = max(werte)
    # y-Achse: schöne Obergrenze in Schritten von 0,05 bzw. 0,1
    schritt = 0.05 if pmax <= 0.3 else 0.1
    ymax = schritt * (int(pmax / schritt) + 1)
    sy = a.hoehe / ymax                     # cm pro Wahrscheinlichkeitseinheit
    sx = a.breite / (n + 1)                 # cm pro k
    lo, hi = (map(int, a.markiere.split("-")) if a.markiere else (-1, -1))
    ptxt = f"{p:g}".replace(".", "{,}")

    z = [f"% Binomialverteilung B({n}; {ptxt}) – erzeugt mit binomial_saeulen.py"]
    if a.tabelle:
        z += [f"%   k = {k:2d}:  P(X = k) = {w:.4f}" for k, w in enumerate(werte)]
    z += [f"\\begin{{tikzpicture}}[x={sx:.3f}cm, y={sy:.3f}cm]",
          "\t% waagerechte Hilfslinien",
          "\t\\foreach \\y in {" + ",".join(f"{schritt * i:.2f}" for i in range(1, round(ymax / schritt) + 1)) + "}",
          f"\t\t\\draw[gray!30, thin] (-0.5,\\y) -- ({n}.5,\\y);",
          "\t% Säulen: k/P(X=k)" + (f", hervorgehoben {lo} bis {hi}" if a.markiere else "")]
    paare = ", ".join(f"{k}/{w:.4f}" for k, w in enumerate(werte))
    z += [f"\t\\foreach \\k/\\w in {{{paare}}} {{",
          "\t\t\\filldraw[fill=blue!25, draw=blue] (\\k-0.4,0) rectangle (\\k+0.4,\\w);"]
    if a.markiere:
        z += [f"\t\t\\ifnum\\k<{lo} \\else \\ifnum\\k>{hi} \\else",
              "\t\t\t\\filldraw[fill=red!40, draw=red] (\\k-0.4,0) rectangle (\\k+0.4,\\w);",
              "\t\t\\fi\\fi"]
    z += ["\t}",
          "\t% Achsen",
          f"\t\\draw[-latex, thick] (-0.5,0) -- ({n + 0.8},0) node[right] {{$k$}};",
          f"\t\\draw[-latex, thick] (-0.5,0) -- (-0.5,{ymax + schritt * 0.6:.3f}) node[above] {{$P(X=k)$}};",
          f"\t\\foreach \\k in {{0,...,{n}}}",
          "\t\t\\node[below, font=\\tiny] at (\\k,0) {$\\k$};",
          "\t\\foreach \\y/\\t in {" + ", ".join(
              f"{schritt * i:.2f}/" + f"{schritt * i:.2f}".replace(".", "{,}")
              for i in range(1, round(ymax / schritt) + 1)) + "}",
          "\t\t\\draw (-0.6,\\y) -- (-0.4,\\y) node[left, font=\\tiny, xshift=-2pt] {$\\t$};",
          "\\end{tikzpicture}"]
    print("\n".join(z))


if __name__ == "__main__":
    main()
