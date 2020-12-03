#Se importa el driver i2c previamente mencionado
import i2c_lcd_driver as LCD
from signal import pause
lcd = LCD.lcd()
#Se importa bluedot
from bluedot import BlueDot

#Utilizando la posicion del bluedot elegiremos el mensaje
def dpad(pos):
    lcd.lcd_clear()
    if pos.left:
        lcd.lcd_display_string("Pedido Recibido", 1)
    elif pos.middle:
        lcd.lcd_display_string("Pedido en progreso", 1)
    elif pos.right:
        lcd.lcd_display_string("Pedido Listo", 1)

bd = BlueDot()
#Cuando es presionado utilizará la funcion dpad
bd.when_pressed = dpad
pause()
