import streamlit as st
import requests
from io import BytesIO

# Configurações da página da segunda aba (Players)
st.set_page_config(
    page_title="Players",
    layout="wide"
)

# Função para baixar a imagem e retornar bytes para o Streamlit
def url_para_bytes(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}  # necessário para alguns sites bloquearem bots
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        return BytesIO(response.content)
    except:
        # Placeholder caso a imagem não carregue
        return BytesIO(requests.get("https://via.placeholder.com/70x70.png?text=No+Image").content)

# Carrega o dataframe da sessão
df_data = st.session_state["data"]

# Filtro de clubes
clubes = df_data["Club"].value_counts().index
club = st.sidebar.selectbox("Clube", clubes)

# Filtra jogadores do clube
df_players = df_data[df_data["Club"] == club]
players = df_players["Name"].value_counts().index
player = st.sidebar.selectbox("Jogador", players)

# Carrega os dados do jogador
player_stats = df_data[df_data["Name"] == player].iloc[0]

# ---- EXIBE A FOTO DO JOGADOR ----
url_foto = player_stats["Photo"]
st.image(url_para_bytes(url_foto), width=70)

# Nome do jogador
st.title(player_stats["Name"])

# Informações básicas
st.markdown(f"**Clube:** {player_stats['Club']}")
st.markdown(f"**Posição:** {player_stats['Position']}")

col1, col2, col3, col4 = st.columns(4)
col1.markdown(f"**Idade:** {player_stats['Age']}")
col2.markdown(f"**Altura:** {player_stats['Height']} cm")
col3.markdown(f"**Peso:** {player_stats['Weight']} kg")

st.divider()

# Overall
st.subheader(f"Overall {player_stats['Overall']}")
st.progress(int(player_stats["Overall"]))

# Valores financeiros
col1, col2, col3, col4 = st.columns(4)
col1.metric("Valor bruto", f"€ {player_stats['Value']:,}")
col2.metric("Remuneração semanal", f"€ {player_stats['Wage']:,}")
col3.metric("Valor de mercado", f"€ {player_stats['Release Clause']:,}")
