import pandas as pd
import csv
tabelaCSV = {"Categoria":[],
             "Informação":[]
             }
with open('categoriaInformaçoes.csv', 'r') as arquivo:
    arquivo_csv =csv.reader(arquivo)

df = pd.DataFrame(tabelaCSV)
def newLine(vetor, tabela):
    for dado in range(len(vetor)):
        tabela.loc[len(tabela)] = vetor[dado]
    print(tabela)
    return tabela

def mostrarTabelA(tabela):
    print(tabela)
