"""API de produtos e tratamento geral de erros.

Cenários: docs/cenarios/06-api-produtos-e-erros.feature
"""

import pytest

from tests.dados import NOMES, PRECOS_EM_CENTAVOS

pytestmark = pytest.mark.api


def test_ct_api_01_lista_os_8_produtos_da_documentacao(api):
    resposta = api.get("/api/produtos")

    assert resposta.status == 200
    produtos = resposta.json()
    assert len(produtos) == 8
    for produto in produtos:
        assert set(produto) == {"id", "nome", "descricao", "categoria", "preco"}
    assert {p["id"]: p["nome"] for p in produtos} == NOMES
    precos = {p["id"]: round(p["preco"] * 100) for p in produtos}
    assert precos == PRECOS_EM_CENTAVOS


def test_ct_api_02_consulta_produto_existente(api):
    resposta = api.get("/api/produtos/P001")

    assert resposta.status == 200
    produto = resposta.json()
    assert produto["nome"] == "Camiseta Essencial"
    assert produto["preco"] == 59.9


def test_ct_api_03_produto_inexistente_devolve_404(api):
    resposta = api.get("/api/produtos/P999")

    assert resposta.status == 404
    assert resposta.json()["erro"]["codigo"] == "PRODUTO_NAO_ENCONTRADO"


def test_ct_api_05_rota_inexistente_devolve_404(api):
    resposta = api.get("/api/rota-que-nao-existe")

    assert resposta.status == 404
    assert resposta.json()["erro"]["codigo"] == "ROTA_NAO_ENCONTRADA"


# parametrize roda o mesmo teste uma vez para cada linha da lista. É o
# equivalente em pytest ao "Esquema do Cenário" com "Exemplos" do Gherkin.
@pytest.mark.parametrize(
    "metodo, rota",
    [
        ("GET", "/api/carrinho/calcular"),
        ("GET", "/api/pedidos"),
        ("POST", "/api/produtos"),
        ("PUT", "/api/produtos/P001"),
    ],
)
def test_ct_api_06_metodo_nao_permitido_devolve_405(api, metodo, rota):
    resposta = api.fetch(rota, method=metodo)

    assert resposta.status == 405
    assert resposta.json()["erro"]["codigo"] == "METODO_NAO_PERMITIDO"


@pytest.mark.parametrize(
    "rota, corpo",
    [
        ("/api/carrinho/calcular", "{itens:"),
        ("/api/carrinho/calcular", "[1, 2]"),
        ("/api/pedidos", "nao e json"),
    ],
    ids=["json-malformado", "lista-em-vez-de-objeto", "texto-puro"],
)
def test_ct_api_07_corpo_invalido_devolve_400(api, rota, corpo):
    resposta = api.post(
        rota,
        data=corpo.encode("utf-8"),  # bytes: o Playwright envia o corpo como está
        headers={"Content-Type": "application/json"},
    )

    assert resposta.status == 400
    assert resposta.json()["erro"]["codigo"] == "JSON_INVALIDO"
