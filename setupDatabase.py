import configparser
import mysql.connector

# Initialisierung der Variablen mit Daten aus der Config
config = configparser.ConfigParser()
config.read('greenhouse.ini')

database = config.get('database', 'database')
host = config.get('database', 'host')
user = config.get('database', 'user')
passwd = config.get('database', 'password')

db = mysql.connector.connect(
    host = host,
    user = user,
    passwd = passwd
)

print(db)
curs = db.cursor() # Datenbank Cursor deklarieren

# Datenbank erstellen
curs.execute ("CREATE DATABASE IF NOT EXISTS {}".format(database))
curs.execute ("USE {}".format(database))

# Erstellung der Tabbel, die keinem Sensor entsprechen
curs.execute ("CREATE TABLE IF NOT EXISTS tbl_messzeitpunkt (mzp_id INT UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE, zeitpunkt DATETIME, PRIMARY KEY (mzp_id))")
curs.execute ("CREATE TABLE IF NOT EXISTS tbl_wasserpumpe (wp_id INT UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE, mzp_id INT UNSIGNED, wp_start DATETIME, wp_ende DATETIME, PRIMARY KEY (wp_id), FOREIGN KEY(mzp_id) REFERENCES tbl_messzeitpunkt(mzp_id))")
curs.execute ("CREATE TABLE IF NOT EXISTS tbl_email (email_id INT UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE, mzp_id INT UNSIGNED, PRIMARY KEY (email_id), FOREIGN KEY(mzp_id) REFERENCES tbl_messzeitpunkt(mzp_id))")

# Sensortabellen erstellen
sensorTabelle = ["bodenfeuchte","wasserwarnung","lufttemp","bodentemp","luftfeuchte","lichtint","pottest"]
abkuerzung = ["bf","ww","lt","bt","lf","li","pt"]
sensorTabelleErstellen = "CREATE TABLE IF NOT EXISTS tbl_{0} ({1}_id INT UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE, mzp_id INT UNSIGNED, {1}_wert DECIMAL(6,2), PRIMARY KEY ({1}_id), FOREIGN KEY(mzp_id) REFERENCES tbl_messzeitpunkt(mzp_id))"
for i in range(len(sensorTabelle)):
    curs.execute (sensorTabelleErstellen.format(sensorTabelle[i],abkuerzung[i]))

# Neuen User für die Visualisierung per PHP/JavaScript
newUser = "chartViewer"
newPassword = "12345"
newView = "chartView"

# Views für Visualisierung erstellen (Lufttemp, -feuchte, Bodentemp, -feuchte)
curs.execute ("DROP VIEW chartViewTemp, chartViewFeuchte")
curs.execute ("""CREATE VIEW chartViewFeuchte AS SELECT DATE_FORMAT(tbl_messzeitpunkt.zeitpunkt, '%Y-%m-%d %H:00') AS DatumStunde, ROUND(AVG(tbl_luftfeuchte.lf_wert), 2) AS LuftFeuchte, ROUND(AVG(tbl_bodenfeuchte.bf_wert), 2) AS BodenFeuchte
    FROM tbl_messzeitpunkt
    JOIN tbl_luftfeuchte ON tbl_messzeitpunkt.mzp_id=tbl_luftfeuchte.mzp_id
    JOIN tbl_bodenfeuchte ON tbl_messzeitpunkt.mzp_id=tbl_bodenfeuchte.mzp_id
    GROUP BY HOUR(tbl_messzeitpunkt.zeitpunkt), DATE(tbl_messzeitpunkt.zeitpunkt)
    ORDER BY tbl_messzeitpunkt.zeitpunkt""")

curs.execute ("""CREATE VIEW chartViewTemp AS SELECT DATE_FORMAT(tbl_messzeitpunkt.zeitpunkt, '%Y-%m-%d %H:00') AS DatumStunde, ROUND(AVG(tbl_lufttemp.lt_wert), 2) AS LuftTemp, ROUND(AVG(tbl_bodentemp.bt_wert), 2) AS BodenTemp
    FROM tbl_messzeitpunkt
    JOIN tbl_lufttemp ON tbl_messzeitpunkt.mzp_id=tbl_lufttemp.mzp_id
    JOIN tbl_bodentemp ON tbl_messzeitpunkt.mzp_id=tbl_bodentemp.mzp_id
    GROUP BY HOUR(tbl_messzeitpunkt.zeitpunkt), DATE(tbl_messzeitpunkt.zeitpunkt)
    ORDER BY tbl_messzeitpunkt.zeitpunkt""")

curs.execute ("GRANT SELECT ON db_greenhouse.chartViewTemp TO '{}' IDENTIFIED BY 'password'".format(newUser))
curs.execute ("GRANT SELECT ON db_greenhouse.chartViewFeuchte TO '{}' IDENTIFIED BY 'password'".format(newUser))

curs.close()
db.close()