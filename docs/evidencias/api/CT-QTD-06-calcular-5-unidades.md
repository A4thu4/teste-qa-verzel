# CT-QTD-06-calcular-5-unidades

Cálculo com 5 unidades, no limite (CA10)

Coletado em 09/10/2026 19:06:03 (UTC)

## Requisição

```bash
POST /api/carrinho/calcular
```

```json
{
  "itens": [
    {
      "produtoId": "P001",
      "quantidade": 5
    }
  ]
}
```

## Resposta: status 200

```json
{
  "itens": [
    {
      "produtoId": "P001",
      "nome": "Camiseta Essencial",
      "precoUnitario": 59.9,
      "quantidade": 5,
      "total": 299.5
    }
  ],
  "subtotal": 299.5,
  "desconto": 0,
  "frete": 0,
  "freteGratis": true,
  "valorFaltanteFreteGratis": 0,
  "total": 299.5,
  "cupom": null
}
```
