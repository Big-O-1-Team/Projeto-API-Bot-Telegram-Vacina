import ollama
import re
import telebot
import whisper
import dotenv
import os

dotenv.load_dotenv() 

modelo = os.getenv('OLLAMA_MODEL')
historico = {}
SYSTEM_PROMPT ='''Seu nome é Oswaldo, um assistente virtual de vacinação simpático. 
Você está aqui para ajudar o usuário a acompanhar e manter sua agenda vacinal atualizada.
responda de forma objetiva mas carismática, evite o uso de *.
'''

def verificarModeloOllama():
    global modelo
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
        return print(f'Modelo carregado: {modelo}')

def chatIA(chat_id: int, message: str) -> str:
    global modelo
    if chat_id not in historico:
        historico[chat_id] = [{
            'role': 'System',
            'content': SYSTEM_PROMPT
        }]
    historico[chat_id].append({
        'role': 'user',
        'content': message
    })
    Bot = ollama.chat(model= modelo, messages=historico[chat_id])
    resposta = Bot['message']['content']
    historico[chat_id].append({
        'role':'assistant',
        'content': resposta
    })
    return resposta

def voz(arquivo):
    modelo_whisper = whisper.load_model('small')
    resultado = modelo_whisper.transcribe(f'{arquivo}', language='pt')
    return resultado["text"]
