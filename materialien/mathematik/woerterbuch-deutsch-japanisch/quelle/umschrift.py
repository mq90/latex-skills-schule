# SPDX-License-Identifier: MIT
r"""Kurzschreibweise für japanischen Text -> Anzeige, Lesung (Kana) und Hepburn-Umschrift.

Japanischer Text wird in den Quelldateien mit Lesung notiert, Wörter durch Leerzeichen getrennt:

    二次|にじ 方程式|ほうていしき を 解きなさい|ときなさい 。

  Wort|Lesung   Wort mit Kanji (oder Ziffern) und seine Lesung in Hiragana/Katakana
  かな          reine Kana-Wörter brauchen keine Lesung
  は へ を      als eigenes Wort = Partikel, Umschrift wa, e, o
  $x$ \\ldots    Mathematik und LaTeX-Befehle bleiben unverändert stehen
  /             trennt gleichwertige Lesarten (wird zu \;/\;)
  In der Lesung:  _  Wortgrenze nur in der Umschrift (さん_てん_いち -> san ten ichi)
                  .  verhindert einen Langvokal über eine Morphemgrenze (ば.あい -> baai)

Daraus entstehen drei Fassungen:
  anzeige()   二次方程式を解きなさい。          (ohne Leerzeichen, wie im Japanischen üblich)
  kana()      にじほうていしきをときなさい。
  romaji()    niji hōteishiki o tokinasai.     (Hepburn mit Längenstrich)
"""
import re

_GRUND = {
    "あ": "a", "い": "i", "う": "u", "え": "e", "お": "o",
    "か": "ka", "き": "ki", "く": "ku", "け": "ke", "こ": "ko",
    "さ": "sa", "し": "shi", "す": "su", "せ": "se", "そ": "so",
    "た": "ta", "ち": "chi", "つ": "tsu", "て": "te", "と": "to",
    "な": "na", "に": "ni", "ぬ": "nu", "ね": "ne", "の": "no",
    "は": "ha", "ひ": "hi", "ふ": "fu", "へ": "he", "ほ": "ho",
    "ま": "ma", "み": "mi", "む": "mu", "め": "me", "も": "mo",
    "や": "ya", "ゆ": "yu", "よ": "yo",
    "ら": "ra", "り": "ri", "る": "ru", "れ": "re", "ろ": "ro",
    "わ": "wa", "を": "o",
    "が": "ga", "ぎ": "gi", "ぐ": "gu", "げ": "ge", "ご": "go",
    "ざ": "za", "じ": "ji", "ず": "zu", "ぜ": "ze", "ぞ": "zo",
    "だ": "da", "ぢ": "ji", "づ": "zu", "で": "de", "ど": "do",
    "ば": "ba", "び": "bi", "ぶ": "bu", "べ": "be", "ぼ": "bo",
    "ぱ": "pa", "ぴ": "pi", "ぷ": "pu", "ぺ": "pe", "ぽ": "po",
    "ゔ": "vu",
}
_KOMBI = {
    "きゃ": "kya", "きゅ": "kyu", "きょ": "kyo", "しゃ": "sha", "しゅ": "shu", "しょ": "sho",
    "ちゃ": "cha", "ちゅ": "chu", "ちょ": "cho", "にゃ": "nya", "にゅ": "nyu", "にょ": "nyo",
    "ひゃ": "hya", "ひゅ": "hyu", "ひょ": "hyo", "みゃ": "mya", "みゅ": "myu", "みょ": "myo",
    "りゃ": "rya", "りゅ": "ryu", "りょ": "ryo", "ぎゃ": "gya", "ぎゅ": "gyu", "ぎょ": "gyo",
    "じゃ": "ja", "じゅ": "ju", "じょ": "jo", "びゃ": "bya", "びゅ": "byu", "びょ": "byo",
    "ぴゃ": "pya", "ぴゅ": "pyu", "ぴょ": "pyo",
    # Lehnwort-Silben (Katakana)
    "ふぁ": "fa", "ふぃ": "fi", "ふぇ": "fe", "ふぉ": "fo", "てぃ": "ti", "でぃ": "di", "でゅ": "dyu",
    "ちぇ": "che", "しぇ": "she", "じぇ": "je", "うぃ": "wi", "うぇ": "we", "うぉ": "wo",
    "とぅ": "tu", "どぅ": "du", "つぁ": "tsa", "ゔぁ": "va", "ゔぃ": "vi", "ゔぇ": "ve", "ゔぉ": "vo",
}
_LANG = {"a": "ā", "i": "ī", "u": "ū", "e": "ē", "o": "ō"}
_SATZZEICHEN = {"、": ",", "。": ".", "：": ":", "（": "(", "）": ")", "・": "·", "「": "„", "」": "“"}
_KANA = re.compile(r"^[぀-ゟ゠-ヿー]+$")
_TOKEN = re.compile(r"\$[^$]*\$|\S+")


def hira(s):
    """Katakana -> Hiragana (der Längenstrich ー bleibt)."""
    return "".join(chr(ord(c) - 0x60) if "ァ" <= c <= "ヶ" else c for c in s)


def _wort(lesung):
    """Ein Wort in Kana -> Hepburn."""
    s = hira(lesung)
    silben, i = [], 0          # Liste aus Silben; "." als Sperre, "っ" und "ん" bleiben zunächst stehen
    while i < len(s):
        if s[i:i + 2] in _KOMBI:
            silben.append(_KOMBI[s[i:i + 2]]); i += 2
        elif s[i] in _GRUND:
            silben.append(_GRUND[s[i]]); i += 1
        elif s[i] in "っんー.":
            silben.append(s[i]); i += 1
        else:
            raise ValueError(f"Lesung enthält ein unbekanntes Zeichen: {lesung!r} ({s[i]!r})")
    aus = ""
    for k, si in enumerate(silben):
        nach = silben[k + 1] if k + 1 < len(silben) else ""
        if si == ".":
            aus += "\x00"                                   # Sperre: kein Langvokal über diese Stelle
        elif si == "っ":
            aus += "t" if nach.startswith("ch") else nach[:1]
        elif si == "ん":
            aus += "n'" if nach[:1] in ("a", "i", "u", "e", "o", "y") else "n"
        elif si == "ー":
            if aus and aus[-1] in _LANG:
                aus = aus[:-1] + _LANG[aus[-1]]
        elif si in ("a", "u", "o", "e") and aus and (
                (aus[-1] == "o" and si in ("u", "o")) or (aus[-1] == "u" and si == "u")
                or (aus[-1] == "a" and si == "a") or (aus[-1] == "e" and si == "e")):
            aus = aus[:-1] + _LANG[aus[-1]]                 # ou, oo -> ō;  uu -> ū;  aa -> ā;  ee -> ē
        else:
            aus += si
    return aus.replace("\x00", "")


def _zerlege(text):
    """-> Liste (Art, Anzeige, Lesung); Art: J = japanisch, P = Satzzeichen, L = LaTeX/Mathematik."""
    teile = []
    for t in _TOKEN.findall(text):
        if t == "/":
            teile.append(("L", r"\;/\;", None))
        elif t in _SATZZEICHEN:
            teile.append(("P", t, None))
        elif "|" in t and not t.startswith("$"):
            wort, lesung = t.split("|", 1)
            if not _KANA.match(lesung.replace("_", "").replace(".", "")):
                raise ValueError(f"Lesung ist kein Kana: {t!r}")
            teile.append(("J", wort, lesung))
        elif _KANA.match(t):
            teile.append(("J", t, t))
        elif re.search(r"[一-鿿々]", t):
            raise ValueError(f"Kanji ohne Lesung: {t!r} in {text!r}")
        else:
            teile.append(("L", t, None))
    return teile


def _fuege(teile, wert):
    """Fügt zusammen: Japanisches ohne Leerzeichen, LaTeX/Mathematik mit Leerzeichen abgesetzt."""
    aus, vor = "", None
    for art, wort, lesung in teile:
        stueck = wert(art, wort, lesung)
        if vor is not None and "L" in (art, vor[0]) and "P" not in (art, vor[0]):
            # Koeffizient direkt vor der Variablen: 3$x$ statt 3 $x$
            if not (vor[0] == "J" and re.fullmatch(r"[0-9.]+", vor[1]) and wort.startswith("$")):
                aus += " "
        aus += stueck
        vor = (art, wort)
    return aus


def anzeige(text):
    return _fuege(_zerlege(text), lambda art, wort, lesung: wort)


def kana(text):
    return _fuege(_zerlege(text), lambda art, wort, lesung: lesung.replace("_", "").replace(".", "") if art == "J" else wort)


def romaji(text):
    aus = []
    for art, wort, lesung in _zerlege(text):
        if art == "L":
            aus.append(wort)
        elif art == "P":
            z = _SATZZEICHEN[wort]
            if z in "(„":
                aus.append(z + "\x01")                      # klebt am folgenden Wort
            elif aus:
                aus[-1] += z
        elif wort in ("は", "へ", "を") and lesung == wort:
            aus.append({"は": "wa", "へ": "e", "を": "o"}[wort])
        else:
            aus.append(" ".join(_wort(w) for w in lesung.split("_")))
    return " ".join(aus).replace("\x01 ", "")


def nur_kana(text):
    """True, wenn der Text ohne Kanji auskommt (dann ist die Kana-Zeile überflüssig)."""
    return anzeige(text) == kana(text)


if __name__ == "__main__":
    import sys
    for zeile in sys.argv[1:] or ["二次|にじ 方程式|ほうていしき を 解きなさい|ときなさい 。"]:
        print(anzeige(zeile), "|", kana(zeile), "|", romaji(zeile))
