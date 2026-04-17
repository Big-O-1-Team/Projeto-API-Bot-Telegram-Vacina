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
                    print(f'\rProgresso: {completo/1073741824:.2f} GB / {total/1073741824:.2f} GB', end="", flush=True),
        except ollama.ResponseError as e:
            e = str(e)
            if '-1' in e:
                raise ValueError(f'Modelo {modelo} não existe no Ollama!')
            raise ValueError('Erro inesperado ao baixar modelo Ollama!', f'Erro: {e}')
        print(f'\nModelo {modelo} baixado!')
    else:
        return print(f'Modelo já baixado: {modelo}')

# Conversa com o modelo
# message (obj) = objeto de mensagem do telebot
# modelo (string) = nome do modelo encontrado no site do ollama
# historicoChatIA (lista) = historico de mensagens
def chatIA(message, modelo, historicoChatIA): 
    historicoChatIA    
    resposta: ollama.ChatResponse = ollama.chat(
        model = modelo,
        messages = historicoChatIA + [{'role': 'user', 'content': message.text}],
    )
    texto = re.sub(r"<unused\d+>.*?<unused\d+>", "", resposta.message.content, flags=re.DOTALL)
    historicoChatIA += [{'role': 'user', 'content': message.text}]
    historicoChatIA += [{'role': 'assistant', 'content': texto}]
    return texto

