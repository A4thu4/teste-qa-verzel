# language: pt
@VZS-142 @frete
Funcionalidade: Frete grátis a partir de R$ 200,00
  Como cliente da Verzel Store
  Quero ganhar frete grátis em compras maiores
  Para pagar menos nas minhas compras

  Contexto:
    Dado que estou na Verzel Store com o carrinho vazio

  # ---------------------------------------------------------------- CA06
  @CT-FRE-01 @CA06 @interface @valor-limite @automatizado
  Cenário: Subtotal de exatamente R$ 200,00 tem frete grátis
    Dado que adicionei 2 unidades de "Mochila Urbana 20L" ao carrinho
    Então o resumo do pedido exibe:
      | Subtotal  | Desconto | Frete  | Total     |
      | R$ 200,00 | R$ 0,00  | Grátis | R$ 200,00 |
    E não vejo o aviso de valor faltante para o frete grátis

  @CT-FRE-02 @CA06 @interface @valor-limite
  Cenário: Subtotal de R$ 200,00 formado por outro produto também tem frete grátis
    Dado que adicionei 4 unidades de "Garrafa Térmica 750ml" ao carrinho
    Então o resumo do pedido exibe:
      | Subtotal  | Desconto | Frete  | Total     |
      | R$ 200,00 | R$ 0,00  | Grátis | R$ 200,00 |

  @CT-FRE-03 @CA06 @interface @automatizado
  Cenário: Subtotal acima de R$ 200,00 tem frete grátis
    Dado que adicionei 1 unidade de "Jaqueta Corta-Vento" ao carrinho
    Então o resumo do pedido exibe:
      | Subtotal  | Desconto | Frete  | Total     |
      | R$ 229,90 | R$ 0,00  | Grátis | R$ 229,90 |
    E não vejo o aviso de valor faltante para o frete grátis

  # ---------------------------------------------------------------- CA07
  @CT-FRE-04 @CA07 @interface @valor-limite @automatizado
  Cenário: Subtotal imediatamente abaixo de R$ 200,00 paga frete fixo e informa o valor faltante
    Dado que adicionei 1 unidade de "Calça Jeans Slim" ao carrinho
    E que adicionei 2 unidades de "Kit 3 Pares de Meias" ao carrinho
    Então o resumo do pedido exibe:
      | Subtotal  | Desconto | Frete    | Total     |
      | R$ 199,70 | R$ 0,00  | R$ 19,90 | R$ 219,60 |
    E vejo o aviso "Faltam R$ 0,30 para o frete grátis."

  @CT-FRE-05 @CA07 @interface
  Cenário: Compra pequena paga frete fixo de R$ 19,90 e informa o valor faltante
    Dado que adicionei 1 unidade de "Camiseta Essencial" ao carrinho
    Então o resumo do pedido exibe:
      | Subtotal | Desconto | Frete    | Total    |
      | R$ 59,90 | R$ 0,00  | R$ 19,90 | R$ 79,80 |
    E vejo o aviso "Faltam R$ 140,10 para o frete grátis."

  @CT-FRE-06 @CA06 @CA07 @interface
  Cenário: Frete e aviso são atualizados quando o subtotal cruza o limite nos dois sentidos
    Dado que adicionei 1 unidade de "Calça Jeans Slim" ao carrinho
    E que adicionei 1 unidade de "Boné Aba Curva" ao carrinho
    E vejo o aviso "Faltam R$ 10,20 para o frete grátis."
    Quando aumento a quantidade de "Boné Aba Curva" para 2
    Então o frete exibido é "Grátis"
    E não vejo o aviso de valor faltante para o frete grátis
    Quando diminuo a quantidade de "Boné Aba Curva" para 1
    Então o frete exibido é "R$ 19,90"
    E vejo o aviso "Faltam R$ 10,20 para o frete grátis."

  # ---------------------------------------------------------------- CA08
  @CT-FRE-07 @CA08 @interface @automatizado
  Cenário: Frete grátis considera o subtotal antes do desconto do cupom
    # Subtotal 219,80. Com o cupom o valor dos produtos cai para 197,82,
    # abaixo de 200,00, mas o frete continua grátis.
    Dado que adicionei 1 unidade de "Tênis Casual Urbano" ao carrinho
    E que adicionei 1 unidade de "Kit 3 Pares de Meias" ao carrinho
    Quando aplico o cupom "BEMVINDO10"
    Então o resumo do pedido exibe:
      | Subtotal  | Desconto   | Frete  | Total     |
      | R$ 219,80 | - R$ 21,98 | Grátis | R$ 197,82 |

  @CT-FRE-08 @CA06 @CA08 @interface @valor-limite
  Cenário: Subtotal de exatamente R$ 200,00 com cupom mantém o frete grátis
    Dado que adicionei 2 unidades de "Mochila Urbana 20L" ao carrinho
    Quando aplico o cupom "BEMVINDO10"
    Então o resumo do pedido exibe:
      | Subtotal  | Desconto   | Frete  | Total     |
      | R$ 200,00 | - R$ 20,00 | Grátis | R$ 180,00 |

  @CT-FRE-09 @CA08 @interface
  Cenário: Aplicar o cupom não altera o valor faltante para o frete grátis
    Dado que adicionei 1 unidade de "Calça Jeans Slim" ao carrinho
    E que adicionei 1 unidade de "Boné Aba Curva" ao carrinho
    Quando aplico o cupom "BEMVINDO10"
    Então vejo o aviso "Faltam R$ 10,20 para o frete grátis."

  # ---------------------------------------------------------------- CA09
  @CT-FRE-10 @CA09 @interface @automatizado
  Cenário: Desconto do cupom não incide sobre o frete
    # 10% sobre 100,00 = 10,00. Se incidisse sobre o frete seria 11,99.
    Dado que adicionei 1 unidade de "Mochila Urbana 20L" ao carrinho
    Quando aplico o cupom "BEMVINDO10"
    Então o desconto exibido é "- R$ 10,00"
    E o frete exibido é "R$ 19,90"
    E o total exibido é "R$ 109,90"

  # ------------------------------------------------------- Fluxo completo
  @CT-FRE-11 @CA06 @interface
  Cenário: Frete grátis é mantido no checkout e na confirmação do pedido
    Dado que adicionei 1 unidade de "Jaqueta Corta-Vento" ao carrinho
    Quando finalizo a compra com dados de cliente válidos
    Então a página de confirmação exibe:
      | Subtotal  | Desconto | Frete  | Total     |
      | R$ 229,90 | R$ 0,00  | Grátis | R$ 229,90 |
