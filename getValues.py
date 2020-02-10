try:
    from gpiozero import MCP3008 # Analog-to-Digital Converter
    
    #ADC
    pottest = MCP3008(channel=0) # Analog-Potentiometer-Test
    wasserwarnung = MCP3008(channel=1) # Wasserstand
    bodenfeuchte = MCP3008(channel=2) # Bodenfeuchte
    lichtint = MCP3008(channel=3) # Lichtintensitaet
except:
    print('FEHLER: gpiozero.MPC3008 konnte nicht importiert werden.') # Fehlerausgabe
    
try:
    import Adafruit_DHT # Luftfeuchtigkeit / Luft-Temperatur
    
    # Digital Sensoren (Lufttemp, Luftfeuchte)
    lufttempfeucht = Adafruit_DHT.DHT22 # Sensortyp
    pin = 13 # GPIO-Pin
except:
    print('FEHLER: Adafruit_DHT konnte nicht importiert werden.')


# get-Functions
def getPottest():
    try:
        return pottest.value
    except:
        print('FEHLER: Wert von Analogsensor 0 (Poti) kann nicht gelesen werden.')
        return -100.0 # Default Value
        
def getWasserwarnung():
    try:
        return wasserwarnung.value
    except:
        print('FEHLER: Wert von Analogsensor 1 (Wasser) kann nicht gelesen werden.')
        return -100.0
        
def getBodenfeuchte():
    try:
        bodenfeuchteProz = (1 - bodenfeuchte.value) * 100 
        return bodenfeuchteProz
    except:
        print('FEHLER: Wert von Analogsensor 2 (Bodenfeuchte) kann nicht gelesen werden.')
        return -100.0

def getLichtint():
    try:
        return lichtint.value
    except:
        print('FEHLER: Wert von Analogsensor 3 (Pohtowiderstand) kann nicht gelesen werden.')
        return -100.0
        
def getLuftfeuchte():
    try:
        luftfeuchte, lufttemp = Adafruit_DHT.read_retry(lufttempfeucht, pin)
        return luftfeuchte
    except:
        print('FEHLER: Wert von Digitalsensor (Luftfeuchte) kann nicht gelesen werden.')
        return -100.0       

def getLufttemp():
    try:
        luftfeuchte, lufttemp = Adafruit_DHT.read_retry(lufttempfeucht, pin)
        return lufttemp
    except:
        print('FEHLER: Wert von Digitalsensor (Lufttemp) kann nicht gelesen werden.')
        return -100.0

def getLuft():
    luftfeuchte, lufttemp = Adafruit_DHT.read_retry(lufttempfeucht, pin, 5)
    
    # Vermeidung von NULL Rückgabewerten
    if (type(luftfeuchte) == float and type(lufttemp) == float):
        return lufttemp, luftfeuchte
    else:
        print('FEHLER: Wert von Digitalsensor (DHT22) kann nicht gelesen werden.')
        return -100.0, -100.0
        
        
# 1-Wire Slave-Liste lesen
try:
    file = open('/sys/devices/w1_bus_master1/w1_master_slaves')
    w1_slaves = file.readlines()
    file.close()
except:
    print('FEHLER: Wert von Digitalsensor (Bodenfeuchte) kann nicht gelesen werden.')


def getBodentemp():
    try:
    # Fuer jeden 1-Wire Slave aktuelle Temperatur ausgeben
        for line in w1_slaves:
      # 1-wire Slave extrahieren
            w1_slave = line.split("\n")[0]
      # 1-wire Slave Datei lesen
            file = open('/sys/bus/w1/devices/' + str(w1_slave) + '/w1_slave')
            filecontent = file.read()
            file.close()

      # Temperaturwerte auslesen und konvertieren
            stringvalue = filecontent.split("\n")[1].split(" ")[9]
            temperature = float(stringvalue[2:]) / 1000

            return temperature
    except:
        return -100.0
    print('FEHLER: Wert von Digitalsensor (Luftfeuchte) kann nicht gelesen werden.')

def getValues():
    lufttemp, luftfeuchte = getLuft()
    werte = [lufttemp, luftfeuchte, getBodentemp(), getBodenfeuchte(), getLichtint(), getWasserwarnung()]
    return werte
    
    

