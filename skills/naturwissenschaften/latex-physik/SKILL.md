---
name: latex-physik
description: Physik-Material mit LaTeX – Einheiten (units), Messwertdiagramme mit automatisch berechneter Ausgleichsgerade (lineare Regression in reinem TikZ), Schaltpläne mit circuitikz (deutsche Symbole, Gruppe A/B aus einer Vorlage), berechnete Strahlengänge an der Sammellinse, Federn und Wellen. Verwende diesen Skill immer, wenn jemand ein Physik-Arbeitsblatt, einen Schaltplan, eine Reihen- oder Parallelschaltung, ein Messwertdiagramm, das Hookesche Gesetz, eine Linsenkonstruktion, Optik-Aufgaben oder physikalische Einheiten in LaTeX braucht.
---

# Physik mit LaTeX

Setzt `latex-grundstil` voraus. In der universalen `header.tex` sind `units`,
`circuitikz` (Option `european`) und TikZ samt `decorations.pathmorphing`
geladen. Grundsatz: Zahlen stehen nur einmal in der Datei, Zeichnung und
Rechnung werden daraus **berechnet** – nichts nachzeichnen.

## Vorlagen (`assets/`, getestet)

| Datei | Inhalt | Was man ändert |
|---|---|---|
| `vorlage_federdehnung.tex` | Messwerte als Punkte, Ausgleichsgerade und Federkonstante D berechnet (kleinste Quadrate, reines TikZ) | `\def\messwerte{0.0/0.00, 1.1/0.50, …}` (s in cm / F in N) |
| `vorlage_schaltplaene.tex` | Reihen- und Parallelschaltung; Gruppe A (Lampen) und B (Widerstände) aus einer Schaltung mit Platzhalterstil `bauteil` | `\tikzset{bauteil/.style={lamp}}` |
| `vorlage_linse.tex` | `\Linse{g}{f}{G}`: Bildweite und -größe aus der Linsengleichung, drei Konstruktionsstrahlen treffen sich im Bildpunkt | Aufrufe `\Linse{4}{1.5}{1.2}` (Werte in cm, g > f) |

## Einheiten

```latex
$g = \unitfrac[9{,}81]{m}{s^2}$   $U = \unit[230]{V}$   $R = \unit[4{,}7]{k\Omega}$
```
Berechnete Werte: `\pgfmathprintnumber[fixed, zerofill, precision=2, use comma]{\D}`.

## Schaltpläne (circuitikz)

`\draw (0,0) to[battery1, l=$U$] (0,3) to[lamp, l=$L_1$] (3,3) to[rmeter, t=A] (3,0) -- (0,0);`
Bauteile: `battery1`, `sV`, `lamp`, `R`, `vR`, `C`, `L`, `D`, `leD`, `nos`,
`rmeter, t=A` / `t=V`; Verzweigung `node[circ]{}`.

## Stolpersteine (getestet)

- **Kein `siunitx`** zusammen mit der universalen `header.tex`: Abbruch mit
  „Package 'units' incompatible“ bzw. „Command '\unit' already defined“.
  Einheiten mit `\unit` aus `units`; `siunitx` nur in eigenständigen Dokumenten.
- **Kein pgfplots** (Repository-Grundsatz): Diagramme mit reinem TikZ, Regression
  über `\foreach` mit `\xdef` (ein `\def` wäre nach jedem Schleifendurchlauf
  vergessen).
- Ohne Option `european` zeichnet circuitikz amerikanische Symbole (Zickzack-Widerstand).
- Exponentialfunktionen über großen Bereichen: „Dimension too large“ –
  `domain` begrenzen oder Achse stauchen (`y=0.01cm`).

## Handreichung

`references/handreichung_physik.tex` (9 Seiten; PDF in `handreichungen/`):
Pakete, Einheiten, Messwerte und Regression, Schaltpläne mit Bauteiltabelle,
Optik, Feder mit `decorations.pathmorphing`, Stolpersteine. Die Beispiele mit
Vorlagen enthalten deren Code wörtlich; nach Änderungen an einer Vorlage dort
mitändern. Stil: Code in `lstlisting[style=latex]`, darunter `ausgabe`.
