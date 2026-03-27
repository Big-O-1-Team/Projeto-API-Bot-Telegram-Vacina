import requests
from bs4 import BeautifulSoup
import csv

BASE_URL = 'https://www.gov.br'
URL_PRINCIPAL = BASE_URL + '/saude/pt-br/vacinacao'
#A URL base e principal do sites para acessar os calendários de vacinação

def acessar_pagina(url, *args, **kwargs):           #Acessa a página e retorna o conteúdo HTML
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


def pegar_links_calendario():       #Pega os links dos calendários de vacinação para diferentes categorias
    soup = acessar_pagina(URL_PRINCIPAL)
    if not soup:
        return []
    links = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        if 'calendario?id=' in href.lower():
            if not href.startswith('http'):
                href = BASE_URL + href
            links.append(href)
    return list(set(links))


def separar_vacina_idade(texto):            #Separa o nome da vacina e a idade recomendada a partir do texto
    texto = texto.replace('\n', ' ').strip()
    palavras = ['ao nascer', 'meses', 'mês', 'anos', 'ano', 'dose', 'reforço', 'única']
    for p in palavras:
        if p in texto.lower():
            partes = texto.lower().split(p, 1)
            vacina = partes[0].strip().title()
            idade = (p + partes[1]).strip()
            return vacina, idade
    return texto.strip(), 'não informado'


def extrair_dados(url):     #Extrai os dados de vacinação da página do calendário e retorna uma lista de tuplas
    soup = acessar_pagina(url)
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
            vacina, idade = separar_vacina_idade(texto)
            dados.append((categoria, vacina, idade))
    return dados

def remover_duplicados(dados):
    return list(set(dados))

def ordenar_dados(dados):       #Ordena os dados por categoria e idade para facilitar a leitura
    return sorted(dados, key=lambda x: (x[0], x[1]))


def salvar_csv(dados):      #Salva os dados em um arquivo CSV com as colunas Categoria, Vacina e Idade
    with open('vacinas.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(['Categoria', 'Vacina', 'Idade'])
        for categoria, vacina, idade in dados:
            writer.writerow([
                categoria.strip(),
                vacina.strip(),
                idade.strip()
            ])


def mostrar_dados(dados):       #Exibe os dados de vacinação no console de forma organizada para facilitar a leitura
    print('\nCALENDÁRIO DE VACINAÇÃO\n')
    for categoria, vacina, idade in dados:
        print('categoria:', categoria)
        print('vacina:', vacina)
        print('idade:', idade)
        print('-' * 40)


def main():         #Função principal para pegar os links dos calendários, extrair os dados, remover duplicados, ordenar, salvar em CSV e mostrar no console
    links = pegar_links_calendario()
    print('links encontrados:', len(links))
    todos_dados = []

    for link in links:
        print('acessando:', link)
        dados = extrair_dados(link)
        todos_dados.extend(dados)

    if todos_dados:
        todos_dados = remover_duplicados(todos_dados)
        todos_dados = ordenar_dados(todos_dados)
        salvar_csv(todos_dados)
        mostrar_dados(todos_dados)
        print('\nCSV gerado com sucesso!')
        print('total de registros:', len(todos_dados))
    else:
        print('nenhum dado encontrado')

if __name__ == '__main__':
    main()