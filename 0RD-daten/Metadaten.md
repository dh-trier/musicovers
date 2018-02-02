
Metadaten zu den Albencovern
============================
Erstellt: 25.11.2017
Stand: 02.01.2018

## Datei "all_albums.json"
* Insgesamt 17.500 Datensätze
* Enthält zu jedem der fünf Genres 3.500 Alben mit den dazugehörigen Metadaten (inkl. Veröffentlichungsjahr).
  * Konnte zu einem Album kein Veröffentlichungsjahr ermittelt werden, steht in dem entsprechenden Feld der Wert "0".
* Zu jedem Album ist im Feld "cover_from" angegeben, ob ein Cover gefunden und heruntergeladen werden konnte.
  * Falls ein Cover gefunden wurde, findet sich als Wert in diesem Feld die MusicBrainz-ID der jeweiligen Veröffentlichung.
  * Falls kein Cover gefunden wurde, steht dort "no_cover_found".
  
## Datei "all_albums.csv"
* Insgesamt 16.987 Datensätze
* Enthält alle Datensätze aus der JSON-Datei, bei denen ein Veröffentlichungsjahr angegeben ist.
* Enthält somit auch diejenigen Datensätze, zu denen es kein Cover gibt oder die vor 1990 bzw. nach 2009 erschienen sind

## Python-Skripte
* Die Python-Skripte "Albums.py" und "Cover.py" haben mithilfe der JSON-Datei 10.973 Cover heruntergeladen.
* Davon habe ich nur diejenigen ausgewählt, deren Erscheinungsjahr zwischen 1990 und 2009 liegt.
* Anzahl der Cover pro Genre:
  * Rock: 1.407 (= 21.33 %)
  * Pop: 1.103 (= 16.72 %)
  * Electronic: 1.324 (= 20.07 %)
  * Hip-Hop: 1.675 (= 25.39 %)
  * Country: 1.087 (= 16.48 %)
  * Insgesamt: 6.596 (= 100 %)
* Diese Cover finden sich in dem Ordner "Albencover" in "covers_1990-2009.zip".

## Weiterverarbeitung der Cover
* Das Skript in "coverPreprocessing.py" versucht, die Cover mit OpenCV zu öffnen. Sollte dies nicht funktionieren, wird das entsprechende Bild in den Ordner "not_used/broken" verschoben.
* Für die anderen Cover werden die Höhe und Breite sowie deren Seitenverhältnisse ermittelt und in die Datei "shapes.csv" geschrieben.
* Die meisten Cover sind nahezu quadratisch (siehe "ratios.png"). Daher werden Cover mit einem Seitenverhältnis < 0.85 oder > 1.15 als Ausreißer betrachtet und in den Ordner "not_used/non_quadratic" verschoben.
* (Zur Dokumentation der Zwischenergebnisse der o.g. Schritte siehe auch "doc.txt")
* Somit bleiben in den einzelnen Genres:
  * Rock: 1.394 (= 21.52 %)
  * Pop: 1.086 (= 16.76 %)
  * Electronic: 1.282 (= 19.79 %)
  * Hip-Hop: 1.650 (= 25.47 %)
  * Country: 1.067 (= 16.47 %)
  * Insgesamt: 6.479 (= 100 %)
  
## Auswahl einer Zufallsstichprobe als Trainingsdatensatz
* Das Skript "chooseRandomCovers.py" erzeugt den Ordner "random" und kopiert in diesen 100 zufällig ausgewählte Coverbilder aus jedem Genre.

## Alle aktuellen Coverbilder finden sich nun in Seafile im Ordner "Albencover" in den jeweiligen Genre-Unterordnern.