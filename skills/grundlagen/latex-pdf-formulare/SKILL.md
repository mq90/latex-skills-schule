---
name: latex-pdf-formulare
description: Ausfüllbare PDFs (PDF-Formulare) mit LaTeX und hyperref – Textfelder, Ankreuzkästchen, Optionsfelder, Auswahllisten; digitale Leistungskontrollen und Arbeitsblätter, die Schülerinnen und Schüler am Tablet oder Laptop ausfüllen, speichern und über LernSax o. Ä. abgeben. Verwende diesen Skill immer, wenn ein Blatt „interaktiv“, „digital ausfüllbar“, „zum Ausfüllen am PC/iPad“ oder als „digitale LK“ werden soll, auch beim Umbau einer vorhandenen Papierfassung, und wenn ausgefüllte Abgaben eingesammelt oder ausgelesen werden sollen.
---

# Ausfüllbare PDF-Formulare

Setzt `latex-grundstil` voraus. `hyperref` steht in der universalen
`header.tex`, die Kurzbefehle `\feld`, `\zeichen`, `\kreuz`, `\antwort` und
das einheitliche Aussehen aller Felder in der `newcommands.tex` (Abschnitt
„Formularfelder“). Kein JavaScript, keine automatische Bewertung: Die
Lehrkraft liest jede Abgabe selbst.

## Grundgerüst

```latex
\input{header.tex}
\input{newcommands.tex}
\hypersetup{unicode=false}   % nötig für Optionsfelder (radio)

\begin{document}
\begin{Form}                 % EINE Form-Umgebung um den ganzen Inhalt

Name: \feld[6cm]{name} \hfill Klasse: \feld[2cm]{klasse} \hfill Datum: \feld[3cm]{datum}

\end{Form}
\end{document}
```

Vorlage für eine kurze digitale LK: `assets/vorlage_lk_digital.tex`.
Vollständiges Beispiel (Python-Grundlagen, Kl. 10, 20 P, eigenständiges
`scrartcl`-Dokument): `references/LK_Python_Grundlagen_digital.tex`.
Handreichung mit allen Feldtypen: `references/handreichung_pdf_formulare.tex`.

## Kurzbefehle (newcommands.tex)

| Papier | Digital | Befehl |
|---|---|---|
| Schreiblücke im Satz | einzeiliges Feld auf der Grundlinie | `\feld[Breite]{name}` (Standard 2,4 cm) |
| Kästchen für einen Buchstaben (E/V/A, Reihenfolge) | 1 Zeichen, zentriert | `\zeichen{name}` |
| `$\square$` / `\kasten` / `\casket` | Ankreuzkästchen | `\kreuz{name}` |
| Schreiblinien | mehrzeiliges Feld, volle Breite | `\antwort[Höhe]{name}` (Standard 3,2 cm ≈ 4 Linien) |

Weitere Feldtypen direkt aus hyperref:

```latex
% genau eine Antwort (Beschriftung steht VOR dem Knopf, default= leer = nichts gewählt)
\ChoiceMenu[radio, name=a7-typ, default=]{}{int=int, float=float, str=str}
% Auswahlliste: BEIDE Schlüssel combo und popdown
\ChoiceMenu[combo, popdown, name=a2-s1, width=1.6cm]{}{E,V,A}
% vorbelegter Text
\TextField[name=klasse, width=2cm, value={10b}]{}
```

## Feldnamen

- Schema nach Aufgaben: `name`, `klasse`, `datum`, `a2-s3`, `a4-1-r`/`a4-1-f`, `a5`, `z-1`.
- **Bindestrich, kein Unterstrich** – `_` wird entfernt (`a4_1_r` → `a41r`, getestet).
- **Jeder Name nur einmal.** Zwei Felder gleichen Namens sind in Chrome zwei
  getrennte Felder (getestet); andere Programme können sie zusammenlegen.

## Papier-LK digital umbauen

1. Lösungsteil heraus in eine eigene Datei (z. B. `qpdf alt.pdf --pages . 3 -- Loesungen.pdf`).
   Nie Lösungen ins Schülerdokument, auch nicht versteckt.
2. `\hypersetup{unicode=false}` (bzw. `[unicode=false]{hyperref}` bei eigenständigen
   Dokumenten) und `\begin{Form}…\end{Form}` um den Inhalt.
3. `\kasten` → `\kreuz{…}`, `\luecke`/`\rule` → `\feld{…}`, `\fbox` für Buchstaben →
   `\zeichen{…}`, `\linie\linie…` → `\antwort{…}`. Layout sonst unverändert lassen.
4. Kopf mit `\feld` für Name/Klasse/Datum. `\lk{…}{…}` setzt nur Text in die Kopfzeile, dort
   gibt es keine Felder.
5. Hinweiszeile unter den Titel: in die blauen Felder klicken, speichern, erneut öffnen, hochladen.
6. Prüfen: Felderzahl und Eindeutigkeit (PyMuPDF), Ausfüllen simulieren (unten), Rendern.

## Abgaben einsammeln

`scripts/antworten_einsammeln.py ordner/ [--aufgaben]` (braucht `pypdf`): eine CSV mit einer
Zeile pro Abgabe und einer Spalte pro Feld (Kästchen → `x`, Optionsfeld → Wert), mit
`--aufgaben` zusätzlich eine Textdatei mit allen Antworten je Aufgabe untereinander.
Unsichtbare Hilfsknöpfe `pbs@…` (kommen vom Paket `animate` aus der header.tex) werden
übersprungen.

## Testen ohne echtes Gerät

PDFium (Chrome/Edge) lässt sich mit `pypdfium2` fernsteuern: `pdf.init_forms()`, dann je
Feld `FORM_OnMouseMove` + `FORM_OnLButtonDown/Up` auf die Feldmitte (Koordinaten aus
PyMuPDF, y umrechnen: `Seitenhöhe − y`), Text mit `FORM_OnChar`, Auswahlliste mit
Pfeil-runter (`FORM_OnKeyDown 0x28`), **nach jedem Feld `FORM_ForceToKillFocus`** (sonst
gehen Klicks verloren), `pdf.save()`, Werte mit `pypdf` `get_fields()` prüfen, mit
`render(may_draw_forms=True)` ansehen.

## Stolpersteine (alle getestet, hyperref 7.01h, TeX Live 2023)

- **Felder in Tabellen zu hoch:** ein nacktes `\TextField`/`\CheckBox` übernimmt die Höhe
  der Tabellenzeile (Kästchen werden lange Rechtecke). Feld in `\raisebox`/`\hbox`
  packen – die Kurzbefehle tun das.
- **Optionsfelder ohne `unicode=false`:** Werte wie `\376\377\000z\0001` statt `z1`;
  Chrome speichert diesen Zeichensalat, beim Auslesen ist die Wahl nicht erkennbar.
  `\hypersetup{unicode=false}` nach dem Laden von hyperref genügt.
- **`popdown` allein** erzeugt eine fest aufgeklappte Liste (ListBox), **`combo` allein**
  ein editierbares, sortiertes Feld. Für eine Auswahlliste `combo, popdown`.
- **`\Reset` leert alle Felder** des Dokuments, auch über mehrere `Form`-Umgebungen.
  Nicht in Leistungskontrollen.
- **Hintergrund-/Randfarbe** als `{r g b}` mit Werten 0–1, nicht als xcolor-Name.
- **Poppler** (pdftoppm, Okular, Evince) zeigt Text richtig, ein Häkchen nur als schmalen
  Strich. Zum Ansehen PDFium (`pypdfium2`) verwenden.
- Mehrzeilige Felder scrollen bei zu viel Text; gedruckt wird nur der sichtbare Teil.

Nicht getestet: Adobe Acrobat, Apple Vorschau, iPad-Dateien-App, GoodNotes. Vor dem ersten
Einsatz eine Probeabgabe auf den Geräten der Klasse empfehlen.

## Benötigt in header/newcommands

- header.tex: `hyperref` (vorhanden).
- newcommands.tex: Abschnitt „Formularfelder“ mit `\DefaultOptionsofText`, `…CheckBox`,
  `…Radio`, `…PopdownBox`, `\DefaultHeightofText` und `\feld`, `\zeichen`, `\kreuz`,
  `\antwort` (seit 2026-11-09).
