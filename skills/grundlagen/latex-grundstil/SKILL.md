---
name: latex-grundstil
description: Grundstil für LaTeX-Unterrichtsmaterial (Arbeitsblätter, Leistungskontrollen, Klassenarbeiten, Handreichungen) mit zentraler header.tex und newcommands.tex, festen Regeln für Aufgaben-Nummerierung, Operatoren, Lösungsteil, Boxen und Notation. Verwende diesen Skill IMMER, sobald ein LaTeX-Dokument für Schule oder Unterricht entsteht oder geändert wird – auch zusammen mit einem Fach-Skill (Funktionsgraphen, Geometrie, Baumdiagramme, Schach …), denn dieser Skill legt fest, wie jedes Dokument aufgebaut ist und wo neue Pakete und Befehle hingehören.
---

# LaTeX-Grundstil für Unterrichtsmaterial

Alle Dokumente teilen sich zwei zentrale Stildateien. Dieser Skill beschreibt
das System, die verbindlichen Regeln für Arbeitsblätter und wie die
Stildateien wachsen. Fach-Skills (z. B. `latex-funktionsgraphen`) liefern die
Zeichen-Vorlagen und setzen diesen Skill voraus.

## Das System: header.tex + newcommands.tex

| Datei | Inhalt |
|---|---|
| `header.tex` | `\documentclass`, **alle** Pakete, TikZ-Bibliotheken, Seitenlayout |
| `newcommands.tex` | **alle** eigenen Makros, Farben, Boxen, Kopfzeilen, Listing-Stile |

Beide liegen einmal zentral in `LaTeX/Arbeitsblätter/`. Die Fassung in
diesem Skill (`assets/header.tex`, `assets/newcommands.tex`) ist die
**universale Referenz**: Sie enthält alles, was die Arbeitsblätter, alle
Handreichungen und alle Fach-Skills brauchen, und wird bei jeder Erweiterung
mitgepflegt. Liste aller Befehle, Boxen, Stile und Pakete:
`references/makros.md`.

Jedes Dokument beginnt so – **ohne** `\documentclass`:

```latex
\input{../../../../header.tex}
\input{../../../../newcommands.tex}

% optional: dokumentspezifische Einstellungen, Kopfzeile (\lk{8a}{Thema})

\begin{document}
...
\end{document}
```

**Pfadregel:** pro Ordnerebene unter `Arbeitsblätter/` ein `../`. Ein Mathe-AB
liegt in `Mathematik/Klasse 8/LB 3 - …/<Thema>/<Thema>.tex`, also vier Ebenen
tief → `../../../../`. Jedes Blatt hat einen eigenen Themenordner mit
gleichnamiger `.tex`-Datei (hält `.aux`, `.log`, `.pdf` beisammen).
LB-Ordner heißen `LB 1 - …` (mit Leerzeichen), Klassen 11 und 12 liegen
gemeinsam in `Jahrgangsstufen 11-12/`.

Compiler: **pdflatex**. Keine Pakete, die XeLaTeX oder LuaLaTeX brauchen.
Umlaute direkt im Quelltext (ä, ö, ü, ß), nie `\"a`.

## Neue Pakete und Befehle: immer zentral

Die Stildateien sind *universal* und wachsen mit. Wenn ein Dokument ein
Paket, eine TikZ-Bibliothek, eine Farbe oder ein Makro braucht, das noch
nicht vorhanden ist:

1. **Nicht** im Dokument laden oder definieren, sondern in `header.tex`
   (Pakete, Bibliotheken) bzw. `newcommands.tex` (Makros, Stile) eintragen –
   im passenden Abschnitt, mit einer Kommentarzeile, wofür es da ist.
2. Vorher prüfen, ob es schon etwas Gleichwertiges gibt (Liste:
   `references/makros.md`). Keine zweite Variante eines vorhandenen Makros.
3. Auf Konflikte achten: Paketoptionen, doppelte Namen, Pakete, die andere
   umdefinieren (z. B. `\unit` aus `units` vs. `siunitx`). Nach der Änderung
   ein bestehendes Dokument und das neue kompilieren.
4. Die Änderung oben in der Datei im Änderungsprotokoll vermerken
   (`% 2026-11-09  tikz-Bibliothek »trees« für Baumdiagramme`) und dem
   Nutzer sagen, welche Zeilen in seine zentrale Datei gehören. Die
   Fassung in `assets/` gleich mit aktualisieren.
5. Im Repository danach `python3 werkzeuge/makros_auflisten.py` (aktualisiert
   `references/makros.md`) und `python3 werkzeuge/alles_kompilieren.py`
   (kompiliert alle Vorlagen und Handreichungen gegen die neuen Dateien).

Bekannte Konflikte, die deshalb **nicht** universal sind: `musixtex`
(definiert `\cup` als Achtelnote um, dann bricht $A \cup B$ – nur für
Musik-Dokumente einkommentieren) und die
Musik-Kürzel aus `latex-musixtex` (`\dis` für dis würde `\dis` für
Displaystyle überschreiben).

Ausnahme: Ein Makro, das wirklich nur in einem einzigen Dokument Sinn ergibt
(z. B. `\graufeld` für ein bestimmtes Rätsel), darf lokal in der Präambel stehen.

Fach-Skills nennen in einem Abschnitt „Benötigt in header/newcommands“, was
sie voraussetzen. Fehlt davon etwas, nach den Schritten oben ergänzen.

## Arbeitsblätter – verbindliche Regeln

- **Titel:** `\begin{center}\textbf{\Large{Titel}}\end{center}` + `\bigskip`.
  Kein `\section`/`\subsection`; Zwischenüberschrift höchstens
  `\bigskip\textbf{\large{Text}}\medskip`.
- **Nummerierung:** Aufgaben `\begin{enumerate}[(1)]`, Teilaufgaben `[(a)]`,
  Unter-Teilaufgaben `[(i)]`. Nie durchnummerieren.
- **Keine Boxen für Aufgaben.** tcolorbox nur für Merksätze (`merke`,
  `merke2`), kurze Beispiel-Lösungen (`solution`) und Vorgehen (`todo`).
- **Operatoren:** jede Aufgabe beginnt mit einem Operator im Imperativ
  („Berechne …“, „Begründe …“), keine W-Fragen, kein Fragezeichen.
  Du-Form in Klasse 5–10, Sie-Form in 11–12. Ein Operator pro Aufgabe,
  mehr über Teilaufgaben. Keine Phasenbegriffe („Vorhersagen, Ausführen …“)
  in Aufgabenstellungen.
- **Differenzierung:** Stufen mit `\leicht`, `\mittel`, `\schwer` (drei
  Balken) vor dem Aufgabentext; Aufgaben nach Stufen gruppieren.
- **Layout:** `multicols` für zweispaltigen Satz, `\luecke{…}` für Lücken,
  `\fk{…}` für neue Begriffe, `\gegges{geg}{ges}` für Gegeben/Gesucht.
  Keine Kopf-/Fußzeilen auf Arbeitsblättern.
- **Lösungsteil:** neue Seite, `\begin{scriptsize}\begin{enumerate}[(1)]`
  (gleiches Argument wie im Aufgabenteil), Aufgaben mit
  `\vspace{0.2cm}\hrule\vspace{0.2cm}` getrennt. Ergebnis mit `\frot{…}`
  (Kurzlösungen, Kl. 5–9) oder `\boxed{…}` (mit Einheit, ab Kl. 10).
- **Aufgabenspirale:** mindestens 5–6 Aufgaben steigender Schwierigkeit,
  mindestens eine Begründungs- oder Umkehraufgabe. Details zu den
  Aufgabentypen (Start-Weg-Ziel-Modell): `references/aufgabentypen.md`.

Für ein Mathematik-Arbeitsblatt **immer** `references/arbeitsblatt-mathematik.md`
lesen (Grundgerüst, Lösungsteil, Produkt-/Kettenregel-Farbcode, Notation).

## Handreichungen und Nachschlagewerke

Handreichungen (Fortbildungsmaterial für Lehrkräfte) haben einen festen
Aufbau. Vorlage: `assets/vorlage_handreichung.tex`.

```latex
\input{header.tex}
\input{newcommands.tex}

\title{Automaten mit \TikZ erstellen}
\author{Fortbildungsmaterial für MINT-Lehrkräfte}
\date{\today}
\pagestyle{plain}
\setlength{\parskip}{1.5em}

\begin{document}
\maketitle
Einleitender Absatz …

%%%%  KAPITEL 1  %%%%
\section{Grundlagen und benötigte Bibliotheken}
%%%%  UNTERKAPITEL 1.1  %%%%
\subsection{…}
```

- Der Handreichungs-Ordner enthält Kopien von `header.tex` und
  `newcommands.tex` (`\input{header.tex}` ohne `../`), damit man ihn als
  Ganzes weitergeben kann.
- Kapitel vom Einfachen zum Komplexen: „Grundlagen und benötigte
  Bibliotheken“ → Einzelthemen → „Vollständige Beispiele“/„Praxis“ →
  „Tipps“ → „Zusammenfassung“ (Stichpunkte + Nutzen für den Unterricht).
  Kapitel mit `%%%%  KAPITEL n  %%%%` kommentieren.
- **Jedes Code-Beispiel:** erst der Code in
  `\begin{lstlisting}[style=latex]`, **direkt darunter** dasselbe
  ausgeführt in `\begin{ausgabe} … \end{ausgabe}`, danach die Erklärung.
  Das gilt auch, wenn das PDF dadurch länger wird. Code und Ausgabe müssen
  identisch sein – den Code kopieren, nicht neu tippen.
- Listing-Stil `latex`: gelber Hintergrund, keine Zeilennummern, Umlaute
  erlaubt. Mit Zeilennummern: `style=latexnummeriert`.
- `\TikZ` schreibt den Namen (Leerzeichen danach ist eingebaut),
  `\hologo{LaTeX}` das Logo.
- Ansprache der Leser mit „Sie“; Schülerinnen und Schüler ausschreiben.

## Leistungskontrollen, Klassenarbeiten, Klausuren

Kopfzeile in der Präambel: `\lk{Klasse}{Thema}`, `\ka{…}{…}`, `\kl{…}{…}`,
`\tu{…}{…}` (Tägliche Übung). `\clearfancyheader` entfernt sie (z. B. ab
der Lösungsseite). Diese Makros setzen Name/Punkte/Note und Typ/Klasse/Datum.

## Mathematische Schreibweise

- Lineare Funktionen: $f(x) = mx + n$ – **nie** $mx + b$.
- Zahlenbereiche `\N \Z \Q \R \C`, Grenzwerte `\limn \limh \limxto{a}`,
  Integrale `\dx` bzw. `\d{t}`, Vektoren `\vektor{x}{y}{z}`,
  `\punktvektor{x}{y}`, `\norm{v}`, Stochastik `\E`, `\V`,
  Bruch in Displaygröße im Text `\dis{\frac{a}{b}}`.
- Einheiten `\unit[10]{cm}`, Dezimalkomma `4{,}50`, Haken/Kreuz `\ding{52}`/`\ding{56}`.
- Fachsprache: „Funktionsuntersuchung“ (nie „Kurvendiskussion“),
  „Achsenschnittpunkte“, „Extrempunkte“. Monotonie als Intervalle
  („fallend für $-\infty < x \le 2$“). Symmetrie präzise
  („achsensymmetrisch zur $y$-Achse“, „punktsymmetrisch zum Ursprung“),
  nie „Symmetrie zum Koordinatensystem“.
- Variablen in Textaufgaben erst in einem Satz einführen, dann verwenden.

## Grafiken

Immer reines TikZ, **kein pgfplots** (das Paket ist in der header.tex zwar
geladen, wird aber nicht verwendet). Für die Standardfälle gibt es eigene Skills mit
festen Vorlagen, damit alles gleich aussieht:

| Was | Skill |
|---|---|
| TikZ allgemein (Linien, Koordinaten, foreach, calc, Füllen) | `latex-tikz-grundlagen` |
| Koordinatensystem, Funktionsgraphen | `latex-funktionsgraphen` |
| Baumdiagramme, Vierfeldertafel, Säulendiagramme | `latex-stochastik-diagramme` |
| Dreiecke, Winkel, Konstruktionen, Körper | `latex-geometrie` |
| Mengen, Venn-Diagramme | `latex-venn-diagramme` |
| Automaten, Schaltungen, PAP, UML, Quellcode | `latex-automaten`, `latex-digitale-schaltungen`, `latex-programmablaufplaene`, `latex-uml-klassendiagramme`, `latex-quellcode-listings` |
| Multiple-Choice | `latex-multiple-choice` |
| Formelsatz, Tabellen, eigene Befehle, Präambel | `latex-grundlagen` |
| Figuren, Sprechblasen | `latex-tikzpeople`, `latex-sprechblasen` |
| Lautschrift, Noten | `latex-lautschrift`, `latex-musixtex` |
| Karten | `latex-geodaten-karten` |
| Sudoku, Schach | `latex-sudoku`, `latex-schach` |

## Checkliste vor dem Ausliefern

- [ ] Kein `\documentclass`, Pfad zu `header.tex`/`newcommands.tex` stimmt
- [ ] Neue Pakete/Makros zentral eingetragen, nicht im Dokument
- [ ] AB: kein `\section`, Titel zentriert, `(1)`/`(a)`-Nummerierung
- [ ] Jede Aufgabe mit Operator im Imperativ, Du-/Sie-Form durchgängig
- [ ] Lösungsteil auf neuer Seite, `scriptsize`, `\hrule`, Ergebnis markiert
- [ ] Grafiken in reinem TikZ, Graphen in `\begin{scope}\clip …\end{scope}`
- [ ] Kompiliert mit pdflatex, PDF als Bild angesehen
