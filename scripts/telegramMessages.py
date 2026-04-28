import time
import scripts.createCSV as createCSV
import dotenv
import os
import telebot
from telebot import types
from telebot.types import KeyboardButton, ReplyKeyboardMarkup
from datetime import date, datetime
import selenium
from selenium import webdriver
from scripts.scrappingselenium import AcessarInformacoes, scrappingVacinaInfoIndividual
import re
import scripts.BotIA as IA
import ollama
dominioGoverno = 'https://www.gov.br'
siteVacinacao = dominioGoverno + '/saude/pt-br/vacinacao/calendario'

dotenv.load_dotenv()
bot_token = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(bot_token)

modelo = 'gemma3n:e2b'
historicoChatIA = {}

sessao = {}

def get_sessao(chat_id):
    if chat_id not in sessao:
        sessao[chat_id] = {'nomesVacinas': [], 'categoria': [], 'ultima_mensagem': None, 'texto_pag': [], 'num_pag': 0} 
    return sessao[chat_id]

def limpar_sessao(chat_id):
    sessao[chat_id] = {'nomesVacinas': [], 'categoria': [], 'ultima_mensagem': None, 'texto_pag': [], 'num_pag': 0}


@bot.message_handler(commands=['start'])
def receber(message):   
    limpar_sessao(message.chat.id)
    markup = types.InlineKeyboardMarkup(row_width=3)

    calendario_vacinal = types.InlineKeyboardButton(
        'Conferir calendário de vacinas', callback_data='answer_calendario_vacinal')
    unidades_proximas = types.InlineKeyboardButton(
        'Buscar postos de vacinação', callback_data='answer_unidades_proximas')
    conversar_IA = types.InlineKeyboardButton(
        'Conversar com a nossa IA Oswaldo', callback_data='ia'
    )
    #Conjunto de botões 
    markup.add(calendario_vacinal, unidades_proximas, conversar_IA)
    bot.send_message(message.chat.id, 'Olá! Meu nome é Oswaldo, seu assistente virtual de vacinação. Estou aqui para ajudar você a acompanhar e manter sua agenda vacinal atualizada. Como deseja prosseguir? (Selecione uma das opções abaixo', reply_markup=markup)

 #resposta ao click do botão
@bot.callback_query_handler(func=lambda call: True)
def answer(callback):
    s = get_sessao(callback.message.chat.id)
    try:
        bot.answer_callback_query(callback.id, text = 'aguarde')
    except Exception as e:
        print(e)
        pass
    
    if callback.data == "answer_calendario_vacinal":
        gestanteMensagem(callback.message)

    if callback.data == 'yesPregnant':
        s['categoria'].append('gestante')
        perg_semanas_gestacao(callback.message, from_callback = True)

    if callback.data == 'noPregnant':
        perg_nascimento(callback.message, from_callback = True)

    if callback.data == 'avançar':
        s['num_pag'] += 1
        imprimir_infoVacinas(callback.message, s)

    if callback.data == "voltar":
        s['num_pag'] -= 1
        imprimir_infoVacinas(callback.message, s)
        
    if callback.data == 'ia':
        s = get_sessao(callback.message.chat.id)
        bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=s['ultima_mensagem'],
            text='Olá! Estou pronto para receber suas dúvidas.'
        )
        bot.register_next_step_handler(callback.message, conversarIA)
    if callback.data == 'sair':
        receber(callback)


def conversarIA(message):
    s = get_sessao(message.chat.id)
    markup = types.InlineKeyboardMarkup(row_width=1)
    sairBotao =types.InlineKeyboardButton('Sair', callback_data= 'sair')
    while True:
        bot.edit_message_text(chat_id=message.chat.id, message_id= s['ultima_mensagem'], text= IA.chatIA( message.text, modelo, historicoChatIA), reply_markup=markup)
        markup.add(sairBotao)
    



def salvar_idade(idade):
    idadeAtual = []
    # Converte o texto digitado em uma data de verdade
    nascimento = datetime.strptime(idade.text, "%d/%m/%Y").date()
    # Calcula a idade em anos e meses
    hoje = date.today()
    anos = hoje.year - nascimento.year
    meses = hoje.month - nascimento.month
    if hoje.day < nascimento.day:
        meses -= 1
    if meses < 0:
        anos -= 1
        meses += 12
    anos = int(anos)
    meses = int(meses)
    idadeAtual.append(anos)
    idadeAtual.append(meses)
    return idadeAtual

def gestanteMensagem(message):
    markup3 = types.InlineKeyboardMarkup(row_width=3)
    respostaSim = types.InlineKeyboardButton('Sim', callback_data='yesPregnant')
    respostaNao = types.InlineKeyboardButton('Nao', callback_data='noPregnant')
    markup3.add(respostaSim, respostaNao)
    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.message_id,
        text="Você é gestante?",
        reply_markup=markup3
    )
    s = get_sessao(message.chat.id)
    s['ultima_mensagem'] = message.message_id

def perg_semanas_gestacao(message, from_callback = False):
    s = get_sessao(message.chat.id)
    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=s['ultima_mensagem'],
        text='Quantas semanas de gestação?'
    )
    bot.register_next_step_handler(message, perg_nascimento)

def perg_nascimento(message, from_callback = False):
    s = get_sessao(message.chat.id)
    if not from_callback:
        try:
          bot.delete_message(
            chat_id=message.chat.id,
            message_id=message.message_id)
        except Exception:
            pass
    
    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=s['ultima_mensagem'],
        text='Qual sua data de nascimento? (DD/MM/AAAA)'
    )
    bot.register_next_step_handler(message, idadePorCategoria)

def idadePorCategoria(message):
    s = get_sessao(message.chat.id)

    try:
        bot.delete_message(
            chat_id=message.chat.id,
            message_id=message.message_id)
    except Exception:
        pass

    idadeAtual = salvar_idade(message)
    idade = 12 * idadeAtual[0] + idadeAtual[1] 
    if idade < 0:
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=s['ultima_mensagem'],
            text='Categoria inválida'
        )


    if idade < 12 * 12:
        s['categoria'].append('crianca')
    elif idade < 18 * 12:
        s['categoria'].append('adolescente')
    elif idade < 60 * 12:
        s['categoria'].append('adulto')
    else:
        s['categoria'].append('idoso')
    for categorias in s['categoria']:
        listaCategoriaFiltrada = createCSV.procuraInfoPCategoria(categorias, idade)
        texto = 'O paciente em questão pode tomar as seguintes vacinas: \n\n'
        for periodo, vacina, doencas in listaCategoriaFiltrada:
            s['nomesVacinas'].append(vacina)
            texto_periodo = ' '.join(periodo.split())
            if texto_periodo not in texto:
                texto += texto_periodo + ':' + '\n'
            texto += '-' + vacina + '\n\n'

        tamanho = len(s['nomesVacinas'])
        if tamanho == 1:
            ultimoTexto = f' {tamanho} vacina'
        else:
            ultimoTexto = f' {tamanho} vacinas'
        texto = texto + '\n' + 'A pessoa pode tomar' + ultimoTexto
    s['num_pag'] = 0
    imprimir_infoVacinas(message, s)

def imprimir_infoVacinas(message, s):
    #identifica textos das categorias por "páginas"
    pag = s['num_pag']
    total_pag = len(s['texto_pag'])
    texto = s['texto_pag'][pag]    

    #botões para navegar entre as páginas e conversar com a IA
    markup2 = types.InlineKeyboardMarkup(row_width=3)
    botoes = []
    if pag > 0:
        botoes.append(types.InlineKeyboardButton('⬅️', callback_data='voltar'))
    botoes.append(types.InlineKeyboardButton('Conversar com nossa IA', callback_data='ia'))
    if pag < total_pag - 1:
        botoes.append(types.InlineKeyboardButton('➡️', callback_data='avançar'))
    markup2.add(*botoes)
    
    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=s['ultima_mensagem'],
        text=texto,
        reply_markup=markup2
    )
    
def iniciarBOT():
    while True:
        try:
            print("Bot iniciado...")
            bot.polling(non_stop=True, interval=0, timeout=20)
        except Exception as e:
            print(f"Erro: {e}")
            print("Reconectando em 5 segundos...")
            time.sleep(5)
    