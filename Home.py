import streamlit as st
import webbrowser
from src.data_loader import load_fifa_data   # Importo minha função que faz toda a limpeza e organização dos dados

# Configurações iniciais da página:
# Aqui só ajusto o título no navegador e deixo a página mais larga,
# o que facilita a visualização dos cards e colunas.
st.set_page_config(
    page_title="Players",
    layout="wide"
)


# Verifico se o dataframe já está salvo na sessão.
# Isso evita recarregar e limpar os dados toda vez que trocar de página.
# Assim economizo processamento e deixo o app mais rápido.
if "data" not in st.session_state:

    # Aqui eu chamo minha função de carregamento e limpeza dos dados.
    # Antes eu fazia tudo manualmente aqui no app.py, mas agora deixei isso
    # organizado dentro do módulo data_loader.py.
    df_data = load_fifa_data()

    # Salvo o dataframe tratado na sessão para usar em outras páginas.
    st.session_state["data"] = df_data


# A partir daqui começa a parte visual da interface:

# Título da página principal
st.title("FIFA 2023 DATASET")

# Apenas uma assinatura no menu lateral
st.sidebar.markdown("Desenvolvido por **Renan Machado**")

# Botão que abre o link original dos dados no Kaggle
btn = st.button("Acesse os dados utilizados no Kaggle.")

# Se o botão for clicado, abro em uma nova aba do navegador.
if btn:
    webbrowser.open_new_tab("https://www.kaggle.com/datasets/bryanb/fifa-player-stats-database")

# Texto explicativo sobre o dataset
# Aqui explico de forma geral o que esse conjunto de dados representa,
# apenas para contextualizar o usuário.
st.markdown(
    """
    O conjunto de dados de jogadores de futebol de 2017 a 2023 fornece informações abrangentes
    sobre jogadores de futebol profissionais.

    Ele contém dados demográficos, atributos físicos, estatísticas de jogo, detalhes contratuais e clubes.

    Com **mais de 17.000 registros**, este dataset é valioso para análises sobre atributos, desempenho,
    valor de mercado, posicionamento e evolução dos jogadores ao longo do tempo.
    """
)
