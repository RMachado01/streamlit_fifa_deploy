import streamlit as st
import pandas as pd

# Configurações da página da segunda aba (Players)
st.set_page_config(
    page_title="Players",
    layout="wide"
)

# ---- CARREGA O DATAFRAME ----
# Uso o dataframe que já está salvo na sessão do app.py
df_data = st.session_state["data"]

# ---- FILTRO DE CLUBES ----
# Lista de todos os clubes disponíveis
clubes = df_data["Club"].value_counts().index
club = st.sidebar.selectbox("Clube", clubes)

# Filtra apenas os jogadores do clube selecionado
df_players = df_data[df_data["Club"] == club]

# ---- FILTRO DE JOGADORES ----
# Lista dos jogadores do clube selecionado
players = df_players["Name"].value_counts().index
player = st.sidebar.selectbox("Jogador", players)

# ---- CARREGA OS DADOS DO JOGADOR SELECIONADO ----
player_stats = df_players[df_players["Name"] == player].iloc[0]

# ---- EXIBE A FOTO DO JOGADOR ----
# Streamlit consegue exibir direto a URL da imagem
st.image(player_stats["Photo"].strip(), width=70)

# Nome do jogador como título
st.title(player_stats["Name"])

# ---- INFORMAÇÕES DO JOGADOR ----
st.markdown(f"**Clube:** {player_stats['Club']}")
st.markdown(f"**Posição:** {player_stats['Position']}")

# Exibição em 4 colunas
col1, col2, col3, col4 = st.columns(4)
col1.markdown(f"**Idade:** {player_stats['Age']}")
col2.markdown(f"**Altura:** {player_stats['Height']} cm")
col3.markdown(f"**Peso:** {player_stats['Weight']} kg")

# Separador visual
st.divider()

# ---- OVERALL DO JOGADOR ----
st.subheader(f"Overall {player_stats['Overall']}")
st.progress(int(player_stats["Overall"]))

# ---- VALORES FINANCEIROS ----
col1, col2, col3, col4 = st.columns(4)

# Função para formatar valores em euros
def formatar_euro(valor):
    return f"€ {valor:,.0f}".replace(",", ".")

col1.metric(label="Valor bruto", value=formatar_euro(player_stats["Value"]))
col2.metric(label="Remuneração semanal", value=formatar_euro(player_stats["Wage"]))
col3.metric(label="Valor de mercado", value=formatar_euro(player_stats["Release Clause"]))

