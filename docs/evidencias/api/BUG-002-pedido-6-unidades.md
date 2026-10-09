# BUG-002-pedido-6-unidades

Pedido com 6 unidades (CA10)

Coletado em 09/10/2026 19:06:03

## Requisição

```bash
POST /api/pedidos
```

```json
{
  "cliente": {
    "nome": "Maria Silva",
    "email": "maria@exemplo.com",
    "cep": "01310-100"
  },
  "itens": [
    {
      "produtoId": "P001",
      "quantidade": 6
    }
  ]
}
```

## Resposta: status 201

```json
{
  "numero": "VZ-760228",
  "criadoEm": "2026-10-09T19:06:03.735Z",
  "cliente": {
    "nome": "Maria Silva",
    "email": "maria@exemplo.com",
    "cep": "01310100"
  },
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
