# language: pt
@api @produtos
Funcionalidade: API de produtos e tratamento geral de erros
  A API fica em /api, envia e recebe JSON e devolve todo erro no formato
  { "erro": { "codigo", "mensagem", "campo" } }.

  # -------------------------------------------------------------- Produtos
  @CT-API-01 @api @automatizado
  Cenário: Listar produtos devolve os 8 produtos da documentação
    Quando envio GET /api/produtos
    Então a resposta tem status 200
    E a lista tem 8 produtos
    E cada produto tem os campos "id", "nome", "descricao", "categoria" e "preco"
    E os ids e preços são:
      | id   | nome                  | preco |
      | P001 | Camiseta Essencial    | 59.9  |
      | P002 | Calça Jeans Slim      | 139.9 |
      | P003 | Tênis Casual Urbano   | 189.9 |
      | P004 | Boné Aba Curva        | 49.9  |
      | P005 | Mochila Urbana 20L    | 100   |
      | P006 | Kit 3 Pares de Meias  | 29.9  |
      | P007 | Jaqueta Corta-Vento   | 229.9 |
      | P008 | Garrafa Térmica 750ml | 50    |

  @CT-API-02 @api @automatizado
  Cenário: Consultar um produto existente pelo id
    Quando envio GET /api/produtos/P001
    Então a resposta tem status 200
    E o produto retornado tem nome "Camiseta Essencial" e preço 59.9

  @CT-API-03 @api @automatizado
  Cenário: Consultar um produto inexistente devolve 404
    Quando envio GET /api/produtos/P999
    Então a resposta tem status 404
    E o código do erro é "PRODUTO_NAO_ENCONTRADO"

  @CT-API-04 @api
  Cenário: Preços da vitrine são os mesmos devolvidos pela API
    Quando acesso a vitrine da loja
    Então cada produto exibe o mesmo nome e preço devolvidos por GET /api/produtos

  # ---------------------------------------------------------- Erros gerais
  @CT-API-05 @api @automatizado
  Cenário: Rota inexistente devolve 404 ROTA_NAO_ENCONTRADA
    Quando envio GET /api/rota-que-nao-existe
    Então a resposta tem status 404
    E o código do erro é "ROTA_NAO_ENCONTRADA"

  @CT-API-06 @api @automatizado
  Esquema do Cenário: Método não aceito pela rota devolve 405 METODO_NAO_PERMITIDO
    Quando envio <metodo> <rota>
    Então a resposta tem status 405
    E o código do erro é "METODO_NAO_PERMITIDO"

    Exemplos:
      | metodo | rota                   |
      | GET    | /api/carrinho/calcular |
      | GET    | /api/pedidos           |
      | POST   | /api/produtos          |
      | PUT    | /api/produtos/P001     |

  @CT-API-07 @api @automatizado
  Esquema do Cenário: Corpo que não é um objeto JSON válido devolve 400 JSON_INVALIDO
    Quando envio POST <rota> com o corpo <corpo>
    Então a resposta tem status 400
    E o código do erro é "JSON_INVALIDO"

    Exemplos:
      | rota                   | corpo     | caso                 |
      | /api/carrinho/calcular | {itens:   | JSON malformado      |
      | /api/carrinho/calcular | [1, 2]    | lista em vez de objeto |
      | /api/pedidos           | nao e json | texto puro           |

  @CT-API-08 @api
  Cenário: Todo erro segue o formato padrão
    Quando envio POST /api/carrinho/calcular com quantidade 0 do produto "P001"
    Então o corpo da resposta tem o objeto "erro" com "codigo", "mensagem" e "campo"
    E a resposta tem o cabeçalho Content-Type "application/json"
