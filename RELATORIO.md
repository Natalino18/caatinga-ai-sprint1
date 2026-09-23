# Relatório — Caatinga.AI (semente 24114007)

**Aluno:** [natalino varela correia]. **Disciplina:** Inteligência Artificial, 2026.2.
Todos os números abaixo são resultados da execução de `python src/main.py 24114007`.

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

**Tipo:** agente baseado em utilidade: compara custo de rota e valor esperado
de inspeções; usa modelo do mapa para antecipar consequências. Maximizar só
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
dessas 119 posições; um nó na fronteira também guarda o caminho/custo.

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

**2.4 — Escala parcial:** na mesma máquina, `n=40` levou 1,77 ms (BFS),
0,76 ms (DFS) e 2,16 ms (UCS); `n=100` levou 12,12 ms, 6,71 ms e 13,78 ms.
Os respectivos estados expandidos em `n=100` foram 8018, 4459 e 8017.
**Pendente:** aumentar `n` até uma falha real ou 60 s, registrar ambiente e
relacionar com as fórmulas de tempo/espaço da Aula 03. Ainda não ocorreu
falha. O gerador aceita `n`, embora o comando principal use 12.

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
`h(n) ≤ h*(n)` para **todo estado**; o exemplo a refuta. A heurística 4
expandiu 32 nós, **83 a menos** que o UCS. A cooperativa poderia usá-la se
medisse em operação que a resposta garantida excede seu prazo de, por
exemplo, **200 ms por consulta**, e aceitasse previamente um limite de custo
extra verificável. Esse limite ainda teria de ser validado em muitas grades.

**Busca local.** Estado: conjunto de 15 talhões livres. Vizinhança: trocar um
talhão escolhido por outro livre. Objetivo didático: soma de escores de risco
(`2 + 3` se molhado `+` número de vizinhos molhados) menos `0,3` vezes
aproximação do deslocamento Manhattan entre escolhidos. Não é evidência de
infestação real nem modelo completo da bateria de 6 horas.

| Método | Média (pontos) | Desvio amostral | Melhor | Rodadas |
|---|---:|---:|---:|---:|
| Subida de encosta | 98,847 | 2,308 | 102,5 | 30 |
| Têmpera simulada | 86,243 | 4,971 | 100,1 | 30 |

Os 30 valores e contagens de pioras aceitas estão em `resultados/analise.json`.
Na execução 1, a têmpera aceitou **85 pioras** e alcançou 83,4 pontos; a
encosta aceitou 0 e alcançou 100,8. Aceitar pioras permite escapar de ótimos
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
humano** deve ser regra explícita e auditável, pois afeta responsabilidades
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

**Pendente para entrega:** aferição de escala 2.4, avaliação do bônus opcional,
nome completo, validação do gerador original e autorização de trabalho individual.
