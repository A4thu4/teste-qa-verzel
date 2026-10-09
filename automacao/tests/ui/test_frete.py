"""Frete grátis a partir de R$ 200,00 (CA06 a CA09), pela interface.

Cenários: docs/cenarios/02-frete.feature
"""

import pytest
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


def montar_carrinho(vitrine, itens: list[tuple[str, int]]) -> None:
    vitrine.abrir()
    for produto, quantidade in itens:
        vitrine.adicionar(produto, quantidade)
    vitrine.ir_para_o_carrinho()


@pytest.mark.xfail(
    reason="BUG-001: subtotal de exatamente R$ 200,00 não recebe frete grátis (CA06)",
    strict=True,
)
def test_ct_fre_01_subtotal_de_200_reais_tem_frete_gratis(vitrine, carrinho):
    montar_carrinho(vitrine, [("Mochila Urbana 20L", 2)])

    carrinho.resumo.deve_exibir("R$ 200,00", "R$ 0,00", "Grátis", "R$ 200,00")
    expect(carrinho.resumo.aviso_frete).to_have_count(0)


def test_ct_fre_03_subtotal_acima_de_200_reais_tem_frete_gratis(vitrine, carrinho):
    montar_carrinho(vitrine, [("Jaqueta Corta-Vento", 1)])

    carrinho.resumo.deve_exibir("R$ 229,90", "R$ 0,00", "Grátis", "R$ 229,90")
    expect(carrinho.resumo.aviso_frete).to_have_count(0)


def test_ct_fre_04_logo_abaixo_de_200_paga_frete_e_informa_o_faltante(vitrine, carrinho):
    montar_carrinho(vitrine, [("Calça Jeans Slim", 1), ("Kit 3 Pares de Meias", 2)])

    carrinho.resumo.deve_exibir("R$ 199,70", "R$ 0,00", "R$ 19,90", "R$ 219,60")
    expect(carrinho.resumo.aviso_frete).to_have_text("Faltam R$ 0,30 para o frete grátis.")


def test_ct_fre_07_frete_gratis_considera_subtotal_antes_do_desconto(vitrine, carrinho):
    montar_carrinho(vitrine, [("Tênis Casual Urbano", 1), ("Kit 3 Pares de Meias", 1)])
    carrinho.resumo.deve_exibir("R$ 219,80", "R$ 0,00", "Grátis", "R$ 219,80")

    carrinho.aplicar_cupom("BEMVINDO10")

    # 219,80 - 21,98 = 197,82: menor que 200,00, e ainda assim o frete é grátis.
    carrinho.resumo.deve_exibir("R$ 219,80", "- R$ 21,98", "Grátis", "R$ 197,82")


def test_ct_fre_10_desconto_nao_incide_sobre_o_frete(vitrine, carrinho):
    montar_carrinho(vitrine, [("Mochila Urbana 20L", 1)])

    carrinho.aplicar_cupom("BEMVINDO10")

    # 10% de 100,00 = 10,00. Se o frete entrasse na base seria 11,99.
    carrinho.resumo.deve_exibir("R$ 100,00", "- R$ 10,00", "R$ 19,90", "R$ 109,90")
