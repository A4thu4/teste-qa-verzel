"""Page Objects da Verzel Store.

Um Page Object reúne em uma classe os seletores e as ações de uma tela. Os
testes passam a ler como passos de negócio ("aplicar cupom", "confirmar
pedido") e, se a tela mudar, o ajuste é feito em um lugar só.

Preferência de seletores, do mais para o menos estável:
1. papel e nome acessível (get_by_role, get_by_label), que é como o usuário
   e um leitor de tela encontram o elemento;
2. atributos feitos para teste (aqui, data-valor no resumo do pedido);
3. classes CSS, só quando não há alternativa.
"""

import re

from playwright.sync_api import Locator, Page, expect


class Cabecalho:
    """Elementos do cabeçalho, presentes em todas as telas."""

    def __init__(self, page: Page):
        self.page = page
        navegacao = page.get_by_role("navigation", name="Principal")
        self.link_carrinho = navegacao.get_by_role("link", name="Carrinho")
        self.contador = page.locator(".contador-carrinho")


class Vitrine(Cabecalho):
    def abrir(self) -> None:
        self.page.goto("/")
        # A lista de produtos vem da API; espera o primeiro produto aparecer.
        expect(self.page.get_by_role("article").first).to_be_visible()

    def produto(self, nome: str) -> Locator:
        return self.page.get_by_role("article", name=nome)

    def botao_adicionar(self, nome: str) -> Locator:
        return self.produto(nome).get_by_role("button", name="Adicionar ao carrinho")

    def aviso(self, nome: str) -> Locator:
        return self.produto(nome).locator(".produto-aviso")

    def adicionar(self, nome: str, quantidade: int = 1) -> None:
        """Clica em "Adicionar ao carrinho" `quantidade` vezes.

        Depois de cada clique espera o contador do cabeçalho subir. Sem essa
        espera, cliques muito rápidos poderiam acontecer antes de a tela
        registrar o anterior.
        """
        inicial = int(self.contador.inner_text())
        for clique in range(1, quantidade + 1):
            self.botao_adicionar(nome).click()
            expect(self.contador).to_have_text(str(inicial + clique))

    def ir_para_o_carrinho(self) -> None:
        self.link_carrinho.click()
        expect(self.page).to_have_url(re.compile(r"/carrinho$"))


class Resumo:
    """Bloco "Resumo do pedido", igual no carrinho, checkout e confirmação."""

    def __init__(self, page: Page):
        self.page = page
        self.subtotal = page.locator('[data-valor="subtotal"]')
        self.desconto = page.locator('[data-valor="desconto"]')
        self.frete = page.locator('[data-valor="frete"]')
        self.total = page.locator('[data-valor="total"]')
        self.aviso_frete = page.locator(".aviso-frete")

    def deve_exibir(self, subtotal: str, desconto: str, frete: str, total: str) -> None:
        """Confere os quatro valores do resumo.

        `expect` repete a verificação por alguns segundos até dar certo. Isso
        cobre o intervalo em que a tela ainda espera a resposta da API, sem
        precisar de pausas fixas (time.sleep) no teste.
        """
        expect(self.subtotal).to_have_text(subtotal)
        expect(self.desconto).to_have_text(desconto)
        expect(self.frete).to_have_text(frete)
        expect(self.total).to_have_text(total)


class Carrinho(Cabecalho):
    def __init__(self, page: Page):
        super().__init__(page)
        self.resumo = Resumo(page)
        self.campo_cupom = page.get_by_label("Cupom de desconto")
        self.botao_aplicar = page.get_by_role("button", name="Aplicar cupom")
        self.botao_remover_cupom = page.get_by_role("button", name="Remover cupom")
        self.mensagem_cupom = page.locator("#mensagem-cupom")
        self.cupom_aplicado = page.locator(".cupom-aplicado")
        self.link_finalizar = page.get_by_role("link", name="Finalizar compra")

    def aplicar_cupom(self, codigo: str) -> None:
        self.campo_cupom.fill(codigo)
        self.botao_aplicar.click()

    def remover_cupom(self) -> None:
        self.botao_remover_cupom.click()

    def quantidade(self, produto: str) -> Locator:
        return self.page.locator(f'output[aria-label="Quantidade de {produto}"]')

    def botao_aumentar(self, produto: str) -> Locator:
        return self.page.get_by_role("button", name=f"Aumentar quantidade de {produto}")

    def botao_diminuir(self, produto: str) -> Locator:
        return self.page.get_by_role("button", name=f"Diminuir quantidade de {produto}")

    def finalizar_compra(self) -> None:
        self.link_finalizar.click()
        expect(self.page).to_have_url(re.compile(r"/checkout$"))


class Checkout(Cabecalho):
    def __init__(self, page: Page):
        super().__init__(page)
        self.resumo = Resumo(page)
        self.campo_nome = page.get_by_label("Nome completo")
        self.campo_email = page.get_by_label("E-mail")
        self.campo_cep = page.get_by_label("CEP")
        self.botao_confirmar = page.get_by_role("button", name="Confirmar pedido")
        self.erro_nome = page.locator("#campo-nome-erro")
        self.erro_email = page.locator("#campo-email-erro")
        self.erro_cep = page.locator("#campo-cep-erro")

    def preencher(self, nome: str, email: str, cep: str) -> None:
        self.campo_nome.fill(nome)
        self.campo_email.fill(email)
        self.campo_cep.fill(cep)

    def confirmar(self) -> None:
        self.botao_confirmar.click()

    def deve_continuar_no_checkout(self) -> None:
        expect(self.page).to_have_url(re.compile(r"/checkout$"))


class Confirmacao(Cabecalho):
    def __init__(self, page: Page):
        super().__init__(page)
        self.resumo = Resumo(page)
        self.numero_pedido = page.locator(".numero-pedido")

    def deve_estar_aberta(self) -> None:
        expect(self.page).to_have_url(re.compile(r"/pedido-confirmado$"))
        expect(self.page.get_by_text("Pedido confirmado", exact=True)).to_be_visible()
