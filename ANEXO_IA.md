# Anexo obrigatório — uso de IA

## A.1 Ferramentas usadas

ChatGPT/Codex ajudou a estruturar os arquivos, escrever a implementação
inicial das buscas, busca local, regras, cálculos de Bayes e texto preliminar
do relatório. O aluno deve revisar o código, executar e explicar os resultados.

## A.2 Dois prompts e respostas na íntegra

**Preencher com dois prompts reais copiados da conversa, incluindo as respostas
integrais.** Não resumir nem inventar. Sugestão: preservar o pedido de
explicação do enunciado e o pedido de construção simples deste projeto, com
as respostas completas correspondentes.

## A.3 Erro ou imprecisão verificada

No primeiro rascunho do relatório, o assistente afirmou que o VPP de dois
testes positivos independentes seria **95,22%**. Verifiquei com:

```bash
python -c 'p=.0483;s=.99;f=.05; print(p*s*s/(p*s*s+(1-p)*f*f))'
```

A saída foi `0.9521451753567314`, ou **95,2145%**, que arredondado a duas
casas decimais é **95,21%**. Corrigi o número no relatório. Esse cálculo
pressupõe independência condicional das leituras, hipótese que também não
foi demonstrada para o sensor real.

## A.4 Aprendizado após executar

Com minha semente 24114007, eu medi que a BFS deu custo 40 e 22 passos,
enquanto o UCS deu custo 37 e também 22 passos, mostrando que duas rotas
igualmente curtas podem ter preços diferentes.
