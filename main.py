import scrapping
from scrapping import dominioGoverno, siteVacinacao
import createCSV
import dotenv
import os

dominioGoverno = 'https://www.gov.br'
siteVacinacao = dominioGoverno + '/saude/pt-br/vacinacao/calendario'

def main():
    #Scrapping 
    print("Main pronta")
    lista = scrapping.pegarLinksCalendario()
    for link in lista:
        print(link)
    dados = scrapping.extrairDadosVacinacao(siteVacinacao)
    print(scrapping.mostrar_dados(dados))

    #Criação do Arquivo CSV
    createCSV.newLine(dados, createCSV.tabelaCSV)

if __name__=="__main__":
    main()