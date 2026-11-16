# Mathematisches Wörterbuch Deutsch – Englisch

Nachschlagewerk für den (bilingualen) Mathematikunterricht: 353 Fachbegriffe
mit englischer Lautschrift, Zeichen und Skizzen, dazu ein Teil „Mathematik
lesen und sprechen“ mit Lesarten und Beispielen in beiden Sprachen.

| Datei | Inhalt |
|---|---|
| [`Mathematisches-Woerterbuch-Deutsch-Englisch.pdf`](Mathematisches-Woerterbuch-Deutsch-Englisch.pdf) | fertiges PDF (89 Seiten) |
| `Mathematisches-Woerterbuch-Deutsch-Englisch.tex` | erzeugter Quelltext, kompiliert mit pdflatex |
| `quelle/` | Daten und Bausteine, aus denen `bauen.py` die `.tex`-Datei erzeugt |

## Aufbau

- **Teil I – Wörterbuch:** zehn Sachgebiete (Zahlen, Algebra, Funktionen,
  Geometrie, Körper, Analysis, Vektoren, Stochastik, Logik), je Zeile
  deutscher Begriff, englischer Begriff mit Lautschrift, Zeichen oder Skizze.
- **Teil II – Mathematik lesen und sprechen:** 22 Kapitel von Zahlen und
  Relationszeichen bis Kegelschnitte und griechisches Alphabet.
- **Teil III – Register** Deutsch → Englisch und English → German.

Jedes Kapitel beginnt auf einer neuen Seite und endet mit Beispielen.

## Bauen

```
python3 quelle/bauen.py Mathematisches-Woerterbuch-Deutsch-Englisch.tex ../../../skills/grundlagen/latex-grundstil/assets
pdflatex Mathematisches-Woerterbuch-Deutsch-Englisch.tex    # dreimal (Inhaltsverzeichnis, Register)
```

Das Dokument nutzt die universalen `header.tex`/`newcommands.tex` und die
Skills `latex-grundstil`, `latex-lautschrift` (tipa, `\ipa`), `latex-geometrie`,
`latex-funktionsgraphen` und `latex-venn-diagramme`. Befehle, die nur dieses
Dokument braucht (`\eintrag`, `\lies`, `\sk…`-Skizzen), stehen lokal in der Präambel.

Neuer Begriff: Zeile in `quelle/daten_zusatz2.py` ergänzen (hinter einem
Ankerbegriff), neu bauen. Lautschrift in tipa-Kürzeln, britische Aussprache.
