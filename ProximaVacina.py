import pandas as pd
from datetime import date, datetime

# Carrega o arquivo CSV como uma tabela
tabela = pd.read_csv("calendario_vacinacao.csv")

# Pede os dados para o usuario
nome = input("Digite seu nome: ")
entrada = input("Digite sua data de nascimento (DD/MM/AAAA): ")

# Converte o texto digitado em uma data de verdade
nascimento = datetime.strptime(entrada, "%d/%m/%Y").date()

# Calcula a idade em anos e meses
hoje = date.today()
anos = hoje.year - nascimento.year
meses = hoje.month - nascimento.month
if hoje.day < nascimento.day:
    meses -= 1
if meses < 0:
    anos -= 1
    meses += 12

# Converte tudo para meses so para facilitar as comparacoes
idade_em_meses = anos * 12 + meses

print("")
print("Nome:", nome)
print("Idade:", anos, "anos e", meses, "meses")
print("")
print("Vacinas recomendadas para sua idade:")
print("-" * 40)

# Percorre cada linha da tabela e verifica se a faixa etaria bate com a idade
encontrou = False

for _, linha in tabela.iterrows():
    faixa = linha["faixa_etaria"]

    # Verifica se a faixa da linha bate com a idade da pessoa
    if faixa == "Ao nascer" and idade_em_meses < 1:
        mostrar = True
    elif faixa == "2 meses" and idade_em_meses == 2:
        mostrar = True
    elif faixa == "3 meses" and idade_em_meses == 3:
        mostrar = True
    elif faixa == "4 meses" and idade_em_meses == 4:
        mostrar = True
    elif faixa == "5 meses" and idade_em_meses == 5:
        mostrar = True
    elif faixa == "6 meses" and idade_em_meses == 6:
        mostrar = True
    elif faixa == "9 meses" and idade_em_meses == 9:
        mostrar = True
    elif faixa == "12 meses" and idade_em_meses == 12:
        mostrar = True
    elif faixa == "15 meses" and idade_em_meses == 15:
        mostrar = True
    elif faixa == "4 anos" and anos == 4:
        mostrar = True
    elif faixa == "5 anos" and anos == 5:
        mostrar = True
    elif faixa == "A partir dos 7 anos" and anos >= 7:
        mostrar = True
    elif faixa == "9 a 14 anos" and 9 <= anos <= 14:
        mostrar = True
    elif faixa == "10 a 14 anos" and 10 <= anos <= 14:
        mostrar = True
    elif faixa == "11 a 14 anos" and 11 <= anos <= 14:
        mostrar = True
    elif faixa == "10 a 24 anos" and 10 <= anos <= 24:
        mostrar = True
    elif faixa == "25 a 59 anos" and 25 <= anos <= 59:
        mostrar = True
    elif faixa == "A partir dos 60 anos" and anos >= 60:
        mostrar = True
    else:
        mostrar = False

    # Se a faixa bateu, mostra a vacina
    if mostrar:
        encontrou = True
        print(linha["vacina"])
        print("Protege contra:", linha["doencas_evitadas"])
        print("")

if not encontrou:
    print("Nenhuma vacina encontrada para sua idade.")