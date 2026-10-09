# Bugs encontrados

| ID | Título | Severidade | Critério | Onde |
| --- | --- | --- | --- | --- |
| [BUG-001](#bug-001) | Subtotal de exatamente R$ 200,00 não recebe frete grátis | Alta | CA06 | API e interface |
| [BUG-002](#bug-002) | API aceita mais de 5 unidades do mesmo produto | Alta | CA10 | API |

O critério usado para a severidade está em [01-plano-de-teste.md](01-plano-de-teste.md#critério-para-classificar-os-bugs).

---

## BUG-001

**Subtotal de exatamente R$ 200,00 não recebe frete grátis**

| | |
| --- | --- |
| Severidade | Alta |
| Critério descumprido | CA06: "O frete é grátis para compras com subtotal a partir de R$ 200,00, inclusive." |
| Onde ocorre | `POST /api/carrinho/calcular`, `POST /api/pedidos` e, por consequência, carrinho, checkout e confirmação na interface |
| Cenários que falham | CT-FRE-01, CT-FRE-02, CT-FRE-08, CT-APC-06 (exemplos de R$ 200,00), CT-APP-05 |
| Ambiente | Versão 2.3.0 · _navegador e sistema_ · _data da execução_ |

### Passos para reproduzir na interface

1. Abrir a loja com o carrinho vazio.
2. Clicar duas vezes em "Adicionar ao carrinho" no produto "Mochila Urbana 20L" (R$ 100,00).
3. Abrir o carrinho.

### Passos para reproduzir na API

```bash
POST /api/carrinho/calcular
Content-Type: application/json

{ "itens": [ { "produtoId": "P005", "quantidade": 2 } ] }
```

### Resultado esperado

Subtotal R$ 200,00, frete grátis, total R$ 200,00, sem aviso de valor faltante.

```json
{ "subtotal": 200, "frete": 0, "freteGratis": true, "valorFaltanteFreteGratis": 0, "total": 200 }
```

### Resultado obtido

O frete de R$ 19,90 é cobrado e o total fica em R$ 219,90. O carrinho ainda exibe o aviso "Faltam R$ 0,00 para o frete grátis.", que contradiz a cobrança.

```json
{ "subtotal": 200, "frete": 19.9, "freteGratis": false, "valorFaltanteFreteGratis": 0, "total": 219.9 }
```

### Análise

O problema está só no valor exato do limite. Com R$ 199,70 o frete é cobrado e com R$ 219,80 é grátis, ambos corretos. O mesmo acontece montando R$ 200,00 com 4 unidades da "Garrafa Térmica 750ml", o que descarta relação com um produto específico. O próprio campo `valorFaltanteFreteGratis` volta 0, ou seja, a API reconhece que não falta nada e mesmo assim cobra. O comportamento é compatível com uma comparação "maior que" onde a regra pede "maior ou igual".

### Impacto

O cliente que monta um carrinho de exatamente R$ 200,00 paga R$ 19,90 que a promoção anunciada na página inicial ("Frete grátis a partir de R$ 200,00") diz que ele não pagaria. Com o cupom BEMVINDO10 o efeito se repete: o total fica em R$ 199,90 em vez de R$ 180,00.

### Evidências

- Interface: `evidencias/BUG-001-carrinho-200.png`
- API: `evidencias/api/BUG-001-calcular-200.md`

---

## BUG-002

**API aceita mais de 5 unidades do mesmo produto**

| | |
| --- | --- |
| Severidade | Alta |
| Critério descumprido | CA10: "Cada produto pode ter no máximo 5 unidades por pedido. A regra vale para a interface e para a API." |
| Onde ocorre | `POST /api/carrinho/calcular` e `POST /api/pedidos` |
| Cenários que falham | CT-QTD-07, CT-QTD-08 |
| Ambiente | Versão 2.3.0 · _data da execução_ |

### Passos para reproduzir

```bash
POST /api/pedidos
Content-Type: application/json

{
  "cliente": { "nome": "Maria Silva", "email": "maria@exemplo.com", "cep": "01310-100" },
  "itens": [ { "produtoId": "P001", "quantidade": 6 } ]
}
```

### Resultado esperado

Status 422 com o erro documentado na tabela de códigos:

```json
{ "erro": { "codigo": "QUANTIDADE_MAXIMA_EXCEDIDA", "mensagem": "...", "campo": "itens[0].quantidade" } }
```

### Resultado obtido

Status 201. O pedido é confirmado com 6 unidades e subtotal de R$ 359,40. O mesmo vale para `POST /api/carrinho/calcular`, que responde 200.

### Análise

A interface respeita o limite: na quinta unidade a vitrine desabilita o botão e mostra "Limite de 5 unidades atingido.", e o carrinho desabilita o botão de aumentar. A validação existe só na tela. Não parece haver nenhum teto na API: uma quantidade de 1.000.000 também é aceita no cálculo. O código `QUANTIDADE_MAXIMA_EXCEDIDA` está na documentação, mas não foi possível obtê-lo em nenhuma chamada.

### Impacto

Qualquer cliente que chame a API diretamente, sem passar pela tela, fecha um pedido acima do limite. A regra de negócio fica dependendo de uma validação que o usuário consegue contornar.

### Evidências

- API: `evidencias/api/BUG-002-pedido-6-unidades.md`
- Interface respeitando o limite, para comparação: `evidencias/CT-QTD-01-limite-vitrine.png`
