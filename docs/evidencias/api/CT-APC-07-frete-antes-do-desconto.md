# CT-APC-07-frete-antes-do-desconto

Frete pelo subtotal antes do desconto (CA08)

Coletado em 09/10/2026 19:06:03

## Requisição

```bash
POST /api/carrinho/calcular
```

```json
{
  "itens": [
    {
      "produtoId": "P003",
      "quantidade": 1
    },
    {
      "produtoId": "P006",
      "quantidade": 1
    }
  ],
  "cupom": "BEMVINDO10"
}
```

## Resposta: status 200

```json
{
  "itens": [
    {
      "produtoId": "P003",
      "nome": "Tênis Casual Urbano",
      "precoUnitario": 189.9,
      "quantidade": 1,
      "total": 189.9
    },
    {
      "produtoId": "P006",
      "nome": "Kit 3 Pares de Meias",
      "precoUnitario": 29.9,
      "quantidade": 1,
      "total": 29.9
    }
  ],
  "subtotal": 219.8,
  "desconto": 21.98,
  "frete": 0,
  "freteGratis": true,
  "valorFaltanteFreteGratis": 0,
  "total": 197.82,
  "cupom": {
    "codigo": "BEMVINDO10",
    "aplicado": true,
    "mensagem": "Cupom aplicado: 10% de desconto nos produtos."
  }
}
```
