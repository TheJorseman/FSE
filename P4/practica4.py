#!/usr/bin/python
# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.
import telebot

API_TOKEN = '1088193438:AAFffJIzdeGBWtSZhzDCeoYTlkDK2O_Naq4'
bot = telebot.TeleBot(API_TOKEN)



# Handle '/ledon'
@bot.message_handler(commands=['ledon'])
def command_ledon(message):
    bot.reply_to(message, "xD")

# Handle '/start' and '/help'
@bot.message_handler(commands=['help','start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hola, soy TheJorsemanBot y estoy aqui para ayudarte a controlar tu raspberry pi!\
""")


bot.polling()