# SPDX-License-Identifier: MIT
"""Erzeugt Mathematisches-Woerterbuch-Deutsch-Japanisch.tex aus den Dateien in diesem Ordner.

  python3 quelle/bauen.py Mathematisches-Woerterbuch-Deutsch-Japanisch.tex ../../../skills/grundlagen/latex-grundstil/assets

daten.py           Begriffe für Teil I (Artikel, Begriff, Japanisch, Zeichen/Skizze)
praeambel.tex      dokumentspezifische Befehle und Skizzen, Japanisch-Satz mit CJKutf8
teil2.tex          Teil II (Lesen und Sprechen)
beispiele.tex      Beispiele am Ende der Kapitel (Block je Kapitel, Titel hinter %%%)
ueberschriften.py  japanische Übersetzung aller Überschriften
umschrift.py       Kurzschreibweise Wort|Lesung -> Japanisch, Lesung in Kana, Hepburn-Umschrift

Japanischer Text steht überall in der Kurzschreibweise aus umschrift.py; erst dieses Skript macht
daraus die Schriftzeichen und die Umschrift. Wer etwas ergänzt, schreibt also nur Wort|Lesung.
"""
import re, sys, unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from daten import KAPITEL
from umschrift import anzeige, kana, romaji, nur_kana, hira

ZIEL = Path(sys.argv[1])
# optional: Pfad zu den universalen Stildateien (Standard: liegen neben dem Dokument)
STIL = sys.argv[2].rstrip("/") + "/" if len(sys.argv) > 2 else ""
HIER = Path(__file__).parent
praeambel = (HIER / "praeambel.tex").read_text(encoding="utf-8")
teil2 = (HIER / "teil2.tex").read_text(encoding="utf-8")

# Beispiele für das Ende jedes Kapitels: die ersten 10 Blöcke gehören zu Teil I, die übrigen zu Teil II
bloecke = [b.split("\n", 1) for b in (HIER / "beispiele.tex").read_text(encoding="utf-8").split("%%% ")[1:]]
BSP_I = {k.strip(): v.strip() for k, v in bloecke[:10]}
BSP_II = {k.strip(): v.strip() for k, v in bloecke[10:]}
assert len(BSP_I) == 10

# Teil II: jeder Abschnitt auf neuer Seite, fehlende Beispiele am Abschnittsende ergänzen
stuecke = re.split(r"(?=\\section\{)", teil2)
neu = [stuecke[0]]
for i, s in enumerate(stuecke[1:]):
    titel = re.match(r"\\section\{([^}]*)\}", s).group(1)
    if titel in BSP_II:
        s = s.rstrip() + "\n\n\\subsection*{Beispiele}\n\n" + BSP_II.pop(titel) + "\n\n"
    neu.append(("\\newpage\n" if i > 0 else "") + s)
assert not BSP_II, BSP_II.keys()
teil2 = "".join(neu)


def sortkey(s):
    s = re.sub(r"\$[^$]*\$", lambda m: re.sub(r"[^a-z]", "", m.group(0)), s)
    s = s.replace("ß", "ss")
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


# Fünfzig-Laute-Tafel: getrübte und kleine Kana werden für die Reihenfolge wie die Grundzeichen behandelt
_TRUEB = str.maketrans("がぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽぁぃぅぇぉっゃゅょゎゔ",
                       "かきくけこさしすせそたちつてとはひふへほはひふへほあいうえおつやゆよわう")
_ZEILEN = ["あいうえお", "かきくけこ", "さしすせそ", "たちつてと", "なにぬねの", "はひふへほ", "まみむめも", "やゆよ", "らりるれろ", "わをん"]
_KOPF = ["あ \\,·\\, a", "か \\,·\\, ka", "さ \\,·\\, sa", "た \\,·\\, ta", "な \\,·\\, na", "は \\,·\\, ha", "ま \\,·\\, ma",
         "や \\,·\\, ya", "ら \\,·\\, ra", "わ \\,·\\, wa"]


def kanakey(ja):
    """Sortierschlüssel nach der Lesung: (Zeile der Tafel, Position in der Tafel ..., Lesung)."""
    k = hira(kana(ja))
    k = re.sub(r"\$([^$]*)\$", lambda m: re.sub(r"[^a-z]", "", m.group(1).lower()), k)
    k = re.sub(r"[ 、ー]", "", k)
    grund = k.translate(_TRUEB)
    tafel = "".join(_ZEILEN)
    return ([tafel.index(c) if c in tafel else -1 for c in grund], k)


def zeile(k):
    """Nummer der Zeile der Fünfzig-Laute-Tafel, -1 für lateinische Buchstaben."""
    erstes, anfang = k[0][0], 0
    if erstes < 0:
        return -1
    for i, z in enumerate(_ZEILEN):
        if erstes < anfang + len(z):
            return i
        anfang += len(z)


def lies_umsetzen(tex):
    r"""\lies{Ausdruck}{Kurzschreibweise}{Deutsch} -> \lies{Ausdruck}{Japanisch}{Umschrift}{Deutsch}"""
    def gruppe(i):
        tiefe = 0
        for j in range(i, len(tex)):
            if tex[j] == "{" and tex[j - 1] != "\\":
                tiefe += 1
            elif tex[j] == "}" and tex[j - 1] != "\\":
                tiefe -= 1
                if tiefe == 0:
                    return tex[i + 1:j], j + 1
        raise ValueError(tex[i:i + 60])
    aus, i = "", 0
    while True:
        j = tex.find("\\lies{", i)
        if j < 0:
            return aus + tex[i:]
        a, p = gruppe(j + 5)
        b, p = gruppe(p)
        c, p = gruppe(p)
        aus += tex[i:j] + "\\lies{" + a + "}{" + anzeige(b) + "}{" + romaji(b) + "}{" + c + "}"
        i = p


zeilen = []
register_de, register_ja = [], []
n = 0
for titel, eintraege in KAPITEL:
    zeilen.append(f"%%%%  {titel.upper()}  %%%%")
    if n > 0:
        zeilen.append("\\newpage")
    zeilen.append(f"\\section{{{titel}}}\n")
    zeilen.append("\\begin{woerter}")
    for art, de, ja, sym in eintraege:
        n += 1
        lesung = "" if nur_kana(ja) else kana(ja)
        zeilen.append(f"\\eintrag{{{n}}}{{{art}}}{{{de}}}{{{anzeige(ja)}}}{{{lesung}}}{{{romaji(ja)}}}{{{sym}}}")
        register_de.append((sortkey(de), de, art, anzeige(ja), n))
        register_ja.append((kanakey(ja), anzeige(ja), lesung, de, art, n))
    zeilen.append("\\end{woerter}\n")
    zeilen.append("\\subsection*{Beispiele}\n\n" + BSP_I[titel] + "\n\n")


def seite(nr):
    return f"\\dotfill\\hyperref[e:{nr}]{{\\pageref*{{e:{nr}}}}}\\par"


def reg_deutsch(liste):
    out = ["\\begin{multicols}{2}\\small\\raggedright"]
    buchstabe = None
    for key, de, art, ja, nr in sorted(liste):
        if key[0] != buchstabe:
            buchstabe = key[0]
            out.append(f"\n\\medskip{{\\large\\textbf{{\\color{{cornflower}}{buchstabe.upper()}}}}}\\par\\nopagebreak")
        artikel = f" ({art})" if art else ""
        out.append(f"\\textbf{{{de}}}{artikel} -- {ja}" + seite(nr))
    out.append("\\end{multicols}")
    return "\n".join(out)


def reg_japanisch(liste):
    out = ["\\begin{multicols}{2}\\small\\raggedright\\raggedcolumns"]
    kopf = None
    for key, ja, lesung, de, art, nr in sorted(liste, key=lambda x: (x[0], x[3])):
        z = zeile(key)
        if z != kopf:
            kopf = z
            name = "A -- Z" if z < 0 else _KOPF[z]
            out.append(f"\n\\smallskip{{\\large\\textbf{{\\color{{cornflower}}{name}}}}}\\par\\nopagebreak")
        les = f" {{\\footnotesize\\color{{black!70}}{lesung}}}" if lesung else ""
        artikel = f"{art} " if art else ""
        out.append(f"\\jfett{{{ja}}}{les} -- {artikel}{de}" + seite(nr))
    out.append("\\end{multicols}")
    return "\n".join(out)


def bsp(*woerter):
    """Beispielwörter für die Aussprachetabelle: 数 [sū]"""
    return "\\leavevmode " + ", ".join(f"{anzeige(w)} [{romaji(w)}]" for w in woerter)


LAUTE = [
    ("ā \\,ī \\,ū \\,ē \\,ō", "langer Vokal, etwa doppelt so lang wie der kurze", bsp("数|すう", "方程式|ほうていしき")),
    ("u", "ungerundet; zwischen stimmlosen Lauten und am Wortende kaum hörbar", bsp("確率|かくりつ")),
    ("r", "kurzer Zungenschlag zwischen r, l und d", bsp("比例|ひれい")),
    ("s, z", "s stimmlos wie in „Tasse“, z stimmhaft wie das s in „Sonne“", bsp("整数|せいすう", "座標|ざひょう")),
    ("sh, ch", "wie „sch“ und „tsch“", bsp("小数|しょうすう", "頂点|ちょうてん")),
    ("j, ts", "wie „dsch“ und wie das deutsche „z“", bsp("二乗|にじょう", "通分|つうぶん")),
    ("y, w", "y wie das deutsche „j“, w wie im Englischen", bsp("要素|ようそ", "和|わ")),
    ("kk, pp, ss, tt", "kurzes Innehalten vor dem Konsonanten", bsp("括弧|かっこ", "直角|ちょっかく")),
    ("n'", "das n schließt die Silbe ab, danach setzt man neu an", bsp("単位|たんい")),
]
laute = "\n".join(f"\t{a} & {b} & {c} \\\\" for a, b, c in LAUTE)

tex = "\\input{" + STIL + "header.tex}\n\\input{" + STIL + "newcommands.tex}\n" + r"""
% Mathematisches Wörterbuch Deutsch – Japanisch mit Lesung und Umschrift
% Skills: latex-grundstil, latex-grundlagen (Formelsatz), latex-geometrie, latex-funktionsgraphen,
%         latex-venn-diagramme
% Kompilieren mit pdflatex (dreimal, wegen Inhaltsverzeichnis und Seitenzahlen im Register).
% Benötigt die Pakete CJK und ipaex-type1 (beide in TeX Live/MacTeX enthalten).

""" + praeambel + r"""

\title{Mathematisches Wörterbuch\\[0.3em] \large Deutsch -- Japanisch mit Lesung, Umschrift, Zeichen und Skizzen}
\author{Martin Quandt}
\date{\today}
\pagestyle{plain}
\setlength{\tabcolsep}{4pt}

\begin{document}
\begin{CJK}{UTF8}{ipxm}\CJKabsatzschutz

\maketitle

Dieses Wörterbuch enthält """ + str(n) + r""" mathematische Fachbegriffe aus der Sekundarstufe I und II,
geordnet nach Sachgebieten. Zu jedem Begriff stehen der japanische Fachausdruck, seine Lesung, die
Umschrift in lateinischen Buchstaben und -- wo es hilft -- das Zeichen, eine Formel oder eine kleine
Skizze. Teil~II zeigt, wie man Zeichen, Formeln und Rechenwege auf Japanisch vorliest, mit vielen
Beispielen. Am Ende finden Sie ein Register Deutsch -- Japanisch und ein Register Japanisch -- Deutsch.

\subsection*{Hinweise zu Schrift und Umschrift}

Japanische Fachbegriffe bestehen meist aus Kanji, den chinesischen Schriftzeichen. Lehnwörter wie
\jp{ベクトル}{bekutoru}, „Vektor“, stehen in der Silbenschrift Katakana. Unter jedem Begriff steht klein
seine Lesung in der Silbenschrift Hiragana und in eckigen Klammern die Umschrift nach dem
Hepburn-System. Ist der Begriff schon in Kana geschrieben, steht dort nur die Umschrift.

Die Umschrift liest man fast wie Deutsch. Das Japanische betont keine Silbe durch Lautstärke: Alle
Silben sind etwa gleich lang und gleich stark. Die Partikeln は, へ und を spricht man \textit{wa},
\textit{e} und \textit{o}; so stehen sie auch in der Umschrift.

\medskip
{\small
\begin{tabular}{@{}>{\raggedright\arraybackslash}p{2.4cm} >{\raggedright\arraybackslash}p{9.2cm} >{\raggedright\arraybackslash}p{5.0cm}@{}}
	\toprule
	\textbf{Umschrift} & \textbf{Aussprache} & \textbf{Beispiel} \\ \midrule
""" + laute + r"""
	\bottomrule
\end{tabular}}

\medskip
\textbf{Farben in den Skizzen:} Figuren sind blau, hervorgehobene Teile (der Begriff selbst, Winkel,
Maße) rot, verdeckte Kanten und Hilfslinien gestrichelt.

\newpage
{\small\setlength{\parskip}{0pt}\tableofcontents}
\newpage

\part{Wörterbuch}

""" + "\n".join(zeilen) + "\n\n" + teil2 + r"""

\newpage
%%%%  REGISTER  %%%%
\part{Register}
\section{Register Deutsch -- Japanisch}
""" + reg_deutsch(register_de) + r"""

\newpage
\section{Register Japanisch -- Deutsch}

Die Begriffe sind nach ihrer Lesung geordnet, in der Reihenfolge der japanischen Silbentafel
(a, ka, sa, ta, na, ha, ma, ya, ra, wa). Begriffe, die mit einer Variablen beginnen, stehen am Anfang.

""" + reg_japanisch(register_ja) + r"""

\clearpage
\end{CJK}
\end{document}
"""
# Kapitel, in denen sonst ein einzelner Eintrag allein auf der letzten Seite stünde: Listen enger setzen
# (Zeilenabstand der Listen, Zeilenhöhe der Tabellen); Standard ist (1.12, 0.93)
ENG = {"Vektoren und analytische Geometrie": ("1.0", "0.80"), "Grundrechenarten": ("1.0", "0.93"),
       "Körper berechnen": ("1.0", "0.93")}
tex = re.sub(r"\\section\{([^{}]*)\}",
             lambda m: m.group(0) + "\\renewcommand{\\lesenabstand}{%s}\\renewcommand{\\arraystretch}{%s}"
             % ENG.get(m.group(1), ("1.12", "0.93")), tex)

kopf, rumpf = tex.split("\\begin{document}", 1)
rumpf = lies_umsetzen(rumpf)   # Kurzschreibweise in allen \\lies-Zeilen auflösen
rumpf = rumpf.replace("\\subsection*{", "\\platz\\subsection*{").replace(
    "\\platz\\subsection*{Hinweise zu Schrift und Umschrift}", "\\subsection*{Hinweise zu Schrift und Umschrift}")
tex = kopf + "\\begin{document}" + rumpf
from ueberschriften import zweisprachig
tex = zweisprachig(tex)
ZIEL.write_text(tex, encoding="utf-8")
print(f"{n} Einträge -> {ZIEL}")
