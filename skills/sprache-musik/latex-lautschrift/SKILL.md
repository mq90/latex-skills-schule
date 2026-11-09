---
name: latex-lautschrift
description: Lautschrift (IPA, phonetische Umschrift) in LaTeX setzen – mit dem Paket tipa unter pdflatex oder mit Unicode-Zeichen unter xelatex, inklusive Lauttabellen für Deutsch und Englisch, Vokalviereck und der Lösung für den Konflikt mit babel (aus "a wird ä). Verwende diesen Skill immer, wenn jemand Aussprache, Lautschrift, IPA-Zeichen, Vokabellisten mit Aussprache, Phonetik, ein Vokalviereck oder eine Handreichung zu tipa in einem LaTeX-Dokument braucht – auch für Englisch-, Französisch- oder DaZ-Material.
---

# Lautschrift mit LaTeX

Es gibt zwei Wege. Vor dem Schreiben entscheiden, welcher passt:

| | **tipa** (pdflatex) | **Unicode** (xelatex/lualatex) |
|---|---|---|
| Eingabe | ASCII-Kürzel: `\textipa{"mE:tC@n}` | Zeichen direkt: `ˈmɛːtçən` |
| Vorteil | läuft überall, auch in bestehenden pdflatex-Dokumenten | lesbarer Quelltext, Kopieren aus Wörterbüchern möglich |
| Nachteil | Kürzel muss man lernen; Konflikt mit babel | braucht eine Schrift mit IPA-Zeichen, anderer Compiler |
| Vorlage | `assets/vorlage_lautschrift_tipa.tex` | `assets/vorlage_lautschrift_unicode.tex` |

Faustregel: Bestehendes Dokument mit pdflatex → tipa. Neues Material mit viel
Lautschrift (Vokabellisten, Sprachunterricht) → Unicode.

## Weg 1: tipa mit pdflatex

In der universalen `header.tex` (Skill `latex-grundstil`) ist tipa bereits
geladen – als `\usepackage[safe]{tipa}` – und `\ipa{…}` steht in der
`newcommands.tex`. Für ein eigenständiges Dokument:

```latex
\usepackage[T1]{fontenc}
\usepackage[ngerman]{babel}
\usepackage[safe]{tipa}

% \ipa{...}: Lautschrift in eckigen Klammern, babel-sicher
\makeatletter
\newcommand\ipa{\begingroup\shorthandoff{"}\ipa@aux}
\newcommand\ipa@aux[1]{[\textipa{#1}]\endgroup}
\makeatother
```

### Warum `[safe]` (getestet)

Ohne `safe` definiert tipa `\;`, `\:`, `\!`, `\*` und `\s` um. Dann bricht
z. B. `\(\;\;\)` mit „Argument of \UseTextAccent has an extra }“ ab – und
`\;` steht in fast jeder Mathe-Lösung. Im safe-Modus gibt es dafür die
Kurzformen nicht; stattdessen Langformen verwenden:

| Laut | Kurzform (ohne safe) | Langform (immer) |
|---|---|---|
| n̩ (silbisch) | `\s{n}` | `\textsyllabic{n}` |
| ɹ | `\*r` | `\textturnr` |
| n̥ (stimmlos) | `\r*n` | `\textsubring{n}` |
| ʀ | `\;R` | `\textscr` |

Achtung: Im safe-Modus ergeben `\*r` und `\;R` **ohne Fehlermeldung**
falsche Zeichen (r statt ɹ). Deshalb nur Langformen schreiben.

### Der babel-Konflikt (getestet)

In tipa steht `"` für die Hauptbetonung ˈ. Mit `babel` und `ngerman` ist `"`
aber ein Kurzbefehl für Umlaute: `\textipa{"a:b@nt}` ergibt **ä:bənt**
statt ˈaːbənt. Betroffen sind `"a`, `"o`, `"u`, `"s` (wird ß) und weitere.
`"m`, `"k` usw. gehen zufällig gut, deshalb fällt der Fehler oft erst spät auf.

Lösungen:
1. Das Makro `\ipa{...}` oben verwenden. Es schaltet `"` aus, *bevor* das
   Argument gelesen wird.
2. Einzeln: `{\shorthandoff{"}\textipa{"a:b@nt}}`
3. Ohne Anführungszeichen: `\textipa{\textprimstress a:b@nt}`,
   Nebenbetonung `\textsecstress`.

Grenze: `\ipa` funktioniert nicht im Argument eines anderen Befehls (z. B. in
`\section{…}` oder `\textbf{…}`), weil dort `"` schon gelesen ist. Dort
`\textprimstress` verwenden.

### Wichtigste tipa-Kürzel

Vollständige Tabelle mit Beispielwörtern: `references/tipa-kuerzel.md`
(lesen, sobald konkrete Wörter transkribiert werden sollen).

`I`=ɪ `E`=ɛ `Y`=ʏ `\o`=ø `\oe`=œ `@`=ə `5`=ɐ `U`=ʊ `O`=ɔ `\ae`=æ `2`=ʌ
`A`=ɑ `6`=ɒ `3`=ɜ · `C`=ç `x`=x `S`=ʃ `Z`=ʒ `N`=ŋ `K`=ʁ `P`=ʔ `T`=θ `D`=ð
`\textturnr`=ɹ · `:` lang · `"` Haupt-, `""` Nebenbetonung · `\textsyllabic{n}` silbisch (n̩)
· `\~{a}` nasal

## Weg 2: Unicode mit xelatex

```latex
\usepackage{fontspec}
\usepackage[ngerman]{babel}
\setmainfont{Charis SIL}       % oder Doulos SIL, Gentium Plus
\newcommand\ipa[1]{[#1]}
...
Mädchen \ipa{ˈmɛːtçən}
```

- Kompilieren mit `xelatex`, nicht `pdflatex`.
- Die Schrift muss IPA abdecken. Latin Modern und viele Systemschriften zeigen
  Kästchen oder lassen Zeichen weg. Prüfen: im Log nach „Missing character“
  suchen (`grep -c "Missing character" datei.log` muss 0 ergeben).
- Charis SIL installieren: Debian/Ubuntu `fonts-sil-charis`, sonst
  software.sil.org/charis. Keine Lizenzfrage, die Schrift ist frei (OFL).
- Hier gibt es keinen babel-Konflikt, weil `ˈ` ein eigenes Zeichen ist.

## Vokalviereck

`assets/vorlage_lautschrift_unicode.tex` enthält ein Vokaltrapez mit TikZ
(vorne/hinten, oben/unten, ungerundet links und gerundet rechts vom Punkt).
Für pdflatex die Beschriftungen durch `\textipa{…}` ersetzen.

## Prüfen

Lautschrift sieht man Fehler nicht an, solange man das PDF nicht ansieht.
Nach dem Kompilieren immer als Bild rendern (`pdftoppm -r 100 -png`) und jede
Umschrift mit dem Beispielwort vergleichen. Typische Fehler: ä statt ˈa (babel),
fehlende Zeichen (Schrift), stimmlos (`\textsubring`) statt silbisch
(`\textsyllabic`), Kurzformen im safe-Modus.

## Für eine Handreichung

Aufbau und Listing-Stil aus `latex-grundstil` (Code in
`lstlisting[style=latex]`, Ausgabe direkt darunter in `ausgabe`). Für den
Unicode-Weg muss die Handreichung mit xelatex laufen – dann ein eigenes
Dokument mit `fontspec` statt der universalen `header.tex`.
