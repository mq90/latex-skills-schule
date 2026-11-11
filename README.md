# latex-skills-schule

Skills für Claude rund um LaTeX im Schulalltag: Arbeitsblätter,
Leistungskontrollen, Klassenarbeiten, Handreichungen, Grafiken, Landkarten,
Naturwissenschaften, Schulorganisation und Rätsel – mit einer
universalen `header.tex`/`newcommands.tex`, getesteten Vorlagen,
Befehlsreferenzen und Hilfsskripten. Alles mit **pdflatex** und reinem
**TikZ** (kein pgfplots).

Ein **Skill** ist ein Ordner mit einer `SKILL.md` (wann und wie Claude ihn
benutzt) und Begleitdateien. Claude lädt nur den Skill, der zur Anfrage
passt – deshalb ist jedes Thema ein eigener Skill.

## Aufbau

```
skills/
├── grundlagen/                Grundstil, LaTeX- und TikZ-Grundlagen, Multiple-Choice
├── mathematik/                Funktionsgraphen, Geometrie, Stochastik, Venn-Diagramme
├── informatik/                Automaten, Schaltungen, Programmablaufpläne, UML, Quellcode, PDF-Formulare
├── sprache-musik/             Lautschrift (IPA), Notensatz (MusiXTeX)
├── naturwissenschaften/       Physik, Chemie, Biologie
├── illustration/              tikzpeople-Figuren, Sprechblasen
├── gesellschaftswissenschaft/ Landkarten aus Geodaten (Atlas mit 10 Karten)
├── schulorganisation/         Stoffverteilungsplan, Sitzplan, Klassenarbeit, Anki-Karten
└── raetsel-spiele/            Sudoku, Schach
handreichungen/                fertige PDFs aller Handreichungen
werkzeuge/                     Prüf- und Hilfsskripte für das Repository
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
| | [`latex-pdf-formulare`](skills/informatik/latex-pdf-formulare) | interaktive, ausfüllbare PDFs, digitale Leistungskontrollen | Handreichung, Vorlage, Beispiel-LK, Skripte zum Einsammeln und Testen |
| Sprache & Musik | [`latex-lautschrift`](skills/sprache-musik/latex-lautschrift) | IPA mit tipa oder Unicode | Handreichung, Lauttabellen, Vokalviereck |
| | [`latex-musixtex`](skills/sprache-musik/latex-musixtex) | Notensatz | Musik-Kürzel |
| Naturwissenschaften | [`latex-physik`](skills/naturwissenschaften/latex-physik) | Einheiten, Messwerttabellen, Ausgleichsgerade, Schaltpläne (circuitikz), Strahlengänge | Handreichung; Vorlagen Federdehnung (Regression in TikZ), Schaltpläne, Sammellinse |
| | [`latex-chemie`](skills/naturwissenschaften/latex-chemie) | Reaktionsgleichungen (mhchem), Oxidationszahlen, Strukturformeln (chemfig), Periodensystem, Titrationskurve, Energiediagramm | Handreichung; 3 Vorlagen, pH-Kurve wird berechnet statt gezeichnet |
| | [`latex-biologie`](skills/naturwissenschaften/latex-biologie) | Kreuzungsschemata, Stammbäume (genealogytree), Codesonne, Nahrungsnetz, Wachstumskurven | Handreichung; 5 Vorlagen |
| Illustration | [`latex-tikzpeople`](skills/illustration/latex-tikzpeople) | Personen-Figuren, Alice/Bob/Eve | Handreichung, Galerie |
| | [`latex-sprechblasen`](skills/illustration/latex-sprechblasen) | Sprech- und Gedankenblasen | `\lehrerblase`, `\schuelerblase` |
| Gesellschaftswissenschaft | [`latex-geodaten-karten`](skills/gesellschaftswissenschaft/latex-geodaten-karten) | echte Karten aus freien Geodaten: Lagekarte, Bundesländer, physische Karte mit Höhenschichten, Verkehr, USA, Europa, Weltprojektionen, Römisches Reich, Deutschland 1871–1990, Generalisierung | Handreichung (37 S.), Atlas mit 10 fertigen Karten, `geo2tikz.py`, `karten_beispiele.py` (lädt Rohdaten und erzeugt alle Kartendaten neu) |
| Schulorganisation | [`latex-stoffverteilungsplan`](skills/schulorganisation/latex-stoffverteilungsplan) | Stoffverteilungsplan aus einer TOML-Datei: Termine, A/B-Wochen, Ferien, Sperrzeiten, Lernbereiche | Handreichung, `stoffverteilungsplan.py`, 2 Beispielpläne, Ferien Sachsen 2026/27 |
| | [`latex-sitzplan`](skills/schulorganisation/latex-sitzplan) | Sitzpläne (Reihen, U-Form, Gruppentische) aus TOML + Namensliste | Handreichung, `sitzplan.py`, 3 Beispiele mit Platzhalternamen |
| | [`latex-klassenarbeit`](skills/schulorganisation/latex-klassenarbeit) | Klassenarbeiten, bei denen LaTeX die Bewertungseinheiten zählt: Kopf, Punktetabelle, Notenschlüssel, Lösungsteil | Handreichung, `ka_makros.tex`, Vorlage |
| | [`latex-anki-karten`](skills/schulorganisation/latex-anki-karten) | Anki-Stapel (Vokabeln, Formeln, Bilder, Multiple Choice), dazu Papiertest und QTI-Paket aus derselben Liste | Handreichung, `anki_karten.py`, Beispiel-CSVs, Bundesländer-Bilder |
| Rätsel & Spiele | [`latex-sudoku`](skills/raetsel-spiele/latex-sudoku) | Sudoku-Arbeitsblätter | Handreichung, Generator mit eindeutiger Lösung |
| | [`latex-schach`](skills/raetsel-spiele/latex-schach) | Bretter, Partien, Mattaufgaben | Handreichung, Prüfskript für FEN |

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

## Handreichungen als PDF

Alle Handreichungen und Nachschlagewerke liegen fertig gesetzt im Ordner
[`handreichungen/`](handreichungen) – zum Lesen, Ausdrucken und Weitergeben,
auch ohne LaTeX-Installation. Die Quelltexte stehen in den
`references/`-Ordnern der jeweiligen Skills.

| Bereich | Handreichung | Seiten |
|---|---|---|
| Grundlagen | [Erste Schritte mit LaTeX: Die Präambel](handreichungen/grundlagen/Erste-Schritte-mit-LaTeX-Die-Pr%C3%A4ambel.pdf) | 5 |
|  | [Erste Schritte mit TikZ: Grundlagen des Grafikpakets](handreichungen/grundlagen/Erste-Schritte-mit-TikZ-Grundlagen-des-Grafikpakets.pdf) | 11 |
|  | [Erste Schritte mit eigenen Befehlen und Umgebungen in LaTeX](handreichungen/grundlagen/Erste-Schritte-mit-eigenen-Befehlen-und-Umgebungen-in-LaTeX.pdf) | 6 |
|  | [Erste Schritte mit mathematischem Formelsatz in LaTeX](handreichungen/grundlagen/Erste-Schritte-mit-mathematischem-Formelsatz-in-LaTeX.pdf) | 16 |
|  | [Multiple-Choice-Fragen mit LaTeX erstellen](handreichungen/grundlagen/Multiple-Choice-Fragen-mit-LaTeX-erstellen.pdf) | 6 |
|  | [Tabellenstruktur und Tabellengestaltung in LaTeX](handreichungen/grundlagen/Tabellenstruktur-und-Tabellengestaltung-in-LaTeX.pdf) | 17 |
|  | [Zeichnen mit TikZ in LaTeX](handreichungen/grundlagen/Zeichnen-mit-TikZ-in-LaTeX.pdf) | 13 |
| Mathematik | [Baumdiagramme und Diagramme der Stochastik mit TikZ](handreichungen/mathematik/Baumdiagramme-und-Diagramme-der-Stochastik-mit-TikZ.pdf) | 9 |
|  | [Funktionsgraphen mit TikZ zeichnen](handreichungen/mathematik/Funktionsgraphen-mit-TikZ-zeichnen.pdf) | 11 |
|  | [Geometrische Figuren mit TikZ zeichnen](handreichungen/mathematik/Geometrische-Figuren-mit-TikZ-zeichnen.pdf) | 10 |
|  | [Venn-Diagramme mit TikZ in LaTeX](handreichungen/mathematik/Venn-Diagramme-mit-TikZ-in-LaTeX.pdf) | 10 |
| Informatik | [Ausfüllbare PDF-Formulare mit LaTeX erstellen](handreichungen/informatik/Ausf%C3%BCllbare-PDF-Formulare-mit-LaTeX-erstellen.pdf) | 15 |
|  | [Automaten mit TikZ erstellen](handreichungen/informatik/Automaten-mit-TikZ-erstellen.pdf) | 7 |
|  | [Digitale Schaltkreise mit TikZ erstellen](handreichungen/informatik/Digitale-Schaltkreise-mit-TikZ-erstellen.pdf) | 5 |
|  | [Programmablaufpläne mit TikZ erstellen](handreichungen/informatik/Programmablaufpl%C3%A4ne-mit-TikZ-erstellen.pdf) | 6 |
|  | [Quellcode mit dem listings-Paket darstellen](handreichungen/informatik/Quellcode-mit-dem-listings-Paket-darstellen.pdf) | 6 |
|  | [UML-Klassendiagramme mit TikZ erstellen](handreichungen/informatik/UML-Klassendiagramme-mit-TikZ-erstellen.pdf) | 9 |
| Illustration | [Sprechblasen mit TikZ in LaTeX](handreichungen/illustration/Sprechblasen-mit-TikZ-in-LaTeX.pdf) | 5 |
|  | [Figuren mit tikzpeople zeichnen](handreichungen/illustration/Figuren-mit-tikzpeople-zeichnen.pdf) | 7 |
| Sprache & Musik | [Notensätze mit MusiXTeX erstellen](handreichungen/sprache-musik/Notens%C3%A4tze-mit-MusiXTeX-erstellen.pdf) | 3 |
|  | [Lautschrift mit LaTeX setzen](handreichungen/sprache-musik/Lautschrift-mit-LaTeX-setzen.pdf) | 12 |
| Gesellschaftswissenschaft | [Landkarten aus Geodaten mit TikZ zeichnen](handreichungen/gesellschaftswissenschaft/Landkarten-aus-Geodaten-mit-TikZ-zeichnen.pdf) | 37 |
| Naturwissenschaften | [Biologie mit LaTeX: Erbgänge, Stammbäume, Codesonne und Wachstum](handreichungen/naturwissenschaften/Biologie-mit-LaTeX-Erbg%C3%A4nge-Stammb%C3%A4ume-Codesonne-und-Wachstum.pdf) | 9 |
|  | [Chemie mit LaTeX: Reaktionsgleichungen, Strukturformeln und Diagramme](handreichungen/naturwissenschaften/Chemie-mit-LaTeX-Reaktionsgleichungen-Strukturformeln-und-Diagramme.pdf) | 10 |
|  | [Physik mit LaTeX: Einheiten, Messwerte, Schaltpläne und Optik](handreichungen/naturwissenschaften/Physik-mit-LaTeX-Einheiten-Messwerte-Schaltpl%C3%A4ne-und-Optik.pdf) | 9 |
| Schulorganisation | [Anki-Karteikarten, Multiple-Choice-Tests und QTI aus einer Liste](handreichungen/schulorganisation/Anki-Karteikarten-Multiple-Choice-Tests-und-QTI-aus-einer-Liste.pdf) | 7 |
|  | [Klassenarbeiten mit automatischer Punktzählung](handreichungen/schulorganisation/Klassenarbeiten-mit-automatischer-Punktz%C3%A4hlung.pdf) | 5 |
|  | [Sitzpläne automatisch erstellen](handreichungen/schulorganisation/Sitzpl%C3%A4ne-automatisch-erstellen.pdf) | 6 |
|  | [Stoffverteilungspläne automatisch erstellen](handreichungen/schulorganisation/Stoffverteilungspl%C3%A4ne-automatisch-erstellen.pdf) | 8 |
| Rätsel & Spiele | [Schach mit skak, xskak und chessboard](handreichungen/raetsel-spiele/Schach-mit-skak-xskak-und-chessboard.pdf) | 9 |
|  | [Sudokus mit dem Paket sudoku setzen](handreichungen/raetsel-spiele/Sudokus-mit-dem-Paket-sudoku-setzen.pdf) | 7 |

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
| `werkzeuge/handreichungen_bauen.py` | baut alle Handreichungen neu als PDF in `handreichungen/` |

Handreichungen dürfen Datendateien aus dem `assets/`-Ordner ihres Skills
laden und PDFs von Vorlagen einbinden (`\includegraphics{vorlage.pdf}`); beide
Skripte kompilieren solche Vorlagen vorher selbst.

Skripte in den Skills:

| Skript | Zweck |
|---|---|
| `latex-geodaten-karten/scripts/geo2tikz.py` | GeoJSON/Shapefile → TikZ-Pfade mit Projektion und Vereinfachung |
| `latex-geodaten-karten/scripts/karten_beispiele.py` | lädt die Rohdaten und erzeugt alle Kartendaten des Atlas neu |
| `latex-stoffverteilungsplan/scripts/stoffverteilungsplan.py` | TOML → Stoffverteilungsplan als LaTeX |
| `latex-sitzplan/scripts/sitzplan.py` | TOML + Namensliste → Sitzplan als LaTeX |
| `latex-anki-karten/scripts/anki_karten.py` | CSV/Fragenliste → Anki-Stapel, Papiertest, QTI-Paket |
| `latex-sudoku/scripts/` | Sudoku-Generator mit Eindeutigkeitsprüfung |
| `latex-schach/scripts/` | FEN-Prüfung |
| `latex-pdf-formulare/scripts/` | ausgefüllte Formulare einsammeln und testen |

Nach jeder Änderung an `header.tex` oder `newcommands.tex` alle drei Skripte
ausführen, nach Änderungen an einer Handreichung `handreichungen_bauen.py`.

## Voraussetzungen

- TeX Live mit `texlive-latex-extra`, `texlive-pictures`, `texlive-science`,
  `texlive-games`, `texlive-plain-generic`, `texlive-fonts-extra`,
  `texlive-lang-german`, `texlive-music`; für Unicode-Lautschrift
  `texlive-xetex` und die Schrift Charis SIL
  sowie `circuitikz`, `mhchem`, `chemfig`, `pgf-periodictable`,
  `genealogytree`, `units` (alle in TeX Live enthalten)
- Python 3.11 oder neuer (für `tomllib`); je nach Skill:

  | Skill | Pakete |
  |---|---|
  | latex-schach | `pip install chess` |
  | latex-geodaten-karten | `pip install shapely pyproj` (geo2tikz), zusätzlich `h5py contourpy scipy` für `karten_beispiele.py` |
  | latex-pdf-formulare | `pip install pypdf pypdfium2 pymupdf` |
  | latex-anki-karten | `pip install genanki` |
  | latex-stoffverteilungsplan, latex-sitzplan | keine (nur Standardbibliothek) |

## Grundsätze

- Jedes Code-Beispiel ist kompiliert und das Ergebnis angesehen worden.
- Stolpersteine stehen in jeder `SKILL.md` mit der echten Fehlermeldung.
- Rätsel werden maschinell auf eindeutige Lösbarkeit geprüft, Wahrscheinlichkeiten
  exakt berechnet statt in TikZ.
- Grafiken in reinem TikZ, **kein pgfplots** – auch Messwertdiagramme,
  Ausgleichsgeraden und Titrationskurven rechnet TikZ selbst.
- **Kein siunitx**: Es kollidiert mit `units` aus der universalen
  `header.tex`. Einheiten mit `\unit[10]{cm}`, Zahlen mit
  `\pgfmathprintnumber[use comma]`.
- Farben schulunabhängig: `akzentblau`, `akzentrot`, `akzentgruen`,
  `akzentorange`, `akzentlila`.
- Beispieldateien enthalten keine echten Namen (Platzhalter wie „N. N.“,
  „Musterschule“, erfundene Schülernamen). Echte Klassenlisten, Noten und
  Fotos gehören nicht in eine KI und nicht ins Repository.
- Geodaten-Rohdaten (GeoJSON, Höhenmodell) liegen nicht im Repository – nur die
  daraus erzeugten, vereinfachten `*_daten.tex`-Dateien. `karten_beispiele.py
  download` lädt die Rohdaten, `karten_beispiele.py` ohne Argument erzeugt alles neu.

## Lizenz

Skripte (`*.py`): MIT. Alle übrigen Inhalte: CC BY 4.0 –
Namensnennung „latex-skills-schule von Martin Quandt“. Ausnahmen bei zwei
Kartendatensätzen: `rom_daten.tex` (ODbL 1.0) und `historisch_daten.tex`
(GPL-3.0). Details in [LICENSE](LICENSE).
