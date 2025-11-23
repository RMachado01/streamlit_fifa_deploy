import streamlit as st
import requests
from io import BytesIO

# Carrega o dataframe salvo na sessão
df_data = st.session_state["data"]

# Filtros de clube e jogador
clubes = df_data["Club"].value_counts().index
club = st.sidebar.selectbox("Clube", clubes)
df_players = df_data[df_data["Club"] == club]
players = df_players["Name"].value_counts().index
player = st.sidebar.selectbox("Jogador", players)
player_stats = df_players[df_players["Name"] == player].iloc[0]

# ---- FUNÇÃO PARA VALIDAR URL DA IMAGEM ----
def validar_url_imagem(url):
    """
    Retorna a URL se válida, caso contrário retorna placeholder.
    """
    if isinstance(url, str) and url.startswith("http"):
        return url.strip()
    else:
        return "https://via.placeholder.com/70x70.png?text=No+Image"

# Exibe a foto do jogador (com placeholder se URL inválida)
st.image(validar_url_imagem(player_stats["Photo"]), width=70)

# Nome e informações do jogador
st.title(player_stats["Name"])
st.markdown(f"**Clube:** {player_stats['Club']}")
st.markdown(f"**Posição:** {player_stats['Position']}")

col1, col2, col3, col4 = st.columns(4)
col1.markdown(f"**Idade:** {player_stats['Age']}")
col2.markdown(f"**Altura:** {player_stats['Height']} cm")
col3.markdown(f"**Peso:** {player_stats['Weight']} kg")

st.divider()

st.subheader(f"Overall {player_stats['Overall']}")
st.progress(int(player_stats["Overall"]))

col1, col2, col3, col4 = st.columns(4)

def formatar_euro(valor):
    return f"€ {valor:,.0f}".replace(",", ".")

col1.metric(label="Valor bruto", value=formatar_euro(player_stats["Value"]))
col2.metric(label="Remuneração semanal", value=formatar_euro(player_stats["Wage"]))
col3.metric(label="Valor de mercado", value=formatar_euro(player_stats["Release Clause"]))
