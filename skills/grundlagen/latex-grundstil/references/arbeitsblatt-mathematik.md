# Mathematik-Arbeitsblätter – ausführliche Regeln

Ergänzt die SKILL.md von latex-grundstil. Gilt für reguläre Mathe-Arbeitsblätter.
Grafik-Vorlagen stehen in den Skills latex-funktionsgraphen, latex-geometrie und
latex-stochastik-diagramme.

Dieser Stil gilt **ausschließlich** für reguläre Mathematik-Arbeitsblätter.
Leistungskontrollen, Klassenarbeiten, Klausuren, Tägliche Übungen und
Informatik-Materialien werden in eigenen Stildateien beschrieben.

---

## 1. Reale Ordnerstruktur

`header.tex` und `newcommands.tex` liegen direkt in `Arbeitsblätter/`.
Mathematik-Arbeitsblätter liegen typischerweise **vier Ordnerebenen tief**:

```
LaTeX/
└── Arbeitsblätter/
    ├── header.tex
    ├── newcommands.tex
    │
    ├── Anhang/
    ├── Druckvorlagen/
    ├── Mathedidaktik/
    ├── MC-Fragen Abi/
    ├── Noch ohne Lösungen/
    ├── Petzzettel/
    ├── Tafelbilder/
    │
    └── Mathematik/
        ├── Klasse 5/
        │   └── LB 1 - Arbeiten mit natürlichen Zahlen/
        │       └── Übung zum Schriftlichen Dividieren/
        │           └── Übung zum Schriftlichen Dividieren.tex
        ├── Klasse 6/
        ├── Klasse 7/
        ├── Klasse 8/
        │   └── LB 3 - Funktionen und lineare Gleichungssysteme/
        │       └── Lineare Gleichungen mit zwei Variablen -- Textaufgaben/
        │           └── Lineare Gleichungen mit zwei Variablen -- Textaufgaben.tex
        ├── Klasse 9/
        ├── Klasse 10/
        └── Jahrgangsstufen 11-12/
            └── LB 1 - Differentialrechnung/
                └── Geometrische Extremwertprobleme/
                    └── Geometrische Extremwertprobleme.tex
```

**Wichtig:**

- LB-Ordner heißen `LB 1 - …`, `LB 2 - …` (mit Leerzeichen, **nicht** `LB1`).
- Klassen 11 und 12 liegen gemeinsam unter `Jahrgangsstufen 11-12/`.
- Jedes Arbeitsblatt liegt in einem **eigenen Themenordner** mit gleichlautendem
  Dateinamen (`<Thema>/<Thema>.tex`). Das hält Hilfsdateien (`.aux`, `.log`, `.pdf`)
  beieinander.

### Pfad zu den Stildateien

Da die `.tex` vier Ebenen unter `Arbeitsblätter/` liegt:

```latex
\input{../../../../header.tex}
\input{../../../../newcommands.tex}
```

Pro Ordnerebene unter `Arbeitsblätter/` ein `../` mehr — der Standard für ein
Mathe-AB ist **immer** `../../../../`.

---

## 2. Grundgerüst eines Mathe-Arbeitsblatts

```latex
\input{../../../../header.tex}
\input{../../../../newcommands.tex}

% Optional: dokumentspezifische lokale Makros / Hilfsboxen
% \newcommand{\graufeld}{...}

\begin{document}

  \begin{center}\textbf{\Large{Titel des Arbeitsblatts}}\end{center}
  \bigskip

  \begin{enumerate}[(1)]
    \item Aufgabentext …
    \item …
  \end{enumerate}

  \newpage

  \begin{center}\textbf{\Large{Lösungen}}\end{center}
  \begin{scriptsize}\begin{enumerate}[(1)]
    \item …
  \end{enumerate}\end{scriptsize}

\end{document}
```

**Regeln:**

- Kein `\documentclass` — steht in `header.tex`.
- Kein `\section`, kein `\subsection` auf Arbeitsblättern.
- Titel **immer** als `\begin{center}\textbf{\Large{...}}\end{center}`,
  gefolgt von `\bigskip` oder `\medskip`.
- Zwischenüberschriften (selten nötig):
  `\bigskip\textbf{\large{Text}}\medskip`.

---

## 3. Aufgaben-Nummerierung (verbindlich)

```latex
\begin{enumerate}[(1)]          % Hauptaufgaben: (1), (2), (3) …
  \item …
  \begin{enumerate}[(a)]        % Teilaufgaben: (a), (b), (c) …
    \item …
    \begin{enumerate}[(i)]      % Unter-Teilaufgaben: (i), (ii), (iii) …
      \item …
    \end{enumerate}
  \end{enumerate}
\end{enumerate}
```

Lösungs-`enumerate` **muss** dasselbe Argument haben wie der Aufgabenteil
(`[(1)]` oder unmarkiert), damit die Nummern übereinstimmen.

---

## 4. Aufgabenformulierung — Operatoren

### 4.1 Grundregeln

- **Keine W-Fragen** als Aufgabenstellung
  (kein „Was …?", „Wie viel …?", „Welche …?", „Wann …?", „Warum …?").
  Stattdessen immer mit einem **Operator im Imperativ** beginnen.
- **Du-Form** in Klassen 5–10, **Sie-Form** in Klassen 11–12.
  („Berechne …" vs. „Berechnen Sie …")
- Operator steht am **Satzanfang** und endet mit einem Punkt — kein Fragezeichen.
- Pro Aufgabe **ein** klarer Operator. Mehrteilige Anweisungen über
  Teilaufgaben `(a), (b), …` strukturieren, nicht in einen Satz packen.
- Schlechte Beispiele → korrigieren:
  - „Was ergibt $2x+5$ für $x=3$?" → „Berechne den Termwert für $x=3$."
  - „Wie groß ist die Steigung?" → „Bestimme die Steigung $m$."
  - „Welche Werte erfüllen die Gleichung?" → „Gib die Lösungsmenge an."

### 4.2 Operatorenliste

> **Platzhalter** — die endgültige Liste der zugelassenen Operatoren wird
> separat geliefert und hier eingepflegt. Bis dahin orientiert sich der Stil
> an den im Material bereits etablierten Operatoren (Bestandsaufnahme aus
> realen Arbeitsblättern):

| Kategorie | Operatoren (aus Bestand) |
|-----------|--------------------------|
| Rechnen / Anwenden | Berechne(n Sie), Bestimme(n Sie), Wende … an, Löse, Ermittle, Vereinfache, Fasse … zusammen, Kürze, Erweitere |
| Aufstellen / Darstellen | Stelle … auf, Schreibe (eine Gleichung / einen Term), Übersetze, Drücke … aus, Gib … an, Nenne |
| Zeichnen / Skizzieren | Skizziere(n Sie), Zeichne(n Sie), Konstruiere, Markiere, Trage … ein |
| Argumentieren | Begründe(n Sie), Zeige(n Sie), Beweise(n Sie), Erkläre, Entscheide … und begründe, Interpretiere |
| Beschreiben | Beschreibe (mit eigenen Worten), Charakterisiere, Vergleiche, Klassifiziere |
| Korrigieren / Ergänzen | Korrigiere, Ergänze, Fülle die Lücken, Ordne … zu |
| Untersuchen | Untersuche(n Sie), Prüfe (rechnerisch / grafisch), Diskutiere |

**Achtung:** Diese Tabelle wird ersetzt, sobald die offizielle Liste nachgereicht
ist. Beim Erstellen neuer Arbeitsblätter ist die offizielle Liste verbindlich.

### 4.3 Form der Aufgabenstellung

- Erst der Operator, dann das **mathematische Objekt**, optional eine
  **Methodenangabe**, optional ein **Modalsatz**:
  > „Berechne die erste Ableitung von $f$ mit Hilfe der Produktregel.
  > Fasse den Funktionsterm soweit wie möglich zusammen."
- Bei Textaufgaben: Sachverhalt im Indikativ, Aufgabe als Imperativ am Ende.
- Größen, Variablen und Einheiten **immer** im Mathe-Modus, mit `\unit[…]{…}`:
  z.B. `\unit[10]{cm}`, `\unit[4]{cm^2}`, `\unit[2\pi]{cm^3}`.

---

## 5. Lösungsteil — Aufbau

### 5.1 Grundgerüst

```latex
\newpage

\begin{center}\textbf{\Large{Lösungen}}\end{center}
\medskip
\begin{scriptsize}\begin{enumerate}[(1)]

  \item <Lösung Aufgabe 1>
    \vspace{0.2cm}\hrule\vspace{0.2cm}

  \item <Lösung Aufgabe 2>
    \vspace{0.2cm}\hrule\vspace{0.2cm}

  % …

\end{enumerate}\end{scriptsize}
```

**Verbindliche Regeln:**

- Lösungen **immer** auf einer **neuen Seite** (`\newpage`).
- Lösungsteil **immer** in `\begin{scriptsize}` — spart Platz und visualisiert
  die Trennung zu den Aufgaben.
- `\begin{enumerate}[(1)]` (bzw. dasselbe Argument wie im Aufgabenteil)
  übernimmt die Aufgabennummern automatisch.
- Trennung der Aufgaben mit `\hrule` (Standardform:
  `\vspace{0.2cm}\hrule\vspace{0.2cm}`). **Kein** `\noindent\rule{...}` mehr
  im Lösungsteil — `\hrule` ist kürzer und etabliert.
- Teilaufgaben ebenfalls in `[(a)]` gegliedert, parallel zur Aufgabenstellung.

### 5.2 Hervorhebung des Ergebnisses

Drei etablierte Muster — je nach Charakter der Aufgabe:

**(a) `\frot{…}` für unterstrichene Endwerte in Kurzlösungen** (Klassen 5–9,
Lückenaufgaben, Termwerte, kurze Brüche):

```latex
\item $\frot{x+58 = 3x}$
\item $\dfrac{36}{48} \overset{\frot{:12}}{=} \dfrac{\frot{3}}{\frot{4}}$
```

**(b) `\boxed{…}` für Endergebnisse mit Einheit** (Klassen 10–12,
Sachaufgaben, Extremwertprobleme):

```latex
$\boxed{a = b = \unit[2]{cm}}$, \; $\boxed{A_{\max} = \unit[4]{cm^2}}$
```

**(c) Farbcodierte Variablen für regelbasierte Rechnungen** (Produktregel,
Kettenregel, Quotientenregel): Verwendung von `\fblau`, `\fcyan`, `\frot`,
`\forange` für $u, u', v, v'$ bzw. $g, g', h, h'$ — siehe Abschnitt 5.4.

### 5.3 Form der Rechenschritte

- Mehrzeilige Umformungen: `\[ … \;\Rightarrow\; … \;\Rightarrow\; … \]`
  oder `align*` — kein Fließtext zwischen Gleichungen.
- Inline-Brüche mit `\dfrac{…}{…}` (groß genug zum Lesen),
  Einheitenbrüche mit `\nicefrac{…}{…}`.
- Proben/Verifikationen mit `\ding{52}` (✓) bzw. `\ding{56}` (✗):
  ```latex
  Probe: $13+7 = 20$\;\ding{52}\quad und $26+28 = 54$\;\ding{52}
  ```
- Bei Textaufgaben: **erst** Variablen deklarieren
  („Sei $n$ der Preis einer Portion Nudeln in €, $g$ der Preis eines Getränks
  in €."), **dann** das Gleichungssystem aufstellen, **dann** lösen, **dann**
  die Probe, **dann** der Antwortsatz mit `\frot` oder `\boxed`.
- Bei Sachaufgaben mit Einheiten **immer** Einheit im Ergebnis:
  `\boxed{r = \unit[2]{cm}}` — niemals nur `\boxed{r = 2}`.

### 5.4 Spezialmuster: Produkt-/Ketten-/Quotientenregel

Etabliertes Layout :
**linke Spalte** mit der schrittweisen Rechnung, **rechte Spalte** mit der
farblich passenden Definitionsliste.

```latex
\begin{minipage}[t]{11cm}
  \begin{scriptsize}\begin{tabular}{c r l}
    (a) & $f'(x)$ & $= \fblau{u(x)} \cdot \forange{v'(x)} + \fcyan{u'(x)} \cdot \frot{v(x)}$\\
        &         & $= \fblau{x} \cdot \forange{2} + \fcyan{1} \cdot \frot{(2x+3)}$\\
        &         & $= 2x + (2x+3)$\\
        &         & $= \boxed{4x+3}$
  \end{tabular}\end{scriptsize}
\end{minipage}
\hfill
\begin{minipage}[t]{4cm}
  \begin{scriptsize}\begin{tabular}{| l}
    \fblau{u(x) = x}\\
    \fcyan{u'(x) = 1}\\
    \frot{v(x) = 2x+3}\\
    \forange{v'(x) = 2}
  \end{tabular}\end{scriptsize}
\end{minipage}
```

**Farbzuordnung (verbindlich):**

| Regel | blau | cyan | rot | orange |
|-------|------|------|-----|--------|
| Produktregel | $u(x)$ | $u'(x)$ | $v(x)$ | $v'(x)$ |
| Kettenregel | $g(x)$ | $g'(x)$ | $h(x)$ | $h'(x)$ |
| Quotientenregel | $u(x)$ | $u'(x)$ | $v(x)$ | $v'(x)$ |

Vor der ersten Lösung dieses Musters eine kurze Hinleitung:
> „Im Folgenden wird die Funktion $f$ stets durch $f(x) = u(x) \cdot v(x)$
> als Produkt der beiden Funktionen $u$ und $v$ betrachtet, um die
> Produktregel anwenden zu können."

---

## 6. Mathematische Notation (verbindlich)

### 6.1 Aus `newcommands.tex`

| Befehl | Bedeutung |
|--------|-----------|
| `\N \Z \Q \R \C` | $\mathbb{N}, \mathbb{Z}, \mathbb{Q}, \mathbb{R}, \mathbb{C}$ |
| `\cP` | Potenzmenge $\mathcal{P}$ |
| `\eps` | $\varepsilon$ |
| `\limn` | $\lim_{n \to \infty}$ |
| `\limh` | $\lim_{h \to 0}$ |
| `\limxto{a}` | $\lim_{x \to a}$ |
| `\dx` | $\,\mathrm{d}x$ (für Integrale) |
| `\d{t}` | $\,\mathrm{d}t$ (beliebige Integrationsvariable) |
| `\norm{v}` | $\lVert v \rVert$ |
| `\vektor{x}{y}{z}` | dreidim. Spaltenvektor |
| `\punktvektor{x}{y}` | zweidim. Spaltenvektor |
| `\E \V` | Erwartungswert, Varianz |
| `\dis{\frac{a}{b}}` | Displaystyle-Bruch im Fließtext |
| `\gegges{geg}{ges}` | Gegeben/Gesucht zweispaltig |
| `\luecke{Text}` | unterstrichene Lücke in Textbreite |
| `\fk{Begriff}` | fett-kursiv, neuer Begriff |
| `\uproman{2025}` | römische Zahl MMXXV |

### 6.2 Aus Paketen

| Befehl | Bedeutung |
|--------|-----------|
| `\unit[Wert]{Einheit}` | Wert mit Einheit, z. B. `\unit[10]{cm}`, `\unit[4]{cm^2}` |
| `\degree` | ° (Gradsymbol) |
| `\euro{}` | € |
| `\nicefrac{a}{b}` | $^a\!/_b$ — schmaler Inline-Bruch |
| `\dfrac{a}{b}` | großer Bruch (auch inline) |
| `\boxed{...}` | gerahmtes Endergebnis |
| `\ding{52}` `\ding{56}` | ✓ und ✗ (pifont) |

### 6.3 Konventionen

- **Lineare Funktionen:** $f(x) = m \cdot x + n$ — **niemals** $mx + b$.
- **Lineare Gleichungssysteme:** Variablen $x, y$ oder kontextpassend
  ($e, k$ für Erwachsene/Kinder etc.). Variablen **vorab in einem Satz
  einführen**, bevor sie in Gleichungen auftauchen.
- **Dezimalzahlen:** deutsche Schreibweise mit Komma als `4{,}50` (geschützt,
  damit kein Abstand entsteht).
- **Umlaute:** direkt im Quelltext (`ä, ö, ü, ß`), niemals als `\"a`.
- **Compiler:** `pdflatex` — keine XeLaTeX-/LuaLaTeX-Pakete einbauen.

---

## 7. Farbige Formeln (für Lösungen)

```latex
\frot{...}   \fblau{...}   \fgruen{...}   \fmagenta{...}
\forange{...}   \fcyan{...}   \folive{...}
```

- Standardgebrauch: `\frot` für **das Ergebnis** in Kurzlösungen.
- Farbcode für Produkt-/Ketten-/Quotientenregel siehe 5.4.
- Mehr als drei Farben pro Aufgabe vermeiden (Lesbarkeit).

---

## 8. Boxen (nur Merksätze und Lösungs-Boxen)

```latex
\begin{merke}  …  \end{merke}      % rot, Titel "Merke:"
\begin{merke2} …  \end{merke2}     % Variante mit gefülltem Titelbalken
\begin{solution} …  \end{solution} % grau, Titel "Lösung:"
\begin{todo} …  \end{todo}         % orange/gelb, ohne Titel
```

**Niemals** Aufgabentexte in tcolorboxen. Aufgaben **immer** in
`enumerate[(1)]`.

`\begin{solution}` ist primär für **einzelne, sehr kurze Beispiel-Lösungen
im Aufgabenteil** gedacht (etwa zur Vorgabe eines Lösungsbeispiels). Der
**reguläre Lösungsteil** des Arbeitsblatts steht nicht in einer Box, sondern
im Format aus Abschnitt 5.

---

## 9. Layout-Helfer

| Zweck | Befehl |
|-------|--------|
| zwei-/mehrspaltiger Satz | `\begin{multicols}{n} … \end{multicols}` |
| Spalten-Trenner (manuell) | `\columnbreak` |
| Trennlinie im Lösungsteil | `\hrule` |
| Trennlinie im Aufgabenteil | `\noindent\rule{\linewidth}{0.3pt}` |
| Lückenzeile | `\luecke{Platzhaltertext}` |
| Seitenumbruch | `\newpage` |
| Unterstreichung bis Zeilenende | `\uline{\hfill}` |
| Tabellenstreckung (gesetzt) | `\renewcommand{\arraystretch}{1.25}` |

---

## 10. TikZ — Koordinatensysteme und geometrische Figuren

### 10.1 Funktionsgraph (Standard-AB)

```latex
\begin{tikzpicture}[scale=0.42]
  % Gitter
  \foreach \x in {-6,...,6} \draw[gray!30, thin] (\x,-6) -- (\x,6);
  \foreach \y in {-6,...,6} \draw[gray!30, thin] (-6,\y) -- (6,\y);
  % Achsen
  \draw[-latex, thick] (-6.3,0) -- (6.5,0) node[right] {$x$};
  \draw[-latex, thick] (0,-6.3) -- (0,6.5) node[above] {$y$};
  % Beschriftungen
  \foreach \x in {-6,-4,-2,2,4,6}
    \draw (\x,0.1) -- (\x,-0.1) node[below, font=\tiny] {$\x$};
  \foreach \y in {-6,-4,-2,2,4,6}
    \draw (0.1,\y) -- (-0.1,\y) node[left, font=\tiny] {$\y$};
  % Graph — IMMER in clip-scope
  \begin{scope}
    \clip (-6,-6) rectangle (6,6);
    \draw[blue, thick, domain=-6:6, samples=200] plot (\x, {2*\x - 1});
  \end{scope}
\end{tikzpicture}
```

| Einstellung | Wert |
|-------------|------|
| Standardskala | `scale=0.42` |
| 3 Graphen nebeneinander | `scale=0.52` |
| Achsenpfeile | `-latex` |
| Tick-Labels | `\tiny` |
| Funktionsbeschriftung | `\scriptsize` |
| Graph | **immer** in `\begin{scope}\clip…\end{scope}` |
| Plot-Engine | **reines TikZ** — kein pgfplots |

### 10.2 Geometrische Figuren in Aufgaben

Etablierte Bestandteile:
- Hauptfigur: `\draw[blue, very thick] …`
- Maßlinien / Dimensionspfeile: `\draw[|<->|, red, thick] … -- node[…] {$a$} …`
- Hervorgehobene Flächen: `\filldraw[gray, opacity=0.5] …`
- Eckpunkte: `\coordinate (A) at (…);`, Beschriftung mit
  `\node[below left] at (A) {$A$};`
- Winkel: `\draw[red, thick] … arc[start angle=…, end angle=…, radius=…];`

Geometrische Skizze typischerweise in `\begin{multicols}{2}` neben den
Teilaufgaben, mit `\columnbreak` als Trenner und `\centering` vor der
`tikzpicture`.

### 10.3 Verfügbare TikZ-Bibliotheken (aus `header.tex`)

`arrows`, `calc`, `angles`, `plotmarks`, `quotes`, `babel`, `intersections`,
`shapes.geometric`, `decorations.pathreplacing`, `automata`, `positioning`,
`shadows`, `patterns`, `patterns.meta`.

---

## 11. Multiple-Choice (selten in Arbeitsblättern)

```latex
\begin{mcquestionh}{Aufgabentext}
  \answerh{A} & \answerh{B} & \answerh{C} & \answerh{D} & \answerh{E}
\end{mcquestionh}

\begin{mcquestionv}{Aufgabentext}
  \answerv{Antwort A}
  \answerv{Antwort B}
\end{mcquestionv}
```

Hauptsächlich für MC-Fragen Abi und vereinzelt für „Markiere die richtige
Aussage"-Aufgaben.

---

## 13. Checkliste vor dem Kompilieren

- [ ] Pfad `\input{../../../../header.tex}` und `…/newcommands.tex` korrekt?
- [ ] Kein `\documentclass`, kein `\section`, kein `\subsection`?
- [ ] Titel als zentriertes `\textbf{\Large{...}}`?
- [ ] Aufgaben in `enumerate[(1)]`, Teilaufgaben in `[(a)]`?
- [ ] **Jede** Aufgabe beginnt mit einem Operator im Imperativ — keine W-Frage?
- [ ] Du-Form (5–10) bzw. Sie-Form (11–12) durchgängig?
- [ ] Einheiten mit `\unit[…]{…}`, Dezimalkomma als `4{,}50`?
- [ ] Lineare Funktionen $f(x) = mx + n$ (nicht $mx + b$)?
- [ ] Lösungsteil auf neuer Seite (`\newpage`)?
- [ ] Lösungsteil in `\begin{scriptsize}\begin{enumerate}[(1)]…`?
- [ ] Aufgaben im Lösungsteil mit `\hrule` getrennt?
- [ ] Endergebnisse mit `\frot{…}` (Kurzlösungen) oder `\boxed{…}` (mit
  Einheit) hervorgehoben?
- [ ] Variablen vor Verwendung im Text deklariert (bei Textaufgaben)?
- [ ] Probe vorhanden, wo sinnvoll (`\ding{52}`)?
- [ ] TikZ-Graphen in `\begin{scope}\clip…\end{scope}`?
- [ ] Umlaute direkt im Quelltext, nicht als `\"a`?

---

## 14. Offene Punkte / Nachzuliefern

- **Offizielle Operatorenliste** (siehe 4.2) — wird hier eingepflegt,
  sobald geliefert.
- Eventuell: feste Konvention, wann `\frot` und wann `\boxed` für Endergebnisse
  benutzt wird (aktueller Vorschlag in 5.2: `\frot` für Klassen 5–9 und
  Kurzlösungen, `\boxed` ab Klasse 10 mit Einheiten).
- Eventuell: einheitliche Hinleitungssätze für Produkt-/Ketten-/Quotientenregel
  in 5.4.
