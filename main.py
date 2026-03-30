import scrapping
from scrapping import dominioGoverno, siteVacinacao
import createCSV
import dotenv
import os
import telebot
from telebot import types
dominioGoverno = 'https://www.gov.br'
siteVacinacao = dominioGoverno + '/saude/pt-br/vacinacao/calendario'




def main():
    #Scrapping 
    print("Main pronta")
    lista = scrapping.pegarLinksCalendario()
    for link in lista:
        print(link)
    dados = scrapping.extrairDadosVacinacao(siteVacinacao)
  
    #Criação do Arquivo CSV
    createCSV.CriarCSV(dados)

    #Bot
 
    

if __name__=="__main__":
    main()