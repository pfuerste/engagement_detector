## Meilensteinbericht 4 (zum 6.7.21)

Zum letzten Meilenstein wurden die vorherigen Teile der Pipeline zusammengesetzt und teilweise noch verändert.

### Persistenz
Das Programm speichert Gesichtsencodings und Modellausgaben automatisch als .npy in Pfaden ab, die aus dem Vorlesungsnamen und einem timestamp bestehen. 
Bei erneutem Aufruf des Mainloops wird gecheckt, ob Daten vorliegen, die aus einer Vorlesung mit gleichem Namen stammen, die vor mehr als (default) 90 Minuten begann.
Ist dies der Fall, werden die gespeicherten Daten geladen und mit neuen erweitert. 
Dies soll eine weitere Analyse vergangener Daten nach einem Crash oder einer Pause ermöglichen.
Das Speichern der Daten bzw. vor allem die Sicherstellung der richtigen Zuordnung von Personen zu ihren Daten unter Positionswechsel, 
Verschwinden und Auftauchen zwischen den Frames kostete hier mehr Zeit als gedacht.


### Mainloop
Das Hauptprogramm startet indem es einige Parameter und Pfade aus einer Konfigurationsdatei ausliest. Diese ist zur hauptsächlich für die Plattformkompatibilität vorhanden.
Für den Endnutzer öffnet sich daraufhin eine graphische Oberfläche, in welcher er Vorlesungsnamen, Dauer (siehe oben), Bildeingabemethode und den Speichermodus (on/off) für Daten wählen kann.
Letzterer ermöglicht die Analyse von Daten über einen längeren Zeitraum als eine Vorlesung. 
In der Hauptschleife werden Bilder in einem definierten Intervall mit der gewählten Methode gesammelt und Gesichter darauf erkannt. Diese werden in Encodings transformiert, um eine
Zuordnung zu Gesichtern im nächsten Bild durch eine Distanz zu ermöglichen.
Die ursprünglichen erkannten Geichter werden durch das CNN klassifiziert und die Ergebnisse werden alle n Iterationen gespeichert. 

### Datenanalyse
Zum jetzigen Zeitpunkt wurde aus Zeitgründen nur ein Anzeige der durchschnittlichen vier Modellausgaben implementiert. Diese soll live währrend der Vorlesung angezeigt werden. 
Ein "Alarm" bei hoher Anzahl an Personen mit kritischen Werten fehlt hier noch. Auch ist noch ist keine Funktionalität zur Analyse der Daten mehrerer Vorlesungen implementiert. 

### GUIs