---
name: latex-schach
description: Schachbretter, Partien, Stellungen und Schachrätsel in LaTeX setzen – mit skak, xskak und chessboard, inklusive FEN, Pfeilen, farbigen Feldern, Kommentarzeichen und einem Prüfskript für Matt-in-N-Aufgaben. Verwende diesen Skill immer, wenn jemand ein Schach-Arbeitsblatt, Mattaufgaben, ein Schachbrett-Diagramm, eine Partie mit Notation, das Acht-Damen-Problem, Springerwege oder eine Handreichung zu skak/xskak/chessboard möchte – auch wenn LaTeX nicht ausdrücklich genannt wird.
---

# Schach mit LaTeX (skak, xskak, chessboard)

Drei Pakete arbeiten zusammen: **skak** (Figurenschrift, Züge ausführen),
**xskak** (Partien speichern, Stellungen nach beliebigem Zug abrufen; lädt skak
mit) und **chessboard** (Bretter, Ausschnitte, Markierungen).
In die Präambel gehören immer:

```latex
\usepackage{xskak}
\usepackage{chessboard}
```

Benötigte TeX-Pakete (Debian/Ubuntu): `texlive-games`, `texlive-plain-generic`
(enthält `lambda.sty`, ohne das skak nicht lädt).

## Arbeitsablauf für Rätsel und Stellungen

1. Stellungen als FEN aufschreiben (oder auf lichess.org/editor zusammenklicken).
2. **Jede Stellung prüfen**, bevor sie aufs Blatt kommt:
   ```bash
   pip install chess
   python3 scripts/pruefe_stellung.py "6k1/5ppp/8/8/8/8/5PPP/3R2K1 w - - 0 1"
   python3 scripts/pruefe_stellung.py --matt 2 --datei stellungen.txt
   ```
   Das Skript meldet illegale Stellungen (z. B. Schwarz steht im Schach, aber
   Weiß ist am Zug) und ob es genau **einen** Lösungszug gibt. Ausgedachte
   Mattaufgaben haben erstaunlich oft eine zweite Lösung – nur „eindeutig“ nehmen.
3. Vorlage `assets/vorlage_matt_in_eins.tex` anpassen (vier Bretter, Lösungen
   unten), mit `pdflatex` kompilieren, als Bild ansehen.

## Wichtigste Befehle

```latex
\newchessgame                         % neue Partie, Grundstellung
\mainline{1. e4 e5 2. Nf3 Nc6 3. Bb5} % Züge ausführen UND drucken
\hidemoves{1. d4 d5 2. c4}            % ausführen, nicht drucken
\variation{2... e6}                   % Nebenvariante drucken (ändert nichts)
\chessboard                           % aktuelle Stellung zeichnen
\chessboard[setfen={r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3}]
\chessboard[setpieces={Kg1,Qd1,kg8,ph7}]   % groß = Weiß, klein = Schwarz
\newchessgame[id=A] ... \chessboard[id=A, moveid=2b]  % Stellung nach 2... (Schwarz)
\xskakset{moveid=3w}\xskakget{san}  % Daten zu einem bestimmten Zug abrufen
\symking \symqueen \symrook \symbishop \symknight \sympawn  % Figur im Fließtext
```

Ausführliche Liste der Brett-Optionen und Kommentarzeichen:
`references/befehle.md` – lesen, sobald Markierungen, Ausschnitte oder
Bewertungssymbole gebraucht werden.

## Stolpersteine (getestet)

- **Englische Buchstaben eingeben:** K, Q (Dame), R (Turm), B (Läufer),
  N (Springer). Gedruckt werden ohnehin Figurensymbole, die Ausgabe ist also
  sprachneutral. `\skaklanguage[german]` bricht mit „Argument of
  \skak@pieceToEnglish has an extra }“ ab. `\newchessgame[language=german]`
  liest zwar `Sf3`, druckt die Züge aber kaputt („ZZSf3“). Deshalb: englisch.
- **FEN ist immer englisch**, Bauer = `P`/`p`, Läufer = `B`/`b`.
- **skak prüft jeden Zug.** Ein Fehler bei `\mainline` heißt fast immer: Tippfehler
  oder Zug passt nicht zur Stellung. Zugnummern müssen zur Partie passen
  (`\hidemoves{1. d4}` mitten in einer Partie bei Zug 3 → Fehler).
- **Zugnummern ohne Punkt** („1 e4 e5 2 ♘f3“) sind skaks Standardstil, kein Fehler.
- **Beispiel-Kästen:** Schachbefehle laufen in den `beispiel`-Kästen der
  Stildatei (Code links, Ergebnis rechts), aber nur mit der aktuellen
  `stil_handreichung.tex`. Ältere Fassungen mit `\newtcblisting{beispiel}[1][…]`
  verschlucken den ersten Befehl nach `\begin{beispiel}` – Symptom:
  „Paragraph ended before \FenBoard was complete“.
- `\chessboard` ohne `setfen` zeigt die Stellung **nach dem letzten**
  `\mainline`/`\hidemoves`.
- Das kleine Quadrat neben dem Brett zeigt, wer am Zug ist:
  `showmover=false` blendet es aus.
- Optionen `arrowheadstyle` und `emptyboard` gibt es nicht. Leeres Brett:
  `setpieces={}`.

## Für eine Handreichung

`assets/stil_handreichung.tex` daneben legen und mit `\input{stil_handreichung}`
einbinden (Farben, `merke`/`hinweis`/`tipp`-Kästen, `\befehl{}`, `\opt{}`,
`\Titel{}{}`). Jedes Beispiel kompilieren und das PDF als Bild prüfen.

## Ideen für den Unterricht

- **Mathematik:** Koordinatensystem am Brett (Felder benennen, Klasse 5/6),
  Springerwege und Graphen, Weizenkornlegende (Potenzen von 2).
- **Informatik:** Acht-Damen-Problem mit Backtracking, FEN als Datenformat
  (Codierung einer Stellung als Zeichenkette), Zuggenerator als Projekt.
- **Rätsel/Vertretung:** Matt in 1 / Matt in 2, gegliedert nach Motiven
  (Grundreihe, ersticktes Matt, Schäfermatt).
