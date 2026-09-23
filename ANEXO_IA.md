# Anexo obrigatório — uso de IA

## A.1 Ferramentas usadas

Nesta revisão, Codex leu os arquivos disponíveis, corrigiu código, criou e
executou testes, mediu a escala local, atualizou a documentação e criou
commits locais usando a identidade Git previamente configurada. A solicitação
foi de Natalino Varela Correia, matrícula 241.14.007, trabalho individual.
O histórico de conversas anteriores não está disponível nesta pasta; não é
possível atestar quais ferramentas produziram cada trecho do material inicial.
O aluno ainda deve revisar e conseguir explicar todo o trabalho.

## A.2 Dois prompts e respostas na íntegra — pendente do aluno

Copiar da conversa **dois pares reais completos**, preservando cada prompt e
sua resposta integral. O pedido desta revisão e a resposta final podem ser
um dos pares, se aceitos pelo professor. Não foram fabricadas transcrições,
respostas anteriores nem um segundo integrante. Este anexo não está completo
para entrega enquanto os dois pares reais não forem inseridos pelo aluno.

## A.3 Imprecisão comprovada nesta revisão

O comentário recebido em `src/busca_local.py` dizia “deslocamento mínimo
aproximado”. O código escolhe repetidamente o ponto mais próximo em distância
Manhattan, um percurso guloso que não garante deslocamento mínimo e ignora
obstáculos. O comentário foi corrigido para “deslocamento por vizinho mais
próximo”. A revisão também passou a salvar as seleções, permitindo recalcular
a pontuação de cada rodada.

O anexo anterior atribuía à IA um arredondamento errado em uma conversa
anterior. Sem essa conversa, a atribuição não é comprovável e foi retirada.
A conta de dois positivos foi implementada e testada: 0,9521451753567314,
ou 95,21%, somente sob independência condicional das leituras.

## A.4 Evidência para o aprendizado

A execução local desta revisão com 24114007 produziu BFS de custo 40 e
22 passos; UCS de custo 37 e 22 passos. Duas rotas de mesmo comprimento
podem ter custos distintos. A têmpera aceitou pioras, mas sua média foi
inferior à encosta nesta configuração. Isso não prova inferioridade universal.
Essas são observações da execução assistida, não uma declaração de teste
manual já realizado pelo aluno em outro computador.
