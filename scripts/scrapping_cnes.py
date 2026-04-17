from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def _configurar_driver():
    opcoes = Options()
    for arg in ["--headless", "--no-sandbox", "--disable-gpu", "--window-size=1920,1080"]:
        opcoes.add_argument(arg)
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opcoes)

def buscar_postos_vacinacao(municipio: str, uf: str = "SP") -> list[dict]:
    driver = _configurar_driver()
    resultados = []
    url = "https://cnes.datasus.gov.br/pages/estabelecimentos/consulta.jsp"

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 15)

        # 1- Seleciona a UF
        select_uf = Select(wait.until(EC.presence_of_element_located((By.ID, "estadoId"))))
        select_uf.select_by_visible_text(uf.upper())

        # 2- Aguarda o campo de município ser habilitado após a UF
        wait.until(lambda d: not d.find_element(By.ID, "municipioId").get_attribute("disabled"))
        
        select_mun = Select(driver.find_element(By.ID, "municipioId"))
        # 3- Busca por aproximação no nome do município
        for option in select_mun.options:
            if municipio.upper() in option.text.upper():
                select_mun.select_by_visible_text(option.text)
                break

        # 4- Clica no botão de busca
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

            # 5- Aguarda a tabela de resultados aparecer
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody tr")))
        linhas = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

        for linha in linhas[:8]: # Limite de 8 para o Telegram
            cols = linha.find_elements(By.TAG_NAME, "td")
            if len(cols) >= 4:
                resultados.append({
                    "nome": cols[1].text.strip(),
                    "tipo": cols[3].text.strip(),
                    "endereco": cols[4].text.strip() if len(cols) > 4 else "Consulte o site"
                })

    except Exception as e:
        print(f"Erro no Scraping: {e}")
    finally:
        driver.quit()
    
    return resultados

def formatar_mensagem_postos(municipio: str, postos: list[dict]) -> str:
    if not postos: return f"❌ Nenhum posto encontrado em {municipio}."
    
    msg = f"💉 *Postos em {municipio}*\n\n"
    for i, p in enumerate(postos, 1):
        msg += f"*{i}. {p['nome']}*\n🏢 {p['tipo']}\n📍 {p['endereco']}\n\n"
    return msg + "🔗 _Fonte: CNES/DATASUS_"
