---
name: latex-digitale-schaltungen
description: Digitale Schaltungen und Logikgatter (AND, OR, NOT, NAND, NOR, XOR, XNOR) mit TikZ zeichnen – US- und IEC-Symbole, Ein- und Ausgänge, Verbindungen, Halbaddierer. Verwende diesen Skill immer, wenn Logikgatter, Schaltnetze, Halb-/Volladdierer, boolesche Schaltungen oder eine Handreichung zu digitalen Schaltungen in LaTeX gebraucht werden.
---

# Digitale Schaltungen mit TikZ

Setzt `latex-grundstil` voraus. `circuits.logic.US`, `circuits.logic.IEC`,
`positioning` und `calc` sind in der universalen `header.tex` geladen.

## Gatter

```latex
\begin{tikzpicture}[circuit logic US]      % oder: circuit logic IEC (DIN-Kästchen)
	\node[and gate]  (g1) {};
	\node[or gate, right=2cm of g1]  (g2) {};
	\node[not gate, right=2cm of g2] (g3) {};
	\node[below=0.3cm of g1] {\small AND};
\end{tikzpicture}
```

Gatter: `and gate`, `or gate`, `not gate`, `nand gate`, `nor gate`,
`xor gate`, `xnor gate`, auch `buffer gate`.
Anzahl Eingänge: `inputs=nn` (zwei normale), `inputs=nin` (mittlerer negiert).

## Verbinden

```latex
\begin{tikzpicture}[circuit logic US, thick]
	\node (A) at (0,1) {A};
	\node (B) at (0,0) {B};
	\node[and gate, inputs=nn] (und) at (2,0.5) {};
	\draw (A) -| ($(und.input 1)+(-0.5,0)$) -- (und.input 1);
	\draw (B) -| ($(und.input 2)+(-0.5,0)$) -- (und.input 2);
	\draw (und.output) -- ++(1,0) node[right] {Y};
\end{tikzpicture}
```

- Anker: `input 1`, `input 2`, … und `output`.
- Rechtwinklige Leitungen mit `-|` und `|-`; Abzweigpunkte mit
  `\fill (p) circle (2pt);` markieren.
- Eingänge links in einer Spalte, Ausgang rechts – Signalfluss von links
  nach rechts.

## Referenz

Vollständige Handreichung (alle Gatter in US/IEC, erweiterte Gatter,
Verbindungen, Halbaddierer): `references/handreichung_digitale_schaltungen.tex`.
Für Wahrheitstabellen die Tabellenregeln aus `latex-grundlagen` verwenden.
