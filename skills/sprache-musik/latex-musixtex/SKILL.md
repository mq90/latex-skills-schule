---
name: latex-musixtex
description: Noten in LaTeX setzen mit MusiXTeX – Notensysteme, Notenwerte, Oktaven, Taktarten, Taktstriche, Pausen, einfache Melodien, plus Musik-Kürzel für Intervalle, Tonnamen und Notenwerte im Text. Verwende diesen Skill, wenn Noten, Melodien, Notenbeispiele, Rhythmusübungen oder eine Handreichung zum Notensatz in einem LaTeX-Dokument gebraucht werden, auch fächerübergreifend (Mathe: Bruchrechnung mit Notenwerten, Physik: Frequenzen).
---

# Notensatz mit MusiXTeX

Setzt `latex-grundstil` voraus. **MusiXTeX ist nicht in der universalen
header.tex geladen**, weil es `\cup` als Achtelnote umdefiniert – danach
bricht `$A \cup B$` mit „Undefined control sequence“ ab (getestet).

## Einbinden (nur in Musik-Dokumenten)

```latex
\input{header.tex}
\usepackage{musixtex}        % direkt nach der header.tex
\input{newcommands.tex}
\input{musik-befehle.tex}    % optionale Musik-Kürzel aus assets/
```

**Drei Durchläufe:** `pdflatex datei` → `musixflx datei` → `pdflatex datei`.
musixflx berechnet die Abstände; ohne den Zwischenlauf stehen die Noten
gestaucht. (`werkzeuge/alles_kompilieren.py` macht das automatisch.)

## Grundgerüst

```latex
\begin{music}
\parindent10mm
\instrumentnumber{1}
\setstaffs1{1}
\generalmeter{\meterfrac44}
\startextract
\Notes\qu{c}\qu{d}\qu{e}\qu{f}\en
\bar
\Notes\hu{g}\qu{a}\qu{b}\en
\bar
\Notes\wh{'c}\en
\endextract
\end{music}
```

| Befehl | Bedeutung |
|---|---|
| `\startextract … \endextract` | kurzes Notenbeispiel (ein System) |
| `\startpiece … \endpiece` | längeres Stück mit Zeilenumbrüchen |
| `\Notes … \en` | eine Notengruppe |
| `\bar` | Taktstrich |
| `\wh{c}` | ganze Note |
| `\hu{d}` / `\hl{d}` | halbe Note, Hals oben / unten |
| `\qu{f}` / `\ql{f}` / `\qa{f}` | Viertel, Hals oben / unten / automatisch |
| `\cu{g}` / `\cl{g}` | Achtel (c = *croche*), Hals oben / unten |
| `\generalmeter{\meterfrac34}` | Taktart |
| `\setname1{Flöte}` | Instrumentenname |

Tonhöhen: `c` ist das c' (eingestrichenes c); Großbuchstaben tiefer,
`'c` und `''c` höher.

## Musik-Kürzel (`assets/musik-befehle.tex`)

Intervalle (`\terz`, `\quint`, …), Tongeschlecht (`\dur`, `\moll`),
Tonnamen (`\cis`, `\fis`, `\es`, `\bb`, …, **`\disTon`** statt `\dis`, weil
`\dis` in der universalen newcommands.tex der Displaystyle ist), Notenwerte
im Text (`\viertel`, `\achtelpause`), Taktarten (`\dreivierteltakt`),
Boxen `musiktheorie`, `uebung`, `repertoire`, Umgebungen `akkordfolge`,
`tonleiter`, Befehle `\liedtitel`, `\tempo`, `\tonart`, `\taktart`.

## Stolpersteine

- `musixlyr` (Liedtexte) fehlt in vielen TeX-Installationen
  („File musixlyr.sty not found“). Erst prüfen (`kpsewhich musixlyr.sty`),
  sonst Liedtext unter die Noten mit einer Tabelle setzen.
- Notennamen: `\cu{b}` ist das h (englische Benennung), `b` im Deutschen heißt
  in MusiXTeX `_b` (Vorzeichen) – vorher die Ausgabe ansehen.
- In der `ausgabe`-Box funktioniert `music` (getestet); `\parindent10mm`
  rückt das System ein, für zentrierte Beispiele `\begin{center}` drumherum.

## Referenz

`references/handreichung_musixtex.tex` – Handreichung im Standardstil
(Grundlagen und Paketeinbindung, Notenwerte, Oktaven).
