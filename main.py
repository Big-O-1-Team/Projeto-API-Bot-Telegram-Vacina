import time
import scripts.createCSV as createCSV
import dotenv
import os
import telebot
from telebot import types
from telebot.types import KeyboardButton, ReplyKeyboardMarkup
from datetime import date, datetime
import selenium
from selenium import webdriver
from scripts.scrappingselenium import AcessarInformacoes
import re
import scripts.BotIA as IA
import ollama
from scripts.telegramMessages import iniciarBOT

dotenv.load_dotenv()
bot_token = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(bot_token)

def main():

    #IA.verificarModeloOllama(modelo)
    
    # Scrapping
    print("Main pronta")
    dados = AcessarInformacoes()

    # Criação do Arquivo CSV
    createCSV.CriarCSV(dados)

    # Bot
    iniciarBOT()

if __name__ == "__main__":
    main()