from CasaInteligente.services.telegram_api import Telegram
from CasaInteligente.components import foco,persiana,alarma,tira_led


alarma_obj = alarma.Alarma(0,"alarma")
persiana_obj = persiana.Persiana(1,"persiana")
foco_obj = foco.Foco(2,"foco")
tira_led_obj = tira_led.TiraLED(3,"tira_led") 
dispositivos = [alarma_obj, persiana_obj, foco_obj, tira_led_obj]

bot_encendido = Telegram("Encendido","1088193438:AAFffJIzdeGBWtSZhzDCeoYTlkDK2O_Naq4")
bot_encendido.set_elements(dispositivos)
bot_encendido.run()

bot_enc = bot_encendido.bot
@bot_enc.message_handler(commands=['on'])
def command_ledon(message):
    bot_encendido.command_on(message)
