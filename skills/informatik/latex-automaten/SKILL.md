---
name: latex-automaten
description: Endliche Automaten (DEA, NEA, Zustandsdiagramme) mit TikZ und der automata-Bibliothek zeichnen – Start- und Endzustände, Übergänge, Schleifen, gebogene Kanten, größere Automaten. Verwende diesen Skill immer, wenn ein Automat, Zustandsübergangsdiagramm, eine formale Sprache als Automat, ein Getränkeautomat-/Ampel-Modell oder eine Handreichung zu Automaten in LaTeX entstehen soll – auch für Arbeitsblätter und Klausuren in Informatik.
---

# Automaten mit TikZ

Setzt `latex-grundstil` voraus. Die Bibliotheken `automata`, `positioning`
und `arrows.meta` sind in der universalen `header.tex` bereits geladen.

## Grundmuster

```latex
\begin{tikzpicture}[initial text={$\mathcal{A}$:}, node distance=3cm, auto]
	\node[state, initial]               (q0) {$q_0$};
	\node[state, right=of q0]           (q1) {$q_1$};
	\node[state, accepting, right=of q1] (q2) {$q_2$};

	\draw[->] (q0) edge[above] node{$a$} (q1);
	\draw[->] (q1) edge[bend left, above] node{$b$} (q2);
	\draw[->] (q2) edge[bend left, below] node{$a$} (q1);
	\draw[->] (q1) edge[loop above] node{$a,b$} (q1);
\end{tikzpicture}
```

| Element | Code |
|---|---|
| Zustand | `\node[state] (q0) {$q_0$};` |
| Startzustand | `initial` (Pfeil von links); Beschriftung mit `initial text={$\mathcal{A}$:}` |
| Endzustand | `accepting` (Doppelkreis) |
| Übergang | `\draw[->] (q0) edge[above] node{$a$} (q1);` |
| Gebogen | `edge[bend left]` / `edge[bend right]`, Hin- und Rückweg immer beide `bend left` |
| Schleife | `edge[loop above]`, `loop right`, `loop below`, `loop left` |
| Positionieren | `right=3cm of q0`, `below right=of q1` (positioning) |
| Einheitliche Abstände | `node distance=3cm, auto` in den tikzpicture-Optionen |
| Verkleinern | `scale=0.8, every node/.style={scale=0.8}` |

## Konventionen

- Zustände einheitlich benennen ($q_0, q_1, …$), mehrere Symbole mit Komma
  ($a,b$), Leerwort als $\varepsilon$.
- Erst alle Zustände, dann alle Übergänge – so bleibt der Code lesbar.
- Bei großen Automaten ein Raster planen (zwei Reihen, `below=of …`),
  Kanten mit `bend` um andere Zustände herumführen.

## Referenz

Die vollständige Handreichung mit allen Beispielen (Grundzustände,
Schleifentypen, Praxisbeispiele „ungerade Anzahl a“, „Teilwort ab“, komplexe
Automaten, Tipps) steht in `references/handreichung_automaten.tex`. Für eine
neue Handreichung den Aufbau aus `latex-grundstil` verwenden (Code in
`lstlisting[style=latex]`, Ausgabe direkt darunter).
