# Ergänzungen aus den Buchseiten zu Geometrie, Stereometrie, Trigonometrie, analytischer Geometrie und Anhang.
SL = r"\textsyllabic{l}"
SN = r"\textsyllabic{n}"
ANG = '"\\ae Ng' + SL
DIAG = 'daI"\\ae g@n' + SL

ZUSATZ2 = [
# --- Geometrie: Grundbegriffe ---
("Winkel", [
("der", "Scheitel", "", "vertex", '"v3:teks', r"\skScheitel"),
("der", "Schenkel", "", "arm, leg", 'A:m, leg', r"\skSchenkel"),
("die", "Winkelhalbierende", "", "angle bisector", ANG+' baI"sekt@', r"\skWinkelhalbierende"),
]),
("Nebenwinkel", [
("der", "Komplementwinkel", "", "complementary angle", '""k6mplI"mentri '+ANG, r"$\alpha + \beta = 90\degree$ \newline \skKomplement"),
("der", "Supplementwinkel", "", "supplementary angle", '""s2plI"mentri '+ANG, r"$\alpha + \beta = 180\degree$"),
]),
("Wechselwinkel", [
("", "entgegengesetzt liegende Winkel", "", "co-interior angles, allied angles", '""k@UIn"tI@ri@ '+ANG+'z, "\\ae laId '+ANG+'z', r"$\alpha + \beta = 180\degree$ \newline \skEntgegen"),
("die", "Mittelsenkrechte", "", "perpendicular bisector", '""p3:p@n"dIkj@l@ baI"sekt@', r"\skMittelsenkrechte"),
]),
# --- Ebene Figuren ---
("Dreieck", [
("der", "Innenwinkel", "", "interior angle", 'In"tI@ri@ '+ANG, r"$\alpha + \beta + \gamma = 180\degree$ \newline \skInnenwinkel"),
("der", "Außenwinkel", "", "exterior angle", 'Ik"stI@ri@ '+ANG, r"\skAussenwinkel"),
("das", "unregelmäßige Dreieck", "", "scalene triangle", '"skeIli:n "traI\\ae Ng'+SL, r"\skDreieck"),
]),
("gleichschenklige Dreieck", [
("die", "Basis (im Dreieck)", "", "base", 'beIs', r"\skBasis"),
("der", "Basiswinkel", "", "base angle", '"beIs ""\\ae Ng'+SL, r"\skBasiswinkel"),
]),
("Kathete", [
("die", "Ankathete", "", "adjacent side", '@"dZeIs'+SN+'t saId', r"\skAnkathete"),
("die", "Gegenkathete", "", "opposite side", '"6p@zIt saId', r"\skGegenkathete"),
]),
("Höhe", [
("die", "Seitenhalbierende", "", "median", '"mi:di@n', r"\skSeitenhalbierende"),
("der", "Inkreis", "", "incircle, inscribed circle", '"Ins3:k'+SL+', In"skraIbd "s3:k'+SL, r"\skInkreis"),
("der", "Umkreis", "", "circumcircle", '"s3:k@m""s3:k'+SL, r"\skUmkreis"),
("", "flächengleich", "", "equal in area", '"i:kw@l In "e@ri@', r"$A_1 = A_2$"),
]),
("Viereck", [
("die", "Diagonale", "", "diagonal", DIAG, r"\skDiagonale"),
]),
("regelmäßige Sechseck", [
("das", "Fünfeck", "", "pentagon", '"pent@g@n', r"\skNeck{5}"),
("das", "Achteck", "", "octagon", '"6kt@g@n', r"\skNeck{8}"),
("das", "Zwölfeck", "", "dodecagon", 'd@U"dek@g@n', r"\skNeck{12}"),
]),
("Sehne", [
("die", "Sekante", "", "secant", '"si:k@nt', r"\skSekante"),
("der", "Berührungspunkt", "", "point of tangency", '"pOInt @v "t\\ae ndZ@nsi', r"\skBeruehrpunkt"),
("der", "Kreisbogen", "", "arc", 'A:k', r"\skKreisbogen"),
("der", "Kreisabschnitt", "", "segment (of a circle)", '"segm@nt', r"\skKreisabschnitt"),
("die", "Kreisfläche", "", "area of a circle", '"e@ri@ @v @ "s3:k'+SL, r"$A = \pi r^2$ \newline \skKreisflaeche"),
]),
# --- Körper ---
("Seitenfläche", [
("die", "Grundfläche", "", "base", 'beIs', r"\skGrundflaeche"),
("die", "Deckfläche", "", "top face", '"t6p feIs', r"\skDeckflaeche"),
("die", "Mantelfläche", "", "lateral surface, curved surface", '"l\\ae t@r@l "s3:fIs, "k3:vd "s3:fIs', r"$M = 2\pi r h$ \newline \skMantel"),
("die", "Flächendiagonale", "", "face diagonal", '"feIs '+DIAG, r"\skFlaechendiagonale"),
("die", "Raumdiagonale", "", "space diagonal", '"speIs '+DIAG, r"$d = \sqrt{a^2 + b^2 + c^2}$ \newline \skRaumdiagonale"),
]),
("Kugel", [
("das", "Polyeder", "", "polyhedron", '""p6li"hi:dr@n', ""),
("das", "Tetraeder", "", "tetrahedron", '""tetr@"hi:dr@n', r"\skTetraeder"),
("der", "Pyramidenstumpf", "", "frustum of a pyramid", '"fr2st@m @v @ "pIr@mId', r"\skPyramidenstumpf"),
("der", "Kegelstumpf", "", "frustum of a cone", '"fr2st@m @v @ "k@Un', r"\skKegelstumpf"),
("der", "Hohlzylinder", "", "hollow cylinder", '"h6l@U "sIlInd@', r"\skHohlzylinder"),
("der", "schiefe Zylinder", "", "oblique cylinder", '@"bli:k "sIlInd@', r"\skSchieferZylinder"),
("der", "Rotationskörper", "", "solid of revolution", '"s6lId @v ""rev@"lu:S'+SN, r"\skRotation"),
("das", "Kugelsegment", "", "spherical cap, spherical segment", '"sferIk'+SL+' k\\ae p', r"\skKugelsegment"),
("der", "Kugelsektor", "", "spherical sector", '"sferIk'+SL+' "sekt@', r"\skKugelsektor"),
("das", "Rotationsellipsoid", "", "spheroid", '"sfI@rOId', r"\skEllipsoid"),
("das", "Rotationsparaboloid", "", "paraboloid of revolution", 'p@"r\\ae b@lOId', r"\skParaboloid"),
("das", "Rotationshyperboloid", "", "hyperboloid of revolution", 'haI"p3:b@lOId', r"\skHyperboloid"),
]),
# --- Funktionen / Trigonometrie ---
("Arkusfunktion", [
("der", "Einheitskreis", "", "unit circle", '"ju:nIt ""s3:k'+SL, r"\skEinheitskreis"),
("das", "Gradmaß", "", "degree measure", 'dI"gri: ""meZ@', r"$360\degree$"),
("das", "Bogenmaß", "", "radian measure", '"reIdi@n ""meZ@', r"$180\degree \mathrel{\widehat{=}} \pi$ \newline \skBogenmass"),
("der", "Sinussatz", "", "sine rule, law of sines", '"saIn ru:l', r"$\frac{a}{\sin\alpha} = \frac{b}{\sin\beta} = \frac{c}{\sin\gamma}$"),
("der", "Kosinussatz", "", "cosine rule, law of cosines", '"k@UsaIn ru:l', r"\small$c^2 = a^2 + b^2 - 2ab\cos\gamma$"),
]),
# --- Analysis ---
("Nullfolge", [
("die", "arithmetische Folge", "", "arithmetic sequence", '""\\ae rIT"metIk "si:kw@ns', r"$a_{n+1} = a_n + d$"),
("die", "geometrische Folge", "", "geometric sequence", '""dZi:@"metrIk "si:kw@ns', r"$a_{n+1} = a_n \cdot q$"),
("das", "Anfangsglied", "", "first term", '"f3:st t3:m', r"$a_1$"),
]),
("Reihe", [
("die", "unendliche Reihe", "", "infinite series", '"InfIn@t "sI@ri:z', r"$\displaystyle\sum_{k=1}^{\infty} a_k$"),
("die", "Potenzreihe", "", "power series", '"paU@ ""sI@ri:z', r"$\displaystyle\sum_{k=0}^{\infty} a_k x^k$"),
]),
# --- Vektoren und analytische Geometrie ---
("Ortsvektor", [
("der", "Einheitsvektor", "", "unit vector", '"ju:nIt ""vekt@', r"$|\vec{e}\,| = 1$"),
("der", "Nullvektor", "", "zero vector", '"zI@r@U ""vekt@', r"$\vec{0}$"),
]),
("Ebene", [
("die", "Geradengleichung", "", "equation of a straight line", 'I"kweIZ'+SN+' @v @ ""streIt "laIn', r"$y = mx + n$"),
("der", "Steigungswinkel", "", "angle of inclination", ANG+' @v ""InklI"neIS'+SN, r"$m = \tan\alpha$"),
("die", "Polarkoordinaten", "", "polar coordinates", '"p@Ul@ k@U"O:dIn@ts', r"$P(r;\,\varphi)$ \newline \skPolar"),
("der", "Kegelschnitt", "", "conic section", '"k6nIk "sekS'+SN, ""),
("die", "Kreisgleichung", "", "equation of a circle", 'I"kweIZ'+SN+' @v @ "s3:k'+SL, r"$x^2 + y^2 = r^2$ \newline \skKreisgleichung"),
("die", "Ellipse", "", "ellipse", 'I"lIps', r"$\frac{x^2}{a^2} + \frac{y^2}{b^2} = 1$ \newline \skEllipse"),
("die", "Hyperbel", "", "hyperbola", 'haI"p3:b@l@', r"$\frac{x^2}{a^2} - \frac{y^2}{b^2} = 1$ \newline \skHyperbel"),
("der", "Brennpunkt", "", "focus", '"f@Uk@s', r"\skBrennpunkt"),
("die", "Halbachse", "", "semi-axis", '""semi"\\ae ksIs', r"\skHalbachse"),
("die", "Leitlinie", "", "directrix", 'd@"rektrIks', r"\skLeitlinie"),
]),
("Matrix", [
("die", "quadratische Matrix", "", "square matrix", '"skwe@ "meItrIks', r"$n \times n$"),
("die", "Zeile", "", "row", 'r@U', ""),
("die", "Spalte", "", "column", '"k6l@m', ""),
("die", "Hauptdiagonale", "", "main diagonal", '"meIn '+DIAG, r"$\begin{pmatrix} \frot{a} & b\\ c & \frot{d}\end{pmatrix}$"),
("die", "Determinante", "", "determinant", 'dI"t3:mIn@nt', r"$\begin{vmatrix} a & b\\ c & d\end{vmatrix} = ad - bc$"),
]),
# --- Stochastik ---
("Fakultät", [
("die", "Permutation", "", "permutation", '""p3:mju"teIS'+SN, r"$n!$"),
("die", "Variation", "", "variation, arrangement", '""ve@ri"eIS'+SN+', @"reIndZm@nt', r"$\dfrac{n!}{(n-k)!}$"),
("die", "Kombination", "", "combination", '""k6mbI"neIS'+SN, r"$\dbinom{n}{k}$"),
]),
]
