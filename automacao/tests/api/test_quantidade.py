"""Limite de 5 unidades por produto na API (CA10).

Cenários: docs/cenarios/03-quantidade.feature
"""

import pytest

from tests.dados import CLIENTE_VALIDO, item

pytestmark = pytest.mark.api

BUG_LIMITE_NA_API = pytest.mark.xfail(
    reason="BUG-002: API aceita mais de 5 unidades do mesmo produto (CA10)",
    strict=True,
)


def test_ct_qtd_06_calculo_aceita_5_unidades(api):
    resposta = api.post("/api/carrinho/calcular", data={"itens": [item("P001", 5)]})

    assert resposta.status == 200
    assert resposta.json()["subtotal"] == 299.5


@BUG_LIMITE_NA_API
def test_ct_qtd_07_calculo_recusa_6_unidades(api):
    resposta = api.post("/api/carrinho/calcular", data={"itens": [item("P001", 6)]})

    assert resposta.status == 422
    assert resposta.json()["erro"]["codigo"] == "QUANTIDADE_MAXIMA_EXCEDIDA"


@BUG_LIMITE_NA_API
def test_ct_qtd_08_pedido_recusa_6_unidades(api):
    resposta = api.post(
        "/api/pedidos",
        data={"cliente": CLIENTE_VALIDO, "itens": [item("P001", 6)]},
    )

    assert resposta.status == 422
    assert resposta.json()["erro"]["codigo"] == "QUANTIDADE_MAXIMA_EXCEDIDA"


@pytest.mark.parametrize(
    "quantidade",
    [0, -1, 1.5, "2", None],
    ids=["zero", "negativa", "decimal", "texto", "nula"],
)
def test_ct_qtd_09_quantidade_invalida(api, quantidade):
    resposta = api.post("/api/carrinho/calcular", data={"itens": [item("P001", quantidade)]})

    assert resposta.status == 422
    erro = resposta.json()["erro"]
    assert erro["codigo"] == "QUANTIDADE_INVALIDA"
    assert erro["campo"] == "itens[0].quantidade"
