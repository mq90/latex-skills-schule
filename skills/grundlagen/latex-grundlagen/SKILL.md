---
name: latex-grundlagen
description: Nachschlagewerk für LaTeX-Grundlagen im Schulkontext – Präambel und Dokumentklassen, mathematischer Formelsatz (Brüche, Summen, Integrale, Matrizen, cases, align), Tabellen (booktabs, multicolumn, multirow, tabularx, longtable, Dezimalkomma, Wahrheitstabellen) und eigene Befehle mit newcommand/newenvironment. Verwende diesen Skill, wenn Formeln oder Tabellen gesetzt, eigene Makros angelegt oder LaTeX-Einsteiger (Kolleginnen, Schüler) angeleitet werden sollen, oder wenn eine Formel- oder Tabellenfrage zu einem Arbeitsblatt auftaucht.
---

# LaTeX-Grundlagen (Nachschlagewerke)

Vier Nachschlagewerke im Handreichungsstil (Code oben, Ausgabe darunter).
Sie sind die Referenz dafür, **wie** Formeln, Tabellen und Befehle in
diesem System geschrieben werden. Bei einer konkreten Frage die passende
Datei lesen (Abschnitt über die Überschrift suchen), nicht alle.

| Thema | Datei | Inhalt |
|---|---|---|
| Präambel, Dokumentklassen, Pakete | `references/grundlagen_von_latex.tex` | Struktur einer Datei, Klassen und Optionen, Grundpakete, Seitengeometrie, Präambel-Vorlagen |
| Formelsatz | `references/mathematischer_formelsatz.tex` | Umgebungen, Operatoren, Indizes, Brüche, Klammern, Summen/Integrale/Grenzwerte, Vektoren, Matrizen, `cases`, `align`, griechische Buchstaben, Akzente, Unterrichtsbeispiele |
| Tabellen | `references/tabellen.tex` | `tabular`, Linien, `booktabs`, feste Spaltenbreiten, `multicolumn`, `multirow`, Dezimalkomma, `tabularx`, `longtable`, `colortbl`, Wahrheitstabellen, Messwerte, Fachbeispiele, häufige Fehler |
| Eigene Befehle | `references/eigene_befehle.tex` | `\newcommand`, `\newenvironment`, Beispiele aus der eigenen `newcommands.tex` |

## Kurzregeln, die immer gelten

**Formeln**
- Abgesetzte Formeln mit `\[ … \]`, mehrzeilig mit `align*` (am `&`
  ausrichten), Fallunterscheidungen mit `cases`. Kein `$$ … $$`.
- Klammern um hohe Ausdrücke mit `\left( … \right)`.
- Funktionsnamen aufrecht: `\sin`, `\ln`, `\lim`; eigene mit
  `\operatorname{…}`.
- Dezimalkomma als `4{,}5`, Einheiten mit `\unit[4{,}5]{cm}`.
- Abkürzungen aus der universalen `newcommands.tex` nutzen (`\R`, `\limn`,
  `\dx`, `\vektor{…}{…}{…}` – Liste in `latex-grundstil/references/makros.md`).

**Tabellen**
- Linien mit `booktabs`: `\toprule`, `\midrule`, `\bottomrule`,
  Gruppen mit `\cmidrule(lr){2-3}`. Möglichst keine senkrechten Linien
  (Ausnahme: Wahrheitstabellen, Wertetabellen in Mathe).
- Zeilenabstand ist in der header.tex mit `\arraystretch` 1,25 gesetzt.
- Feste Breite mit Umbruch: `p{3cm}`; zentriert:
  `>{\centering\arraybackslash}p{3cm}` (Paket `array` ist geladen).
- Über die Textbreite: `tabularx` mit `X`-Spalten; über mehrere Seiten:
  `longtable`.

**Eigene Befehle**
- Neue Befehle gehören in die universale `newcommands.tex`, nicht ins
  Dokument (Regeln in `latex-grundstil`). Erst in `makros.md` nachsehen.
- Sprechende Namen ohne Ziffern, deutsche Namen sind üblich (`\luecke`,
  `\gegges`). Kein bestehender LaTeX-Befehl überschreiben – vorher mit
  `\newcommand` testen (meldet „already defined“).

## Eigenständige Dateien

Drei der Nachschlagewerke (`grundlagen_von_latex`, `mathematischer_formelsatz`,
`tabellen`) haben eine eigene Präambel mit `\documentclass` und kompilieren
ohne header.tex; `eigene_befehle.tex` nutzt `\input{header.tex}`.
