# Evidências da execução

As evidências ficam na pasta [`evidencias/`](evidencias/). Cada arquivo começa com o ID do cenário ou do bug a que se refere.

## Como foram coletadas

| Tipo | Como | Onde fica |
|---|---|---|
| Interface, execução manual | Captura de tela do resultado de cada cenário | `evidencias/*.png` |
| API | Script [`automacao/coletar_evidencias_api.py`](../automacao/coletar_evidencias_api.py), que grava a requisição e a resposta de cada chamada | `evidencias/api/*.md` |
| Automação | Relatório do pytest e captura de tela, vídeo e trace do Playwright nos testes que falham | `evidencias/automacao/` |

## Bugs

| Bug | Evidência |
|---|---|
| BUG-001 | ![Carrinho com subtotal de R$ 200,00 cobrando frete](evidencias/BUG-001-carrinho-200.png) |
| BUG-001 | [Requisição e resposta da API](evidencias/api/BUG-001-calcular-200.md) |
| BUG-002 | [Requisição e resposta da API](evidencias/api/BUG-002-pedido-6-unidades.md) |

## Cenários por critério de aceite

_Uma linha por evidência. Modelo:_

| Cenário | Resultado | Evidência |
|---|---|---|
| CT-CUP-01 | ✅ | ![CT-CUP-01](evidencias/CT-CUP-01-cupom-aplicado.png) |

## Execução da automação

_Colar aqui o resumo final do pytest e apontar para o relatório salvo em `evidencias/automacao/`._

```
(saída do comando pytest)
```
