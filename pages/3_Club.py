import streamlit as st
import requests
from io import BytesIO

# Configurações da página
st.set_page_config(
    page_title="Clubes",
    layout="wide"
)

# Função para baixar a imagem e retornar bytes
def url_para_bytes(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        return BytesIO(response.content)
    except:
        return BytesIO(requests.get("https://via.placeholder.com/70x70.png?text=No+Image").content)

# Carrega o dataframe da sessão
df_data = st.session_state["data"]

# Lista de clubes
clubes = df_data["Club"].value_counts().index
club = st.sidebar.selectbox("Clube", clubes)

# Filtra os dados do clube
df_filtered = df_data[df_data["Club"] == club]

# ---- EXIBE O LOGO DO CLUBE ----
url_logo = df_filtered.iloc[0]["Club Logo"]
st.image(url_para_bytes(url_logo), width=120)

# Nome do clube
st.markdown(f"## {club}")

# Colunas do dataframe
columns = ["Age", "Photo", "Flag", "Overall", 'Value', 'Wage','Joined', 'Height', 'Weight', 'Contract Valid Until','Release Clause']

# Cria colunas base64 para fotos e bandeiras
df_filtered["Photo_bytes"] = df_filtered["Photo"].apply(url_para_bytes)
df_filtered["Flag_bytes"] = df_filtered["Flag"].apply(url_para_bytes)

# Exibe o dataframe
st.dataframe(
    df_filtered.set_index("Name")[columns + ["Photo_bytes", "Flag_bytes"]],
    column_config={
        "Overall": st.column_config.ProgressColumn("Overall Rating", format="%d", min_value=0, max_value=100),
        "Wage": st.column_config.ProgressColumn(
            "Weekly Wage", 
            format="€ %.0f",
            min_value=int(df_filtered["Wage"].min()),
            max_value=int(df_filtered["Wage"].max())
        ),
        "Photo_bytes": st.column_config.ImageColumn("Foto"),
        "Flag_bytes": st.column_config.ImageColumn("Bandeira")
    }
)
