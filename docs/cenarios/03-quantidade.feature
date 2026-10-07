# language: pt
@VZS-142 @quantidade
Funcionalidade: Limite de 5 unidades por produto
  Cada produto pode ter no máximo 5 unidades por pedido.
  A regra vale para a interface e para a API (CA10).

  # ------------------------------------------------------------ Interface
  @CT-QTD-01 @CA10 @interface @valor-limite @automatizado
  Cenário: Vitrine não permite adicionar a sexta unidade do mesmo produto
    Dado que estou na Verzel Store com o carrinho vazio
    Quando clico 5 vezes em "Adicionar ao carrinho" no produto "Mochila Urbana 20L"
    Então vejo no produto o aviso "Limite de 5 unidades atingido."
    E o botão "Adicionar ao carrinho" do produto fica desabilitado
    E o contador do carrinho exibe 5

  @CT-QTD-02 @CA10 @interface @valor-limite @automatizado
  Cenário: Carrinho não permite aumentar a quantidade acima de 5
    Dado que adicionei 5 unidades de "Mochila Urbana 20L" ao carrinho
    Quando acesso o carrinho
    Então a quantidade exibida de "Mochila Urbana 20L" é 5
    E o botão de aumentar a quantidade está desabilitado

  @CT-QTD-03 @CA10 @interface @valor-limite
  Cenário: Carrinho não permite diminuir a quantidade abaixo de 1
    Dado que adicionei 1 unidade de "Mochila Urbana 20L" ao carrinho
    Quando acesso o carrinho
    Então o botão de diminuir a quantidade está desabilitado

  @CT-QTD-04 @CA10 @interface
  Cenário: O limite é por produto, não pelo total de itens do carrinho
    Dado que adicionei 5 unidades de "Mochila Urbana 20L" ao carrinho
    Quando adiciono 5 unidades de "Garrafa Térmica 750ml" ao carrinho
    Então o contador do carrinho exibe 10
    E o subtotal exibido no carrinho é "R$ 750,00"

  @CT-QTD-05 @CA10 @interface
  Cenário: Limite continua valendo depois de voltar do carrinho para a vitrine
    Dado que adicionei 5 unidades de "Mochila Urbana 20L" ao carrinho
    Quando acesso o carrinho
    E volto para a vitrine
    Então o botão "Adicionar ao carrinho" do produto "Mochila Urbana 20L" está desabilitado

  # ------------------------------------------------------------------ API
  @CT-QTD-06 @CA10 @api @valor-limite @automatizado
  Cenário: API calcula o carrinho com 5 unidades de um produto
    Quando envio POST /api/carrinho/calcular com 5 unidades do produto "P001"
    Então a resposta tem status 200
    E o subtotal é 299.5

  @CT-QTD-07 @CA10 @api @valor-limite @automatizado
  Cenário: API recusa o cálculo do carrinho com 6 unidades de um produto
    Quando envio POST /api/carrinho/calcular com 6 unidades do produto "P001"
    Então a resposta tem status 422
    E o código do erro é "QUANTIDADE_MAXIMA_EXCEDIDA"

  @CT-QTD-08 @CA10 @api @valor-limite @automatizado
  Cenário: API recusa o pedido com 6 unidades de um produto
    Quando envio POST /api/pedidos com cliente válido e 6 unidades do produto "P001"
    Então a resposta tem status 422
    E o código do erro é "QUANTIDADE_MAXIMA_EXCEDIDA"

  @CT-QTD-09 @CA10 @api @automatizado
  Esquema do Cenário: API recusa quantidade que não é um inteiro maior ou igual a 1
    Quando envio POST /api/carrinho/calcular com quantidade <quantidade> do produto "P001"
    Então a resposta tem status 422
    E o código do erro é "QUANTIDADE_INVALIDA"
    E o campo do erro é "itens[0].quantidade"

    Exemplos:
      | quantidade | caso                 |
      | 0          | zero                 |
      | -1         | negativa             |
      | 1.5        | decimal              |
      | "2"        | texto em vez de número |
      | null       | nula                 |
