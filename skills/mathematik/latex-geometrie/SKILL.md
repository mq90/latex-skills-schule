---
name: latex-geometrie
description: Geometrische Figuren in LaTeX mit TikZ nach festen Gestaltungsregeln – Dreiecke mit Ecken, Seiten und Winkeln, rechte Winkel, Höhen, Maßlinien, Kreise und Sektoren, Vierecke, Konstruktionen mit Zirkelbögen, Körper im Schrägbild (Quader, Zylinder, Pyramide, Kegel), Würfelnetze, Skizze neben Teilaufgaben. Verwende diesen Skill IMMER, wenn eine geometrische Skizze, Konstruktion oder ein Körper auf ein Arbeitsblatt, in eine Leistungskontrolle oder Handreichung soll.
---

# Geometrie mit TikZ

Setzt `latex-grundstil` voraus. `calc`, `angles`, `quotes` und der Stil
`punkt` sind in den universalen Dateien vorhanden.

## Gestaltungsregeln

| Element | Stil |
|---|---|
| Hauptfigur | `blue, very thick` |
| Maße, Winkel, Hervorhebungen | `red, thick` |
| Hilfslinien (Höhe, Durchmesser), verdeckte Kanten | `dashed` |
| Konstruktionslinien (Zirkelbögen) | `gray, thin` |
| Flächen | `\filldraw[gray, opacity=0.5]` |
| Eckpunkte | erst `\coordinate (A) at (…);`, Beschriftung `\node[below left] at (A) {$A$};` |
| Seiten | gegenüber der gleichnamigen Ecke, Mitte mit `($(A)!0.5!(B)$)` |
| Maßlinie | `\draw[|<->|, red, thick] (0,-0.5) -- node[below] {$a = \unit[4]{cm}$} (4,-0.5);` mit Abstand zur Figur |

## Dreieck (Grundvorlage)

```latex
\begin{tikzpicture}
	\coordinate (A) at (0,0);
	\coordinate (B) at (5,0);
	\coordinate (C) at (1.5,3);
	\pic[draw=red, thick, "$\alpha$", angle radius=0.6cm, angle eccentricity=1.6] {angle=B--A--C};
	\pic[draw=red, thick, "$\beta$", angle radius=0.6cm, angle eccentricity=1.6] {angle=C--B--A};
	\pic[draw=red, thick, "$\gamma$", angle radius=0.6cm, angle eccentricity=1.6] {angle=A--C--B};
	\draw[blue, very thick] (A) -- (B) -- (C) -- cycle;
	\node[below left] at (A) {$A$};
	\node[below right] at (B) {$B$};
	\node[above] at (C) {$C$};
	\node[below] at ($(A)!0.5!(B)$) {$c$};
	\node[above right] at ($(B)!0.5!(C)$) {$a$};
	\node[above left] at ($(A)!0.5!(C)$) {$b$};
\end{tikzpicture}
```

- `angle=B--A--C` misst **gegen den Uhrzeigersinn** von AB nach AC. Bei
  Ecken im Uhrzeigersinn ergibt die falsche Reihenfolge den Außenwinkel.
- Rechter Winkel: `\pic[draw=red, thick, angle radius=0.35cm] {right angle=B--H--C};`
  oder Winkelbogen mit Punkt (Vorlage in der Referenz).
- Winkel vor dem Dreieck zeichnen, damit die Seiten darüber liegen.

## Körper im Schrägbild

Kavalierperspektive: Tiefe unter 45° und halb so lang, z. B.
`\coordinate (E) at ($(A)+(45:\t*0.5)$);`. Verdeckte Kanten zuerst und
gestrichelt, dann die sichtbaren. Zylinder und Kegel: Grundfläche als zwei
Halbellipsen – vorne `arc[start angle=180, end angle=360, x radius=\r, y radius=\e]`
durchgezogen, hinten gestrichelt.

## Skizze neben Teilaufgaben

```latex
\begin{multicols}{2}
	\begin{enumerate}[(a)]
		\item Konstruiere das Dreieck.
		\item Berechne den Flächeninhalt.
	\end{enumerate}
	\columnbreak
	\centering
	\begin{tikzpicture}[scale=0.6]
		\draw[blue, very thick] (0,0) -- (5,0) -- (1.5,3) -- cycle;
	\end{tikzpicture}
\end{multicols}
```

## Stolpersteine

- Winkelbeschriftung mit `"$\alpha$"` braucht die Bibliotheken `quotes` und
  `babel` (beide geladen) – sonst kollidiert `"` mit ngerman.
- `scale` verkleinert auch `angle radius` und Punktgrößen mit; Punkte deshalb
  mit dem Knoten-Stil `punkt`.
- Konstruktionen: Bögen mit `(A) ++(Startwinkel:r) arc[start angle=…, end angle=…, radius=r]`
  ansetzen – der Bogen beginnt am aktuellen Punkt, nicht am Mittelpunkt.
- Maße realistisch wählen oder „Skizze nicht maßstabsgetreu“ dazuschreiben.

## Referenz

`references/handreichung_geometrie.tex` – Handreichung mit allen Vorlagen
(Code oben, Ausgabe darunter): Dreieck, rechtwinkliges Dreieck, Höhe,
Maßlinien und Teilflächen, Kreis mit Sektor, Parallelogramm und Trapez,
Mittelsenkrechte, Quader, Zylinder, Pyramide, Kegel, Würfelnetz, Skizze
neben Teilaufgaben.
