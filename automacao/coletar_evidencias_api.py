"""Coleta evidências da API: grava requisição e resposta em arquivos Markdown.

Uso, a partir da pasta automacao:

    python coletar_evidencias_api.py

Cada chamada da lista CHAMADAS vira um arquivo em docs/evidencias/api/ com o
método, a rota, o corpo enviado, o status e o corpo recebido. O script não
julga se a resposta está certa: ele só registra o que a API respondeu. Usa
apenas a biblioteca padrão do Python.
"""

import json
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

BASE = "https://verzel-store.qa-test-verzel-store.workers.dev"
SAIDA = Path(__file__).resolve().parent.parent / "docs" / "evidencias" / "api"
CLIENTE = {"nome": "Maria Silva", "email": "maria@exemplo.com", "cep": "01310-100"}


def item(produto_id, quantidade):
    return {"produtoId": produto_id, "quantidade": quantidade}


# (nome do arquivo, o que a chamada demonstra, método, rota, corpo)
CHAMADAS = [
    ("BUG-001-calcular-200", "Subtotal de exatamente R$ 200,00 (CA06)", "POST", "/api/carrinho/calcular",
     {"itens": [item("P005", 2)]}),
    ("BUG-001-calcular-200-outro-produto", "R$ 200,00 com outro produto (CA06)", "POST", "/api/carrinho/calcular",
     {"itens": [item("P008", 4)]}),
    ("BUG-001-pedido-200", "Pedido de exatamente R$ 200,00 (CA06)", "POST", "/api/pedidos",
     {"cliente": CLIENTE, "itens": [item("P005", 2)]}),
    ("BUG-002-calcular-6-unidades", "Cálculo com 6 unidades (CA10)", "POST", "/api/carrinho/calcular",
     {"itens": [item("P001", 6)]}),
    ("BUG-002-pedido-6-unidades", "Pedido com 6 unidades (CA10)", "POST", "/api/pedidos",
     {"cliente": CLIENTE, "itens": [item("P001", 6)]}),
    ("CT-QTD-06-calcular-5-unidades", "Cálculo com 5 unidades, no limite (CA10)", "POST", "/api/carrinho/calcular",
     {"itens": [item("P001", 5)]}),
    ("CT-APC-06-calcular-199-70", "Subtotal logo abaixo do limite do frete (CA07)", "POST", "/api/carrinho/calcular",
     {"itens": [item("P002", 1), item("P006", 2)]}),
    ("CT-APC-07-frete-antes-do-desconto", "Frete pelo subtotal antes do desconto (CA08)", "POST", "/api/carrinho/calcular",
     {"itens": [item("P003", 1), item("P006", 1)], "cupom": "BEMVINDO10"}),
    ("CT-CAL-01-exemplo-da-documentacao", "Exemplo de cálculo da documentação", "POST", "/api/carrinho/calcular",
     {"itens": [item("P002", 1), item("P004", 2)], "cupom": "BEMVINDO10"}),
    ("CT-APC-02-cupom-minusculas-com-espacos", "Cupom em minúsculas e com espaços (CA02)", "POST", "/api/carrinho/calcular",
     {"itens": [item("P005", 1)], "cupom": " bemvindo10 "}),
    ("CT-APC-03-cupom-inexistente", "Cupom inexistente no cálculo (CA03)", "POST", "/api/carrinho/calcular",
     {"itens": [item("P005", 1)], "cupom": "XPTO"}),
    ("CT-APC-04-cupom-expirado", "Cupom expirado no cálculo (CA04)", "POST", "/api/carrinho/calcular",
     {"itens": [item("P005", 1)], "cupom": "VERAO2026"}),
    ("CT-APP-01-pedido-com-cupom", "Pedido válido com cupom", "POST", "/api/pedidos",
     {"cliente": CLIENTE, "itens": [item("P005", 1)], "cupom": "BEMVINDO10"}),
    ("CT-APP-04-pedido-cupom-expirado", "Pedido com cupom expirado (CA04)", "POST", "/api/pedidos",
     {"cliente": CLIENTE, "itens": [item("P005", 1)], "cupom": "VERAO2026"}),
    ("CT-API-01-listar-produtos", "Lista de produtos", "GET", "/api/produtos", None),
    ("CT-API-03-produto-inexistente", "Produto inexistente", "GET", "/api/produtos/P999", None),
]


def chamar(metodo, rota, corpo):
    dados = json.dumps(corpo).encode("utf-8") if corpo is not None else None
    requisicao = urllib.request.Request(
        BASE + rota,
        data=dados,
        method=metodo,
        headers={"Content-Type": "application/json", "User-Agent": "teste-qa-verzel"},
    )
    try:
        with urllib.request.urlopen(requisicao, timeout=30) as resposta:
            return resposta.status, resposta.read().decode("utf-8")
    except urllib.error.HTTPError as erro:
        # Status 4xx chega como exceção, mas para o teste é uma resposta válida.
        return erro.code, erro.read().decode("utf-8")


def formatar(texto):
    try:
        return json.dumps(json.loads(texto), ensure_ascii=False, indent=2)
    except ValueError:
        return texto


def main():
    SAIDA.mkdir(parents=True, exist_ok=True)
    for nome, descricao, metodo, rota, corpo in CHAMADAS:
        status, texto = chamar(metodo, rota, corpo)
        partes = [
            f"# {nome}",
            "",
            descricao,
            "",
            f"Coletado em {datetime.now():%d/%m/%Y %H:%M:%S}",
            "",
            "## Requisição",
            "",
            "```",
            f"{metodo} {rota}",
            "```",
        ]
        if corpo is not None:
            partes += ["", "```json", json.dumps(corpo, ensure_ascii=False, indent=2), "```"]
        partes += ["", f"## Resposta: status {status}", "", "```json", formatar(texto), "```", ""]
        (SAIDA / f"{nome}.md").write_text("\n".join(partes), encoding="utf-8")
        print(f"{status}  {metodo:4} {rota:28} -> {nome}.md")


if __name__ == "__main__":
    main()
