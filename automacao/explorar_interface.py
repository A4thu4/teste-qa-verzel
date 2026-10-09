"""Sessões exploratórias da interface: executa as tentativas fora do roteiro
no navegador, tira uma captura de cada uma e grava um relatório Markdown.

Uso, a partir da pasta automacao:

    python explorar_interface.py            # navegador invisível (Codespace)
    python explorar_interface.py --headed   # navegador visível (Windows)

Gera docs/evidencias/exploratorio/sessoes-interface.md e as capturas em
docs/evidencias/exploratorio/interface/.

Este script não é um teste: ele não tem resultado esperado nem diz se algo
passou ou falhou. Ele registra o que a loja fez em cada tentativa (endereço,
mensagens na tela, valores do resumo), e a análise vai para as anotações das
sessões em docs/02-execucao-dos-testes.md. Se uma tentativa der erro, o erro
fica registrado e as próximas continuam.

Cada tentativa usa um contexto de navegador novo, então começa com o carrinho
vazio e não interfere nas outras.
"""

import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from playwright.sync_api import Page, sync_playwright

from pages.loja import Carrinho, Checkout, Vitrine

BASE = "https://verzel-store.qa-test-verzel-store.workers.dev"
RAIZ = Path(__file__).resolve().parent.parent / "docs" / "evidencias" / "exploratorio"
PASTA_PRINTS = RAIZ / "interface"
RELATORIO = RAIZ / "sessoes-interface.md"
BRASILIA = timezone(timedelta(hours=-3))  # sem horário de verão desde 2019
CELULAR = {"width": 390, "height": 844}

NOME, EMAIL, CEP = "Maria Silva", "maria@exemplo.com", "01310-100"
MOCHILA = "Mochila Urbana 20L"


# ------------------------------------------------------------- utilitários


def texto_ou_nada(page: Page, seletor: str) -> str:
    """Texto do primeiro elemento que casa com o seletor, ou "-" se não existir."""
    elementos = page.locator(seletor)
    if elementos.count() == 0:
        return "-"
    return " ".join(elementos.first.inner_text().split())


def resumo_do_pedido(page: Page) -> str:
    partes = []
    for campo in ["subtotal", "desconto", "frete", "total"]:
        partes.append(f"{campo} {texto_ou_nada(page, f'[data-valor={campo!r}]')}")
    aviso = texto_ou_nada(page, ".aviso-frete")
    if aviso != "-":
        partes.append(f"aviso: {aviso}")
    return " · ".join(partes)


def caminho(page: Page) -> str:
    return re.sub(r"^https?://[^/]+", "", page.url) or "/"


def carrinho_com_mochila(page: Page) -> Carrinho:
    vitrine = Vitrine(page)
    vitrine.abrir()
    vitrine.adicionar(MOCHILA)
    vitrine.ir_para_o_carrinho()
    return Carrinho(page)


def checkout_com_mochila(page: Page) -> Checkout:
    carrinho_com_mochila(page).finalizar_compra()
    return Checkout(page)


def enviar_dados(page: Page, nome: str, email: str, cep: str) -> str:
    """Preenche o checkout, confirma e descreve o que aconteceu."""
    checkout = checkout_com_mochila(page)
    checkout.preencher(nome, email, cep)
    checkout.confirmar()
    try:
        page.wait_for_url(re.compile(r"/pedido-confirmado$"), timeout=5000)
        return f"**aceito**: pedido {texto_ou_nada(page, '.numero-pedido')} confirmado"
    except Exception:
        erros = [" ".join(e.split()) for e in page.locator(".mensagem-erro").all_inner_texts()]
        return "**recusado**: " + ("; ".join(erros) if erros else "nenhuma mensagem de erro visível")


# ------------------------------------------------------------- tentativas
# Cada tentativa recebe uma página nova e devolve o texto do resultado.


def s1_cupom(codigo):
    def tentativa(page: Page) -> str:
        carrinho = carrinho_com_mochila(page)
        carrinho.aplicar_cupom(codigo)
        page.wait_for_timeout(1500)
        mensagem = texto_ou_nada(page, "#mensagem-cupom")
        aplicado = texto_ou_nada(page, ".cupom-aplicado")
        return f"mensagem: {mensagem} · cupom aplicado: {aplicado} · {resumo_do_pedido(page)}"
    return tentativa


def s1_f5_com_cupom(page: Page) -> str:
    carrinho = carrinho_com_mochila(page)
    carrinho.aplicar_cupom("BEMVINDO10")
    page.wait_for_timeout(1500)
    antes = resumo_do_pedido(page)
    page.reload()
    page.wait_for_timeout(2000)
    return f"antes do F5: {antes}<br>depois do F5: cupom aplicado: {texto_ou_nada(page, '.cupom-aplicado')} · {resumo_do_pedido(page)}"


def s1_esvaziar_com_cupom(page: Page) -> str:
    carrinho = carrinho_com_mochila(page)
    carrinho.aplicar_cupom("BEMVINDO10")
    page.wait_for_timeout(1500)
    page.once("dialog", lambda dialogo: dialogo.accept())
    page.get_by_role("button", name="Esvaziar carrinho").click()
    page.wait_for_timeout(1000)
    vitrine = Vitrine(page)
    vitrine.abrir()
    vitrine.adicionar(MOCHILA)
    vitrine.ir_para_o_carrinho()
    page.wait_for_timeout(1500)
    return (f"depois de esvaziar e adicionar a mochila de novo: cupom aplicado: "
            f"{texto_ou_nada(page, '.cupom-aplicado')} · {resumo_do_pedido(page)}")


def s2_dados(nome=NOME, email=EMAIL, cep=CEP):
    def tentativa(page: Page) -> str:
        return enviar_dados(page, nome, email, cep)
    return tentativa


def s3_f5_carrinho(page: Page) -> str:
    carrinho_com_mochila(page)
    antes = resumo_do_pedido(page)
    page.reload()
    page.wait_for_timeout(2000)
    return f"antes: {antes}<br>depois do F5: {resumo_do_pedido(page)} · contador {texto_ou_nada(page, '.contador-carrinho')}"


def s3_f5_checkout(page: Page) -> str:
    checkout = checkout_com_mochila(page)
    checkout.preencher(NOME, EMAIL, CEP)
    page.reload()
    page.wait_for_timeout(2000)
    valores = [page.locator(f"#campo-{c}").input_value() if page.locator(f"#campo-{c}").count() else "-"
               for c in ["nome", "email", "cep"]]
    return f"depois do F5: endereço {caminho(page)} · campos preenchidos: {valores} · {resumo_do_pedido(page)}"


def s3_f5_confirmacao(page: Page) -> str:
    enviar_dados(page, NOME, EMAIL, CEP)
    numero = texto_ou_nada(page, ".numero-pedido")
    page.reload()
    page.wait_for_timeout(2000)
    return f"pedido {numero}; depois do F5: endereço {caminho(page)} · número exibido {texto_ou_nada(page, '.numero-pedido')}"


def s3_voltar_depois_de_confirmar(page: Page) -> str:
    enviar_dados(page, NOME, EMAIL, CEP)
    page.go_back()
    page.wait_for_timeout(2000)
    titulo = texto_ou_nada(page, "main h1")
    return f"depois de voltar: endereço {caminho(page)} · título \"{titulo}\" · contador {texto_ou_nada(page, '.contador-carrinho')}"


def s3_confirmacao_direta(page: Page) -> str:
    page.goto("/pedido-confirmado")
    page.wait_for_timeout(2000)
    return f"endereço final {caminho(page)} · título \"{texto_ou_nada(page, 'main h1')}\""


def s3_cliques_rapidos(page: Page) -> str:
    carrinho_com_mochila(page)
    botao = page.get_by_role("button", name=f"Aumentar quantidade de {MOCHILA}")
    for _ in range(10):
        if botao.is_enabled():
            botao.click(no_wait_after=True)
    page.wait_for_timeout(3000)
    quantidade = texto_ou_nada(page, f'output[aria-label="Quantidade de {MOCHILA}"]')
    return f"10 cliques rápidos no + a partir de 1 unidade: quantidade {quantidade} · {resumo_do_pedido(page)}"


def s3_celular(page: Page) -> str:
    resultado = enviar_dados(page, NOME, EMAIL, CEP)
    largura = page.evaluate("document.documentElement.scrollWidth")
    return f"compra completa em tela de {CELULAR['width']}px: {resultado} · largura da página {largura}px"


def s3_teclado(page: Page) -> str:
    """Compra usando só Tab, digitação e Enter. Nenhum clique."""
    def tab_ate(condicao_js: str, limite: int = 60) -> bool:
        for _ in range(limite):
            page.keyboard.press("Tab")
            if page.evaluate(condicao_js):
                return True
        return False

    passos = []
    page.goto("/")
    page.get_by_role("article").first.wait_for()
    achou = tab_ate("document.activeElement?.textContent?.trim() === 'Adicionar ao carrinho'")
    passos.append(f"Tab até 'Adicionar ao carrinho': {'sim' if achou else 'não'}")
    if not achou:
        return "<br>".join(passos)
    page.keyboard.press("Enter")
    page.wait_for_timeout(800)
    passos.append(f"Enter adicionou: contador {texto_ou_nada(page, '.contador-carrinho')}")

    achou = tab_ate("document.activeElement?.classList?.contains('link-carrinho')")
    passos.append(f"Tab até o link do carrinho: {'sim' if achou else 'não'}")
    if not achou:
        return "<br>".join(passos)
    page.keyboard.press("Enter")
    page.wait_for_timeout(1500)

    achou = tab_ate("document.activeElement?.textContent?.trim() === 'Finalizar compra'")
    passos.append(f"Tab até 'Finalizar compra': {'sim' if achou else 'não'}")
    if not achou:
        return "<br>".join(passos)
    page.keyboard.press("Enter")
    page.wait_for_timeout(1500)

    achou = tab_ate("document.activeElement?.id === 'campo-nome'")
    passos.append(f"Tab até o campo nome: {'sim' if achou else 'não'}")
    if not achou:
        return "<br>".join(passos)
    page.keyboard.type(NOME)
    page.keyboard.press("Tab")
    page.keyboard.type(EMAIL)
    page.keyboard.press("Tab")
    page.keyboard.type(CEP)
    page.keyboard.press("Enter")
    page.wait_for_timeout(3000)
    passos.append(f"Enter no CEP: endereço {caminho(page)} · pedido {texto_ou_nada(page, '.numero-pedido')}")
    return "<br>".join(passos)


# (sessão, descrição, função, viewport ou None)
TENTATIVAS = [
    ("1", "Cupom só com espaços", s1_cupom("   "), None),
    ("1", "Cupom com caractere especial no fim (BEMVINDO10!)", s1_cupom("BEMVINDO10!"), None),
    ("1", "Cupom com número no lugar de letra (B3MVINDO10)", s1_cupom("B3MVINDO10"), None),
    ("1", "Cupom com 200 caracteres", s1_cupom("BEMVINDO10" * 20), None),
    ("1", "F5 com o cupom aplicado", s1_f5_com_cupom, None),
    ("1", "Esvaziar o carrinho com cupom e adicionar produto de novo", s1_esvaziar_com_cupom, None),
    ("2", "Nome com partes de uma letra (A B)", s2_dados(nome="A B"), None),
    ("2", "Nome com sobrenome de uma letra (Maria S)", s2_dados(nome="Maria S"), None),
    ("2", "Nome só com números (123 456)", s2_dados(nome="123 456"), None),
    ("2", "Nome com vários espaços no meio", s2_dados(nome="Maria     Silva"), None),
    ("2", "E-mail com dois pontos seguidos no domínio", s2_dados(email="maria@exemplo..com"), None),
    ("2", "E-mail com ponto no fim", s2_dados(email="maria@exemplo.com."), None),
    ("2", "E-mail com domínio de uma letra (.c)", s2_dados(email="maria@exemplo.c"), None),
    ("2", "CEP só com zeros", s2_dados(cep="00000-000"), None),
    ("2", "CEP com espaços antes e depois", s2_dados(cep="  01310-100  "), None),
    ("2", "CEP com pontos (01.310-100)", s2_dados(cep="01.310-100"), None),
    ("3", "F5 no carrinho", s3_f5_carrinho, None),
    ("3", "F5 no checkout com os dados preenchidos", s3_f5_checkout, None),
    ("3", "F5 na confirmação do pedido", s3_f5_confirmacao, None),
    ("3", "Botão voltar depois de confirmar o pedido", s3_voltar_depois_de_confirmar, None),
    ("3", "Abrir /pedido-confirmado direto, sem pedido", s3_confirmacao_direta, None),
    ("3", "Cliques rápidos no botão de aumentar quantidade", s3_cliques_rapidos, None),
    ("3", "Compra completa em tela de celular", s3_celular, CELULAR),
    ("3", "Compra usando só o teclado", s3_teclado, None),
]


def main():
    headed = "--headed" in sys.argv
    PASTA_PRINTS.mkdir(parents=True, exist_ok=True)
    resultados = []
    with sync_playwright() as p:
        navegador = p.chromium.launch(headless=not headed)
        for numero, (sessao, descricao, funcao, viewport) in enumerate(TENTATIVAS, start=1):
            opcoes = {"base_url": BASE}
            if viewport:
                opcoes["viewport"] = viewport
            contexto = navegador.new_context(**opcoes)
            contexto.set_default_timeout(10000)
            page = contexto.new_page()
            try:
                resultado = funcao(page)
            except Exception as erro:
                primeira_linha = str(erro).strip().splitlines()[0] if str(erro).strip() else type(erro).__name__
                resultado = f"**não foi possível concluir a tentativa**: {primeira_linha}"
            arquivo = f"{numero:02d}-sessao-{sessao}.png"
            try:
                page.screenshot(path=str(PASTA_PRINTS / arquivo), full_page=True)
            except Exception:
                arquivo = None
            contexto.close()
            resultados.append((numero, sessao, descricao, resultado, arquivo))
            print(f"{numero:2}. sessão {sessao} · {descricao}")
        navegador.close()

    linhas = [
        "# Sessões exploratórias da interface",
        "",
        f"Executado em {datetime.now(BRASILIA):%d/%m/%Y %H:%M:%S} (horário de Brasília) pelo script "
        "[`automacao/explorar_interface.py`](../../../automacao/explorar_interface.py), no Chromium do Playwright. "
        "Cada tentativa começa com o carrinho vazio. A captura é o estado da tela ao fim da tentativa.",
        "",
        "| # | Sessão | Tentativa | O que aconteceu | Captura |",
        "| --- | --- | --- | --- | --- |",
    ]
    for numero, sessao, descricao, resultado, arquivo in resultados:
        captura = f"[ver](interface/{arquivo})" if arquivo else "-"
        linhas.append(f"| {numero} | {sessao} | {descricao} | {resultado.replace('|', '/')} | {captura} |")
    RELATORIO.write_text("\n".join(linhas) + "\n", encoding="utf-8")
    print(f"\nRelatório gravado em {RELATORIO}")


if __name__ == "__main__":
    main()
