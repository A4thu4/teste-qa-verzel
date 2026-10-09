# BUG-001-pedido-200

Pedido de exatamente R$ 200,00 (CA06)

Coletado em 09/10/2026 20:09:01 (horário de Brasília)

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
      "produtoId": "P005",
      "quantidade": 2
    }
  ]
}
```

## Resposta: status 201

Content-Type: `application/json; charset=utf-8`

```json
{
  "numero": "VZ-170415",
  "criadoEm": "2026-10-09T23:09:02.107Z",
  "cliente": {
    "nome": "Maria Silva",
    "email": "maria@exemplo.com",
    "cep": "01310100"
  },
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
