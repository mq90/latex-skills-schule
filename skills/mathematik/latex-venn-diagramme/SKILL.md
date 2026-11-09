---
name: latex-venn-diagramme
description: Venn-Diagramme und Mengenoperationen mit TikZ zeichnen – zwei und drei Mengen, Vereinigung, Schnitt, Differenz, symmetrische Differenz, Komplement, Muster statt Grau. Verwende diesen Skill immer, wenn Mengen, Mengendiagramme, Mengenlehre, Ereignisse in der Stochastik (A ∩ B, Gegenereignis) oder eine Handreichung zu Venn-Diagrammen in LaTeX gebraucht werden.
---

# Venn-Diagramme mit TikZ

Setzt `latex-grundstil` voraus. `patterns` ist in der universalen
`header.tex` geladen.

## Feste Vorlage (zwei Mengen)

Immer dieselben Maße, damit alle Diagramme eines Blattes gleich aussehen:
Grundmenge `(0,0) rectangle (6,4)`, Kreise `(2,2)` und `(4,2)` mit Radius
`1.2cm`, Beschriftungen `A` bei `(1.3,2)`, `B` bei `(4.7,2)`, `Ω` bei `(0.3,3.7)`.

```latex
\begin{tikzpicture}
	% 1. Fläche füllen (immer in scope, damit clip nur hier wirkt)
	\begin{scope}
		\clip (2,2) circle (1.2cm);
		\fill[gray, opacity=0.5] (4,2) circle (1.2cm);   % A ∩ B
	\end{scope}
	% 2. Konturen und Beschriftung zuletzt
	\draw (0,0) rectangle (6,4);
	\draw (2,2) circle (1.2cm);
	\draw (4,2) circle (1.2cm);
	\node at (1.3,2) {$A$};
	\node at (4.7,2) {$B$};
	\node at (0.3,3.7) {$\Omega$};
\end{tikzpicture}
```

## Füllregeln

| Menge | Inhalt der scope-Umgebung |
|---|---|
| $A$ | `\fill[gray, opacity=0.5] (2,2) circle (1.2cm);` |
| $A \cup B$ | beide Kreise füllen (ohne clip) |
| $A \cap B$ | `\clip` A, dann B füllen |
| $A \setminus B$ | `\clip` A, B weiß füllen, dann A grau füllen |
| $A \triangle B$ | zwei scopes: $A \setminus B$ und $B \setminus A$ |
| $\overline{A}$ | `\clip` Rechteck, Rechteck grau, A weiß |

Drei Mengen: Grundmenge `(0,0) rectangle (7,5)`, Kreise `(2.5,2.5)`,
`(4.5,2.5)`, `(3.5,1.3)` mit Radius `1.3cm`, `scale=0.9`. Verschachtelte
`\clip`-Befehle in einer scope ergeben Schnitte mehrerer Mengen.

## Stolpersteine

- Erst füllen, **dann** Konturen zeichnen – sonst überdeckt die Füllung
  die Linien.
- `\clip` immer in eine `scope`, sonst wirkt er auf das ganze Bild.
- „Weiß füllen“ zum Aussparen funktioniert nur auf weißem Untergrund (nicht
  in farbigen Boxen). Dort Muster oder `even odd rule` verwenden.
- Für Schwarz-Weiß-Kopien Muster statt Grau: `\fill[pattern=north east lines]`.

## Referenz

Vollständige Handreichung (alle Operationen für zwei und drei Mengen,
Muster): `references/handreichung_venn.tex`.
