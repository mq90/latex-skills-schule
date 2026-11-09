---
name: latex-sudoku
description: Sudokus in LaTeX setzen und erzeugen – mit dem Paket sudoku und einem Python-Generator, der Rätsel mit garantiert eindeutiger Lösung in drei Schwierigkeitsstufen samt Lösungsblatt liefert. Verwende diesen Skill immer, wenn jemand ein Sudoku-Arbeitsblatt, Sudoku-Rätsel, eine Rätselseite, eine Vertretungsstunde mit Knobelaufgaben, ein Sudoku als Backtracking-Beispiel im Informatikunterricht oder eine Handreichung zum sudoku-Paket möchte, auch wenn LaTeX nicht ausdrücklich erwähnt wird.
---

# Sudokus mit LaTeX

Dieser Skill deckt zwei Dinge ab: das **Setzen** von Sudoku-Gittern mit dem
Paket `sudoku` und das **Erzeugen** neuer Rätsel mit `scripts/sudoku_generator.py`.
Rätsel nie selbst „ausdenken“ oder abtippen: Ein von Hand erfundenes Sudoku hat
fast immer keine oder mehrere Lösungen. Der Generator prüft jede Aufgabe per
Backtracking auf genau eine Lösung.

## Arbeitsablauf

1. Rätsel erzeugen:
   ```bash
   python3 scripts/sudoku_generator.py -n 4 -s mittel --seed 1 -o sudokus.tex
   ```
   - `-s leicht|mittel|schwer` → etwa 40 / 32 / 28 Vorgaben
   - `--seed` macht das Ergebnis reproduzierbar (gleiche Zahl = gleiche Rätsel);
     für Parallelklassen verschiedene Seeds verwenden
   - `--loesen "53..7....6.."` (81 Zeichen, `.` oder `0` = leer) prüft und löst
     ein vorhandenes Sudoku, z. B. aus einer Zeitung
2. `sudokus.tex` enthält pro Rätsel die Befehle `\SudokuAufgabeA`,
   `\SudokuLoesungA`, `\SudokuAufgabeB`, … In der Lösung sind Vorgaben fett,
   ergänzte Ziffern grau.
3. Für ein Arbeitsblatt `assets/vorlage_sudoku_arbeitsblatt.tex` kopieren
   (vier Rätsel auf Seite 1, Lösungen auf Seite 2) und mit `pdflatex` kompilieren.
4. PDF in ein Bild umwandeln (`pdftoppm -r 50 -png`) und ansehen, bevor es
   ausgeliefert wird.

## Das Paket `sudoku` – Befehlsreferenz

```latex
\usepackage{sudoku}
\setlength\sudokusize{7cm}                       % Kantenlänge (Standard 10cm)
\setlength\sudokuthinline{0.4pt}                 % dünne Linien
\setlength\sudokuthickline{1.6pt}                % Blockränder (Standard 2pt)
\renewcommand*\sudokuformat[1]{\LARGE\sffamily#1} % Schrift der Ziffern

\begin{sudoku}          % zentriert (center-Umgebung)
|5|3| | |7| | | | |.
|6| | |1|9|5| | | |.
...                     % genau 9 Zeilen
\end{sudoku}
```

| Element | Bedeutung |
|---|---|
| `sudoku` | Umgebung, setzt das Gitter zentriert |
| `sudoku-block` | wie `sudoku`, aber ohne `center` – für `minipage`, Tabellen, nebeneinander |
| `\|5\|` | Zelle mit Ziffer; Leerzeichen `\| \|` = leere Zelle |
| `.` am Zeilenende | schließt die Zeile ab – fehlt er, verrutscht alles |
| `\sudokusize`, `\sudokuthinline`, `\sudokuthickline` | Längen, mit `\setlength` ändern |
| `\sudokuformat` | Formatierung jeder Zelle, mit `\renewcommand*` ändern |

## Stolpersteine (getestet)

- **Befehle in einer Zelle immer in Klammern:** `|{\textbf{5}}|`, nicht
  `|\textbf{5}|`. Das Trennzeichen `|` liest genau *ein* Argument; ohne Klammern
  zerfällt der Befehl und es kommt „Argument of \textcolor has an extra }“.
- **Kein Punkt im Zellinhalt.** Der Punkt ist das Zeilenende-Zeichen.
- **`sudoku` nicht zusammen mit `printsudoku`/`sudokubundle` laden.** Beide
  definieren `\sudoku` – die Fehlermeldung ist dann unverständlich. Für
  Arbeitsblätter reicht `sudoku` plus Generator völlig.
- Das Gitter darf in Makros stehen (der Generator nutzt das), weil das Paket mit
  e-TeX (`\scantokens`) arbeitet – also mit pdflatex, xelatex oder lualatex.
- Nur 9×9. Für 4×4- oder 6×6-Mini-Sudokus (Klasse 5/6) ein Gitter mit TikZ
  zeichnen (`\draw[step=1] (0,0) grid (4,4);` plus dicke Linien) – dann die
  Eindeutigkeit von Hand prüfen.

## Für eine Handreichung

Wenn eine Handreichung zum Paket gewünscht ist (statt eines Arbeitsblatts),
`assets/stil_handreichung.tex` daneben legen, mit `\input{stil_handreichung}` einbinden und mit den Umgebungen `beispiel` (Code links,
Ergebnis rechts), `merke`, `hinweis`, `tipp` arbeiten. Jedes Code-Beispiel muss
kompiliert sein, bevor es in die Handreichung kommt.

## Ideen für den Unterricht

- **Informatik:** Sudoku als Einstieg in Backtracking und Rekursion – die
  Funktion `loese()` im Generator ist kurz genug, um sie gemeinsam zu lesen.
  Spannend: Warum ist „Feld mit den wenigsten Kandidaten zuerst“ so viel schneller?
- **Mathematik:** Wie viele Vorgaben braucht man mindestens? (17 – bewiesen 2012
  per Computer.) Lateinische Quadrate als Verallgemeinerung.
- **Vertretung/Differenzierung:** gleiche Seite, drei Stufen, Lösung auf der
  Rückseite.
