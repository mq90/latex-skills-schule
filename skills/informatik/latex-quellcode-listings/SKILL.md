---
name: latex-quellcode-listings
description: Quellcode in LaTeX mit dem listings-Paket darstellen – Python, Java, HTML, SQL, C und LaTeX selbst, eigene Stile, Code aus Dateien einbinden, Beschriftungen, Umlaute im Code. Verwende diesen Skill immer, wenn Programmcode auf ein Arbeitsblatt, in eine Klausur, eine Präsentation oder eine Handreichung soll, auch für Fehlersuche-Aufgaben mit Code.
---

# Quellcode mit listings

Setzt `latex-grundstil` voraus. `listings` ist in der universalen
`header.tex` geladen, der Stil `latex` (gelber Hintergrund, ohne
Zeilennummern) und `latexnummeriert` stehen in der `newcommands.tex`.

## Grundmuster

```latex
\begin{lstlisting}[language=Python]
def fakultaet(n):
    # Rekursion: n! = n · (n-1)!
    return 1 if n <= 1 else n * fakultaet(n - 1)
\end{lstlisting}

Im Fließtext: \lstinline|print("Hallo")|.

\begin{lstlisting}[language=Java, caption=Hallo Welt, label=lst:hallo]
System.out.println("Hallo Welt");
\end{lstlisting}
```

Ganze Datei einbinden: `\lstinputlisting[language=Python]{programm.py}`.

Sprachen: `Python`, `Java`, `HTML`, `SQL`, `C`, `TeX`, `[LaTeX]TeX` u. v. m.

## Eigene Stile

Wird ein Sprachstil öfter gebraucht (z. B. Python im Informatikunterricht),
gehört er als `\lstdefinestyle{python}{…}` in die universale
`newcommands.tex` (Abschnitt „Listing Settings“) – nicht ins Dokument.
Vorschlag aus der Stil-Dokumentation:

```latex
\lstdefinestyle{python}{language=Python, basicstyle=\small\ttfamily,
  keywordstyle=\bfseries\color{blue}, commentstyle=\itshape\color{green!50!black},
  stringstyle=\color{red!70!black}, numbers=left, numberstyle=\tiny\color{gray},
  numbersep=5pt, breaklines=true, frame=single, backgroundcolor=\color{yellow!10},
  showstringspaces=false, tabsize=2}
```

## Stolpersteine

- **Sonderzeichen im Code:** Die universale `newcommands.tex` setzt per
  `\lstset{literate=…}` Umlaute, ß, ·, €, °, →, ≤, ≥, ≠, –, —, „, “, …, ×, ², ³, π für alle Sprachen.
  Jedes andere Nicht-ASCII-Zeichen bricht mit „Invalid UTF-8 byte sequence“
  ab (getestet) – dann dort in der `literate`-Liste ergänzen. Ein eigener
  Stil mit eigenem `literate=` ersetzt die globale Liste.
- Einrückung in Python ist Bedeutung: Tabs vermeiden, `tabsize` setzen,
  Code nicht automatisch umbrechen lassen, wenn Schüler ihn abtippen sollen
  (`breaklines=false`, lieber kürzere Zeilen).
- `lstlisting` in Makro-Argumenten (z. B. in `\textbf{…}` oder Tabellenzellen
  mit Befehl) funktioniert nicht – dort `\lstinline` oder eine `minipage`.
- `\lstlistingname` heißt in der header.tex bereits „Quellcode“.

## Referenz

Vollständige Handreichung (Grundlagen, Stil-Parameter, Java/HTML/SQL/
Python/C, Dateien einbinden, Beschriftungen):
`references/handreichung_listings.tex`.
