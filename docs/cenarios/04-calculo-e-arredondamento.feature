# language: pt
@VZS-142 @calculo
Funcionalidade: Cálculo do pedido e arredondamento
  total = subtotal - desconto + frete
  Todos os valores são arredondados para 2 casas decimais (CA11).

  @CT-CAL-01 @CA11 @api @automatizado
  Cenário: Exemplo de cálculo da documentação
    Quando envio POST /api/carrinho/calcular com:
      | produtoId | quantidade |
      | P002      | 1          |
      | P004      | 2          |
    E o cupom "BEMVINDO10"
    Então a resposta tem status 200
    E os valores calculados são:
      | subtotal | desconto | frete | freteGratis | valorFaltanteFreteGratis | total  |
      | 239.7    | 23.97    | 0     | true        | 0                        | 215.73 |
    E o cupom retornado tem aplicado "true" e mensagem "Cupom aplicado: 10% de desconto nos produtos."

  @CT-CAL-02 @CA11 @api @automatizado
  Esquema do Cenário: Valores com centavos são devolvidos com no máximo 2 casas decimais
    Quando envio POST /api/carrinho/calcular com <quantidade> unidades do produto "<produto>" e o cupom "BEMVINDO10"
    Então os valores calculados são:
      | subtotal   | desconto   | frete   | total   |
      | <subtotal> | <desconto> | <frete> | <total> |

    Exemplos:
      | produto | quantidade | subtotal | desconto | frete | total  |
      | P001    | 1          | 59.9     | 5.99     | 19.9  | 73.81  |
      | P001    | 3          | 179.7    | 17.97    | 19.9  | 181.63 |
      | P004    | 1          | 49.9     | 4.99     | 19.9  | 64.81  |
      | P006    | 1          | 29.9     | 2.99     | 19.9  | 46.81  |
      | P006    | 3          | 89.7     | 8.97     | 19.9  | 100.63 |
      | P006    | 5          | 149.5    | 14.95    | 19.9  | 154.45 |
      | P007    | 3          | 689.7    | 68.97    | 0     | 620.73 |

  @CT-CAL-03 @CA11 @api @automatizado
  Cenário: Total de cada item é o preço unitário vezes a quantidade
    Quando envio POST /api/carrinho/calcular com:
      | produtoId | quantidade |
      | P001      | 3          |
      | P006      | 2          |
    Então os itens retornados são:
      | produtoId | precoUnitario | quantidade | total |
      | P001      | 59.9          | 3          | 179.7 |
      | P006      | 29.9          | 2          | 59.8  |
    E o subtotal é 239.5

  @CT-CAL-04 @CA07 @api @automatizado
  Cenário: Valor faltante para o frete grátis nunca é negativo
    Quando envio POST /api/carrinho/calcular com 5 unidades do produto "P007"
    Então o valor faltante para o frete grátis é 0

  @CT-CAL-05 @CA11 @interface
  Cenário: Interface exibe todos os valores com 2 casas decimais no formato brasileiro
    Dado que adicionei 3 unidades de "Camiseta Essencial" ao carrinho
    Quando aplico o cupom "BEMVINDO10"
    Então o total do item "Camiseta Essencial" é "R$ 179,70"
    E o resumo do pedido exibe:
      | Subtotal  | Desconto   | Frete    | Total     |
      | R$ 179,70 | - R$ 17,97 | R$ 19,90 | R$ 181,63 |

  @CT-CAL-06 @CA11 @interface
  Cenário: Valores acima de mil reais usam separador de milhar
    Dado que adicionei 5 unidades de "Jaqueta Corta-Vento" ao carrinho
    Quando acesso o carrinho
    Então o subtotal exibido no carrinho é "R$ 1.149,50"
