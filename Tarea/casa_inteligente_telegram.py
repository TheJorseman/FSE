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
bot_encendido.add_action_message("\n \on disp,disp Enciende el/los dispositivos seleccionados")
bot_encendido.add_action_message("\n \off disp,disp Apaga el/los dispositivos seleccionados")
bot_encendido.add_action_message("\n \show Muestra los dispositivos que se encuentran activados")

@bot_enc.message_handler(commands=['on'])
def command_ledon(message):
    response = bot_encendido.command_on(message)
    bot_enc.reply_to(message, response)
    
@bot_enc.message_handler(commands=['off'])
def command_ledoff(self,message):
    response = bot_encendido.command_off(message)
    bot_enc.reply_to(message, response)

@bot_enc.message_handler(commands=['help','start'])
def send_welcome(self,message):
    response = bot_encendido.command_start_help()
    bot_enc.reply_to(message, response)

@bot_enc.message_handler(commands=['show'])
def command_show(self,message):
    response = bot_encendido.command_show(message)
    bot_enc.reply_to(message, response)

bot_enc.polling()
