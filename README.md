# latex-skills-schule

Skills für Claude rund um LaTeX im Schulalltag: Arbeitsblätter,
Leistungskontrollen, Handreichungen, Grafiken und Rätsel – mit einer
universalen `header.tex`/`newcommands.tex`, getesteten Vorlagen,
Befehlsreferenzen und Hilfsskripten. Alles mit **pdflatex** und reinem
**TikZ** (kein pgfplots).

Ein **Skill** ist ein Ordner mit einer `SKILL.md` (wann und wie Claude ihn
benutzt) und Begleitdateien. Claude lädt nur den Skill, der zur Anfrage
passt – deshalb ist jedes Thema ein eigener Skill.

## Aufbau

```
skills/
├── grundlagen/        Grundstil, LaTeX- und TikZ-Grundlagen, Multiple-Choice
├── mathematik/        Funktionsgraphen, Geometrie, Stochastik, Venn-Diagramme
├── informatik/        Automaten, Schaltungen, Programmablaufpläne, UML, Quellcode
├── sprache-musik/     Lautschrift (IPA), Notensatz (MusiXTeX)
├── illustration/      tikzpeople-Figuren, Sprechblasen
├── geografie/         Landkarten aus Geodaten
└── raetsel-spiele/    Sudoku, Schach
werkzeuge/             Prüf- und Hilfsskripte für das Repository
```

## Die Skills

| Bereich | Skill | Wofür | Extras |
|---|---|---|---|
| Grundlagen | [`latex-grundstil`](skills/grundlagen/latex-grundstil) | **Basis für alle anderen**: header/newcommands-System, Regeln für Arbeitsblätter, Lösungsteil, Handreichungen | universale `header.tex` + `newcommands.tex`, Vorlage Handreichung, Mathe-AB-Regeln, Aufgabentypen |
| | [`latex-grundlagen`](skills/grundlagen/latex-grundlagen) | Präambel, Formelsatz, Tabellen, eigene Befehle | 4 Nachschlagewerke |
| | [`latex-tikz-grundlagen`](skills/grundlagen/latex-tikz-grundlagen) | Zeichnen mit TikZ allgemein | Nachschlagewerk + Handreichung |
| | [`latex-multiple-choice`](skills/grundlagen/latex-multiple-choice) | Ankreuzaufgaben horizontal/vertikal | Handreichung |
| Mathematik | [`latex-funktionsgraphen`](skills/mathematik/latex-funktionsgraphen) | Koordinatensysteme und Graphen im festen Stil | `\koordinatensystem`, 13 Vorlagen |
| | [`latex-geometrie`](skills/mathematik/latex-geometrie) | Dreiecke, Winkel, Konstruktionen, Körper | 14 Vorlagen |
| | [`latex-stochastik-diagramme`](skills/mathematik/latex-stochastik-diagramme) | Baumdiagramme, Vierfeldertafeln, Binomialverteilungen | Stil `baumdiagramm`, Skript für Säulendiagramme |
| | [`latex-venn-diagramme`](skills/mathematik/latex-venn-diagramme) | Mengen und Mengenoperationen | Handreichung |
| Informatik | [`latex-automaten`](skills/informatik/latex-automaten) | endliche Automaten | Handreichung |
| | [`latex-digitale-schaltungen`](skills/informatik/latex-digitale-schaltungen) | Logikgatter, Halbaddierer | Handreichung |
| | [`latex-programmablaufplaene`](skills/informatik/latex-programmablaufplaene) | PAP/Flussdiagramme | Stile `input`, `operation`, `condition`, `output` |
| | [`latex-uml-klassendiagramme`](skills/informatik/latex-uml-klassendiagramme) | Klassen und Beziehungen | Stile `umlclass`, `inherit` … |
| | [`latex-quellcode-listings`](skills/informatik/latex-quellcode-listings) | Programmcode mit listings | Handreichung |
| Sprache & Musik | [`latex-lautschrift`](skills/sprache-musik/latex-lautschrift) | IPA mit tipa oder Unicode | Lauttabellen, Vokalviereck |
| | [`latex-musixtex`](skills/sprache-musik/latex-musixtex) | Notensatz | Musik-Kürzel |
| Illustration | [`latex-tikzpeople`](skills/illustration/latex-tikzpeople) | Personen-Figuren, Alice/Bob/Eve | Galerie |
| | [`latex-sprechblasen`](skills/illustration/latex-sprechblasen) | Sprech- und Gedankenblasen | `\lehrerblase`, `\schuelerblase` |
| Geografie | [`latex-geodaten-karten`](skills/geografie/latex-geodaten-karten) | echte Karten aus freien Geodaten | `geo2tikz.py` |
| Rätsel & Spiele | [`latex-sudoku`](skills/raetsel-spiele/latex-sudoku) | Sudoku-Arbeitsblätter | Generator mit eindeutiger Lösung |
| | [`latex-schach`](skills/raetsel-spiele/latex-schach) | Bretter, Partien, Mattaufgaben | Prüfskript für FEN |

## Die universalen Stildateien

`skills/grundlagen/latex-grundstil/assets/header.tex` und `newcommands.tex`
enthalten **alles**, was die Skills brauchen: alle Pakete und
TikZ-Bibliotheken, alle Befehle, Boxen und Stile. Jedes Dokument beginnt mit

```latex
\input{../../../../header.tex}      % Pfad je nach Ordnertiefe
\input{../../../../newcommands.tex}
```

Neue Pakete oder Befehle kommen immer dort hinein, nicht ins Dokument, und
werden oben in der Datei im Änderungsprotokoll vermerkt. Ausnahme:
`musixtex` (definiert `\cup` um) wird nur in Musik-Dokumenten geladen.

Die Liste aller Befehle steht in
[`makros.md`](skills/grundlagen/latex-grundstil/references/makros.md).

## Handreichungen

Alle Handreichungen haben denselben Aufbau: Titel, Autor, Datum,
einleitender Absatz, Kapitel vom Einfachen zum Komplexen, Zusammenfassung.
Jedes Beispiel steht erst als Code (gelber Kasten, `style=latex`) und
**direkt darunter** als Ausgabe (blauer Kasten `ausgabe`). Die Dateien in
den `references/`-Ordnern sind vollständige Handreichungen und zugleich die
Vorlagen-Sammlung für Claude.

## Installieren

- **claude.ai / Claude-App:** den Ordner eines Skills als ZIP packen (der
  Ordner selbst muss im ZIP liegen) und in den Einstellungen unter Skills
  hochladen. **`latex-grundstil` immer mit installieren** – die anderen
  Skills bauen darauf auf.
- **Claude Code:** die Skill-Ordner nach `~/.claude/skills/` kopieren.

## Werkzeuge

| Skript | Zweck |
|---|---|
| `werkzeuge/alles_kompilieren.py` | kompiliert jede Vorlage, jede Handreichung und jedes Code-Beispiel aus den SKILL.md-Dateien gegen die universalen Stildateien; `--pdf ordner` sammelt die PDFs |
| `werkzeuge/makros_auflisten.py` | erzeugt `makros.md` neu aus header/newcommands |

Nach jeder Änderung an `header.tex` oder `newcommands.tex` beide Skripte
ausführen.

## Voraussetzungen

- TeX Live mit `texlive-latex-extra`, `texlive-pictures`, `texlive-science`,
  `texlive-games`, `texlive-plain-generic`, `texlive-fonts-extra`,
  `texlive-lang-german`, `texlive-music`; für Unicode-Lautschrift
  `texlive-xetex` und die Schrift Charis SIL
- Python 3; je nach Skill `pip install chess` bzw. `pip install shapely pyproj`

## Grundsätze

- Jedes Code-Beispiel ist kompiliert und das Ergebnis angesehen worden.
- Stolpersteine stehen in jeder `SKILL.md` mit der echten Fehlermeldung.
- Rätsel werden maschinell auf eindeutige Lösbarkeit geprüft, Wahrscheinlichkeiten
  exakt berechnet statt in TikZ.
- Fremde Daten (Geodaten) liegen nicht im Repository.

## Lizenz

Skripte (`*.py`): MIT. Alle übrigen Inhalte: CC BY 4.0 –
Namensnennung „latex-skills-schule von Martin Quandt“. Details in [LICENSE](LICENSE).
