---
name: latex-funktionsgraphen
description: Funktionsgraphen und Koordinatensysteme in LaTeX mit reinem TikZ (kein pgfplots) im festen Arbeitsblatt-Stil – lineare, quadratische, Potenz-, Exponential-, trigonometrische und gebrochen-rationale Funktionen, Punkte, Schnittpunkte, Asymptoten, Flächen unter Graphen, Tangenten, Sachaufgaben-Achsen, drei Graphen nebeneinander. Verwende diesen Skill IMMER, wenn auf einem Arbeitsblatt, in einer Leistungskontrolle oder Handreichung ein Koordinatensystem oder Graph vorkommt.
---

# Funktionsgraphen mit TikZ

Setzt `latex-grundstil` voraus. Alles sieht gleich aus, weil immer
dieselben Vorlagen benutzt werden. **Kein pgfplots.**

## Standard: `\koordinatensystem`

Der Befehl steht in der universalen `newcommands.tex` und zeichnet exakt das
Standard-Koordinatensystem (Gitter `gray!30`, Achsen `-latex`, jede zweite
Einheit beschriftet in `\tiny`):

```latex
\begin{tikzpicture}[scale=0.42]
	\koordinatensystem{-6}{6}{-6}{6}            % [Schritt]{xmin}{xmax}{ymin}{ymax}
	\begin{scope}
		\clip (-6,-6) rectangle (6,6);           % gleicher Bereich wie das Gitter
		\draw[blue, thick, domain=-6:6, samples=200] plot (\x, {2*\x - 1});
	\end{scope}
	\node[blue, font=\scriptsize] at (4.2,5.4) {$f$};
\end{tikzpicture}
```

- Bereich: ganze Zahlen, muss 0 enthalten. `[1]` beschriftet jede Einheit.
- Maßstab `scale=0.42`; drei Systeme nebeneinander `scale=0.52` mit
  Bereich −4…4 und `\hfill` dazwischen.
- Ausgeschriebene Fassung (zum Abwandeln von Gitter oder Achsen): Kapitel 1
  der Referenz.

## Feste Regeln

| Was | So |
|---|---|
| Graph | `\draw[blue, thick, domain=…, samples=200] plot (\x, {…});` in `scope` + `\clip` |
| Mehrere Graphen | Farben in der Reihenfolge `blue`, `red`, `green!60!black`, `orange` |
| Funktionsname | `\node[Farbe, font=\scriptsize] at (…) {$f$};` an freier Stelle nahe am Graphen |
| Punkt | `\node[punkt, label={[font=\scriptsize]right:$P(2\mid 3)$}] at (2,3) {};` |
| Offener Punkt | `\node[punktoffen] at (…) {};` |
| Asymptote | `\draw[dashed, gray] (1,-6) -- (1,6);` |
| Fläche | erst `\fill[gray, opacity=0.5] (a,0) -- plot[domain=a:b] (\x,{…}) -- (b,0) -- cycle;`, dann Graph |
| Sachaufgabe | 1. Quadrant, Achsen `$t$ in s`, `$s$ in m`, Null unten links (Vorlage in der Referenz) |
| Winkelfunktionen | Gitter bei Vielfachen von π/2, Beschriftung `\frac{\pi}{2}` …, `sin(\x r)` |

## Stolpersteine (getestet)

- **Bogenmaß:** `sin(\x)` rechnet in Grad. Für Graphen im Bogenmaß
  `sin(\x r)`, Bereich `domain={-2*pi}:{2*pi}`.
- **Negative Basis:** `\x^2` ergibt für negative x einen negativen Wert
  (pgf rechnet `-2^2 = -4`). Immer `(\x)^2`, `(\x-1)^3`.
- **Polstellen:** Bereich in zwei Äste teilen (`domain=-6:0.87` und
  `domain=1.13:6` bei einer Polstelle in x = 1), sonst verbindet TikZ die Äste mit einer senkrechten Linie.
- **Punkte:** `circle (3pt)` wird mit `scale=0.42` mitverkleinert (auf gut
  1 pt). Deshalb die Knoten-Stile `punkt`/`punktoffen`.
- **clip vergessen:** Der Graph läuft über das Gitter hinaus.
- Die Schleifenvariable `\x` in `plot` stört `\koordinatensystem` nicht (das
  Makro nutzt intern andere Namen).

## Referenz

`references/handreichung_funktionsgraphen.tex` – Handreichung im
Standardstil mit allen Vorlagen (Code oben, Ausgabe darunter):
Standard-System ausführlich und als Makro, mehrere Graphen, Punkte,
Sachaufgabe, drei nebeneinander, Sinus/Kosinus, Hyperbel mit Asymptoten,
Exponentialfunktionen, abschnittsweise Funktionen, Fläche, Tangente.
Vor dem Zeichnen eines neuen Graphentyps dort die passende Vorlage
kopieren.
