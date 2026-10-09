# CT-APC-04-cupom-expirado

Cupom expirado no cálculo (CA04)

Coletado em 09/10/2026 19:06:04

## Requisição

```bash
POST /api/carrinho/calcular
```

```json
{
  "itens": [
    {
      "produtoId": "P005",
      "quantidade": 1
    }
  ],
  "cupom": "VERAO2026"
}
```

## Resposta: status 200

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
    "codigo": "VERAO2026",
    "aplicado": false,
    "mensagem": "Cupom expirado."
  }
}
```
