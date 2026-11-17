# SPDX-License-Identifier: MIT
"""Japanische Übersetzung aller Überschriften (in der Kurzschreibweise aus umschrift.py).

Deutsch -> Japanisch. bauen.py ersetzt damit \\part, \\section und \\subsection* durch
\\teil, \\kapitel und \\zwischen und ergänzt die Umschrift.
"""
import re
from umschrift import anzeige, romaji

UEB = {
# Teile und wiederkehrende Zwischenüberschriften
"Wörterbuch": "辞書|じしょ",
"Register": "索引|さくいん",
"Mathematik lesen und sprechen": "数学|すうがく の 読み方|よみかた と 話し方|はなしかた",
"Beispiele": "例|れい",
"Hinweise zu Schrift und Umschrift": "表記|ひょうき と ローマ字|ローマじ",
# Teil I
"Zahlen und Rechenarten": "数|かず と 計算|けいさん",
"Algebra, Gleichungen und Mengen": "代数|だいすう 、 方程式|ほうていしき 、 集合|しゅうごう",
"Funktionen": "関数|かんすう",
"Geometrie: Grundbegriffe, Winkel, Abbildungen": "幾何|きか ： 基本|きほん 用語|ようご 、 角|かく 、 移動|いどう",
"Ebene Figuren": "平面|へいめん 図形|ずけい",
"Körper": "立体|りったい",
"Analysis": "微分|びぶん 積分|せきぶん",
"Vektoren und analytische Geometrie": "ベクトル と 解析|かいせき 幾何|きか",
"Stochastik": "確率|かくりつ と 統計|とうけい",
"Logik und Beweis": "論理|ろんり と 証明|しょうめい",
# Teil II
"Zahlen, Zeichen und Schreibweisen": "数|かず 、 記号|きごう 、 表記|ひょうき",
"Relationszeichen": "等号|とうごう と 不等号|ふとうごう",
"Grundrechenarten": "四則|しそく 演算|えんざん",
"Rechnen mit Brüchen": "分数|ぶんすう の 計算|けいさん",
"Potenzen, Wurzeln und Logarithmen": "累乗|るいじょう 、 累乗根|るいじょうこん 、 対数|たいすう",
"Zahlbereiche": "数|かず の 集合|しゅうごう",
"Mengen": "集合|しゅうごう",
"Gleichungen und Ungleichungen lösen": "方程式|ほうていしき と 不等式|ふとうしき を 解く|とく",
"Winkelfunktionen": "三角|さんかく 関数|かんすう",
"Intervalle und Grenzwerte": "区間|くかん と 極限|きょくげん",
"Differenzialrechnung": "微分法|びぶんほう",
"Integralrechnung": "積分法|せきぶんほう",
"Geraden und Winkel": "直線|ちょくせん と 角|かく",
"Dreiecke, Vierecke und Vielecke": "三角形|さんかくけい 、 四角形|しかくけい 、 多角形|たかくけい",
"Der Kreis und seine Teile": "円|えん と その 部分|ぶぶん",
"Körper berechnen": "立体|りったい の 体積|たいせき と 表面積|ひょうめんせき",
"Trigonometrie im Dreieck": "三角比|さんかくひ",
"Koordinaten und Geraden": "座標|ざひょう と 直線|ちょくせん",
"Kegelschnitte": "円錐|えんすい 曲線|きょくせん",
"Folgen, Vektoren, Matrizen und Kombinatorik": "数列|すうれつ 、 ベクトル 、 行列|ぎょうれつ 、 組合せ|くみあわせ",
"Das griechische Alphabet": "ギリシャ 文字|もじ",
"Wurzeln": "累乗根|るいじょうこん",
"Winkel an geschnittenen Parallelen": "平行線|へいこうせん と 角|かく",
"Vierecke und regelmäßige Vielecke": "四角形|しかくけい と 正多角形|せいたかくけい",
"Vektoren und Matrizen": "ベクトル と 行列|ぎょうれつ",
"Potenzen": "累乗|るいじょう",
"Ordnungszahlen, Indizes und Aufzählungen": "序数|じょすう 、 添え字|そえじ 、 列挙|れっきょ",
"Logarithmen": "対数|たいすう",
"Kombinatorik": "順列|じゅんれつ と 組合せ|くみあわせ",
"Gleichungsarten": "方程式|ほうていしき の 種類|しゅるい",
"Folgen und Reihen": "数列|すうれつ と 級数|きゅうすう",
"Einteilung der elementaren Funktionen": "初等|しょとう 関数|かんすう の 分類|ぶんるい",
"Dezimalzahlen, große Zahlen und Brüche": "小数|しょうすう 、 大きな|おおきな 数|かず 、 分数|ぶんすう",
"Der Graph einer Funktion": "関数|かんすう の グラフ",
"Japanische Schreibweisen": "日本|にほん の 表記|ひょうき",
"Besondere Körper": "特別|とくべつ な 立体|りったい",
"Besondere Dreiecke": "特別|とくべつ な 三角形|さんかくけい",
"Beispiel: eine lineare Ungleichung": "例|れい ： 一次|いちじ 不等式|ふとうしき",
"Beispiel: eine lineare Gleichung": "例|れい ： 一次|いちじ 方程式|ほうていしき",
}
# schon zweisprachig, bleiben unverändert
UNVERAENDERT = {"Register Deutsch -- Japanisch", "Register Japanisch -- Deutsch"}

MAKROS = r"""
% Zweisprachige Überschriften: \teil, \kapitel, \zwischen{Deutsch}{Japanisch}{Umschrift}
% Ins Inhaltsverzeichnis und in die PDF-Lesezeichen kommt nur „Deutsch -- Japanisch“ ohne Umschrift.
\newcommand\teil[3]{\part[#1 -- #2]{\raggedright #1\\[5pt]{\normalfont\Large\color{black!55}#2\hspace{0.5em}\penalty0 [#3]}}}
\newcommand\kapitel[3]{\section[#1 -- #2]{\raggedright #1\\[0pt]{\normalfont\small\color{black!55}#2\hspace{0.5em}\penalty0 [#3]}}}
\newcommand\zwischen[3]{\subsection*{\raggedright #1 {\normalfont\small\color{black!55}\,--\, #2\hspace{0.5em}\penalty0 [#3]}}}
% Die zweite Überschriftenzeile kostet Platz: Zeilen in den Listen und Tabellen etwas enger setzen
\setlength{\aboverulesep}{0.15ex}\setlength{\belowrulesep}{0.3ex}\renewcommand{\arraystretch}{0.93}
"""


def zweisprachig(tex):
    """Ersetzt im fertigen Dokument alle Überschriften durch die zweisprachige Fassung."""
    def neu(m):
        befehl, titel = m.group(1), m.group(2)
        if titel in UNVERAENDERT:
            return m.group(0)
        ja = UEB[titel]                # KeyError = Überschrift fehlt in UEB
        makro = {"part": "teil", "section": "kapitel", "subsection*": "zwischen"}[befehl]
        return f"\\{makro}{{{titel}}}{{{anzeige(ja)}}}{{{romaji(ja)}}}"
    tex = re.sub(r"\\(part|section|subsection\*)\{([^{}]*)\}", neu, tex)
    return tex.replace("\\begin{document}", MAKROS + "\n\\begin{document}", 1)
