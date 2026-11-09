# Befehle und Pakete der universalen Stildateien

Automatisch erzeugt mit `werkzeuge/makros_auflisten.py` aus `assets/newcommands.tex` und
`assets/header.tex`. Vor dem Anlegen eines neuen Befehls hier nachsehen, ob es schon
etwas Gleichwertiges gibt.

## Mathematische Kürzel

| Befehl | Zweck |
|---|---|
| `\dis{…}` | vereinfachte Schreibweise für den Displaystyle |
| `\N` | natürliche Zahlen |
| `\Z` | ganze Zahlen |
| `\Q` | rationale Zahlen |
| `\R` | reelle Zahlen |
| `\C` | komplexe Zahlen |
| `\cP` | Potenzmenge |
| `\eps` | Kürzel für Epsilon |
| `\limn` | Grenzwert für n gegen Unendlich |
| `\limh` | Grenzwert für h gegen Null |
| `\limxto{…}` | beliebiger funktionaler Grenzwert x gegen .... |
| `\dx` | dx Operator für Integrale |
| `\d{…}` | Operator für beliebige Integrationsvariable |
| `\norm{…}` | \norm{...} für die Normdarstellung \|\|...\|\| |
| `\vektor{…}{…}{…}` | dreidimensionaler Vektor |
| `\punktvektor{…}{…}` | zweidimensionaler Vektor |
| `\E` | Erwartungswert |
| `\V` | Varianz |
| `\gegges{…}{…}` | Umgebung für gegeben und gesucht |

## Verschiedene  hilfreiche Kürzel

| Befehl | Zweck |
|---|---|
| `\uproman{…}` | römische Darstellung einer Zahl \uproman{2021} ergibt MMXXI |
| `\luecke{…}` | Automatisch erstellte Lücke wie die Länge des Textes mit \luecke{<Text>} |
| `\fk{…}` | fett-kursive Schrift für neu eingeführte Begriffe |
| `\leicht` | Schwierigkeitsstufen für Aufgaben mit \leicht , \mittel , \schwer |
| `\mittel` | Schwierigkeitsstufen für Aufgaben mit \leicht , \mittel , \schwer |
| `\schwer` | Schwierigkeitsstufen für Aufgaben mit \leicht , \mittel , \schwer |

## Verschiedene Farben

| Befehl | Zweck |
|---|---|
| `\frot{…}` | rote Formel für Lösungen |
| `\fgruen{…}` | grüne Formel für Lösungen |
| `\fblau{…}` | blaue Formel für Lösungen |
| `\fmagenta{…}` | magenta-farbige Formel für Lösungen |
| `\forange{…}` | orangene Formel für Lösungen |
| `\fcyan{…}` | cyan-farbige Formel für Lösungen |
| `\folive{…}` | olive-farbige Formel für Lösungen |
| `Farbe plum` | Custom made colors |
| `Farbe chameleon` | Custom made colors |
| `Farbe cornflower` | Custom made colors |
| `Farbe scarlet` | Custom made colors |
| `Farbe brick` | Custom made colors |
| `Farbe sunrise` | Custom made colors |
| `Farbe lightblue` | Custom made colors |
| `Farbe carolina` | Custom made colors |

## Kopfzeilen für Leistungsüberprüfungen

| Befehl | Zweck |
|---|---|
| `\lk{…}{…}` | Definition Kopfzeile für Leistungskontrolle mit \lk{Klasse}{Thema} |
| `\headrulewidth` | Definition Kopfzeile für Leistungskontrolle mit \lk{Klasse}{Thema} |
| `\ka{…}{…}` | Definition Kopfzeile für Klassenarbeit mit \ka{Klasse}{Thema} |
| `\headrulewidth` | Definition Kopfzeile für Klassenarbeit mit \ka{Klasse}{Thema} |
| `\kl{…}{…}` | Definition Kopfzeile für Klausur mit \kl{Klasse}{Thema} |
| `\headrulewidth` | Definition Kopfzeile für Klausur mit \kl{Klasse}{Thema} |
| `\clearfancyheader` | Entfernt den Header für Leistungskontrollen, Klassenarbeiten oder Klausuren |
| `\headrulewidth` | Entfernt den Header für Leistungskontrollen, Klassenarbeiten oder Klausuren |
| `\headheight` | Entfernt den Header für Leistungskontrollen, Klassenarbeiten oder Klausuren |
| `\tu{…}{…}` | Definition Kopfzeile für Tägliche Übungen mit \tu{Klasse}{Thema} |
| `\headrulewidth` | Definition Kopfzeile für Tägliche Übungen mit \tu{Klasse}{Thema} |

## Colorboxes für Hervorhebungen

| Befehl | Zweck |
|---|---|
| `\begin{solution}` | Colorboxes für Lösungen mit \begin{solution}<Text>\end{solution} |
| `\begin{todo}` | Colorboxes für das chronologische Vorgehen |
| `\begin{merke}` | Colorboxes für Merksätze |
| `\begin{merke}` | Colorbox2 für Merksätze |

## MC-Fragen

| Befehl | Zweck |
|---|---|
| `\casket` | Definition des Kästchens zum ankreuzen |
| `\begin{mcquestionh}` | Umgebung für horizontale MC-Fragen |
| `\answerh{…}` | Antwort für horizontale MC-Fragen mit \answerh{<Antwort>} |
| `\begin{mcquestionv}` | Umgebung für vertikale MC-Fragen |
| `\answerv{…}` | Antwort für vertikale MC-Frage mit \answerv{<Antwort>} |

## Tikz Settings

| Befehl | Zweck |
|---|---|
| `\koordinatensystem{…}{…}{…}{…}{…}` | Striche und Zahlen bei allen Vielfachen von Schritt (Standard 2). Innerhalb von tikzpicture[scale=0.42] verwenden. |

## Handreichungen

| Befehl | Zweck |
|---|---|
| `\TikZ` | Schriftzug TikZ im Fließtext (Leerzeichen danach ist eingebaut) |
| `\begin{ausgabe}` | Box für die Ausgabe unter einem Code-Beispiel: erst lstlisting[style=latex], darunter \begin{ausgabe} ... \end{ausgabe} |

## Lautschrift

| Befehl | Zweck |
|---|---|
| `\ipa` | Lautschrift in eckigen Klammern mit \ipa{"a:b@nt} – schaltet das babel-Kürzel " vorher aus (sonst wird "a zu ä) |
| `\ipa` | Lautschrift in eckigen Klammern mit \ipa{"a:b@nt} – schaltet das babel-Kürzel " vorher aus (sonst wird "a zu ä) |

## Sprechblasen

| Befehl | Zweck |
|---|---|
| `\lehrerblase{…}{…}` | Sprechblase mit Zipfel links unten (Lehrkraft) mit \lehrerblase[TikZ-Optionen]{Text} (benötigt shapes.callouts) |
| `\schuelerblase{…}{…}` | Sprechblase mit Zipfel rechts unten (Schülerin/Schüler) mit \schuelerblase[TikZ-Optionen]{Text} |

## TikZ-Stile für Programmablaufpläne

| Befehl | Zweck |
|---|---|
| `TikZ-Stil input` | align=center, damit \\ im Knotentext eine neue Zeile ergibt (ohne align wird \\ stillschweigend verschluckt) |
| `TikZ-Stil operation` | align=center, damit \\ im Knotentext eine neue Zeile ergibt (ohne align wird \\ stillschweigend verschluckt) |
| `TikZ-Stil condition` | align=center, damit \\ im Knotentext eine neue Zeile ergibt (ohne align wird \\ stillschweigend verschluckt) |
| `TikZ-Stil output` | align=center, damit \\ im Knotentext eine neue Zeile ergibt (ohne align wird \\ stillschweigend verschluckt) |

## TikZ-Stile für UML-Klassendiagramme

| Befehl | Zweck |
|---|---|
| `TikZ-Stil umlclass` | Klasse mit drei Teilen: Name, Attribute, Methoden (benötigt shapes.multipart) |
| `TikZ-Stil inherit` | Vererbung |
| `TikZ-Stil compose` | Komposition |
| `TikZ-Stil aggregate` | Aggregation |
| `TikZ-Stil associate` | Assoziation |
| `TikZ-Stil depend` | Abhängigkeit |

## Listing Settings

| Befehl | Zweck |
|---|---|
| `style=latex` | Verwendung: \begin{lstlisting}[style=latex] ... \end{lstlisting}, darunter \begin{ausgabe} ... \end{ausgabe} |
| `style=latexnummeriert` | Variante mit Zeilennummern: \begin{lstlisting}[style=latexnummeriert] |

## Pakete in header.tex

| Paket | Zweck |
|---|---|
| `inputenc` | UTF-8 als Zeichenkodierung  ... ABER nicht immer notwendig, je nach Compiler |
| `fontenc` | Verwendet westeuropäische Schriftkodierung |
| `babel` | Ermöglicht deutsche Übersetzung und Silbentrennung |
| `lmodern` | Verwendet moderne Schriftarten |
| `geometry` | Ermöglicht die Ausrichtung des Blattes mit \geometry{...} |
| `fancyhdr` | Ermöglicht die Gestaltung einer Kopfzeile für LK's oder KA's |
| `lscape` | Ermöglicht eventuelles Querformat des Blattes mit \begin{landscape} ... \end{landscape} |
| `pdfpages` | Ermöglicht einbinden PDF-Dokumente bzw. einzelene Seiten mit \includepdf[pages={1,3,5}]{Dateiname} bzw. pages=- |
| `layout` | Ermöglicht es mit den Befehl \layout sich die Default-Layout beschreiben zu lassen (Bild vom Layout) |
| `enumitem` | Ermöglicht die Nummerierung selbst festzulegen mit \begin{enumerate}[Art der Nummerierung] ...   \end{enumerate} |
| `setspace` | Ermöglicht verschiedene Funktion zur Abstandsregelung, z.B.: \hspace{2.5cm} ; \onehalfspacing |
| `csquotes` | Ermöglicht den deutschen Zitierstil darstellen zu lassen mt \enquote{Zitat} |
| `multicol` | Ermöglicht gleichgroße Aufteilung des Dokuments in n Spalten mit \begin{multicols}{n} ... \end{multicols} |
| `xcolor,colortbl` | Ermöglicht Zeilen, Spalten und Zellen einer Tabelle zu färben |
| `caption` | Ermöglicht die Bezeichnung und Strukturierung von Abbildungen oder Quellcode |
| `fancybox` | Ermöglicht die Umrandung einzelner Abschnitte |
| `tcolorbox` | Ermöglicht die Nutzung von Colorboxen für Merksätze, Lösungen, Definitionen, usw mit \newtcolorbox |
| `ifthen` | Ermöglicht \ifthenelse Befehle |
| `amsmath, amssymb, mathrsfs, amsfonts, amsthm, dsfont` | sämtliche Pakete für mathematische Zeichen, Symbole und Formelsatz |
| `units` | Ermöglicht die Angabe von Einheiten mit \unit[Wert]{Einheit} |
| `gensymb` | Ermöglicht Nutzung von \degree für das macro des Grad-Symbols ° |
| `eurosym` | Ermöglicht die Nutzung von \euro{} |
| `pifont` | Ermöglicht die Nutzung verschiedener Fonts, z.B.: \ding{42} , \ding{52} , \ding{56} |
| `tikzsymbols` | Ermöglicht die Nutzung von u.a. Smileys und anderen Symbolen, z.B.: \Winkey , \Smiley[1.5] |
| `tikz` | \begin{tikzpicture} .... \end{tikzpicture} |
| `pgf, pgfplots` | Ermöglicht 2D und 3D Plof-Funktion |
| `animate` | animierte Darstellungen |
| `graphicx` | \includegraphics[width=..px,height=..px]{Dateiname} |
| `multirow` | Zellen über mehrere Zeilen mit \multirow{n}{*}{Text} |
| `array` | erweiterte Spaltentypen, z.B. >{\centering\arraybackslash}p{2cm} |
| `booktabs` | schöne Tabellenlinien \toprule, \midrule, \bottomrule |
| `longtable` | Tabellen über mehrere Seiten |
| `hologo` | \hologo{LaTeX} |
| `suetterl` | Sütterlin als Schriftart mit \mathfrak{Text} |
| `qrcode` | Einbindung eines QR-Codes |
| `url` | Einbindung eines URL-Links |
| `ccicons` | Creative Commons Symbole |
| `listings` | \begin{lstlisting} ... \end{lstlisting} |
| `struktex` | Struktogrammdarstellung |
| `ulem` | Unterstreichung mit \uline{} ggf. mit \hfill im Inneren für Unterstrich bis zum Ende der Zeile |
| `xskak` | Schach: Partien und Züge mit \newchessgame, \mainline{1. e4 e5} (lädt skak) |
| `chessboard` | Schachbretter mit \chessboard[setfen=...] |
| `sudoku` | Sudoku-Gitter mit \begin{sudoku} \|5\|3\| \| ... \|. \end{sudoku} |
| `tikzpeople` | Personen-Figuren als TikZ-Knoten, z.B. \node[alice, minimum size=2cm]{}; |
| `tipa` | Lautschrift mit \textipa{...}; [safe], weil tipa sonst \; \: \! \* \s umdefiniert (bricht z.B. \(\;\)) – Langformen sieh |

**TikZ-Bibliotheken:** `arrows`, `calc`, `angles`, `plotmarks`, `quotes`, `babel`, `intersections`, `shapes.geometric`, `decorations.pathreplacing`, `automata`, `positioning`, `shadows`, `patterns`, `patterns.meta`, `fit`, `shapes.multipart`, `arrows.meta`, `shapes.callouts`, `circuits.logic.US`, `circuits.logic.IEC`

**Bewusst nicht geladen:** `musixtex` – nur für Musik-Dokumente in der header.tex einkommentieren, weil es `\cup` als Achtelnote umdefiniert (bricht `$A \cup B$`).
