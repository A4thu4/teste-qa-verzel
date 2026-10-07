# language: pt
@regressao @checkout
Funcionalidade: Finalização da compra
  Regras que já existiam antes da entrega VZS-142 e não podem ter sido quebradas:
  nome com nome e sobrenome, e-mail em formato válido, CEP com 8 dígitos
  (com ou sem hífen) e pagamento feito na entrega.

  Contexto:
    Dado que adicionei 1 unidade de "Mochila Urbana 20L" ao carrinho
    E que estou na página "Finalizar compra"

  # --------------------------------------------------------- Caminho feliz
  @CT-CHK-01 @interface @automatizado
  Cenário: Pedido é confirmado com dados válidos
    Quando preencho o nome "Maria Silva", o e-mail "maria@exemplo.com" e o CEP "01310-100"
    E confirmo o pedido
    Então sou levado para a página "Pedido confirmado"
    E vejo um número de pedido no formato "VZ-000000"
    E a página de confirmação exibe:
      | Subtotal  | Desconto | Frete    | Total     |
      | R$ 100,00 | R$ 0,00  | R$ 19,90 | R$ 119,90 |
    E o contador do carrinho exibe 0

  @CT-CHK-02 @interface
  Cenário: Resumo do checkout repete os valores e os itens do carrinho
    Então o resumo do pedido exibe:
      | Subtotal  | Desconto | Frete    | Total     |
      | R$ 100,00 | R$ 0,00  | R$ 19,90 | R$ 119,90 |
    E a lista de itens do resumo contém "1x Mochila Urbana 20L" com "R$ 100,00"

  @CT-CHK-03 @interface
  Cenário: Checkout informa que o pagamento é feito na entrega
    Então vejo o texto "O pagamento é feito na entrega."
    E não existe campo de dados de pagamento

  # ------------------------------------------------------------------ Nome
  @CT-CHK-04 @interface @automatizado
  Esquema do Cenário: Nome sem sobrenome é recusado
    Quando preencho o nome "<nome>", o e-mail "maria@exemplo.com" e o CEP "01310-100"
    E confirmo o pedido
    Então vejo no campo nome a mensagem "<mensagem>"
    E continuo na página "Finalizar compra"

    Exemplos:
      | nome   | mensagem                  | caso                         |
      |        | Informe o nome completo.  | campo vazio                  |
      | Maria  | Informe nome e sobrenome. | só o primeiro nome           |
      | Maria␣ | Informe nome e sobrenome. | primeiro nome seguido de espaço |

  @CT-CHK-05 @interface
  Esquema do Cenário: Nome com nome e sobrenome é aceito
    Quando preencho o nome "<nome>", o e-mail "maria@exemplo.com" e o CEP "01310-100"
    E confirmo o pedido
    Então sou levado para a página "Pedido confirmado"

    Exemplos:
      | nome            | caso                      |
      | Maria Silva     | nome e sobrenome          |
      | Maria da Silva  | três partes               |
      | João Conceição  | com acentos               |
      | Ana D'Ávila     | com apóstrofo             |
      | Ana-Maria Souza | com hífen                 |
      | Li Wu           | partes com duas letras    |

  # ---------------------------------------------------------------- E-mail
  @CT-CHK-06 @interface @automatizado
  Esquema do Cenário: E-mail em formato inválido é recusado
    Quando preencho o nome "Maria Silva", o e-mail "<email>" e o CEP "01310-100"
    E confirmo o pedido
    Então vejo no campo e-mail a mensagem "<mensagem>"
    E continuo na página "Finalizar compra"

    Exemplos:
      | email                   | mensagem                 | caso                |
      |                         | Informe o e-mail.        | campo vazio         |
      | maria                   | Informe um e-mail válido. | sem arroba          |
      | maria@                  | Informe um e-mail válido. | sem domínio         |
      | @exemplo.com            | Informe um e-mail válido. | sem usuário         |
      | maria@exemplo           | Informe um e-mail válido. | domínio sem ponto   |
      | maria silva@exemplo.com | Informe um e-mail válido. | com espaço no meio  |
      | maria@@exemplo.com      | Informe um e-mail válido. | duas arrobas        |

  @CT-CHK-07 @interface
  Esquema do Cenário: E-mail em formato válido é aceito
    Quando preencho o nome "Maria Silva", o e-mail "<email>" e o CEP "01310-100"
    E confirmo o pedido
    Então sou levado para a página "Pedido confirmado"

    Exemplos:
      | email                                | caso                     |
      | maria@exemplo.com                    | formato simples          |
      | maria.silva+teste@sub.exemplo.com.br | ponto, mais e subdomínio |
      | MARIA@EXEMPLO.COM                    | maiúsculas               |

  # ------------------------------------------------------------------- CEP
  @CT-CHK-08 @interface @automatizado
  Esquema do Cenário: CEP que não tem 8 dígitos é recusado
    Quando preencho o nome "Maria Silva", o e-mail "maria@exemplo.com" e o CEP "<cep>"
    E confirmo o pedido
    Então vejo no campo CEP a mensagem "<mensagem>"
    E continuo na página "Finalizar compra"

    Exemplos:
      | cep        | mensagem                     | caso                       |
      |            | Informe o CEP.               | campo vazio                |
      | 0131010    | Informe um CEP com 8 dígitos. | 7 dígitos                  |
      | 013101000  | Informe um CEP com 8 dígitos. | 9 dígitos                  |
      | 01310-10A  | Informe um CEP com 8 dígitos. | letra no lugar de dígito   |
      | 013-10100  | Informe um CEP com 8 dígitos. | hífen na posição errada    |
      | 01310 100  | Informe um CEP com 8 dígitos. | espaço no lugar do hífen   |

  @CT-CHK-09 @interface @automatizado
  Esquema do Cenário: CEP com 8 dígitos é aceito com ou sem hífen
    Quando preencho o nome "Maria Silva", o e-mail "maria@exemplo.com" e o CEP "<cep>"
    E confirmo o pedido
    Então sou levado para a página "Pedido confirmado"

    Exemplos:
      | cep       | caso      |
      | 01310-100 | com hífen |
      | 01310100  | sem hífen |

  # ---------------------------------------------------------- Vários erros
  @CT-CHK-10 @interface
  Cenário: Formulário em branco aponta os três campos obrigatórios de uma vez
    Quando confirmo o pedido sem preencher nenhum campo
    Então vejo no campo nome a mensagem "Informe o nome completo."
    E vejo no campo e-mail a mensagem "Informe o e-mail."
    E vejo no campo CEP a mensagem "Informe o CEP."

  @CT-CHK-11 @interface
  Cenário: Corrigir os dados depois de um erro permite confirmar o pedido
    Quando preencho o nome "Maria", o e-mail "maria@" e o CEP "123"
    E confirmo o pedido
    E corrijo para o nome "Maria Silva", o e-mail "maria@exemplo.com" e o CEP "01310-100"
    E confirmo o pedido
    Então sou levado para a página "Pedido confirmado"

  # ---------------------------------------------------------- Navegação
  @CT-CHK-12 @interface
  Cenário: Checkout não fica acessível com o carrinho vazio
    Dado que esvaziei o carrinho
    Quando acesso o endereço "/checkout" diretamente
    Então vejo a mensagem "Seu carrinho está vazio"
