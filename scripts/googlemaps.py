from pathlib import Path
from urllib.parse import quote_plus
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def cria_driver(headless: bool = True) -> webdriver.Chrome:
    options = Options()
    if headless:
        options.add_argument('headless=new')
        options.add_argument('window-size=1366,900')
        options.add_argument('disable-gpu')
        options.add_argument('no-sandbox')
    return webdriver.Chrome(options=options)

def salvar_csv(resultados, arquivo='ubs_próximas.csv'):
    df = pd.DataFrame(resultados)
    df.to_csv(arquivo, index=False, encoding='utf-8-sig')
    return arquivo

def busca_no_maps(local: str, limite: int = 5):
    query = f'UBS perto de {local}'.strip()
    url = f'https://www.google.com/maps/search/{quote_plus(query)}'
    driver = cria_driver(headless=True)
    wait = WebDriverWait(driver, 15)
    resultados = []
    try:
        driver.get(url)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        print('Página carregada')
        cards = driver.find_elements(By.CSS_SELECTOR, 'div[role="article"]')
        print('busacando elementos...')
        print('Qtd de resultados', len(cards))
        for card in cards:
            nome = ''
            endereco = ''
            try:
                nome = card.find_element(By.CSS_SELECTOR, 'h3').text.strip()
            except Exception:
                pass
            try:
                endereco = card.text.strip()
            except Exception:
                pass
            if nome or endereco:
                resultados.append({'consulta': query, 'nome': nome, 'endereco': endereco, 'url': driver.current_url})
            if len(resultados) >= limite:
                break
        if not resultados:
            resultados.append({'consulta': query, 'nome': 'Nenhuma UBS encontrada', 'endereco': '', 'url': driver.current_url})
    finally:
        driver.quit()
    salvar_csv(resultados, 'ubs_próximas.csv')
    return resultados

def formatar_resultados(resultados):
    texto = ''
    for i, item in enumerate(resultados, start=1):
        nome = item.get('nome', '').strip() or 'sem nome identificado'
        endereco = item.get('endereco', '').strip() or 'endereço não identificado'
        texto += f'{i}. {nome}\n{endereco}\n\n'
    return texto.strip()

if __name__ == '__main__':
    print('Testando scrapping.../n')
    resultados = busca_no_maps('São José dos Campos SP', limite=5)
    print('resultados brutos:')
    print(resultados)
    print('/n Resultados Formatados: /n')
    print(formatar_resultados(resultados))
