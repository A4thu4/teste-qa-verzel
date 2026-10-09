# BUG-001-calcular-200

Subtotal de exatamente R$ 200,00 (CA06)

Coletado em 09/10/2026 20:09:01 (horário de Brasília)

## Requisição

```bash
POST /api/carrinho/calcular
```

```json
{
  "itens": [
    {
      "produtoId": "P005",
      "quantidade": 2
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
      "produtoId": "P005",
      "nome": "Mochila Urbana 20L",
      "precoUnitario": 100,
      "quantidade": 2,
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
