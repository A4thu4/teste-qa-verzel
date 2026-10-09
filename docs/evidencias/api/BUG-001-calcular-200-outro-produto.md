# BUG-001-calcular-200-outro-produto

R$ 200,00 com outro produto (CA06)

Coletado em 09/10/2026 19:06:03 (UTC)

## Requisição

```bash
POST /api/carrinho/calcular
```

```json
{
  "itens": [
    {
      "produtoId": "P008",
      "quantidade": 4
    }
  ]
}
```

## Resposta: status 200

```json
{
  "itens": [
    {
      "produtoId": "P008",
      "nome": "Garrafa Térmica 750ml",
      "precoUnitario": 50,
      "quantidade": 4,
      "total": 200
    }
  ],
  "subtotal": 200,
  "desconto": 0,
  "frete": 19.9,
  "freteGratis": false,
  "valorFaltanteFreteGratis": 0,
  "total": 219.9,
  "cupom": null
}
```
