import datetime
import configparser

# Initialisierung der Variablen mit Daten aus der Config
config = configparser.ConfigParser()
config.read('greenhouse.ini')

try:
    import mysql.connector
    db = mysql.connector.connect(
        host = config.get('database', 'host'),
        user = config.get('database', 'user'),
        passwd = config.get('database', 'password'),
        database = config.get('database', 'database')
        )
    curs = db.cursor()
except:
    print('FEHLER: mysql.connector konnte nicht importiert werden.')

# Messzeipunkt (ID, Zeit), gibt die ID des neusten Tabelleneintrages zurück
def uploadMesszeitpunkt(aktuelleZeit):
    sql = "INSERT INTO tbl_messzeitpunkt (zeitpunkt) VALUES ('%s')"
    curs.execute(sql % aktuelleZeit)
    db.commit()
    curs.close()
    db.close()
    return curs.lastrowid


def uploadMesswert(sensor, messwert, mzp):
    # Zuweisung der übergebenen Sensorkürzel -> Sensorname für die Datenbank entsprechend Tabellennamen
    if sensor == "bf":
        tabelle = "bodenfeuchte"
    elif sensor == "ww":
        tabelle = "wasserwarnung"
    elif sensor == "lt":
        tabelle = "lufttemp"
    elif sensor == "bt":
        tabelle = "bodentemp"
    elif sensor == "lf":
        tabelle = "luftfeuchte"
    elif sensor == "li":
        tabelle = "lichtint"
    elif sensor == "pt":
        tabelle = "pottest"
    
    # Einfügen der Werte und Namen in das MySQL Statement
    sql = "INSERT INTO tbl_{0} (mzp_id, {1}_wert) VALUES ({2}, {3:.2f})"
    curs.execute(sql.format(tabelle, sensor, mzp, messwert))
    db.commit()
    curs.close()
    db.close()

# Gibt den letzten Uploadzeitpunkt zurück
def getLastMesszeitpunkt():
    sql = "SELECT zeitpunkt FROM tbl_messzeitpunkt ORDER BY mzp_id DESC LIMIT 1"
    curs.execute(sql)
    curs.close()
    db.close()
    return curs.fetchall() # fetchall = Hole alles, was da ist
