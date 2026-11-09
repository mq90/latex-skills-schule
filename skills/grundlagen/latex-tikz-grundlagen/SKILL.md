---
name: latex-tikz-grundlagen
description: Grundlagen des Zeichnens mit TikZ für Unterrichtsmaterial – draw, Koordinaten, Linienarten, Formen, Knoten (node), Farben, cycle, foreach-Schleifen, Berechnungen mit calc, Flächen füllen, Kästchenpapier mit topline, plot mit scope und clip. Verwende diesen Skill, sobald in einem LaTeX-Dokument etwas mit TikZ gezeichnet wird und kein spezieller Fach-Skill passt, oder wenn jemand TikZ lernen bzw. Kolleginnen erklären will.
---

# TikZ-Grundlagen

Zwei Referenzen im Handreichungsstil:

| Datei | Inhalt |
|---|---|
| `references/grundlagen_in_tikz.tex` (Nachschlagewerk) | Einbinden, Grundstruktur, Linien und Pfade, Linientypen, Flächen, Grundformen, `node` (Positionierung, Formen, Knoten auf Pfaden), Farben, `cycle`, Beispiele: Koordinatensystem, Funktionsgraph, Flussdiagramm, Winkel |
| `references/zeichnen_mit_tikz.tex` (Handreichung) | `\draw`, Koordinaten und Winkel, `\foreach`, `\fill`, `calc`-Bibliothek, Füllen entlang berechneter Pfade, Kästchenpapier mit `multicols` + `topline`, `plot` in `scope`/`clip`, Flächen unter Graphen |

Für Funktionsgraphen, Geometrie und Baumdiagramme gibt es Fach-Skills mit
festen Vorlagen (`latex-funktionsgraphen`, `latex-geometrie`,
`latex-stochastik-diagramme`) – die haben Vorrang.

## Das Wichtigste in Kürze

```latex
\begin{tikzpicture}[scale=0.9]
	\draw[blue, very thick] (0,0) -- (4,0) -- (2,3) -- cycle;     % geschlossener Pfad
	\draw[dashed] (2,0) -- (2,3);                                 % Linientyp
	\fill[gray, opacity=0.5] (5,0) rectangle (7,2);               % Fläche
	\draw (8,1) circle (1cm);
	\foreach \i in {0,60,...,300}                                 % Schleife
		\draw (8,1) -- ($(8,1) + cos(\i)*(1,0) + sin(\i)*(0,1)$);  % calc
	\node[below] at (2,0) {$c$};                                   % Beschriftung
\end{tikzpicture}
```

- **`cycle`** schließt einen Pfad sauber (sonst eine Lücke an der Ecke).
- **`\foreach \i in {0,60,...,300}`**: Schrittweite ergibt sich aus den
  ersten beiden Werten; Dezimalschritte `{1,1.5,...,7}`.
- **calc**: `($(A)+(1,2)$)`, `($(A)!0.5!(B)$)` (Mitte), Winkel in Grad
  (`cos(60)`), Wurzel `sqrt(12)`.
- **scope + clip**: `\begin{scope}\clip (…) rectangle (…); … \end{scope}` –
  der Clip wirkt nur innerhalb der scope.
- **Kästchenpapier/Bild oben bündig in Aufzählungen:** Option `topline`
  (steht in der universalen `newcommands.tex`, braucht `calc`):
  `\item \begin{tikzpicture}[topline] … \end{tikzpicture}`.
- **Linienstärken:** `thin`, `thick`, `very thick`; Farben mit Deckkraft
  `gray, opacity=0.5`; Mischfarben `blue!20`.

## Stolpersteine

- Winkel in `cos`/`sin` sind **Grad**. In `plot` mit Bogenmaß rechnen:
  `sin(\x r)`.
- Negative Werte potenzieren: `(\x)^2` statt `\x^2` – sonst rechnet pgf
  `-2^2 = -4`.
- `scale` skaliert Koordinaten, aber nicht Schriftgröße und Linienbreite.
- Umlaute in Knoten gehen direkt (`\node {Höhe};`).
