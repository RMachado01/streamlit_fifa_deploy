import streamlit as st

# Configurações da página
st.set_page_config(
    page_title="Players",
    layout="wide"
)

# Carrega o dataframe da sessão
df_data = st.session_state["data"]

# ---- FILTROS ----
clubes = df_data["Club"].value_counts().index
club = st.sidebar.selectbox("Clube", clubes)

df_players = df_data[df_data["Club"] == club]
players = df_players["Name"].value_counts().index
player = st.sidebar.selectbox("Jogador", players)

player_stats = df_data[df_data["Name"] == player].iloc[0]

# ---- FOTO DO JOGADOR ----
url_foto = player_stats.get("Photo", "")

# Se a URL estiver presente, usa; caso contrário, usa placeholder local
if url_foto.startswith("http"):
    st.image(url_foto, width=70)
else:
    st.image("assets/no_image.png", width=70)

# Nome do jogador
st.title(player_stats["Name"])

# Informações básicas
st.markdown(f"**Clube:** {player_stats['Club']}")
st.markdown(f"**Posição:** {player_stats['Position']}")

col1, col2, col3, col4 = st.columns(4)
col1.markdown(f"**Idade:** {player_stats['Age']}")
col2.markdown(f"**Altura:** {player_stats['Height']}")
col3.markdown(f"**Peso:** {player_stats['Weight']}")

st.divider()

# Overall
st.subheader(f"Overall {player_stats['Overall']}")
st.progress(int(player_stats["Overall"]))

# Valores financeiros
col1, col2, col3, col4 = st.columns(4)
col1.metric("Valor bruto", f"€ {player_stats['Value']:,}".replace(",", "."))
col2.metric("Remuneração semanal", f"€ {player_stats['Wage']:,}".replace(",", "."))
col3.metric("Valor de mercado", f"€ {player_stats['Release Clause']:,}".replace(",", "."))
