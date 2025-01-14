# radar-shield

# Intelligent Radar Shield

Dieses Repository enthält den Quellcode und die Dokumentation für das Intelligent Radar Shield, das mithilfe eines Radarsensors die Geschwindigkeit vorbeilaufender Personen misst und bei Überschreiten eines definierten Schwellenwerts automatisch eine "Blitzfunktion" auslöst. 

## Funktionen:

* **Geschwindigkeitsmessung:** Verwendet einen hochpräzisen Radarsensor zur Erfassung der Geschwindigkeit von vorbeilaufenden Personen.
* **Schwellenwertüberwachung:** Vergleicht die gemessene Geschwindigkeit mit einem konfigurierbaren Grenzwert.
* **Blitzfunktion:** Löst eine Kamera aus, um ein Foto der Person zu machen, die den Schwellenwert überschreitet.
* **Strafzettelgenerierung:** Erstellt automatisch einen Bericht über den Verstoß.


Aufbau

Das Projekt besteht aus folgenden Hauptkomponenten:

##  Hardware:
1. Radarsensor (OPS 243) 
2. Kamera (Logitech C920) 
3. Matrix-Led Display 
4. Fotodrucker (Canon SELPHY CP1500)
5. Raspberry Pi 3+


## Installation
Python Version 3.9+

### Schritte zur Einrichtung
Git Repository download:

    $ git clone https://github.com/dein-benutzername/intelligent-radar-shield.git

Libraries installieren:

    $ pip install -r requirements.txt

Starting the Script (sudo is required because the LED Matrix Driver needs elevated permissions):
    
    # ./IRS.py
