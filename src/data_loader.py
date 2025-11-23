import pandas as pd
from datetime import datetime
from io import BytesIO
import requests

# Função auxiliar para converter valores monetários do FIFA
def converter_valor(valor):
    if pd.isna(valor) or valor == "":
        return 0
    valor = str(valor).replace("€", "").strip()
    try:
        if valor.endswith("M"):
            return int(float(valor[:-1]) * 1_000_000)
        elif valor.endswith("K"):
            return int(float(valor[:-1]) * 1_000)
        else:
            return int(float(valor))
    except:
        return 0

# Função auxiliar para converter altura
def converter_altura(altura):
    """
    Converte altura do formato "1,80" ou "1.80" para centímetros.
    """
    if pd.isna(altura):
        return None
    altura = str(altura).replace(",", ".").strip()
    try:
        return int(float(altura) * 100)
    except:
        return None

# Função auxiliar para converter peso
def converter_peso(peso):
    """
    Converte peso para kg, removendo letras e espaços.
    """
    if pd.isna(peso):
        return None
    peso = str(peso).replace("kg", "").strip()
    try:
        return int(float(peso))
    except:
        return None

# Função principal para carregar e limpar os dados do FIFA
def load_fifa_data(csv_path="Data/CLEAN_FIFA2023_offcial_data.csv"):
    # Carrega o CSV
    df = pd.read_csv(csv_path, index_col=0)

    # Padroniza strings
    df["Photo"] = df["Photo"].astype(str).str.strip()
    df["Flag"] = df["Flag"].astype(str).str.strip()
    df["Club Logo"] = df["Club Logo"].astype(str).str.strip()

    # Converte contratos para números e filtra contratos válidos
    df["Contract Valid Until"] = pd.to_numeric(df["Contract Valid Until"], errors="coerce")
    df = df[df["Contract Valid Until"] >= datetime.today().year]

    # Converte valores monetários
    df["Value"] = df["Value"].apply(converter_valor)
    df["Wage"] = df["Wage"].apply(converter_valor)
    df["Release Clause"] = df["Release Clause"].apply(converter_valor)

    # Converte altura e peso
    df["Height"] = df["Height"].apply(converter_altura)
    df["Weight"] = df["Weight"].apply(converter_peso)

    # Remove jogadores sem valor
    df = df[df["Value"] > 0]

    # Ordena por Overall
    df = df.sort_values(by="Overall", ascending=False)

    # Retorna dataframe limpo
    return df
