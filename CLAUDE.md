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
- Keine Stolpersteine in eine SKILL.md schreiben, die nicht getestet sind.
- Commits mit der anonymen GitHub-Adresse (`72416397+mq90@users.noreply.github.com`).
