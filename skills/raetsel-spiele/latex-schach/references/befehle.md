# Befehlsreferenz skak / xskak / chessboard

Alle Einträge sind mit TeX Live 2023 getestet, sofern nicht anders vermerkt.

## Partien (xskak)

| Befehl | Wirkung |
|---|---|
| `\newchessgame` | neue Partie in Grundstellung |
| `\newchessgame[id=A]` | Partie unter einem Namen speichern (mehrere Partien parallel) |
| `\newchessgame[setfen={FEN}]` | Partie aus einer Stellung beginnen |
| `\mainline{1. e4 e5}` | Züge ausführen und fett drucken |
| `\hidemoves{1. e4 e5}` | Züge ausführen, nichts drucken |
| `\variation{1... c5}` | Variante drucken, Stellung bleibt unverändert |
| `\xskakset{id=A, moveid=3w}` `\chessboard[setfen=\xskakget{nextfen}]` | Stellung der Partie A **nach** dem 3. Zug von Weiß (`3b` = Schwarz) |
| `\xskakset{id=A, moveid=3w}` `\chessboard[setfen=\xskakget{pastfen}]` | Stellung **vor** diesem Zug |
| `\xskakset{moveid=3w}\xskakget{san}` | Daten zu einem Zug abrufen: `san` (Rfe1+), `lan` (e2–e4), `movenr`, `player` (w/b), `nextfen` (FEN danach), `pastfen` (FEN davor). Ohne `moveid` bezieht sich `\xskakget` nicht auf den letzten Zug! |

Zug von Schwarz am Anfang: `1... e5` (drei Punkte). Rochade `O-O` / `O-O-O`,
Umwandlung `e8=Q`, Schach `+`, Matt `#`, Schlagen `x`, Doppeldeutigkeit
`Nbd2` / `R1e1`. Bewertungszeichen direkt am Zug: `e4!`, `e5?`, `Nf3!?`, `Nc6?!`.

## Bretter (chessboard)

| Option | Wirkung |
|---|---|
| `tinyboard`, `smallboard`, `normalboard`, `largeboard` | Größe |
| `boardfontsize=15pt` | Größe frei wählen |
| `showmover=false` | Anzeige „wer ist am Zug“ ausblenden |
| `label=false` | Koordinaten a–h / 1–8 ausblenden |
| `inverse` | Brett aus Sicht von Schwarz |
| `printarea=a1-d4` | nur einen Ausschnitt zeigen |
| `setfen={FEN}` | Stellung aus FEN |
| `setpieces={Ke1,ke8,Pa2}` | nur diese Figuren (Rest leer); `setpieces={}` = leeres Brett |
| `addpieces={Nf3}` | Figuren zur aktuellen Stellung hinzufügen |
| `clearfields={e2,d2}` | Felder leeren |
| `\setchessboard{smallboard, showmover=false}` | Voreinstellung für alle folgenden Bretter |

## Markierungen

Erst den Stil wählen (`pgfstyle=…`), dann Farbe (`color=…`), dann die Felder
oder Züge. Mehrere Markierungen hintereinander in einem `\chessboard[...]`
sind erlaubt.

| Stil | dann | Ergebnis |
|---|---|---|
| `pgfstyle=straightmove` | `markmoves={d1-d8}` | gerader Pfeil |
| `pgfstyle=curvemove` | `markmoves={d4-a7}` | gebogener Pfeil |
| `pgfstyle=knightmove` | `markmoves={g1-f3}` | geschwungener Pfeil für Springerzüge |
| `pgfstyle=circle` | `markfields={g8}` | Kreis um ein Feld |
| `pgfstyle=cross` | `markfields={a1}` | Kreuz auf einem Feld |
| `pgfstyle=border` | `markfields={h8}` | farbiger Rahmen um ein Feld |
| `pgfstyle=color` | `colorbackfields={e4,d5}` | Feld einfärben |
| `pgfstyle=color, opacity=0.45` | `markfields={g2,a2}` | Feld halbtransparent **über** den Figuren einfärben |
| `pgfstyle=text, text=\bfseries X` | `markfield={h8}` | Text auf ein Feld |

Feinschliff für Pfeile und Markierungen (gilt jeweils für alles, was danach
im selben `\chessboard[...]` steht):

| Option | Wirkung |
|---|---|
| `linewidth=0.09em` | Strichstärke der Pfeile und Rahmen |
| `shortenend=0.35em` | Pfeil endet vor der Feldmitte – die Spitze verschwindet nicht hinter der Figur |
| `shortenstart=0.2em` | Pfeil beginnt später |
| `opacity=0.45` | Deckkraft (danach mit `opacity=1` zurücksetzen) |

Zug und Antwort in einem Brett (grün = Weiß, rot = Schwarz):
```latex
\chessboard[smallboard, showmover=false, setfen={6k1/5ppp/8/8/8/8/5PPP/3R2K1 w - - 0 1},
  linewidth=0.09em, shortenend=0.35em,
  pgfstyle=straightmove, color=akzentgruen, markmoves={d1-d8},
  pgfstyle=border, color=akzentrot, markfields={g8}]
```

Beispiel (Springerzüge zeigen):
```latex
\chessboard[smallboard, showmover=false, setpieces={Ne4},
  pgfstyle=circle, color=green, markfields={c3,c5,d2,d6,f2,f6,g3,g5}]
```

## Farbiges Brett

Mit den universalen Stildateien sind alle Bretter farbig (Schema `blau`).
Umschalten in der Präambel oder mitten im Dokument – gilt für alle folgenden
Bretter:

| Befehl | Aussehen |
|---|---|
| `\schachbrettfarben{blau}` | hellblau / graublau (Standard) |
| `\schachbrettfarben{braun}` | klassisches Holzbrett |
| `\schachbrettfarben{gruen}` | grünes Turnierbrett |
| `\schachbrettfarben{grau}` | hellgrau / grau, für Schwarz-Weiß-Druck |
| `\schachbrettfarben{klassisch}` | schraffierte Felder wie in skak ohne Farbe |

`\schachbrettfarben` setzt die Voreinstellungen von `\setchessboard` zurück.
Eigene Voreinstellungen (`\setchessboard{smallboard, showmover=false}`)
deshalb **danach** schreiben.

Start- und Zielfeld eines Zuges hervorheben (liegt über dem Feld, unter der Figur):
```latex
\chessboard[smallboard, setfen={6k1/5ppp/8/8/8/8/5PPP/3R2K1 w - - 0 1},
  pgfstyle=color, color=brettmarke, colorbackfields={d1,d8},
  pgfstyle=straightmove, color=akzentgruen, markmoves={d1-d8}]
```

Eigene Farben: `\definecolor{brettrothell}{HTML}{...}` und
`\definecolor{brettrotdunkel}{HTML}{...}` anlegen, dann wirkt
`\schachbrettfarben{rot}` (der Name wird zu `brett<Name>hell` / `brett<Name>dunkel`).

**Hintergrund.** Die Standardschrift von skak schraffiert die dunklen Felder;
Figur und Schraffur sind dort **ein** Zeichen und lassen sich nicht getrennt
einfärben (`blackfieldcolor` färbt auch die Figuren auf dunklen Feldern).
`\schachbrettfarben` nimmt deshalb die Schrift `skaknew` in der Kodierung
`LSBC5`, die nur die Figuren zeichnet (weiße Figuren weiß gefüllt), und lässt
chessboard die Felder als Flächen darunter malen.

**Ohne die universalen Stildateien** (eigenständiges Dokument) dasselbe von Hand:
```latex
\usepackage[LSBC5,T1]{fontenc}   % Kodierung laden, T1 bleibt Standard
\usepackage{xcolor}
\usepackage{xskak}
\usepackage{chessboard}
\definecolor{bretthell}{HTML}{F0D9B5}
\definecolor{brettdunkel}{HTML}{B58863}
\setchessboard{boardfontfamily=skaknew, boardfontencoding=LSBC5,
  piececolor=black, piecemaskcolor=white, setfontcolors,   % setfontcolors NACH den Farben
  pgfstyle=color, color=bretthell, colorbackboard,         % alle Felder hell
  color=brettdunkel, colorblackbackfields,                 % dunkle Felder darüber
  color=black, labelfont=\sffamily\color{black!65}}
```
Fehlt die `fontenc`-Zeile, bricht LaTeX mit „Encoding scheme LSBC5 unknown“ ab.
Steht `setfontcolors` vor den Farbangaben, werden sie nicht übernommen.
Die Kodierungen `LSBC2` bis `LSBC4` zeichnen die Felder selbst (Farben dann
über `whitefieldmaskcolor` / `blackfieldmaskcolor`); dort verschwinden
`colorbackfields`-Markierungen unter der Feldfläche. `LSBC1` behält die Schraffur.
Im Fließtext (`\mainline`, `\symknight`) ändert sich durch all das nichts.

Fertiges Beispiel: `assets/vorlage_matt_in_n_loesung.tex`.

## Figuren und Kommentarzeichen im Text

| Befehl | Zeichen |
|---|---|
| `\symking` `\symqueen` `\symrook` `\symbishop` `\symknight` `\sympawn` | Figurensymbole |
| `\wbetter` / `\bbetter` | Weiß / Schwarz steht etwas besser |
| `\wupperhand` / `\bupperhand` | Weiß / Schwarz steht deutlich besser |
| `\wdecisive` / `\bdecisive` | Weiß / Schwarz steht auf Gewinn |
| `\equal` | ausgeglichen |
| `\unclear` | unklar |
| `\compensation` | Kompensation |
| `\withidea` | mit der Idee |
| `\onlymove` | einziger Zug |
| `\novelty` | Neuerung |
| `\zugzwang` | Zugzwang |
| `\bishoppair` | Läuferpaar |
| `\passedpawn` | Freibauer |
| `\centre`, `\kside`, `\qside` | Zentrum, Königs-, Damenflügel |
| `\attack`, `\initiative`, `\counterplay` | Angriff, Initiative, Gegenspiel |
| `\betteris` | besser ist |

## Was es nicht gibt (häufige Fehlannahmen)

`\textmove`, `\wwinning` (heißt `\wdecisive`), `emptyboard`,
`arrowheadstyle` – führen zu „Undefined control sequence“ bzw. xkeyval-Fehlern.

`\chessboard[id=A, moveid=3w]` wählt **keine** Stellung aus: Die Schlüssel werden
ohne Fehlermeldung übergangen, und es erscheint die letzte Stellung der Partie.
Richtig: erst `\xskakset{id=A, moveid=3w}`, dann `setfen=\xskakget{nextfen}`.
