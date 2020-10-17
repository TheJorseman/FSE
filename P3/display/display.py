import i2c_lcd_driver as LCD
#from time import *
from signal import pause

lcd = LCD.lcd()
#while True:
#lcd.lcd_display_string("Hola mundo.", 1)
#pause()

from bluedot import BlueDot
#from signal import pause

def dpad(pos):
    lcd.lcd_clear()
    if pos.top:
        lcd.lcd_display_string("UP", 1)
    elif pos.bottom:
        lcd.lcd_display_string("DOWN", 1)
    elif pos.left:
        lcd.lcd_display_string("LEFT", 1)
    elif pos.right:
        lcd.lcd_display_string("RIGHT", 1)
    elif pos.middle:
        lcd.lcd_display_string("Miguel A. Lopez S.", 1)
        
bd = BlueDot()
bd.when_pressed = dpad
pause()
