import os
import re
import telebot
import dotenv
from telebot import types
from datetime import datetime, date
from scripts.scrappingselenium import AcessarInformacoes, scrappingVacinaInfoIndividual
import scripts.createCSV as createCSV
from scripts.scrapping_cnes import buscar_ubs_por_municipio, formatar_mensagem_ubs

dotenv.load_dotenv()
bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))
MSG_PEDIR_IBGE = (
    "*Busca de UBS por Município*\n\n"
    "Por favor, informe o *código IBGE* do seu município (7 dígitos).\n\n"
    "*Exemplos:*\n"
    "• São José dos Campos: `3549904`\n"
    "• São Paulo: `3550308`"
)

def iniciar_fluxo_ubs(chat_id):
    msg = bot.send_message(chat_id, MSG_PEDIR_IBGE, parse_mode='Markdown')
    bot.register_next_step_handler(msg, processar_busca_ubs)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton('Calendário', callback_data='cal')
    btn2 = types.InlineKeyboardButton('Buscar Postos', callback_data='ubs')
    markup.add(btn1, btn2)
    
    bot.send_message(message.chat.id, "Olá! Sou o *Oswaldo*. Como posso ajudar?", 
                     reply_markup=markup, parse_mode='Markdown')

@bot.message_handler(commands=['horarios'])
def cmd_horarios(message):
    iniciar_fluxo_ubs(message.chat.id)

@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    if call.data == "ubs":
        iniciar_fluxo_ubs(call.message.chat.id)
    elif call.data == "cal":
        pass
    bot.answer_callback_query(call.id)


def processar_busca_ubs(message):
    codigo = message.text.strip()
    
    if not re.fullmatch(r'\d{7}', codigo):
        return bot.send_message(message.chat.id, "Erro: Use 7 números. Tente /horarios novamente.")

    bot.send_message(message.chat.id, "Consultando base do CNES...")
    
    try:
        lista_ubs = buscar_ubs_por_municipio(codigo)
        resposta = formatar_mensagem_ubs(lista_ubs)
        
        bot.send_message(message.chat.id, resposta, parse_mode='Markdown', disable_web_page_preview=True)
    except Exception as e:
        bot.send_message(message.chat.id, "Erro ao conectar com o serviço de saúde. Tente mais tarde.")
        print(f"Erro técnico: {e}")

if __name__ == "__main__":
    print("Oswaldo ON")
    bot.polling()
