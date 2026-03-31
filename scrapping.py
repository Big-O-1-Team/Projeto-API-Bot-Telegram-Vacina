import requests
from bs4 import BeautifulSoup
import csv
import dotenv
import os


dominioGoverno = 'https://www.gov.br'
siteVacinacao = dominioGoverno + '/saude/pt-br/vacinacao/calendario'
#A URL base e principal do sites para acessar os calendários de vacinação

def acessarPagina(url, *args, **kwargs):           #Acessa a página e retorna o conteúdo HTML
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    try:
        resposta = requests.get(url, headers=headers, *args, **kwargs)
        resposta.raise_for_status()
    except requests.exceptions.RequestException as erro:        #Trata erros de conexão e HTTP
        print('erro ao acessar:', url, erro)
        return None
    return BeautifulSoup(resposta.text, 'html.parser')


def pegarLinksCalendario():       #Pega os links dos calendários de vacinação para diferentes categorias
    soup = acessarPagina(siteVacinacao)
    if not soup:
        return []
    links = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        if 'calendario?id=' in href.lower():
            if not href.startswith('http'):
                href = dominioGoverno + href
            links.append(href)
    return list(set(links))




def extrairDadosVacinacao(url):     #Extrai os dados de vacinação da página do calendário e retorna uma lista de tuplas
    soup = acessarPagina(url)
    if not soup:
        return []
    main = soup.find('main')
    if not main:
        return []
    dados = []
    categoria = None

    for tag in main.find_all(['h2', 'h3', 'li', 'p']):
        texto = tag.get_text(strip=True)
        if not texto:
            continue
        t = texto.lower()
        if 'criança' in t:
            categoria = 'criança'
            continue
        elif 'adolescente' in t:
            categoria = 'adolescente'
            continue
        elif 'adulto' in t:
            categoria = 'adulto'
            continue
        elif 'idoso' in t:
            categoria = 'idoso'
            continue
        elif 'gestante' in t:
            categoria = 'gestante'
            continue
        if categoria:
            dados.append((categoria, texto))
    return dados

