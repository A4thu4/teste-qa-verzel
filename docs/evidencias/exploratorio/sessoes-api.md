# Sessões exploratórias da API

Executado em 09/10/2026 20:30:24 (horário de Brasília) pelo script [`automacao/explorar_api.py`](../../../automacao/explorar_api.py).

## Resumo

| # | Sessão | Tentativa | Requisição | Status | Resultado |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | Cupom só com espaços | `POST /api/carrinho/calcular` | 200 | subtotal 100 · desconto 0 · total 119.9 · cupom: Cupom inválido. |
| 2 | 1 | Cupom como número | `POST /api/carrinho/calcular` | 200 | subtotal 100 · desconto 0 · total 119.9 · cupom: Cupom inválido. |
| 3 | 1 | Cupom como lista | `POST /api/carrinho/calcular` | 200 | subtotal 100 · desconto 0 · total 119.9 · cupom: Cupom inválido. |
| 4 | 1 | Cupom muito longo (200 caracteres) | `POST /api/carrinho/calcular` | 200 | subtotal 100 · desconto 0 · total 119.9 · cupom: Cupom inválido. |
| 5 | 1 | Cupom com caractere especial no fim | `POST /api/carrinho/calcular` | 200 | subtotal 100 · desconto 0 · total 119.9 · cupom: Cupom inválido. |
| 6 | 1 | Cupom só com espaços no pedido | `POST /api/pedidos` | 422 | erro CUPOM_INVALIDO · chaves: codigo, mensagem, campo |
| 7 | 4 | Raiz da API, sem caminho | `GET /api` | 200 | não é JSON (536 caracteres) |
| 8 | 4 | Lista de produtos com barra no fim | `GET /api/produtos/` | 200 | lista com 8 itens |
| 9 | 4 | Produto com barra no fim | `GET /api/produtos/P001/` | 200 | JSON dict |
| 10 | 4 | Cálculo com Content-Type de formulário em vez de JSON | `POST /api/carrinho/calcular` | 200 | subtotal 100 · desconto 0 · total 119.9 |
| 11 | 4 | Cálculo com Content-Type text/plain | `POST /api/carrinho/calcular` | 200 | subtotal 100 · desconto 0 · total 119.9 |
| 12 | 4 | Campo extra no corpo | `POST /api/carrinho/calcular` | 200 | subtotal 100 · desconto 0 · total 119.9 |
| 13 | 4 | Campo extra dentro do item | `POST /api/carrinho/calcular` | 200 | subtotal 100 · desconto 0 · total 119.9 |
| 14 | 4 | produtoId em minúsculas | `POST /api/carrinho/calcular` | 422 | erro PRODUTO_NAO_ENCONTRADO · chaves: codigo, mensagem, campo |
| 15 | 4 | Consulta de produto com id em minúsculas | `GET /api/produtos/p001` | 404 | erro PRODUTO_NAO_ENCONTRADO · chaves: codigo, mensagem |
| 16 | 4 | Quantidade muito grande | `POST /api/carrinho/calcular` | 200 | subtotal 59900000 · desconto 0 · total 59900000 |
| 17 | 4 | Formato do erro 400 (corpo que não é JSON) | `POST /api/carrinho/calcular` | 400 | erro JSON_INVALIDO · chaves: codigo, mensagem |
| 18 | 4 | Formato do erro 404 (rota inexistente) | `GET /api/rota-que-nao-existe` | 404 | erro ROTA_NAO_ENCONTRADA · chaves: codigo, mensagem |
| 19 | 4 | Formato do erro 404 (produto inexistente) | `GET /api/produtos/P999` | 404 | erro PRODUTO_NAO_ENCONTRADO · chaves: codigo, mensagem |
| 20 | 4 | Formato do erro 405 (método não permitido) | `DELETE /api/produtos` | 405 | erro METODO_NAO_PERMITIDO · chaves: codigo, mensagem |
| 21 | 4 | Formato do erro 422 (quantidade inválida) | `POST /api/carrinho/calcular` | 422 | erro QUANTIDADE_INVALIDA · chaves: codigo, mensagem, campo |

## Detalhes

### 1. Cupom só com espaços

```bash
POST /api/carrinho/calcular
Content-Type: application/json
```

Corpo enviado:

```bash
{
  "itens": [
    {
      "produtoId": "P005",
      "quantidade": 1
    }
  ],
  "cupom": "   "
}
```

Resposta: status 200 · Content-Type: `application/json; charset=utf-8`

```json
{
  "itens": [
    {
      "produtoId": "P005",
      "nome": "Mochila Urbana 20L",
      "precoUnitario": 100,
      "quantidade": 1,
      "total": 100
    }
  ],
  "subtotal": 100,
  "desconto": 0,
  "frete": 19.9,
  "freteGratis": false,
  "valorFaltanteFreteGratis": 100,
  "total": 119.9,
  "cupom": {
    "codigo": "",
    "aplicado": false,
    "mensagem": "Cupom inválido."
  }
}
```

### 2. Cupom como número

```bash
POST /api/carrinho/calcular
Content-Type: application/json
```

Corpo enviado:

```bash
{
  "itens": [
    {
      "produtoId": "P005",
      "quantidade": 1
    }
  ],
  "cupom": 123
}
```

Resposta: status 200 · Content-Type: `application/json; charset=utf-8`

```json
{
  "itens": [
    {
      "produtoId": "P005",
      "nome": "Mochila Urbana 20L",
      "precoUnitario": 100,
      "quantidade": 1,
      "total": 100
    }
  ],
  "subtotal": 100,
  "desconto": 0,
  "frete": 19.9,
  "freteGratis": false,
  "valorFaltanteFreteGratis": 100,
  "total": 119.9,
  "cupom": {
    "codigo": "123",
    "aplicado": false,
    "mensagem": "Cupom inválido."
  }
}
```

### 3. Cupom como lista

```bash
POST /api/carrinho/calcular
Content-Type: application/json
```

Corpo enviado:

```bash
{
  "itens": [
    {
      "produtoId": "P005",
      "quantidade": 1
    }
  ],
  "cupom": [
    "BEMVINDO10"
  ]
}
```

Resposta: status 200 · Content-Type: `application/json; charset=utf-8`

```json
{
  "itens": [
    {
      "produtoId": "P005",
      "nome": "Mochila Urbana 20L",
      "precoUnitario": 100,
      "quantidade": 1,
      "total": 100
    }
  ],
  "subtotal": 100,
  "desconto": 0,
  "frete": 19.9,
  "freteGratis": false,
  "valorFaltanteFreteGratis": 100,
  "total": 119.9,
  "cupom": {
    "codigo": "BEMVINDO10",
    "aplicado": false,
    "mensagem": "Cupom inválido."
  }
}
```

### 4. Cupom muito longo (200 caracteres)

```bash
POST /api/carrinho/calcular
Content-Type: application/json
```

Corpo enviado:

```bash
{
  "itens": [
    {
      "produtoId": "P005",
      "quantidade": 1
    }
  ],
  "cupom": "BEMVINDO10BEMVINDO10BEMVINDO10BEMVINDO10BEMVINDO10BEMVINDO10BEMVINDO10BEMVINDO10BEMVINDO10BEMVINDO10BEMVINDO10BEMVINDO10BEMVINDO10BEMVINDO10BEMVINDO10BEMVINDO10BEMVINDO10BEMVINDO10BEMVINDO10BEMVINDO10"
}
```

Resposta: status 200 · Content-Type: `application/json; charset=utf-8`

```json
{
  "itens": [
    {
      "produtoId": "P005",
      "nome": "Mochila Urbana 20L",
      "precoUnitario": 100,
      "quantidade": 1,
      "total": 100
    }
  ],
  "subtotal": 100,
  "desconto": 0,
  "frete": 19.9,
  "freteGratis": false,
  "valorFaltanteFreteGratis": 100,
  "total": 119.9,
  "cupom": {
    "codigo": "BEMVINDO10BEMVINDO10BEMVINDO10BEMVINDO10BEMVINDO10BEMVINDO10BEMVINDO10BEMVINDO10BEMVINDO10BEMVINDO10BEMVINDO10BEMVINDO10BEMVINDO10BEMVINDO10BEMVINDO10BEMVINDO10BEMVINDO10BEMVINDO10BEMVINDO10BEMVINDO10",
    "aplicado": false,
    "mensagem": "Cupom inválido."
  }
}
```

### 5. Cupom com caractere especial no fim

```bash
POST /api/carrinho/calcular
Content-Type: application/json
```

Corpo enviado:

```bash
{
  "itens": [
    {
      "produtoId": "P005",
      "quantidade": 1
    }
  ],
  "cupom": "BEMVINDO10!"
}
```

Resposta: status 200 · Content-Type: `application/json; charset=utf-8`

```json
{
  "itens": [
    {
      "produtoId": "P005",
      "nome": "Mochila Urbana 20L",
      "precoUnitario": 100,
      "quantidade": 1,
      "total": 100
    }
  ],
  "subtotal": 100,
  "desconto": 0,
  "frete": 19.9,
  "freteGratis": false,
  "valorFaltanteFreteGratis": 100,
  "total": 119.9,
  "cupom": {
    "codigo": "BEMVINDO10!",
    "aplicado": false,
    "mensagem": "Cupom inválido."
  }
}
```

### 6. Cupom só com espaços no pedido

```bash
POST /api/pedidos
Content-Type: application/json
```

Corpo enviado:

```bash
{
  "cliente": {
    "nome": "Maria Silva",
    "email": "maria@exemplo.com",
    "cep": "01310-100"
  },
  "itens": [
    {
      "produtoId": "P005",
      "quantidade": 1
    }
  ],
  "cupom": "   "
}
```

Resposta: status 422 · Content-Type: `application/json; charset=utf-8`

```json
{
  "erro": {
    "codigo": "CUPOM_INVALIDO",
    "mensagem": "Cupom inválido.",
    "campo": "cupom"
  }
}
```

### 7. Raiz da API, sem caminho

```bash
GET /api
(sem cabeçalho Content-Type)
```

Resposta: status 200 · Content-Type: `text/html`

```text
<!doctype html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="robots" content="noindex" />
    <title>Verzel Store | Ambiente de teste técnico</title>
    <script type="module" crossorigin src="/assets/index-DimFnQZA.js"></script>
    <link rel="stylesheet" crossorigin href="/assets/index-BvlSHWkv.css">
  </head>
  <body>
    <div
... (cortado)
```

### 8. Lista de produtos com barra no fim

```bash
GET /api/produtos/
(sem cabeçalho Content-Type)
```

Resposta: status 200 · Content-Type: `application/json; charset=utf-8`

```json
[
  {
    "id": "P001",
    "nome": "Camiseta Essencial",
    "descricao": "Algodão penteado e corte reto.",
    "categoria": "Vestuário",
    "preco": 59.9
  },
  {
    "id": "P002",
    "nome": "Calça Jeans Slim",
    "descricao": "Jeans com elastano e lavagem escura.",
    "categoria": "Vestuário",
    "preco": 139.9
  },
  {
    "id": "P003",
    "nome": "Tênis Casual Urbano",
    "descricao": "Solado de borracha e cabedal em lona.",
    "categoria": "Calçados",
    "preco": 189.9
  },
  {
    "id": "P004",
    "nome": "Boné Aba Curva",
    "descricao": "Ajuste traseiro com fivela metálica.",
    "categoria": "Acessórios",
    "preco": 49.9
  },
  {
    "id": "P005",
    "nome": "Mochila Urbana 20L",
    "descricao": "Compartimento acolchoado para notebook.",
    "categoria": "Acessórios",
    "preco": 100
  },
  {
    "id": "P006",
    "nome": "Kit 3 Pares de Meias",
    "descricao": "Cano médio, algodão com reforço no calcanhar.",
    "categoria": "Vestuário",
    "preco": 29.9
  },
  {
    "id": "P007",
    "nome": "Jaqueta Corta-Vento",
    "descricao": "Tecido leve e repelente à água.",
    "categoria": "Vestuário",
    "preco": 229.9
  },
  {
    "id": "P008",
    "nome": "Garrafa Térmica 750ml",
    "descricao": "Mantém a temperatura por até 12 horas.",
    "categoria": "Acessórios",
    "preco": 50
  }
]
```

### 9. Produto com barra no fim

```bash
GET /api/produtos/P001/
(sem cabeçalho Content-Type)
```

Resposta: status 200 · Content-Type: `application/json; charset=utf-8`

```json
{
  "id": "P001",
  "nome": "Camiseta Essencial",
  "descricao": "Algodão penteado e corte reto.",
  "categoria": "Vestuário",
  "preco": 59.9
}
```

### 10. Cálculo com Content-Type de formulário em vez de JSON

```bash
POST /api/carrinho/calcular
Content-Type: application/x-www-form-urlencoded
```

Corpo enviado:

```bash
{"itens": [{"produtoId": "P005", "quantidade": 1}]}
```

Resposta: status 200 · Content-Type: `application/json; charset=utf-8`

```json
{
  "itens": [
    {
      "produtoId": "P005",
      "nome": "Mochila Urbana 20L",
      "precoUnitario": 100,
      "quantidade": 1,
      "total": 100
    }
  ],
  "subtotal": 100,
  "desconto": 0,
  "frete": 19.9,
  "freteGratis": false,
  "valorFaltanteFreteGratis": 100,
  "total": 119.9,
  "cupom": null
}
```

### 11. Cálculo com Content-Type text/plain

```bash
POST /api/carrinho/calcular
Content-Type: text/plain
```

Corpo enviado:

```bash
{"itens": [{"produtoId": "P005", "quantidade": 1}]}
```

Resposta: status 200 · Content-Type: `application/json; charset=utf-8`

```json
{
  "itens": [
    {
      "produtoId": "P005",
      "nome": "Mochila Urbana 20L",
      "precoUnitario": 100,
      "quantidade": 1,
      "total": 100
    }
  ],
  "subtotal": 100,
  "desconto": 0,
  "frete": 19.9,
  "freteGratis": false,
  "valorFaltanteFreteGratis": 100,
  "total": 119.9,
  "cupom": null
}
```

### 12. Campo extra no corpo

```bash
POST /api/carrinho/calcular
Content-Type: application/json
```

Corpo enviado:

```bash
{
  "itens": [
    {
      "produtoId": "P005",
      "quantidade": 1
    }
  ],
  "teste": 1
}
```

Resposta: status 200 · Content-Type: `application/json; charset=utf-8`

```json
{
  "itens": [
    {
      "produtoId": "P005",
      "nome": "Mochila Urbana 20L",
      "precoUnitario": 100,
      "quantidade": 1,
      "total": 100
    }
  ],
  "subtotal": 100,
  "desconto": 0,
  "frete": 19.9,
  "freteGratis": false,
  "valorFaltanteFreteGratis": 100,
  "total": 119.9,
  "cupom": null
}
```

### 13. Campo extra dentro do item

```bash
POST /api/carrinho/calcular
Content-Type: application/json
```

Corpo enviado:

```bash
{
  "itens": [
    {
      "produtoId": "P005",
      "quantidade": 1,
      "preco": 1
    }
  ]
}
```

Resposta: status 200 · Content-Type: `application/json; charset=utf-8`

```json
{
  "itens": [
    {
      "produtoId": "P005",
      "nome": "Mochila Urbana 20L",
      "precoUnitario": 100,
      "quantidade": 1,
      "total": 100
    }
  ],
  "subtotal": 100,
  "desconto": 0,
  "frete": 19.9,
  "freteGratis": false,
  "valorFaltanteFreteGratis": 100,
  "total": 119.9,
  "cupom": null
}
```

### 14. produtoId em minúsculas

```bash
POST /api/carrinho/calcular
Content-Type: application/json
```

Corpo enviado:

```bash
{
  "itens": [
    {
      "produtoId": "p001",
      "quantidade": 1
    }
  ]
}
```

Resposta: status 422 · Content-Type: `application/json; charset=utf-8`

```json
{
  "erro": {
    "codigo": "PRODUTO_NAO_ENCONTRADO",
    "mensagem": "Produto p001 não encontrado.",
    "campo": "itens[0].produtoId"
  }
}
```

### 15. Consulta de produto com id em minúsculas

```bash
GET /api/produtos/p001
(sem cabeçalho Content-Type)
```

Resposta: status 404 · Content-Type: `application/json; charset=utf-8`

```json
{
  "erro": {
    "codigo": "PRODUTO_NAO_ENCONTRADO",
    "mensagem": "Produto p001 não encontrado."
  }
}
```

### 16. Quantidade muito grande

```bash
POST /api/carrinho/calcular
Content-Type: application/json
```

Corpo enviado:

```bash
{
  "itens": [
    {
      "produtoId": "P001",
      "quantidade": 1000000
    }
  ]
}
```

Resposta: status 200 · Content-Type: `application/json; charset=utf-8`

```json
{
  "itens": [
    {
      "produtoId": "P001",
      "nome": "Camiseta Essencial",
      "precoUnitario": 59.9,
      "quantidade": 1000000,
      "total": 59900000
    }
  ],
  "subtotal": 59900000,
  "desconto": 0,
  "frete": 0,
  "freteGratis": true,
  "valorFaltanteFreteGratis": 0,
  "total": 59900000,
  "cupom": null
}
```

### 17. Formato do erro 400 (corpo que não é JSON)

```bash
POST /api/carrinho/calcular
Content-Type: application/json
```

Corpo enviado:

```bash
nao e json
```

Resposta: status 400 · Content-Type: `application/json; charset=utf-8`

```json
{
  "erro": {
    "codigo": "JSON_INVALIDO",
    "mensagem": "O corpo da requisição deve ser um objeto JSON válido."
  }
}
```

### 18. Formato do erro 404 (rota inexistente)

```bash
GET /api/rota-que-nao-existe
(sem cabeçalho Content-Type)
```

Resposta: status 404 · Content-Type: `application/json; charset=utf-8`

```json
{
  "erro": {
    "codigo": "ROTA_NAO_ENCONTRADA",
    "mensagem": "Rota não encontrada."
  }
}
```

### 19. Formato do erro 404 (produto inexistente)

```bash
GET /api/produtos/P999
(sem cabeçalho Content-Type)
```

Resposta: status 404 · Content-Type: `application/json; charset=utf-8`

```json
{
  "erro": {
    "codigo": "PRODUTO_NAO_ENCONTRADO",
    "mensagem": "Produto P999 não encontrado."
  }
}
```

### 20. Formato do erro 405 (método não permitido)

```bash
DELETE /api/produtos
(sem cabeçalho Content-Type)
```

Resposta: status 405 · Content-Type: `application/json; charset=utf-8`

```json
{
  "erro": {
    "codigo": "METODO_NAO_PERMITIDO",
    "mensagem": "O método DELETE não é permitido nesta rota."
  }
}
```

### 21. Formato do erro 422 (quantidade inválida)

```bash
POST /api/carrinho/calcular
Content-Type: application/json
```

Corpo enviado:

```bash
{
  "itens": [
    {
      "produtoId": "P001",
      "quantidade": 0
    }
  ]
}
```

Resposta: status 422 · Content-Type: `application/json; charset=utf-8`

```json
{
  "erro": {
    "codigo": "QUANTIDADE_INVALIDA",
    "mensagem": "A quantidade deve ser um número inteiro maior ou igual a 1.",
    "campo": "itens[0].quantidade"
  }
}
```
