from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


def _configurar_driver() -> webdriver.Chrome:
    opcoes = Options()
    for arg in ["--headless", "--no-sandbox", "--disable-gpu", "--window-size=1920,1080"]:
        opcoes.add_argument(arg)
    return webdriver.Chrome(options=opcoes)


def buscar_postos_vacinacao(municipio: str, uf: str = "SP") -> list[dict]:
    driver = _configurar_driver()
    resultados = []
    url = "https://cnes.datasus.gov.br/pages/estabelecimentos/consulta.jsp"

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 15)

        # 1 — Seleciona UF
        select_uf = Select(wait.until(EC.presence_of_element_located((By.ID, "estadoId"))))
        select_uf.select_by_visible_text(uf.upper())

        # 2 — Aguarda município habilitar
        wait.until(EC.element_to_be_clickable((By.ID, "municipioId")))
        select_mun = Select(driver.find_element(By.ID, "municipioId"))

        # 3 — Busca aproximada pelo nome do município
        for option in select_mun.options:
            if municipio.upper() in option.text.upper():
                select_mun.select_by_visible_text(option.text)
                break

        # 4 — Submete o formulário
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # 5 — Coleta resultados
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody tr")))
        linhas = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

        for linha in linhas[:8]:
            cols = linha.find_elements(By.TAG_NAME, "td")
            if len(cols) >= 4:
                resultados.append({
                    "nome": cols[1].text.strip(),
                    "tipo": cols[3].text.strip(),
                    "endereco": cols[4].text.strip() if len(cols) > 4 else "Consulte o site",
                })

    except Exception as e:
        print(f"Erro no scraping: {e}")
    finally:
        driver.quit()

    return resultados
