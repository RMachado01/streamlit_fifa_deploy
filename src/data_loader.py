import pandas as pd
from datetime import datetime
from src.cleaning import converter_valor   # Importo minha função de conversão de valores
import re


# ------------------------------------------------------------
# Função para converter alturas que vêm no padrão do FIFA:
# Exemplos possíveis no dataset:
#   5'11"   |  6'2  |  5′11″  |  181cm
#
# O objetivo é transformar tudo em centímetros (int).
# ------------------------------------------------------------
def convert_height(h):

    # Converto para string e removo espaços desnecessários
    h = str(h).strip()

    # Caso já venha no formato “181cm”, apenas removo o sufixo
    if "cm" in h.lower():
        return int(h.lower().replace("cm", "").strip())

    # Padrão para capturar "pés" e "polegadas" mesmo com símbolos diferentes
    match = re.match(r"(\d+)[^\d]+(\d+)", h)

    # Caso o formato esteja muito fora do padrão, retorno NaN
    if not match:
        return None

    ft, inch = match.groups()

    # Conversão real → pés/ft e polegadas/inch para centímetros
    return round(int(ft) * 30.48 + int(inch) * 2.54)



# ------------------------------------------------------------
# Função para converter pesos que vêm no padrão:
#   "150lbs", "150 lbs", "72kg", "72 kg"
#
# Tudo vira quilogramas (int).
# ------------------------------------------------------------
def convert_weight(w):

    # Converto sempre para string minúscula
    w = str(w).strip().lower()

    # Caso já esteja em kg, só removo o texto
    if "kg" in w:
        return int(w.replace("kg", "").strip())

    # Caso esteja em libras (padrão FIFA)
    if "lb" in w:
        num = re.sub(r"[^\d]", "", w)  # remove caracteres não numéricos
        return round(int(num) * 0.453592)

    # Valores muito ruins ou vazios viram None
    return None



# ------------------------------------------------------------
# Função principal que carrega todo o dataset do FIFA,
# faz as limpezas necessárias e retorna um dataframe pronto
# para uso em todas as páginas.
# ------------------------------------------------------------
def load_fifa_data():

    # Carrego meu arquivo já limpo (oficial do projeto)
    df = pd.read_csv("Data/CLEAN_FIFA2023_offcial_data.csv", index_col=0)

    # A coluna de fotos às vezes vem com lixo → padronizo como texto limpo
    df["Photo"] = df["Photo"].astype(str).str.strip()
    df["Flag"] = df["Flag"].astype(str).str.strip()

    # Converto ano do contrato para númerico (quem estiver com erro vira NaN)
    df["Contract Valid Until"] = pd.to_numeric(df["Contract Valid Until"], errors="coerce")

    # Removo jogadores com contrato vencido
    df = df[df["Contract Valid Until"] >= datetime.today().year]

    # Aplico conversão de altura e peso
    df["Height"] = df["Height"].apply(convert_height)
    df["Weight"] = df["Weight"].apply(convert_weight)

    # --------------------------------------------------------
    # Função interna para tratar valores monetários do FIFA:
    #   "€10.5M" → 10500000
    #   "€300K"  →   300000
    #   "€0"     →        0
    # --------------------------------------------------------
    def money_to_number(v):

        # Se estiver vazio → vira 0
        if pd.isna(v):
            return 0

        v = str(v).replace("€", "").strip()

        if v == "":
            return 0

        # Milhões (“10.5M”)
        if v.endswith("M"):
            return int(float(v[:-1]) * 1_000_000)

        # Milhares (“300K”)
        if v.endswith("K"):
            return int(float(v[:-1]) * 1_000)

        # Número puro
        try:
            return int(float(v))
        except:
            return 0

    # Agora aplico nas 3 colunas de valores
    df["Value"] = df["Value"].apply(money_to_number)
    df["Wage"] = df["Wage"].apply(money_to_number)
    df["Release Clause"] = df["Release Clause"].apply(money_to_number)

    # Removo jogadores com valor zero (dados ruins)
    df = df[df["Value"] > 0]

    # Ordeno pela nota geral (Overall)
    df = df.sort_values(by="Overall", ascending=False)

    return df
