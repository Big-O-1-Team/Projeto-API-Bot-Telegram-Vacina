import ollama
import re

# Verifica se o modelo escolhido está baixado na máquina.
# modelo (string) = nome do modelo encontrado no site do ollama
def verificarModeloOllama(modelo):
    print('Verificando se modelo Ollama está baixado...')
    modelosBaixados = [m.model.lower() for m in ollama.list().models]
    if not modelo in modelosBaixados:
        try:
            print(f'Baixando {modelo}...')
            for progresso in ollama.pull(modelo, stream=True):
                completo = progresso.get('completed')
                total = progresso.get('total')
                if completo is not None and total is not None and total > 0:
                    print(f'\rProgresso: {completo/1073741824:.2f} GB / {total/1073741824:.2f} GB', end="", flush=True)
        except ollama.ResponseError as e:
            e = str(e)
            if '-1' in e:
                raise ValueError(f'Modelo {modelo} não existe no Ollama!')
            raise ValueError('Erro inesperado ao baixar modelo Ollama!', f'Erro: {e}')
        print(f'\nModelo {modelo} baixado!')
    else:
        print(f'Modelo já baixado: {modelo}')

# Conversa com o modelo
# message (obj) = objeto de mensagem do telebot
# modelo (string) = nome do modelo encontrado no site do ollama
# historicoChatIA = historico de mensagens
def chatIA(message, modelo, historicoChatIA): 
    cid = message.chat.id
    if cid not in historicoChatIA:
        historicoChatIA[cid] = [{'role': 'system', 'content': '''
                Você é o Oswaldo, um bot do telegram e um assistente virtual simpático capaz 
                de utilizar dados de portais públicos oficiais de saúde sobre vacinação, 
                com o objetivo de informar o cidadão sobre: Calendário de vacinação para 
                diferentes faixas etárias (crianças, adolescentes/jovens, adultos e idosos). 
                Coberturas vacinais em diferentes regiões brasileiras. Informações gerais 
                sobre vacinas disponíveis. Você irá interagir com o usuário 
                utilizando o Telegram. Responda de forma curta, apenas á perguntas sobre vacinas, e apenas
                informações brasileiras. Responda apenas em Português brasileiro. Apenas use '*' quando 
                for para organizar o texto em tópicos.
                IMPORTANTE: Não responda a esta mensagem de forma alguma.'''},
        {'role': 'assistant', 'content': '''
                Entendido. Sou o Oswaldo, um bot do telegram e um assistente virtual simpático, 
                apenas responderei a perguntas sobre vacinas no brasil, e apenas falarei em português 
                brasileiro.'''}]
    resposta: ollama.ChatResponse = ollama.chat(
        model = modelo,
        messages = historicoChatIA[cid] + [{'role': 'user', 'content': message.text}]
    )
    texto = re.sub(r"<unused\d+>.*?<unused\d+>", "", resposta.message.content, flags=re.DOTALL)
    historicoChatIA[cid] += [{'role': 'user', 'content': message.text}]
    historicoChatIA[cid] += [{'role': 'assistant', 'content': texto}]
    return texto

