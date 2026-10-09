"""API de cálculo do carrinho: cupom, frete e validação de itens.

Cenários: docs/cenarios/07-api-carrinho.feature
          docs/cenarios/04-calculo-e-arredondamento.feature
"""

import pytest

from tests.dados import (
    CUPOM_EXPIRADO,
    CUPOM_INEXISTENTE,
    CUPOM_VALIDO,
    PRECOS_EM_CENTAVOS,
    esperado,
    item,
)

pytestmark = pytest.mark.api

ROTA = "/api/carrinho/calcular"

# xfail = "falha esperada". O teste descreve o comportamento CORRETO segundo a
# documentação; enquanto o bug existir ele falha e o pytest mostra XFAIL em vez
# de vermelho. strict=True faz o contrário quando o bug for corrigido: o teste
# passa, o pytest acusa XPASS como falha e alguém lembra de tirar a marcação.
BUG_FRETE_NO_LIMITE = pytest.mark.xfail(
    reason="BUG-001: subtotal de exatamente R$ 200,00 não recebe frete grátis (CA06)",
    strict=True,
)


def calcular(api, itens, cupom=None):
    corpo = {"itens": [item(produto, qtd) for produto, qtd in itens]}
    if cupom is not None:
        corpo["cupom"] = cupom
    return api.post(ROTA, data=corpo)


def valores(corpo: dict) -> dict:
    """Recorta da resposta só os campos de valores, para comparar de uma vez."""
    campos = ["subtotal", "desconto", "frete", "freteGratis", "valorFaltanteFreteGratis", "total"]
    return {campo: corpo[campo] for campo in campos}


# ------------------------------------------------------------------- Cupom


def test_ct_apc_01_cupom_aplica_10_por_cento_sobre_o_subtotal(api):
    resposta = calcular(api, [("P005", 1)], CUPOM_VALIDO)

    assert resposta.status == 200
    corpo = resposta.json()
    assert valores(corpo) == {
        "subtotal": 100,
        "desconto": 10,
        "frete": 19.9,
        "freteGratis": False,
        "valorFaltanteFreteGratis": 100,
        "total": 109.9,
    }
    assert corpo["cupom"]["codigo"] == "BEMVINDO10"
    assert corpo["cupom"]["aplicado"] is True


@pytest.mark.parametrize(
    "cupom",
    ["bemvindo10", "BemVindo10", "  BEMVINDO10  ", " bemvindo10 "],
    ids=["minusculas", "caixa-mista", "espacos-nas-pontas", "minusculas-com-espacos"],
)
def test_ct_apc_02_cupom_ignora_caixa_e_espacos_nas_pontas(api, cupom):
    corpo = calcular(api, [("P005", 1)], cupom).json()

    assert corpo["desconto"] == 10
    assert corpo["cupom"]["codigo"] == "BEMVINDO10"
    assert corpo["cupom"]["aplicado"] is True


@pytest.mark.parametrize(
    "cupom, mensagem",
    [
        (CUPOM_INEXISTENTE, "Cupom inválido."),
        (CUPOM_EXPIRADO, "Cupom expirado."),
    ],
    ids=["ct_apc_03-inexistente", "ct_apc_04-expirado"],
)
def test_cupom_recusado_responde_200_sem_desconto(api, cupom, mensagem):
    resposta = calcular(api, [("P005", 1)], cupom)

    assert resposta.status == 200
    corpo = resposta.json()
    assert corpo["desconto"] == 0
    assert corpo["total"] == 119.9
    assert corpo["cupom"]["aplicado"] is False
    assert corpo["cupom"]["mensagem"] == mensagem


def test_ct_apc_05_calculo_sem_cupom_nao_aplica_desconto(api):
    resposta = calcular(api, [("P005", 1)])

    assert resposta.status == 200
    corpo = resposta.json()
    assert corpo["desconto"] == 0
    assert corpo["cupom"] is None


# ------------------------------------------------------------------- Frete


@pytest.mark.parametrize(
    "itens",
    [
        pytest.param([("P001", 1)], id="59.90-bem-abaixo"),
        pytest.param([("P002", 1), ("P006", 2)], id="199.70-logo-abaixo"),
        pytest.param([("P005", 2)], id="200.00-no-limite", marks=BUG_FRETE_NO_LIMITE),
        pytest.param([("P008", 4)], id="200.00-no-limite-outro-produto", marks=BUG_FRETE_NO_LIMITE),
        pytest.param([("P003", 1), ("P006", 1)], id="219.80-logo-acima"),
        pytest.param([("P007", 1)], id="229.90-acima"),
    ],
)
def test_ct_apc_06_frete_conforme_o_subtotal(api, itens):
    """Análise de valor-limite em torno de R$ 200,00 (CA06 e CA07)."""
    corpo = calcular(api, itens).json()

    assert valores(corpo) == esperado(itens)


def test_ct_apc_07_frete_gratis_considera_subtotal_antes_do_desconto(api):
    # Subtotal 219,80. Com o cupom os produtos saem por 197,82, abaixo de
    # 200,00. Pelo CA08 o frete continua grátis.
    corpo = calcular(api, [("P003", 1), ("P006", 1)], CUPOM_VALIDO).json()

    assert corpo["subtotal"] == 219.8
    assert corpo["desconto"] == 21.98
    assert corpo["frete"] == 0
    assert corpo["freteGratis"] is True
    assert corpo["total"] == 197.82


def test_ct_apc_08_desconto_nao_incide_sobre_o_frete(api):
    # 10% de 59,90 = 5,99. Se o frete entrasse na base seria 7,98.
    corpo = calcular(api, [("P001", 1)], CUPOM_VALIDO).json()

    assert corpo["desconto"] == 5.99
    assert corpo["frete"] == 19.9
    assert corpo["total"] == 73.81


# ------------------------------------------------- Cálculo e arredondamento


def test_ct_cal_01_exemplo_da_documentacao(api):
    resposta = calcular(api, [("P002", 1), ("P004", 2)], CUPOM_VALIDO)

    assert resposta.status == 200
    corpo = resposta.json()
    assert valores(corpo) == {
        "subtotal": 239.7,
        "desconto": 23.97,
        "frete": 0,
        "freteGratis": True,
        "valorFaltanteFreteGratis": 0,
        "total": 215.73,
    }
    assert corpo["cupom"] == {
        "codigo": "BEMVINDO10",
        "aplicado": True,
        "mensagem": "Cupom aplicado: 10% de desconto nos produtos.",
    }


@pytest.mark.parametrize(
    "produto, quantidade",
    [("P001", 1), ("P001", 3), ("P004", 1), ("P006", 1), ("P006", 3), ("P006", 5), ("P007", 3)],
)
def test_ct_cal_02_valores_com_no_maximo_2_casas_decimais(api, produto, quantidade):
    itens = [(produto, quantidade)]

    corpo = calcular(api, itens, CUPOM_VALIDO).json()

    assert valores(corpo) == esperado(itens, percentual_cupom=10)
    for campo in ["subtotal", "desconto", "frete", "total", "valorFaltanteFreteGratis"]:
        # Um valor com 2 casas não muda quando é arredondado para 2 casas.
        assert corpo[campo] == round(corpo[campo], 2), f"{campo} tem mais de 2 casas decimais"


def test_ct_cal_03_total_do_item_e_preco_vezes_quantidade(api):
    corpo = calcular(api, [("P001", 3), ("P006", 2)]).json()

    assert [(i["produtoId"], i["precoUnitario"], i["quantidade"], i["total"]) for i in corpo["itens"]] == [
        ("P001", 59.9, 3, 179.7),
        ("P006", 29.9, 2, 59.8),
    ]
    assert corpo["subtotal"] == 239.5


def test_ct_cal_04_valor_faltante_nunca_e_negativo(api):
    corpo = calcular(api, [("P007", 5)]).json()

    assert corpo["valorFaltanteFreteGratis"] == 0


# ----------------------------------------------------- Validação dos itens


@pytest.mark.parametrize("corpo", [{}, {"itens": []}], ids=["sem-itens", "itens-vazio"])
def test_ct_apc_09_itens_obrigatorios(api, corpo):
    resposta = api.post(ROTA, data=corpo)

    assert resposta.status == 422
    assert resposta.json()["erro"]["codigo"] == "ITENS_OBRIGATORIOS"


def test_ct_apc_10_item_invalido(api):
    resposta = api.post(ROTA, data={"itens": ["P001"]})

    assert resposta.status == 422
    assert resposta.json()["erro"]["codigo"] == "ITEM_INVALIDO"


def test_ct_apc_11_produto_inexistente_no_item(api):
    resposta = api.post(ROTA, data={"itens": [item("P999", 1)]})

    assert resposta.status == 422
    erro = resposta.json()["erro"]
    assert erro["codigo"] == "PRODUTO_NAO_ENCONTRADO"
    assert erro["campo"] == "itens[0].produtoId"


def test_ct_apc_12_item_duplicado(api):
    resposta = api.post(ROTA, data={"itens": [item("P001", 1), item("P001", 2)]})

    assert resposta.status == 422
    assert resposta.json()["erro"]["codigo"] == "ITEM_DUPLICADO"


def test_precos_usados_no_oraculo_batem_com_a_api(api):
    """Protege os outros testes: se um preço mudar, este aponta a causa."""
    produtos = api.get("/api/produtos").json()

    assert {p["id"]: round(p["preco"] * 100) for p in produtos} == PRECOS_EM_CENTAVOS
