---
name: latex-sprechblasen
description: Sprechblasen und Gedankenblasen (Callouts) mit TikZ – abgerundete Comic-Blasen, Zipfel gezielt links oder rechts setzen, fertige Befehle \lehrerblase und \schuelerblase für Dialoge, Impulse und Unterrichtsgespräche. Verwende diesen Skill immer, wenn Sprechblasen, Dialoge, Comics, Denkblasen, Lehrer-Schüler-Gespräche oder Hinweise mit Zeiger in einem LaTeX-Dokument gebraucht werden – auch zusammen mit tikzpeople-Figuren.
---

# Sprechblasen mit TikZ

Setzt `latex-grundstil` voraus. `shapes.callouts` ist in der universalen
`header.tex` geladen, `\lehrerblase` und `\schuelerblase` stehen in der
`newcommands.tex`.

## Fertige Befehle für Dialoge

```latex
\lehrerblase[text width=0.82\linewidth]{\textbf{Impuls:} Was passiert bei einer Verschiebung um 3?}

\vspace{5mm}

\hfill\schuelerblase[text width=0.62\linewidth]{Man ersetzt jeden Buchstaben durch den dritten danach.}
```

Lehrerblase: blau, Zipfel links unten. Schülerblase: grün, Zipfel rechts
unten. Im optionalen Argument gehen alle TikZ-Knotenoptionen
(`text width=…`, `fill=…`, `callout relative pointer=…`).

## Freie Sprechblase

```latex
\begin{tikzpicture}
	\node[rectangle callout, rounded corners=6pt, draw, thick, fill=blue!6,
	      align=left, inner sep=3.5mm,
	      callout relative pointer={(-12mm,-7mm)}] {Lehrer: Guten Morgen!};
\end{tikzpicture}
```

| Option | Wirkung |
|---|---|
| `rectangle callout` / `ellipse callout` / `cloud callout` | Form (cloud = Gedanken, mit `aspect=2.5`) |
| `callout relative pointer={(x,y)}` | Zipfel relativ zur Mitte – gut fürs Layout |
| `callout absolute pointer={(A.mouth)}` | Zipfel auf einen Punkt, z. B. eine tikzpeople-Figur |
| `callout pointer width=10mm`, `callout pointer arc=18` | Breite/Form des Zipfels |
| `callout pointer shorten=1mm` | Zipfel kürzen |

## Stolpersteine

- Sehr lange Texte brechen nicht über Seiten um – Callouts sind für kurze
  bis mittlere Texte. Für lange Texte eine tcolorbox verwenden.
- `rounded corners` gilt auch für den Zipfel; bei großen Radien wirkt er
  stumpf – dann `callout pointer shorten` oder kleinerer Radius.
- Die Blasen-Befehle **nicht** im Dokument neu definieren (stehen zentral).

## Referenz

Vollständige Handreichung (Grundidee, Comic-Optik, Zipfel links/rechts,
relative vs. absolute Pointer, Feintuning, Komfort-Befehle):
`references/handreichung_sprechblasen.tex`. Figuren dazu: `latex-tikzpeople`.
