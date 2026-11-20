---
name: unterrichtsmaterial-ablage
description: Unterrichtsmaterial (Arbeitsblätter, Leistungskontrollen, Klassenarbeiten mit Lösungen) nach dem Erstellen oder Ändern immer dreifach ablegen – im lokalen Ordner der Lehrkraft, in einem privaten Git-Repository und in einem Cloud-Ordner (z. B. Google Drive), jeweils als .tex und .pdf im selben Themenordner. Verwende diesen Skill immer, wenn Material für den Unterricht entsteht, verschoben oder überarbeitet wird.
---

# Dreifach-Ablage für Unterrichtsmaterial

Jedes neue oder geänderte Material liegt danach **gleichzeitig** an drei Orten,
jeweils mit `.tex` **und** `.pdf` im selben Themenordner:

1. **lokaler Ordner** auf dem Rechner der Lehrkraft (Arbeitsstand, Druck)
2. **privates Git-Repository** (Versionen, Sicherung, Zugriff für Claude)
3. **Cloud-Ordner**, z. B. Google Drive (Zugriff von Schule und Handy)

Die drei Orte haben dieselbe Ordnerstruktur. Das Repository bleibt **privat**:
Schulbuchaufgaben und fremde Materialien dürfen nicht öffentlich werden.

## Konfiguration (einmal festlegen)

Diese Angaben trägt die Lehrkraft in ihre eigene Kopie des Skills ein:

| Angabe | Beispiel |
|---|---|
| lokaler Ordner | `~/Dokumente/LaTeX/Arbeitsblätter` |
| Repository | `<konto>/unterrichtsmaterial`, Branch `main` |
| Cloud-Ordner | Drive-Ordner „Arbeitsblätter“ mit seiner Ordner-ID |
| Ordner, die **nicht** angefasst werden | z. B. ein alter Drive-Ordner |

## Ordnerstruktur

```
Arbeitsblätter/
├── header.tex, newcommands.tex, CLAUDE.md
├── Stile/                         verbindliche Stildateien
├── Mathematik/Klasse 7/LB 2 - Terme und Gleichungen/<Thema>/<Thema>.tex + .pdf
├── Mathematik/Jg 11-12/LB 1 - Differentialrechnung/<Thema>/…
└── Informatik/…
```

Dokumente binden die Stildateien relativ ein (`\input{../../../../header.tex}`,
Tiefe je nach Ordner). Persönliche Dateien (Sitzpläne, Noten, Namenslisten)
gehören weder ins Repository noch in die Cloud.

## Ablauf

1. **Fertig bauen:** zweimal kompilieren, Hilfsdateien (`aux`, `log`, `out`)
   löschen, Seiten als PNG rendern und ansehen, Rechenergebnisse nachrechnen.
2. **Repository:** Dateien an den Zielort, `git add`, Commit, `git push`.
3. **Cloud:** Zielordner suchen, fehlende Ordner anlegen, `.tex` und `.pdf`
   ohne Umwandlung in Google-Formate hochladen. Google Drive überschreibt
   keine Dateien: bei Änderungen die alte Fassung in den Papierkorb, dann die
   neue hochladen.
4. **Lokaler Ordner:** Dateien schreiben; bei vielen Dateien ein `tar.gz`
   übertragen und dort entpacken. Verschobenes Material am alten Ort entfernen.
   Ist der Rechner gerade nicht erreichbar, zuerst Repository und Cloud
   erledigen und den lokalen Ordner später nachziehen.
5. **Melden:** kurz sagen, dass alle drei Orte auf demselben Stand sind –
   oder was noch fehlt.
