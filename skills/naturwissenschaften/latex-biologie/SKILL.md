---
name: latex-biologie
description: Biologie-Material mit LaTeX – Kreuzungsschema (Punnett-Quadrat), das Genotypen bildet, nach Phänotyp färbt und das Aufspaltungsverhältnis selbst zählt; Stammbäume mit genealogytree und Lösungsschalter; berechnete Codesonne (genetischer Code); exponentielles und logistisches Wachstum; Nahrungsnetze als Graph. Verwende diesen Skill immer, wenn jemand ein Biologie-Arbeitsblatt zu Genetik, Erbgängen, Mendel, Stammbaumanalyse, Proteinbiosynthese, Codesonne, Populationsökologie oder Nahrungsnetzen in LaTeX braucht.
---

# Biologie mit LaTeX

Setzt `latex-grundstil` voraus. In der universalen `header.tex` sind TikZ
(mit `positioning`, `arrows.meta`) und `genealogytree` geladen. LaTeX ist
hier stark, wo Biologie **Struktur** ist – Fotos und realistische Zeichnungen
lieber als Bild einbinden.

## Vorlagen (`assets/`, getestet)

| Datei | Inhalt | Was man ändert |
|---|---|---|
| `vorlage_kreuzungsschema.tex` | `\kreuzung{AB,Ab,aB,ab}{AB,Ab,aB,ab}`: Genotypen, Färbung nach Phänotyp, gezähltes Verhältnis (9:3:3:1, Testkreuzung 1:1:1:1) | Keimzellen der Eltern (je 2 Buchstaben, 1. Merkmal zuerst) |
| `vorlage_stammbaum.tex` | Stammbaum autosomal-rezessiv, `\loesungfalse`/`\loesungtrue` blendet Überträger ein | Familie in `child{ g[…]{} p[…]{} c[…]{} … }` |
| `vorlage_codesonne.tex` | Codesonne aus drei Schleifen über U, C, A, G; Farben nach Eigenschaft der Aminosäure, Start AUG markiert | Farbzuordnung, Aminosäure-Liste |
| `vorlage_wachstum.tex` | exponentielles und logistisches Wachstum, Kapazität K | `\Nnull`, `\rate`, `\K` |
| `vorlage_nahrungsnetz.tex` | Nahrungsnetz mit `positioning`, Produzenten/Konsumenten farbig | Knoten und Liste der Fressbeziehungen |

## Stammbaum-Grundgerüst (genealogytree)

```latex
\begin{genealogypicture}[node size=7mm, level distance=1.1cm,
   mann/.style={box={sharp corners}}, frau/.style={box={arc=3.5mm}},
   krank/.style={box={colback=black, colupper=white}}]
  child{ g[mann]{1} p[frau]{2}  c[frau]{3}  c[mann, krank]{4} }
\end{genealogypicture}
```

## Stolpersteine (getestet)

- **Kein pgfplots** (Repository-Grundsatz): Wachstumskurven mit `\draw plot`,
  Exponentialkurve mit `domain=0:\tend` begrenzen, sonst „Dimension too large“.
- Makro für die Wachstumsrate heißt `\rate`, nicht `\r` (`\r` ist in LaTeX der Ring-Akzent).
- `\newcount` für eigene Zähler in die Präambel, nicht in den Befehl.

## Handreichung

`references/handreichung_biologie.tex` (9 Seiten; PDF in `handreichungen/`):
alle fünf Vorlagen mit vollständigem Code und Ausgabe, Erklärung der
Rechenlogik, weitere Pakete (forest, pgfmolbio), Stolpersteine.
