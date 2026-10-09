"""Dados de teste tirados da documentação da entrega VZS-142."""

# Preços em centavos. Fazer as contas em inteiros evita o erro de ponto
# flutuante do tipo 0.1 + 0.2 = 0.30000000000000004, que faria um teste de
# arredondamento falhar por culpa do próprio teste.
PRECOS_EM_CENTAVOS = {
    "P001": 5990,   # Camiseta Essencial
    "P002": 13990,  # Calça Jeans Slim
    "P003": 18990,  # Tênis Casual Urbano
    "P004": 4990,   # Boné Aba Curva
    "P005": 10000,  # Mochila Urbana 20L
    "P006": 2990,   # Kit 3 Pares de Meias
    "P007": 22990,  # Jaqueta Corta-Vento
    "P008": 5000,   # Garrafa Térmica 750ml
}

NOMES = {
    "P001": "Camiseta Essencial",
    "P002": "Calça Jeans Slim",
    "P003": "Tênis Casual Urbano",
    "P004": "Boné Aba Curva",
    "P005": "Mochila Urbana 20L",
    "P006": "Kit 3 Pares de Meias",
    "P007": "Jaqueta Corta-Vento",
    "P008": "Garrafa Térmica 750ml",
}

CUPOM_VALIDO = "BEMVINDO10"       # 10%
CUPOM_EXPIRADO = "VERAO2026"      # expirou em 31/03/2026
CUPOM_INEXISTENTE = "XPTO"

LIMITE_FRETE_GRATIS_EM_CENTAVOS = 20000
FRETE_FIXO_EM_CENTAVOS = 1990

# Cliente do exemplo da própria documentação. Dados fictícios.
CLIENTE_VALIDO = {
    "nome": "Maria Silva",
    "email": "maria@exemplo.com",
    "cep": "01310-100",
}


def item(produto_id: str, quantidade: int) -> dict:
    return {"produtoId": produto_id, "quantidade": quantidade}


def esperado(itens: list[tuple[str, int]], percentual_cupom: int = 0) -> dict:
    """Calcula o resultado esperado pelas regras da documentação.

    É o "oráculo" dos testes de varredura: uma implementação independente e
    simples das regras, usada para conferir a resposta da API.
    """
    subtotal = sum(PRECOS_EM_CENTAVOS[produto] * qtd for produto, qtd in itens)
    desconto = round(subtotal * percentual_cupom / 100)
    frete_gratis = subtotal >= LIMITE_FRETE_GRATIS_EM_CENTAVOS
    frete = 0 if frete_gratis else FRETE_FIXO_EM_CENTAVOS
    faltante = max(0, LIMITE_FRETE_GRATIS_EM_CENTAVOS - subtotal)
    return {
        "subtotal": subtotal / 100,
        "desconto": desconto / 100,
        "frete": frete / 100,
        "freteGratis": frete_gratis,
        "valorFaltanteFreteGratis": faltante / 100,
        "total": (subtotal - desconto + frete) / 100,
    }
