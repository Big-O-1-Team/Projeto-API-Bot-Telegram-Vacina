from urllib.parse import urlencode

_BASE_URL = "https://www.google.com/maps/dir/?api=1&"


def gerar_link_rota(ubs_info: dict) -> str:
    destino = _extrair_destino(ubs_info)
    if not destino:
        return ""
    return _BASE_URL + urlencode({"destination": destino})


def _extrair_destino(ubs_info: dict) -> str:
    lat = ubs_info.get("latitude")
    lon = ubs_info.get("longitude")
    if lat is not None and lon is not None:
        return f"{lat},{lon}"
    return _destino_por_texto(ubs_info)


def _destino_por_texto(ubs_info: dict) -> str:
    campos = ["nome", "endereco", "cidade"]
    partes = [str(ubs_info.get(k, "")).strip() for k in campos]
    return ", ".join([p for p in partes if p])
