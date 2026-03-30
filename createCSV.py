import pandas as pd
import csv

#Cria tabela csv
with open('categoriaInformaçoes.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
tabelaCSV = {"Categoria":[],
             "Informação":[]
             }

with open('categoriaInformaçoes.csv', 'r') as f:
    reader =csv.reader(f)
df = pd.DataFrame(tabelaCSV)

def newLine(vetor, tabela):
    for dado in range(len(vetor)):
        tabela.loc[len(tabela)] = vetor[dado]
    print(tabela)
    return tabela

def mostrarTabele(tabela):
    print(tabela)

