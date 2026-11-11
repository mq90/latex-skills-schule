---
name: latex-stoffverteilungsplan
description: Stoffverteilungspläne automatisch erstellen – ein Python-Skript verteilt Lernbereiche strikt nach Unterrichtsstunden auf die echten Termine jeder Klasse (Ferien und Feiertage Sachsen, A/B-Wochen, Klassenfahrten, Prüfungszeiträume als Puffer, Übergabelinie, Wahlbereich) und schreibt einen LaTeX-Plan mit Teil A, Halbjahresübersicht und Teil B. Verwende diesen Skill immer, wenn jemand einen Stoffverteilungsplan, Jahresplan, Unterrichtsplan mit Datum, eine Halbjahresplanung oder Terminplanung für Klassen erstellen oder aktualisieren will.
---

# Stoffverteilungsplan

Eine TOML-Datei beschreibt Klassen, Termine, Sperren und Lernbereiche,
`scripts/stoffverteilungsplan.py` rechnet die Termine aus und schreibt
`plan_….tex`; `pdflatex` übersetzt. Python ≥ 3.11, keine Zusatzpakete.

```bash
python3 scripts/stoffverteilungsplan.py assets/plan_informatik10.toml   # schreibt plan_informatik10.tex
pdflatex plan_informatik10.tex
```
Die Bilanz im Terminal („0 Pflicht-Termine offen“) zeigt, ob alles passt.

## Dateien (`assets/`)

| Datei | Inhalt |
|---|---|
| `plan_informatik10.toml` | 4 Klassen, A/B-Wochen, Klassenfahrt (`ausfall`), Prüfungszeitraum (`puffer`), Übergabe zum Halbjahr |
| `plan_mathe_lk11.toml` | Kurs mit 2 wöchentlichen + 1 14-täglichen Doppelstunde (`woche = "B"`, `bemerkung`) |
| `ferien_sachsen_2026_27.toml` | Ferien und Feiertage Sachsen 2026/27 (`[[frei]]`, Eintrag ohne `bis` = ein Tag) |
| `plan_*.tex` | vom Skript erzeugte Beispielpläne (kompilieren direkt) |

## Eingabeformat (Kurzfassung)

```toml
[plan]        # titel, schuljahr, lehrkraft, schule, beginn, ende, uebergabe_am,
              # ferien, woche_bei_beginn = "A", ab_zaehlung = "schulwochen", ustd_pro_termin = 2
[[gruppe]]    # name = "10b"; termine = [ { tag = "Di", woche = "A"|"B"|"AB", zeit = "08:00–09:30" } ]
[[sperre]]    # grund, von, bis, modus = "ausfall"|"puffer", thema, nur = ["10b"]
[[lernbereich]]  # kurz, name, ustd, farbe = "akzentblau", themen = [ "…", { thema = "…", note = true } ]
                 # wahl = true: Wahlbereich füllt den Rest
```
Jedes Thema ist ein Termin; zu wenige Themen werden mit „Fortsetzung“ aufgefüllt.
Farben: Akzentfarben der universalen newcommands.tex (`akzentblau`, `akzentgruen`,
`akzentorange`, `akzentlila`, `akzentrot`).

## Bitte prüfen

- `woche_bei_beginn` muss zur Woche von `beginn` passen; A/B in den Ferien → `ab_zaehlung = "kalenderwochen"`.
- Titel und Ustd. der Lernbereiche sind Beispielwerte – mit dem Lehrplan abgleichen.
- 07.05.2027 (beweglicher Ferientag?) ist in der Ferien-Datei auskommentiert.
- Keine echten Namen von Lehrkräften oder Schulen in öffentliche Beispiele.

## Handreichung

`references/handreichung_stoffverteilungsplan.tex` (PDF in `handreichungen/`):
Prinzip, alle Blöcke der Eingabedatei, Ergebnis mit Seiten der erzeugten Pläne,
Rechenregeln, zweites Beispiel, KI-Prompt, Prüfliste. Die Seiten der Pläne
bindet die Handreichung als PDF ein; die Bauskripte kompilieren dafür
vorher `assets/plan_*.tex`.
