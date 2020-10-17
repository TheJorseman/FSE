from bluedot import BlueDot
from gpiozero import PWMLED

red = PWMLED(13)
yellow = PWMLED(19)
green = PWMLED(26)

led = yellow

def set_brightness(pos):
    brightness = (pos.y + 1) / 2
    led.value = brightness

def dpad(pos):
    if pos.top:
        set_brightness(pos)
    elif pos.bottom:
        set_brightness(pos)
    elif pos.left:
        led = red
        led.on()
    elif pos.right:
        led = green
        led.on()
    elif pos.middle:
        led = yellow
        led.on()

bd = BlueDot()
while True:   
    bd.when_pressed = dpad
