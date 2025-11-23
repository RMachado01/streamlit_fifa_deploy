import streamlit as st
import pandas as pd

# Configurações da página
st.set_page_config(
    page_title="Clubes",
    layout="wide"
)

# ---- CARREGA O DATAFRAME ----
# Uso o dataframe que foi carregado e tratado no app.py
df_data = st.session_state["data"]

# Lista de clubes para filtro
clubes = df_data["Club"].value_counts().index
club = st.sidebar.selectbox("Clube", clubes)

# Filtra os dados do clube selecionado
df_filtered = df_data[df_data["Club"] == club].copy()

# ---- EXIBE O LOGO DO CLUBE ----
# Para exibir a primeira imagem como referência
url_logo = df_filtered.iloc[0]["Club Logo"].strip()
st.image(url_logo, width=80)

# Nome do clube
st.markdown(f"## {club}")

# ---- DEFINIÇÃO DAS COLUNAS ----
columns = ["Age", "Photo", "Flag", "Overall", "Value", "Wage", "Joined", 
           "Height", "Weight", "Contract Valid Until", "Release Clause"]

# ---- GARANTE QUE AS COLUNAS DE IMAGEM SÃO STRINGS LIMPAS ----
# Isso evita problemas com URLs quebradas ou espaços extras
df_filtered["Photo"] = df_filtered["Photo"].astype(str).str.strip()
df_filtered["Flag"] = df_filtered["Flag"].astype(str).str.strip()

# ---- EXIBE O DATAFRAME COM CONFIGURAÇÃO DE COLUNAS ----
st.dataframe(
    df_filtered.set_index("Name")[columns],
    column_config={

        # Barra de progresso representando o rating geral do jogador
        "Overall": st.column_config.ProgressColumn(
            "Overall Rating",     # Nome exibido na coluna
            format="%d",          # Exibe número inteiro
            min_value=0,          # Valor mínimo da barra
            max_value=100         # Valor máximo da barra (escala do FIFA)
        ),

        # Barra de progresso representando o salário semanal
        "Wage": st.column_config.ProgressColumn(
            "Weekly Wage",
            format="€ %.0f",
            min_value=int(df_filtered["Wage"].min()),
            max_value=int(df_filtered["Wage"].max())
        ),

        # Exibição das imagens diretamente via URL
        "Photo": st.column_config.ImageColumn("Photo"),
        "Flag": st.column_config.ImageColumn("Flag")
    }
)
