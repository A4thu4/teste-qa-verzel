# CT-APP-04-pedido-cupom-expirado

Pedido com cupom expirado (CA04)

Coletado em 09/10/2026 19:06:04

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
  "cupom": "VERAO2026"
}
```

## Resposta: status 422

```json
{
  "erro": {
    "codigo": "CUPOM_EXPIRADO",
    "mensagem": "Cupom expirado.",
    "campo": "cupom"
  }
}
```
