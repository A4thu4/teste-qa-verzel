# Teste técnico de QA Júnior: Verzel Store

Validação da entrega **VZS-142, cupom de desconto e frete grátis** (versão 2.3.0) da Verzel Store.

- Loja: https://verzel-store.qa-test-verzel-store.workers.dev/
- Documentação da entrega: https://verzel-store.qa-test-verzel-store.workers.dev/documentacao

## Resultado em resumo

| | |
|---|---|
| Cenários levantados | 84, cobrindo os 11 critérios de aceite, as regras anteriores à entrega e o contrato da API |
| Cenários automatizados | 54, com Playwright (Python) |
| Bugs encontrados | _preencher após a execução_ |
| Parecer | _preencher: a entrega pode ou não seguir para produção, e por quê_ |

## Onde encontrar cada entrega

| Entrega pedida | Onde está |
|---|---|
| Cenários de teste em Gherkin | [`docs/cenarios/`](docs/cenarios/), um arquivo `.feature` por funcionalidade |
| Execução dos testes, manuais e exploratórios, com o resultado de cada cenário | [`docs/02-execucao-dos-testes.md`](docs/02-execucao-dos-testes.md) |
| Report dos bugs | [`docs/03-bugs.md`](docs/03-bugs.md) |
| Evidências da execução | [`docs/04-evidencias.md`](docs/04-evidencias.md) e a pasta [`docs/evidencias/`](docs/evidencias/) |
| Automação com Playwright | [`automacao/`](automacao/) |
| Como rodar a automação | [Nesta página](#como-rodar-a-automação) |

Documentos de apoio:

- [`docs/01-plano-de-teste.md`](docs/01-plano-de-teste.md): escopo, técnicas usadas e rastreabilidade entre critérios de aceite e cenários.
- [`docs/05-ambiguidades-e-observacoes.md`](docs/05-ambiguidades-e-observacoes.md): pontos ambíguos da documentação com a interpretação adotada.

## Estrutura do repositório

```
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
    ├── pages/loja.py             page objects: vitrine, carrinho, checkout, confirmação
    └── tests/
        ├── dados.py              produtos, cupons e cálculo do resultado esperado
        ├── api/                  testes que chamam a API diretamente
        └── ui/                   testes que usam a loja no navegador
```

## Como os cenários estão identificados

Cada cenário tem um ID no formato `CT-<área>-<número>`, usado igual nos arquivos `.feature`, na tabela de execução, nos bugs, nos nomes das evidências e nos nomes dos testes automatizados (`test_ct_cup_01_...`).

| Prefixo | Área |
|---|---|
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

### No GitHub Codespaces, sem instalar nada no computador

O repositório tem uma configuração de devcontainer em [`.devcontainer/`](.devcontainer/devcontainer.json). Ao criar um Codespace, as dependências e o Chromium são instalados automaticamente.

1. Na página do repositório, clique em **Code**, aba **Codespaces**, e depois em **Create codespace on** o branch desejado.
2. Espere a instalação terminar. O terminal mostra o progresso do `postCreateCommand` na primeira abertura.
3. No terminal:

```bash
cd automacao
pytest
```

O Codespace não tem tela, então os testes rodam sem abrir o navegador e a opção `--headed` não funciona. Para ver o que aconteceu em um teste de interface, gere o trace e abra o arquivo `trace.zip` em https://trace.playwright.dev:

```bash
pytest tests/ui --tracing on --output ../docs/evidencias/automacao
```

Os testes também aparecem na aba **Testing** do VS Code do Codespace, onde podem ser rodados um a um.

### Como ler o resultado

Os testes descrevem o comportamento **esperado pela documentação**. Os que cobrem um bug já reportado estão marcados com `xfail` e o ID do bug:

| Resultado | Significado |
|---|---|
| `passed` | A loja se comporta como a documentação descreve. |
| `xfailed` | Falha esperada: o teste confirma que um bug já reportado continua presente. O motivo aparece no resumo final. |
| `failed` | Comportamento diferente do esperado e ainda não reportado. Precisa ser investigado. |
| `XPASS(strict)`, contado como `failed` | Um teste marcado como bug passou: o bug foi corrigido e a marcação `xfail` deve ser removida. |

Com isso a suíte fica verde enquanto só existirem os bugs conhecidos, e qualquer falha nova chama atenção.

### Cuidados com o ambiente compartilhado

A loja é usada por outros candidatos ao mesmo tempo. A suíte roda em sequência, faz cerca de uma centena de requisições leves e não inclui teste de carga, estresse ou segurança.
