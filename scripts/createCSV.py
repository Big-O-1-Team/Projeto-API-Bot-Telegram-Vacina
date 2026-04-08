import pandas as pd
from IPython.display import display

def CriarCSV(tabela):
    df = pd.DataFrame(tabela, columns=["Categoria","periodo", "Vacina", "Doenças Evitadas"])
    CSVFile = df.to_csv("CategoriaInformacoes.csv", index=False)
    display(df)
    return CSVFile

def procuraInfoPCategoria(categoria):
    with open("CategoriaInformacoes.csv", 'r') as arquivo:
        CSVFile= pd.read_csv(arquivo)
        infoFiltrada = CSVFile[CSVFile['Categoria'] == categoria]

    return infoFiltrada[['periodo', 'Vacina', 'Doenças Evitadas']].values.tolist()