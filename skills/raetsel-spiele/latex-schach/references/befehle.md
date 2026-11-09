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
| `\chessboard[id=A, moveid=3w]` | Stellung der Partie A nach dem 3. Zug von Weiß (`3b` = Schwarz) |
| `\xskakset{moveid=3w}\xskakget{san}` | Daten zu einem Zug abrufen: `san` (Rfe1+), `lan` (e2–e4), `movenr`, `player` (w/b), `nextfen` (FEN danach). Ohne `moveid` bezieht sich `\xskakget` nicht auf den letzten Zug! |

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
| `pgfstyle=circle` | `markfields={g8}` | Kreis um ein Feld |
| `pgfstyle=cross` | `markfields={a1}` | Kreuz auf einem Feld |
| `pgfstyle=color` | `colorbackfields={e4,d5}` | Feld einfärben |
| `pgfstyle=text, text=\bfseries X` | `markfield={h8}` | Text auf ein Feld |

Beispiel (Springerzüge zeigen):
```latex
\chessboard[smallboard, showmover=false, setpieces={Ne4},
  pgfstyle=circle, color=green, markfields={c3,c5,d2,d6,f2,f6,g3,g5}]
```

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
