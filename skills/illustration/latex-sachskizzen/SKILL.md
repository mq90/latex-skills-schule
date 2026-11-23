---
name: latex-sachskizzen
description: Kleine lehrbuchartige Illustrationen zu Text- und Sachaufgaben mit TikZ zeichnen – maßstäbliche Szenen (Springbrunnen, Kugelstoß, Hängebrücke, Torbogen mit Lkw, Brückenbogen mit Schiff, Freistoß, Leiter, Schattenwurf, Steigung), Emoji-Figuren mit twemojis, Untergründe, Flugbahnen, dezente Maßlinien, Lösungsbild mit Koordinatensystem hinter der Skizze, Emoji-Köpfe mit Sprechblasen für Fehlersuch-Aufgaben. Verwende diesen Skill IMMER, wenn eine Sachaufgabe, Textaufgabe oder Fehlersuche auf einem Arbeitsblatt, in einer Leistungskontrolle oder Klassenarbeit eine Skizze, Illustration, ein Bild zur Situation oder „Emoji-Männchen“ bekommen soll – auch wenn nur „mach das anschaulicher“ gesagt wird.
---

# Illustrationen zu Sachaufgaben

Setzt `latex-grundstil` voraus. In der universalen `header.tex` sind `twemojis`,
`tikzpeople`, `calc`, `shapes.callouts` und `shadows` geladen; die Befehle unten
stehen in der `newcommands.tex`.

## Die drei Leitlinien

1. **In Metern zeichnen.** Maßstab einmal in die Optionen
   (`[x=0.5cm, y=0.5cm]` = 1 m entspricht 0,5 cm), beide Achsen gleich.
   Danach sind alle Koordinaten die Zahlen aus der Aufgabe.
2. **Nur zeigen, was gegeben ist.** Keine Ergebnisse im Aufgabenbild
   (kein Scheitelpunkt, keine Nullstelle, kein berechneter Wert).
3. **Sparsam bemaßen.** Höchstens zwei bis drei Maße, dünn und grau
   (`\masslinie`), nicht rot. Mehrere Entfernungen auf einer Linie als
   Entfernungsleiste. Lieber `x` und `h(x)` zeigen als Zahlen.

## Befehle (newcommands.tex)

| Befehl | Wirkung |
|---|---|
| `\emojifigur[Optionen]{(x,y)}{Name}{Höhe}` | Emoji steht auf dem Punkt; Höhe = Größe in m × Maßstab; `xscale=-1` spiegelt, `rotate=7` dreht |
| `\masslinie{(x1,y1)}{(x2,y2)}{Text}` | dezente Maßlinie, Text mittig auf weißem Grund |
| `\skizzenraster{xmin}{xmax}{ymin}{ymax}{Schritt}{x-Liste}{y-Liste}` | Koordinatensystem hinter der Skizze (Gitter, Achsen, Beschriftungen aus den Listen) |
| `\skizzenpunkt{(x,y)}{Lage}{Text}` | markanter Punkt im Lösungsbild |
| `\emojisprecher[Breite]{x}{Emoji}{Name}{Aussage}` | Emoji-Kopf, Name darunter, Sprechblase darüber |
| `\ifmitKS … \else … \fi` | Schalter: Lösungsbild mit Koordinatensystem / Aufgabenbild |

## Grundgerüst einer Skizze

Reihenfolge der Ebenen: Untergrund → Gegenstände und Figuren → Kurve →
Beschriftung.

```latex
\begin{tikzpicture}[x=0.5cm, y=0.5cm]   % 1 m entspricht 0,5 cm
	\fill[green!25] (-1.2,-0.45) rectangle (11.2,0);            % Wiese
	\draw[thick, green!40!black] (-1.2,0) -- (11.2,0);
	\draw[blue!35, line width=3pt, line cap=round, domain=0:10, samples=100] plot (\x,{-0.2*(\x-5)^2+5});
	\draw[blue!75, line width=1.1pt, line cap=round, domain=0:10, samples=100] plot (\x,{-0.2*(\x-5)^2+5});
	\emojifigur{(8.5,0)}{man standing}{0.9cm}                   % 1,80 m groß
	\masslinie{(0,-1.1)}{(8.5,-1.1)}{$\unit[8{,}5]{m}$}
\end{tikzpicture}
```

Maßstab nach Platz wählen: neben dem Text 5–7 cm Bildbreite, über die volle
Breite bis 14 cm (10 m → `0.5cm`, 20 m neben dem Text → `0.28cm`,
20 m volle Breite → `0.6cm`, 100 m → `0.05cm`).

## Figuren: Emojis

`\twemoji[height=1cm]{man standing}`; Namen = englische Unicode-Namen klein.
Hauttöne mit Doppelpunkt: `girl: medium skin tone` (light, medium-light,
medium, medium-dark, dark). Bei mehreren Personen bewusst mischen.

- Ganze Personen: `man standing`, `woman standing`, `person standing`,
  `person walking`, `person running`, `person biking`, `person swimming`,
  `person playing handball` (Werfer), `person bouncing ball`, `person climbing`
- Köpfe für Dialoge: `boy`, `girl`, `child`, `man`, `woman`, `person`,
  `man teacher`, `woman teacher`, `thinking face`
- Dinge: `soccer ball`, `basketball`, `goal net`, `skateboard`, `kite`,
  `automobile`, `delivery truck`, `bus`, `bicycle`, `ship`, `sailboat`,
  `airplane`, `rocket`, `house`, `deciduous tree`, `sun`, `fountain`,
  `ladder`, `light bulb`, `stopwatch`

Fahrzeuge **von vorn** (Lkw im Torbogen, Schiff unter der Brücke) selbst aus
Rechtecken bauen – Umriss exakt nach den Maßen der Aufgabe (Vorlagen in der
Handreichung, Kapitel 7). Für Schwarz-Weiß-Druck das Piktogramm aus der
Handreichung (Kapitel 4.4) statt Emojis.

## Lösungsbild: Koordinatensystem hinter der Skizze

Skizze als Befehl in der Präambel des Arbeitsblatts definieren und mit
`\ifmitKS` verzweigen. Aufgabenteil: `\skizzeKugelstoss`, Lösungsteil:
`{\mitKStrue \skizzeKugelstoss}` (Klammern, damit der Schalter wieder aus ist).

```latex
\begin{tikzpicture}[x=0.5cm, y=0.5cm]
	\skizzenraster{-1}{11}{0}{4}{1}{2,4,6,8,10}{1,2,3,4}
	\draw[thick, orange!50!black] (-2,0) -- (11.2,0);
	\emojifigur[xscale=-1]{(-0.85,0)}{person playing handball}{1.25cm}
	\draw[akzentblau, thick, domain=0:10, samples=100] plot (\x,{-0.1*(\x-4)^2+3.6});
	\skizzenpunkt{(0,2)}{above left}{$(0\,|\,2)$}
	\skizzenpunkt{(4,3.6)}{above}{$S(4\,|\,3{,}6)$}
	\skizzenpunkt{(10,0)}{above right}{$N(10\,|\,0)$}
\end{tikzpicture}
```

- Raster **vor** den Gegenständen zeichnen; gefüllte Untergründe im
  Lösungsbild weglassen (`\ifmitKS … \else \fill… \fi`), gefüllte Mauern mit
  `\fill[white, opacity=0.55]` aufhellen und das Raster danach setzen.
- Im Lösungsbild: Graph durchgezogen in `akzentblau`, Scheitelpunkt,
  Nullstellen und berechnete Punkte mit `\skizzenpunkt`, keine Maßlinien.
- Vollständige Vorlage (Aufgabe + Lösung): `assets/vorlage_sachaufgabe_mit_skizze.tex`.

## Fehlersuche als Gespräch

```latex
\begin{tikzpicture}
	\emojisprecher{0}{boy}{A}{\textbf{(i)} Der Scheitelpunkt ist $S(3\,|\,1)$.}
	\emojisprecher{2.8}{girl: medium skin tone}{B}{\textbf{(ii)} Der Graph ist nach oben geöffnet.}
	\emojisprecher{5.6}{boy: medium-dark skin tone}{C}{\textbf{(iii)} Der Graph ist gestreckt.}
\end{tikzpicture}
```

Abstand der Köpfe 2,7–2,8 cm bei Blasenbreite 2,3 cm; sechs Köpfe füllen eine
Zeile. Nummern (i), (ii) … in die Blasen, damit die Lösung darauf verweisen
kann. Zwei Personen im Dialog und der Notizzettel mit fehlerhafter Rechnung:
Handreichung, Kapitel 10.

## Einbau ins Arbeitsblatt

- Skizze neben dem Text: zwei `minipage[t]` (Text 0,56–0,62, Bild 0,36–0,42),
  im Bild-Kasten zuerst `\vspace{0pt}\centering`. Steht ein Makro wie `\mittel`
  am Anfang der Text-minipage, `\leavevmode` davorsetzen.
- Breite Szenen (Freistoß) zentriert zwischen Aufgabentext und Teilaufgaben.
- Lösungsteil: Rechnung links (`\raggedright`), rechts
  `\resizebox{\linewidth}{!}{{\mitKStrue \skizze…}}`.
- Aufgabenstellungen weiter nach `latex-grundstil` (Operatoren, keine W-Fragen).

## Stolpersteine (getestet)

- `\clip[even odd rule]` gibt einen Fehler – die Option an die `scope`
  oder an `\fill` setzen.
- Ein großzügiger `\clip` (z. B. bis y = −20) vergrößert die Bounding Box und
  erzeugt eine Lücke unter dem Bild – Ausschnitt knapp wählen.
- `pattern=bricks` und `pattern=crosshatch` erscheinen nicht in jedem
  PDF-Betrachter – Fugen und Netze aus `\foreach`-Schleifen zeichnen.
- tikzpeople-Figuren sind Büsten ohne Beine – nicht maßstäblich verwendbar.
  Farbmischungen dort nie direkt in `shirt=`/`skin=` (siehe `latex-tikzpeople`).
- In einem Dokument mit **eigener** Präambel Pakete wie `tikzpeople` vor
  `\singlespacing` laden; danach geladen, meldet pgf beim Laden von
  `arrows.meta` „You can't use \unskip in vertical mode“.
- In `plot` immer `(\x-4)^2` klammern (siehe `latex-tikz-grundlagen`).

## Referenz

Ausführliche Handreichung mit allen Bausteinen und neun vollständigen
Beispielen: `references/handreichung_sachskizzen.tex` (PDF unter
`handreichungen/illustration/`). Verwandte Skills: `latex-sprechblasen`,
`latex-tikzpeople`, `latex-funktionsgraphen`, `latex-geometrie`.
