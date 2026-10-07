"""Limite de 5 unidades por produto na interface (CA10).

Cenários: docs/cenarios/03-quantidade.feature
"""

import pytest
from playwright.sync_api import expect

pytestmark = pytest.mark.ui

MOCHILA = "Mochila Urbana 20L"


def test_ct_qtd_01_vitrine_bloqueia_a_sexta_unidade(vitrine):
    vitrine.abrir()

    vitrine.adicionar(MOCHILA, 5)

    expect(vitrine.aviso(MOCHILA)).to_have_text("Limite de 5 unidades atingido.")
    expect(vitrine.botao_adicionar(MOCHILA)).to_be_disabled()
    expect(vitrine.contador).to_have_text("5")


def test_ct_qtd_02_carrinho_bloqueia_aumentar_acima_de_5(vitrine, carrinho):
    vitrine.abrir()
    vitrine.adicionar(MOCHILA, 5)

    vitrine.ir_para_o_carrinho()

    expect(carrinho.quantidade(MOCHILA)).to_have_text("5")
    expect(carrinho.botao_aumentar(MOCHILA)).to_be_disabled()
    expect(carrinho.resumo.subtotal).to_have_text("R$ 500,00")
