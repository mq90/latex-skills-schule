#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""
Erzeugt references/makros.md des Skills latex-grundstil aus den universalen
Stildateien header.tex und newcommands.tex. Nach jeder Änderung an den
Stildateien ausführen:

  python3 werkzeuge/makros_auflisten.py
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "grundlagen" / "latex-grundstil"
NC = (SKILL / "assets" / "newcommands.tex").read_text(encoding="utf-8")
HD = (SKILL / "assets" / "header.tex").read_text(encoding="utf-8")

DEF = re.compile(r"\s*\\(?:re)?(newcommand|newtcolorbox|newenvironment|lstdefinestyle|definecolor|tikzstyle)"
                 r"\{?\\?([A-Za-z]+)\}?\s*(?:\[(\d)\])?(?:\[[^\]]*\])?[^%]*(?:%(.*))?$")


def zelle(t):
    t = (t or "").strip().strip("%").strip()
    return t.replace("|", "\\|")


out = ["# Befehle und Pakete der universalen Stildateien", "",
       "Automatisch erzeugt mit `werkzeuge/makros_auflisten.py` aus `assets/newcommands.tex` und",
       "`assets/header.tex`. Vor dem Anlegen eines neuen Befehls hier nachsehen, ob es schon",
       "etwas Gleichwertiges gibt."]
letzter_kommentar = ""
for line in NC.splitlines():
    m = re.match(r"%%%+\s+(.*?)\s+%%%+", line)
    if m:
        if "NEWCOMMANDS" not in m.group(1):
            out += ["", f"## {m.group(1).strip()}", "", "| Befehl | Zweck |", "|---|---|"]
        letzter_kommentar = ""
        continue
    if re.match(r"\s*%[^-]", line):
        letzter_kommentar = line.strip().lstrip("%").strip()
        continue
    m = DEF.match(line)
    if m:
        art, name, n, kom = m.groups()
        if art == "newcommand":
            befehl = "\\" + name + ("{…}" * int(n) if n else "")
        elif art in ("newtcolorbox", "newenvironment"):
            befehl = f"\\begin{{{name}}}"
        elif art == "lstdefinestyle":
            befehl = f"style={name}"
        elif art == "definecolor":
            befehl = f"Farbe {name}"
        else:
            befehl = f"TikZ-Stil {name}"
        out.append(f"| `{befehl}` | {zelle(kom) or zelle(letzter_kommentar)} |")
        if not kom:
            letzter_kommentar = letzter_kommentar  # gilt ggf. für mehrere Zeilen (z. B. Zahlenbereiche)
    elif line.strip() == "":
        letzter_kommentar = ""

out += ["", "## Pakete in header.tex", "", "| Paket | Zweck |", "|---|---|"]
for line in HD.splitlines():
    m = re.match(r"\s*\\usepackage(\[[^\]]*\])?\{([^}]+)\}\s*(%(.*))?", line)
    if m:
        out.append(f"| `{m.group(2)}` | {zelle(m.group(4))[:120]} |")
m = re.search(r"\\usetikzlibrary\{(.*?)\}\s*%nützliche", HD, re.S)
libs = [l.strip() for l in re.sub(r"%[^\n]*", "", m.group(1)).replace("\n", ",").split(",") if l.strip()]
out += ["", "**TikZ-Bibliotheken:** " + ", ".join(f"`{l}`" for l in libs), "",
        "**Bewusst nicht geladen:** `musixtex` – nur für Musik-Dokumente in der header.tex "
        "einkommentieren, weil es `\\cup` als Achtelnote umdefiniert (bricht `$A \\cup B$`)."]
ziel = SKILL / "references" / "makros.md"
ziel.write_text("\n".join(out) + "\n", encoding="utf-8")
print(f"{ziel.relative_to(ROOT)}: {sum(1 for z in out if z.startswith('| `'))} Einträge")
