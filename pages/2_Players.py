import streamlit as st
import pandas as pd

# Configurações da página
st.set_page_config(
    page_title="Players",
    layout="wide"
)

# Carrega o dataframe que foi salvo na primeira página dentro do session_state
df_data = st.session_state["data"]

# Função para formatar valores monetários
def formatar_euro(valor):
    return f"€ {valor:,.0f}".replace(",", ".")

# ---- FILTRO DE CLUBES ----
clubes = df_data["Club"].value_counts().index
club = st.sidebar.selectbox("Clube", clubes)

# ---- FILTRO DE JOGADORES ----
df_players = df_data[df_data["Club"] == club]
players = df_players["Name"].value_counts().index
player = st.sidebar.selectbox("Jogador", players)

# ---- DADOS DO JOGADOR ----
player_stats = df_data[df_data["Name"] == player].iloc[0]

# ---- FOTO DO JOGADOR ----
# Agora usamos URL direto, sem requests/BytesIO
st.image(player_stats["Photo"], width=60)

# Nome do jogador
st.title(player_stats["Name"])

# ---- INFORMAÇÕES DO JOGADOR ----
st.markdown(f"**Clube:** {player_stats['Club']}")
st.markdown(f"**Posição:** {player_stats['Position']}")

col1, col2, col3, col4 = st.columns(4)
col1.markdown(f"**Idade:** {player_stats['Age']}")
col2.markdown(f"**Altura:** {player_stats['Height']}")
col3.markdown(f"**Peso:** {player_stats['Weight']}")

st.divider()

# ---- OVERALL ----
st.subheader(f"Overall {player_stats['Overall']}")
st.progress(int(player_stats["Overall"]))

# ---- VALORES FINANCEIROS ----
col1, col2, col3, col4 = st.columns(4)
col1.metric(label="Valor bruto", value=formatar_euro(player_stats["Value"]))
col2.metric(label="Remuneração semanal", value=formatar_euro(player_stats["Wage"]))
col3.metric(label="Valor de mercado", value=formatar_euro(player_stats["Release Clause"]))
