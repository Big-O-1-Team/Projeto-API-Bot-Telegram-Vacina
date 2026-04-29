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
from scripts.scrappingselenium import AcessarInformacoes
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

#✅
def criar_sessao(chat_id):
    if chat_id not in sessao:
        sessao[chat_id] = {'nomesVacinas': [], 'categoria': [], 'ultima_mensagem': None, 'texto_pag': '', 'pag_atual': 0}
        return sessao[chat_id] 
    return sessao[chat_id]
#✅
def limpar_sessao(chat_id):
    sessao[chat_id] = {'nomesVacinas': [], 'categoria': [], 'ultima_mensagem': None, 'texto_pag': [], 'pag_atual': 0}

#✅
@bot.message_handler(commands=['start'])
def receber(message):   
    limpar_sessao(message.chat.id)
    criar_sessao(message.chat.id)
    #Botões Iniciais
    markup = types.InlineKeyboardMarkup(row_width=3)
    calendario_vacinal = types.InlineKeyboardButton('Conferir calendário de vacinas', callback_data='answer_calendario_vacinal')
    unidades_proximas = types.InlineKeyboardButton('Buscar postos de vacinação', callback_data='answer_unidades_proximas')
    conversar_IA = types.InlineKeyboardButton('Conversar com a nossa IA Oswaldo', callback_data='ia')
    markup.add(calendario_vacinal, unidades_proximas, conversar_IA)
    bot.send_message(message.chat.id, 'Olá! Meu nome é Oswaldo, seu assistente virtual de vacinação. Estou aqui para ajudar você a acompanhar e manter sua agenda vacinal atualizada. Como deseja prosseguir? (Selecione uma das opções abaixo', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def answer(callback):
    #✅
    s = criar_sessao(callback.message.chat.id)
    try:
        bot.answer_callback_query(callback.id, text = 'aguarde')
    except Exception as e:
        print(e)
        pass
    #✅
    if callback.data == "answer_calendario_vacinal":
        gestanteMensagem(callback.message)
    #✅
    elif callback.data == 'yesPregnant':
        s['categoria'].append('gestante')
        perg_nascimento(callback.message)
    #✅
    elif callback.data == 'noPregnant':
        perg_nascimento(callback.message)
    #🔁
    elif callback.data == 'avançar':
        s['pag_atual'] += 1
        imprimir_infoVacinas(callback.message, s)
    #🔁
    elif callback.data == "voltar":
        s['pag_atual'] -= 1
        imprimir_infoVacinas(callback.message, s)
    #🔁
    elif callback.data == 'ia':
        conversarIA(callback.message, s)
    #🔁
    elif callback.data == 'sair':
        receber(callback.message)

#🔁
def conversarIA(message, s):
    s = criar_sessao(message.chat.id)
    markup = types.InlineKeyboardMarkup(row_width=1)
    sairBotao =types.InlineKeyboardButton('Sair', callback_data= 'sair')
    try:
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=s['ultima_mensagem'],
            text='Olá! Estou pronto para receber suas dúvidas.',
            reply_markup=markup
        )
    except Exception:
        bot.send_message(s, "Olá, como posso te ajudar?🐧")
    bot.register_next_step_handler(message, iaPensando)
#🔁
def iaPensando(message, s):
    s = criar_sessao(message.chat.id)
    markup = types.InlineKeyboardMarkup(row_width=1)
    sairBotao = types.InlineKeyboardButton('Sair', callback_data= 'sair')
    texto_resposta = IA.chatIA(message.text, modelo = 'llama3.1:8b', historicoChatIA=historicoChatIA)
    try:
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=s['ultima_mensagem'],
            text=texto_resposta,
            reply_markup=markup
        )
    except Exception:
        bot.send_message(s, texto_resposta, reply_markup=markup)
    bot.register_next_step_handler(message, iaPensando)

#✅   
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
#✅
def gestanteMensagem(message):
    markup3 = types.InlineKeyboardMarkup(row_width=2)
    respostaSim = types.InlineKeyboardButton('Sim', callback_data='yesPregnant')
    respostaNao = types.InlineKeyboardButton('Nao', callback_data='noPregnant')
    markup3.add(respostaSim, respostaNao)
    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.message_id,
        text="Você é gestante?",
        reply_markup=markup3
    )
    s = criar_sessao(message.chat.id)
    s['ultima_mensagem'] = message.message_id

#✅
def perg_nascimento(message):
    s = criar_sessao(message.chat.id)
    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=s['ultima_mensagem'],
        text='Qual sua data de nascimento? (DD/MM/AAAA)'
    )   
    bot.register_next_step_handler(message, idadePorCategoria)
#🔁
def idadePorCategoria(message):
    #✅
    s = criar_sessao(message.chat.id)
    idadeAtual = salvar_idade(message)
    idade = 12 * idadeAtual[0] + idadeAtual[1] 
    if idade < 0:
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=s['ultima_mensagem'],
            text='Categoria inválida'
        )
    if idade <= 14 * 12:
        s['categoria'].append('crianca')
    if idade <= 24 * 12:
        s['categoria'].append('adolescente')
    if idade < 60 * 12:
        s['categoria'].append('adulto')
    if idade >= 60 *12:
        s['categoria'].append('idoso')

    #❌❌❌
    for categorias in s['categoria']:
        listaCategoriaFiltrada = createCSV.procuraInfoPCategoria(categorias, idade)
        #✅
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
    texto_completo = texto + '\n' + 'A pessoa pode tomar' + ultimoTexto
    print(s['categoria'])
    print(texto_completo)
    s['pag_atual'] = 0
    imprimir_infoVacinas(message, s, texto_completo)
    try:
        bot.delete_message(
            chat_id=message.chat.id,
            message_id=message.message_id)
    except Exception:
        pass

def dividir_mensagem(texto, s):
    limite = 4096
    tamanho_texto = len(texto)
    if tamanho_texto <= limite:
        s['texto_pag'].append(texto)
        return None
    while tamanho_texto > 0:
        sessao['texto_pag'].append(texto[:limite])
        texto = texto[limite:]
        tamanho_texto = len(texto)

        
#Criar função para calcular o tamanho máximo de caracteres que podem ter uma mensagem
def num_pags(texto):
    limite = 4096
    tamanho_texto = len(texto)
    if tamanho_texto % limite == 0: numero_de_paginas = tamanho_texto//limite
    else: numero_de_paginas = (tamanho_texto//limite) + 1
    return numero_de_paginas

#❌
def imprimir_infoVacinas(message, s, texto):
    #✅
    pag = s['pag_atual']
    total_pag = num_pags(texto)

    dividir_mensagem(texto, s)
    texto = s['texto_pag'][pag]    
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

#✅
def iniciarBOT():
    while True:
        bot.polling(non_stop=True, interval=0, timeout=20)

    