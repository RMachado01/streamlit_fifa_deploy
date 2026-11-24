import streamlit as st

from src.data_loader import load_fifa_data


@st.cache_data(show_spinner="Carregando jogadores...")
def dados_fifa():
    """Carrega os dados uma vez só e reaproveita em todas as páginas.

    Antes a Home guardava o DataFrame no st.session_state e as outras páginas
    liam de lá. Só que quem abria /Players direto (ou dava F5 nela) recebia
    KeyError, porque a Home nunca tinha rodado. Com o cache, qualquer página
    pode chamar esta função e o CSV só é lido na primeira vez.
    """
    return load_fifa_data()
