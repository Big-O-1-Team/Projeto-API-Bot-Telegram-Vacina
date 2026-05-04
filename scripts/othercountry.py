from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import pandas as pd
from IPython.display import display

nav= webdriver.Chrome()

nav.get('https://wwwnc.cdc.gov/travel')

def listCountries():
    lista = []
    for x in range(283):
        country = nav.find_element(By.XPATH, f'//*[@id="thlrdssl-traveler"]/option[{x+1}]')
        lista.append(country.text)
    print(lista)

def getLinkCountry(name):
    name = name.replace(' ', '-')
    name = name.lower()
    link = 'https://wwwnc.cdc.gov/travel/destinations/traveler/none/'+ name
    nav.get(link)
    time.sleep(2)
    return link


listCountries()


def InfoAcessPCountry(country):
    link = getLinkCountry(country)
    link_traduzido = f"https://translate.google.com/translate?sl=auto&tl=pt&u={link}"
    nav.get(link_traduzido)
    time.sleep(20)
    tabela = nav.find_element(By.XPATH, "//*[@id='dest-vm-a']")
    vaccines_for_disease_tb = tabela.find_elements(By.CLASS_NAME, 'clinician-disease')
    recomendantions_tb = tabela.find_elements(By.CLASS_NAME, 'clinician-recomendations')
    guidance_tb = tabela.find_elements(By.CLASS_NAME, 'clinician-guidance')

    vaccine_txt =[x.text for x in vaccines_for_disease_tb]
    recomendations_txt =[x.text for x in recomendantions_tb]
    guidance_txt = [x.text for x in guidance_tb]
    final_table = {"Vacina": vaccine_txt, "Recomendação": recomendations_txt,"Guidance": guidance_txt}

    df = pd.DataFrame(final_table)
    csvFile = df.to_csv("CountryInfo.csv", index= False)
    display(df)



