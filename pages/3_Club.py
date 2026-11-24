import streamlit as st

from src.estado import dados_fifa

st.set_page_config(
    page_title="Clubes",
    layout="wide"
)

df_data = dados_fifa()

# Filtro de clube
clubes = df_data["Club"].value_counts().index
club = st.sidebar.selectbox("Clube", clubes)
df_filtered = df_data[df_data["Club"] == club].copy()

# Logo do clube
url_logo = df_filtered.iloc[0].get("Club Logo", "")
if url_logo.startswith("http"):
    st.image(url_logo, width=120)
else:
    st.image("assets/no_image.png", width=120)

# Nome do clube
st.markdown(f"## {club}")

columns = ["Age", "Photo", "Flag", "Overall", 'Value', 'Wage', 'Joined', 'Height', 'Weight', 'Contract Valid Until', 'Release Clause']

# Sem URL válida, deixo vazio (a tabela mostra a célula em branco em vez de quebrar)
for coluna in ["Photo", "Flag"]:
    df_filtered[coluna] = df_filtered[coluna].where(df_filtered[coluna].str.startswith("http"), None)

# column_config transforma URL em imagem e número em formato legível
st.dataframe(
    df_filtered.set_index("Name")[columns],
    column_config={
        "Photo": st.column_config.ImageColumn("Foto"),
        "Flag": st.column_config.ImageColumn("País"),
        "Age": "Idade",
        "Overall": st.column_config.ProgressColumn("Overall", min_value=0, max_value=100, format="%d"),
        "Value": st.column_config.NumberColumn("Valor (€)", format="localized"),
        "Wage": st.column_config.NumberColumn("Salário/semana (€)", format="localized"),
        "Release Clause": st.column_config.NumberColumn("Multa (€)", format="localized"),
        "Joined": "Chegou em",
        "Height": st.column_config.NumberColumn("Altura (cm)"),
        "Weight": st.column_config.NumberColumn("Peso (kg)"),
        "Contract Valid Until": st.column_config.NumberColumn("Contrato até", format="%d"),
    },
)
