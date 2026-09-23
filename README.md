# Caatinga.AI — Sprint 1

**Disciplina:** Inteligência Artificial, UniRios, 2026.2  
**Aluno:** [preencher nome completo], matrícula **241.14.007**  
**Matrícula-semente:** `24114007` (sem pontos).  
**Formato individual:** confirmar autorização com o professor, pois o enunciado pede dupla.

## O que faz

Gera um pomar de 12 × 12, compara BFS, DFS, UCS e três versões do A*.
Seleciona 15 talhões por busca local, explica decisões por regras e calcula
alertas falsos do sensor com Bayes.

## Como rodar

Python 3.10 ou superior. Na raiz do repositório:

```bash
python -m pip install -r requirements.txt
python src/main.py 24114007
```

O programa recria `resultados/pomar.txt`, `resultados/resultados.csv`,
`resultados/grafico.png` e `resultados/analise.json`. Para a arguição, substitua
o número no mesmo comando pela nova matrícula. O código usa apenas uma
dependência externa (`matplotlib`) para criar o gráfico.

## Resultados da matrícula 24114007

| Estratégia | Custo (unidades) | Passos | Nós expandidos | Fronteira máxima (itens) |
|---|---:|---:|---:|---:|
| BFS | 40 | 22 | 119 | 12 |
| DFS | 103 | 46 | 73 | 39 |
| UCS | 37 | 22 | 115 | 13 |
| A* h=0 | 37 | 22 | 115 | 13 |
| A* Manhattan | 37 | 22 | 94 | 16 |
| A* 4×Manhattan | 37 | 22 | 32 | 23 |

Ordem de expansão: **Norte, Sul, Oeste, Leste**. A* atualiza o menor custo
conhecido e reabre estados quando aparece um caminho mais barato; entradas
antigas da fila são descartadas. Nós expandidos são os itens válidos retirados
da fronteira, inclusive o objetivo. A fronteira máxima conta entradas físicas
na estrutura, inclusive entradas antigas ainda não descartadas.

## Arquivos

- [`src/gerador_pomar.py`](src/gerador_pomar.py): geração determinística da grade e do sensor.
- [`src/buscas.py`](src/buscas.py): buscas e contadores.
- [`src/busca_local.py`](src/busca_local.py): subida de encosta e têmpera simulada.
- [`src/especialista.py`](src/especialista.py): regras e explicação por encadeamento para trás.
- [`src/bayes.py`](src/bayes.py): probabilidades do sensor.
- [`src/main.py`](src/main.py): comando único que gera os resultados.
- [`RELATORIO.md`](RELATORIO.md): análises e questões do enunciado.
- [`ANEXO_IA.md`](ANEXO_IA.md): registro obrigatório do uso de IA.

## Limitações conhecidas

- A pontuação de risco da busca local é **didática**, construída a partir da
  grade; não há dados reais de infestação. O deslocamento ali é aproximação
  Manhattan, não uma rota válida entre os 15 talhões.
- A experiência de escala até falha acima de 60 segundos da Parte 2.4 ainda
  precisa ser medida e documentada.
- O código do gerador foi reconstruído a partir do texto extraído do enunciado;
  **compare-o com o arquivo original disponibilizado pelo professor** antes
  de entregar. O PDF acessado pela conversa exige autenticação no AVA.
- O repositório público, os commits dos alunos, o teste em outra máquina e
  o PDF do AVA precisam ser realizados no GitHub e no ambiente de entrega.
