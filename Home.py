import streamlit as st
from src.estado import dados_fifa   # carrega e limpa os dados (com cache)

# Configurações iniciais da página:
# Aqui só ajusto o título no navegador e deixo a página mais larga,
# o que facilita a visualização dos cards e colunas.
st.set_page_config(
    page_title="FIFA 23 Dataset",
    layout="wide"
)


# Carrego os dados aqui também pra já deixar o cache pronto quando
# a pessoa trocar de página.
dados_fifa()


# A partir daqui começa a parte visual da interface:

# Título da página principal
st.title("FIFA 2023 DATASET")

# Apenas uma assinatura no menu lateral
st.sidebar.markdown("Desenvolvido por **Renan Machado**")

# Botão que abre o link original dos dados no Kaggle.
# Antes eu usava webbrowser.open_new_tab, mas isso abre a aba no SERVIDOR
# onde o app roda, não no navegador de quem está vendo. O st.link_button
# é um link de verdade, que abre na máquina do usuário.
st.link_button("Acesse os dados utilizados no Kaggle", "https://www.kaggle.com/datasets/bryanb/fifa-player-stats-database")

# Texto explicativo sobre o dataset
# Aqui explico de forma geral o que esse conjunto de dados representa,
# apenas para contextualizar o usuário.
st.markdown(
    """
    O conjunto de dados oficial do FIFA 23 traz informações abrangentes
    sobre jogadores de futebol profissionais.

    Ele contém dados demográficos, atributos físicos, estatísticas de jogo, detalhes contratuais e clubes.

    Com **mais de 17.000 jogadores**, este dataset é valioso para análises sobre atributos, desempenho,
    valor de mercado, posicionamento e evolução dos jogadores ao longo do tempo.
    """
)
