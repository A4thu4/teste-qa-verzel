# language: pt
@VZS-142 @api @pedidos
Funcionalidade: API de pedidos
  POST /api/pedidos valida e confirma um pedido. Responde 201 com o número
  no formato VZ-000000 e o mesmo resumo de valores do cálculo do carrinho.
  Aqui um cupom inválido ou expirado gera erro 422.

  @CT-APP-01 @api @automatizado
  Cenário: Pedido válido com cupom é confirmado
    Quando envio POST /api/pedidos com cliente válido, 1 unidade do produto "P005" e o cupom "BEMVINDO10"
    Então a resposta tem status 201
    E o número do pedido tem o formato "VZ-" seguido de 6 dígitos
    E "criadoEm" é uma data e hora em formato ISO 8601
    E o CEP do cliente é devolvido sem hífen: "01310100"
    E os valores calculados são:
      | subtotal | desconto | frete | freteGratis | valorFaltanteFreteGratis | total |
      | 100      | 10       | 19.9  | false       | 100                      | 109.9 |

  @CT-APP-02 @api @automatizado
  Cenário: Pedido devolve os mesmos valores do cálculo do carrinho
    Dado o resultado de POST /api/carrinho/calcular para os itens P002 x1 + P004 x2 e o cupom "BEMVINDO10"
    Quando envio POST /api/pedidos com cliente válido e os mesmos itens e cupom
    Então a resposta tem status 201
    E subtotal, desconto, frete, freteGratis, valorFaltanteFreteGratis e total são iguais aos do cálculo

  @CT-APP-03 @CA03 @api @automatizado
  Cenário: Pedido com cupom inexistente devolve 422 CUPOM_INVALIDO
    Quando envio POST /api/pedidos com cliente válido, 1 unidade do produto "P005" e o cupom "XPTO"
    Então a resposta tem status 422
    E o código do erro é "CUPOM_INVALIDO"

  @CT-APP-04 @CA04 @api @automatizado
  Cenário: Pedido com cupom expirado devolve 422 CUPOM_EXPIRADO
    Quando envio POST /api/pedidos com cliente válido, 1 unidade do produto "P005" e o cupom "VERAO2026"
    Então a resposta tem status 422
    E o código do erro é "CUPOM_EXPIRADO"

  @CT-APP-05 @CA06 @api @valor-limite @automatizado
  Cenário: Pedido com subtotal de exatamente R$ 200,00 tem frete grátis
    Quando envio POST /api/pedidos com cliente válido e 2 unidades do produto "P005"
    Então a resposta tem status 201
    E o frete é 0
    E o total é 200

  @CT-APP-06 @api @automatizado
  Esquema do Cenário: Dados do cliente inválidos devolvem 422 DADOS_INVALIDOS
    Quando envio POST /api/pedidos com <campo> igual a "<valor>" e os demais dados válidos
    Então a resposta tem status 422
    E o código do erro é "DADOS_INVALIDOS"
    E a lista "campos" aponta "<campo apontado>"

    Exemplos:
      | campo | valor         | campo apontado | caso                    |
      | nome  | Maria         | cliente.nome   | sem sobrenome           |
      | nome  |               | cliente.nome   | vazio                   |
      | email | maria         | cliente.email  | sem arroba              |
      | email | maria@exemplo | cliente.email  | domínio sem ponto       |
      | cep   | 0131010       | cliente.cep    | 7 dígitos               |
      | cep   | 013101000     | cliente.cep    | 9 dígitos               |
      | cep   | 01310-10A     | cliente.cep    | letra no lugar de dígito |

  @CT-APP-07 @api @automatizado
  Cenário: Pedido sem os dados do cliente aponta os três campos
    Quando envio POST /api/pedidos sem o objeto "cliente"
    Então a resposta tem status 422
    E o código do erro é "DADOS_INVALIDOS"
    E a lista "campos" aponta "cliente.nome", "cliente.email" e "cliente.cep"

  @CT-APP-08 @api @automatizado
  Esquema do Cenário: CEP com 8 dígitos é aceito com ou sem hífen
    Quando envio POST /api/pedidos com cep igual a "<cep>" e os demais dados válidos
    Então a resposta tem status 201
    E o CEP do cliente é devolvido sem hífen: "01310100"

    Exemplos:
      | cep       |
      | 01310-100 |
      | 01310100  |

  @CT-APP-09 @api @automatizado
  Cenário: Pedido sem itens devolve 422 ITENS_OBRIGATORIOS
    Quando envio POST /api/pedidos com cliente válido e a lista de itens vazia
    Então a resposta tem status 422
    E o código do erro é "ITENS_OBRIGATORIOS"

  @CT-APP-10 @api
  Cenário: Número do pedido é gerado a cada confirmação
    Quando envio duas vezes o mesmo POST /api/pedidos válido
    Então as duas respostas têm status 201
    E os dois números de pedido seguem o formato "VZ-000000"
