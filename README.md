# greenhouse

Kurzbeschreibung:
Rapsberry Pi Projekt zur Messung von Lichtintensität, Luft- u. Bodentemperatur 
bzw. Luft- u. Bodenfeuchtigkeit. Generierte Messdaten werden in eine MySQL-Datenbank geschrieben
und mit Hilfe eines Google Diagramms visualisiert. Lokale Daten werden auf einem LCD Display ausgegeben.


#SPI, I2C und 1-Wire-Bus Schnittstellen müssen auf dem Raspberry Pi aktiviert sein.

#Folgende Pakete sollten installiert werden, falls nicht vorhanden:

sudo apt install python-dev
sudo apt build-essential
sudo apt python-openssl
sudo pip3 install mysql-connector-python
sudo apt install python3-gpiozero / sudo pip3 install gpiozero 

#Adafruit DHT Luft und Feuchtigkeitssensor:
git clone https://github.com/adafruit/Adafruit_Python_DHT.git
	cd Adafruit_Python_DHT/
	python setup.py install

#1-Write
sudo modprobe w1-gpio
sudo modprobe w1-therm
sudo nano /boot/config.txt
	#Als neue Zeile in config.text hinzufügen: "dtoverlay=w1-gpio,gpioin=4,pullup=on"
sudo nano /etc/modules
	#Als neue Zeile hinzufügen: 
	w1_gpio
	w1_therm
#Sensor abfragen zur Kontrolle: 
	cat /sys/bus/w1/devices/XX-XXXXXXXXXXXX/w1_slave
	
#Für Initialisierung "setupConfig.py" ausführen
#Datenbank erstellen: "setupDatabase.py" ausführen
#Ausführungsprogramm: "runGreenhouse.py"
