# language: pt
@VZS-142 @api @carrinho
Funcionalidade: API de cálculo do carrinho
  POST /api/carrinho/calcular calcula o carrinho sem gravar nada.
  O cupom é opcional. Cupom inválido ou expirado não gera erro: a resposta
  é 200, sem desconto, com o motivo em cupom.mensagem.

  # ----------------------------------------------------------------- Cupom
  @CT-APC-01 @CA01 @api @automatizado
  Cenário: Cupom BEMVINDO10 aplica 10% sobre o subtotal
    Quando envio POST /api/carrinho/calcular com 1 unidade do produto "P005" e o cupom "BEMVINDO10"
    Então a resposta tem status 200
    E os valores calculados são:
      | subtotal | desconto | frete | freteGratis | valorFaltanteFreteGratis | total |
      | 100      | 10       | 19.9  | false       | 100                      | 109.9 |
    E o cupom retornado tem código "BEMVINDO10" e aplicado "true"

  @CT-APC-02 @CA02 @api @automatizado
  Esquema do Cenário: Código do cupom ignora caixa e espaços nas pontas
    Quando envio POST /api/carrinho/calcular com 1 unidade do produto "P005" e o cupom "<cupom>"
    Então o desconto é 10
    E o cupom retornado tem código "BEMVINDO10" e aplicado "true"

    # O símbolo ␣ representa um espaço em branco.
    Exemplos:
      | cupom          |
      | bemvindo10     |
      | BemVindo10     |
      | ␣␣BEMVINDO10␣␣ |
      | ␣bemvindo10␣   |

  @CT-APC-03 @CA03 @api @automatizado
  Cenário: Cupom inexistente responde 200 sem desconto
    Quando envio POST /api/carrinho/calcular com 1 unidade do produto "P005" e o cupom "XPTO"
    Então a resposta tem status 200
    E o desconto é 0
    E o total é 119.9
    E o cupom retornado tem aplicado "false" e mensagem "Cupom inválido."

  @CT-APC-04 @CA04 @api @automatizado
  Cenário: Cupom expirado responde 200 sem desconto
    Quando envio POST /api/carrinho/calcular com 1 unidade do produto "P005" e o cupom "VERAO2026"
    Então a resposta tem status 200
    E o desconto é 0
    E o total é 119.9
    E o cupom retornado tem aplicado "false" e mensagem "Cupom expirado."

  @CT-APC-05 @CA01 @api @automatizado
  Cenário: Cálculo sem o campo cupom não aplica desconto
    Quando envio POST /api/carrinho/calcular com 1 unidade do produto "P005" e sem cupom
    Então a resposta tem status 200
    E o desconto é 0
    E o cupom retornado é nulo

  # ----------------------------------------------------------------- Frete
  @CT-APC-06 @CA06 @CA07 @api @valor-limite @automatizado
  Esquema do Cenário: Frete conforme o subtotal
    Quando envio POST /api/carrinho/calcular com os itens <itens>
    Então os valores calculados são:
      | subtotal   | frete   | freteGratis   | valorFaltanteFreteGratis | total   |
      | <subtotal> | <frete> | <freteGratis> | <faltante>               | <total> |

    Exemplos:
      | itens              | subtotal | frete | freteGratis | faltante | total | caso                    |
      | P001 x1            | 59.9     | 19.9  | false       | 140.1    | 79.8  | bem abaixo do limite    |
      | P002 x1 + P006 x2  | 199.7    | 19.9  | false       | 0.3      | 219.6 | logo abaixo do limite   |
      | P005 x2            | 200      | 0     | true        | 0        | 200   | exatamente no limite    |
      | P008 x4            | 200      | 0     | true        | 0        | 200   | exatamente no limite    |
      | P003 x1 + P006 x1  | 219.8    | 0     | true        | 0        | 219.8 | logo acima do limite    |
      | P007 x1            | 229.9    | 0     | true        | 0        | 229.9 | acima do limite         |

  @CT-APC-07 @CA08 @api @automatizado
  Cenário: Frete grátis considera o subtotal antes do desconto
    Quando envio POST /api/carrinho/calcular com os itens P003 x1 + P006 x1 e o cupom "BEMVINDO10"
    Então os valores calculados são:
      | subtotal | desconto | frete | freteGratis | total  |
      | 219.8    | 21.98    | 0     | true        | 197.82 |

  @CT-APC-08 @CA09 @api @automatizado
  Cenário: Desconto não incide sobre o frete
    Quando envio POST /api/carrinho/calcular com 1 unidade do produto "P001" e o cupom "BEMVINDO10"
    Então o desconto é 5.99
    E o frete é 19.9
    E o total é 73.81

  # ---------------------------------------------------- Validação de itens
  @CT-APC-09 @api @automatizado
  Esquema do Cenário: Lista de itens ausente ou vazia devolve 422 ITENS_OBRIGATORIOS
    Quando envio POST /api/carrinho/calcular com o corpo <corpo>
    Então a resposta tem status 422
    E o código do erro é "ITENS_OBRIGATORIOS"

    Exemplos:
      | corpo            |
      | {}               |
      | { "itens": [] }  |

  @CT-APC-10 @api @automatizado
  Cenário: Item que não é um objeto com produtoId e quantidade devolve 422 ITEM_INVALIDO
    Quando envio POST /api/carrinho/calcular com o corpo { "itens": ["P001"] }
    Então a resposta tem status 422
    E o código do erro é "ITEM_INVALIDO"

  @CT-APC-11 @api @automatizado
  Cenário: Item com produto inexistente devolve 422 PRODUTO_NAO_ENCONTRADO
    Quando envio POST /api/carrinho/calcular com 1 unidade do produto "P999"
    Então a resposta tem status 422
    E o código do erro é "PRODUTO_NAO_ENCONTRADO"
    E o campo do erro é "itens[0].produtoId"

  @CT-APC-12 @api @automatizado
  Cenário: Mesmo produto repetido na lista devolve 422 ITEM_DUPLICADO
    Quando envio POST /api/carrinho/calcular com o produto "P001" em dois itens
    Então a resposta tem status 422
    E o código do erro é "ITEM_DUPLICADO"

  @CT-APC-13 @api
  Cenário: Cálculo não grava nada entre uma chamada e outra
    Quando envio duas vezes o mesmo POST /api/carrinho/calcular
    Então as duas respostas são idênticas
