from smbus2 import SMBus
import RPi.GPIO as GPIO
from time import sleep #nødvendige bibliotek

from DFRobot_RGBLCD1602 import DFRobot_RGBLCD1602

høyre = 17 #pins for knappene
venstre = 27

GPIO.setmode(GPIO.BCM) #basically for å gjøre at pinsa vi definerte over passer til pien

GPIO.setup(høyre, GPIO.IN, pull_up_down=GPIO.PUD_UP) #når knappen er trykket ned er den = 0 ellers er den lik 1 
GPIO.setup(venstre, GPIO.IN, pull_up_down=GPIO.PUD_UP) #bruker internal pull up til dette

lcd = DFRobot_RGBLCD1602(0x6B, 16, 2)

lcd.set_RGB(255, 255, 255)  # White

sleep(0.2)

#tømmer skjermen 
lcd.clear()
lcd.set_cursor(0, 0) 
sleep(0.1)

spørsmål = ["Test 1", "Test 2", "Test 3"] #ting som vises på skjermen, obviously

indeks = 0 #Første element i lista med spørsmål

def clear():
    #først tømmer jeg skjermen, så flytter jeg markøren slikt at den kan skrive fra starten
    lcd.clear()
    sleep(0.05)
    lcd.set_cursor(0, 0) 
    sleep(0.05)

    

def skriv(tekst):
    #For løkka skriver de første 16 tegnene (siden det er så mye plass)
    #før den hopper ned en linje
    #parameteren er en indeks i lista over spørsmål
    lcd.set_cursor(0, 0) 
    lcd.print_out(tekst[:16])

    lcd.set_cursor(0, 1) 
    lcd.print_out(tekst[16:32])


def vis_beskjed(spørsmål, indeks):
    clear()
    skriv(spørsmål[indeks]) #bruker funksjonene over 

vis_beskjed(spørsmål, indeks) #viser første spærsmål på skjermen 


try: 
    while True: #Åpenbart at den må kjøre hele tida (det er fordi den må hele tida sjekke om en knapp blir trykket)
        if GPIO.input(venstre) == 0: #Hvis trykket Så blir indeks +1 (altså neste spørsmål)
            indeks = (indeks + 1)  % len(spørsmål) #Veldig fornøyd med denne logikken 
            vis_beskjed(spørsmål, indeks) #det % len(spørsmål) gjør er at den sørger for at hvis 
            sleep(0.3) #trykker når man er på siste spørsmpl så kommer man tilbake til starten eks: du er ved indeks 2 i lista (siste spørsmål) så trykker, da blir det blir 3%3 = 0, og vipps så er du tilbake til færste spørsmål
        if GPIO.input(høyre) == 0:
            indeks = (indeks - 1) % len(spørsmål)
            vis_beskjed(spørsmål, indeks)
            sleep(0.3)
except KeyboardInterrupt:
    GPIO.cleanup() #sånn at man kan avbryte med ctrl c
    
  
