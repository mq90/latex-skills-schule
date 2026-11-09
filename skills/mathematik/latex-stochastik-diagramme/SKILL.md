---
name: latex-stochastik-diagramme
description: Stochastik-Darstellungen in LaTeX mit festen TikZ-Vorlagen – Baumdiagramme (waagerecht oder von oben nach unten, zwei- und dreistufig, mit Pfadwahrscheinlichkeiten, ohne Zurücklegen, mit Lücken), Vierfeldertafeln und Säulendiagramme/Histogramme von Binomialverteilungen (Skript mit exakten Werten, kein pgfplots). Verwende diesen Skill IMMER, wenn Wahrscheinlichkeiten, Zufallsexperimente, Baumdiagramme, Vierfeldertafeln, bedingte Wahrscheinlichkeiten oder Binomialverteilungen auf ein Arbeitsblatt, in eine Klausur oder Handreichung kommen.
---

# Stochastik-Diagramme mit TikZ

Setzt `latex-grundstil` voraus. Die Stile `baumdiagramm`,
`baumdiagrammvertikal`, `wkeit` und `punkt` stehen in der universalen
`newcommands.tex`. Mengendiagramme für Ereignisse: `latex-venn-diagramme`.

## Baumdiagramm (Standard)

```latex
\begin{tikzpicture}[baumdiagramm]
	\node[punkt] {}
		child {node {$A$}
			child {node {$B$} edge from parent node[wkeit, above] {$0{,}5$}}
			child {node {$\overline{B}$} edge from parent node[wkeit, below] {$0{,}5$}}
			edge from parent node[wkeit, above] {$0{,}6$}}
		child {node {$\overline{A}$}
			child {node {$B$} edge from parent node[wkeit, above] {$0{,}2$}}
			child {node {$\overline{B}$} edge from parent node[wkeit, below] {$0{,}8$}}
			edge from parent node[wkeit, below] {$0{,}4$}};
\end{tikzpicture}
```

- Wächst nach rechts, **erstes `child` = oberer Ast**; oben `above`, unten
  `below`. `edge from parent …` steht im `child` **nach** den Kindern.
- Dezimalkomma `0{,}5`, Brüche `\tfrac{3}{5}`.
- Pfadwahrscheinlichkeit rechts am Blatt:
  `node[label={[font=\small]right:$P(A \cap B) = 0{,}6 \cdot 0{,}5 = 0{,}30$}] {$B$}`
- Drei Stufen: `[baumdiagramm, level distance=2.2cm]` – Astabstände der
  Ebenen 1–3 (3 / 1,6 / 0,8 cm) stehen im Stil.
- Lücke: statt der Zahl `{\rule{0.7cm}{0.4pt}}`.
- Mehr als zwei Äste pro Knoten: drei `child`-Einträge; mittlerer Ast
  ohne `above`/`below` (`node[wkeit, fill=white]`), ggf. `sibling distance`
  im Bild vergrößern.

## Baumdiagramm von oben nach unten

```latex
\begin{tikzpicture}[baumdiagrammvertikal]
	\node[punkt] {}
		child {node {$A$}
			child {node[label={[font=\scriptsize]below:$0{,}30$}] {$B$}
				edge from parent node[wkeit, left] {$0{,}5$}}
			child {node {$\overline{B}$} edge from parent node[wkeit, right] {$0{,}5$}}
			edge from parent node[wkeit, left] {$0{,}6$}}
		child {node {$\overline{A}$}
			child {node {$B$} edge from parent node[wkeit, left] {$0{,}2$}}
			child {node {$\overline{B}$} edge from parent node[wkeit, right] {$0{,}8$}}
			edge from parent node[wkeit, right] {$0{,}4$}};
\end{tikzpicture}
```

- Wächst nach unten, **erstes `child` = linker Ast**; links `left`, rechts
  `right`, Beschriftung waagerecht (kein `sloped`).
- Pfadwahrscheinlichkeit unter dem Blatt mit `label=below:…`.
- Astabstände der Ebenen 1–3: 4,8 / 2,4 / 1,2 cm; dreistufig
  `[baumdiagrammvertikal, level distance=1.4cm]`.
- Passt platzsparend in die rechte Spalte von `multicols` neben Teilaufgaben.
- Wann welche Richtung? Waagerecht, wenn Pfadrechnungen rechts daneben
  stehen sollen; senkrecht, wenn das Blatt schmal ist oder der Baum neben
  Teilaufgaben steht.

## Vierfeldertafel

```latex
{\renewcommand{\arraystretch}{1.6}
\begin{tabular}{c|c|c|c}
	               & $B$      & $\overline{B}$ & $\Sigma$ \\ \hline
	$A$            & $0{,}30$ & $0{,}30$       & $0{,}60$ \\ \hline
	$\overline{A}$ & $0{,}08$ & $0{,}32$       & $0{,}40$ \\ \hline
	$\Sigma$       & $0{,}38$ & $0{,}62$       & $1$      \\
\end{tabular}}
```

Mit Lücken: Spalten `>{\centering\arraybackslash}p{1.5cm}` (Vorlage in der
Referenz). Die Werte immer nachrechnen (Zeilen- und Spaltensummen).

## Säulendiagramm einer Binomialverteilung

Nicht in TikZ rechnen lassen – `scripts/binomial_saeulen.py` berechnet die
Werte exakt und schreibt fertigen TikZ-Code:

```bash
python3 scripts/binomial_saeulen.py 10 0.3                     # B(10; 0,3)
python3 scripts/binomial_saeulen.py 20 0.5 --markiere 0-8      # P(X ≤ 8) rot
python3 scripts/binomial_saeulen.py 10 0.3 --hoehe 4.5 --breite 10 --tabelle
```

Säulen `blue!25`, hervorgehobene `red!40`, Gitter `gray!30`, Achsen `-latex`,
y-Beschriftung mit Dezimalkomma.

## Stolpersteine (getestet)

- Mit `grow=right` stünde das erste Kind **unten**; der Stil nutzt deshalb
  `grow'=right`. In eigenen Bäumen nicht auf `grow=right` zurückwechseln.
- `\arraystretch` nur in einer Gruppe `{…}` ändern – die header.tex setzt
  1,25 für alle anderen Tabellen.
- pgfmath kann keine großen Fakultäten: `factorial(8)` bricht mit
  „Arithmetic overflow“ ab (Grenze 16383). Binomialkoeffizienten deshalb
  immer mit dem Skript.

## Referenz

`references/handreichung_stochastik.tex` – Handreichung mit allen Vorlagen
(Code oben, Ausgabe darunter): zweistufig, mit Pfadwahrscheinlichkeiten,
ohne Zurücklegen, dreistufig, mit Lücken, von oben nach unten (zwei- und
dreistufig, mit Pfadwahrscheinlichkeiten), Vierfeldertafel ausgefüllt und mit
Lücken, Säulendiagramm B(10; 0,3) mit P(X ≤ 3).
