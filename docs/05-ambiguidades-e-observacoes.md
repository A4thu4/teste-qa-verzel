# Ambiguidades e observações

## Ambiguidades da documentação

Pontos em que a documentação permite mais de uma leitura. Para cada um está registrada a interpretação adotada nos testes.

| ID | Trecho | Dúvida | Interpretação adotada |
| --- | --- | --- | --- |
| AMB-01 | CA11: "Todos os valores são arredondados para 2 casas decimais." | O critério não diz a regra de arredondamento (metade para cima, para baixo ou para o par). | Arredondamento comercial, metade para cima. **O critério não pôde ser exercitado de verdade:** todos os preços são múltiplos de R$ 0,10 e o único cupom válido é de 10%, então o desconto sempre cai exato em centavos. Nenhum cenário possível gera a terceira casa decimal. Os testes confirmam que os valores saem com no máximo 2 casas e sem resíduo de ponto flutuante, mas a regra de arredondamento em si só seria testável com um cupom de 15% válido ou um preço com centavos quebrados. |
| AMB-02 | CA10: "no máximo 5 unidades por pedido." | O limite é por produto ou pelo total de itens do pedido? | Por produto, como diz o início da frase ("Cada produto pode ter"). Um pedido com 5 mochilas e 5 garrafas é válido. |
| AMB-03 | CA03: cupom inexistente exibe "Cupom inválido." | O que acontece ao aplicar com o campo vazio ou só com espaços? | Não é um cupom inexistente, é ausência de cupom. Espera-se uma mensagem orientando o preenchimento e nenhum desconto. O texto exato não é cobrado. |
| AMB-04 | CA02: "espaços no início e no fim são ignorados." | E espaços no meio do código? | Não são ignorados. "BEM VINDO10" é um cupom inexistente. |
| AMB-05 | CA05: "Apenas um cupom pode ser aplicado por vez." | A API precisa recusar dois cupons? | Não se aplica: o corpo da requisição tem um único campo `cupom`. O critério foi verificado só na interface. |
| AMB-06 | "O nome do cliente precisa ter nome e sobrenome." | Qual o tamanho mínimo de cada parte? Números e símbolos são aceitos? | Duas ou mais palavras separadas por espaço. A documentação não define tamanho mínimo nem caracteres permitidos, então esses casos estão registrados como observação, não como bug. |
| AMB-07 | "O e-mail precisa ter um formato válido." | Qual o nível de rigor? | Formato `usuario@dominio.tld`, sem espaços e com uma única arroba. Casos de borda como dois pontos seguidos no domínio estão como observação. |
| AMB-08 | CA07: o carrinho "informa quanto falta para o frete grátis." | O aviso aparece quando o frete já é grátis? | Não. Com frete grátis não há valor faltante a informar e o aviso some. |
| AMB-09 | CA06 e CA08 combinados. | Subtotal de R$ 200,00 com cupom: o frete é calculado sobre R$ 200,00 ou sobre R$ 180,00? | Sobre R$ 200,00, pelo CA08. O frete é grátis e o total é R$ 180,00. |
| AMB-10 | Códigos de erro: "Todo erro segue o mesmo formato", com `codigo`, `mensagem` e `campo`. | Erros que não se referem a um campo (404, 405, 400) também trazem `campo`? E o `DADOS_INVALIDOS`, que usa `campos`? | `campo` só aparece quando o erro aponta para um campo da requisição. `DADOS_INVALIDOS` usa a lista `campos`, como a própria tabela descreve. |

## Observações

Comportamentos notados durante a execução que não descumprem um critério de aceite, mas que valem uma conversa com o time. Não foram abertos como bug.

| ID | Observação | Onde | Sugestão |
| --- | --- | --- | --- |
| OBS-01 | _preencher com o que for confirmado nas sessões exploratórias_ | | |
