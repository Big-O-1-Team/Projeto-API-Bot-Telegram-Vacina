import ollama

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
