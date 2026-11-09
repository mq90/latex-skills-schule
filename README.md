# latex-skills-schule

Skills für Claude rund um LaTeX im Schulalltag: Arbeitsblätter, Rätsel,
Karten und Handreichungen – mit getesteten Vorlagen, Befehlsreferenzen und
Hilfsskripten.

Ein **Skill** ist ein Ordner mit einer `SKILL.md` (wann und wie Claude ihn
benutzt) und Begleitdateien. Claude lädt einen Skill nur, wenn er zur Anfrage
passt – deshalb ist jedes Thema ein eigener Skill.

## Enthaltene Skills

| Skill | Wofür | Extras |
|---|---|---|
| [`latex-sudoku`](skills/latex-sudoku) | Sudoku-Arbeitsblätter mit Lösungsseite | Generator mit garantiert eindeutiger Lösung, drei Stufen |
| [`latex-schach`](skills/latex-schach) | Schachbretter, Partien, Mattaufgaben (skak, xskak, chessboard) | Prüfskript für FEN und Matt-in-N, Befehlsreferenz |
| [`latex-tikzpeople`](skills/latex-tikzpeople) | Personen-Figuren und Szenen (Alice, Bob, Eve …) | Galerie, Kryptografie-Vorlage |
| [`latex-lautschrift`](skills/latex-lautschrift) | IPA-Lautschrift mit tipa oder Unicode | Lösung für den babel-Konflikt, Lauttabellen, Vokalviereck |
| [`latex-geodaten-karten`](skills/latex-geodaten-karten) | echte Landkarten aus freien Geodaten | `geo2tikz.py` (Projektion, Vereinfachung, Zuschnitt) |

Alle Skills enthalten außerdem `assets/stil_handreichung.tex`, den gemeinsamen
Stil für Handreichungen (Farben, Merke-/Achtung-/Tipp-Kästen, Beispiel-Kästen
mit Code links und Ergebnis rechts). Die Hauptfassung liegt in
[`shared/`](shared/stil_handreichung.tex); bei Änderungen in alle Skills kopieren.

## Installieren

- **claude.ai / Claude-App:** den Ordner eines Skills als ZIP packen (der Ordner
  selbst muss im ZIP liegen, nicht nur sein Inhalt) und in den Einstellungen
  unter Skills hochladen.
- **Claude Code:** den Skill-Ordner nach `~/.claude/skills/` kopieren.

## Voraussetzungen

- TeX Live mit `texlive-games` (Schach, Sudoku), `texlive-plain-generic`
  (für skak), `texlive-pictures` (tikzpeople), `texlive-lang-german`,
  für Unicode-Lautschrift `texlive-xetex` und die Schrift Charis SIL
- Python 3; je nach Skill `pip install chess` bzw. `pip install shapely pyproj`

## Grundsätze

- Jedes Code-Beispiel ist kompiliert und das Ergebnis angesehen worden.
- Stolpersteine stehen in jeder `SKILL.md` mit der echten Fehlermeldung.
- Rätsel (Sudoku, Schach) werden maschinell auf eindeutige Lösbarkeit geprüft.
- Fremde Daten (Geodaten) liegen nicht im Repo; die Skills erklären, woher
  man sie lädt und welche Lizenz gilt.

## Farben anpassen

Die Farben stehen zentral in `stil_handreichung.tex` (`hrblau`, `hrrot`,
`hrgruen`, `hrlila`, `hrorange`; „hr“ = Handreichung). Wer Schul- oder
Hausfarben möchte, ändert nur die HTML-Werte dort.

## Lizenz

Skripte (`*.py`): MIT. Alle übrigen Inhalte: CC BY 4.0 –
Namensnennung „latex-skills-schule von Martin Quandt“. Details in [LICENSE](LICENSE).
