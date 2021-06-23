## Meilensteinbericht 1 (zum 8.6.21)

Zum dritten Meilenstein wurde das Modell trainiert, hier gab es allerdings mehrere Probleme, die den Verlauf erheblich verzögerten. 
Außerdem wurde mit der Arbeit an Funktionalitäten für die Persistenz der ermittelten Daten gearbeitet.

### Model
Das Modell wurde eine Zeit lang auf den Rechner der CV-Gruppe trainiert. Hierbei ist zu erwähnen, dass die GPUs aufgrund technischer Probleme nicht genutzt werden konnten.
Trotz sich bessernder Metriken waren die Ergebnisse bei anschließenden Tests 
danach sehr ernüchternd. Grund war ein Fehler in der Architektur des Modell, genauer bei der Dimensionalität der Outputs.
Das Modell wurde neu designed: Es verfügt nun über vier Äste, die auf einen CNN-Teil folgen, welcher eine geteilte grundlegende Merkmalsrepräsentation erstellt.
Die Äste lösen daraufhin je ein Klassifikationproblem (*Boredom*, *Engagement*, *Frustration*, *Confusion*).
Das Training des Modells musste leider früh aufgrund von mangelnden Kapazitäten auf den Rechnern beendet werden. 
Das Training wurde danach auf *Google Colab* verschoben. Hierzu mussten einige kleineere infrastrukturelle Probleme bezüglich des Datenuploads behoben werden.
Danach wurde dort ein Trainingsdurchlaf beendet. Bei näherer Analyse fielen allerdings zwei kleinere Probleme mit dem Modell auf:
- Zwei Zeilen des zugrunde liegenden Dataframes waren vertauscht, was bei der Analyse der Performance für Verwirrung sorgte
- Die Verteilung der einzelnen Klassen innerhalb der Kategorien wurde nicht berücksichtigt
Gegeben dieser Probleme und mangelnder Performance wird morgen *(Stand: 22.6.)* ein neuer Trainingslauf gestartet.

### Persistenz / IO
Es wurden Methoden implementiert, die es ermöglichen gesammelte Daten (Face-Features und Modelloutputs) gruppiert nach Veranstaltungen und Datum zu speichern und auszulesen, 
um diese für die statistische Datenanalyse verfügbar zu machen. 