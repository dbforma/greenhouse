import configparser
import getpass

config = configparser.ConfigParser()
config.read('greenhouse.ini')

# Funktionen für die einzelnen Einträge
def dbHost():
    config['database']['host'] = input('    Database Host: ')

def dbUser():
    config['database']['user'] = input('    Benutzer: ')

def dbPassword():
    config['database']['password'] = getpass.getpass('    Passwort: ')

def dbDatabase():
    config['database']['database'] = input('    Datenbankname: ')

def emailSender():
    config['email']['sender_mail'] = input('    Absender: ')

def emailReceiver():
    config['email']['receiver_mail'] = input('    Emfänger: ')

def emailPassword():
    config['email']['password'] = getpass.getpass('    Passwort: ')

# Funktionen pro Kategorie
def setupDatabse():
    print('Datenbank:')
    config['database'] = {}
    dbHost()
    dbUser()
    dbPassword()
    dbDatabase()

def setupEmail():
    print('E-Mails:')
    config['email'] = {}
    emailSender()
    emailReceiver()
    emailPassword()

# Menü
while True:
    print('1: Alles einrichten')
    print('2: Datenbank')
    print('3: E-Mail')
    print('4: Beenden')
    inp = input('Zahl eingeben: ')

    if int(inp) == 1:
        setupDatabse()
        setupEmail()
        break
    elif int(inp) == 2:
        setupDatabse()
        break
    elif int(inp) == 3:
        setupEmail()
        break
    elif int(inp) == 4:
        raise SystemExit

# Config Datei schreiben
with open('greenhouse.ini', 'w') as configfile:
    config.write(configfile)