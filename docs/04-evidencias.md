# Evidências da execução

As evidências ficam na pasta [`evidencias/`](evidencias/). Cada arquivo começa com o ID do cenário ou do bug a que se refere.

## Como foram coletadas

| Tipo | Como | Onde fica |
| --- | --- | --- |
| Interface, execução manual | Captura de tela do resultado de cada cenário | `evidencias/feature_*/`, uma pasta por funcionalidade |
| API | Script [`automacao/coletar_evidencias_api.py`](../automacao/coletar_evidencias_api.py), que grava a requisição e a resposta de cada chamada | `evidencias/api/*.md` |
| Automação | Relatório do pytest e captura de tela, vídeo e trace do Playwright nos testes que falham | `evidencias/automacao/` |

## Bugs

| Bug | Evidência |
| --- | --- |
| BUG-001 | [Carrinho com R$ 200,00 em garrafas cobrando frete (CT-FRE-02)](evidencias/feature_frete/CT-FRE-02-subtotal-200-frete-gratis.png) |
| BUG-001 | [Carrinho com R$ 200,00 e cupom cobrando frete (CT-FRE-08)](evidencias/feature_frete/CT-FRE-08-subtotal-200-com-cupom-frete-gratis.png) |
| BUG-001 | [Requisição e resposta da API](evidencias/api/BUG-001-calcular-200.md) |
| BUG-002 | [Requisição e resposta da API](evidencias/api/BUG-002-pedido-6-unidades.md) |
| BUG-002 | [Vitrine bloqueando a 6ª unidade, para comparação (CT-QTD-05)](evidencias/feature_qntd/CT-QTD-05-limite-continua-na-vitrine.png) |

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
| CT-API-08 | ✅ | [CT-API-08-formato-padrao-do-erro](evidencias/api/CT-API-08-formato-padrao-do-erro.md) |
| CT-APC-13 | ✅ | [CT-APC-13-calculo-nao-grava-nada](evidencias/api/CT-APC-13-calculo-nao-grava-nada.md) |
| CT-APP-10 | ✅ | [CT-APP-10-numero-novo-a-cada-pedido](evidencias/api/CT-APP-10-numero-novo-a-cada-pedido.md) |

### Interface

| Cenário | Resultado | Evidência |
| --- | --- | --- |
| CT-CUP-02 | ✅ | [print](evidencias/feature_cupom/CT-CUP-02-desconto-sobre-todos-produtos.png) |
| CT-CUP-03 | ✅ | [print](evidencias/feature_cupom/CT-CUP-03-desconto-recalculado-cupom-aplicado.png) |
| CT-CUP-05 | ✅ | [print](evidencias/feature_cupom/CT-CUP-05-espaco-ignorado-cupom-invalido.png) |
| CT-CUP-07 | ✅ | [print](evidencias/feature_cupom/CT-CUP-07-cupom-vazio-nao-gera-desconto.png) |
| CT-CUP-09 | ✅ | [print](evidencias/feature_cupom/CT-CUP-09-cupom-minusculo-continua-expirado.png) |
| CT-CUP-12 | ✅ | [print 1](evidencias/feature_cupom/CT-CUP-12_1-cupom-exige-remover-atual.png) · [print 2](evidencias/feature_cupom/CT-CUP-12_2-cupom-exige-remover-atual.png) |
| CT-CUP-13 | ✅ | [print 1](evidencias/feature_cupom/CT-CUP-13_1-cupom-valido-aplicado-apos-invalido.png) · [print 2](evidencias/feature_cupom/CT-CUP-13_2-cupom-valido-aplicado-apos-invalido.png) |
| CT-CUP-15 | ✅ | [print 1](evidencias/feature_cupom/CT-CUP-15_1-cupom-ativado-apos-remover-item.png) · [print 2](evidencias/feature_cupom/CT-CUP-15_2-cupom-ativado-apos-remover-item.png) |
| CT-FRE-02 | ❌ [BUG-001](03-bugs.md#bug-001) | [print](evidencias/feature_frete/CT-FRE-02-subtotal-200-frete-gratis.png) |
| CT-FRE-05 | ✅ | [print](evidencias/feature_frete/CT-FRE-05-compra-pequena-frete-fixo.png) |
| CT-FRE-06 | ✅ | [print 1](evidencias/feature_frete/CT-FRE-06_1-frete-aviso-atualizados-subtotal-cruza-limite.png) · [print 2](evidencias/feature_frete/CT-FRE-06_2-frete-aviso-atualizados-subtotal-cruza-limite.png) |
| CT-FRE-08 | ❌ [BUG-001](03-bugs.md#bug-001) | [print](evidencias/feature_frete/CT-FRE-08-subtotal-200-com-cupom-frete-gratis.png) |
| CT-FRE-09 | ✅ | [print](evidencias/feature_frete/CT-FRE-09-cupom-nao-altera-faltante-para-frete.png) |
| CT-FRE-11 | ✅ | [print](evidencias/feature_frete/CT-FRE-11-frete-gratis-mantido-checkout-e-confirmacao.png) |
| CT-QTD-03 | ✅ | [print](evidencias/feature_qntd/CT-QTD-03-botao-diminuir-desabilitado.png) |
| CT-QTD-04 | ✅ | [print](evidencias/feature_qntd/CT-QTD-04-limite-por-produto-nao-total.png) |
| CT-QTD-05 | ✅ | [print](evidencias/feature_qntd/CT-QTD-05-limite-continua-na-vitrine.png) |
| CT-CAL-05 | ✅ | [print](evidencias/feature_calculo/CT-CAL-05-exibe-valores-decimais-em-ptbr.png) |
| CT-CAL-06 | ✅ | [print](evidencias/feature_calculo/CT-CAL-06-valores-acima-1000-separa-por-milhar.png) |
| CT-CHK-02 | ✅ | [checkout](evidencias/feature_checkout/CT-CHK-10-formulario-em-branco-aponta-obrigatorios.png) · [confirmação](evidencias/feature_checkout/CT-CHK-02e03-resumo-checkout-repete-valores-e-itens-com-pagamento-entrega.png) |
| CT-CHK-03 | ✅ | [checkout](evidencias/feature_checkout/CT-CHK-10-formulario-em-branco-aponta-obrigatorios.png) · [confirmação](evidencias/feature_checkout/CT-CHK-02e03-resumo-checkout-repete-valores-e-itens-com-pagamento-entrega.png) |
| CT-CHK-10 | ✅ | [print](evidencias/feature_checkout/CT-CHK-10-formulario-em-branco-aponta-obrigatorios.png) |
| CT-CHK-11 | ✅ | [print](evidencias/feature_checkout/CT-CHK-11-erro-e-solicitar-corrigir-dados.png) |
| CT-API-04 | ✅ | [print](evidencias/feature_api/CT-API-04-precos-vitrine-iguais-da-api.png) · comparado com [CT-API-01](evidencias/api/CT-API-01-listar-produtos.md) |

## Sessões exploratórias

| Sessão | Evidência |
| --- | --- |
| 1 (parte de API) e 4 | [Relatório das 21 tentativas de API](evidencias/exploratorio/sessoes-api.md), gerado por [`automacao/explorar_api.py`](../automacao/explorar_api.py) |

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

### Segunda execução: cenários de checkout automatizados depois

CT-CHK-05, CT-CHK-07 e CT-CHK-12, executados em 09/10/2026 no GitHub Codespaces.

```bash
$ pytest tests/ui/test_checkout.py -k "chk_05 or chk_07 or chk_12"
platform linux -- Python 3.12.11, pytest-8.4.1, pluggy-1.6.0
rootdir: /workspaces/teste-qa-verzel/automacao
configfile: pytest.ini
plugins: playwright-0.10.0
collected 29 items / 19 deselected / 10 selected

tests/ui/test_checkout.py ..........                                     [100%]

========================= 10 passed, 19 deselected in 7.61s =========================
```
