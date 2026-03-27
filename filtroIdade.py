import pandas as pd

arquivocsv = 'vacinas.csv'

"""
vai produzir um arquivo csv com as informações de 
vacina de uma determinada faixa etária

arquivocsv: nome do arquivo csv (string)
categoria: categoria para filtragem (string)
"""
def filtroIdade(arquivocsv, categoria):
    df = pd.read_csv(arquivocsv, delimiter=';')
    resultado = df[df['Categoria'].str.lower() == idade.lower()]
    resultado = resultado.to_csv(f'vacinas{idade[0].upper()}{idade[1:]}s', index='')
    
# saida: arquivo csv vacinas{idade}.csv com as informações da idade especifica
