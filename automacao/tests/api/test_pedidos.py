"""API de pedidos.

Cenários: docs/cenarios/08-api-pedidos.feature
"""

import re
from datetime import datetime

import pytest

from tests.dados import CLIENTE_VALIDO, CUPOM_EXPIRADO, CUPOM_INEXISTENTE, CUPOM_VALIDO, item

pytestmark = pytest.mark.api

ROTA = "/api/pedidos"
CAMPOS_DE_VALOR = ["subtotal", "desconto", "frete", "freteGratis", "valorFaltanteFreteGratis", "total"]


def pedir(api, itens=None, cupom=None, **cliente):
    """Envia um pedido válido, trocando só o que o teste informar.

    Ex.: pedir(api, cep="123") envia o cliente válido com o CEP trocado.
    """
    corpo = {
        "cliente": {**CLIENTE_VALIDO, **cliente},
        "itens": itens if itens is not None else [item("P005", 1)],
    }
    if cupom is not None:
        corpo["cupom"] = cupom
    return api.post(ROTA, data=corpo)


def test_ct_app_01_pedido_valido_com_cupom(api):
    resposta = pedir(api, cupom=CUPOM_VALIDO)

    assert resposta.status == 201
    corpo = resposta.json()
    assert re.fullmatch(r"VZ-\d{6}", corpo["numero"])
    # fromisoformat lança erro se o texto não for uma data ISO 8601 válida.
    datetime.fromisoformat(corpo["criadoEm"].replace("Z", "+00:00"))
    assert corpo["cliente"] == {"nome": "Maria Silva", "email": "maria@exemplo.com", "cep": "01310100"}
    assert {campo: corpo[campo] for campo in CAMPOS_DE_VALOR} == {
        "subtotal": 100,
        "desconto": 10,
        "frete": 19.9,
        "freteGratis": False,
        "valorFaltanteFreteGratis": 100,
        "total": 109.9,
    }


def test_ct_app_02_pedido_devolve_os_mesmos_valores_do_calculo(api):
    itens = [item("P002", 1), item("P004", 2)]
    calculo = api.post("/api/carrinho/calcular", data={"itens": itens, "cupom": CUPOM_VALIDO}).json()

    resposta = pedir(api, itens=itens, cupom=CUPOM_VALIDO)

    assert resposta.status == 201
    pedido = resposta.json()
    for campo in CAMPOS_DE_VALOR + ["itens", "cupom"]:
        assert pedido[campo] == calculo[campo], f"{campo} difere entre o cálculo e o pedido"


@pytest.mark.parametrize(
    "cupom, codigo",
    [
        (CUPOM_INEXISTENTE, "CUPOM_INVALIDO"),
        (CUPOM_EXPIRADO, "CUPOM_EXPIRADO"),
    ],
    ids=["ct_app_03-inexistente", "ct_app_04-expirado"],
)
def test_pedido_com_cupom_recusado_devolve_422(api, cupom, codigo):
    resposta = pedir(api, cupom=cupom)

    assert resposta.status == 422
    assert resposta.json()["erro"]["codigo"] == codigo


@pytest.mark.xfail(
    reason="BUG-001: subtotal de exatamente R$ 200,00 não recebe frete grátis (CA06)",
    strict=True,
)
def test_ct_app_05_pedido_de_200_reais_tem_frete_gratis(api):
    resposta = pedir(api, itens=[item("P005", 2)])

    assert resposta.status == 201
    corpo = resposta.json()
    assert corpo["frete"] == 0
    assert corpo["total"] == 200


@pytest.mark.parametrize(
    "campo, valor",
    [
        ("nome", "Maria"),
        ("nome", ""),
        ("email", "maria"),
        ("email", "maria@exemplo"),
        ("cep", "0131010"),
        ("cep", "013101000"),
        ("cep", "01310-10A"),
    ],
)
def test_ct_app_06_dados_do_cliente_invalidos(api, campo, valor):
    resposta = pedir(api, **{campo: valor})

    assert resposta.status == 422
    erro = resposta.json()["erro"]
    assert erro["codigo"] == "DADOS_INVALIDOS"
    assert [c["campo"] for c in erro["campos"]] == [f"cliente.{campo}"]


def test_ct_app_07_pedido_sem_cliente_aponta_os_tres_campos(api):
    resposta = api.post(ROTA, data={"itens": [item("P005", 1)]})

    assert resposta.status == 422
    erro = resposta.json()["erro"]
    assert erro["codigo"] == "DADOS_INVALIDOS"
    assert {c["campo"] for c in erro["campos"]} == {"cliente.nome", "cliente.email", "cliente.cep"}


@pytest.mark.parametrize("cep", ["01310-100", "01310100"], ids=["com-hifen", "sem-hifen"])
def test_ct_app_08_cep_com_8_digitos_e_aceito(api, cep):
    resposta = pedir(api, cep=cep)

    assert resposta.status == 201
    assert resposta.json()["cliente"]["cep"] == "01310100"


def test_ct_app_09_pedido_sem_itens(api):
    resposta = pedir(api, itens=[])

    assert resposta.status == 422
    assert resposta.json()["erro"]["codigo"] == "ITENS_OBRIGATORIOS"
