import csv
import math

ARQUIVO_UBS = "ubs.csv"

# Estados da conversa
ESCOLHA, AGUARDANDO_LOCALIZACAO, AGUARDANDO_ENDERECO = range(3)


# Calcula a distância em km entre dois pontos geográficos usando a fórmula de Haversine
def calcular_distancia(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return R * 2 * math.asin(math.sqrt(a))


# Lê o CSV e retorna a UBS com menor distância em relação às coordenadas fornecidas
def ubs_mais_proxima(lat, lon):
    mais_proxima = None
    menor_distancia = float("inf")

    with open(ARQUIVO_UBS, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for linha in reader:
            dist = calcular_distancia(lat, lon, float(linha["lat"]), float(linha["lng"]))
            if dist < menor_distancia:
                menor_distancia = dist
                mais_proxima = dict(linha)
                mais_proxima["distancia_km"] = round(menor_distancia, 2)

    return mais_proxima


# Pergunta ao usuário se a busca é para ele ou para outra pessoa
async def start_ubs(update, context):
    teclado = [
        [KeyboardButton("Para mim")],
        [KeyboardButton("Para outra pessoa")],
    ]
    markup = ReplyKeyboardMarkup(teclado, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text(
        "A busca e para voce ou para outra pessoa?",
        reply_markup=markup,
    )
    return ESCOLHA


# Processa a escolha e direciona para o fluxo correto
async def tratar_escolha(update, context):
    texto = update.message.text

    # Se for para o proprio usuario, pede a localizacao via botao nativo do Telegram
    if "Para mim" in texto:
        botao = KeyboardButton("Enviar minha localizacao", request_location=True)
        markup = ReplyKeyboardMarkup([[botao]], resize_keyboard=True, one_time_keyboard=True)
        await update.message.reply_text(
            "Clique no botao abaixo para enviar sua localizacao.",
            reply_markup=markup,
        )
        return AGUARDANDO_LOCALIZACAO

    # Se for para outra pessoa, pede o endereco em texto
    else:
        await update.message.reply_text(
            "Digite o endereco completo. Exemplo: Rua das Flores 123, Taubate, SP",
            reply_markup=ReplyKeyboardRemove(),
        )
        return AGUARDANDO_ENDERECO


# Recebe a localizacao enviada pelo Telegram e busca a UBS mais proxima
async def tratar_localizacao(update, context):
    loc = update.message.location
    await update.message.reply_text("Buscando...", reply_markup=ReplyKeyboardRemove())

    ubs = ubs_mais_proxima(loc.latitude, loc.longitude)

    if ubs:
        await update.message.reply_text(
            f"UBS mais proxima: {ubs['nome']}\n"
            f"Cidade: {ubs['cidade']} - {ubs['estado']}\n"
            f"Distancia: {ubs['distancia_km']} km"
        )
    else:
        await update.message.reply_text("Nenhuma UBS encontrada no cadastro.")

    return ConversationHandler.END


# Informa que busca por endereco nao e suportada sem API externa
async def tratar_endereco(update, context):
    await update.message.reply_text(
        "Busca por endereco nao disponivel sem conexao externa.\n"
        "Use /start e escolha a opcao de localizacao.",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END