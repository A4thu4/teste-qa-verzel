# CT-APP-01-pedido-com-cupom

Pedido válido com cupom

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
  ],
  "cupom": "BEMVINDO10"
}
```

## Resposta: status 201

Content-Type: `application/json; charset=utf-8`

```json
{
  "numero": "VZ-228353",
  "criadoEm": "2026-10-09T23:09:02.608Z",
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
  "desconto": 10,
  "frete": 19.9,
  "freteGratis": false,
  "valorFaltanteFreteGratis": 100,
  "total": 109.9,
  "cupom": {
    "codigo": "BEMVINDO10",
    "aplicado": true,
    "mensagem": "Cupom aplicado: 10% de desconto nos produtos."
  }
}
```
