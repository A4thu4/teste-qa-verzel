# CT-API-08-formato-padrao-do-erro

Formato padrão do erro e cabeçalho Content-Type

Coletado em 09/10/2026 20:09:02 (horário de Brasília)

## Requisição

```bash
POST /api/carrinho/calcular
```

```json
{
  "itens": [
    {
      "produtoId": "P001",
      "quantidade": 0
    }
  ]
}
```

## Resposta: status 422

Content-Type: `application/json; charset=utf-8`

```json
{
  "erro": {
    "codigo": "QUANTIDADE_INVALIDA",
    "mensagem": "A quantidade deve ser um número inteiro maior ou igual a 1.",
    "campo": "itens[0].quantidade"
  }
}
```
