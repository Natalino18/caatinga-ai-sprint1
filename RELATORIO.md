# Relatório — Caatinga.AI (semente 24114007)

**Integrantes:** Natalino Varela Correia — matrícula 241.14.007 (integrante mais velho); nome completo do integrante da matrícula 241.14.002 ainda precisa ser informado. **Disciplina:** Inteligência Artificial, 2026.2.
Os resultados principais vêm de `python src/main.py 24114007`; a escala
vem de `python src/escala.py 24114007`. Valores hipotéticos são identificados.
O enunciado original e a Aula 03 não estão disponíveis nesta pasta; as
interpretações do texto recebido ainda precisam ser confrontadas com o AVA.

## Parte 1 — Agente

**PEAS.** Desempenho: custo total de entrada nos talhões (unidades de custo),
tempo até o ponto de coleta (minutos, caso seja medido), alertas corretos por
100 inspeções e horas semanais gastas em alertas falsos. Ambiente: pomar de
12 × 12, talhões `.`, `~`, `#`, portão e ponto de coleta. Atuadores: mover
N/S/O/L e emitir recomendação de inspeção. Sensores: posição, grade e sensor
óptico de pragas.

**Dimensões.** A grade é discreta (12 × 12 e quatro movimentos); o planejador
atua como agente único (o enunciado só descreve um agente); o deslocamento na
grade é determinístico (entrar num talhão tem custo fixo); a rota é sequencial
(cada passo altera posição e custo acumulado). É **discutível** chamar o
ambiente de totalmente observável: o enunciado dá a grade ao programa, mas
não diz se o robô conhece o pomar inteiro antes de partir. Também é
**discutível** chamá-lo estático: o arquivo gerado não muda durante a busca,
mas o enunciado não diz se alagamento e pragas mudam durante as seis horas.
Seriam necessários, respectivamente, especificação da percepção inicial e
frequência de atualização do pomar. A busca de rota assume grade totalmente
conhecida e fixa. A detecção de pragas é incerta por causa de sensibilidade e
falsos positivos.

**Tipo proposto:** agente baseado em utilidade: compara custo de rota e valor esperado
de inspeções; usa modelo do mapa para antecipar consequências. O programa implementa os
componentes didáticos separadamente; não controla um robô integrado. Maximizar só
o número de alertas seria uma **métrica perversa**: perto dos talhões `~`, o
agente poderia elevar a frequência de alertas sem confirmação para aparentar
mais descobertas. Corrigir medindo pragas confirmadas por hora de trabalho,
com penalidade para alertas falsos e validação humana.

## Parte 2 — Busca cega

Estado = coordenada `(linha, coluna)`; inicial `(0,0)`; ações N/S/O/L dentro
da grade e fora dos bloqueios; transição = coordenada vizinha; objetivo
`(11,11)`; custo = 1 para entrar em `.` e 4 para entrar em `~`, sem cobrar a
origem. A grade tem 144 coordenadas e **119 estados transitáveis** nesta
semente. O espaço de estados das buscas de rota implementadas é o conjunto
dessas 119 posições; a fronteira guarda posições (e custos nas buscas ponderadas); um mapa de
pais permite reconstruir a rota, sem copiar caminhos a cada expansão.

| Estratégia | Custo | Passos | Expandidos | Fronteira máx. | Ótima em custo? |
|---|---:|---:|---:|---:|---|
| BFS | 40 | 22 | 119 | 12 | Não |
| DFS | 103 | 46 | 73 | 39 | Não |
| UCS | 37 | 22 | 115 | 13 | Sim |

Unidades: custo em unidades de entrada; passos e nós em contagens; fronteira
em itens. BFS minimiza passos quando todos têm profundidade unitária; isso
não implica menor custo quando entradas custam **1 ou 4**. Neste pomar, seus
22 passos custaram 40, contra 37 do UCS. A hipótese violada é **custo igual
para todos os passos**.

**2.4 — Escala medida nesta revisão.** Semente 24114007, uma execução por
tamanho e método, em subprocessos independentes. Ambiente: macOS 12.7.6,
Intel Core i7-4870HQ @ 2,50 GHz, 8 CPUs lógicas, 16 GiB RAM, Python 3.13.3.
A geração tem limite separado de 60 s; os tempos abaixo são da busca,
incluindo validação da grade e reconstrução da rota. Execuções interrompidas
não têm tempo de conclusão, custo ou contadores finais estimados.

| Método | n | Tempo de busca (s) | Expandidos | Fronteira máxima |
|---|---:|---:|---:|---:|
| BFS | 100 | 0.027 | 8018 | 102 |
| BFS | 400 | 0.363 | 127659 | 383 |
| BFS | 1000 | 2.431 | 798875 | 926 |
| BFS | 2000 | 10.818 | 3193075 | 1805 |
| BFS | 4000 | 50.643 | 12775400 | 3569 |
| BFS | 8000 | timeout após 60 s | não disponível | não disponível |
| DFS | 100 | 0.013 | 4459 | 2317 |
| DFS | 400 | 0.182 | 62252 | 32530 |
| DFS | 1000 | 1.277 | 397775 | 211871 |
| DFS | 2000 | 5.427 | 1570365 | 847603 |
| DFS | 4000 | 22.758 | 6252651 | 3416226 |
| DFS | 8000 | timeout após 60 s | não disponível | não disponível |
| UCS | 100 | 0.028 | 8017 | 154 |
| UCS | 400 | 0.551 | 127658 | 614 |
| UCS | 1000 | 4.330 | 798874 | 1485 |
| UCS | 2000 | 20.461 | 3193063 | 2981 |
| UCS | 4000 | timeout após 60 s | não disponível | não disponível |

BFS e DFS concluíram até n=4000; UCS até n=2000. O primeiro tamanho
testado com timeout foi n=8000 para BFS/DFS e n=4000 para UCS. Não se
afirma que esses sejam os menores tamanhos que ultrapassam 60 s. Não houve
falha de memória registrada nesta execução. Valores brutos e data UTC estão
em `resultados/escala.json`. O limite de 60 s é critério operacional; uma
execução pode terminar com tempo diferente em outra ocasião. Não são médias,
não houve isolamento da carga do computador e pequenas verificações do
projeto ocorreram durante o experimento.

**Relação com complexidade.** Em busca em árvore, usando fator de ramificação
`b`, profundidade da solução `d` e profundidade máxima `m`, BFS usa tempo e
espaço O(b^(d+1)); DFS usa tempo O(b^m) e espaço O(bm). Para UCS com custo
ótimo C* e menor custo de passo ε>0, o limite clássico é
O(b^(1+⌊C*/ε⌋)) para tempo/espaço. Aqui b≤4 e ε=1. A notação exata adotada
na Aula 03 ainda precisa ser conferida no material original.

Nesta implementação em **grafo**, o conjunto de descobertos evita repetição
de posições. Com V≤n² e E≤4V, BFS/DFS têm tempo O(V+E) e espaço O(V); UCS
com heap tem tempo O((V+E) log V) e espaço O(V+E), que aqui é O(V). A grade
também ocupa O(n²). Portanto, não se deve aplicar diretamente a economia
de memória da DFS em árvore a esta versão com visitados globais: por exemplo,
em n=4000 sua fronteira chegou a 3.416.226 itens contra 3.569 da BFS.
Fronteira não mede memória total em bytes; pais, visitados, custos e a grade
também consomem memória. Dobrar n quadruplica as posições, coerente com o
crescimento observado; UCS acrescenta o trabalho de prioridade do heap.

## Parte 3 — Busca informada e local

| Heurística | Custo | Nós expandidos | Admissível? |
|---|---:|---:|---|
| 0 | 37 | 115 | Sim: 0 ≤ custo restante |
| Manhattan | 37 | 94 | Sim: cada passo necessário custa ao menos 1 |
| 4×Manhattan | 37 | 32 | Não: pode superar custo restante |

Qualquer caminho precisa de pelo menos `|11-i|+|11-j|` passos; cada entrada
custa pelo menos 1. Logo Manhattan nunca supera o custo restante. Exemplo
concreto contra 4×Manhattan: do talhão `(11,10)` ao objetivo `(11,11)`, que
é `.`, o custo real restante é **1** e a heurística dá **4**. Ter encontrado
37 como o UCS **não prova** admissibilidade: admissibilidade exige que
`h(n) ≤ h*(n)` para **todo estado**; o exemplo a refuta. Uma execução adicional com semente 0 produziu UCS=33
e A* 4×Manhattan=37, um contraexemplo concreto de otimalidade. Na semente
24114007, a heurística 4 expandiu 32 nós, **83 a menos** que o UCS. A cooperativa poderia usá-la se
medisse em operação que a resposta garantida excede seu prazo de, por
exemplo, **200 ms por consulta**, e aceitasse previamente um limite de custo
extra verificável. Esse limite ainda teria de ser validado em muitas grades.

**Busca local.** Estado: conjunto de 15 talhões livres. Vizinhança: trocar um
talhão escolhido por outro livre. Objetivo didático: soma de escores de risco
(`2 + 3×indicador_de_molhado + número_de_vizinhos_molhados`) menos `0,3` vezes
aproximação do deslocamento Manhattan entre escolhidos. O percurso parte de (0,0), visita os escolhidos por proximidade e não inclui
retorno ao portão ou deslocamento final à coleta. Não é evidência de
infestação real nem modelo completo da bateria de 6 horas.

| Método | Média (pontos) | Desvio amostral | Melhor | Rodadas |
|---|---:|---:|---:|---:|
| Subida de encosta | 99,137 | 2,246 | 103,7 | 30 |
| Têmpera simulada | 88,043 | 4,180 | 96,2 | 30 |

Foram 300 propostas por rodada, semente `24114007 + índice` (índice 0–29).
A encosta amostra um vizinho e aceita melhora estrita; não examina toda a
vizinhança e não garante alcançar um ótimo local. A têmpera usa
`T=max(0,05; 8×(1−t/300))`, aceita empates e pioras com probabilidade
`exp(delta/T)`. Ambos devolvem a melhor seleção visitada, não a última.
Os 30 valores, seleções e contagens de pioras aceitas estão em `resultados/analise.json`.
Na execução 1, a têmpera aceitou **82 pioras** e alcançou 95,5 pontos; a
encosta aceitou 0 e alcançou 100,3. Aceitar pioras permite escapar de ótimos
locais, mas **nesta configuração não trouxe ganho de desempenho**. A
temperatura e o número de passos precisariam de ajuste, sem apagar esse
resultado desfavorável.

## Parte 4 — Regras e incerteza

Parâmetros: prevalência **0,0483**, sensibilidade **0,99**, falso positivo
**0,05**, **1200 talhões/semana**. As sete regras `R1` a `R7` estão em
`src/especialista.py` e o programa imprime a cadeia R1→R2→R3→R4 para
`inspecionar_prioridade_alta` com os fatos observados. Caso que quebra a
base: sensor negativo **com sintomas visuais**. Antes não se prova prioridade
alta; a regra corretiva `R8`, **SE sintomas_visuais ENTÃO
inspecionar_prioridade_alta**, prova a conclusão pelo fato observado e R8.
R6 requer também `sem_sintomas_visuais`, evitando conclusão conflitante.

P(infestado | positivo) = `0,99×0,0483 / (0,99×0,0483 + 0,05×0,9517)`
= **0,501216**. A cada 100 alertas, aproximadamente **49,88 são falsos**.
Falsos por semana = `1200×0,9517×0,05` = **57,102**; em média,
`57,102×12/60` = **11,4204 horas/semana** de inspeções falsas. Com
sensibilidade 0,999 e mesmo falso positivo,
VPP = `0,999×0,0483/(0,999×0,0483+0,05×0,9517)` = **0,503478**.
Melhora pouco; reduzir a taxa de falsos positivos tem maior efeito no VPP
e no número de visitas inúteis. A decisão de **não pulverizar sem laudo
humano** está representada pela regra explícita R7, pois afeta responsabilidades
e permite explicar quem autorizou o manejo.

## Parte 5 — Auditoria do fornecedor

1. **Incorreta:** A* só garante otimalidade sob condições da heurística;
   `(11,10)` demonstra `h3=4 > 1`. O custo 37 igual ao UCS nesta grade
   não é prova universal.
2. **Parcialmente correta:** trocar BFS pelo A* Manhattan reduziu de 40 para
   37 nesta semente (**7,5%**, não os alegados 38%). A diferença decorre
   de otimizar custo em vez de passos; UCS sem heurística também obteve 37.
3. **Incorreta:** sensibilidade 99% e VPP **50,12%** são probabilidades
   condicionais diferentes.
4. **Incorreta como garantia:** duas leituras independentes condicionadas ao
   estado teriam VPP `p·s²/[p·s²+(1-p)·f²]` ≈ **95,21%** aqui, não acima
   de 99%. Leituras repetidas podem ser correlacionadas, tornando a conta
   de independência inaplicável.
5. **Parcialmente correta:** DFS costuma usar menos memória em busca em
   árvore profunda, mas nesta implementação com visitados mediu fronteira
   máxima **39**, contra **13** no UCS, e custo **103** contra **37**.
   Ser estático/observável não a torna suficiente para minimizar custo.

**Recomendação:** recusar o laudo como justificativa de compra. Reconsiderar
se o fornecedor publicar testes reproduzíveis em grades com custos 1 e 4,
comprovar limites de custo da rota e medir o VPP e as horas de inspeção falsa
em dados reais. Nesta semente, a recomendação de rota da DFS custa 103 contra
37 do UCS e o VPP do sensor é aproximadamente 50,12%.

**Pendente para entrega:** informar o nome completo do integrante da matrícula
241.14.002, obter e conferir o PDF do enunciado (inclusive bônus e fórmulas da
Aula 03), comparar o gerador com o original do professor, publicar no GitHub,
testar em outro computador, completar os dois pares integrais de
prompts/respostas reais e gerar/conferir o PDF final exigido no AVA. O commit
feito nesta revisão usa apenas a identidade de Natalino Varela Correia; o
segundo integrante ainda precisa realizar uma alteração real e criar seu
próprio commit com sua conta e configuração Git. Não se deve criar um commit
fingindo ser essa pessoa.
