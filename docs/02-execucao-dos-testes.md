# Execução dos testes

| | |
| --- | --- |
| Executado por | Arthur Mamedes Borges |
| Data | 09/10/2026 |
| Ambiente | <https://verzel-store.qa-test-verzel-store.workers.dev>, versão 2.3.0 |
| Navegador e sistema | Brave/Chrome - Windows 11 |
| Ambiente da automação | Chromium headless do Playwright, GitHub Codespaces (Linux, Python 3.12.11, pytest 8.4.1, pytest-playwright 0.10.0) |

**Legenda do status:** ✅ passou · ❌ falhou (bug aberto) · ⚠️ passou com observação · ⬜ não executado

## Resumo

| Total de cenários | ✅ Passou | ❌ Falhou | ⚠️ Com observação | ⬜ Não executado |
| --- | --- | --- | --- | --- |
| 84 | 70 | 7 | 0 | 7 |

Dos 84 cenários, 54 estão automatizados com Playwright e os outros 30 são executados manualmente.

Os 54 automatizados foram executados em 09/10/2026: 49 passaram e 5 falharam pelos bugs BUG-001 e BUG-002. Na automação isso aparece como 97 testes `passed` e 6 `xfailed`, porque um cenário com vários exemplos vira vários testes. A saída completa está em [04-evidencias.md](04-evidencias.md#execução-da-automação) e o relatório em [`resultado.xml`](evidencias/automacao/resultado.xml).

Dos 30 manuais, 23 foram executados em 09/10/2026: 21 passaram e 2 falharam pelo BUG-001 (CT-FRE-02 e CT-FRE-08). Faltam CT-CHK-05, CT-CHK-07, CT-CHK-12, CT-API-04, CT-API-08, CT-APC-13 e CT-APP-10.

## Testes roteirizados

### Cupom de desconto no carrinho

Arquivo: [`01-cupom.feature`](cenarios/01-cupom.feature)

| ID | Cenário | Critério | Tipo | Automatizado | Status | Evidência / Bug |
| --- | --- | --- | --- | --- | --- | --- |
| CT-CUP-01 | Cupom BEMVINDO10 aplica 10% sobre o subtotal de um único produto | CA01 | Interface | Sim | ✅ | [automação](evidencias/automacao/resultado.xml) |
| CT-CUP-02 | Desconto de 10% incide sobre a soma de todos os produtos do carrinho | CA01 | Interface | Não | ✅ | [print](evidencias/feature_cupom/CT-CUP-02-desconto-sobre-todos-produtos.png) |
| CT-CUP-03 | Desconto é recalculado quando a quantidade muda com o cupom aplicado | CA01 | Interface | Não | ✅ | [print](evidencias/feature_cupom/CT-CUP-03-desconto-recalculado-cupom-aplicado.png) |
| CT-CUP-04 | Código do cupom ignora maiúsculas, minúsculas e espaços nas pontas (4 exemplos) | CA02 | Interface | Sim | ✅ | [automação](evidencias/automacao/resultado.xml) |
| CT-CUP-05 | Espaço no meio do código não é ignorado | CA02 | Interface | Não | ✅ | [print](evidencias/feature_cupom/CT-CUP-05-espaco-ignorado-cupom-invalido.png) |
| CT-CUP-06 | Cupom inexistente exibe "Cupom inválido." e não gera desconto | CA03 | Interface | Sim | ✅ | [automação](evidencias/automacao/resultado.xml) |
| CT-CUP-07 | Aplicar com o campo de cupom vazio não gera desconto | CA03 | Interface | Não | ✅ | [print](evidencias/feature_cupom/CT-CUP-07-cupom-vazio-nao-gera-desconto.png) |
| CT-CUP-08 | Cupom fora da validade exibe "Cupom expirado." e não gera desconto | CA04 | Interface | Sim | ✅ | [automação](evidencias/automacao/resultado.xml) |
| CT-CUP-09 | Cupom expirado digitado em minúsculas continua sendo identificado como expirado | CA02, CA04 | Interface | Não | ✅ | [print](evidencias/feature_cupom/CT-CUP-09-cupom-minusculo-continua-expirado.png) |
| CT-CUP-10 | Com um cupom aplicado não é possível informar um segundo cupom | CA05 | Interface | Sim | ✅ | [automação](evidencias/automacao/resultado.xml) |
| CT-CUP-11 | Remover o cupom zera o desconto e libera o campo novamente | CA05 | Interface | Sim | ✅ | [automação](evidencias/automacao/resultado.xml) |
| CT-CUP-12 | Trocar de cupom exige remover o atual e aplicar o outro | CA05 | Interface | Não | ✅ | [print 1](evidencias/feature_cupom/CT-CUP-12_1-cupom-exige-remover-atual.png) · [print 2](evidencias/feature_cupom/CT-CUP-12_2-cupom-exige-remover-atual.png) |
| CT-CUP-13 | Cupom válido aplicado depois de uma tentativa inválida limpa a mensagem de erro | CA03 | Interface | Não | ✅ | [print 1](evidencias/feature_cupom/CT-CUP-13_1-cupom-valido-aplicado-apos-invalido.png) · [print 2](evidencias/feature_cupom/CT-CUP-13_2-cupom-valido-aplicado-apos-invalido.png) |
| CT-CUP-14 | Cupom aplicado no carrinho é mantido no checkout e na confirmação do pedido | CA01 | Interface | Sim | ✅ | [automação](evidencias/automacao/resultado.xml) |
| CT-CUP-15 | Cupom continua aplicado depois de remover um dos itens do carrinho | CA01 | Interface | Não | ✅ | [print 1](evidencias/feature_cupom/CT-CUP-15_1-cupom-ativado-apos-remover-item.png) · [print 2](evidencias/feature_cupom/CT-CUP-15_2-cupom-ativado-apos-remover-item.png) |

### Frete grátis a partir de R$ 200,00

Arquivo: [`02-frete.feature`](cenarios/02-frete.feature)

| ID | Cenário | Critério | Tipo | Automatizado | Status | Evidência / Bug |
| --- | --- | --- | --- | --- | --- | --- |
| CT-FRE-01 | Subtotal de exatamente R$ 200,00 tem frete grátis | CA06 | Interface | Sim | ❌ | [BUG-001](03-bugs.md#bug-001) · [automação](evidencias/automacao/resultado.xml) · [API](evidencias/api/BUG-001-calcular-200.md) |
| CT-FRE-02 | Subtotal de R$ 200,00 formado por outro produto também tem frete grátis | CA06 | Interface | Não | ❌ | [BUG-001](03-bugs.md#bug-001) · [print](evidencias/feature_frete/CT-FRE-02-subtotal-200-frete-gratis.png) |
| CT-FRE-03 | Subtotal acima de R$ 200,00 tem frete grátis | CA06 | Interface | Sim | ✅ | [automação](evidencias/automacao/resultado.xml) |
| CT-FRE-04 | Subtotal imediatamente abaixo de R$ 200,00 paga frete fixo e informa o valor faltante | CA07 | Interface | Sim | ✅ | [automação](evidencias/automacao/resultado.xml) |
| CT-FRE-05 | Compra pequena paga frete fixo de R$ 19,90 e informa o valor faltante | CA07 | Interface | Não | ✅ | [print](evidencias/feature_frete/CT-FRE-05-compra-pequena-frete-fixo.png) |
| CT-FRE-06 | Frete e aviso são atualizados quando o subtotal cruza o limite nos dois sentidos | CA06, CA07 | Interface | Não | ✅ | [print 1](evidencias/feature_frete/CT-FRE-06_1-frete-aviso-atualizados-subtotal-cruza-limite.png) · [print 2](evidencias/feature_frete/CT-FRE-06_2-frete-aviso-atualizados-subtotal-cruza-limite.png) |
| CT-FRE-07 | Frete grátis considera o subtotal antes do desconto do cupom | CA08 | Interface | Sim | ✅ | [automação](evidencias/automacao/resultado.xml) |
| CT-FRE-08 | Subtotal de exatamente R$ 200,00 com cupom mantém o frete grátis | CA06, CA08 | Interface | Não | ❌ | [BUG-001](03-bugs.md#bug-001) · [print](evidencias/feature_frete/CT-FRE-08-subtotal-200-com-cupom-frete-gratis.png) |
| CT-FRE-09 | Aplicar o cupom não altera o valor faltante para o frete grátis | CA08 | Interface | Não | ✅ | [print](evidencias/feature_frete/CT-FRE-09-cupom-nao-altera-faltante-para-frete.png) |
| CT-FRE-10 | Desconto do cupom não incide sobre o frete | CA09 | Interface | Sim | ✅ | [automação](evidencias/automacao/resultado.xml) |
| CT-FRE-11 | Frete grátis é mantido no checkout e na confirmação do pedido | CA06 | Interface | Não | ✅ | [print](evidencias/feature_frete/CT-FRE-11-frete-gratis-mantido-checkout-e-confirmacao.png) |

### Limite de 5 unidades por produto

Arquivo: [`03-quantidade.feature`](cenarios/03-quantidade.feature)

| ID | Cenário | Critério | Tipo | Automatizado | Status | Evidência / Bug |
| --- | --- | --- | --- | --- | --- | --- |
| CT-QTD-01 | Vitrine não permite adicionar a sexta unidade do mesmo produto | CA10 | Interface | Sim | ✅ | [automação](evidencias/automacao/resultado.xml) |
| CT-QTD-02 | Carrinho não permite aumentar a quantidade acima de 5 | CA10 | Interface | Sim | ✅ | [automação](evidencias/automacao/resultado.xml) |
| CT-QTD-03 | Carrinho não permite diminuir a quantidade abaixo de 1 | CA10 | Interface | Não | ✅ | [print](evidencias/feature_qntd/CT-QTD-03-botao-diminuir-desabilitado.png) |
| CT-QTD-04 | O limite é por produto, não pelo total de itens do carrinho | CA10 | Interface | Não | ✅ | [print](evidencias/feature_qntd/CT-QTD-04-limite-por-produto-nao-total.png) |
| CT-QTD-05 | Limite continua valendo depois de voltar do carrinho para a vitrine | CA10 | Interface | Não | ✅ | [print](evidencias/feature_qntd/CT-QTD-05-limite-continua-na-vitrine.png) |
| CT-QTD-06 | API calcula o carrinho com 5 unidades de um produto | CA10 | API | Sim | ✅ | [automação](evidencias/automacao/resultado.xml) · [API](evidencias/api/CT-QTD-06-calcular-5-unidades.md) |
| CT-QTD-07 | API recusa o cálculo do carrinho com 6 unidades de um produto | CA10 | API | Sim | ❌ | [BUG-002](03-bugs.md#bug-002) · [automação](evidencias/automacao/resultado.xml) · [API](evidencias/api/BUG-002-calcular-6-unidades.md) |
| CT-QTD-08 | API recusa o pedido com 6 unidades de um produto | CA10 | API | Sim | ❌ | [BUG-002](03-bugs.md#bug-002) · [automação](evidencias/automacao/resultado.xml) · [API](evidencias/api/BUG-002-pedido-6-unidades.md) |
| CT-QTD-09 | API recusa quantidade que não é um inteiro maior ou igual a 1 (5 exemplos) | CA10 | API | Sim | ✅ | [automação](evidencias/automacao/resultado.xml) |

### Cálculo do pedido e arredondamento

Arquivo: [`04-calculo-e-arredondamento.feature`](cenarios/04-calculo-e-arredondamento.feature)

| ID | Cenário | Critério | Tipo | Automatizado | Status | Evidência / Bug |
| --- | --- | --- | --- | --- | --- | --- |
| CT-CAL-01 | Exemplo de cálculo da documentação | CA11 | API | Sim | ✅ | [automação](evidencias/automacao/resultado.xml) · [API](evidencias/api/CT-CAL-01-exemplo-da-documentacao.md) |
| CT-CAL-02 | Valores com centavos são devolvidos com no máximo 2 casas decimais (7 exemplos) | CA11 | API | Sim | ✅ | [automação](evidencias/automacao/resultado.xml) |
| CT-CAL-03 | Total de cada item é o preço unitário vezes a quantidade | CA11 | API | Sim | ✅ | [automação](evidencias/automacao/resultado.xml) |
| CT-CAL-04 | Valor faltante para o frete grátis nunca é negativo | CA07 | API | Sim | ✅ | [automação](evidencias/automacao/resultado.xml) |
| CT-CAL-05 | Interface exibe todos os valores com 2 casas decimais no formato brasileiro | CA11 | Interface | Não | ✅ | [print](evidencias/feature_calculo/CT-CAL-05-exibe-valores-decimais-em-ptbr.png) |
| CT-CAL-06 | Valores acima de mil reais usam separador de milhar | CA11 | Interface | Não | ✅ | [print](evidencias/feature_calculo/CT-CAL-06-valores-acima-1000-separa-por-milhar.png) |

### Finalização da compra

Arquivo: [`05-checkout.feature`](cenarios/05-checkout.feature)

| ID | Cenário | Critério | Tipo | Automatizado | Status | Evidência / Bug |
| --- | --- | --- | --- | --- | --- | --- |
| CT-CHK-01 | Pedido é confirmado com dados válidos | Regressão | Interface | Sim | ✅ | [automação](evidencias/automacao/resultado.xml) |
| CT-CHK-02 | Resumo do checkout repete os valores e os itens do carrinho | Regressão | Interface | Não | ✅ | [checkout](evidencias/feature_checkout/CT-CHK-10-formulario-em-branco-aponta-obrigatorios.png) · [confirmação](evidencias/feature_checkout/CT-CHK-02e03-resumo-checkout-repete-valores-e-itens-com-pagamento-entrega.png) |
| CT-CHK-03 | Checkout informa que o pagamento é feito na entrega | Regressão | Interface | Não | ✅ | [checkout](evidencias/feature_checkout/CT-CHK-10-formulario-em-branco-aponta-obrigatorios.png) · [confirmação](evidencias/feature_checkout/CT-CHK-02e03-resumo-checkout-repete-valores-e-itens-com-pagamento-entrega.png) |
| CT-CHK-04 | Nome sem sobrenome é recusado (3 exemplos) | Regressão | Interface | Sim | ✅ | [automação](evidencias/automacao/resultado.xml) |
| CT-CHK-05 | Nome com nome e sobrenome é aceito (6 exemplos) | Regressão | Interface | Não | ⬜ | |
| CT-CHK-06 | E-mail em formato inválido é recusado (7 exemplos) | Regressão | Interface | Sim | ✅ | [automação](evidencias/automacao/resultado.xml) |
| CT-CHK-07 | E-mail em formato válido é aceito (3 exemplos) | Regressão | Interface | Não | ⬜ | |
| CT-CHK-08 | CEP que não tem 8 dígitos é recusado (6 exemplos) | Regressão | Interface | Sim | ✅ | [automação](evidencias/automacao/resultado.xml) |
| CT-CHK-09 | CEP com 8 dígitos é aceito com ou sem hífen (2 exemplos) | Regressão | Interface | Sim | ✅ | [automação](evidencias/automacao/resultado.xml) |
| CT-CHK-10 | Formulário em branco aponta os três campos obrigatórios de uma vez | Regressão | Interface | Não | ✅ | [print](evidencias/feature_checkout/CT-CHK-10-formulario-em-branco-aponta-obrigatorios.png) |
| CT-CHK-11 | Corrigir os dados depois de um erro permite confirmar o pedido | Regressão | Interface | Não | ✅ | [print](evidencias/feature_checkout/CT-CHK-11-erro-e-solicitar-corrigir-dados.png) |
| CT-CHK-12 | Checkout não fica acessível com o carrinho vazio | Regressão | Interface | Não | ⬜ | |

### API de produtos e tratamento geral de erros

Arquivo: [`06-api-produtos-e-erros.feature`](cenarios/06-api-produtos-e-erros.feature)

| ID | Cenário | Critério | Tipo | Automatizado | Status | Evidência / Bug |
| --- | --- | --- | --- | --- | --- | --- |
| CT-API-01 | Listar produtos devolve os 8 produtos da documentação | Doc. da API | API | Sim | ✅ | [automação](evidencias/automacao/resultado.xml) · [API](evidencias/api/CT-API-01-listar-produtos.md) |
| CT-API-02 | Consultar um produto existente pelo id | Doc. da API | API | Sim | ✅ | [automação](evidencias/automacao/resultado.xml) |
| CT-API-03 | Consultar um produto inexistente devolve 404 | Doc. da API | API | Sim | ✅ | [automação](evidencias/automacao/resultado.xml) · [API](evidencias/api/CT-API-03-produto-inexistente.md) |
| CT-API-04 | Preços da vitrine são os mesmos devolvidos pela API | Doc. da API | API | Não | ⬜ | |
| CT-API-05 | Rota inexistente devolve 404 ROTA_NAO_ENCONTRADA | Doc. da API | API | Sim | ✅ | [automação](evidencias/automacao/resultado.xml) |
| CT-API-06 | Método não aceito pela rota devolve 405 METODO_NAO_PERMITIDO (4 exemplos) | Doc. da API | API | Sim | ✅ | [automação](evidencias/automacao/resultado.xml) |
| CT-API-07 | Corpo que não é um objeto JSON válido devolve 400 JSON_INVALIDO (3 exemplos) | Doc. da API | API | Sim | ✅ | [automação](evidencias/automacao/resultado.xml) |
| CT-API-08 | Todo erro segue o formato padrão | Doc. da API | API | Não | ⬜ | |

### API de cálculo do carrinho

Arquivo: [`07-api-carrinho.feature`](cenarios/07-api-carrinho.feature)

| ID | Cenário | Critério | Tipo | Automatizado | Status | Evidência / Bug |
| --- | --- | --- | --- | --- | --- | --- |
| CT-APC-01 | Cupom BEMVINDO10 aplica 10% sobre o subtotal | CA01 | API | Sim | ✅ | [automação](evidencias/automacao/resultado.xml) |
| CT-APC-02 | Código do cupom ignora caixa e espaços nas pontas (4 exemplos) | CA02 | API | Sim | ✅ | [automação](evidencias/automacao/resultado.xml) · [API](evidencias/api/CT-APC-02-cupom-minusculas-com-espacos.md) |
| CT-APC-03 | Cupom inexistente responde 200 sem desconto | CA03 | API | Sim | ✅ | [automação](evidencias/automacao/resultado.xml) · [API](evidencias/api/CT-APC-03-cupom-inexistente.md) |
| CT-APC-04 | Cupom expirado responde 200 sem desconto | CA04 | API | Sim | ✅ | [automação](evidencias/automacao/resultado.xml) · [API](evidencias/api/CT-APC-04-cupom-expirado.md) |
| CT-APC-05 | Cálculo sem o campo cupom não aplica desconto | CA01 | API | Sim | ✅ | [automação](evidencias/automacao/resultado.xml) |
| CT-APC-06 | Frete conforme o subtotal (6 exemplos) | CA06, CA07 | API | Sim | ❌ | [BUG-001](03-bugs.md#bug-001) · [automação](evidencias/automacao/resultado.xml) · [API](evidencias/api/BUG-001-calcular-200.md) |
| CT-APC-07 | Frete grátis considera o subtotal antes do desconto | CA08 | API | Sim | ✅ | [automação](evidencias/automacao/resultado.xml) · [API](evidencias/api/CT-APC-07-frete-antes-do-desconto.md) |
| CT-APC-08 | Desconto não incide sobre o frete | CA09 | API | Sim | ✅ | [automação](evidencias/automacao/resultado.xml) |
| CT-APC-09 | Lista de itens ausente ou vazia devolve 422 ITENS_OBRIGATORIOS (2 exemplos) | Doc. da API | API | Sim | ✅ | [automação](evidencias/automacao/resultado.xml) |
| CT-APC-10 | Item que não é um objeto com produtoId e quantidade devolve 422 ITEM_INVALIDO | Doc. da API | API | Sim | ✅ | [automação](evidencias/automacao/resultado.xml) |
| CT-APC-11 | Item com produto inexistente devolve 422 PRODUTO_NAO_ENCONTRADO | Doc. da API | API | Sim | ✅ | [automação](evidencias/automacao/resultado.xml) |
| CT-APC-12 | Mesmo produto repetido na lista devolve 422 ITEM_DUPLICADO | Doc. da API | API | Sim | ✅ | [automação](evidencias/automacao/resultado.xml) |
| CT-APC-13 | Cálculo não grava nada entre uma chamada e outra | Doc. da API | API | Não | ⬜ | |

### API de pedidos

Arquivo: [`08-api-pedidos.feature`](cenarios/08-api-pedidos.feature)

| ID | Cenário | Critério | Tipo | Automatizado | Status | Evidência / Bug |
| --- | --- | --- | --- | --- | --- | --- |
| CT-APP-01 | Pedido válido com cupom é confirmado | Doc. da API | API | Sim | ✅ | [automação](evidencias/automacao/resultado.xml) · [API](evidencias/api/CT-APP-01-pedido-com-cupom.md) |
| CT-APP-02 | Pedido devolve os mesmos valores do cálculo do carrinho | Doc. da API | API | Sim | ✅ | [automação](evidencias/automacao/resultado.xml) |
| CT-APP-03 | Pedido com cupom inexistente devolve 422 CUPOM_INVALIDO | CA03 | API | Sim | ✅ | [automação](evidencias/automacao/resultado.xml) |
| CT-APP-04 | Pedido com cupom expirado devolve 422 CUPOM_EXPIRADO | CA04 | API | Sim | ✅ | [automação](evidencias/automacao/resultado.xml) · [API](evidencias/api/CT-APP-04-pedido-cupom-expirado.md) |
| CT-APP-05 | Pedido com subtotal de exatamente R$ 200,00 tem frete grátis | CA06 | API | Sim | ❌ | [BUG-001](03-bugs.md#bug-001) · [automação](evidencias/automacao/resultado.xml) · [API](evidencias/api/BUG-001-pedido-200.md) |
| CT-APP-06 | Dados do cliente inválidos devolvem 422 DADOS_INVALIDOS (7 exemplos) | Doc. da API | API | Sim | ✅ | [automação](evidencias/automacao/resultado.xml) |
| CT-APP-07 | Pedido sem os dados do cliente aponta os três campos | Doc. da API | API | Sim | ✅ | [automação](evidencias/automacao/resultado.xml) |
| CT-APP-08 | CEP com 8 dígitos é aceito com ou sem hífen (2 exemplos) | Doc. da API | API | Sim | ✅ | [automação](evidencias/automacao/resultado.xml) |
| CT-APP-09 | Pedido sem itens devolve 422 ITENS_OBRIGATORIOS | Doc. da API | API | Sim | ✅ | [automação](evidencias/automacao/resultado.xml) |
| CT-APP-10 | Número do pedido é gerado a cada confirmação | Doc. da API | API | Não | ⬜ | |

## Testes exploratórios

Sessões curtas com uma missão definida, sem roteiro passo a passo. O que foi encontrado virou bug em [03-bugs.md](03-bugs.md) ou observação em [05-ambiguidades-e-observacoes.md](05-ambiguidades-e-observacoes.md).

### Sessão 1: entradas inesperadas no cupom

| | |
| --- | --- |
| Missão | Descobrir como o campo de cupom e a API se comportam com entradas que a documentação não prevê. |
| Duração | _preencher_ |
| O que explorar | Campo vazio, só espaços, espaço no meio, caracteres especiais, texto muito longo, cupom como número ou lista na API, aplicar duas vezes seguidas, aplicar e esvaziar o carrinho. |
| Anotações | _preencher_ |
| Resultado | _preencher_ |

### Sessão 2: dados do cliente no checkout

| | |
| --- | --- |
| Missão | Encontrar nomes, e-mails e CEPs válidos que são recusados e inválidos que são aceitos. |
| Duração | _preencher_ |
| O que explorar | Nomes com acento, apóstrofo, hífen, partes de uma letra, só números. E-mails com subdomínio, sinal de mais, dois pontos seguidos, ponto no fim. CEP com espaços, pontos, só zeros. Comparar a interface com a API para o mesmo dado. |
| Anotações | _preencher_ |
| Resultado | _preencher_ |

### Sessão 3: navegação e estado do carrinho

| | |
| --- | --- |
| Missão | Verificar se o carrinho, o cupom e o resumo continuam coerentes fora do caminho feliz. |
| Duração | _preencher_ |
| O que explorar | Recarregar a página em cada etapa, botão voltar do navegador depois de confirmar o pedido, abrir /checkout e /pedido-confirmado direto pelo endereço, esvaziar o carrinho com cupom aplicado, cliques rápidos nos botões de quantidade, tela estreita de celular, navegação só pelo teclado. |
| Anotações | _preencher_ |
| Resultado | _preencher_ |

### Sessão 4: contrato da API

| | |
| --- | --- |
| Missão | Procurar diferenças entre o que a documentação da API promete e o que ela responde. |
| Duração | _preencher_ |
| O que explorar | Rotas com barra no fim, /api sem caminho, requisição sem Content-Type, campos extras no corpo, produtoId em minúsculas, quantidade muito grande, formato dos erros em cada status. |
| Anotações | _preencher_ |
| Resultado | _preencher_ |
