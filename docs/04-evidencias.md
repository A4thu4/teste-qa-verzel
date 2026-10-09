# Evidências da execução

As evidências ficam na pasta [`evidencias/`](evidencias/). Cada arquivo começa com o ID do cenário ou do bug a que se refere.

## Como foram coletadas

| Tipo | Como | Onde fica |
| --- | --- | --- |
| Interface, execução manual | Captura de tela do resultado de cada cenário | `evidencias/*.png` |
| API | Script [`automacao/coletar_evidencias_api.py`](../automacao/coletar_evidencias_api.py), que grava a requisição e a resposta de cada chamada | `evidencias/api/*.md` |
| Automação | Relatório do pytest e captura de tela, vídeo e trace do Playwright nos testes que falham | `evidencias/automacao/` |

## Bugs

| Bug | Evidência |
| --- | --- |
| BUG-001 | ![Carrinho com subtotal de R$ 200,00 cobrando frete](evidencias/BUG-001-carrinho-200.png) |
| BUG-001 | [Requisição e resposta da API](evidencias/api/BUG-001-calcular-200.md) |
| BUG-002 | [Requisição e resposta da API](evidencias/api/BUG-002-pedido-6-unidades.md) |

## Cenários

### API

| Cenário | Resultado | Evidência |
| --- | --- | --- |
| CT-APC-02 | ✅ | [CT-APC-02-cupom-minusculas-com-espacos](evidencias/api/CT-APC-02-cupom-minusculas-com-espacos.md) |
| CT-APC-03 | ✅ | [CT-APC-03-cupom-inexistente](evidencias/api/CT-APC-03-cupom-inexistente.md) |
| CT-APC-04 | ✅ | [CT-APC-04-cupom-expirado](evidencias/api/CT-APC-04-cupom-expirado.md) |
| CT-APC-06 | ✅ no exemplo de R$ 199,70; os exemplos de R$ 200,00 falham pelo [BUG-001](03-bugs.md#bug-001) | [CT-APC-06-calcular-199-70](evidencias/api/CT-APC-06-calcular-199-70.md) |
| CT-APC-07 | ✅ | [CT-APC-07-frete-antes-do-desconto](evidencias/api/CT-APC-07-frete-antes-do-desconto.md) |
| CT-API-01 | ✅ | [CT-API-01-listar-produtos](evidencias/api/CT-API-01-listar-produtos.md) |
| CT-API-03 | ✅ | [CT-API-03-produto-inexistente](evidencias/api/CT-API-03-produto-inexistente.md) |
| CT-APP-01 | ✅ | [CT-APP-01-pedido-com-cupom](evidencias/api/CT-APP-01-pedido-com-cupom.md) |
| CT-APP-04 | ✅ | [CT-APP-04-pedido-cupom-expirado](evidencias/api/CT-APP-04-pedido-cupom-expirado.md) |
| CT-CAL-01 | ✅ | [CT-CAL-01-exemplo-da-documentacao](evidencias/api/CT-CAL-01-exemplo-da-documentacao.md) |
| CT-QTD-06 | ✅ | [CT-QTD-06-calcular-5-unidades](evidencias/api/CT-QTD-06-calcular-5-unidades.md) |

### Interface

| Cenário | Resultado | Evidência |
| --- | --- | --- |

## Execução da automação

Execução de 09/10/2026 no GitHub Codespaces. Relatório completo em [`evidencias/automacao/resultado.xml`](evidencias/automacao/resultado.xml).

```bash
============================================================================= test session starts ==============================================================================
platform linux -- Python 3.12.11, pytest-8.4.1, pluggy-1.6.0
rootdir: /workspaces/teste-qa-verzel/automacao
configfile: pytest.ini
testpaths: tests
plugins: playwright-0.10.0
collected 103 items                                                                                                                                                            

tests/api/test_carrinho.py ..........xx....................                                                                                                              [ 31%]
tests/api/test_pedidos.py ....x...........                                                                                                                               [ 46%]
tests/api/test_produtos_e_erros.py ...........                                                                                                                           [ 57%]
tests/api/test_quantidade.py .xx.....                                                                                                                                    [ 65%]
tests/ui/test_checkout.py ...................                                                                                                                            [ 83%]
tests/ui/test_cupom.py ..........                                                                                                                                        [ 93%]
tests/ui/test_frete.py x....                                                                                                                                             [ 98%]
tests/ui/test_quantidade.py ..                                                                                                                                           [100%]

=========================================================================== short test summary info ============================================================================
XFAIL tests/api/test_carrinho.py::test_ct_apc_06_frete_conforme_o_subtotal[200.00-no-limite] - BUG-001: subtotal de exatamente R$ 200,00 não recebe frete grátis (CA06)
XFAIL tests/api/test_carrinho.py::test_ct_apc_06_frete_conforme_o_subtotal[200.00-no-limite-outro-produto] - BUG-001: subtotal de exatamente R$ 200,00 não recebe frete grátis (CA06)
XFAIL tests/api/test_pedidos.py::test_ct_app_05_pedido_de_200_reais_tem_frete_gratis - BUG-001: subtotal de exatamente R$ 200,00 não recebe frete grátis (CA06)
XFAIL tests/api/test_quantidade.py::test_ct_qtd_07_calculo_recusa_6_unidades - BUG-002: API aceita mais de 5 unidades do mesmo produto (CA10)
XFAIL tests/api/test_quantidade.py::test_ct_qtd_08_pedido_recusa_6_unidades - BUG-002: API aceita mais de 5 unidades do mesmo produto (CA10)
XFAIL tests/ui/test_frete.py::test_ct_fre_01_subtotal_de_200_reais_tem_frete_gratis[chromium] - BUG-001: subtotal de exatamente R$ 200,00 não recebe frete grátis (CA06)
======================================================================== 97 passed, 6 xfailed in 32.31s ========================================================================
```
