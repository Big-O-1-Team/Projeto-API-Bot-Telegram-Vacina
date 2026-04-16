import os
import telebot
from telebot import types
from telebot.types import KeyboardButton
import dotenv

dotenv.load_dotenv()
bot_token = os.getenv('BOT_TOKEN')

bot = telebot.TeleBot(bot_token)

@bot.message_handler(commands=['start'])
def receber(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    unidades_proximas = types.InlineKeyboardButton(
        'Buscar postos de vacinação', callback_data='answer_unidades_proximas')
    markup.add(unidades_proximas)
    bot.send_message(message.chat.id, 'Olá! Como deseja prosseguir?', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def answer(callback):
    if callback.data == "answer_unidades_proximas":
        pedir_localizacao(callback.message)
        bot.answer_callback_query(callback.id)

def pedir_localizacao(message):
    markup = types.ReplyKeyboardMarkup(row_width=1)
    botao_loc = KeyboardButton('📍 Compartilhar localização', request_location=True)
    markup.add(botao_loc)
    bot.send_message(message.chat.id, "Compartilhe sua localização", reply_markup=markup)

@bot.message_handler(content_types=['location'])
def receber_localizacao(message):
    latitude = message.location.latitude
    longitude = message.location.longitude
    bot.send_message(message.chat.id, "Localização recebida!")

if __name__ == "__main__":
    bot.polling()