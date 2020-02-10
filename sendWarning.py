#!/usr/bin/python
#-*- enconding: iso-8859-1 -*-
import smtplib
import ssl
import datetime
from time import *
import configparser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Initialisierung der Variablen mit Daten aus der Config
config = configparser.ConfigParser()
config.read('greenhouse.ini')
port = 465
password = config.get('email', 'password')
sender_email = config.get('email', 'sender_mail')
receiver_email = config.get('email', 'receiver_mail')

# Übergebene Strings wird in HTML formatiert, kritische Werte rot und fett
def plainToHtml(plainStringList):
    htmlStringList = []
    for i in range(len(plainStringList)):
        if plainStringList[i].count('*') > 0:
            htmlStringList.append('<b><p style=\"color:Tomato;\">{}</p></b>'.format(plainStringList[i]))
        else:
            htmlStringList.append(plainStringList[i])
    return htmlStringList

# Versenden der E-Mail
def sendWarning(werteString, messzeitpunkt):
    
    # Message container
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Kritische(r) Wert(e) erreicht!"
    msg['From'] = sender_email
    msg['To'] = receiver_email
    
    messzeitpunkt = messzeitpunkt.strftime("%Y-%m-%d %H:%M:%S")
    htmlStringList = plainToHtml(werteString)

    # Plaintextversion der E-Mail
    text = """Folgende Werte wurden gemessen:
    
    Messzeitpunkt       Lufttemp (C) Luftfeuchte (%) Bodentemp (C) Bodenfeuchte (%) Lichtint Wasserstand
    
    {} {:12} {:15} {:13} {:16} {:8} {:11}
    
    * unterhalb des Schwellenwertes, ** oberhalb des Schwellenwertes""".format(messzeitpunkt, *werteString) # *werteString geht jedes Element in der Liste durch    

    # HTML-Formatierung, Werte in Tabellenform
    html = """\
    <html>
        <head>
        <style>
        table, th, td {{
            border: 1px solid black;
            border-collapse: collapse;
        }}
        th, td {{
            padding: 3px;
        }}
        th {{
            text-align: left;
        }}
        </style>
        </head>
        <body>
            <p>Folgende Werte wurden gemessen:<br>
            <table style="width:100%">
                 <tr>
                    <th>Messzeitpunkt</th>
                    <th>Lufttemp. (°C)</th>
                    <th>Luftfeuchte (%)</th>
                    <th>Bodentemp. (°C)</th>
                    <th>Bodenfeuchte (%)</th>
                    <th>Lichtint.</th>
                    <th>Wasserstand</th>
                </tr>
                <tr>
                    <td>{}</td>
                    <td>{}</td>
                    <td>{}</td>
                    <td>{}</td>
                    <td>{}</td>
                    <td>{}</td>
                    <td>{}</td>
                </tr>
            </table>
            * unterhalb des Schwellenwertes, ** oberhalb des Schwellenwertes
            </p>
        </body>
    </html>""".format(messzeitpunkt, *htmlStringList)

    # Zusammenfügen der E-Mail
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html', 'iso-8859-1')
    
    msg.attach(part1)
    msg.attach(part2)
    
    # E-Mail versenden
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(sender_email,password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print('E-Mail wurde gesendet.')
    except:
        print('FEHLER: E-Mail Probleme.')
