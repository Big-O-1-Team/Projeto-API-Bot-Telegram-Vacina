from difflib import SequenceMatcher

def similaridade(a, b):
    a_minusc = a.lower()
    b_minusc = b.lower()
    return SequenceMatcher(None, a_minusc, b_minusc).ratio()

def comparar_postos(lista_google, lista_cnes, minimo=0.5):
    confirmados = []

    for posto_g in lista_google:
        for posto_c in lista_cnes:
            pontuacao_nome     = similaridade(posto_g['nome'],     posto_c['nome'])
            pontuacao_endereco = similaridade(posto_g['endereco'], posto_c['endereco'])
            pontuacao_final    = (pontuacao_nome + pontuacao_endereco) / 2

            if pontuacao_final >= minimo:
                confirmados.append({
                    'nome':     posto_c['nome'],
                    'tipo':     posto_c['tipo'],
                    'endereco': posto_g['endereco'],
                })

    return confirmados