from time import *

try:
    import lcddriver
except:
    print('FEHLER: lcddriver konnte nicht importiert werden. (kein Raspi?)')

try:
    from gpiozero import RGBLED
    led = RGBLED(red=26, green=19, blue=0) # GPIO-Pins
    lcd = lcddriver.lcd()
except:
    print('FEHLER: gpiozero.RGBLED konnte nicht importiert werden. (kein Raspi?)')


lcdAusgabe1 = '{:18}'.format('LT: {0:.2f}C') # LCD Lufttemperatur mit zwei Nachkommastellen
lcdAusgabe2 = '{:18}'.format('LF: {0:.2f}%') # LCD Luftfeuchte mit zwei Nachkommastellen
lcdAusgabe3 = '{:18}'.format('BT: {0:.2f}C') # LCD Bodentemperatur mit zwei Nachkommastellen
lcdAusgabe4 = '{:18}'.format('BF: {0:.2f}%') # LCD Bodenfeuchte mit zwei Nachkommastellen

lcdCount = 1
lcdPage = 1

ledErrCount = 5
lcdErrCount = 3


def localLED(ledWert):
    global ledErrCount
    try:
        if ledWert >= 0.45:
            led.color = (1,0,0)                   
        elif ledWert >= 0.3:
            led.color = (1,1,0)
        else:
            led.color = (0,1,0)
    except:
        if ledErrCount == 5:
            print('FEHLER: LED nicht funktionfähig/vorhanden')
            ledErrCount = 0
        else:
            ledErrCount += 1

        
def localLCD(array):
    global lcdErrCount
    try:
        global lcdCount
        global lcdPage
        if lcdCount == 1:
            lcdPage = 1
        elif lcdCount == 3:
            lcdPage = 2
            
        if lcdPage == 1:
            lcd.lcd_display_string(lcdAusgabe1.format(array[0]),1)
            lcd.lcd_display_string(lcdAusgabe2.format(array[1]),2)
            lcdCount += 1
        elif lcdPage == 2:
            lcd.lcd_display_string(lcdAusgabe3.format(array[2]),1)
            lcd.lcd_display_string(lcdAusgabe4.format(array[3]),2)
            lcdCount -= 1
    except:
        if lcdErrCount == 3:
            print('FEHLER: LCD nicht funktionfähig/vorhanden')
            lcdErrCount = 1
        else:
            lcdErrCount += 1