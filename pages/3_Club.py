import streamlit as st

st.set_page_config(
    page_title="Clubes",
    layout="wide"
)

df_data = st.session_state["data"]

# Filtro de clube
clubes = df_data["Club"].value_counts().index
club = st.sidebar.selectbox("Clube", clubes)
df_filtered = df_data[df_data["Club"] == club]

# Logo do clube
url_logo = df_filtered.iloc[0].get("Club Logo", "")
if url_logo.startswith("http"):
    st.image(url_logo, width=120)
else:
    st.image("assets/no_image.png", width=120)

# Nome do clube
st.markdown(f"## {club}")

columns = ["Age", "Photo", "Flag", "Overall", 'Value', 'Wage', 'Joined', 'Height', 'Weight', 'Contract Valid Until', 'Release Clause']

# Adicionando colunas de fallback para imagens
df_filtered["Photo"] = df_filtered["Photo"].apply(lambda x: x if str(x).startswith("http") else "assets/no_image.png")
df_filtered["Flag"] = df_filtered["Flag"].apply(lambda x: x if str(x).startswith("http") else "assets/no_image.png")

# Dataframe
st.dataframe(
    df_filtered.set_index("Name")[columns]
)
