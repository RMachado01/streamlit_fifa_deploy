# FIFA 23 — Explorador de jogadores e clubes

[![CI](https://github.com/RMachado01/streamlit_fifa_deploy/actions/workflows/ci.yml/badge.svg)](https://github.com/RMachado01/streamlit_fifa_deploy/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)

App multipágina em Streamlit para explorar o dataset oficial do **FIFA 23**
(mais de 17 mil jogadores): ficha de cada jogador com atributos e valores, e
visão do elenco completo de cada clube.

## Páginas

| Página | O que mostra |
| --- | --- |
| **Home** | Contexto do dataset e link para a fonte no Kaggle |
| **Players** | Ficha do jogador: posição, idade, altura, peso, overall, valor de mercado, salário e multa |
| **Club** | Elenco do clube com foto, bandeira, overall em barra e valores formatados |

## Como os dados são tratados

Toda a limpeza fica em [`src/data_loader.py`](src/data_loader.py), em funções
pequenas e testadas:

- valores como `€78.5M` e `€115K` viram euros inteiros;
- altura e peso são normalizados para cm e kg, aceitando `189cm`, `1,89`,
  `6'2` e `190lbs` (as versões do dataset usam formatos diferentes);
- a posição vem com HTML do site de origem (`<span class="pos pos25">ST`) e é
  limpa;
- jogadores duplicados (mesmo `ID`) e sem valor de mercado são removidos;
- só entram contratos válidos em 2023, o ano de referência do dataset.

Os dados são lidos uma vez e ficam em cache (`st.cache_data`), então qualquer
página pode ser aberta direto pela URL.

## Rodando localmente

```bash
pip install -r requirements.txt
streamlit run Home.py
```

## Testes

```bash
pip install -r requirements-dev.txt
pytest -v
```

## Estrutura

```text
Home.py               página inicial
pages/                páginas Players e Club
src/data_loader.py    leitura e limpeza do CSV
src/estado.py         cache compartilhado entre as páginas
tests/                testes das conversões e da limpeza
Data/                 FIFA23_official_data.csv
```

## Fonte dos dados

[FIFA Player Stats Database — Kaggle](https://www.kaggle.com/datasets/bryanb/fifa-player-stats-database)
