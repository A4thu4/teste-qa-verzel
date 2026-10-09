"""Fixtures compartilhadas por todos os testes.

Uma fixture é uma função que prepara algo de que o teste precisa. O pytest
executa a fixture e entrega o resultado ao teste que pede aquele nome como
parâmetro. As fixtures `page`, `playwright` e `base_url` vêm prontas do plugin
pytest-playwright; as que estão aqui são as do projeto.
"""

import pytest
from playwright.sync_api import APIRequestContext, Page, Playwright

from pages.loja import Carrinho, Checkout, Confirmacao, Vitrine


@pytest.fixture(scope="session")
def api(playwright: Playwright, base_url: str):
    """Cliente HTTP do Playwright apontado para a loja.

    scope="session" cria um único cliente para a execução inteira, em vez de
    um por teste. Como a API não guarda estado entre chamadas (está na seção
    "Sobre este ambiente" da documentação), compartilhar o cliente é seguro.
    """
    contexto: APIRequestContext = playwright.request.new_context(base_url=base_url)
    yield contexto
    contexto.dispose()


# Cada teste de interface recebe uma `page` nova, em um contexto de navegador
# novo. Como o carrinho fica no sessionStorage da aba, todo teste começa com o
# carrinho vazio e um teste não interfere no outro.


@pytest.fixture
def vitrine(page: Page) -> Vitrine:
    return Vitrine(page)


@pytest.fixture
def carrinho(page: Page) -> Carrinho:
    return Carrinho(page)


@pytest.fixture
def checkout(page: Page) -> Checkout:
    return Checkout(page)


@pytest.fixture
def confirmacao(page: Page) -> Confirmacao:
    return Confirmacao(page)
