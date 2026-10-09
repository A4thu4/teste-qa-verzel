# CT-APC-03-cupom-inexistente

Cupom inexistente no cálculo (CA03)

Coletado em 09/10/2026 19:06:04 (UTC)

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
  "cupom": "XPTO"
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
    "codigo": "XPTO",
    "aplicado": false,
    "mensagem": "Cupom inválido."
  }
}
```
