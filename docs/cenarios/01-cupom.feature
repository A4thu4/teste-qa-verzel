# language: pt
@VZS-142 @cupom
Funcionalidade: Cupom de desconto no carrinho
  Como cliente da Verzel Store
  Quero aplicar um cupom de desconto no carrinho
  Para pagar menos nas minhas compras

  Contexto:
    Dado que estou na Verzel Store com o carrinho vazio

  # ---------------------------------------------------------------- CA01
  @CT-CUP-01 @CA01 @interface @automatizado
  Cenário: Cupom BEMVINDO10 aplica 10% sobre o subtotal de um único produto
    Dado que adicionei 1 unidade de "Mochila Urbana 20L" ao carrinho
    Quando aplico o cupom "BEMVINDO10"
    Então vejo a confirmação "Cupom BEMVINDO10 aplicado."
    E o resumo do pedido exibe:
      | Subtotal | Desconto   | Frete    | Total     |
      | R$ 100,00 | - R$ 10,00 | R$ 19,90 | R$ 109,90 |

  @CT-CUP-02 @CA01 @interface
  Cenário: Desconto de 10% incide sobre a soma de todos os produtos do carrinho
    Dado que adicionei 1 unidade de "Calça Jeans Slim" ao carrinho
    E que adicionei 1 unidade de "Boné Aba Curva" ao carrinho
    Quando aplico o cupom "BEMVINDO10"
    Então o resumo do pedido exibe:
      | Subtotal  | Desconto   | Frete    | Total     |
      | R$ 189,80 | - R$ 18,98 | R$ 19,90 | R$ 190,72 |

  @CT-CUP-03 @CA01 @interface
  Cenário: Desconto é recalculado quando a quantidade muda com o cupom aplicado
    Dado que adicionei 1 unidade de "Garrafa Térmica 750ml" ao carrinho
    E que apliquei o cupom "BEMVINDO10"
    Quando aumento a quantidade de "Garrafa Térmica 750ml" para 3
    Então o resumo do pedido exibe:
      | Subtotal  | Desconto   | Frete    | Total     |
      | R$ 150,00 | - R$ 15,00 | R$ 19,90 | R$ 154,90 |

  # ---------------------------------------------------------------- CA02
  @CT-CUP-04 @CA02 @interface @automatizado
  Esquema do Cenário: Código do cupom ignora maiúsculas, minúsculas e espaços nas pontas
    Dado que adicionei 1 unidade de "Mochila Urbana 20L" ao carrinho
    Quando aplico o cupom "<codigo digitado>"
    Então vejo a confirmação "Cupom BEMVINDO10 aplicado."
    E o desconto exibido é "- R$ 10,00"

    # O símbolo ␣ representa um espaço em branco digitado no campo.
    Exemplos:
      | codigo digitado | variação                        |
      | bemvindo10      | tudo em minúsculas              |
      | BemVindo10      | maiúsculas e minúsculas         |
      | ␣␣BEMVINDO10␣␣  | espaços no início e no fim      |
      | ␣bemvindo10␣    | minúsculas com espaços          |

  @CT-CUP-05 @CA02 @interface
  Cenário: Espaço no meio do código não é ignorado
    Dado que adicionei 1 unidade de "Mochila Urbana 20L" ao carrinho
    Quando aplico o cupom "BEM VINDO10"
    Então vejo a mensagem "Cupom inválido."
    E o desconto exibido é "R$ 0,00"

  # ---------------------------------------------------------------- CA03
  @CT-CUP-06 @CA03 @interface @automatizado
  Cenário: Cupom inexistente exibe "Cupom inválido." e não gera desconto
    Dado que adicionei 1 unidade de "Mochila Urbana 20L" ao carrinho
    Quando aplico o cupom "XPTO"
    Então vejo a mensagem "Cupom inválido."
    E o resumo do pedido exibe:
      | Subtotal  | Desconto | Frete    | Total     |
      | R$ 100,00 | R$ 0,00  | R$ 19,90 | R$ 119,90 |

  @CT-CUP-07 @CA03 @interface
  Cenário: Aplicar com o campo de cupom vazio não gera desconto
    # A documentação não define a mensagem para o campo vazio. Ver AMB-03.
    Dado que adicionei 1 unidade de "Mochila Urbana 20L" ao carrinho
    Quando aplico o cupom ""
    Então vejo uma mensagem orientando a informar um cupom
    E o desconto exibido é "R$ 0,00"

  # ---------------------------------------------------------------- CA04
  @CT-CUP-08 @CA04 @interface @automatizado
  Cenário: Cupom fora da validade exibe "Cupom expirado." e não gera desconto
    Dado que adicionei 1 unidade de "Mochila Urbana 20L" ao carrinho
    Quando aplico o cupom "VERAO2026"
    Então vejo a mensagem "Cupom expirado."
    E o resumo do pedido exibe:
      | Subtotal  | Desconto | Frete    | Total     |
      | R$ 100,00 | R$ 0,00  | R$ 19,90 | R$ 119,90 |

  @CT-CUP-09 @CA02 @CA04 @interface
  Cenário: Cupom expirado digitado em minúsculas continua sendo identificado como expirado
    Dado que adicionei 1 unidade de "Mochila Urbana 20L" ao carrinho
    Quando aplico o cupom "verao2026"
    Então vejo a mensagem "Cupom expirado."
    E o desconto exibido é "R$ 0,00"

  # ---------------------------------------------------------------- CA05
  @CT-CUP-10 @CA05 @interface @automatizado
  Cenário: Com um cupom aplicado não é possível informar um segundo cupom
    Dado que adicionei 1 unidade de "Mochila Urbana 20L" ao carrinho
    E que apliquei o cupom "BEMVINDO10"
    Então o campo "Cupom de desconto" não está disponível
    E vejo a opção "Remover cupom"

  @CT-CUP-11 @CA05 @interface @automatizado
  Cenário: Remover o cupom zera o desconto e libera o campo novamente
    Dado que adicionei 1 unidade de "Mochila Urbana 20L" ao carrinho
    E que apliquei o cupom "BEMVINDO10"
    Quando removo o cupom
    Então o campo "Cupom de desconto" está disponível e vazio
    E o resumo do pedido exibe:
      | Subtotal  | Desconto | Frete    | Total     |
      | R$ 100,00 | R$ 0,00  | R$ 19,90 | R$ 119,90 |

  @CT-CUP-12 @CA05 @interface
  Cenário: Trocar de cupom exige remover o atual e aplicar o outro
    Dado que adicionei 1 unidade de "Mochila Urbana 20L" ao carrinho
    E que apliquei o cupom "BEMVINDO10"
    Quando removo o cupom
    E aplico o cupom "VERAO2026"
    Então vejo a mensagem "Cupom expirado."
    E o desconto exibido é "R$ 0,00"

  @CT-CUP-13 @CA03 @interface
  Cenário: Cupom válido aplicado depois de uma tentativa inválida limpa a mensagem de erro
    Dado que adicionei 1 unidade de "Mochila Urbana 20L" ao carrinho
    E que tentei aplicar o cupom "XPTO"
    Quando aplico o cupom "BEMVINDO10"
    Então vejo a confirmação "Cupom BEMVINDO10 aplicado."
    E não vejo a mensagem "Cupom inválido."

  # ------------------------------------------------- Persistência do cupom
  @CT-CUP-14 @CA01 @interface @automatizado
  Cenário: Cupom aplicado no carrinho é mantido no checkout e na confirmação do pedido
    Dado que adicionei 1 unidade de "Mochila Urbana 20L" ao carrinho
    E que apliquei o cupom "BEMVINDO10"
    Quando finalizo a compra com dados de cliente válidos
    Então a página de confirmação exibe:
      | Subtotal  | Desconto   | Frete    | Total     |
      | R$ 100,00 | - R$ 10,00 | R$ 19,90 | R$ 109,90 |

  @CT-CUP-15 @CA01 @interface
  Cenário: Cupom continua aplicado depois de remover um dos itens do carrinho
    Dado que adicionei 1 unidade de "Camiseta Essencial" ao carrinho
    E que adicionei 1 unidade de "Kit 3 Pares de Meias" ao carrinho
    E que apliquei o cupom "BEMVINDO10"
    Quando removo "Kit 3 Pares de Meias" do carrinho
    Então o resumo do pedido exibe:
      | Subtotal | Desconto  | Frete    | Total    |
      | R$ 59,90 | - R$ 5,99 | R$ 19,90 | R$ 73,81 |
