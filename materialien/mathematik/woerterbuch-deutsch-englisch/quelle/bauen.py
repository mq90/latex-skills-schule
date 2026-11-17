# SPDX-License-Identifier: MIT
"""Erzeugt Mathematisches-Woerterbuch-Deutsch-Englisch.tex aus den Dateien in diesem Ordner.

  python3 quelle/bauen.py Mathematisches-Woerterbuch-Deutsch-Englisch.tex ../../../skills/grundlagen/latex-grundstil/assets

daten.py, daten_zusatz.py, daten_zusatz2.py  Begriffe für Teil I (Artikel, Begriff, englisch, Lautschrift, Zeichen/Skizze)
skizzen.tex, teil_b_praeambel.tex            dokumentspezifische Befehle und Skizzen
teil_b.tex, teil_c.tex                       Teil II (Lesen und Sprechen)
ueberschriften.py  englische Übersetzung und Lautschrift aller Überschriften
beispiele.tex                                Beispiele am Ende der Kapitel (Block je Kapitel, Titel hinter %%%)
"""
import re, sys, unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from daten import KAPITEL
from daten_zusatz import ZUSATZ
from daten_zusatz2 import ZUSATZ2
ZUSATZ = ZUSATZ + ZUSATZ2

# Ergänzungen hinter den jeweiligen Ankerbegriff einsortieren
for anker, neu in ZUSATZ:
    treffer = [(k, i) for k, (_, e) in enumerate(KAPITEL) for i, x in enumerate(e) if x[1] == anker]
    assert len(treffer) == 1, (anker, treffer)
    k, i = treffer[0]
    KAPITEL[k][1][i + 1:i + 1] = neu

ZIEL = Path(sys.argv[1])
# optional: Pfad zu den universalen Stildateien (Standard: liegen neben dem Dokument)
STIL = sys.argv[2].rstrip("/") + "/" if len(sys.argv) > 2 else ""
HIER = Path(__file__).parent
skizzen = (HIER / "skizzen.tex").read_text(encoding="utf-8") + "\n" + (HIER / "teil_b_praeambel.tex").read_text(encoding="utf-8")
teil_b = (HIER / "teil_b.tex").read_text(encoding="utf-8") + "\n" + (HIER / "teil_c.tex").read_text(encoding="utf-8")

# Beispiele für das Ende jedes Kapitels: die ersten 10 Blöcke gehören zu Teil I, die übrigen zu Teil II
bloecke = [b.split("\n", 1) for b in (HIER / "beispiele.tex").read_text(encoding="utf-8").split("%%% ")[1:]]
BSP_I = {k.strip(): v.strip() for k, v in bloecke[:10]}
BSP_II = {k.strip(): v.strip() for k, v in bloecke[10:]}
assert len(BSP_I) == 10

# Teil II: jeder Abschnitt auf neuer Seite, fehlende Beispiele am Abschnittsende ergänzen
stuecke = re.split(r"(?=\\section\{)", teil_b)
neu = [stuecke[0]]
for i, s in enumerate(stuecke[1:]):
    titel = re.match(r"\\section\{([^}]*)\}", s).group(1)
    if titel in BSP_II:
        s = s.rstrip() + "\n\n\\subsection*{Beispiele}\n\n" + BSP_II.pop(titel) + "\n\n"
    neu.append(("\\newpage\n" if i > 0 else "") + s)
assert not BSP_II, BSP_II.keys()
teil_b = "".join(neu)


def sortkey(s):
    s = re.sub(r"\$[^$]*\$", lambda m: re.sub(r"[^a-z]", "", m.group(0)), s)
    s = s.replace("ß", "ss")
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


zeilen = []
register_de, register_en = [], []
n = 0
for titel, eintraege in KAPITEL:
    zeilen.append(f"%%%%  {titel.upper()}  %%%%")
    if n > 0:
        zeilen.append("\\newpage")
    zeilen.append(f"\\section{{{titel}}}\n")
    zeilen.append("\\begin{woerter}")
    for art, de, deipa, en, enipa, sym in eintraege:
        n += 1
        zeilen.append(f"\\eintrag{{{n}}}{{{art}}}{{{de}}}{{{en}}}{{{enipa}}}{{{sym}}}")
        register_de.append((sortkey(de), de, art, en, n))
        register_en.append((sortkey(en), en, de, art, n))
    zeilen.append("\\end{woerter}\n")
    zeilen.append("\\subsection*{Beispiele}\n\n" + BSP_I[titel] + "\n\n")


def register(liste, deutsch_zuerst):
    out = ["\\begin{multicols}{2}\\small\\raggedright"]
    buchstabe = None
    for key, a, b, c, nr in sorted(liste):
        if key[0] != buchstabe:
            buchstabe = key[0]
            out.append(f"\n\\medskip{{\\large\\textbf{{\\color{{cornflower}}{buchstabe.upper()}}}}}\\par\\nopagebreak")
        if deutsch_zuerst:   # a = Begriff, b = Artikel, c = englisch
            art = f" ({b})" if b else ""
            out.append(f"\\textbf{{{a}}}{art} -- {c}\\dotfill\\hyperref[e:{nr}]{{\\pageref*{{e:{nr}}}}}\\par")
        else:                # a = englisch, b = deutsch, c = Artikel
            art = f"{c} " if c else ""
            out.append(f"\\textbf{{{a}}} -- {art}{b}\\dotfill\\hyperref[e:{nr}]{{\\pageref*{{e:{nr}}}}}\\par")
    out.append("\\end{multicols}")
    return "\n".join(out)


reg_de = register([(k, de, art, en, nr) for k, de, art, en, nr in register_de], True)
reg_en = register([(k, en, de, art, nr) for k, en, de, art, nr in register_en], False)

tex = "\\input{" + STIL + "header.tex}\n\\input{" + STIL + "newcommands.tex}\n" + r"""
% Mathematisches Wörterbuch Deutsch – Englisch mit Lautschrift
% Skills: latex-grundstil, latex-lautschrift (tipa, \ipa), latex-grundlagen (Formelsatz), latex-geometrie,
%         latex-funktionsgraphen, latex-venn-diagramme
% Kompilieren mit pdflatex (zweimal, wegen Inhaltsverzeichnis und Seitenzahlen im Register).

""" + skizzen + r"""

\title{Mathematisches Wörterbuch\\[0.3em] \large Deutsch -- Englisch mit englischer Lautschrift, Zeichen und Skizzen}
\author{Martin Quandt}
\date{\today}
\pagestyle{plain}
\setlength{\tabcolsep}{4pt}

\begin{document}

\maketitle

Dieses Wörterbuch enthält """ + str(n) + r""" mathematische Fachbegriffe aus der Sekundarstufe I und II,
geordnet nach Sachgebieten. Zu jedem Begriff stehen der englische Fachausdruck mit seiner Aussprache und
-- wo es hilft -- das Zeichen, eine Formel oder eine kleine Skizze. Teil~II zeigt, wie man Zeichen,
Formeln und Rechenwege auf Englisch vorliest, mit vielen Beispielen. Am Ende finden Sie je ein
alphabetisches Register Deutsch -- Englisch und Englisch -- Deutsch.

\subsection*{Hinweise zur Lautschrift}

Die Lautschrift folgt dem Internationalen Phonetischen Alphabet (IPA) und gibt die britische
Aussprache wieder, wie sie in Schulwörterbüchern steht (dort wird \textipa{r} statt
\textipa{\textturnr} geschrieben). Der Strich \textipa{\textprimstress} steht \textit{vor} der
betonten Silbe, \textipa{\textsecstress} vor einer Silbe mit Nebenbetonung, \textipa{:} bedeutet lang.

\medskip
{\small
\begin{tabular}{>{\centering\arraybackslash}p{0.9cm} l @{\hspace{1.2cm}} >{\centering\arraybackslash}p{0.9cm} l}
	\toprule
	\textbf{Laut} & \textbf{Beispiel} & \textbf{Laut} & \textbf{Beispiel} \\ \midrule
	\textipa{@} & \textbf{a}rea \ipa{"e@ri@} & \textipa{T} & \textbf{th}eorem \ipa{"TI@r@m} \\
	\textipa{\ae} & \textbf{a}ngle \ipa{"\ae Ng\textsyllabic{l}} & \textipa{D} & less \textbf{th}an \ipa{"les D@n} \\
	\textipa{2} & n\textbf{u}mber \ipa{"n2mb@} & \textipa{S} & frac\textbf{t}ion \ipa{"fr\ae kS\textsyllabic{n}} \\
	\textipa{6} & pr\textbf{o}duct \ipa{"pr6d2kt} & \textipa{dZ} & e\textbf{dge} \ipa{edZ} \\
	\textipa{3:} & v\textbf{er}tex \ipa{"v3:teks} & \textipa{N} & a\textbf{n}gle \ipa{"\ae Ng\textsyllabic{l}} \\
	\textipa{@U} & c\textbf{o}ne \ipa{k@Un} & \textipa{\textsyllabic{l}} & circ\textbf{le} \ipa{"s3:k\textsyllabic{l}} \\
	\bottomrule
\end{tabular}}

\medskip
\textbf{Farben in den Skizzen:} Figuren sind blau, hervorgehobene Teile (der Begriff selbst, Winkel,
Maße) rot, verdeckte Kanten und Hilfslinien gestrichelt.

\newpage
{\small\setlength{\parskip}{0pt}\tableofcontents}
\newpage

\part{Wörterbuch}

""" + "\n".join(zeilen) + "\n\n" + teil_b + r"""

\newpage
%%%%  REGISTER  %%%%
\part{Register}
\section{Register Deutsch -- Englisch}
""" + reg_de + r"""

\newpage
\section{Index English -- German}
""" + reg_en + r"""

\end{document}
"""

kopf, rumpf = tex.split("\\begin{document}", 1)
tex = kopf + "\\begin{document}" + rumpf.replace("\\subsection*{", "\\platz\\subsection*{").replace("\\platz\\subsection*{Hinweise zur Lautschrift}", "\\subsection*{Hinweise zur Lautschrift}")
from ueberschriften import zweisprachig
tex = zweisprachig(tex)
ZIEL.write_text(tex, encoding="utf-8")
print(f"{n} Einträge -> {ZIEL}")
