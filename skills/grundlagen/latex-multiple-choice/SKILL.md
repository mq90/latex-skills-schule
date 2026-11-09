---
name: latex-multiple-choice
description: Multiple-Choice-Fragen in LaTeX setzen – horizontal mit fünf Antworten nebeneinander oder vertikal untereinander, mit Ankreuzkästchen, für Tests, Diagnosen, Abi-Vorbereitung und Leistungskontrollen. Verwende diesen Skill immer, wenn Ankreuzaufgaben, MC-Tests, Single-/Multiple-Choice, Quizfragen auf Papier oder eine Handreichung zu MC-Fragen in LaTeX entstehen sollen.
---

# Multiple-Choice-Fragen

Setzt `latex-grundstil` voraus. Die Umgebungen stehen in der universalen
`newcommands.tex` (Abschnitt „MC-Fragen“).

## Horizontal – genau fünf Antworten

```latex
\begin{mcquestionh}{Die Einheit der elektrischen Leistung ist:}
	\answerh{Watt (W)} & \answerh{Volt (V)} & \answerh{Ampere (A)} & \answerh{Ohm ($\Omega$)} & \answerh{Joule (J)}
\end{mcquestionh}
```

Spalten sind 2,5 cm breit; `\answerh{…}` bricht lange Antworten in der
Spalte um. Die Umgebung erwartet **genau fünf** Antworten (vier `&`). Für
weniger Antworten leere Zellen lassen oder vertikal arbeiten.

## Vertikal – beliebig viele Antworten

```latex
\begin{mcquestionv}{Welche Aussage ist richtig?}
	\answerv{Antwort A}
	\answerv{Antwort B}
	\answerv{Antwort C}
\end{mcquestionv}
```

## Hinweise

- Fragen in `enumerate[(1)]` nummerieren, wie alle Aufgaben.
- Auch MC-Fragen beginnen mit Operator, wo es geht („Kreuze die richtige
  Aussage an.“); für Abi-Formate ist die Frageform üblich.
- Lösungen: im Lösungsteil die richtige Antwort nennen, nicht im Aufgabenteil
  markieren.

## Referenz

Vollständige Handreichung (eigene Befehle und Umgebungen als Grundlage,
horizontale und vertikale Fragen, Praxisbeispiele):
`references/handreichung_multiple_choice.tex`.
