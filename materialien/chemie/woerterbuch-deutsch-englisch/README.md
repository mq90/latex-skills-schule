# Chemisches Wörterbuch Deutsch – Englisch

Nachschlagewerk für den (bilingualen) Chemieunterricht: 260 Fachbegriffe mit
englischer Lautschrift, Formeln und Skizzen, dazu ein Teil „Chemie lesen und
sprechen“ mit Lesarten und Beispielen in beiden Sprachen.

| Datei | Inhalt |
|---|---|
| [`Chemisches-Woerterbuch-Deutsch-Englisch.pdf`](Chemisches-Woerterbuch-Deutsch-Englisch.pdf) | fertiges PDF (50 Seiten) |
| `Chemisches-Woerterbuch-Deutsch-Englisch.tex` | erzeugter Quelltext, kompiliert mit pdflatex |
| `quelle/` | Daten und Bausteine, aus denen `bauen.py` die `.tex`-Datei erzeugt |

## Aufbau

- **Teil I – Wörterbuch:** Stoffe, Laborgeräte, Atombau und Periodensystem,
  Bindung, Reaktionen, Säuren und Basen, Redox und Elektrochemie, organische
  Chemie, Stoffmenge.
- **Teil II – Chemie lesen und sprechen:** Elementnamen, Formeln und
  Reaktionsgleichungen, Benennung von Salzen, Säuren, Basen und organischen
  Verbindungen, pH-Wert, Rechnen mit Stoffmengen, Experimente und Sicherheit.
- **Teil III – Register** Deutsch → Englisch und English → German.

Jedes Kapitel beginnt auf einer neuen Seite und endet mit Beispielen. Alle
Überschriften stehen zweisprachig da, die englische mit Lautschrift
(`quelle/ueberschriften.py`).

## Bauen

```
python3 quelle/bauen.py Chemisches-Woerterbuch-Deutsch-Englisch.tex ../../../skills/grundlagen/latex-grundstil/assets
pdflatex Chemisches-Woerterbuch-Deutsch-Englisch.tex    # dreimal
```

Nutzt die universalen Stildateien sowie `latex-lautschrift` (`\ipa`) und
`latex-chemie` (`\ce` aus mhchem, `\chemfig`). Neuer Begriff: Zeile in
`quelle/daten.py` ergänzen und neu bauen.
