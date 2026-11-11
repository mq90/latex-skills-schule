---
name: latex-chemie
description: Chemie-Material mit LaTeX – Reaktionsgleichungen mit mhchem (\ce), Oxidationszahlen (\oz), Strukturformeln und Valenzstrichformeln mit chemfig, Periodensystem mit pgf-PeriodicTable (deutsch, eingefärbt, Ausschnitte), berechnete Titrationskurve (inkl. Autoprotolyse, reines TikZ) und Energiediagramm mit/ohne Katalysator. Verwende diesen Skill immer, wenn jemand ein Chemie-Arbeitsblatt, eine Reaktions- oder Redoxgleichung, eine Strukturformel, Lewis-Formel, ein Periodensystem, eine Titrationskurve oder ein Energiediagramm in LaTeX braucht.
---

# Chemie mit LaTeX

Setzt `latex-grundstil` voraus. In der universalen `header.tex` sind
`mhchem` (version=4), `chemfig` und `pgf-PeriodicTable` geladen, in der
`newcommands.tex` der Befehl `\oz{+II}{Cu}` für Oxidationszahlen.

## Vorlagen (`assets/`, getestet)

| Datei | Inhalt | Was man ändert |
|---|---|---|
| `vorlage_titration.tex` | Titrationskurve HCl/NaOH, berechnet inkl. Autoprotolyse, Äquivalenzpunkt markiert | `\def\cS{0.1}`, `\def\VS{20}`, `\def\cB{0.1}` |
| `vorlage_energiediagramm.tex` | Energieverlauf mit und ohne Katalysator (Sigmoid + Gaußglocke), E_A, ΔH | `\Eedukt`, `\Eprodukt`, `\Ea`, `\Eak` (in cm) |
| `vorlage_periodensystem.tex` | vollständig (MNM-Farben) und Elemente 1–20 | Optionen von `\pgfPT[…]` |

## Kurzreferenz

```latex
\ce{2 H2 + O2 -> 2 H2O}   \ce{N2 + 3 H2 <=> 2 NH3}   \ce{Cu^2+ + 2 e- -> Cu}
\ce{CaCO3 ->[\Delta] CaO + CO2}   \ce{H2 ^}  \ce{AgCl v}   \ce{Na+(aq)}
\ce{$\oz{0}{Zn}$ + $\oz{+II}{Cu}$^2+ -> ...}      % \oz in \ce zwischen $…$
\chemfig{H-C(-[2]H)(-[6]H)-H}   \chemfig{*6(-=-=-=)}   \chemfig{H-\charge{90=\|,270=\|}{O}-H}
\pgfPTsetLanguage{de} \pgfPT[show title=false, show legend=false, Z list={1,...,20}]
```
chemfig-Richtungen in 45°-Schritten: `[0]` rechts, `[2]` oben, `[4]` links, `[6]` unten.

## Stolpersteine (getestet)

- **`chemmacros` mit deutschem `babel`:** `\ch` benutzt `"` – pdflatex blieb hängen.
  Gleichungen mit `\ce` aus mhchem.
- **`\lewis` gibt es nicht mehr** – freie Elektronenpaare mit `\charge`.
- **Ionenladung mit Oxidationszahl:** `$\oz{-II}{O}_4^-$` setzt das Minus an die
  Oxidationszahl. Richtig: `\ce{$\oz{+VII}{Mn}$$\oz{-II}{O}$4^-}`.
- **pH-Rechnung in TikZ:** pgfmath kann 1e-14 nicht darstellen (nur ca. 1e-5 bis
  16000). Deshalb pH = 7 − arsinh(d/2e-7)/ln 10, für |d| ≥ 1e-5 als
  sign(d)·(ln|d| + 16.1181)/ln 10 (Fehler < 0,0004); siehe Vorlage.
- **Kein pgfplots** (Repository-Grundsatz): alle Diagramme in reinem TikZ.
- `pgf-PeriodicTable` erzeugt in den Elementkästchen kleine Overfull-Meldungen (< 4 pt) – harmlos.

## Handreichung

`references/handreichung_chemie.tex` (10 Seiten; PDF in `handreichungen/`):
mhchem mit Eingabetabelle, Oxidationszahlen, chemfig (Ketten, Ringe,
Valenzstrichformeln), Periodensystem, Titration mit Herleitung, Energiediagramm,
weitere Pakete, Stolpersteine. Beispiele mit Vorlagen enthalten deren Code wörtlich.
