import streamlit as st
import requests
from io import BytesIO

# Configurações da página
st.set_page_config(
    page_title="Players",
    layout="wide"
)

# Carrega o dataframe salvo na primeira página
df_data = st.session_state["data"]

# Função para formatar valores em euros
def formatar_euro(valor):
    return f"€ {valor:,.0f}".replace(",", ".")


# ---- FILTRO DE CLUBES ----
clubes = df_data["Club"].value_counts().index
club = st.sidebar.selectbox("Clube", clubes)


# ---- FILTRO DE JOGADORES ----
df_players = df_data[df_data["Club"] == club]
players = df_players["Name"].unique()   # melhor que value_counts()

player = st.sidebar.selectbox("Jogador", players)


# ---- SELEÇÃO DO JOGADOR ----
player_stats = df_players[df_players["Name"] == player].iloc[0]


# ---- FOTO DO JOGADOR ----
url_foto = player_stats["Photo"]
response = requests.get(url_foto, headers={"User-Agent": "Mozilla/5.0"})
img_bytes = BytesIO(response.content)

st.image(img_bytes, width=70)
st.title(player_stats["Name"])


# ---- INFORMAÇÕES ----
st.markdown(f"**Clube:** {player_stats['Club']}")
st.markdown(f"**Posição:** {player_stats['Position']}")

col1, col2, col3 = st.columns(3)
col1.markdown(f"**Idade:** {player_stats['Age']}")
col2.markdown(f"**Altura:** {player_stats['Height']}")
col3.markdown(f"**Peso:** {player_stats['Weight']}")

st.divider()


# ---- OVERALL ----
st.subheader(f"Overall {player_stats['Overall']}")
st.progress(int(player_stats["Overall"]))


# ---- VALORES FINANCEIROS ----
col1, col2, col3 = st.columns(3)

col1.metric("Valor bruto", formatar_euro(player_stats["Value"]))
col2.metric("Salário semanal", formatar_euro(player_stats["Wage"]))
col3.metric("Valor de mercado", formatar_euro(player_stats["Release Clause"]))
