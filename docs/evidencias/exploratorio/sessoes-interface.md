# Sessões exploratórias da interface

Executado em 09/10/2026 20:42:55 (horário de Brasília) pelo script [`automacao/explorar_interface.py`](../../../automacao/explorar_interface.py), no Chromium do Playwright. Cada tentativa começa com o carrinho vazio. A captura é o estado da tela ao fim da tentativa.

| # | Sessão | Tentativa | O que aconteceu | Captura |
| --- | --- | --- | --- | --- |
| 1 | 1 | Cupom só com espaços | mensagem: Informe um cupom. · cupom aplicado: - · subtotal R$ 100,00 · desconto R$ 0,00 · frete R$ 19,90 · total R$ 119,90 · aviso: Faltam R$ 100,00 para o frete grátis. | [ver](interface/01-sessao-1.png) |
| 2 | 1 | Cupom com caractere especial no fim (BEMVINDO10!) | mensagem: Cupom inválido. · cupom aplicado: - · subtotal R$ 100,00 · desconto R$ 0,00 · frete R$ 19,90 · total R$ 119,90 · aviso: Faltam R$ 100,00 para o frete grátis. | [ver](interface/02-sessao-1.png) |
| 3 | 1 | Cupom com número no lugar de letra (B3MVINDO10) | mensagem: Cupom inválido. · cupom aplicado: - · subtotal R$ 100,00 · desconto R$ 0,00 · frete R$ 19,90 · total R$ 119,90 · aviso: Faltam R$ 100,00 para o frete grátis. | [ver](interface/03-sessao-1.png) |
| 4 | 1 | Cupom com 200 caracteres | mensagem: Cupom inválido. · cupom aplicado: - · subtotal R$ 100,00 · desconto R$ 0,00 · frete R$ 19,90 · total R$ 119,90 · aviso: Faltam R$ 100,00 para o frete grátis. | [ver](interface/04-sessao-1.png) |
| 5 | 1 | F5 com o cupom aplicado | antes do F5: subtotal R$ 100,00 · desconto - R$ 10,00 · frete R$ 19,90 · total R$ 109,90 · aviso: Faltam R$ 100,00 para o frete grátis.<br>depois do F5: cupom aplicado: Cupom BEMVINDO10 aplicado. Remover cupom · subtotal R$ 100,00 · desconto - R$ 10,00 · frete R$ 19,90 · total R$ 109,90 · aviso: Faltam R$ 100,00 para o frete grátis. | [ver](interface/05-sessao-1.png) |
| 6 | 1 | Esvaziar o carrinho com cupom e adicionar produto de novo | depois de esvaziar e adicionar a mochila de novo: cupom aplicado: - · subtotal R$ 100,00 · desconto R$ 0,00 · frete R$ 19,90 · total R$ 119,90 · aviso: Faltam R$ 100,00 para o frete grátis. | [ver](interface/06-sessao-1.png) |
| 7 | 2 | Nome com partes de uma letra (A B) | **recusado**: Informe nome e sobrenome. | [ver](interface/07-sessao-2.png) |
| 8 | 2 | Nome com sobrenome de uma letra (Maria S) | **recusado**: Informe nome e sobrenome. | [ver](interface/08-sessao-2.png) |
| 9 | 2 | Nome só com números (123 456) | **aceito**: pedido VZ-700268 confirmado | [ver](interface/09-sessao-2.png) |
| 10 | 2 | Nome com vários espaços no meio | **aceito**: pedido VZ-113964 confirmado | [ver](interface/10-sessao-2.png) |
| 11 | 2 | E-mail com dois pontos seguidos no domínio | **aceito**: pedido VZ-286249 confirmado | [ver](interface/11-sessao-2.png) |
| 12 | 2 | E-mail com ponto no fim | **aceito**: pedido VZ-419469 confirmado | [ver](interface/12-sessao-2.png) |
| 13 | 2 | E-mail com domínio de uma letra (.c) | **aceito**: pedido VZ-363287 confirmado | [ver](interface/13-sessao-2.png) |
| 14 | 2 | CEP só com zeros | **aceito**: pedido VZ-279554 confirmado | [ver](interface/14-sessao-2.png) |
| 15 | 2 | CEP com espaços antes e depois | **aceito**: pedido VZ-897162 confirmado | [ver](interface/15-sessao-2.png) |
| 16 | 2 | CEP com pontos (01.310-100) | **recusado**: Informe um CEP com 8 dígitos. | [ver](interface/16-sessao-2.png) |
| 17 | 3 | F5 no carrinho | antes: subtotal R$ 100,00 · desconto R$ 0,00 · frete R$ 19,90 · total R$ 119,90 · aviso: Faltam R$ 100,00 para o frete grátis.<br>depois do F5: subtotal R$ 100,00 · desconto R$ 0,00 · frete R$ 19,90 · total R$ 119,90 · aviso: Faltam R$ 100,00 para o frete grátis. · contador 1 | [ver](interface/17-sessao-3.png) |
| 18 | 3 | F5 no checkout com os dados preenchidos | depois do F5: endereço /checkout · campos preenchidos: ['', '', ''] · subtotal R$ 100,00 · desconto R$ 0,00 · frete R$ 19,90 · total R$ 119,90 | [ver](interface/18-sessao-3.png) |
| 19 | 3 | F5 na confirmação do pedido | pedido VZ-847340; depois do F5: endereço /pedido-confirmado · número exibido VZ-847340 | [ver](interface/19-sessao-3.png) |
| 20 | 3 | Botão voltar depois de confirmar o pedido | depois de voltar: endereço /carrinho · título "Seu carrinho está vazio" · contador 0 | [ver](interface/20-sessao-3.png) |
| 21 | 3 | Abrir /pedido-confirmado direto, sem pedido | endereço final /pedido-confirmado · título "Nenhum pedido recente" | [ver](interface/21-sessao-3.png) |
| 22 | 3 | Cliques rápidos no botão de aumentar quantidade | 10 cliques rápidos no + a partir de 1 unidade: quantidade 5 · subtotal R$ 500,00 · desconto R$ 0,00 · frete Grátis · total R$ 500,00 | [ver](interface/22-sessao-3.png) |
| 23 | 3 | Compra completa em tela de celular | compra completa em tela de 390px: **aceito**: pedido VZ-248802 confirmado · largura da página 390px | [ver](interface/23-sessao-3.png) |
| 24 | 3 | Compra usando só o teclado | Tab até 'Adicionar ao carrinho': sim<br>Enter adicionou: contador 1<br>Tab até o link do carrinho: sim<br>Tab até 'Finalizar compra': sim<br>Tab até o campo nome: sim<br>Enter no CEP: endereço /pedido-confirmado · pedido VZ-374197 | [ver](interface/24-sessao-3.png) |
