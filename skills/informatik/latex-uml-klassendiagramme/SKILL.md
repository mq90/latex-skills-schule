---
name: latex-uml-klassendiagramme
description: UML-Klassendiagramme mit TikZ zeichnen – Klassen mit Attributen und Methoden, Sichtbarkeiten, Vererbung, Assoziation, Komposition, Aggregation, Abhängigkeit, Gruppierungen. Verwende diesen Skill immer, wenn Klassendiagramme, Objektorientierung (OOP) im Informatikunterricht, Klassenkarten oder eine Handreichung zu UML in LaTeX gebraucht werden.
---

# UML-Klassendiagramme mit TikZ

Setzt `latex-grundstil` voraus. Die Stile `umlclass`, `inherit`,
`compose`, `aggregate`, `associate`, `depend` stehen in der universalen
`newcommands.tex`; `shapes.multipart`, `arrows.meta`, `positioning`, `fit`,
`calc` sind in der `header.tex` geladen.

## Klasse

```latex
\begin{tikzpicture}
	\node[umlclass] (person) {
		\textbf{Person}
		\nodepart{second}
		- name: String \\
		- alter: int
		\nodepart{third}
		+ getName(): String \\
		+ setName(name: String): void
	};
\end{tikzpicture}
```

Sichtbarkeit: `+` public, `-` private, `\#` protected (Raute escapen!).
Breite anpassen: `\node[umlclass, text width=6cm]`.

## Beziehungen

| Beziehung | Code | Pfeil |
|---|---|---|
| Vererbung | `\draw[inherit] (kind) -- (eltern);` | offenes Dreieck an der Oberklasse |
| Assoziation | `\draw[associate] (a) -- (b);` | Linie |
| Komposition | `\draw[compose] (teil) -- (ganzes);` | gefüllte Raute am Ganzen |
| Aggregation | `\draw[aggregate] (teil) -- (ganzes);` | offene Raute am Ganzen |
| Abhängigkeit | `\draw[depend] (a) -- (b);` | gestrichelt |

Multiplizitäten/Rollen: `\node[above] at ($(a)!0.5!(b)$) {besucht *};`
Pakete/Gruppen: `\node[draw, dashed, fit=(a) (b), inner sep=5mm] {};`

## Referenz

Vollständige Handreichung (Stil-Definitionen, alle Beziehungen, eigene
Befehle, Schulverwaltungssystem als großes Beispiel, Gruppierungen mit
`fit`): `references/handreichung_uml.tex`.
