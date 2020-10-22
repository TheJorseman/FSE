from bluedot import BlueDot
from gpiozero import PWMLED
from time import sleep
from threading import Thread,Event
from math import ceil

alarma_LED =  PWMLED(6)
Foco_LED = PWMLED(13)
tira_LED = PWMLED(19)
persiana_LED = PWMLED(26)

alarma_stop = False 
alarma_time = 5
alarma_time_inter = 0.5
alarma_n = ceil(alarma_time/(2 * alarma_time_inter))



def alarma(disp):
    print("Alarma")
    for k in range(alarma_n):
        if alarma_stop:
            break
        disp.on()
        sleep(alarma_time_inter)
        disp.off()
        sleep(alarma_time_inter)
    return

tira_rgb_time = 5
def tiraLED(disp):
    print("TiraLed")
    disp.on()
    sleep(tira_rgb_time)
    disp.off()

motor_time = 5
def persiana(disp):
    print("Persiana")
    disp.on()
    sleep(motor_time)
    disp.off()

def Foco(disp,pos):
    print("Persiana")
    disp.value = pos.y 

def dpad(pos):
    alarma_LED.off()
    Foco_LED.off()
    tira_LED.off()
    persiana_LED.off()
    
    if pos.x < 0 and pos.y>0 :
        alarma(alarma_LED)
    elif pos.x >= 0 and pos.y>0:
        Foco(Foco_LED,pos)
    elif pos.x < 0 and pos.y <=0:
        persiana(persiana_LED)
    elif pos.x >= 0 and pos.y<0:
        tiraLED(tira_LED)

bd = BlueDot()
while True:   
    bd.when_pressed = dpad
