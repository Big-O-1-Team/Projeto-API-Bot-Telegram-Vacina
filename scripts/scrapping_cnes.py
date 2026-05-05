from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time

def cria_driver(headless: bool = True) -> webdriver.Chrome:
    options = Options()
    if headless:
        options.add_argument('headless=new')
        options.add_argument('window-size=1366,900')
        options.add_argument('disable-gpu')
        options.add_argument('no-sandbox')
    return webdriver.Chrome(options=options)

def UBSPublicOrNo(name: str) -> bool:
    driver = webdriver.Chrome()
    resultados = []
    url = "https://cnes.datasus.gov.br/pages/estabelecimentos/consulta.jsp"
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 15)
        wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/main/div/div[2]/div/form[1]')))
        entrada = driver.find_element(By.XPATH,'//*[@id="pesquisaValue"]')
        entrada.send_keys(name)
        entrada.send_keys(Keys.ENTER)
        time.sleep(1)
        try:
            tabela = '.table.table-condensed.table-bordered.table-striped.ng-scope.ng-table'
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, tabela)))
            time.sleep(3)
            UBSAtendeSUs = driver.find_element(By.CSS_SELECTOR, "[data-title-text='Atende SUS']").text.strip().lower()
            print(repr(UBSAtendeSUs))
            if UBSAtendeSUs in 'sim':
                print('True')
                return True
            else:
                print('False')
                return False
        except:
            print('Não foi encontrado o elemento!')
            pass
    except Exception as e:
        print(f"Erro no Scraping: {e}")
