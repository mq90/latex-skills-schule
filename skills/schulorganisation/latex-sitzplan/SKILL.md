---
name: latex-sitzplan
description: Sitzpläne automatisch erstellen – Raum aus Reihen, Gruppentischen, U-Form oder einzelnen Tischen, Namen aus einer lokalen CSV per Zufall verteilt unter Regeln (nicht nebeneinander, nebeneinander, vorne, allein, fester Platz), Lehrer- und Klassensicht als LaTeX/PDF, leere Pläne zum Ausfüllen. Verwende diesen Skill immer, wenn jemand einen Sitzplan, eine Sitzordnung, einen Klassenraumplan oder eine neue Tischverteilung erstellen will. Schülernamen nie an eine KI geben.
---

# Sitzplan

`scripts/sitzplan.py` liest eine TOML-Datei (Raum, Anordnung, Regeln) und
eine CSV mit Namen und schreibt `sitzplan_….tex` (Querformat). Python ≥ 3.11.

```bash
python3 scripts/sitzplan.py assets/sitzplan_10b.toml   # 22 Namen, 24 Plätze, 0 Regelverstöße
pdflatex sitzplan_10b.tex
```

## Datenschutz (immer beachten)

Schülernamen, Fotos mit Schülern und Noten gehören nicht in eine KI. Die Namen
stehen in einer CSV **auf dem Rechner der Lehrkraft** (`Vorname;Nachname`),
das Skript setzt sie lokal ein. Claude baut nur Raum und Regeln; wenn Namen
gebraucht werden, mit Platzhaltern arbeiten und die Lehrkraft die CSV selbst
eintragen lassen. Beispiel-CSVs enthalten nur berühmte Mathematiker*innen.

## Dateien (`assets/`)

| Datei | Inhalt |
|---|---|
| `sitzplan_10b.toml` + `klasse_beispiel.csv` | Reihen 4×3 Tische à 2, alle Regeltypen, Lehrer- und Klassensicht |
| `sitzplan_u_form.toml` + `kurs_beispiel.csv` | U-Form 4/5/4, Reihenfolge wie CSV |
| `sitzplan_gruppen_leer.toml` | Gruppentische 2×3 à 4, ohne Namen (`csv = ""`) zum Ausfüllen |
| `sitzplan_*.tex` | vom Skript erzeugte Beispiele |

## Eingabeformat (Kurzfassung)

```toml
titel = "…"  stand = "…"
[raum]    # name, ansichten = ["lehrer","schueler"], tafelbreite, pult/fenster/tuer = "links"|"rechts"|""
[layout]  # typ = "reihen" (reihen, tische_pro_reihe, plaetze_pro_tisch)
          #     | "gruppen" (gruppen_reihen, gruppen_pro_reihe, plaetze_pro_gruppe = 4|6)
          #     | "u_form" (links, hinten, rechts)
[[tisch]] # x, y in cm (y = 0 an der Tafel), plaetze
[namen]   # csv, verteilung = "zufall"|"liste", seed
[regeln]  # nicht_neben = [[a,b]], neben = [[a,b]], vorne = [..], vorne_reihen, allein = [..]
[regeln.fest]  # "Vorname Nachname" = Platznummer
```

## Hinweise

- Namen in Regeln exakt wie in der CSV als `"Vorname Nachname"`.
- Unerfüllbare Regeln: Plan wird trotzdem geschrieben, mit rotem Hinweis.
- Neuer `seed` = neue Mischung, gleicher `seed` = gleicher Plan.

## Handreichung

`references/handreichung_sitzplan.tex` (PDF in `handreichungen/`): Prinzip,
Namensliste, Raum und Anordnungen, Regeln, Ergebnis (Lehrer-/Klassensicht,
U-Form, leerer Plan als eingebundene PDF-Seiten), KI-Prompt für Raumfotos
ohne Personen, Stolpersteine.
