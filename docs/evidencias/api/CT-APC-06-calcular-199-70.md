# CT-APC-06-calcular-199-70

Subtotal logo abaixo do limite do frete (CA07)

Coletado em 09/10/2026 19:06:03 (UTC)

## Requisição

```bash
POST /api/carrinho/calcular
```

```json
{
  "itens": [
    {
      "produtoId": "P002",
      "quantidade": 1
    },
    {
      "produtoId": "P006",
      "quantidade": 2
    }
  ]
}
```

## Resposta: status 200

```json
{
  "itens": [
    {
      "produtoId": "P002",
      "nome": "Calça Jeans Slim",
      "precoUnitario": 139.9,
      "quantidade": 1,
      "total": 139.9
    },
    {
      "produtoId": "P006",
      "nome": "Kit 3 Pares de Meias",
      "precoUnitario": 29.9,
      "quantidade": 2,
      "total": 59.8
    }
  ],
  "subtotal": 199.7,
  "desconto": 0,
  "frete": 19.9,
  "freteGratis": false,
  "valorFaltanteFreteGratis": 0.3,
  "total": 219.6,
  "cupom": null
}
```
