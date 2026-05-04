import scripts.createCSV as createCSV
import dotenv
import os
import telebot
from telebot import types
from telebot.types import KeyboardButton
from datetime import date, datetime
import scripts.BotIA as IA
import shelve
from scripts.googlemaps import busca_no_maps as BuscarUBS
from scripts.othercountry import listCountries, InfoAcessPCountry
dominioGoverno = 'https://www.gov.br'
siteVacinacao = dominioGoverno + '/saude/pt-br/vacinacao/calendario'
dotenv.load_dotenv()
bot_token = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(bot_token)
modelo = 'gemma3n:e2b'
historicoChatIA = {}
sessao = {}

def criar_sessao(chat_id):
    if chat_id not in sessao:
        sessao[chat_id] = {'nomesVacinas': [], 'categoria': [], 'ultima_mensagem': None, 'texto_pag': '', 'pag_atual': 0}
        return sessao[chat_id] 
    return sessao[chat_id]

def limpar_sessao(chat_id):
    sessao[chat_id] = {'nomesVacinas': [], 'categoria': [], 'ultima_mensagem': None, 'texto_pag': [], 'pag_atual': 0}

@bot.message_handler(commands=['start'])
def receber(message): 
    #Conseguir informações do usuário
    messageFromUser = message.from_user 
    #Salvar o nome ou username do usuário
    nome_exibir = messageFromUser.username if messageFromUser.username else messageFromUser.full_name

        
    limpar_sessao(message.chat.id)
    markup = types.InlineKeyboardMarkup(row_width=2)
  
    try:
        markup = types.InlineKeyboardMarkup(row_width=1)
        calendario_vacinal = types.InlineKeyboardButton('📅 Calendário de vacinas', callback_data='answer_calendario_vacinal')
        unidades_proximas = types.InlineKeyboardButton('🏥 Postos de vacinação', callback_data='answer_unidades_proximas')
        conversar_IA = types.InlineKeyboardButton('🐧 Falar com nosso agente AI Oswaldo', callback_data='ia')
        outroPais = types.InlineKeyboardButton('🗺️ Vacinas para outros países', callback_data='otherCountry')
        markup.add(calendario_vacinal, unidades_proximas, conversar_IA, outroPais)
        bot.edit_message_text(message.chat.id, text='Gostaria de fazer uma nova consulta? (Selecione uma das opções abaixo)', reply_markup=markup)
    except:
        limpar_sessao(message.chat.id)
        criar_sessao(message.chat.id)
        #Botões Iniciais
        markup = types.InlineKeyboardMarkup(row_width=1)
        calendario_vacinal = types.InlineKeyboardButton('📅 Calendário de vacinas', callback_data='answer_calendario_vacinal')
        unidades_proximas = types.InlineKeyboardButton('🏥 Postos de vacinação', callback_data='answer_unidades_proximas')
        conversar_IA = types.InlineKeyboardButton('🐧 Falar com nosso agente AI Oswaldo', callback_data='ia')
        outroPais = types.InlineKeyboardButton('🗺️ Vacinas para outros países', callback_data='otherCountry')
        markup.add(calendario_vacinal, unidades_proximas, conversar_IA, outroPais)
        bot.send_message(message.chat.id, f'Olá!🐧 {nome_exibir},meu nome é Oswaldo, seu assistente virtual de vacinação. Estou aqui para ajudar você a acompanhar e manter sua agenda vacinal atualizada. Como deseja prosseguir?', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def answer(callback):
    s = criar_sessao(callback.message.chat.id)
    try:
        bot.answer_callback_query(callback.id, text = 'aguarde')
    except Exception as e:
        print(e)
        pass
    if callback.data == "answer_calendario_vacinal":
        gestanteMensagem(callback.message)
    elif callback.data == 'yesPregnant':
        s['categoria'].append('gestante')
        perg_nascimento(callback.message)
    elif callback.data == 'noPregnant':
        perg_nascimento(callback.message)
    elif callback.data == 'avançar':
        s['pag_atual'] += 1
        imprimir_infoVacinas(callback.message, s, '')
    elif callback.data == "voltar":
        s['pag_atual'] -= 1
        imprimir_infoVacinas(callback.message, s, '')
    elif callback.data == 'ia':
        markup = types.InlineKeyboardMarkup(row_width=1)
        sairBotao =types.InlineKeyboardButton('Sair', callback_data= 'sair')
        bot.send_message(callback.message.chat.id, 'Qual seria a sua dúvida?')
        bot.register_next_step_handler(callback.message, conversarIA)
    elif callback.data == 'sair':
        bot.clear_step_handler_by_chat_id(callback.message.chat.id)
        receber(callback.message)
    elif callback.data == "answer_unidades_proximas":
        botaoEscolherPessoaLoc(callback.message)
    elif callback.data == 'locForMe':
        pedir_localizacao(callback.message)
    elif callback.data == 'locManually':
        bot.send_message(callback.message.chat.id, "Digite o endereço")
        bot.register_next_step_handler(callback.message, receber_localizacao)
        return   
    elif callback.data =='otherCountry':
        messageOtherCountry(callback.message)

def messageOtherCountry(message):
    countryButton = []
    lista = listCountries()
    markup = types.ReplyKeyboardMarkup(row_width=2)
    for country in lista:
        countryButton.append(types.KeyboardButton(country))
    markup.add(*countryButton)
    bot.send_message(message.chat.id, 'Escolha o país que você viajará: ', reply_markup=markup)
    bot.register_next_step_handler(message, answerOtherCountry)

def answerOtherCountry(message):
    s =criar_sessao(message.chat.id)
    msg = bot.send_message(message.chat.id, "🔄️ Buscando Informações, aguarde...")
    s['ultima_mensagem'] = msg.message_id
    infos = InfoAcessPCountry(message.text)
    imprimir_infoVacinas(message,s, infos)

def botaoEscolherPessoaLoc(message):
    s =criar_sessao(message.chat.id)
    markup = types.InlineKeyboardMarkup(row_width=2)
    respostaSim = types.InlineKeyboardButton('Localização atual', callback_data='locForMe')
    respostaNao = types.InlineKeyboardButton('Inserir manualmente', callback_data='locManually')
    markup.add(respostaSim, respostaNao)
    msg = bot.send_message(message.chat.id,"Escolha uma das opçoes abaixo",reply_markup=markup)
    s['ultima_mensagem'] = msg.message_id

    
def pedir_localizacao(message):
    s =criar_sessao(message.chat.id)
    markup = types.ReplyKeyboardMarkup(row_width=2)
    botao_loc_sim = types.KeyboardButton('📍 Sim, compartilhar', request_location=True)
    botao_loc_nao = types.KeyboardButton('📍 Não, mudei de ideia')
    markup.add(botao_loc_sim, botao_loc_nao)
    msg = bot.send_message(message.chat.id, "Deseja compartilhar sua localização?",reply_markup=markup)
    s['ultima_mensagem'] = msg.message_id

@bot.message_handler(content_types=['location'])
def receber_localizacao(message):
    s =criar_sessao(message.chat.id)
    try:
        latitude = message.location.latitude
        longitude = message.location.longitude
        localizacao = f"{latitude}, {longitude}"
        print(f" latitude : {latitude}, longitude: {longitude}")
    except:
        localizacao = message.text
        print(f" endereco : {localizacao}")
    bot.send_message(message.chat.id, "Localização recebida!")
    UBSPRoximas = BuscarUBS(localizacao)
    texto = ''
    for UBS in range(len(UBSPRoximas)):
        texto += UBSPRoximas[UBS]['nome'] + '\n'
        texto += UBSPRoximas[UBS]['endereco'] + '\n\n'
    print(texto)
    msg = bot.send_message(message.chat.id, texto)
    s['ultima_mensagem'] = msg.message_id


def conversarIA(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    sairBotao =types.InlineKeyboardButton('Sair', callback_data= 'sair')
    resposta = IA.chatIA(message.chat.id, message.text)
    markup.add(sairBotao)
    bot.send_message(message.chat.id, text= resposta, reply_markup=markup)
    bot.register_next_step_handler(message, conversarIA)


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


def perg_nascimento(message):
    s = criar_sessao(message.chat.id)
    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=s['ultima_mensagem'],
        text='Qual sua data de nascimento? (DD/MM/AAAA)'
    )   
    bot.register_next_step_handler(message, idadePorCategoria)

def idadePorCategoria(message):
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
    print(f"A idade é {idade}")
    texto = 'O paciente em questão pode tomar as seguintes vacinas: \n\n'
    for categorias in s['categoria']:
        listaCategoriaFiltrada = createCSV.procuraInfoPCategoria(categorias, idade)
        for Periodo, Vacina, Doencas in listaCategoriaFiltrada:
            s['nomesVacinas'].append(Vacina)
            texto_periodo = ' '.join(Periodo.split())
            if texto_periodo not in texto:
                texto += texto_periodo + ':' + '\n'
            texto += '-' + Vacina + '\n\n'
            print( f"- {Vacina}" )
    tamanho = len(s['nomesVacinas'])
    if tamanho == 1:
        ultimoTexto = f' {tamanho} vacina'
    else:
        ultimoTexto = f' {tamanho} vacinas'
    texto_completo = texto + '\n' + 'A pessoa pode tomar' + ultimoTexto
    s['pag_atual'] = 0
    imprimir_infoVacinas(message, s, texto_completo)
    try:
        bot.delete_message(
            chat_id=message.chat.id,
            message_id=message.message_id)
    except Exception:
        pass

def dividir_mensagem(texto, s):
    if s['texto_pag']:  
        return
    limite_individual = 300
    caracteres = 'abcdefghijklmnopqrstuvwxyz:,.-êç '
    while texto:
        string_atual = texto[:limite_individual].lower()
        if string_atual in caracteres:
            while string_atual in caracteres:
                limite_individual+=1
                string_atual = texto[:limite_individual]
        s['texto_pag'].append(texto[:limite_individual])
        texto = texto[limite_individual:]

def num_pags(texto,s):
    if not texto:
        return len(s['texto_pag'])
    limite = 300
    tamanho_texto = len(texto)
    if tamanho_texto % limite == 0: numero_de_paginas = tamanho_texto//limite
    else: numero_de_paginas = (tamanho_texto//limite) + 1
    return numero_de_paginas

def imprimir_infoVacinas(message, s, texto):
    if texto:
        dividir_mensagem(texto, s)
    total_pag = num_pags(texto,s)
    pag = s['pag_atual']
    texto_pag = s['texto_pag'][pag]    
    markup2 = types.InlineKeyboardMarkup(row_width=3)
    botoes = []
    if pag > 0:
        botoes.append(types.InlineKeyboardButton('⬅️', callback_data='voltar'))
    botoes.append(types.InlineKeyboardButton('Conversar com nossa IA', callback_data='ia'))
    if pag < total_pag - 1:
        botoes.append(types.InlineKeyboardButton('➡️', callback_data='avançar'))
    markup2.add(*botoes)
    texto_pag = s['texto_pag'][pag] + f'\n\n Página {pag + 1} de {total_pag}'
    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=s['ultima_mensagem'],
        text=texto_pag,
        reply_markup=markup2
    )
    

def iniciarBOT():
    while True:
        bot.polling(non_stop=True, interval=0, timeout=20)

    