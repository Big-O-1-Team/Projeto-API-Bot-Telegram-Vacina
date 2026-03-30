import pandas as pd
from IPython.display import display

def CriarCSV(tabela):
    df = pd.DataFrame(tabela, columns=["Categoria", "Vacina/Info"])
    CSVFile = df.to_csv("CategoriaInformacoes.csv", index=False)
    display(df)
    return CSVFile

