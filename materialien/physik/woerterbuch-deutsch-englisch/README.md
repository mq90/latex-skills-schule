# Physikalisches Wörterbuch Deutsch – Englisch

Nachschlagewerk für den (bilingualen) Physikunterricht: 295 Fachbegriffe mit
englischer Lautschrift, Formelzeichen und Skizzen, dazu ein Teil „Physik lesen und
sprechen“ mit Lesarten und Beispielen in beiden Sprachen.

| Datei | Inhalt |
|---|---|
| [`Physikalisches-Woerterbuch-Deutsch-Englisch.pdf`](Physikalisches-Woerterbuch-Deutsch-Englisch.pdf) | fertiges PDF (59 Seiten) |
| `Physikalisches-Woerterbuch-Deutsch-Englisch.tex` | erzeugter Quelltext, kompiliert mit pdflatex |
| `quelle/` | Daten und Bausteine, aus denen `bauen.py` die `.tex`-Datei erzeugt |

## Aufbau

- **Teil I – Wörterbuch:** Größen und Messen, Bewegungen, Kräfte, Energie,
  Wärmelehre, Elektrizität und Magnetismus, Schwingungen und Wellen, Optik,
  Atom- und Kernphysik.
- **Teil II – Physik lesen und sprechen:** SI-Einheiten, Vorsätze,
  angloamerikanische Einheiten, Temperaturskalen, Formeln lesen, Experimente
  und Diagramme beschreiben, griechische Buchstaben.
- **Teil III – Register** Deutsch → Englisch und English → German.

Jedes Kapitel beginnt auf einer neuen Seite und endet mit Beispielen. Alle
Überschriften stehen zweisprachig da, die englische mit Lautschrift
(`quelle/ueberschriften.py`).

## Bauen

```
python3 quelle/bauen.py Physikalisches-Woerterbuch-Deutsch-Englisch.tex ../../../skills/grundlagen/latex-grundstil/assets
pdflatex Physikalisches-Woerterbuch-Deutsch-Englisch.tex    # dreimal
```

Nutzt die universalen Stildateien sowie `latex-lautschrift` (`\ipa`) und
`latex-physik` (Schaltzeichen mit circuitikz). Neuer Begriff: Zeile in
`quelle/daten.py` ergänzen und neu bauen.
