from gpiozero import MotionSensor
import i2c_lcd_driver as LCD
"""
La lógica es la siguiente, en un restaurante se colocan dos sensores, uno a la entrada del establecimiento, apuntando hacia la calle
y la otro sensor apuntando a la misma entrada pero dentro del establecimiento. 
Asi cuando alguien está en la puerta pero dentro del establecimiento se muestra el mensaje "Hasta luego :)"
Pero si esta fuera y quiere entrar entonces se activa el sensor de la entrada y muestra el mensaje de bienvenida.
"""
lcd = LCD.lcd()
entrada = MotionSensor(4)
salida = MotionSensor(5)
while 1:
    if entrada.motion_detected:
        lcd.lcd_display_string("Bienvenido", 1)
    if salida.motion_detected:
        lcd.lcd_display_string("Hasta luego :)", 1)
