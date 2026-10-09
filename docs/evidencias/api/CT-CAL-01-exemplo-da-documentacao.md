# CT-CAL-01-exemplo-da-documentacao

Exemplo de cálculo da documentação

Coletado em 09/10/2026 19:06:03

## Requisição

```bash
POST /api/carrinho/calcular
```

```json
{
  "itens": [
    {
      "produtoId": "P002",
      "quantidade": 1
    },
    {
      "produtoId": "P004",
      "quantidade": 2
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
      "produtoId": "P002",
      "nome": "Calça Jeans Slim",
      "precoUnitario": 139.9,
      "quantidade": 1,
      "total": 139.9
    },
    {
      "produtoId": "P004",
      "nome": "Boné Aba Curva",
      "precoUnitario": 49.9,
      "quantidade": 2,
      "total": 99.8
    }
  ],
  "subtotal": 239.7,
  "desconto": 23.97,
  "frete": 0,
  "freteGratis": true,
  "valorFaltanteFreteGratis": 0,
  "total": 215.73,
  "cupom": {
    "codigo": "BEMVINDO10",
    "aplicado": true,
    "mensagem": "Cupom aplicado: 10% de desconto nos produtos."
  }
}
```
