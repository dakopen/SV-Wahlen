# SV-Wahlen

Für die SV-Wahl der FVS entwickelt, nimmt eine Excel Tabelle mit den Spalten "Name" (voller Name) und "Ausweisnummer" als Input.

## Installation
1. `pip install -r requirements.txt`
2. Schülerliste (Formatierung siehe oben, sonst mich nochmal fragen, kann das anpassen) in den `speicher` kopieren und Dateinamen zu `students.xlsx` ändern.

## Verwendung
1. Programm starten
2. Im besten Fall Schülerausweis an Scannerhalten, der an den Laptop angeschlossen wird. Schüler darf wählen, wenn grüner Bestätigungstext kommt.
3. Wenn kein Schülerausweis vorhanden ist, erste Buchstaben des Vor- oder Nachnamen schreiben, dann Zeilennummer auswählen.
4. "break" zum Beenden verwenden
5. "undo" schreiben und dann wie oben beschrieben einen Schüler auswählen, um ihn wieder wählen zu lassen.
6. Alle 10 Schüler wird eine Zwischenspeicherdatei erstellt. Sollte es zu Problemen kommen, einfach diese Datei zu `students.csv` umbenennen.

Bei Fragen am Wahltag, nur an Herrn Christ wenden, nicht an mich!
