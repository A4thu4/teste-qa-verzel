# CT-APP-10-numero-novo-a-cada-pedido

Mesmo pedido enviado duas vezes: cada um recebe um número no formato VZ-000000

Coletado em 09/10/2026 20:09:02 (horário de Brasília)

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
      "quantidade": 1
    }
  ]
}
```

## Resposta 1: status 201

Content-Type: `application/json; charset=utf-8`

```json
{
  "numero": "VZ-729603",
  "criadoEm": "2026-10-09T23:09:02.940Z",
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
  "cupom": null
}
```

## Resposta 2: status 201

Content-Type: `application/json; charset=utf-8`

```json
{
  "numero": "VZ-804313",
  "criadoEm": "2026-10-09T23:09:02.984Z",
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
  "cupom": null
}
```
