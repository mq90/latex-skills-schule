---
name: latex-geodaten-karten
description: Echte Landkarten in LaTeX/TikZ zeichnen – Deutschland mit Bundesländern, Sachsen, Europa, Weltkarten in verschiedenen Projektionen, Flüsse, Seen, Gebirge, Straßen, historische Grenzen – aus freien Geodaten (GeoJSON) mit dem Skript geo2tikz.py. Verwende diesen Skill immer, wenn jemand eine Karte, stumme Karte, Umrisskarte, Länder- oder Bundesländerkarte, Kartenprojektionen (Mercator, Robinson, Equal Earth), Polygonvereinfachung (Douglas-Peucker) oder Geografie-Arbeitsblätter mit LaTeX oder TikZ erstellen will.
---

# Karten aus Geodaten mit TikZ

Karten nie „aus dem Kopf“ als Koordinaten zeichnen – das wird nie richtig.
Stattdessen freie Geodaten laden und mit `scripts/geo2tikz.py` in TikZ-Pfade
umrechnen lassen. Das Skript projiziert, vereinfacht, schneidet zu und
schreibt eine `.tex`-Datei mit einem Makro pro Ebene.

## Arbeitsablauf

1. **Daten holen** (GeoJSON, siehe Datenquellen unten), z. B.:
   ```bash
   B=https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson
   curl -sSfLO $B/ne_10m_admin_1_states_provinces.geojson   # 39 MB
   curl -sSfLO $B/ne_10m_rivers_lake_centerlines.geojson
   curl -sSfLO $B/ne_10m_lakes.geojson
   curl -sSfLO $B/ne_50m_admin_0_countries.geojson
   ```
2. **Umrechnen** – alle Ebenen in *einem* Aufruf, damit sie übereinanderpassen:
   ```bash
   pip install shapely pyproj
   python3 scripts/geo2tikz.py --bbox 5.8,47.2,15.1,55.1 --breite 12 --proj EPSG:3035 \
     --ebene "name=laender; datei=ne_10m_admin_1_states_provinces.geojson; filter=iso_a2=DE; id=iso_3166_2" \
     --ebene "name=nachbarn; datei=ne_50m_admin_0_countries.geojson; filter=ISO_A2_EH=PL|CZ|AT|CH|FR|BE|NL|LU|DK; id=ISO_A2_EH" \
     --ebene "name=fluesse; datei=ne_10m_rivers_lake_centerlines.geojson; id=name" \
     --ebene "name=seen; datei=ne_10m_lakes.geojson; id=name" \
     -o karte_daten.tex
   ```
   Das Skript meldet Objektzahl und Kartengröße (z. B. „12.0 × 15.2 cm“).
3. **Gestalten** mit `assets/vorlage_karte.tex`: `\input{karte_daten}`, dann
   Stile setzen und die Ebenen in der gewünschten Reihenfolge aufrufen
   (unten zuerst: Nachbarn → Länder → Seen → Flüsse → Beschriftung).
4. Kompilieren, als Bild rendern, ansehen. Erst dann ausliefern.

## Was die erzeugte Datei bereitstellt

| Element | Beispiel | Zweck |
|---|---|---|
| Makro pro Ebene | `\geolaender` | zeichnet alle Objekte der Ebene |
| Stil der Ebene | `geo laender/.style={fill=gray!15, draw=white}` | Aussehen aller Objekte |
| Stil pro Objekt | `geo laender/DE-SN/.style={fill=red!40}` | ein Objekt hervorheben |
| Punkt pro Objekt | `\node at (laender-DE-SN) {Sachsen};` | Beschriften (Punkt liegt garantiert innen) |

**Punkt-Ebenen** (Städte) zeichnen nichts, legen aber beim Aufruf die Punkte an.
Das Makro also trotzdem aufrufen, dann z. B.:
`\geostaedte \fill (staedte-Leipzig) circle (2pt) node[right]{Leipzig};`
(Städte: `ne_10m_populated_places_simple`, Filter `adm0_a3=DEU`, ID `name`.)

Stile sind leer vordefiniert, also nach `\input` einfach mit `\tikzset`
überschreiben. Ohne Stil wird nichts gezeichnet (`\path`), das ist Absicht.
Die ID kommt aus der Eigenschaft `id=`, Umlaute werden ersetzt (Müritz → Mueritz),
Leerzeichen zu `-`, mehrfach vorkommende IDs bekommen `-2`, `-3` (Rhein, Rhein-2).

## Optionen von geo2tikz.py

| Option | Bedeutung |
|---|---|
| `--bbox lon1,lat1,lon2,lat2` | Ausschnitt in Grad. Bei negativen Werten mit `=` schreiben: `--bbox=-180,-60,180,84` |
| `--breite 12` | Kartenbreite in cm, Höhe ergibt sich |
| `--proj` | `plattkarte` (Standard), `mercator`, oder ein Code: `EPSG:3035` (Europa, flächentreu), `EPSG:25833` (Ostdeutschland/Sachsen), `EPSG:25832` (West), `EPSG:8857` (Equal Earth, Welt), `ESRI:54030` (Robinson, Welt) |
| `--toleranz 0.02` | Vereinfachung in cm (Douglas-Peucker). Größer = kleinere Datei, gröbere Umrisse. `0` = aus |
| `--nachkomma 2` | Nachkommastellen der Koordinaten |

## Datenquellen und Lizenzen

| Quelle | Inhalt | Lizenz |
|---|---|---|
| **Natural Earth** (github.com/nvkelso/natural-earth-vector, Ordner `geojson/`) | Staaten (`ne_50m_admin_0_countries`), Bundesländer/Provinzen (`ne_10m_admin_1_states_provinces`), Flüsse, Seen, Gebirgsregionen (`ne_10m_geography_regions_polys`), Straßen (`ne_10m_roads`), Bahn (`ne_10m_railroads`), Städte (`ne_10m_populated_places_simple`, Punkte) | gemeinfrei – Quellenangabe trotzdem üblich |
| historical-basemaps (github.com/aourednik/historical-basemaps) | Weltgrenzen zu Stichjahren, z. B. `world_1938.geojson` | GPL-3.0: Quelle nennen; abgeleitete *Daten* müssen GPL bleiben |
| AWMC geodata (github.com/AWMC/geodata) | Antike, z. B. Römisches Reich (`Cultural-Data/political_shading/`) | ODbL: Quelle nennen, Datenbank-Weitergabe unter ODbL |

Rohdaten **nicht** in ein öffentliches Repo oder Material-Paket legen
(Größe, Lizenzpflichten). Besser: Download-Befehl dokumentieren. Auf jede
Karte eine Quellenzeile setzen (in der Vorlage enthalten).

## Stolpersteine (getestet)

- **Frankreich und Norwegen fehlen** beim Filter `ISO_A2=FR`: In Natural Earth
  steht dort `-99`. Für Staaten `ISO_A2_EH` oder `ADM0_A3` (DEU, FRA) verwenden.
- Bundesländer: Datei `ne_10m_admin_1_states_provinces`, Filter `iso_a2=DE`,
  ID `iso_3166_2` → `DE-SN`, `DE-BY`, `DE-BE` …
- **Alle Ebenen in einem Aufruf.** Getrennte Aufrufe haben verschiedene Maßstäbe,
  dann liegen Flüsse neben den Ländern.
- Benachbarte Flächen werden einzeln vereinfacht. Bei großer `--toleranz`
  entstehen an gemeinsamen Grenzen kleine Lücken – dann Toleranz senken.
- Der Zuschnitt erfolgt am rechteckigen Kartenrand nach der Projektion. Für
  einen sauberen Rand im Dokument `\clip (0,0) rectangle (Breite,Höhe);`
  (Werte stehen am Ende der erzeugten Datei).
- Flussnamen sind uneinheitlich (Rhein/Rhin/Rhine, je nach Abschnitt).
  Erst `grep -o "fluesse/[A-Za-z-]*" karte_daten.tex | sort -u` ansehen,
  dann Stile setzen.
- Große Dateien (Welt in 10m) machen LaTeX langsam: für Übersichtskarten 50m-
  oder 110m-Daten und eine größere Toleranz nehmen.

## Ideen für den Unterricht

- **Informatik:** Douglas-Peucker als Algorithmus (Sachsen mit Toleranz
  0 / 0.05 / 0.2 cm nebeneinander, Punktzahl vergleichen), GeoJSON als
  Datenformat, Vierfarbensatz mit Greedy- oder DSatur-Färbung der Europakarte.
- **Mathematik:** Projektionen vergleichen (Mercator vs. Equal Earth: Grönland
  gegen Afrika), Maßstab und Flächenberechnung, Koordinatensysteme.
- **Geografie/Geschichte:** stumme Karten zum Beschriften, Grenzen 1938/1945/1990.

## Für eine Handreichung

Aufbau und Listing-Stil aus `latex-grundstil` übernehmen
(`assets/vorlage_handreichung.tex` dort): `\input{header.tex}` und
`\input{newcommands.tex}`, Titel/Autor/Datum mit `\maketitle`, Kapitel mit
`\section`, jedes Beispiel erst als `\begin{lstlisting}[style=latex]` und
**direkt darunter** dasselbe ausgeführt in `\begin{ausgabe}`. Jedes Beispiel
kompilieren und das PDF als Bild prüfen.

Karten-Code in der Handreichung nur mit kleinen Ausschnitten zeigen – die
erzeugten Pfade sind lang. Die Ausgabe darunter darf die ganze Karte sein.
