---
name: latex-musixtex
description: Noten in LaTeX setzen mit MusiXTeX – Notensysteme, Notenwerte, Oktaven, Taktarten, Taktstriche, Pausen, Vorzeichen und Tonart, Akkorde, Liedtext mit musixlyr und Akkordsymbole über den Noten, komplette Liedsätze; dazu ein Quintenzirkel in reinem TikZ. Plus Musik-Kürzel für Intervalle, Tonnamen und Notenwerte im Text. Verwende diesen Skill, wenn Noten, Melodien, Liedsätze mit Text und Akkorden, ein Quintenzirkel, Notenbeispiele, Rhythmusübungen oder eine Handreichung zum Notensatz in einem LaTeX-Dokument gebraucht werden, auch fächerübergreifend (Mathe: Bruchrechnung mit Notenwerten, Physik: Frequenzen).
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

## Vorzeichen, Tonart und Akkorde

Vorzeichen stehen **vor** der Note: `\sh` (Kreuz), `\fl` (Be), `\na`
(Auflösung), z. B. `\qu{\sh f}` für fis. Eine durchgehende Tonart setzt
`\generalsignature{n}` **vor** `\startextract` (positiv = Kreuze,
negativ = Be): `-1` = F-Dur, `2` = D-Dur.

Akkorde stapelt man mit `\zw` (ganze) oder `\zq` (Viertel) für die unteren
Töne; die **oberste** Note trägt den Notenwert. Ein Vorzeichen gehört an die
Zusatznote, nicht an die ganze Wertnote: `\notes\zw{c}\zw{e}\zw{\fl b}\wh{g}\en`
ergibt C7 (c-e-g-b).

## Liedtext und Akkordsymbole

Liedtext unter den Noten mit `musixlyr` (Bibliothek, **nach** `\usepackage{musixtex}`
per `\input musixlyr` laden). Text **vor** den Noten festlegen, Silben mit
**einfachem** `-` trennen:

```latex
\setlyrics{strophe}{Häns-chen klein ging al-lein ...}
\assignlyrics1{strophe}
```

Stößt der Text an tiefe Notenköpfe: `\interstaff{10}` (mehr Abstand, vor der
`music`-Umgebung), `\lyrraise1{-2pt}` (Text tiefer) und bei tiefer Lage `\qu`
(Hälse nach oben vom Text weg). **`\lyrraise`** ist der richtige Befehl, nicht
`\setlyrraise`. Tonhöhen möglichst **ohne** Apostroph schreiben – MusiXTeX
wählt die nächstliegende Oktave, so bleibt die Melodie kompakt im System; nur
die erste Note je Zeile anheben.

Akkordsymbole (Harmonien) über das System mit `\zcharnote{10}{\bf F}` – nur
an Harmoniewechseln, nicht an jede Note. Hochgestellte Ziffer: `C$^7$`.

## Vorlagen (`assets/`)

| Vorlage | Inhalt |
|---|---|
| `vorlage_lied_haenschen.tex` | kompletter Liedsatz „Hänschen klein“ (F-Dur) mit Liedtext und Akkorden – Muster für eigene Lieder |
| `vorlage_quintenzirkel.tex` | Quintenzirkel in reinem TikZ: Dur außen, parallele Moll innen, Zahl der Vorzeichen; braucht **kein** MusiXTeX |

## Stolpersteine

- `musixlyr` (Liedtexte) fehlt in manchen TeX-Installationen
  („File musixlyr.tex not found“). Erst prüfen (`kpsewhich musixlyr.tex`),
  sonst Liedtext unter die Noten mit einer Tabelle oder `\zcharnote` setzen.
- Akkord-Vorzeichen: `\wh{\fl b}` als **ganze** Wertnote setzt das Be nicht
  zuverlässig – das Vorzeichen an eine `\zw`-Zusatznote hängen (getestet).
- Notennamen: `\cu{b}` ist das h (englische Benennung), `b` im Deutschen heißt
  in MusiXTeX `_b` (Vorzeichen) – vorher die Ausgabe ansehen.
- In der `ausgabe`-Box funktioniert `music` (getestet); `\parindent10mm`
  rückt das System ein, für zentrierte Beispiele `\begin{center}` drumherum.

## Referenz

`references/handreichung_musixtex.tex` – Handreichung im Standardstil
(Grundlagen und Paketeinbindung, Notenwerte, Oktaven, deutsche Notennamen und
Vorzeichen, Tonart, Pausen, Akkorde, Liedtext mit musixlyr samt
Kollisionsvermeidung, Akkordsymbole, Quintenzirkel sowie ein Abschnitt zum
Urheberrecht beim Teilen von Noten).
