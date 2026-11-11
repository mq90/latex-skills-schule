# Hinweise für Claude – Repository latex-skills-schule

- Jeder Skill liegt in `skills/<bereich>/<skill>/` mit `SKILL.md`, optional
  `references/`, `assets/`, `scripts/`. Neue Skills in den passenden Bereich
  einsortieren und in der Tabelle der `README.md` ergänzen.
- `skills/grundlagen/latex-grundstil/assets/header.tex` und `newcommands.tex`
  sind die universalen Stildateien. Neue Pakete/Befehle dort eintragen (mit
  Kommentar und Zeile im Änderungsprotokoll oben), nie in einzelne Dokumente.
- Handreichungen im Standardstil: `lstlisting[style=latex]`, direkt darunter
  derselbe Code in `\begin{ausgabe}`. Vorlage: `latex-grundstil/assets/vorlage_handreichung.tex`.
- Nach jeder Änderung:
  `python3 werkzeuge/makros_auflisten.py` und
  `python3 werkzeuge/alles_kompilieren.py` – es muss alles kompilieren.
  Neue oder geänderte Grafiken als PNG rendern und ansehen.
- Nach Änderungen an Handreichungen oder Stildateien
  `python3 werkzeuge/handreichungen_bauen.py` ausführen und die PDFs in
  `handreichungen/` mit committen; neue Handreichungen in der PDF-Tabelle der
  `README.md` ergänzen.
- Grafiken in reinem TikZ, **kein pgfplots** (auch für Messwerte und Funktionen;
  Regression und pH-Kurven rechnet TikZ selbst, siehe latex-physik/-chemie).
  **Kein siunitx** in Dokumenten mit der universalen header.tex (kollidiert mit units).
- Farben: Akzentfarben `akzentblau/-rot/-gruen/-orange/-lila` aus der newcommands.tex,
  keine schulspezifischen Farbnamen. Große Ausgaben in `\begin{passend}`, Hinweise in
  `\begin{hinweis}[Titel]`.
- Handreichungen dürfen Datendateien aus `assets/` desselben Skills per `\input`
  laden und PDFs kompilierter Vorlagen per `\includegraphics{name.pdf}` einbinden;
  die Bauskripte stellen beides bereit (`vorlagen_vorbauen`).
- Keine echten Personen- oder Schulnamen in Beispieldateien (Platzhalter „N. N.“,
  „Musterschule“); Schülernamen nie, auch nicht als Beispiel.
- Keine Stolpersteine in eine SKILL.md schreiben, die nicht getestet sind.
- Commits mit der anonymen GitHub-Adresse (`72416397+mq90@users.noreply.github.com`).
