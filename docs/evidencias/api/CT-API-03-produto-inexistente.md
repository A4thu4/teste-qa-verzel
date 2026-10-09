# CT-API-03-produto-inexistente

Produto inexistente

Coletado em 09/10/2026 20:09:02 (horário de Brasília)

## Requisição

```bash
GET /api/produtos/P999
```

## Resposta: status 404

Content-Type: `application/json; charset=utf-8`

```json
{
  "erro": {
    "codigo": "PRODUTO_NAO_ENCONTRADO",
    "mensagem": "Produto P999 não encontrado."
  }
}
```
