"""Cupom de desconto no carrinho (CA01 a CA05), pela interface.

Cenários: docs/cenarios/01-cupom.feature
"""

import pytest
from playwright.sync_api import expect

pytestmark = pytest.mark.ui

MOCHILA = "Mochila Urbana 20L"  # R$ 100,00: facilita conferir 10% de cabeça


@pytest.fixture
def carrinho_com_mochila(vitrine, carrinho):
    """Pré-condição de quase todos os testes: 1 mochila no carrinho, carrinho aberto."""
    vitrine.abrir()
    vitrine.adicionar(MOCHILA)
    vitrine.ir_para_o_carrinho()
    carrinho.resumo.deve_exibir("R$ 100,00", "R$ 0,00", "R$ 19,90", "R$ 119,90")
    return carrinho


def test_ct_cup_01_cupom_aplica_10_por_cento(carrinho_com_mochila):
    carrinho = carrinho_com_mochila

    carrinho.aplicar_cupom("BEMVINDO10")

    expect(carrinho.cupom_aplicado).to_contain_text("Cupom BEMVINDO10 aplicado.")
    carrinho.resumo.deve_exibir("R$ 100,00", "- R$ 10,00", "R$ 19,90", "R$ 109,90")


@pytest.mark.parametrize(
    "codigo_digitado",
    ["bemvindo10", "BemVindo10", "  BEMVINDO10  ", " bemvindo10 "],
    ids=["minusculas", "caixa-mista", "espacos-nas-pontas", "minusculas-com-espacos"],
)
def test_ct_cup_04_cupom_ignora_caixa_e_espacos(carrinho_com_mochila, codigo_digitado):
    carrinho = carrinho_com_mochila

    carrinho.aplicar_cupom(codigo_digitado)

    expect(carrinho.cupom_aplicado).to_contain_text("Cupom BEMVINDO10 aplicado.")
    expect(carrinho.resumo.desconto).to_have_text("- R$ 10,00")


@pytest.mark.parametrize(
    "codigo, mensagem",
    [
        ("XPTO", "Cupom inválido."),
        ("VERAO2026", "Cupom expirado."),
    ],
    ids=["ct_cup_06-inexistente", "ct_cup_08-expirado"],
)
def test_cupom_recusado_mostra_mensagem_e_nao_da_desconto(carrinho_com_mochila, codigo, mensagem):
    carrinho = carrinho_com_mochila

    carrinho.aplicar_cupom(codigo)

    expect(carrinho.mensagem_cupom).to_have_text(mensagem)
    carrinho.resumo.deve_exibir("R$ 100,00", "R$ 0,00", "R$ 19,90", "R$ 119,90")


def test_ct_cup_10_com_cupom_aplicado_nao_ha_campo_para_outro(carrinho_com_mochila):
    carrinho = carrinho_com_mochila

    carrinho.aplicar_cupom("BEMVINDO10")

    expect(carrinho.botao_remover_cupom).to_be_visible()
    expect(carrinho.campo_cupom).to_have_count(0)  # o campo sai da tela
    expect(carrinho.botao_aplicar).to_have_count(0)


def test_ct_cup_11_remover_cupom_zera_o_desconto(carrinho_com_mochila):
    carrinho = carrinho_com_mochila
    carrinho.aplicar_cupom("BEMVINDO10")
    carrinho.resumo.deve_exibir("R$ 100,00", "- R$ 10,00", "R$ 19,90", "R$ 109,90")

    carrinho.remover_cupom()

    expect(carrinho.campo_cupom).to_be_visible()
    expect(carrinho.campo_cupom).to_have_value("")
    carrinho.resumo.deve_exibir("R$ 100,00", "R$ 0,00", "R$ 19,90", "R$ 119,90")


def test_ct_cup_14_cupom_segue_ate_a_confirmacao_do_pedido(carrinho_com_mochila, checkout, confirmacao):
    carrinho = carrinho_com_mochila
    carrinho.aplicar_cupom("BEMVINDO10")
    carrinho.resumo.deve_exibir("R$ 100,00", "- R$ 10,00", "R$ 19,90", "R$ 109,90")

    carrinho.finalizar_compra()
    checkout.resumo.deve_exibir("R$ 100,00", "- R$ 10,00", "R$ 19,90", "R$ 109,90")
    checkout.preencher("Maria Silva", "maria@exemplo.com", "01310-100")
    checkout.confirmar()

    confirmacao.deve_estar_aberta()
    confirmacao.resumo.deve_exibir("R$ 100,00", "- R$ 10,00", "R$ 19,90", "R$ 109,90")
