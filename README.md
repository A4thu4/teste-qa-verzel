# Teste técnico de QA Júnior: Verzel Store

Validação da entrega **VZS-142, cupom de desconto e frete grátis** (versão 2.3.0) da Verzel Store.

- Loja: <https://verzel-store.qa-test-verzel-store.workers.dev/>
- Documentação da entrega: <https://verzel-store.qa-test-verzel-store.workers.dev/documentacao>

## Resultado em resumo

| | |
| --- | --- |
| Cenários levantados | 84, cobrindo os 11 critérios de aceite, as regras anteriores à entrega e o contrato da API |
| Cenários automatizados | 57, com Playwright (Python) |
| Bugs encontrados | 2, ambos de severidade alta: [BUG-001](docs/03-bugs.md#bug-001), subtotal de exatamente R$ 200,00 sem frete grátis (CA06), e [BUG-002](docs/03-bugs.md#bug-002), API aceitando mais de 5 unidades por produto (CA10) |
| Parecer | **Não recomendada para produção** até a correção dos dois bugs. O BUG-001 cobra frete de quem a promoção anunciada diz que não deveria pagar, inclusive em pedidos confirmados. O BUG-002 deixa uma regra de negócio depender só da tela: quem chama a API direto fecha pedidos acima do limite. Os outros 9 critérios de aceite foram atendidos na interface e na API, com a ressalva do CA11: o arredondamento não pôde ser exercitado com os dados disponíveis ([AMB-01](docs/05-ambiguidades-e-observacoes.md)). |

## Onde encontrar cada entrega

| Entrega pedida | Onde está |
| --- | --- |
| Cenários de teste em Gherkin | [`docs/cenarios/`](docs/cenarios/), um arquivo `.feature` por funcionalidade |
| Execução dos testes, manuais e exploratórios, com o resultado de cada cenário | [`docs/02-execucao-dos-testes.md`](docs/02-execucao-dos-testes.md) |
| Report dos bugs | [`docs/03-bugs.md`](docs/03-bugs.md) |
| Evidências da execução | [`docs/04-evidencias.md`](docs/04-evidencias.md) e a pasta [`docs/evidencias/`](docs/evidencias/) |
| Automação com Playwright | [`automacao/`](automacao/) |
| Como rodar a automação | [Nesta página](#como-rodar-a-automação) |

Documentos de apoio:

- [`docs/01-plano-de-teste.md`](docs/01-plano-de-teste.md): escopo, técnicas usadas e rastreabilidade entre critérios de aceite e cenários.
- [`docs/05-ambiguidades-e-observacoes.md`](docs/05-ambiguidades-e-observacoes.md): pontos ambíguos da documentação com a interpretação adotada.
- [`Uso de inteligência artificial`](#uso-de-inteligência-artificial): onde e como a IA foi usada neste teste.

## Estrutura do repositório

```bash
├── README.md
├── docs/
│   ├── 01-plano-de-teste.md
│   ├── 02-execucao-dos-testes.md
│   ├── 03-bugs.md
│   ├── 04-evidencias.md
│   ├── 05-ambiguidades-e-observacoes.md
│   ├── cenarios/                 cenários em Gherkin
│   │   ├── 01-cupom.feature
│   │   ├── 02-frete.feature
│   │   ├── 03-quantidade.feature
│   │   ├── 04-calculo-e-arredondamento.feature
│   │   ├── 05-checkout.feature
│   │   ├── 06-api-produtos-e-erros.feature
│   │   ├── 07-api-carrinho.feature
│   │   └── 08-api-pedidos.feature
│   └── evidencias/               capturas de tela e respostas da API
├── .devcontainer/                configuração do GitHub Codespaces
└── automacao/
    ├── requirements.txt
    ├── pytest.ini                endereço da loja e opções do pytest
    ├── conftest.py               fixtures compartilhadas
    ├── coletar_evidencias_api.py grava requisição e resposta da API em arquivos
    ├── explorar_api.py           requisições fora do roteiro das sessões exploratórias
    ├── explorar_interface.py     tentativas fora do roteiro na interface, com capturas
    ├── pages/loja.py             page objects: vitrine, carrinho, checkout, confirmação
    └── tests/
        ├── dados.py              produtos, cupons e cálculo do resultado esperado
        ├── api/                  testes que chamam a API diretamente
        └── ui/                   testes que usam a loja no navegador
```

## Como os cenários estão identificados

Cada cenário tem um ID no formato `CT-<área>-<número>`, usado igual nos arquivos `.feature`, na tabela de execução, nos bugs, nos nomes das evidências e nos nomes dos testes automatizados (`test_ct_cup_01_...`).

| Prefixo | Área |
| --- | --- |
| CT-CUP | Cupom de desconto (CA01 a CA05) |
| CT-FRE | Frete grátis (CA06 a CA09) |
| CT-QTD | Limite de unidades por produto (CA10) |
| CT-CAL | Cálculo e arredondamento (CA11) |
| CT-CHK | Checkout, regras anteriores à entrega |
| CT-API, CT-APC, CT-APP | API: produtos e erros, carrinho, pedidos |

## Como rodar a automação

### Pré-requisitos

- Python 3.10 ou mais recente
- Acesso à internet: os testes rodam contra a loja publicada

### Instalação

No Windows (PowerShell), a partir da raiz do repositório:

```powershell
cd automacao
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
playwright install chromium
```

No Linux ou macOS, troque a terceira linha por `source .venv/bin/activate`.

### Execução

```powershell
pytest                    # tudo: API e interface
pytest tests/api          # só a API, sem abrir navegador
pytest tests/ui           # só a interface
pytest tests/ui --headed  # interface com o navegador visível
pytest -k ct_fre          # só os testes cujo nome contém "ct_fre"
```

Para gerar evidências da execução (captura de tela, vídeo e trace dos testes que falharem, mais um relatório em XML):

```powershell
pytest --screenshot only-on-failure --video retain-on-failure --tracing retain-on-failure --output ../docs/evidencias/automacao --junitxml ../docs/evidencias/automacao/resultado.xml
```

Para gravar a requisição e a resposta das principais chamadas à API em `docs/evidencias/api/`:

```powershell
python coletar_evidencias_api.py
```

Para rodar as tentativas de API das sessões exploratórias e gravar o relatório em `docs/evidencias/exploratorio/sessoes-api.md`:

```powershell
python explorar_api.py
```

Para rodar as tentativas de interface das sessões exploratórias, com uma captura de cada uma, e gravar o relatório em `docs/evidencias/exploratorio/sessoes-interface.md` (no Windows, acrescente `--headed` para ver o navegador):

```powershell
python explorar_interface.py
```

### No GitHub Codespaces, sem instalar nada no computador

O repositório tem uma configuração de devcontainer em [`.devcontainer/`](.devcontainer/devcontainer.json). Ao criar um Codespace, as dependências e o Chromium são instalados automaticamente.

1. Na página do repositório, clique em **Code**, aba **Codespaces**, e depois em **Create codespace on** o branch desejado.
2. Espere a instalação terminar. O terminal mostra o progresso do `postCreateCommand` na primeira abertura.
3. No terminal:

```bash
cd automacao
pytest
```

O Codespace não tem tela, então os testes rodam sem abrir o navegador e a opção `--headed` não funciona. Para ver o que aconteceu em um teste de interface, gere o trace e abra o arquivo `trace.zip` em <https://trace.playwright.dev>:

```bash
pytest tests/ui --tracing on --output ../docs/evidencias/automacao
```

Os testes também aparecem na aba **Testing** do VS Code do Codespace, onde podem ser rodados um a um.

### Como ler o resultado

Os testes descrevem o comportamento **esperado pela documentação**. Os que cobrem um bug já reportado estão marcados com `xfail` e o ID do bug:

| Resultado | Significado |
| --- | --- |
| `passed` | A loja se comporta como a documentação descreve. |
| `xfailed` | Falha esperada: o teste confirma que um bug já reportado continua presente. O motivo aparece no resumo final. |
| `failed` | Comportamento diferente do esperado e ainda não reportado. Precisa ser investigado. |
| `XPASS(strict)`, contado como `failed` | Um teste marcado como bug passou: o bug foi corrigido e a marcação `xfail` deve ser removida. |

Com isso a suíte fica verde enquanto só existirem os bugs conhecidos, e qualquer falha nova chama atenção.

### Cuidados com o ambiente compartilhado

A loja é usada por outros candidatos ao mesmo tempo. A suíte roda em sequência, faz cerca de uma centena de requisições leves e não inclui teste de carga, estresse ou segurança.

## Uso de inteligência artificial

Usei o Claude (Anthropic) como assistente durante todo o teste. Os commits em que ele participou estão identificados no histórico com `Co-Authored-By: Claude`.

### Onde a IA foi usada

| Etapa | O que a IA fez | O que eu fiz |
| --- | --- | --- |
| Cenários de teste | Redigiu os 84 cenários em Gherkin a partir da documentação da entrega e montou a rastreabilidade com os critérios de aceite. | Revisei os cenários e executei manualmente os 24 de interface que não foram automatizados, com as capturas de tela. |
| Automação | Ajudou a estruturar a suíte em Playwright com Python (page objects, fixtures, testes de API e de interface) e a configuração do Codespaces. | Rodei a suíte no GitHub Codespaces, acompanhei a correção do erro de instalação do navegador e gerei o relatório final (107 `passed`, 6 `xfailed`). |
| Bugs | Apontou os dois desvios (BUG-001 e BUG-002) ao explorar a loja e a API, e redigiu os reports. | Reproduzi os dois: o BUG-001 manualmente na interface, com captura, e o BUG-002 pela API, com o script de evidências e os testes automatizados. |
| Testes exploratórios | Estruturou os scripts `explorar_api.py` e `explorar_interface.py` com as tentativas de cada sessão e registrou as observações a partir dos resultados. | Defini que as sessões seriam feitas por script, executei os scripts e versionei os relatórios e capturas gerados. |
| Evidências de API | Estruturou o script `coletar_evidencias_api.py`. | Executei o script, ajustei o registro de horário para o fuso de Brasília e versionei os arquivos gerados. |
| Documentação | Redigiu o plano de teste, a tabela de execução, o registro de ambiguidades e o README, incluindo o parecer. | Preenchi os dados de execução e ambiente, revisei o conteúdo e aprovei cada alteração por pull request antes de ir para o `main`. |

### Como foi usada

- Trabalhei em conversa com a IA: ela propunha e eu executava, conferia o resultado no ambiente real e pedia ajustes.
- Toda execução contra a loja que consta como evidência foi feita por mim: os testes manuais, a suíte automatizada e os scripts.
- Usei as explicações da IA para estudar os conceitos aplicados (análise de valor-limite, partição de equivalência, page objects, `xfail`).
