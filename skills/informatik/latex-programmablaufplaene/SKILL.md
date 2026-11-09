---
name: latex-programmablaufplaene
description: Programmablaufpläne (PAP, Flussdiagramme) mit TikZ zeichnen – feste Stile für Ein-/Ausgabe, Verarbeitung und Verzweigung, Knoten positionieren, Pfeile beschriften, Schleifen zurückführen. Verwende diesen Skill immer, wenn ein Programmablaufplan, Flussdiagramm, Ablaufdiagramm eines Algorithmus oder eine Handreichung dazu in LaTeX entstehen soll (für Struktogramme ebenfalls zuerst hier nachsehen).
---

# Programmablaufpläne mit TikZ

Setzt `latex-grundstil` voraus. Die Stile stehen in der universalen
`newcommands.tex` – **nicht** im Dokument neu definieren:

| Stil | Form | Farbe | für |
|---|---|---|---|
| `input` | Parallelogramm | grün | Eingabe |
| `operation` | Rechteck | orange | Verarbeitung, Start, Ende |
| `condition` | Raute | magenta | Verzweigung (Frage mit ?) |
| `output` | Parallelogramm | rot | Ausgabe |

## Grundmuster

```latex
\begin{tikzpicture}[node distance=1.5cm]
	\node[operation] (start) {Start};
	\node[input, below=of start] (ein) {Zahl $n$ einlesen};
	\node[condition, below=of ein] (test) {$n \geq 0$?};
	\node[output, right=2.5cm of test] (fehler) {Fehler};
	\node[operation, below=of test] (ende) {Ende};

	\draw[->] (start) -- (ein);
	\draw[->] (ein) -- (test);
	\draw[->] (test) -- node[left] {ja} (ende);
	\draw[->] (test) -- node[above] {nein} (fehler);
	\draw[->] (fehler) |- (ende);
\end{tikzpicture}
```

- Erst alle Knoten (relativ mit `below=of …`, `right=2.5cm of …`), dann
  alle Pfeile.
- Verzweigungen immer mit „ja“/„nein“ beschriften.
- Schleife zurück: `\draw[->] (calc) -- ++(-2.5,0) |- (loop);`
- Mehrzeiliger Knotentext mit `\\` (z. B. `{$fak = 1$\\$i = 1$}`) funktioniert,
  weil die Stile `align=center` enthalten. In eigenen Knoten ohne `align`
  verschluckt TikZ den Umbruch **ohne Fehlermeldung** („fak = 1i = 1“) –
  also immer `align=center` setzen (getestet).

## Referenz

Vollständige Handreichung (eigene Stile definieren, Node-Grundlagen,
Abstände, Beschriftungen, komplexe Pfade, Fakultät als Beispiel):
`references/handreichung_programmablaufplaene.tex`.
