import streamlit as st
import requests
from io import BytesIO

# Carrega dataframe
df_data = st.session_state["data"]

# Filtros
clubes = df_data["Club"].value_counts().index
club = st.sidebar.selectbox("Clube", clubes)
df_filtered = df_data[df_data["Club"] == club]

# ---- FUNÇÃO PARA VALIDAR URL ----
def validar_url_imagem(url):
    if isinstance(url, str) and url.startswith("http"):
        return url.strip()
    else:
        return "https://via.placeholder.com/70x70.png?text=No+Image"

# Exibe o logo do clube
st.image(validar_url_imagem(df_filtered.iloc[0]["Club Logo"]), width=120)
st.markdown(f"## {club}")

# Converte as colunas Photo e Flag para URLs válidas
df_filtered["Photo"] = df_filtered["Photo"].apply(validar_url_imagem)
df_filtered["Flag"] = df_filtered["Flag"].apply(validar_url_imagem)

columns = ["Age", "Photo", "Flag", "Overall", 'Value', 'Wage','Joined', 'Height', 'Weight', 'Contract Valid Until','Release Clause']

# Exibe o dataframe com barra de progresso e imagens
st.dataframe(
    df_filtered.set_index("Name")[columns],
    column_config={
        "Overall": st.column_config.ProgressColumn(
            "Overall Rating",
            format="%d",
            min_value=0,
            max_value=100
        ),
        "Wage": st.column_config.ProgressColumn(
            "Weekly Wage",
            format="€ %.0f",
            min_value=int(df_filtered["Wage"].min()),
            max_value=int(df_filtered["Wage"].max())
        ),
        "Photo": st.column_config.ImageColumn("Photo"),
        "Flag": st.column_config.ImageColumn("Flag")
    }
)
