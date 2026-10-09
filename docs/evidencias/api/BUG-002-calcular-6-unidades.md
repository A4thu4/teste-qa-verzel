# BUG-002-calcular-6-unidades

Cálculo com 6 unidades (CA10)

Coletado em 09/10/2026 20:09:01 (horário de Brasília)

## Requisição

```bash
POST /api/carrinho/calcular
```

```json
{
  "itens": [
    {
      "produtoId": "P001",
      "quantidade": 6
    }
  ]
}
```

## Resposta: status 200

Content-Type: `application/json; charset=utf-8`

```json
{
  "itens": [
    {
      "produtoId": "P001",
      "nome": "Camiseta Essencial",
      "precoUnitario": 59.9,
      "quantidade": 6,
      "total": 359.4
    }
  ],
  "subtotal": 359.4,
  "desconto": 0,
  "frete": 0,
  "freteGratis": true,
  "valorFaltanteFreteGratis": 0,
  "total": 359.4,
  "cupom": null
}
```
