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
| OBS-01 | Cupom só com espaços é tratado de três formas. A tela trata como campo vazio e mostra "Informe um cupom."; o cálculo da API responde "Cupom inválido." com código vazio; o pedido é recusado com 422 `CUPOM_INVALIDO`. Já o cupom `""` é aceito pela API como "sem cupom". Pelo CA02 os espaços das pontas são ignorados, então `"   "` e `""` deveriam dar o mesmo resultado. | Interface e API · relatórios de [interface, tentativa 1](evidencias/exploratorio/sessoes-interface.md) e de [API, tentativas 1 e 6](evidencias/exploratorio/sessoes-api.md) | Aplicar a remoção de espaços antes de verificar se o cupom foi informado, tratando `"   "` como cupom vazio. |
| OBS-02 | `GET /api` devolve a página HTML da loja com status 200, em vez do 404 `ROTA_NAO_ENCONTRADA` em JSON que a documentação descreve para rota inexistente. | API · [relatório, tentativa 7](evidencias/exploratorio/sessoes-api.md) | Responder 404 em JSON para qualquer caminho sob `/api` que não seja uma rota, incluindo o próprio `/api`. |
| OBS-03 | A API aceita corpo enviado com `Content-Type` de formulário ou `text/plain`, embora a documentação diga para enviar sempre `application/json`. | API · [relatório, tentativas 10 e 11](evidencias/exploratorio/sessoes-api.md) | Recusar com 415 o que não for JSON, ou registrar na documentação que o cabeçalho é opcional. |
| OBS-04 | A regra do nome não bate com a mensagem. `A B` e `Maria S` são recusados com "Informe nome e sobrenome.", embora tenham nome e sobrenome; já `123 456`, que não é um nome, é aceito e a confirmação mostra "Obrigado, 123.". A loja parece exigir duas palavras com pelo menos duas letras cada, sem olhar se são letras. | Checkout e API · [relatório de interface, tentativas 7 a 9](evidencias/exploratorio/sessoes-interface.md) | Definir a regra na documentação e alinhar a mensagem a ela, por exemplo "Cada parte do nome precisa ter ao menos 2 letras". Avaliar recusar números. |
| OBS-05 | A validação de e-mail aceita formatos inválidos: dois pontos seguidos no domínio (`maria@exemplo..com`), ponto no fim (`maria@exemplo.com.`) e domínio de uma letra (`maria@exemplo.c`). | Checkout e API · [relatório de interface, tentativas 11 a 13](evidencias/exploratorio/sessoes-interface.md) | Recusar pontos seguidos ou no fim do domínio e exigir ao menos 2 letras no domínio de topo. |
