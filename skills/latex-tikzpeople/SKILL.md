---
name: latex-tikzpeople
description: Personen-Figuren (Alice, Bob, Ärztin, Polizist, Koch …) mit dem LaTeX-Paket tikzpeople zeichnen – mit allen Figuren, Optionen, Farben, Sprechblasen und Szenen. Verwende diesen Skill immer, wenn jemand Figuren, Personen, Strichmännchen-Ersatz, Comic-Szenen, Sprechblasen, Alice-und-Bob-Szenarien für Kryptografie oder Netzwerke, Rollen in Sachaufgaben oder eine Handreichung zu tikzpeople in einem LaTeX-Dokument möchte – auch wenn das Paket nicht beim Namen genannt wird.
---

# Figuren mit tikzpeople

tikzpeople stellt Personen als TikZ-Knoten bereit. Eine Figur ist ein normaler
`\node` mit dem Figurennamen als Form – sie lässt sich also wie jeder andere
Knoten positionieren, verbinden und beschriften.

```latex
\usepackage{tikzpeople}               % lädt tikz und positioning mit
\usetikzlibrary{shapes.callouts}      % nur für Sprechblasen

\begin{tikzpicture}
  \node[alice, minimum size=2cm] (A) at (0,0) {};
  \node[bob, mirrored, minimum size=2cm] (B) at (6,0) {};
  \draw[->] (A.east) -- (B.west);
\end{tikzpicture}
```

## Die Figuren (28 empfohlen)

`alice` `bob` `bride` `builder` `businessman` `charlie` `chef` `conductor`
`cowboy` `criminal` `dave` `devil` `duck` `graduate` `groom` `guard` `jester`
`judge` `maninblack` `nun` `nurse` `physician` `pilot` `police` `priest`
`sailor` `santa` `surgeon`

Das Paket enthält eine 29. Figur, `mexican`. Sie zeigt ein Klischee
(Sombrero, Poncho) und gehört nicht auf Unterrichtsmaterial. Nicht verwenden
und nicht in Galerien aufnehmen. Wenn jemand ausdrücklich danach fragt, kurz
erklären, warum sie fehlt.

Die Übersicht als PDF erzeugt `assets/galerie_tikzpeople.tex`.

## Optionen

| Option | Wirkung |
|---|---|
| `minimum size=2cm` | Größe (ohne Angabe sehr klein, ca. 0,5 cm) |
| `mirrored` | Figur spiegeln (schaut nach links statt rechts) |
| `female` | weibliche Variante – wirkt nur bei manchen Figuren |
| `evil` | Hörner (z. B. für Angreifer) |
| `good` | Heiligenschein |
| `monitor` | Bildschirm vor der Figur (Computer, Netzwerk) |
| `shield`, `sword` | Schild bzw. Schwert (z. B. Firewall/Verteidigung) |
| `saturated` | kräftigere Farben |
| `shirt=`, `undershirt=`, `skin=`, `hair=`, `hat=` | Farben ändern |
| `pc=`, `halo=`, `horns=`, `shieldmid=` … | Farben der Zusätze |

Paketoptionen: `\usepackage[saturated]{tikzpeople}` (alle kräftig),
`[nobeards]`, `[draft]` (Entwurfsmodus).

**Anker** für Pfeile und Sprechblasen: `mouth`, `north`, `south`, `east`,
`west`, `center`, `base`, `mid`, `text`.

## Stolpersteine (getestet)

- **Keine Farbmischungen direkt in Farb-Optionen.** `skin=brown!60` bricht mit
  „Undefined color `40'“ ab, weil das Paket selbst noch `!70` anhängt.
  Stattdessen vorher benennen:
  `\colorlet{haut}{brown!60}` und dann `skin=haut`.
- **Inhalt leer lassen:** `\node[alice]{};` – Text im Knoten verschiebt die Figur.
  Namen per `\node[below=1mm of A] {Alice};` darunter setzen.
- **Größe immer angeben**, sonst sind die Figuren winzig.
- Sprechblase: `\node[ellipse callout, draw, fill=white,
  callout absolute pointer={(A.mouth)}] at (1,2) {Hallo!};`
  Für Gedanken `cloud callout` mit `aspect=2.5`.

## Vielfalt

Mit `skin=` und `hair=` lassen sich Hauttöne und Haarfarben variieren. Bei
Szenen mit mehreren Personen bewusst mischen, damit nicht alle gleich aussehen.

## Szenen und Vorlagen

- `assets/vorlage_alice_bob_eve.tex` – Kryptografie-Szenario mit Sprech- und
  Gedankenblase. Passt zu Caesar, Vigenère, Steganografie, Schlüsselaustausch.
- Weitere Ideen für Informatik: `monitor` für Client/Server, `evil` als
  Angreifer (Mallory), `shield` als Firewall, `police` als Zertifizierungsstelle.
- Mathematik: Personen in Sachaufgaben („Der Koch braucht …“), Rollen bei
  Wahrscheinlichkeitsaufgaben.

## Für eine Handreichung

`assets/stil_handreichung.tex` daneben legen und mit `\input{stil_handreichung}`
einbinden. tikzpeople läuft auch in den `beispiel`-Kästen (Code links,
Ergebnis rechts). Jedes Beispiel kompilieren und das PDF als Bild prüfen.
