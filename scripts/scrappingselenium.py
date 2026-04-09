from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re

nav = webdriver.Chrome()
dominioGoverno = 'https://www.gov.br'
siteVacinacao = dominioGoverno + '/saude/pt-br/vacinacao/calendario'
nav.get(siteVacinacao)

#Aceitar Cookies
try:
    cookieButton = nav.find_element(By.XPATH, "/html/body/div[5]/div/div/div/div/div[2]/button[3]")
    cookieButton.click()
except Exception as e:
    print(f"Não foi possível Aceitar os Cookies \n Ocorreu o problema: {e}")
    pass

def getHrefPCategoria():
    hrefCategoria = f"https://www.gov.br/saude/pt-br/vacinacao/calendario"
    return hrefCategoria

id = {"crianca": 1, 
      "adolescente": 2, 
      "adulto": 3, 
      "idoso":4,  
      "gestante": 5
      }
dados = []
#Acessar Informações
def AcessarInformacoes():
    for i, num in id.items():
        print(f"A Categoria é {i}")
        link = getHrefPCategoria()
        nav.get(link)
        #Acessar Label da categoria
        try:
            container = nav.find_element(By.ID, i)
            #Tentar pegar descrição da Categoria
            try:
                description = nav.find_element(By.CSS_SELECTOR, "p.calendario-header__descricao__texto")
                print(description)
            except:
                print("Não foi possível pegar a descrição")
            
            #Tentar pegar informações primeiro e se gundo nivel
            try:
                servicos = container.find_elements(By.CSS_SELECTOR, "ul.servicos > li")
                for servs in servicos:
                    #primeiro nivel
                    try:
                        primeiroServ = servs.find_element(By.CSS_SELECTOR, "a.servico-primeiro-nivel")
                        periodo = nav.execute_script("return arguments[0].innerText;", primeiroServ)
                        print(periodo.strip())
                    except:
                        pass
                    #segundo nivel
                    try:
                        segundoServ = servs.find_elements(By.CSS_SELECTOR, "ul.servicos-segundo-nivel > li")
                        for item in segundoServ:
                            tituloVacina = item.find_element(By.CSS_SELECTOR, "p.vacina__titulo")
                            deoncasEvitadas = item.find_element(By.CSS_SELECTOR, "a.vacina__link")
                            texto_vacina = nav.execute_script("return arguments[0].innerText;", tituloVacina)
                            texto_doenca = nav.execute_script("return arguments[0].innerText;", deoncasEvitadas)
                            texto_vacina = ' '.join(texto_vacina.split())
                            texto_doenca = ' '.join(texto_vacina.split())
                            print(f"-{texto_vacina.strip()}")
                            print(f"-{texto_doenca.strip()}")
                            dados.append((i, periodo,  texto_vacina, texto_doenca))
                    except:
                        pass
            except:
                print("Não foi possível pegar Servicos")
        except Exception as e:
            print(f"Ocorreu o erro {e}")
        time.sleep(5)
        print("_" * 60)
    return dados



def getLinkVacina(name: str) -> str:
    name = name.upper()
    if 'BCG' in name:
        return 'https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/b/bcg'
    elif 'HEPATITE B' in name:
        return 'https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/h/hepatites-virais/hepatite-b'
    elif 'HEPATITE A' in name:
        return 'https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/h/hepatites-virais/hepatite-a'
    elif 'PENTA' in name:
        return 'https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/p/pentavalente'
    elif 'POLIOMELITE' in name:
        return 'https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/p/poliomielite'
    elif 'ROTAVIRUS' in name or 'ROTAVÍRUS' in name:
        return 'https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/r/rotavirus'
    elif 'MENINGITE' in name:
        return 'https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/m/meningite'
    elif 'FEBRE AMARELA' in name:
        return 'https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/f/febre-amarela'
    elif 'TRIPLICE VIRAL' in name or 'TRÍPLICE VIRAL' in name or 'TRÍPLICE VIRAL SCR' in name:
        return 'https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/t/triplice-viral'
    elif 'DTPA' in name:
        return 'https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/d/dtpa'
    elif 'DTP' in name:
        return 'https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/d/dtp'
    elif 'VARICELA' in name or 'CATAPORA' in name:
        return 'https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/c/catapora-varicela'
    elif 'HPV' in name or 'HPV4' in name:
        return 'https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/h/hpv'
    elif 'COVID' in name:
        return 'https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/c/covid-19'
    elif ' DT ' in name or name.endswith('DT'):
        return 'https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/d/dt'
    elif 'INFLUENZA' in name or 'GRIPE' in name:
        return 'https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/i/influenza'
    elif 'PNEUMO' in name:
        return 'https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/p/pneumonia'
    else:
        return None
def scrappingVacinaInfoIndividual(name):
    link = getLinkVacina(name)
    nav.get(link)
    title = nav.find_element(By.CSS_SELECTOR, ".outstanding-title").text
    primeiraparte = nav.find_element(By.CSS_SELECTOR, ".column.col-md-12 ")
    reacoes = nav.find_elements(By.CSS_SELECTOR, ".xxmsonormal")
    texto = title +'\n'
    for xxmnsonormal in reacoes:
        texto = xxmnsonormal.text + '\n\n' + texto
    print(texto + '\n')
    mainElement = nav.find_element(By.TAG_NAME, "main").text
    return mainElement

scrappingVacinaInfoIndividual('HPV')
