import pandas as pd
import pytest

from src.data_loader import ANO_REFERENCIA, converter_altura, converter_peso, converter_valor, limpar


@pytest.mark.parametrize(
    "entrada, esperado",
    [("€91M", 91_000_000), ("€78.5M", 78_500_000), ("€115K", 115_000), ("€500", 500), ("", 0), (None, 0), ("abc", 0)],
)
def test_converter_valor(entrada, esperado):
    assert converter_valor(entrada) == esperado


@pytest.mark.parametrize(
    "entrada, esperado",
    [("189cm", 189), ("1.80", 180), ("1,75", 175), ("6'0", 183), ("5'10", 178), (None, None), ("?", None)],
)
def test_converter_altura(entrada, esperado):
    assert converter_altura(entrada) == esperado


@pytest.mark.parametrize("entrada, esperado", [("82kg", 82), ("190lbs", 86), (None, None), ("x", None)])
def test_converter_peso(entrada, esperado):
    assert converter_peso(entrada) == esperado


def _linha(id_, nome, contrato, valor="€1M", overall=80):
    return {
        "ID": id_, "Name": nome, "Photo": " http://f ", "Flag": "http://b", "Club Logo": "http://c",
        "Contract Valid Until": contrato, "Value": valor, "Wage": "€10K", "Release Clause": "€2M",
        "Height": "180cm", "Weight": "75kg", "Overall": overall, "Position": '<span class="pos pos25">ST',
    }


def test_limpar_filtra_contrato_vencido_sem_valor_e_duplicado():
    cru = pd.DataFrame([
        _linha(1, "Válido", "2026", overall=70),
        _linha(1, "Válido", "2026", overall=70),        # duplicado
        _linha(2, "Vencido", str(ANO_REFERENCIA - 1)),  # contrato antigo
        _linha(3, "Sem valor", "2025", valor="€0"),
        _linha(4, "Melhor", "Jun 30, 2024", overall=90),  # formato de data por extenso
    ])
    limpo = limpar(cru)
    assert limpo["Name"].tolist() == ["Melhor", "Válido"]   # ordenado por Overall
    assert limpo.loc[1, "Photo"] == "http://f"
    assert limpo.loc[1, "Height"] == 180
    assert limpo.loc[1, "Position"] == "ST"


def test_contratos_nao_dependem_do_ano_atual():
    # regressão: antes o filtro usava datetime.today().year e esvaziava o app com o tempo
    cru = pd.DataFrame([_linha(1, "A", str(ANO_REFERENCIA))])
    assert len(limpar(cru)) == 1
