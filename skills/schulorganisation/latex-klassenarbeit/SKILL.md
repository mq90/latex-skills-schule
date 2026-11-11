---
name: latex-klassenarbeit
description: Klassenarbeiten und Leistungskontrollen in LaTeX, bei denen LaTeX die Bewertungseinheiten selbst zählt – \BE{2} an jeder Teilaufgabe, automatischer Kopf mit erreichbaren BE, Punktetabelle, Notenschlüssel nach Prozentgrenzen (auf halbe BE gerundet), Lösungsteil per Schalter, Gruppe A/B. Verwende diesen Skill immer, wenn jemand eine Klassenarbeit, Klausur, Leistungskontrolle, Kurzkontrolle, einen Test mit Punkten, einen Notenschlüssel oder Bewertungseinheiten in LaTeX erstellen will.
---

# Klassenarbeit mit automatischer Punktzählung

Setzt `latex-grundstil` voraus (Konventionen für Arbeitsblätter: Aufgaben (1),
(2) mit (a), (b), `\leicht`/`\mittel`/`\schwer` vor dem Aufgabentext, keine
Kästen, keine Kopf-/Fußzeilen, Lösung auf neuer Seite in `\scriptsize`,
Ergebnisse in `\boxed{}`).

## Dateien (`assets/`)

- `ka_makros.tex` – die Makros. Funktioniert nach `\input{header.tex}` +
  `\input{newcommands.tex}` **und** allein nach `\documentclass[11pt]{article}`
  (lädt Pakete nur, wenn sie fehlen; kein siunitx, Zahlen mit `\KAzahl`).
- `vorlage_klassenarbeit.tex` – vollständige Beispielarbeit Mathe LK 11, 25 BE, mit Lösung.

```latex
\input{header.tex}
\input{newcommands.tex}
\input{ka_makros.tex}
\loesungtrue                                  % \loesungfalse = Schülerfassung
\Arbeit{titel = Klassenarbeit, fach = Mathematik, klasse = 8a, thema = …,
        datum = …, zeit = 45 Minuten, hilfsmittel = …, gruppe = A}
\Grenzen{95,80,60,40,20}                      % Mindestprozent Note 1–5
\begin{document}
\Kopf
\begin{enumerate}
  \item \leicht Aufgabentext
  \begin{enumerate} \item Teilaufgabe \BE{2} \item … \BE{1.5} \end{enumerate}
\end{enumerate}
\vfill \Punktetabelle \bigskip \Notenschluessel
\ifloesung \begin{loesungsteil} … \end{loesungsteil} \fi
\end{document}
```

## Regeln

- **Zweimal `pdflatex`**: erster Lauf sammelt die BE (Kopf zeigt 0), zweiter trägt sie ein.
- Halbe BE mit Punkt eingeben (`\BE{1.5}`), gedruckt wird ein Komma.
- Koordinatensysteme mit `\koordinatensystem` aus der newcommands.tex (reines TikZ, kein pgfplots).
- Getestet: ältere Fassung mit `siunitx` brach mit „Package 'units' incompatible“
  ab; die aktuelle verträgt sich mit der universalen header.tex.

## Handreichung

`references/handreichung_klassenarbeit.tex` (PDF in `handreichungen/`):
Aufbau, Angaben, `\BE` und Befehlsübersicht, Ergebnis (Seiten der kompilierten
Vorlage), Lösungsteil, KI-Prompt, Stolpersteine.
