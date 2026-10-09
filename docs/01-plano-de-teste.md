# Plano de teste: VZS-142, cupom de desconto e frete grátis

| | |
| --- | --- |
| Entrega | VZS-142, versão 2.3.0, publicada em 30/09/2026 |
| Ambiente | <https://verzel-store.qa-test-verzel-store.workers.dev> |
| Documentação | <https://verzel-store.qa-test-verzel-store.workers.dev/documentacao> |
| Período de execução | 09/10/2026 |
| Navegador e sistema | Brave/Chrome - Windows 11 |

## O que foi testado

1. Os 11 critérios de aceite da entrega (CA01 a CA11), na interface e na API.
2. As regras que já existiam antes da entrega (nome, e-mail, CEP e pagamento na entrega), como regressão: a entrega mexeu no carrinho e no resumo do pedido, que alimentam o checkout.
3. O contrato da API descrito na documentação: rotas, status, formato das respostas e tabela de códigos de erro.

## O que ficou de fora

| Item | Motivo |
| --- | --- |
| Carga, estresse e segurança | Fora do escopo pelo enunciado: o ambiente é compartilhado. |
| Login, cadastro, pagamento online, consulta de pedidos | Fora do escopo pela documentação. |
| Carrinho entre abas, armazenamento de pedidos, envio de e-mail, estoque | Simplificações declaradas na seção "Sobre este ambiente". Não são bugs. |

## Como os cenários foram levantados

Cada critério de aceite virou pelo menos um cenário positivo e um negativo. Três técnicas guiaram a escolha dos dados:

- **Análise de valor-limite.** As regras com fronteira numérica foram testadas no limite e nos vizinhos imediatos. Para o frete grátis (R$ 200,00), os subtotais R$ 199,70, R$ 200,00 e R$ 219,80; para o limite de unidades, 5 e 6; para a quantidade mínima, 0 e 1. Os produtos da loja permitem montar exatamente R$ 200,00 de duas formas (2 mochilas ou 4 garrafas), e as duas foram usadas para descartar um problema ligado a um produto específico.
- **Partição de equivalência.** Entradas que a regra trata do mesmo jeito foram agrupadas e cada grupo recebeu um representante: cupom válido, inexistente e expirado; CEP com hífen, sem hífen e malformado.
- **Tabela de decisão.** A combinação cupom × frete tem quatro casos (com e sem cupom, acima e abaixo do limite). O caso que mais interessa é o do CA08: subtotal acima de R$ 200,00 que cai abaixo desse valor depois do desconto.

Os mesmos critérios foram verificados em dois níveis. Na **API**, porque é ela que faz os cálculos e é onde uma regra pode ser burlada sem passar pela tela. Na **interface**, porque é o que o cliente vê e porque ela pode exibir errado um valor que a API calculou certo.

Além dos cenários roteirizados, foram feitas sessões de **teste exploratório** com missão definida, registradas em [02-execucao-dos-testes.md](02-execucao-dos-testes.md).

## Rastreabilidade: critério de aceite × cenários

| Critério | Cenários de interface | Cenários de API |
| --- | --- | --- |
| CA01 desconto de 10% | CT-CUP-01, 02, 03, 14, 15 | CT-APC-01, 05 |
| CA02 caixa e espaços | CT-CUP-04, 05, 09 | CT-APC-02 |
| CA03 cupom inválido | CT-CUP-06, 07, 13 | CT-APC-03, CT-APP-03 |
| CA04 cupom expirado | CT-CUP-08, 09 | CT-APC-04, CT-APP-04 |
| CA05 um cupom por vez | CT-CUP-10, 11, 12 | não se aplica: a API recebe um único campo `cupom` |
| CA06 frete grátis a partir de R$ 200,00 | CT-FRE-01, 02, 03, 06, 08, 11 | CT-APC-06, CT-APP-05 |
| CA07 frete fixo e valor faltante | CT-FRE-04, 05, 06 | CT-APC-06, CT-CAL-04 |
| CA08 frete pelo subtotal antes do desconto | CT-FRE-07, 08, 09 | CT-APC-07 |
| CA09 desconto não incide no frete | CT-FRE-10 | CT-APC-08 |
| CA10 máximo de 5 unidades | CT-QTD-01 a 05 | CT-QTD-06 a 09 |
| CA11 duas casas decimais | CT-CAL-05, 06 | CT-CAL-01, 02, 03 |
| Regras anteriores (regressão) | CT-CHK-01 a 12 | CT-APP-01, 02, 06 a 10 |
| Contrato da API | CT-API-04 | CT-API-01 a 08, CT-APC-09 a 13 |

## Critério para classificar os bugs

| Severidade | Quando se aplica |
| --- | --- |
| Alta | Um critério de aceite não é atendido e o cliente ou a loja tem prejuízo financeiro, ou uma regra de negócio pode ser burlada. |
| Média | Um critério de aceite não é atendido, mas existe contorno ou o impacto é limitado. |
| Baixa | Comportamento inconsistente ou confuso que não descumpre um critério de aceite. |
