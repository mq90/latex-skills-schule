# Ergänzungen aus den Buchseiten (Fachbegriffe), eingefügt jeweils NACH dem genannten Ankerbegriff.
# Format wie daten.py; deutsche Lautschrift wird nicht mehr ausgegeben (leer).
SL = r"\textsyllabic{l}"
SN = r"\textsyllabic{n}"

ZUSATZ = [
# --- Zahlen und Rechenarten ---
("Ziffer", [
("die", "Ordnungszahl", "", "ordinal number", '"O:dIn'+SL+' "n2mb@', r"1.\ 2.\ 3. \newline \footnotesize engl. 1st, 2nd, 3rd"),
("der", "Index", "", "subscript, index", '"s2bskrIpt, "Indeks', r"$x_1;\ x_2;\ \ldots;\ x_n$"),
]),
("reelle Zahl", [
("die", "irrationale Zahl", "", "irrational number", 'I"r\\ae S@n'+SL+' "n2mb@', r"$\sqrt{2};\ \pi$"),
("die", "komplexe Zahl", "", "complex number", '"k6mpleks "n2mb@', r"$\C$ \newline $z = a + b\,\mathrm{i}$"),
("die", "imaginäre Einheit", "", "imaginary unit", 'I"m\\ae dZIn@ri "ju:nIt', r"$\mathrm{i}^2 = -1$"),
]),
("Summe", [
("der", "Summand", "", "summand, addend", '"s2m\\ae nd, "\\ae dend', r"$\underbrace{a}_{\text{Summand}} + \underbrace{b}_{\text{Summand}}$"),
]),
("Differenz", [
("der", "Minuend", "", "minuend", '"mInjuend', r"$\underbrace{a}_{\text{Minuend}} - \underbrace{b}_{\text{Subtrahend}}$"),
("der", "Subtrahend", "", "subtrahend", '"s2btr@hend', r"$a - \frot{b}$"),
]),
("Produkt", [
("der", "Faktor", "", "factor", '"f\\ae kt@', r"$\underbrace{a}_{\text{Faktor}} \cdot \underbrace{b}_{\text{Faktor}}$"),
]),
("Quotient", [
("der", "Dividend", "", "dividend", '"dIvIdend', r"$\underbrace{a}_{\text{Dividend}} : \underbrace{b}_{\text{Divisor}}$"),
("der", "Divisor", "", "divisor", 'dI"vaIz@', r"$a : \frot{b}$"),
]),
("Nenner", [
("der", "echte Bruch", "", "proper fraction", '"pr6p@ "fr\\ae kS'+SN, r"$\dfrac{3}{4}$"),
("der", "unechte Bruch", "", "improper fraction", 'Im"pr6p@ "fr\\ae kS'+SN, r"$\dfrac{7}{4}$"),
("die", "gemischte Zahl", "", "mixed number", '"mIkst "n2mb@', r"$1\tfrac{3}{4}$"),
("", "gleichnamige Brüche", "", "like fractions", '"laIk "fr\\ae kS'+SN+'z', r"$\dfrac{1}{5};\ \dfrac{3}{5}$"),
("", "ungleichnamige Brüche", "", "unlike fractions", '""2n"laIk "fr\\ae kS'+SN+'z', r"$\dfrac{1}{2};\ \dfrac{1}{3}$"),
("der", "Hauptnenner", "", "lowest common denominator", '"l@UIst "k6m@n dI"n6mIneIt@', r"$\dfrac{1}{2} + \dfrac{1}{3} = \dfrac{3}{\frot{6}} + \dfrac{2}{\frot{6}}$"),
("", "kürzen", "", "cancel, reduce", '"k\\ae ns'+SL+', rI"dju:s', r"$\dfrac{6}{8} = \dfrac{3}{4}$"),
("", "erweitern", "", "expand (a fraction)", 'Ik"sp\\ae nd', r"$\dfrac{3}{4} = \dfrac{15}{20}$"),
]),
("Kehrwert", [
("das", "Verhältnis", "", "ratio", '"reISi@U', r"$a : b$"),
("die", "Verhältnisgleichung", "", "proportion", 'pr@"pO:S'+SN, r"$a : b = c : d$"),
]),
("Quadratwurzel", [
("die", "Kubikwurzel", "", "cube root", '"kju:b "ru:t', r"$\sqrt[3]{a}$"),
("die", "$n$-te Wurzel", "", "$n$th root", '"enT "ru:t', r"$\sqrt[n]{a}$"),
("der", "Radikand", "", "radicand", '"r\\ae dIk\\ae nd', r"$\sqrt[n]{\frot{a}}$"),
("der", "Wurzelexponent", "", "index (of a root)", '"Indeks', r"$\sqrt[\frot{n}]{a}$"),
("", "potenzieren", "", "raise to a power", '"reIz tu: @ "paU@', r"$2^5 = 32$"),
("", "quadrieren", "", "square", 'skwe@', r"$7^2 = 49$"),
("", "radizieren, Wurzel ziehen", "", "extract a root", 'Ik"str\\ae kt @ "ru:t', r"$\sqrt{49} = 7$"),
]),
("ungleich", [
("", "identisch gleich", "", "identically equal", 'aI"dentIkli "i:kw@l', r"$\equiv$"),
]),
("größer als", [
("", "kleiner oder gleich", "", "less than or equal to", '"les D@n O:r "i:kw@l tu:', r"$\le$"),
("", "größer oder gleich", "", "greater than or equal to", '"greIt@ D@n O:r "i:kw@l tu:', r"$\ge$"),
("", "viel kleiner als", "", "much less than", '"m2tS "les D@n', r"$\ll$"),
("", "proportional zu", "", "proportional to", 'pr@"pO:S@n'+SL+' tu:', r"$y \sim x$ \newline \footnotesize engl. $y \propto x$"),
]),
# --- Algebra ---
("Term", [
("die", "Unbekannte", "", "unknown", '""2n"n@Un', r"$x$"),
("der", "Koeffizient", "", "coefficient", '""k@UI"fIS'+SN+'t', r"$\frot{3}x^2$"),
("der", "Grad", "", "degree", 'dI"gri:', r"$x^3 + x$: 3.\,Grad"),
]),
("Gleichungssystem", [
("die", "lineare Gleichung", "", "linear equation", '"lIni@ I"kweIZ'+SN, r"$3x - 7 = 11$"),
("die", "quadratische Gleichung", "", "quadratic equation", 'kw6"dr\\ae tIk I"kweIZ'+SN, r"$x^2 - 5x + 6 = 0$"),
("die", "Wurzelgleichung", "", "radical equation", '"r\\ae dIk'+SL+' I"kweIZ'+SN, r"$\sqrt{x + 3} = 5$"),
("die", "Exponentialgleichung", "", "exponential equation", '""eksp@"nenS'+SL+' I"kweIZ'+SN, r"$2^x = 64$"),
("die", "logarithmische Gleichung", "", "logarithmic equation", '""l6g@"rIDmIk I"kweIZ'+SN, r"$\log_3 x = 4$"),
("die", "trigonometrische Gleichung", "", "trigonometric equation", '""trIg@n@"metrIk I"kweIZ'+SN, r"$2\sin x = 1$"),
]),
("Klammer", [
("die", "runden Klammern", "", "round brackets, parentheses", '"raUnd "br\\ae kIts, p@"renT@si:z', r"$(\ \ )$"),
("die", "eckigen Klammern", "", "square brackets", '"skwe@ "br\\ae kIts', r"$[\ \ ]$"),
("die", "geschweiften Klammern", "", "curly brackets, braces", '"k3:li "br\\ae kIts, "breIsIz', r"$\{\ \ \}$"),
]),
("Teilmenge", [
("die", "echte Teilmenge", "", "proper subset", '"pr6p@ "s2bset', r"$A \subset B$"),
]),
("Vereinigungsmenge", [
("die", "Differenzmenge", "", "set difference", '"set "dIfr@ns', r"$A \setminus B$"),
("das", "kartesische Produkt", "", "Cartesian product", 'kA:"ti:zi@n "pr6d2kt', r"$A \times B$"),
]),
# --- Funktionen ---
("Funktion", [
("die", "unabhängige Variable", "", "independent variable", '""IndI"pend@nt "ve@ri@b'+SL, r"$x$"),
("die", "abhängige Variable", "", "dependent variable", 'dI"pend@nt "ve@ri@b'+SL, r"$y = f(x)$"),
("der", "Funktionswert", "", "value of a function", '"v\\ae lju: @v @ "f2NkS'+SN, r"$f(3) = 15$"),
]),
("Ursprung", [
("die", "Koordinaten", "", "coordinates", 'k@U"O:dIn@ts', r"$P(x_P \mid y_P)$"),
("die", "Abszisse", "", "abscissa", '\\ae b"sIs@', r"$P(\frot{x_P} \mid y_P)$"),
("die", "Ordinate", "", "ordinate", '"O:dIn@t', r"$P(x_P \mid \frot{y_P})$"),
]),
("Parabel", [
("die", "ganzrationale Funktion", "", "polynomial function", '""p6li"n@Umi@l "f2NkS'+SN, r"$f(x) = x^3 - 2x$"),
("die", "gebrochenrationale Funktion", "", "rational function", '"r\\ae Sn@l "f2NkS'+SN, r"$f(x) = \dfrac{x + 1}{x - 2}$"),
("die", "Wurzelfunktion", "", "square root function", '""skwe@ "ru:t "f2NkS'+SN, r"$f(x) = \sqrt{x}$"),
]),
("Tangens", [
("der", "Kotangens", "", "cotangent", '""k@U"t\\ae ndZ@nt', r"$\cot x = \dfrac{\cos x}{\sin x}$"),
("die", "Arkusfunktion", "", "inverse trigonometric function", '""Inv3:s ""trIg@n@"metrIk "f2NkS'+SN, r"$\arcsin x$ \newline \footnotesize engl. auch $\sin^{-1} x$"),
]),
# --- Analysis ---
("Folge", [
("die", "Nullfolge", "", "null sequence", '"n2l "si:kw@ns', r"$\limn a_n = 0$"),
("", "konvergent", "", "convergent", 'k@n"v3:dZ@nt', ""),
("", "divergent", "", "divergent", 'daI"v3:dZ@nt', ""),
]),
("stetig", [
("", "unstetig", "", "discontinuous", '""dIsk@n"tInju@s', ""),
("das", "Intervall", "", "interval", '"Int@v'+SL, r"$[a;\,b]$"),
]),
("Ableitung", [
("die", "Differenzialrechnung", "", "differential calculus", '""dIf@"renS'+SL+' "k\\ae lkj@l@s', ""),
("der", "Differenzialquotient", "", "differential quotient", '""dIf@"renS'+SL+' "kw@US'+SN+'t', r"$\dfrac{\mathrm{d}y}{\mathrm{d}x}$"),
("das", "Differenzial", "", "differential", '""dIf@"renS'+SL, r"$\mathrm{d}y$"),
("die", "partielle Ableitung", "", "partial derivative", '"pA:S'+SL+' dI"rIv@tIv', r"$\dfrac{\partial z}{\partial x}$"),
]),
("Stammfunktion", [
("die", "Integralrechnung", "", "integral calculus", '"IntIgr@l "k\\ae lkj@l@s', ""),
("das", "unbestimmte Integral", "", "indefinite integral", 'In"defIn@t "IntIgr@l', r"$\displaystyle\int f(x)\dx$"),
("das", "bestimmte Integral", "", "definite integral", '"defIn@t "IntIgr@l', r"$\displaystyle\int_a^b f(x)\dx$"),
("das", "Integralzeichen", "", "integral sign", '"IntIgr@l saIn', r"$\displaystyle\int$"),
("der", "Integrand", "", "integrand", '"IntIgr\\ae nd', r"$\displaystyle\int \frot{f(x)}\dx$"),
("die", "Integrationsvariable", "", "variable of integration", '"ve@ri@b'+SL+' @v ""IntI"greIS'+SN, r"$\displaystyle\int f(\frot{x})\,\mathrm{d}\frot{x}$"),
("die", "Integrationskonstante", "", "constant of integration", '"k6nst@nt @v ""IntI"greIS'+SN, r"$F(x) + \frot{C}$"),
("die", "Obersumme", "", "upper sum", '"2p@ s2m', r"\skObersumme"),
("die", "Untersumme", "", "lower sum", '"l@U@ s2m', r"\skUntersumme"),
]),
]
