# SPDX-License-Identifier: MIT
"""Erzeugt Chemisches-Woerterbuch-Deutsch-Englisch.tex aus den Dateien in diesem Ordner.

  python3 quelle/bauen.py Chemisches-Woerterbuch-Deutsch-Englisch.tex ../../../skills/grundlagen/latex-grundstil/assets

daten.py        Begriffe für Teil I (Artikel, Begriff, englisch, Lautschrift, Formel/Skizze)
praeambel.tex   dokumentspezifische Befehle und Skizzen
teil2.tex       Teil II (Lesen und Sprechen) mit Beispielen
ueberschriften.py  englische Übersetzung und Lautschrift aller Überschriften
beispiele.tex   Beispiele am Ende der Kapitel von Teil I (Block je Kapitel, Titel hinter %%%)
"""
import re, sys, unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from daten import KAPITEL

ZIEL = Path(sys.argv[1])
# optional: Pfad zu den universalen Stildateien (Standard: liegen neben dem Dokument)
STIL = sys.argv[2].rstrip("/") + "/" if len(sys.argv) > 2 else ""
HIER = Path(__file__).parent
praeambel = (HIER / "praeambel.tex").read_text(encoding="utf-8")
teil2 = (HIER / "teil2.tex").read_text(encoding="utf-8")
bloecke = [b.split("\n", 1) for b in (HIER / "beispiele.tex").read_text(encoding="utf-8").split("%%% ")[1:]]
BSP = {k.strip(): v.strip() for k, v in bloecke}

# Teil II: jeder Abschnitt auf neuer Seite
stuecke = re.split(r"(?=\\section\{)", teil2)
teil2 = stuecke[0] + "\\newpage\n".join(stuecke[1:])


def ipa(s):
    return s.replace("=l", r"\textsyllabic{l}").replace("=n", r"\textsyllabic{n}")


def sortkey(s):
    s = s.replace("ß", "ss")
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


zeilen, register_de, register_en, n = [], [], [], 0
for titel, eintraege in KAPITEL:
    zeilen.append(f"%%%%  {titel.upper()}  %%%%")
    if n > 0:
        zeilen.append("\\newpage")
    zeilen.append(f"\\section{{{titel}}}\n")
    zeilen.append("\\begin{woerter}")
    for art, de, en, lautschrift, sym in eintraege:
        n += 1
        zeilen.append(f"\\eintrag{{{n}}}{{{art}}}{{{de}}}{{{en}}}{{{ipa(lautschrift)}}}{{{sym}}}")
        register_de.append((sortkey(de), de, art, en, n))
        register_en.append((sortkey(en), en, de, art, n))
    zeilen.append("\\end{woerter}\n")
    zeilen.append("\\subsection*{Beispiele}\n\n" + BSP.pop(titel) + "\n\n")
assert not BSP, BSP.keys()


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


reg_de = register(register_de, True)
reg_en = register([(k, en, de, art, nr) for k, en, de, art, nr in register_en], False)

tex = "\\input{" + STIL + "header.tex}\n\\input{" + STIL + "newcommands.tex}\n" + r"""
% Chemisches Wörterbuch Deutsch – Englisch mit Lautschrift
% Skills: latex-grundstil, latex-lautschrift (tipa, \ipa), latex-chemie (mhchem \ce, chemfig),
%         latex-funktionsgraphen, latex-tikz-grundlagen
% Kompilieren mit pdflatex (dreimal, wegen Inhaltsverzeichnis und Seitenzahlen im Register).

""" + praeambel + r"""

\title{Chemisches Wörterbuch\\[0.3em] \large Deutsch -- Englisch mit englischer Lautschrift, Formeln und Skizzen}
\author{Martin Quandt}
\date{\today}
\pagestyle{plain}
\setlength{\tabcolsep}{4pt}

\begin{document}

\maketitle

Dieses Wörterbuch enthält """ + str(n) + r""" chemische Fachbegriffe aus der Sekundarstufe I und II,
geordnet nach Sachgebieten. Zu jedem Begriff stehen der englische Fachausdruck mit seiner Aussprache und
-- wo es hilft -- eine Formel, eine Reaktionsgleichung oder eine kleine Skizze. Teil~II zeigt, wie man
Elementnamen, Formeln und Reaktionsgleichungen auf Englisch liest, wie Verbindungen benannt werden und
wie man Experimente beschreibt. Am Ende finden Sie je ein alphabetisches Register Deutsch -- Englisch
und Englisch -- Deutsch.

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
	\textipa{@} & wat\textbf{er} \ipa{"wO:t@} & \textipa{T} & me\textbf{th}ane \ipa{"mi:TeIn} \\
	\textipa{\ae} & \textbf{a}cid \ipa{"\ae sId} & \textipa{S} & solu\textbf{t}ion \ipa{s@"lu:S\textsyllabic{n}} \\
	\textipa{2} & s\textbf{u}lfur \ipa{"s2lf@} & \textipa{dZ} & hydro\textbf{g}en \ipa{"haIdr@dZ@n} \\
	\textipa{6} & s\textbf{o}lid \ipa{"s6lId} & \textipa{aI} & ox\textbf{i}de \ipa{"6ksaId} \\
	\textipa{3:} & b\textbf{ur}ner \ipa{"b3:n@} & \textipa{eI} & sulf\textbf{a}te \ipa{"s2lfeIt} \\
	\textipa{@U} & s\textbf{o}dium \ipa{"s@Udi@m} & \textipa{\textsyllabic{l}} & meta\textbf{l} \ipa{"met\textsyllabic{l}} \\
	\bottomrule
\end{tabular}}

\medskip
\textbf{Schreibweisen:} Die englischen Namen folgen den IUPAC-Empfehlungen (\textit{sulfur},
\textit{ethanoic acid}); verbreitete ältere Namen stehen in Klammern. \textbf{Farben in den Skizzen:}
Geräte sind blau, hervorgehobene Teile (der Begriff selbst) rot, Hilfslinien gestrichelt.

\newpage
{\footnotesize\setlength{\parskip}{0pt}\tableofcontents}
\newpage

\part{Wörterbuch}

""" + "\n".join(zeilen) + "\n\n" + teil2 + r"""

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
