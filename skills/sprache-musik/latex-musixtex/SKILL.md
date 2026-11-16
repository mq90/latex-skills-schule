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
\Notes\hu{g}\qu{h}\qu{i}\en
\bar
\Notes\wh{j}\en
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

**Tonhöhen sind absolute Buchstaben** (getestet): `c d e f g` = c'–g',
dann geht das Alphabet weiter: `h` = a', `i` = h', `j` = c'', `k` = d'' …
`a`/`b` sind das kleine a/h **unter** dem System. Großbuchstaben setzen die
Reihe nach unten fort: `N` = g, `J` = c (kleine Oktave), `H` = A – Bassstimmen
also mit Großbuchstaben (Klavierbass `\qb0{JNL}` = c–g–e).
`'` hebt alle folgenden Töne bis zum nächsten `\en` um eine Oktave (`!` hebt
auf). Beim Abschreiben von Melodien deshalb `h i j …` statt `a b 'c` schreiben.

## Musik-Kürzel (`assets/musik-befehle.tex`)

Intervalle (`\terz`, `\quint`, …), Tongeschlecht (`\dur`, `\moll`),
Tonnamen (`\cis`, `\fis`, `\es`, `\bb`, …, **`\disTon`** statt `\dis`, weil
`\dis` in der universalen newcommands.tex der Displaystyle ist), Notenwerte
im Text (`\viertel`, `\achtelpause`), Taktarten (`\dreivierteltakt`),
Boxen `musiktheorie`, `uebung`, `repertoire`, Umgebungen `akkordfolge`,
`tonleiter`, Befehle `\liedtitel`, `\tempo`, `\tonart`, `\taktart`.

## Vorzeichen, Tonart und Akkorde

Vorzeichen als Kurzform in der Notenklammer: `^` (Kreuz), `_` (Be),
`=` (Auflösung), z. B. `\qu{^f}` für fis, `\qu{_i}` für b'. Gleichwertig:
Befehl **vor** dem Notenbefehl, `\sh f\qu f`. Eine durchgehende Tonart setzt
`\generalsignature{n}` **vor** `\startextract` (positiv = Kreuze,
negativ = Be): `-1` = F-Dur, `2` = D-Dur.

Akkorde stapelt man mit `\zw` (ganze) oder `\zq` (Viertel) für die unteren
Töne; die letzte Note trägt den Notenwert. Vorzeichen als Kurzform an die
Zusatznote: `\notes\zw{c}\zw{e}\zw{_i}\wh{g}\en` ergibt C7 (c-e-g-b').

## Liedtext und Akkordsymbole

Liedtext unter den Noten mit `musixlyr` (Bibliothek, **nach** `\usepackage{musixtex}`
per `\input musixlyr` laden). Text **vor** den Noten festlegen, Silben mit
**einfachem** `-` trennen:

```latex
\setlyrics{strophe}{Häns-chen klein ging al-lein ...}
\assignlyrics1{strophe}
```

Größe und Abstände in mehrzeiligen Liedsätzen (alle getestet, siehe
`vorlage_lied_haenschen.tex`):

| Befehl | Wirkung |
|---|---|
| `\Largemusicsize` | größeres System; **vor** `\begin{music}`, innen wirkungslos |
| `\staffbotmarg=8\Interligne` | Platz unter jedem System; **innerhalb** `music` |
| `\stafftopmarg=4\Interligne` | Platz über jedem System (Akkordsymbole) |
| `\setsongraise1{8mm}` | Text verschieben (positiv = höher, bezogen auf den unteren Rand) |

Ein großer `\staffbotmarg` schiebt den Text mit nach unten; mit positivem
`\setsongraise` wieder unter die eigene Zeile holen.

Akkordsymbole (Harmonien) über das System mit `\zcharnote{12}{\bf F}` – nur
an Harmoniewechseln, nicht an jede Note. Hochgestellte Ziffer: `C$^7$`.

## Vorlagen (`assets/`)

| Vorlage | Inhalt |
|---|---|
| `notenpapier.tex` | Basis für das Notenpapier, nicht allein kompilierbar (Schnipsel) |
| `vorlage_lied_haenschen.tex` | kompletter Liedsatz „Hänschen klein“ (F-Dur) mit Liedtext und Akkorden, großes System, 4 Takte pro Zeile – Muster für eigene Lieder |
| `vorlage_quintenzirkel.tex` | Quintenzirkel in TikZ: großer Kreis, Dur außen, parallele Moll innen, außen je ein Notenlinien-Ausschnitt mit den Vorzeichen (Ges links, Fis rechts), Eselsbrücken und Merkregeln darunter; Schlüssel/Vorzeichen aus der Schrift `musix24` (`\char71/52/50`), **kein** `\usepackage{musixtex}` |
| `vorlage_notenpapier_a5_{hoch,quer}_{mit,ohne}_schluessel.tex` | Blanko-Notenpapier A5; setzen nur zwei Schalter und laden `notenpapier.tex` (dort Linien- und Systemabstand einstellen). Druckfertige PDFs in `druckvorlagen/musik/` |

## Stolpersteine

- `musixlyr` (Liedtexte) fehlt in manchen TeX-Installationen
  („File musixlyr.tex not found“). Erst prüfen (`kpsewhich musixlyr.tex`),
  sonst Liedtext unter die Noten mit einer Tabelle oder `\zcharnote` setzen.
- `\qu{\sh f}`, `\wh{\fl i}`: Vorzeichen**befehl** in der Notenklammer setzt
  **gar keine** Note, ohne Fehlermeldung (getestet). Kurzform `^ _ =` in der
  Klammer oder Befehl davor (`\sh f\qu f`).
- `\qu a` ist das kleine a unter dem System, nicht das a' (das ist `\qu h`).
  Abgeschriebene Melodien als PNG rendern und Note für Note mit der Vorlage
  vergleichen.
- `\lyrraise1{-2pt}` ohne Bezugsbuchstaben schiebt den Text ins System;
  `\setsongraise1{…}` verwenden (oder `\lyrraise1{b-2pt}`).
- `\assignlyrics1{name}` gilt global, auch in späteren `music`-Umgebungen
  (Reste erscheinen als Punkte unter fremden Noten); nach dem Lied
  `\assignlyrics1{}` (getestet).
- `\bar` direkt vor `\alaligne` ergibt einen doppelten Strich am Zeilenende;
  `\alaligne` setzt den Taktstrich selbst.
- In der `ausgabe`-Box funktioniert `music` (getestet); `\parindent10mm`
  rückt das System ein, für zentrierte Beispiele `\begin{center}` drumherum.

## Referenz

`references/handreichung_musixtex.tex` – Handreichung im Standardstil
(Drei-Wege-Kompilierung, Notenwerte und Punktierung, absolute Tonhöhen und
Oktavieren, B/H, Vorzeichen und Tonart, Takt/Schlüssel/Pausen, Balken und
Haltebögen, Akkorde, Klaviersystem, Liedtext mit musixlyr samt Größe und
Abständen, „Alle meine Entchen“, Akkordsymbole, Quintenzirkel, Urheberrecht
beim Teilen von Noten, Praxistipps).
