from urlib.parse import quote_plus
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def cria_driver(headless: bool = True) -> webdriver.Chrome:
  options = Options()
  if headless:
      options.add_argument('--headless=new')
  options.add_argument('--window-size=1366, 900')
  options.add_argument('--disable-gpu')
  options.add_argument('--no-sandbox')
  return webdriver.Chrome(Options=options)

def busca_no_maps(local: str) ->dict:
  query = f'postos de vacinação em {local}'.strip()
  url = f'https://www.google.com/maps/search/{quote_plus(query)}'
  driver = cria_driver(headless=True)
  wait = WebDriverWait(driver, 15)
  try:
      driver.get(url)
      wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
      titulo = ''
      endereco = ''
      try:
          titulo = wait.until(
              EC.presence_of_element_located((By.CSS_SELECTOR, 'h1'))
          ).text.strip()
      except Exception:
          pass
      try:
          endereco = driver.find_element(
              By.CSS_SELECTOR, 'button[data-item-id='address']'
          ).text.strip()
      except Exception:
        pass
      return {
          'query': query,
          'titulo': titulo,
          'endereco': endereco,
          'url': driver.current_url,
      }
  finally:
      driver.quit()
