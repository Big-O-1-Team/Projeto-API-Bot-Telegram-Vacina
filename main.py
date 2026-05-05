import scripts.createCSV as createCSV
from scripts.scrappingselenium import AcessarInformacoes
from scripts.telegramMessages import iniciarBOT

def main():
    # Scrapping
    print("Main pronta")
    dados = AcessarInformacoes()
    # Criação do Arquivo CSV
    createCSV.CriarCSV(dados)
    # Bot
    iniciarBOT()
if __name__ == "__main__":
    main()