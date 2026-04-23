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
dominioGoverno = 'https://www.gov.br'
siteVacinacao = dominioGoverno + '/saude/pt-br/vacinacao/calendario'
dotenv.load_dotenv()
bot_token = os.getenv('BOT_TOKEN')

# criar bot ligado com a chave
bot = telebot.TeleBot(bot_token)
#Variáveis Globais
nomesVacina = []
categoria = []

# função para o bot receber algo e retornar algo
@bot.message_handler(commands=['start'])
def receber(message):
    # criar botões / row_width = x define quantos botões por linha
    markup = types.InlineKeyboardMarkup(row_width=3)

    # personalizar botões
    calendario_vacinal = types.InlineKeyboardButton(
        'Conferir calendário de vacinas', callback_data='answer_calendario_vacinal')
    unidades_proximas = types.InlineKeyboardButton(
        'Buscar postos de vacinação', callback_data='answer_unidades_proximas')

    # "iniciar" botões
    markup.add(calendario_vacinal, unidades_proximas)

    # bot enviar mensagem
    bot.send_message(message.chat.id, 'Olá! Meu nome é Oswaldo, seu assistente virtual de vacinação. Estou aqui para ajudar você a acompanhar e manter sua agenda vacinal atualizada. Como deseja prosseguir? (Selecione uma das opções abaixo', reply_markup=markup)

# #resposta ao click do botão
@bot.callback_query_handler(func=lambda call: True)
def answer(callback):
    if callback.data == "answer_calendario_vacinal":
        gestanteMensagem(callback.message)
        bot.answer_callback_query(callback.id)
    
    if callback.data == "answer_unidades_proximas":
	pedir_localizacao(callback.message)

    if callback.data == 'yes':
        reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        for vacina in nomesVacina:
            vacinaname = re.sub(r"\(.*?\)", '', vacina).strip()
            reply_keyboard.add(f"{vacinaname}",)
        bot.send_message(callback.message.chat.id, "Escolha uma Opção abaixo.",reply_markup=reply_keyboard)

        bot.register_next_step_handler(callback.message, terceiroMenu)

        bot.answer_callback_query(callback.id)

    if  callback.data == 'yesPregnant':
        categoria.append('gestante')
        bot.send_message(callback.message.chat.id, "Digite a sua data de nascimento")
        bot.register_next_step_handler(callback.message, idadePorCategoria)
        bot.answer_callback_query(callback.id)

    if  callback.data == 'noPregnant':
        bot.send_message(callback.message.chat.id, "Digite a sua data de nascimento")
        bot.register_next_step_handler(callback.message, idadePorCategoria)
        bot.answer_callback_query(callback.id)
        
def terceiroMenu(message):
    texto = scrappingVacinaInfoIndividual(message.text)
    enviar_mensagem_longa(message.chat.id, texto)

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

def enviar_mensagem_longa(chat_id, texto):
    limite = 4096
    # divide o texto em partes de 4096 caracteres
    for i in range(0, len(texto), limite):
        parte = texto[i:i + limite]
        bot.send_message(chat_id, parte)

def gestanteMensagem(message):
    markup3 = types.InlineKeyboardMarkup(row_width=3)
    respostaSim = types.InlineKeyboardButton('Sim', callback_data= 'yesPregnant')
    respostaNao = types.InlineKeyboardButton('Nao', callback_data= 'noPregnant')
    markup3.add(respostaSim, respostaNao)
    bot.send_message(message.chat.id,"Você é gestante?", reply_markup=markup3)


def pedir_localizacao(message):	   # pede localização
        markup = types.ReplyKeyboardMarkup(row_width=1)
        botao_loc = KeyboardButton('📍 Compartilhar localização', request_location=True)
        markup.add(botao_loc)
        bot.send_message(message.chat.id, "Recebendo a localização", reply_markup = markup)
 
@bot.message_handler(content_types=['location']) #bot recebe localizacao
def receber_localizacao(message):
	latitude = message.location.latitude
	longitude = message.location.longitude


def idadePorCategoria(message):
    idadeAtual = salvar_idade(message)
    idade = idadeAtual[1] + 12 * idadeAtual[0]
    if idade < 0:
        bot.send_message(message.chat, "Categoria Inválida")
    if idade < 12 * 12:
        categoria.append('crianca')
    elif idade < 18 * 12:
        categoria.append('adolescente')
    elif idade < 60 * 12:
        categoria.append('adulto')
    else:
        categoria.append('idoso')

    for categorias in categoria:
        listaCategoriaFiltrada = createCSV.procuraInfoPCategoria(categorias)
        texto ='O paciente em questão pode tomar as seguintes vacinas: \n\n'
        for periodo, vacina, doencas in listaCategoriaFiltrada:
            nomesVacina.append(vacina)
            texto_periodo = ' '.join(periodo.split())
            if texto_periodo not in texto:
                texto += texto_periodo + ':' + '\n'   
            texto += '-' + vacina + '\n\n'

        tamanho = len(nomesVacina)
        if tamanho == 1:
            ultimoTexto = f' {tamanho} vacina'
        else:
            ultimoTexto= f' {tamanho} vacinas'
        texto = texto + '\n' + 'A pessoa pode tomar' + ultimoTexto
        enviar_mensagem_longa(message.chat.id, texto)
    perguntaMenu2(message)
        
def perguntaMenu2(message):
    markup2 = types.InlineKeyboardMarkup(row_width=3)
    respostaSim = types.InlineKeyboardButton('Sim', callback_data= 'yes')
    respostaNao = types.InlineKeyboardButton('Nao', callback_data= 'no')
    markup2.add(respostaSim, respostaNao)
    bot.send_message(message.chat.id,"Gostaria de saber mais informações sobre alguma vacina?", reply_markup=markup2)

def main():
    #Scrapping 
    print("Main pronta")
    dados = AcessarInformacoes()

    #Criação do Arquivo CSV
    createCSV.CriarCSV(dados)
    #Bot

    bot.polling()

if __name__=="__main__":
    main()
