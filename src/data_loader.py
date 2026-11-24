"""Carrega e limpa o dataset oficial do FIFA 23 (Kaggle).

Tudo o que é conversão de texto pra número fica em funções pequenas e puras,
pra dar pra testar cada uma separada (veja tests/test_data_loader.py).
"""

import re
from pathlib import Path

import pandas as pd

# Caminho do CSV relativo à raiz do projeto, não à pasta de onde o
# streamlit foi chamado. Assim o app abre de qualquer lugar.
CAMINHO_PADRAO = Path(__file__).resolve().parent.parent / "Data" / "FIFA23_official_data.csv"

# O dataset é do FIFA 23, então "contrato ainda válido" é relativo a 2023.
# Antes eu usava o ano atual (datetime.today().year), e isso fazia o app
# perder jogadores a cada ano que passava, até ficar vazio.
ANO_REFERENCIA = 2023


def converter_valor(valor) -> int:
    """Converte '€10.5M', '€300K' ou '€500' em euros inteiros. Vazio vira 0."""
    if pd.isna(valor):
        return 0
    texto = str(valor).replace("€", "").strip().upper()
    if not texto:
        return 0
    multiplicador = 1
    if texto.endswith("M"):
        multiplicador, texto = 1_000_000, texto[:-1]
    elif texto.endswith("K"):
        multiplicador, texto = 1_000, texto[:-1]
    try:
        return int(round(float(texto) * multiplicador))
    except ValueError:
        return 0


def converter_altura(altura) -> int | None:
    """Converte altura pra centímetros.

    Aceita os formatos que aparecem nas versões do dataset:
    '189cm', '1.89', '1,89' e o formato em pés/polegadas "6'2".
    """
    if pd.isna(altura):
        return None
    texto = str(altura).strip().lower()

    pes_polegadas = re.fullmatch(r"(\d+)'(\d+)\"?", texto)
    if pes_polegadas:
        pes, polegadas = map(int, pes_polegadas.groups())
        return round((pes * 12 + polegadas) * 2.54)

    texto = texto.replace("cm", "").replace(",", ".").strip()
    try:
        numero = float(texto)
    except ValueError:
        return None
    # "1.89" está em metros; "189" já está em centímetros
    return round(numero * 100) if numero < 3 else round(numero)


def converter_peso(peso) -> int | None:
    """Converte peso pra kg. Aceita '82kg' e '190lbs'."""
    if pd.isna(peso):
        return None
    texto = str(peso).strip().lower()
    em_libras = texto.endswith("lbs")
    texto = texto.replace("lbs", "").replace("kg", "").strip()
    try:
        numero = float(texto)
    except ValueError:
        return None
    return round(numero * 0.4536) if em_libras else round(numero)


def limpar(df: pd.DataFrame) -> pd.DataFrame:
    """Aplica todas as conversões e filtros num DataFrame cru do FIFA 23."""
    df = df.copy()

    for coluna in ["Photo", "Flag", "Club Logo"]:
        df[coluna] = df[coluna].astype(str).str.strip()

    # Jogador repetido no CSV (mesmo ID) só atrapalha os filtros por nome
    df = df.drop_duplicates(subset="ID")

    df["Contract Valid Until"] = pd.to_numeric(
        df["Contract Valid Until"].astype(str).str[-4:], errors="coerce"
    )
    df = df[df["Contract Valid Until"] >= ANO_REFERENCIA]

    for coluna in ["Value", "Wage", "Release Clause"]:
        df[coluna] = df[coluna].apply(converter_valor)
    df["Height"] = df["Height"].apply(converter_altura)
    df["Weight"] = df["Weight"].apply(converter_peso)

    # A posição vem com HTML do site de origem: '<span class="pos pos25">ST'
    df["Position"] = df["Position"].astype(str).str.replace(r"<[^>]*>", "", regex=True).str.strip()

    df = df[df["Value"] > 0]
    return df.sort_values(by="Overall", ascending=False).set_index("ID")


def load_fifa_data(csv_path: Path | str = CAMINHO_PADRAO) -> pd.DataFrame:
    """Lê o CSV e devolve o DataFrame limpo, ordenado por Overall."""
    return limpar(pd.read_csv(csv_path))
