## Meilensteinbericht 1 (zum 8.6.21)

Das Vorgehen bis zum ersten Meilenstein verlief soweit weitestgehend nach Plan, 
es gab allerdings einige unvorhergesehene Schwierigkeiten im Bereich der Datenvorverarbeitung,
die das Vorankommen erschwerten.

### Model
Die Implementierung des zuvor recherchierten Modells wurde beendet.

### Datenvorverarbeitung
Hier mussten einige Probleme mit dem dem Datenset beiliegenden Skript behoben werden, das Frames aus Videos extrahiert. 
Aus den so gewonnenen Frames wurden mittels der im letzten Meilenstein implementierten Gesichtserkennung Gesichter ausgeschnitten und in 32x32 Pixel
großen Bildern gespeichert. Dieser Part der Vorverarbeitung auf einzelnen Bildern wurde mittels des *joblib*-Pakets auf mehreren CPUs durch Multiprocessing parallelisiert.
Des weiteren mussten zu den so gewonnenen Gesichtsbildern Label im .csv-Format generiert werden, welche die Label aus den 
Videos darstellten und von *Keras* nutzbar sind.

### Infrastruktur
Es wurde ein Zugang zu Rechnern der CV-Gruppe angefragt, welche über eine GPU verfügen, um das Training später zu beschleunigen.
Auf das dortige Netzwerk wurden mittels *scp*-Befehl die Daten geladen.

### Gesichtsmerkmale

### Andere Eingabemethoden

### Verzögerungen 
Durch Probleme beim Upload und Unklarheit bezüglich der Bedienung der Rechner der CV-Gruppe sowie mehr benötigter Vorverarbeitung als erwartet
konnte das Training des Modells noch nicht begonnen werden. 