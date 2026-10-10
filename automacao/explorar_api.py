"""Sessões exploratórias da API: envia as requisições "fora do roteiro" e
grava tudo em um único relatório Markdown.

Uso, a partir da pasta automacao:

    python explorar_api.py

Gera docs/evidencias/exploratorio/sessoes-api.md com uma tabela-resumo e, para
cada tentativa, a requisição enviada, o status, o Content-Type e o corpo da
resposta. Assim como o coletar_evidencias_api.py, o script não julga se a
resposta está certa: ele registra o que aconteceu, e a análise vai para as
anotações das sessões em docs/02-execucao-dos-testes.md.

Diferente do outro script, este precisa enviar requisições "malformadas" de
propósito (sem Content-Type, corpo que não é JSON), por isso monta cada uma à
mão. Usa apenas a biblioteca padrão do Python.
"""

import json
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

BASE = "https://verzel-store.qa-test-verzel-store.workers.dev"
SAIDA = Path(__file__).resolve().parent.parent / "docs" / "evidencias" / "exploratorio" / "sessoes-api.md"
BRASILIA = timezone(timedelta(hours=-3))  # sem horário de verão desde 2019
JSON = {"Content-Type": "application/json"}


def item(produto_id, quantidade):
    return {"produtoId": produto_id, "quantidade": quantidade}


# (sessão, o que está sendo explorado, método, rota, cabeçalhos, corpo)
# O corpo pode ser um objeto Python (enviado como JSON), um texto (enviado
# exatamente como está) ou None (sem corpo).
TENTATIVAS = [
    # Sessão 1: entradas inesperadas no cupom
    ("1", "Cupom só com espaços", "POST", "/api/carrinho/calcular", JSON,
     {"itens": [item("P005", 1)], "cupom": "   "}),
    ("1", "Cupom como número", "POST", "/api/carrinho/calcular", JSON,
     {"itens": [item("P005", 1)], "cupom": 123}),
    ("1", "Cupom como lista", "POST", "/api/carrinho/calcular", JSON,
     {"itens": [item("P005", 1)], "cupom": ["BEMVINDO10"]}),
    ("1", "Cupom muito longo (200 caracteres)", "POST", "/api/carrinho/calcular", JSON,
     {"itens": [item("P005", 1)], "cupom": "BEMVINDO10" * 20}),
    ("1", "Cupom com caractere especial no fim", "POST", "/api/carrinho/calcular", JSON,
     {"itens": [item("P005", 1)], "cupom": "BEMVINDO10!"}),
    ("1", "Cupom só com espaços no pedido", "POST", "/api/pedidos", JSON,
     {"cliente": {"nome": "Maria Silva", "email": "maria@exemplo.com", "cep": "01310-100"},
      "itens": [item("P005", 1)], "cupom": "   "}),
    # Sessão 4: contrato da API
    ("4", "Raiz da API, sem caminho", "GET", "/api", {}, None),
    ("4", "Lista de produtos com barra no fim", "GET", "/api/produtos/", {}, None),
    ("4", "Produto com barra no fim", "GET", "/api/produtos/P001/", {}, None),
    # O urllib preenche sozinho um Content-Type de formulário quando a requisição
    # tem corpo e nenhum é informado; aqui ele fica explícito para o relatório
    # mostrar exatamente o que foi enviado.
    ("4", "Cálculo com Content-Type de formulário em vez de JSON", "POST", "/api/carrinho/calcular",
     {"Content-Type": "application/x-www-form-urlencoded"}, json.dumps({"itens": [item("P005", 1)]})),
    ("4", "Cálculo com Content-Type text/plain", "POST", "/api/carrinho/calcular",
     {"Content-Type": "text/plain"}, json.dumps({"itens": [item("P005", 1)]})),
    ("4", "Campo extra no corpo", "POST", "/api/carrinho/calcular", JSON,
     {"itens": [item("P005", 1)], "teste": 1}),
    ("4", "Campo extra dentro do item", "POST", "/api/carrinho/calcular", JSON,
     {"itens": [{"produtoId": "P005", "quantidade": 1, "preco": 1}]}),
    ("4", "produtoId em minúsculas", "POST", "/api/carrinho/calcular", JSON,
     {"itens": [item("p001", 1)]}),
    ("4", "Consulta de produto com id em minúsculas", "GET", "/api/produtos/p001", {}, None),
    ("4", "Quantidade muito grande", "POST", "/api/carrinho/calcular", JSON,
     {"itens": [item("P001", 1000000)]}),
    ("4", "Formato do erro 400 (corpo que não é JSON)", "POST", "/api/carrinho/calcular", JSON, "nao e json"),
    ("4", "Formato do erro 404 (rota inexistente)", "GET", "/api/rota-que-nao-existe", {}, None),
    ("4", "Formato do erro 404 (produto inexistente)", "GET", "/api/produtos/P999", {}, None),
    ("4", "Formato do erro 405 (método não permitido)", "DELETE", "/api/produtos", {}, None),
    ("4", "Formato do erro 422 (quantidade inválida)", "POST", "/api/carrinho/calcular", JSON,
     {"itens": [item("P001", 0)]}),
]


def enviar(metodo, rota, cabecalhos, corpo):
    if corpo is None:
        dados = None
    elif isinstance(corpo, str):
        dados = corpo.encode("utf-8")
    else:
        dados = json.dumps(corpo).encode("utf-8")
    requisicao = urllib.request.Request(
        BASE + rota,
        data=dados,
        method=metodo,
        headers={"User-Agent": "teste-qa-verzel", **cabecalhos},
    )
    try:
        with urllib.request.urlopen(requisicao, timeout=30) as resposta:
            return resposta.status, resposta.headers.get("Content-Type"), resposta.read().decode("utf-8")
    except urllib.error.HTTPError as erro:
        # Status 4xx chega como exceção, mas aqui é uma resposta como outra qualquer.
        return erro.code, erro.headers.get("Content-Type"), erro.read().decode("utf-8")


def resumir(texto):
    """Uma linha com o que interessa na resposta, para a tabela do topo."""
    try:
        corpo = json.loads(texto)
    except ValueError:
        return f"não é JSON ({len(texto)} caracteres)"
    if isinstance(corpo, dict) and "erro" in corpo:
        erro = corpo["erro"]
        chaves = ", ".join(erro)
        return f"erro {erro.get('codigo')} · chaves: {chaves}"
    if isinstance(corpo, dict) and "subtotal" in corpo:
        cupom = corpo.get("cupom")
        sobre_cupom = f" · cupom: {cupom.get('mensagem')}" if isinstance(cupom, dict) else ""
        return f"subtotal {corpo['subtotal']} · desconto {corpo['desconto']} · total {corpo['total']}{sobre_cupom}"
    if isinstance(corpo, dict) and "numero" in corpo:
        return f"pedido {corpo['numero']} criado"
    if isinstance(corpo, list):
        return f"lista com {len(corpo)} itens"
    return "JSON " + type(corpo).__name__


def formatar(texto):
    try:
        return "json", json.dumps(json.loads(texto), ensure_ascii=False, indent=2)
    except ValueError:
        # Respostas que não são JSON (HTML, por exemplo) são cortadas: o que
        # importa é saber o que veio, não guardar a página inteira.
        return "text", texto if len(texto) <= 500 else texto[:500] + "\n... (cortado)"


def main():
    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    resultados = []
    for numero, (sessao, descricao, metodo, rota, cabecalhos, corpo) in enumerate(TENTATIVAS, start=1):
        status, tipo, texto = enviar(metodo, rota, cabecalhos, corpo)
        resultados.append((numero, sessao, descricao, metodo, rota, cabecalhos, corpo, status, tipo, texto))
        print(f"{numero:2}. sessão {sessao} · {status} · {descricao}")

    linhas = [
        "# Sessões exploratórias da API",
        "",
        f"Executado em {datetime.now(BRASILIA):%d/%m/%Y %H:%M:%S} (horário de Brasília) "
        "pelo script [`automacao/explorar_api.py`](../../../automacao/explorar_api.py).",
        "",
        "## Resumo",
        "",
        "| # | Sessão | Tentativa | Requisição | Status | Resultado |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for numero, sessao, descricao, metodo, rota, _, _, status, _, texto in resultados:
        linhas.append(f"| {numero} | {sessao} | {descricao} | `{metodo} {rota}` | {status} | {resumir(texto)} |")

    linhas += ["", "## Detalhes"]
    for numero, sessao, descricao, metodo, rota, cabecalhos, corpo, status, tipo, texto in resultados:
        linhas += ["", f"### {numero}. {descricao}", "", "```", f"{metodo} {rota}"]
        linhas += [f"{nome}: {valor}" for nome, valor in cabecalhos.items()] or ["(sem cabeçalho Content-Type)"]
        linhas += ["```"]
        if corpo is not None:
            enviado = corpo if isinstance(corpo, str) else json.dumps(corpo, ensure_ascii=False, indent=2)
            linhas += ["", "Corpo enviado:", "", "```", enviado, "```"]
        linguagem, recebido = formatar(texto)
        linhas += ["", f"Resposta: status {status} · Content-Type: `{tipo}`", "", f"```{linguagem}", recebido, "```"]

    SAIDA.write_text("\n".join(linhas) + "\n", encoding="utf-8")
    print(f"\nRelatório gravado em {SAIDA}")


if __name__ == "__main__":
    main()
