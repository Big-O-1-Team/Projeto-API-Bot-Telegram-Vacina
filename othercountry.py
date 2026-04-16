from selenium import webdriver
from selenium.webdriver.common.by import By
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

link = getLinkCountry('Barbados')
nav.get(link)
tabela_de_infos = nav.find_element(By.XPATH, '//*[@id="dest-vm-a"]')
elementos1 = tabela_de_infos.find_elements(By.TAG_NAME, 'clinician-disease')
elementos2 = tabela_de_infos.find_elements(By.TAG_NAME, 'clinician-recomendations')
elementos3 = tabela_de_infos.find_elements(By.TAG_NAME, 'clinician-guidance')
tabela = []
tabela.append(elementos1, elementos2, elementos3)
def CriarCSVCountry(tabela):
    df = pd.DataFrame(tabela, columns=["Vaccines for disease","Recommendations", "Clinical Guidance for Healthcare providers", ])
    CSVFile = df.to_csv("CountryRequirements.csv", index=False)
    display(df)
    return CSVFile
CriarCSVCountry(tabela)


 