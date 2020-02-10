#!/usr/bin/python
#-*- encoding: iso-8859-1 -*-
import datetime
from time import sleep
from getValues import getValues
from sendWarning import sendWarning
from dbValueUpload import *
import localOutput
    

sensor = ""
schwellenwertListMin = [0.0, 35.0, 5.0, 20.0, -1.0, -1.0] # LT LF BT BF LI WS    # erlaubte Minmalwerte bevor Warnungen ausgegeben werden
schwellenwertListMax = [35.0, 65.0, 30.0, 120.0, 2.0, 0.2] # LT LF BT BF LI WS   # erlaubte Maximalwerte bevor Warnungen ausgegeben werden
lastWarning = datetime.datetime(1970, 1, 1, 12, 0, 0) # Initialisierung, erste Warnung nach Start soll versendet werden
errCount = 5


while True:
    werteList = getValues() # Werte auslesen
    localOutput.localLCD(werteList) # Lufttemp, -feuchte, Bodentemp, -feuchte
    localOutput.localLED(werteList[5]) # Wasserstand
    

    aktuelleZeit = datetime.datetime.now()
    
    try:
        if getLastMesszeitpunkt():
            lastUpload = getLastMesszeitpunkt()[0] # Letztes Schreiben in die DB
        else:   
            lastUpload = [datetime.datetime(1970, 1, 1, 12, 0, 0)] # Wenn noch nichts in die DB geschrieben wurde
            print('Kein Datensatz')
            
        if getLastMesszeitpunkt() and aktuelleZeit > lastUpload[0] + datetime.timedelta(seconds = 30): # Zeit zwischen den Uploads in die DB
            mzpId = uploadMesszeitpunkt(aktuelleZeit) # Upload des Messzeitpunktes, 
            for i in range(len(werteList)): # Durchlaufen des Messwerte-Arrays, Zuweisung der Sensorkürzel
                if i == 0:
                    sensor = 'lt'
                elif i == 1:
                    sensor = 'lf'
                elif i == 2:
                    sensor = 'bt'
                elif i == 3:
                    sensor = 'bf'
                elif i == 4:
                    sensor = 'li'
                elif i == 5:
                    sensor = 'ww'

                uploadMesswert(sensor, werteList[i], mzpId) # Schreiben der jeweiligen Werte in die DB
            print('Datenbank wurde aktualisiert.')
        else:
            print('Datenbank wurde nicht aktualisiert.')
    except:
        print('FEHLER: Problem mit der Datenbank aufgetreten.')

       
    # sendWarning Email
    if aktuelleZeit > lastWarning + datetime.timedelta(seconds = 30): # Zeit zwischen dem Senden der Warnemails
        werteStringList = []
        istKritisch = False
        for i in range(len(schwellenwertListMin)):
            if werteList[i] > schwellenwertListMax[i]: # Über Maximalwert
                werteStringList.append('{0:.2f}**'.format(werteList[i])) # Anpassung der Formatierung kritischer Werte
                istKritisch = True
            elif werteList[i] < schwellenwertListMin[i]: # Unter Minimalwert
                werteStringList.append('{0:.2f}*'.format(werteList[i]))
                istKritisch = True
            else: # Innerhalb des Sollbereiches
                werteStringList.append('{0:.2f}'.format(werteList[i]))

        # Senden einer Warn-Email bei mindestens einem kritischen Wertes
        if istKritisch == True:
            print('Email soll gesendet werden.')
            sendWarning(werteStringList, aktuelleZeit)
            lastWarning = aktuelleZeit
        else:
            print('Keine Email gesendet.')
    sleep(2)
    
    
    
    
    
    
    