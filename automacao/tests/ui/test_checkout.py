"""Finalização da compra: regras que já existiam antes da entrega (regressão).

Cenários: docs/cenarios/05-checkout.feature
"""

import re

import pytest
from playwright.sync_api import expect

pytestmark = pytest.mark.ui

NOME, EMAIL, CEP = "Maria Silva", "maria@exemplo.com", "01310-100"


@pytest.fixture
def checkout_aberto(vitrine, carrinho, checkout):
    """Pré-condição: 1 mochila no carrinho e a página "Finalizar compra" aberta."""
    vitrine.abrir()
    vitrine.adicionar("Mochila Urbana 20L")
    vitrine.ir_para_o_carrinho()
    carrinho.finalizar_compra()
    return checkout


def test_ct_chk_01_pedido_confirmado_com_dados_validos(checkout_aberto, confirmacao):
    checkout = checkout_aberto

    checkout.preencher(NOME, EMAIL, CEP)
    checkout.confirmar()

    confirmacao.deve_estar_aberta()
    expect(confirmacao.numero_pedido).to_have_text(re.compile(r"^VZ-\d{6}$"))
    confirmacao.resumo.deve_exibir("R$ 100,00", "R$ 0,00", "R$ 19,90", "R$ 119,90")
    expect(confirmacao.contador).to_have_text("0")


@pytest.mark.parametrize(
    "nome, mensagem",
    [
        ("", "Informe o nome completo."),
        ("Maria", "Informe nome e sobrenome."),
        ("Maria ", "Informe nome e sobrenome."),
    ],
    ids=["vazio", "so-primeiro-nome", "primeiro-nome-e-espaco"],
)
def test_ct_chk_04_nome_sem_sobrenome_e_recusado(checkout_aberto, nome, mensagem):
    checkout = checkout_aberto

    checkout.preencher(nome, EMAIL, CEP)
    checkout.confirmar()

    expect(checkout.erro_nome).to_have_text(mensagem)
    checkout.deve_continuar_no_checkout()


@pytest.mark.parametrize(
    "email, mensagem",
    [
        ("", "Informe o e-mail."),
        ("maria", "Informe um e-mail válido."),
        ("maria@", "Informe um e-mail válido."),
        ("@exemplo.com", "Informe um e-mail válido."),
        ("maria@exemplo", "Informe um e-mail válido."),
        ("maria silva@exemplo.com", "Informe um e-mail válido."),
        ("maria@@exemplo.com", "Informe um e-mail válido."),
    ],
)
def test_ct_chk_06_email_invalido_e_recusado(checkout_aberto, email, mensagem):
    checkout = checkout_aberto

    checkout.preencher(NOME, email, CEP)
    checkout.confirmar()

    expect(checkout.erro_email).to_have_text(mensagem)
    checkout.deve_continuar_no_checkout()


@pytest.mark.parametrize(
    "cep, mensagem",
    [
        ("", "Informe o CEP."),
        ("0131010", "Informe um CEP com 8 dígitos."),
        ("013101000", "Informe um CEP com 8 dígitos."),
        ("01310-10A", "Informe um CEP com 8 dígitos."),
        ("013-10100", "Informe um CEP com 8 dígitos."),
        ("01310 100", "Informe um CEP com 8 dígitos."),
    ],
)
def test_ct_chk_08_cep_invalido_e_recusado(checkout_aberto, cep, mensagem):
    checkout = checkout_aberto

    checkout.preencher(NOME, EMAIL, cep)
    checkout.confirmar()

    expect(checkout.erro_cep).to_have_text(mensagem)
    checkout.deve_continuar_no_checkout()


@pytest.mark.parametrize("cep", ["01310-100", "01310100"], ids=["com-hifen", "sem-hifen"])
def test_ct_chk_09_cep_com_8_digitos_e_aceito(checkout_aberto, confirmacao, cep):
    checkout = checkout_aberto

    checkout.preencher(NOME, EMAIL, cep)
    checkout.confirmar()

    confirmacao.deve_estar_aberta()
