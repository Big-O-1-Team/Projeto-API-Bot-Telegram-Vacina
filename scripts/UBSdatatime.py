import re
from telebot import types
from scripts.scrapping_cnes import buscar_ubs_por_municipio, formatar_mensagem_ubs

MSG_PEDIR_IBGE = (
    "*Busca de UBS por Município*\n\n"
    "Por favor, informe o *código IBGE* do seu município (7 dígitos).\n\n"
    "*Exemplos:*\n"
    "• São José dos Campos: `3549904`\n"
    "• São Paulo: `3550308`"
)

def iniciar_fluxo_ubs(bot, chat_id: int) -> None:
    """Inicia o diálogo de busca de UBS."""
    msg = bot.send_message(chat_id, MSG_PEDIR_IBGE, parse_mode='Markdown')
    bot.register_next_step_handler(msg, lambda m: processar_busca_ubs(bot, m))

def processar_busca_ubs(bot, message) -> None:
    """Valida o código e entrega o resultado final."""
    codigo = message.text.strip()

    if not re.fullmatch(r'\d{7}', codigo):
        bot.send_message(message.chat.id, "⚠️ Código inválido. Use 7 números.")
        return

    bot.send_message(message.chat.id, "⏳ Consultando base do CNES...")

    try:
        lista_ubs = buscar_ubs_por_municipio(codigo)
        resposta = formatar_mensagem_ubs(lista_ubs)
        bot.send_message(message.chat.id, resposta, parse_mode='Markdown', disable_web_page_preview=True)
    except Exception as erro:
        bot.send_message(message.chat.id, "Erro ao conectar com o serviço.")
        print(f"[ERRO]: {erro}")
