#!/usr/bin/python
# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.
import telebot
import json
import re
from gpiozero import LED

LED_Dict = {}

API_TOKEN = '1088193438:AAFffJIzdeGBWtSZhzDCeoYTlkDK2O_Naq4'
bot = telebot.TeleBot(API_TOKEN)

def get_full_name(message):
    """
    Regresa el nombre completo del usuario con el que se esta interactuando.

    Args:
        message (json): Respuesta del bot en formato Json

    Returns:
        str: Nombre del usuario
    """    
    user_info = message.from_user.to_dict()
    return user_info["first_name"] + " " + user_info["last_name"] + "\n"
    
def parse_leds(message,command):
    """
    Verifica con expresiones regulares la validez de los comandos y los valores que se mandan para 
    apagar o encender LEDS.

    Args:
        message (json): Respuesta del usuario hacia el bot.
        command (str): comando a evaluar

    Returns:
        Bool,object: Si el texto coincide con lo esperado, se devuelve un True y la lista de los GPIO, en caso contrario se regresa 
                     False y un mensaje de error.
    """

    texto = message.text
    correct_command = re.search(command+"\s+GPIO\s",texto)
    if not correct_command:
        return False,"\nEl mensaje enviado no coincide con lo que se esperaba "+ command +" GPIO n,n,..."
    list_GPIO = re.findall(r'(\b([0-9]|1[0-9]|2[0-7])\b)(?=\,|\s|$)+', texto) 
    return True, [int(match[0]) for match in list_GPIO ]

def leds_on(list_GPIO):
    """
    Enciende LEDS con una lista de GPIO.
    Si no existen se agregan a un diccionario para su uso posterior
    Args:
        list_GPIO (list): Lista de GPIO
    """    
    for GPIO in list_GPIO:
        if GPIO not in LED_Dict.keys():
            LED_Dict[GPIO] = LED(GPIO)
        LED_Dict[GPIO].on()

def leds_off(list_GPIO):
    """
    Apaga LEDS con una lista de GPIO
    Si no existen se manda un mensaje de warning.
    Args:
        list_GPIO (list): Lista de GPIO
    """ 
    global LED_Dict
    warning_message=""
    for GPIO in list_GPIO:
        if GPIO not in LED_Dict.keys():
            warning_message += "\nAdvertencia:\n El pin GPIO {} no esta declarado como encendido. Se apagara.".format(GPIO)
            LED_Dict[GPIO] = LED(GPIO)
        LED_Dict[GPIO].off()
    return warning_message

@bot.message_handler(commands=['ledon'])
def command_ledon(message):
    return_message = ""
    return_message = "Hola " + get_full_name(message)
    success,parse_response = parse_leds(message,"/ledon")
    if not success:
        return_message += parse_message
        bot.reply_to(message, return_message)
        return
    leds_on(parse_response)
    return_message += "Se han encedido los LEDS ubicados en los GPIO " + ",".join([str(GPIO) for GPIO in parse_response]) + "\n"
    bot.reply_to(message, return_message)


# Handle '/ledon'
@bot.message_handler(commands=['ledoff'])
def command_ledoff(message):
    return_message = ""
    return_message = "Hola " + get_full_name(message)
    success,parse_response = parse_leds(message,"/ledoff")
    if not success:
        return_message += parse_response
        bot.reply_to(message, return_message)
        return
    message_off = leds_off(parse_response)
    return_message += "Se han apagado los LEDS ubicados en los GPIO " + ",".join([str(GPIO) for GPIO in parse_response]) + "\n" + message_off
    bot.reply_to(message, return_message)

# Handle '/start' and '/help'
@bot.message_handler(commands=['help','start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hola, soy TheJorsemanBot y estoy aqui para ayudarte a controlar tu raspberry pi!\
Los comandos son:

/ledon GPIO n,n : Enciende los LEDS conectados a los GPIO n. 

Ejemplos: 
/ledon GPIO 17
/ledon GPIO 13,7,20


/ledoff GPIO n,n : Apaga los LEDS conectados a los GPIO n. 

Ejemplos: 
/ledoff GPIO 17
/ledoff GPIO 13,7,20

Si no hay un LED declarado en el GPIO dado, se lanzara un warning
""")


bot.polling()
