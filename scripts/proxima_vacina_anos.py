import pandas as pd
import re
from datetime import date

# Carrega o arquivo CSV como uma tabela
tabela = pd.read_csv("calendario_vacinacao.csv")


def faixa_e_gestante(faixa, semanas_gestacao):
    """Retorna True se a faixa pertence ao grupo de gestantes."""
    faixa = str(faixa).strip()
    return faixa in (
        "Ao saber da gravidez",
        "A partir da 20ª semana gestacional",
        "A partir da 28ª semana gestacional",
    )


def faixa_bate_com_idade(faixa, idade_anos, idade_meses_total):
    """
    Verifica apenas faixas de idade (ignora faixas de gestante).
    Retorna True se o usuario se encaixa naquela faixa.
    """
    faixa = str(faixa).strip()

    # Bebes em meses
    if faixa == "Ao nascer":
        return idade_meses_total == 0

    # "X meses" exato
    match = re.fullmatch(r"(\d+) meses", faixa)
    if match:
        return idade_meses_total == int(match.group(1))

    # "X a Y meses"
    match = re.fullmatch(r"(\d+) a (\d+) meses", faixa)
    if match:
        return int(match.group(1)) <= idade_meses_total <= int(match.group(2))

    # Crianças e adultos em anos

    # "X anos" exato
    match = re.fullmatch(r"(\d+) anos", faixa)
    if match:
        return idade_anos == int(match.group(1))

    # "X a Y anos"
    match = re.fullmatch(r"(\d+) a (\d+) anos", faixa)
    if match:
        return int(match.group(1)) <= idade_anos <= int(match.group(2))

    # "A partir dos X anos" ou "A partir de X anos"
    match = re.search(r"[Aa] partir d[oe]s?\s+(\d+)", faixa)
    if match:
        return idade_anos >= int(match.group(1))

    return False


def faixa_bate_com_gestante(faixa, semanas_gestacao):
    """Verifica apenas faixas de gestante."""
    faixa = str(faixa).strip()

    if faixa == "Ao saber da gravidez":
        return True

    if faixa == "A partir da 20ª semana gestacional":
        return semanas_gestacao >= 20

    if faixa == "A partir da 28ª semana gestacional":
        return semanas_gestacao >= 28

    return False


# Coleta de dados do usuario

nome = input("Digite seu nome: ")

anos = int(input("Digite sua idade (em anos completos): "))

# Para bebes, pede meses tambem
if anos == 0:
    meses_extras = int(input("Quantos meses completos você tem? "))
else:
    meses_extras = 0

idade_em_meses = (anos * 12) + meses_extras

gestante_resposta = input("Você é gestante? (s/n): ").strip().lower()
gestante = gestante_resposta in ("s", "sim")

semanas_gestacao = 0
if gestante:
    semanas_gestacao = int(input("Com quantas semanas de gravidez você está? "))

# Exibicao dos resultados

print()
print("Nome:", nome)
if anos == 0:
    print("Idade:", meses_extras, "meses")
else:
    print("Idade:", anos, "anos")
print()

# Grupo 1: vacinas por idade

print("Vacinas para sua idade:")
print("-" * 45)

encontrou_idade = False

for _, linha in tabela.iterrows():
    faixa = linha["faixa_etaria"]

    if faixa_bate_com_idade(faixa, anos, idade_em_meses):
        encontrou_idade = True
        print("Vacina:", linha["vacina"])
        print("Protege contra:", linha["doencas_evitadas"])

        obs = str(linha.get("observacoes", "")).strip()
        if obs and obs.lower() != "nan":
            print("Observação:", obs)

        print()

if not encontrou_idade:
    print("Nenhuma vacina encontrada para sua idade.")
    print()

print("-" * 45)

# Grupo 2: vacinas por gestante (só aparece se for gestante) 

if gestante:
    print()
    print("Vacinas para gestantes:")
    print("-" * 45)

    encontrou_gestante = False

    for _, linha in tabela.iterrows():
        faixa = linha["faixa_etaria"]

        if faixa_bate_com_gestante(faixa, semanas_gestacao):
            encontrou_gestante = True
            print("Vacina:", linha["vacina"])
            print("Protege contra:", linha["doencas_evitadas"])

            obs = str(linha.get("observacoes", "")).strip()
            if obs and obs.lower() != "nan":
                print("Observação:", obs)

            print()

    if not encontrou_gestante:
        print("Nenhuma vacina encontrada para gestantes.")
        print()

    print("-" * 45)