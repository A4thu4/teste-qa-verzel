# Pasta de evidências

Padrão de nome: `<ID>-<descrição-curta>.<extensão>`, por exemplo `CT-FRE-05-compra-pequena-frete-fixo.png`. Quando um cenário tem mais de uma captura, o número da etapa vem depois do ID: `CT-CUP-12_1-...` e `CT-CUP-12_2-...`.

- `feature_cupom/`, `feature_frete/`, `feature_qntd/`, `feature_calculo/`, `feature_checkout/`, `feature_api/`: capturas de tela da execução manual, uma pasta por funcionalidade
- `api/`: requisição e resposta das chamadas à API, gravadas por `automacao/coletar_evidencias_api.py`
- `exploratorio/`: relatórios das sessões exploratórias de API e de interface, com as capturas de interface em `exploratorio/interface/`
- `automacao/`: relatório da execução do Playwright
