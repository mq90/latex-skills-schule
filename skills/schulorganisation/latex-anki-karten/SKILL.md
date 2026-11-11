---
name: latex-anki-karten
description: Anki-Karteikarten (.apkg) aus einfachen Listen bauen – Vokabeln, Begriffe und Formeln aus CSV (MathJax, Bilder, Rückrichtung), Multiple-Choice-Fragen aus einer Textdatei, daraus zusätzlich ein LaTeX-Papiertest mit Lösungsteil und ein QTI-2.1-Paket für Testsysteme wie ONYX. Verwende diesen Skill immer, wenn jemand Karteikarten, Anki-Stapel, Vokabeltrainer, Lernkarten, Multiple-Choice-Fragen, BLF- oder Abiturtraining, einen MC-Test oder QTI-Export erstellen will.
---

# Anki-Karteikarten

`scripts/anki_karten.py` schreibt fertige Anki-Stapel (Doppelklick → in Anki,
AnkiDroid, AnkiMobile). Python ≥ 3.11 und `pip install genanki`.

```bash
python3 scripts/anki_karten.py vokabeln assets/englisch_beispiel.csv --deck "Englisch::Unit 3" --rueckrichtung
python3 scripts/anki_karten.py vokabeln assets/mathe_formeln.csv --deck "Mathematik::Formeln"
python3 scripts/anki_karten.py vokabeln assets/bundeslaender.csv --deck "Geografie::Bundesländer" --bilder assets/bilder
python3 scripts/anki_karten.py mc assets/fragen_blf_mathe.txt --deck "Mathematik::BLF" --mischen --pdf --qti --titel "…"
pdflatex fragen_blf_mathe.tex      # Papiertest mit Lösungsteil
```
Alle vier Aufrufe getestet (15×2, 8, 16 mit 16 Bildern, 10 Fragen).

## Formate

- **CSV:** `Vorderseite;Rückseite;Zusatz;Tags` (Trennzeichen `;`, `,` oder Tab; erste Zeile = Überschrift).
  Formeln in `$…$` (MathJax), Bilder mit `[bild:sh.png]` + `--bilder Ordner`.
- **Multiple Choice** (Textdatei, Leerzeile trennt Fragen, `%` = Kommentar):
  ```
  ? Frage (Folgezeilen gehören dazu)
  + richtige Antwort        (mehrere + = Mehrfachauswahl)
  - falsche Antwort
  > Erklärung (optional)
  @ tags (optional)
  ```
- Erneuter Import aktualisiert Karten (Schlüssel = Vorderseite), Lernfortschritt bleibt.

## Dateien (`assets/`)

`englisch_beispiel.csv`, `mathe_formeln.csv`, `bundeslaender.csv` mit `bilder/*.png`,
`fragen_blf_mathe.txt` (10 BLF-Fragen), `fragen_blf_mathe.tex` (erzeugter Test),
`vorlage_bundeslaender_bilder.tex` (erzeugt die 16 Bilder; braucht
`deutschland_daten.tex` aus `latex-geodaten-karten/assets`).
Erzeugte `.apkg` und `*_qti21.zip` stehen in `.gitignore`.

## Hinweise

- QTI-Import in ONYX noch **nicht getestet**; Formeln kommen dort als LaTeX-Text an, Bilder nicht.
- Keine personenbezogenen Daten in Fragen oder Prompts.

## Handreichung

`references/handreichung_anki_karten.tex` (PDF in `handreichungen/`):
Einrichten, CSV-Karten mit Formeln und Bildern (Kartenvorschau), Multiple
Choice mit Format-Tabelle, Papiertest (eingebundene Seiten), QTI, KI-Prompt,
alle Optionen.
