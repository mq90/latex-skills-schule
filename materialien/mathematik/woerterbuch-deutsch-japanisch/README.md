# Mathematisches Wörterbuch Deutsch – Japanisch

Nachschlagewerk für den Mathematikunterricht: 353 Fachbegriffe mit Lesung in
Hiragana, Hepburn-Umschrift, Zeichen und Skizzen, dazu ein Teil „Mathematik lesen
und sprechen“ mit Lesarten und Beispielen in beiden Sprachen. Aufbau und Skizzen
entsprechen dem [Wörterbuch Deutsch – Englisch](../woerterbuch-deutsch-englisch).

| Datei | Inhalt |
|---|---|
| [`Mathematisches-Woerterbuch-Deutsch-Japanisch.pdf`](Mathematisches-Woerterbuch-Deutsch-Japanisch.pdf) | fertiges PDF (93 Seiten) |
| `Mathematisches-Woerterbuch-Deutsch-Japanisch.tex` | erzeugter Quelltext, kompiliert mit pdflatex |
| `quelle/` | Daten und Bausteine, aus denen `bauen.py` die `.tex`-Datei erzeugt |

## Aufbau

- **Teil I – Wörterbuch:** zehn Sachgebiete, je Zeile deutscher Begriff,
  japanischer Begriff mit Lesung und Umschrift, Zeichen oder Skizze.
- **Teil II – Mathematik lesen und sprechen:** 22 Kapitel von Zahlen und
  Relationszeichen bis Kegelschnitte und griechisches Alphabet. Je Zeile der
  Ausdruck, die japanische Lesart, ihre Umschrift und die deutsche Lesart.
  Japanische Schreibweisen, die von den deutschen abweichen (≒, ≦, ∽, ₙCₖ …),
  stehen klein unter dem Ausdruck und gesammelt in Kapitel 11.
- **Teil III – Register** Deutsch → Japanisch und Japanisch → Deutsch (nach der
  Lesung geordnet, in der Reihenfolge der japanischen Silbentafel).

Jedes Kapitel beginnt auf einer neuen Seite und endet mit Beispielen. Alle
Überschriften stehen zweisprachig da (`quelle/ueberschriften.py`).

## Bauen

```
python3 quelle/bauen.py Mathematisches-Woerterbuch-Deutsch-Japanisch.tex ../../../skills/grundlagen/latex-grundstil/assets
pdflatex Mathematisches-Woerterbuch-Deutsch-Japanisch.tex    # dreimal (Inhaltsverzeichnis, Register)
```

Das Dokument nutzt die universalen `header.tex`/`newcommands.tex`. Japanisch
setzt pdflatex mit dem Paket `CJKutf8` und den Schriften IPAex Mincho und IPAex
Gothic (`ipaex-type1`); beides ist in TeX Live und MacTeX enthalten. `CJKutf8`
wird nur in diesem Dokument geladen, nicht in der universalen `header.tex`.

## Japanisch schreiben: die Kurzschreibweise

In den Quelldateien steht Japanisch mit Lesung, Wörter durch Leerzeichen getrennt:

```
二次|にじ 方程式|ほうていしき を 解きなさい|ときなさい 。
```

`quelle/umschrift.py` macht daraus die Anzeige (二次方程式を解きなさい。), die
Lesung in Hiragana und die Umschrift (niji hōteishiki o tokinasai.). Die Regeln
stehen am Anfang der Datei; zum Ausprobieren:

```
python3 quelle/umschrift.py "直角|ちょっかく 三角形|さんかくけい"
```

Neuer Begriff: Zeile in `quelle/daten.py` ergänzen, neu bauen. Neue Lesart:
`\lies{Ausdruck}{Kurzschreibweise}{deutsche Lesart}` in `quelle/teil2.tex`.

## Stand der Prüfung

Die Lesungen aller Kanji-Wörter sind maschinell gegen ein Wörterbuch (MeCab,
UniDic) geprüft. Die Auswahl der Fachbegriffe und die Beispielsätze hat noch keine
Muttersprachlerin und kein Muttersprachler durchgesehen.
