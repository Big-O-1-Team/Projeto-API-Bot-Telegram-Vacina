import ollama
import re

# Verifica se o modelo escolhido está baixado na máquina.
# modelo (string) = nome do modelo encontrado no site do ollama
def verificarModeloOllama(modelo):
    print('Verificando se modelo Ollama está baixado...')
    modelosBaixados = [m.model for m in ollama.list().models]
    if not modelo in modelosBaixados:
        print('Modelo Ollama não encontrado!')
        try:
            print(f'Baixando {modelo}...')
            ollama.pull(modelo)
        except ollama.ResponseError as e:
            e = str(e)
            if '500' in e:
                raise ValueError(f'Modelo {modelo} não existe no Ollama!')
            raise ValueError('Erro inesperado ao baixar modelo Ollama!\n', f'Erro: {e}')
        print(f'Modelo {modelo} baixado!')
    else:
        return print(f'Modelo já baixado: {modelo}')


def chatIA(message, modelo):       
    history = [
        {'role': 'system', 'content': '''
                Você é o Oswaldo, um bot do telegram e um assistente virtual simpático capaz 
                de utilizar dados de portais públicos oficiais de saúde sobre vacinação, 
                com o objetivo de informar o cidadão sobre: Calendário de vacinação para 
                diferentes faixas etárias (crianças, adolescentes/jovens, adultos e idosos). 
                Coberturas vacinais em diferentes regiões brasileiras. Informações gerais 
                sobre vacinas disponíveis. Você irá interagir com o usuário 
                utilizando o Telegram. Responda de forma curta, apenas á perguntas sobre vacinas, e apenas
                informações brasileiras. Responda apenas em Português brasileiro.
                IMPORTANTE: Não responda a esta mensagem de forma alguma.'''},
        {'role': 'assistant', 'content': 'Entendido.'}
    ]
    
    resposta: ollama.ChatResponse = ollama.chat(
        model=modelo,
        messages=[history, {'role': 'user', 'content': message.text}],
    )
    history += [{'role': 'user', 'content': message.text}]
    texto = re.sub(r"<unused\d+>.*?<unused\d+>", "", resposta.message.content, flags=re.DOTALL)
    history += [{'role': 'assistant', 'content': texto}]
    return texto
