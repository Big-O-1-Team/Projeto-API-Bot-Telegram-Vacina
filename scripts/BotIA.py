import ollama
import re
import telebot
# Verifica se o modelo escolhido está baixado na máquina.
# modelo (string) = nome do modelo encontrado no site do ollama
historico = {}
SYSTEM_PROMPT ='''Você é um bot de assistencia pessoal'''
#✅
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
#✅
def chatIA(chat_id: int, message: str) -> str:
    if chat_id not in historico:
        historico[chat_id] = [{
            'role': 'System',
            'content': SYSTEM_PROMPT
        }]
    historico[chat_id].append({
        'role': 'user',
        'content': message
    })
    Bot = ollama.chat(model= 'llama3.1:8b', messages=historico[chat_id])
    resposta = Bot['message']['content']
    historico[chat_id].append({
        'role':'IA',
        'content': resposta
    })
    return resposta



