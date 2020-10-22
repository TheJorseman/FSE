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
alarma_time = 10
alarma_time_inter = 0.3
alarma_n = ceil(10/0.3)



def alarma(disp):
    print("Alarma")
    for k in range(alarma_n):
        if alarma_stop:
            break
        disp.on()
        sleep(alarma_time_inter)
        disp.off()
    return

tira_rgb_time = 5
def tiraLED(disp):
    disp.on()
    sleep(tira_rgb_time)
    disp.off()

motor_time = 5
def persiana(disp):
    disp.on()
    sleep(motor_time)
    disp.off()

def Foco(disp,pos):
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
    elif pos.x < 0 and pos.y <0:
        persiana(persiana_LED)
    else:
        tiraLED(tira_LED)

bd = BlueDot()
while True:   
    bd.when_pressed = dpad