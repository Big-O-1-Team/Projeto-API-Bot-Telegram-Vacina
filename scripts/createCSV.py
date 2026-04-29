import pandas as pd
from IPython.display import display
import csv
import re

def CriarCSV(tabela):
    df = pd.DataFrame(tabela, columns=["Categoria","Periodo", "Vacina", "Doencas Evitadas"])
    df['Desde'] = df[['Periodo', 'Categoria']].apply(lambda row: extrairPeriodo(row['Periodo'], row['Categoria'])[0], axis=1)
    df['Ate'] =  df[['Periodo', 'Categoria']].apply(lambda row: extrairPeriodo(row['Periodo'], row['Categoria'])[1], axis=1)
    CSVFile = df.to_csv("CategoriaInformacoes.csv", index=False)
    display(df)
    return CSVFile


def extrairPeriodo(periodo: str, categoria :str):
    periodo = periodo.lower().strip()
    categoria = categoria.lower().strip()
    vetor_aux = []
    if categoria == 'idoso':
        return 60 * 12, 999*12
    elif categoria == 'adulto':
        return 24*12, 59*12
    elif categoria =='gestante':
        return 0, 9
    elif categoria =='adolescente' or 'crianca':
        if periodo == 'ao nascer':
            return 0 , 1
        regex = re.findall(r"\d{1,2}", periodo)
        for x in regex:
            x = x.replace(' ', '')
            x = int(x)
            vetor_aux.append(x)
        if len(vetor_aux) == 1:
            if 'meses' in periodo:
                return vetor_aux[0], 999
            else:
                return vetor_aux[0]*12, 999*12
        else:
            if 'meses' in periodo:
                return vetor_aux[0], vetor_aux[1]
            else:
                return vetor_aux[0]*12, vetor_aux[1]*12



def procuraInfoPCategoria(categoria, idade):
    with open("CategoriaInformacoes.csv", 'r', encoding = 'utf-8') as arquivo:
        CSVFile= pd.read_csv(arquivo)
        CSVFile.columns = CSVFile.columns.str.strip()
        if categoria == 'gestante':
            infoFiltrada = CSVFile[CSVFile['Categoria'] == categoria]
        else:
            infoFiltrada = CSVFile[
                (CSVFile['Categoria'] == categoria) &
                (CSVFile['Desde']>=idade) &
                (CSVFile['Ate']<=idade)
            ]
        if infoFiltrada.empty:
            return []           
        return infoFiltrada[['Periodo', 'Vacina', 'Doencas Evitadas']].values.tolist()

def salvar_csv_ubs(resultados, arquivo='ubs_próximas.csv'):
    df = pd.DataFrame(resultados)
    df.to_csv(arquivo, index=False, encoding='utf-8-sig')
    return arquivo



        


