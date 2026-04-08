from selenium import webdriver
from selenium.webdriver.common.by import By
import time


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



