import streamlit as st

# Configurações da página
st.set_page_config(
    page_title="Clubes",
    layout="wide"
)

# Dataframe carregado da primeira página
df_data = st.session_state["data"]

# Lista de clubes
clubes = df_data["Club"].value_counts().index
club = st.sidebar.selectbox("Clube", clubes)

# Filtra os dados do clube
df_filtered = df_data[df_data["Club"] == club]

# ---- LOGO DO CLUBE ----
# URL direto no st.image()
st.image(df_filtered.iloc[0]["Club Logo"], width=50)

# Nome do clube
st.markdown(f"## {club}")

# Colunas a exibir
columns = ["Age", "Photo", "Flag", "Overall", 'Value', 'Wage','Joined', 'Height', 'Weight', 'Contract Valid Until','Release Clause']

# Dataframe com índice no nome do jogador
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
