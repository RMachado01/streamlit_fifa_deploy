import pandas as pd

def converter_valor(valor):
    """Converte valores como '€10.5M' ou '€300K' para números inteiros."""

    # Se for NaN, considero como 0 para não quebrar nada.
    if pd.isna(valor):
        return 0

    # Removo o símbolo do euro e deixo só o número com a letra final.
    valor = str(valor).replace("€", "").strip()

    # Se a string ficar vazia por algum erro, retorno 0.
    if valor == "":
        return 0

    # Caso de valores em milhões, exemplo: "10.5M"
    if valor.endswith("M"):
        try:
            return int(float(valor[:-1]) * 1_000_000)
        except:
            return 0

    # Caso de valores em milhares, exemplo: "300K"
    if valor.endswith("K"):
        try:
            return int(float(valor[:-1]) * 1_000)
        except:
            return 0

    # Caso seja número puro, sem K ou M
    try:
        return int(float(valor))
    except:
        return 0
