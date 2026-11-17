# SPDX-License-Identifier: MIT
"""Englische Übersetzung und Lautschrift für alle Überschriften der Wörterbücher.

Deutsch -> (English, Lautschrift in tipa-Kürzeln; =l und =n stehen für silbisches l und n).
Achtung: Der Doppelpunkt ist in tipa das Längenzeichen, als Satzzeichen deshalb ein Komma setzen.
bauen.py ersetzt damit \\part, \\section und \\subsection* durch \\teil, \\kapitel und \\zwischen.
"""
import re

RS = '"ri:dIN @n "spi:kIN '
RF = '"ri:dIN "fO:mjuli:, '
UEB = {
# Teile und wiederkehrende Zwischenüberschriften
"Wörterbuch": ("Dictionary", '"dIkS@nri'),
"Register": ("Index", '"Indeks'),
"Mathematik lesen und sprechen": ("Reading and speaking mathematics", RS + '""m\\ae T@"m\\ae tIks'),
"Physik lesen und sprechen": ("Reading and speaking physics", RS + '"fIzIks'),
"Chemie lesen und sprechen": ("Reading and speaking chemistry", RS + '"kemIstri'),
"Beispiele": ("Examples", 'Ig"zA:mp=lz'),
"Hinweise zur Lautschrift": ("Notes on the phonetic transcription", '"n@Uts 6n D@ f@"netIk tr\\ae n"skrIpS=n'),
# Mathematik
"Zahlen und Rechenarten": ("Numbers and operations", '"n2mb@z @n ""6p@"reIS=nz'),
"Algebra, Gleichungen und Mengen": ("Algebra, equations and sets", '"\\ae ldZIbr@, I"kweIZ=nz @n "sets'),
"Funktionen": ("Functions", '"f2NkS=nz'),
"Geometrie: Grundbegriffe, Winkel, Abbildungen": ("Geometry: basic terms, angles, transformations", 'dZi"6m@tri, "beIsIk "t3:mz, "\\ae Ng=lz, ""tr\\ae nsf@"meIS=nz'),
"Ebene Figuren": ("Plane figures", '"pleIn "fIg@z'),
"Körper": ("Solids", '"s6lIdz'),
"Analysis": ("Calculus", '"k\\ae lkj@l@s'),
"Vektoren und analytische Geometrie": ("Vectors and coordinate geometry", '"vekt@z @n k@U"O:dIn@t dZi"6m@tri'),
"Stochastik": ("Probability and statistics", '""pr6b@"bIl@ti @n st@"tIstIks'),
"Logik und Beweis": ("Logic and proof", '"l6dZIk @n "pru:f'),
"Zahlen, Zeichen und Schreibweisen": ("Numbers, symbols and notation", '"n2mb@z, "sImb=lz @n n@U"teIS=n'),
"Relationszeichen": ("Relation symbols", 'rI"leIS=n ""sImb=lz'),
"Grundrechenarten": ("The four basic operations", 'D@ "fO: "beIsIk ""6p@"reIS=nz'),
"Rechnen mit Brüchen": ("Calculating with fractions", '"k\\ae lkjuleItIN wID "fr\\ae kS=nz'),
"Potenzen, Wurzeln und Logarithmen": ("Powers, roots and logarithms", '"paU@z, "ru:ts @n "l6g@rID@mz'),
"Zahlbereiche": ("Number sets", '"n2mb@ sets'),
"Mengen": ("Sets", 'sets'),
"Gleichungen und Ungleichungen lösen": ("Solving equations and inequalities", '"s6lvIN I"kweIZ=nz @n ""InI"kw6l@tiz'),
"Winkelfunktionen": ("Trigonometric functions", '""trIg@n@"metrIk "f2NkS=nz'),
"Intervalle und Grenzwerte": ("Intervals and limits", '"Int@v=lz @n "lImIts'),
"Differenzialrechnung": ("Differential calculus", '""dIf@"renS=l "k\\ae lkj@l@s'),
"Integralrechnung": ("Integral calculus", '"IntIgr@l "k\\ae lkj@l@s'),
"Geraden und Winkel": ("Lines and angles", '"laInz @n "\\ae Ng=lz'),
"Dreiecke, Vierecke und Vielecke": ("Triangles, quadrilaterals and polygons", '"traI\\ae Ng=lz, ""kw6drI"l\\ae t@r@lz @n "p6lIg@nz'),
"Der Kreis und seine Teile": ("The circle and its parts", 'D@ "s3:k=l @n Its "pA:ts'),
"Körper berechnen": ("Calculating solids", '"k\\ae lkjuleItIN "s6lIdz'),
"Trigonometrie im Dreieck": ("Trigonometry in triangles", '""trIg@"n6m@tri In "traI\\ae Ng=lz'),
"Koordinaten und Geraden": ("Coordinates and straight lines", 'k@U"O:dIn@ts @n ""streIt "laInz'),
"Kegelschnitte": ("Conic sections", '"k6nIk "sekS=nz'),
"Folgen, Vektoren, Matrizen und Kombinatorik": ("Sequences, vectors, matrices and combinatorics", '"si:kw@nsIz, "vekt@z, "meItrIsi:z @n ""k6mbIn@"t6rIks'),
"Das griechische Alphabet": ("The Greek alphabet", 'D@ "gri:k "\\ae lf@bet'),
"Wurzeln": ("Roots", 'ru:ts'),
"Winkel an geschnittenen Parallelen": ("Angles on parallel lines", '"\\ae Ng=lz 6n "p\\ae r@lel "laInz'),
"Vierecke und regelmäßige Vielecke": ("Quadrilaterals and regular polygons", '""kw6drI"l\\ae t@r@lz @n "regj@l@ "p6lIg@nz'),
"Vektoren und Matrizen": ("Vectors and matrices", '"vekt@z @n "meItrIsi:z'),
"Potenzen": ("Powers", '"paU@z'),
"Ordnungszahlen, Indizes und Aufzählungen": ("Ordinal numbers, subscripts and lists", '"O:dIn=l "n2mb@z, "s2bskrIpts @n "lIsts'),
"Logarithmen": ("Logarithms", '"l6g@rID@mz'),
"Kombinatorik": ("Combinatorics", '""k6mbIn@"t6rIks'),
"Gleichungsarten": ("Types of equations", '"taIps @v I"kweIZ=nz'),
"Folgen und Reihen": ("Sequences and series", '"si:kw@nsIz @n "sI@ri:z'),
"Einteilung der elementaren Funktionen": ("Classification of the elementary functions", '""kl\\ae sIfI"keIS=n @v Di ""elI"mentri "f2NkS=nz'),
"Dezimalzahlen, große Zahlen und Brüche": ("Decimals, large numbers and fractions", '"desIm=lz, "lA:dZ "n2mb@z @n "fr\\ae kS=nz'),
"Der Graph einer Funktion": ("The graph of a function", 'D@ "grA:f @v @ "f2NkS=n'),
"Britisches und amerikanisches Englisch": ("British and American English", '"brItIS @n @"merIk@n "INglIS'),
"Besondere Körper": ("Special solids", '"speS=l "s6lIdz'),
"Besondere Dreiecke": ("Special triangles", '"speS=l "traI\\ae Ng=lz'),
"Beispiel: eine lineare Ungleichung": ("Example: a linear inequality", 'Ig"zA:mp=l, @ "lIni@r ""InI"kw6l@ti'),
"Beispiel: eine lineare Gleichung": ("Example: a linear equation", 'Ig"zA:mp=l, @ "lIni@r I"kweIZ=n'),
# Physik
"Größen, Einheiten und Messen": ("Quantities, units and measurement", '"kw6nt@tiz, "ju:nIts @n "meZ@m@nt'),
"Bewegungen": ("Motion", '"m@US=n'),
"Kräfte und ihre Wirkungen": ("Forces and their effects", '"fO:sIz @n De@r I"fekts'),
"Energie, Arbeit und Leistung": ("Energy, work and power", '"en@dZi, "w3:k @n "paU@'),
"Wärmelehre": ("Thermal physics", '"T3:m=l "fIzIks'),
"Elektrizität und Magnetismus": ("Electricity and magnetism", 'I""lek"trIs@ti @n "m\\ae gn@tIz@m'),
"Schwingungen und Wellen": ("Oscillations and waves", '""6sI"leIS=nz @n "weIvz'),
"Optik": ("Optics", '"6ptIks'),
"Atom- und Kernphysik": ("Atomic and nuclear physics", '@"t6mIk @n "nju:kli@ "fIzIks'),
"Die Basiseinheiten des SI": ("The SI base units", 'Di ""es "aI "beIs ""ju:nIts'),
"Abgeleitete Einheiten mit eigenem Namen": ("Derived units with special names", 'dI"raIvd "ju:nIts wID "speS=l "neImz'),
"Vorsätze für Einheiten": ("Prefixes for units", '"pri:fIksIz f@ "ju:nIts'),
"Einheiten und Größenangaben lesen": ("Reading units and quantities", '"ri:dIN "ju:nIts @n "kw6nt@tiz'),
"Angloamerikanische Einheiten": ("Imperial and US units", 'Im"pI@ri@l @n ""ju: "es "ju:nIts'),
"Temperaturskalen": ("Temperature scales", '"tempr@tS@ skeIlz'),
"Formeln lesen: Mechanik": ("Reading formulae: mechanics", RF + 'mI"k\\ae nIks'),
"Formeln lesen: Elektrizitätslehre": ("Reading formulae: electricity", RF + 'I""lek"trIs@ti'),
"Formeln lesen: Wärme, Wellen, Optik und Atome": ("Reading formulae: heat, waves, optics and atoms", RF + '"hi:t, "weIvz, "6ptIks @n "\\ae t@mz'),
"Experimente beschreiben": ("Describing experiments", 'dI"skraIbIN Ik"sperIm@nts'),
"Diagramme beschreiben": ("Describing graphs", 'dI"skraIbIN "grA:fs'),
"Griechische Buchstaben in der Physik": ("Greek letters in physics", '"gri:k "let@z In "fIzIks'),
"Länge": ("Length", 'leNT'),
"Volumen und Masse": ("Volume and mass", '"v6lju:m @n "m\\ae s'),
"Geschwindigkeit, Druck, Leistung, Energie": ("Speed, pressure, power, energy", '"spi:d, "preS@, "paU@, "en@dZi'),
# Chemie
"Stoffe und ihre Eigenschaften": ("Substances and their properties", '"s2bst@nsIz @n De@ "pr6p@tiz'),
"Laborgeräte und Arbeitsweisen": ("Laboratory apparatus and techniques", 'l@"b6r@tri ""\\ae p@"reIt@s @n tek"ni:ks'),
"Atombau und Periodensystem": ("Atomic structure and the periodic table", '@"t6mIk "str2ktS@r @n D@ ""pI@ri"6dIk "teIb=l'),
"Chemische Bindung": ("Chemical bonding", '"kemIk=l "b6ndIN'),
"Chemische Reaktionen": ("Chemical reactions", '"kemIk=l ri"\\ae kS=nz'),
"Säuren, Basen und Salze": ("Acids, bases and salts", '"\\ae sIdz, "beIsIz @n "sO:lts'),
"Redoxreaktionen und Elektrochemie": ("Redox reactions and electrochemistry", '"ri:d6ks ri"\\ae kS=nz @n I""lektr@U"kemIstri'),
"Organische Chemie": ("Organic chemistry", 'O:"g\\ae nIk "kemIstri'),
"Stoffmenge und chemisches Rechnen": ("Amount of substance and chemical calculations", '@"maUnt @v "s2bst@ns @n "kemIk=l ""k\\ae lkju"leIS=nz'),
"Die Elemente: Namen und Aussprache": ("The elements: names and pronunciation", 'Di "elIm@nts, "neImz @n pr@""n2nsi"eIS=n'),
"Formeln und Reaktionsgleichungen lesen": ("Reading formulae and equations", '"ri:dIN "fO:mjuli: @n I"kweIZ=nz'),
"Verbindungen aus zwei Elementen benennen": ("Naming binary compounds", '"neImIN "baIn@ri "k6mpaUndz'),
"Säuren, Basen und ihre Salze benennen": ("Naming acids, bases and their salts", '"neImIN "\\ae sIdz, "beIsIz @n De@ "sO:lts'),
"Der pH-Wert und Indikatoren": ("pH and indicators", '""pi: "eItS @n "IndIkeIt@z'),
"Organische Verbindungen benennen": ("Naming organic compounds", '"neImIN O:"g\\ae nIk "k6mpaUndz'),
"Rechnen mit Stoffmengen": ("Calculating with moles", '"k\\ae lkjuleItIN wID "m@Ulz'),
"Experimente beschreiben und sicher arbeiten": ("Describing experiments and working safely", 'dI"skraIbIN Ik"sperIm@nts @n "w3:kIN "seIfli'),
"Zahlwörter bei Verbindungen aus Nichtmetallen": ("Number prefixes for non-metal compounds", '"n2mb@ "pri:fIksIz f@ ""n6n"met=l "k6mpaUndz'),
"Gefahren und Sicherheit": ("Hazards and safety", '"h\\ae z@dz @n "seIfti'),
"Beobachtungen und Nachweise": ("Observations and tests", '""6bz@"veIS=nz @n "tests'),
"Basen und bekannte Salze": ("Bases and common salts", '"beIsIz @n "k6m@n "sO:lts'),
}
# schon zweisprachig, bleiben unverändert
UNVERAENDERT = {"Register Deutsch -- Englisch", "Index English -- German"}

MAKROS = r"""
% Zweisprachige Überschriften: \teil, \kapitel, \zwischen{Deutsch}{English}{Lautschrift}
% Wie \eintrag wird " ausgeschaltet, BEVOR die Argumente gelesen werden (Betonungszeichen der Lautschrift).
% Ins Inhaltsverzeichnis und in die PDF-Lesezeichen kommt nur „Deutsch -- English“ ohne Lautschrift.
\makeatletter
\newcommand\teil{\begingroup\shorthandoff{"}\teil@aux}
\newcommand\teil@aux[3]{\endgroup\part[#1 -- #2]{\raggedright #1\\[5pt]{\normalfont\Large\color{black!55}#2\hspace{0.35em}\penalty0 \ipa{#3}}}}
\newcommand\kapitel{\begingroup\shorthandoff{"}\kapitel@aux}
\newcommand\kapitel@aux[3]{\endgroup\section[#1 -- #2]{\raggedright #1\\[0pt]{\normalfont\small\color{black!55}#2\hspace{0.35em}\penalty0 \ipa{#3}}}}
\newcommand\zwischen{\begingroup\shorthandoff{"}\zwischen@aux}
\newcommand\zwischen@aux[3]{\endgroup\subsection*{\raggedright #1 {\normalfont\small\color{black!55}\,--\, #2\hspace{0.35em}\penalty0 \ipa{#3}}}}
% Die zweite Überschriftenzeile kostet Platz: Zeilen in den Listen und Tabellen etwas enger setzen
\renewcommand\lies@aux[3]{\endgroup #1 & #2\newline{\color{black!60}#3} \\[1.5pt]}
\makeatother
\setlength{\aboverulesep}{0.15ex}\setlength{\belowrulesep}{0.3ex}\renewcommand{\arraystretch}{0.93}
"""


def zweisprachig(tex):
    """Ersetzt im fertigen Dokument alle Überschriften durch die zweisprachige Fassung."""
    def neu(m):
        befehl, titel = m.group(1), m.group(2)
        if titel in UNVERAENDERT:
            return m.group(0)
        en, laut = UEB[titel]          # KeyError = Überschrift fehlt in UEB
        laut = laut.replace("=l", r"\textsyllabic{l}").replace("=n", r"\textsyllabic{n}")
        makro = {"part": "teil", "section": "kapitel", "subsection*": "zwischen"}[befehl]
        return f"\\{makro}{{{titel}}}{{{en}}}{{{laut}}}"
    tex = re.sub(r"\\(part|section|subsection\*)\{([^{}]*)\}", neu, tex)
    return tex.replace("\\begin{document}", MAKROS + "\n\\begin{document}", 1)
