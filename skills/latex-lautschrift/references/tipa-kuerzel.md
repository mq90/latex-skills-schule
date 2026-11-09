# tipa-Kürzel mit Beispielwörtern

Alle Einträge mit pdflatex + tipa kompiliert und am PDF geprüft.
Die Spalte „Eingabe“ ist das, was innerhalb von `\textipa{…}` bzw. `\ipa{…}`
steht. Beispiele mit `"` immer über `\ipa{…}` setzen (babel-Konflikt, siehe SKILL.md).

## Deutsch – Vokale

| Zeichen | Eingabe | Wort | Umschrift (Eingabe) |
|---|---|---|---|
| iː | `i:` | Lied | `li:t` |
| ɪ | `I` | Mitte | `"mIt@` |
| yː | `y:` | müde | `"my:d@` |
| ʏ | `Y` | Hütte | `"hYt@` |
| eː | `e:` | Beet | `be:t` |
| ɛ | `E` | Bett | `bEt` |
| ɛː | `E:` | Käse | `"kE:z@` |
| øː | `\o:` | schön | `S\o:n` |
| œ | `\oe` | Hölle | `"h\oe l@` (Leerzeichen nach `\oe`!) |
| ə | `@` | Hase | `"ha:z@` |
| ɐ | `5` | Lehrer | `"le:K5` |
| a | `a` | Mann | `man` |
| uː | `u:` | gut | `gu:t` |
| ʊ | `U` | Hund | `hUnt` |
| oː | `o:` | Boot | `bo:t` |
| ɔ | `O` | Sonne | `"zOn@` |
| aɪ | `aI` | Eis | `aIs` |
| aʊ | `aU` | Haus | `haUs` |
| ɔʏ | `OY` | Leute | `"lOYt@` |

## Deutsch – Konsonanten

| Zeichen | Eingabe | Wort | Umschrift (Eingabe) |
|---|---|---|---|
| ç | `C` | ich | `IC` |
| x | `x` | Bach | `bax` |
| ʃ | `S` | Schule | `"Su:l@` |
| ʒ | `Z` | Garage | `ga"Ka:Z@` |
| ŋ | `N` | lang | `laN` |
| ʁ | `K` | Rose | `"Ko:z@` |
| ʔ | `P` | beachten | `b@"Paxt\s{n}` |
| j | `j` | ja | `ja:` |
| z | `z` | Sonne | `"zOn@` |
| ts | `ts` | Zeit | `tsaIt` |
| pf | `pf` | Apfel | `"apf\s{l}` |
| tʃ | `tS` | deutsch | `dOYtS` |

## Englisch

| Zeichen | Eingabe | Wort | Umschrift (Eingabe) |
|---|---|---|---|
| æ | `\ae` | cat | `k\ae t` |
| ʌ | `2` | cup | `k2p` |
| ɑː | `A:` | car | `kA:` |
| ɒ | `6` | hot | `h6t` |
| ɜː | `3:` | bird | `b3:d` |
| ɔː | `O:` | law | `lO:` |
| əʊ | `@U` | go | `g@U` |
| θ | `T` | thing | `TIN` |
| ð | `D` | this | `DIs` |
| ɹ | `\*r` | red | `\*red` |
| w | `w` | we | `wi:` |
| dʒ | `dZ` | job | `dZ6b` |

## Französisch – Nasalvokale

| Zeichen | Eingabe | Wort |
|---|---|---|
| ɑ̃ / ã | `\~a` | blanc |
| ɔ̃ | `\~O` | bon |
| ɛ̃ | `\~E` | vin |
| œ̃ | `\~{\oe}` | un |

## Zeichen und Diakritika

| Zeichen | Eingabe | Bedeutung |
|---|---|---|
| ˈ | `"` oder `\textprimstress` | Hauptbetonung (vor der Silbe) |
| ˌ | `""` oder `\textsecstress` | Nebenbetonung |
| ː | `:` | lang |
| n̩, l̩ | `\s{n}`, `\s{l}` | silbisch (haben, Apfel) |
| ɪ̯ | `\textsubarch{I}` | unsilbisch (zweiter Teil eines Diphthongs) |
| n̥ | `\r*n` | stimmlos – **nicht** silbisch verwechseln |
| t̪ | `\|[t` | dental |
| tsʰ | `ts\super h` | behaucht |
| ɾ | `R` | getippter r-Laut (Tap) |
| ʀ | `\;R` | gerolltes Zäpfchen-R (uvularer Vibrant) |
| ɡ | `\textscriptg` | IPA-g |

Achtung bei Befehlen mitten im Wort: nach `\oe`, `\ae`, `\o` ein Leerzeichen
setzen, wenn ein Buchstabe folgt (`h\oe l@`), sonst liest TeX `\oel` als Befehl.
