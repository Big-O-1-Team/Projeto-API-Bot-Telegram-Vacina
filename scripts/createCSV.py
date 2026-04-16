import pandas as pd
from IPython.display import display

def CriarCSV(tabela):
    df = pd.DataFrame(tabela, columns=["Categoria","periodo", "Vacina", "Doencas Evitadas"])
    CSVFile = df.to_csv("CategoriaInformacoes.csv", index=False)
    display(df)
    return CSVFile

def procuraInfoPCategoria(categoria):
    with open("CategoriaInformacoes.csv", 'r', encoding = 'utf-8') as arquivo:
        CSVFile= pd.read_csv(arquivo)
        infoFiltrada = CSVFile[CSVFile['Categoria'] == categoria]
        infoFiltrada.columns = infoFiltrada.columns.str.strip()

    return infoFiltrada[['periodo', 'Vacina', 'Doencas Evitadas']].values.tolist()

def salvar_csv_ubs(resultados, arquivo='ubs_próximas.csv'):
    df = pd.DataFrame(resultados)
    df.to_csv(arquivo, index=False, encoding='utf-8-sig')
    return arquivo
