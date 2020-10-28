from CasaInteligente.services.telegram_api import Telegram
from CasaInteligente.components import foco,persiana,alarma,tira_led
import telebot

alarma_obj = alarma.Alarma(0,"alarma")
persiana_obj = persiana.Persiana(1,"persiana")
foco_obj = foco.Foco(2,"foco")
tira_led_obj = tira_led.TiraLED(3,"tira_led") 
dispositivos = [alarma_obj, persiana_obj, foco_obj, tira_led_obj]

bot_enc = telebot.TeleBot("1088193438:AAFffJIzdeGBWtSZhzDCeoYTlkDK2O_Naq4")

bot_encendido = Telegram("Encendido", bot_enc)
bot_encendido.set_elements(dispositivos)
bot_encendido.add_action_message("\on","\nEnciende el/los dispositivos seleccionados","\n\on alarma,foco")
bot_encendido.add_action_message("\off","\nApaga el/los dispositivos seleccionados","\n\off alarma,foco")
bot_encendido.add_action_message("\setvalue","\nEstablece el valor PWM al seleccionado","\n\setvalue alarma 0.5")
bot_encendido.add_action_message("\show","\nMuestra los dispositivos que se encuentran activados","\show")

@bot_enc.message_handler(commands=['on'])
def command_ledon(message):
    response = bot_encendido.command_on(message)
    bot_enc.reply_to(message, response)
    
@bot_enc.message_handler(commands=['off'])
def command_ledoff(message):
    response = bot_encendido.command_off(message)
    bot_enc.reply_to(message, response)

@bot_enc.message_handler(commands=['help','start'])
def send_welcome(message):
    response = bot_encendido.command_start_help()
    bot_enc.reply_to(message, response)

@bot_enc.message_handler(commands=['show'])
def command_show(message):
    response = bot_encendido.command_show(message)
    bot_enc.reply_to(message, response)

@bot_enc.message_handler(commands=['setvalue'])
def command_show(message):
    response = bot_encendido.command_set_value(message)
    bot_enc.reply_to(message, response)


bot_enc.polling()
