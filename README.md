# Caatinga.AI — Sprint 1

**Disciplina:** Inteligência Artificial, UniRios, 2026.2

**Aluno:** Natalino Varela Correia, matrícula **241.14.007**

**Matrícula-semente:** `24114007` (sem pontos).

**Formato individual:** confirmar autorização com o professor, pois o enunciado pede dupla.

## O que faz

Gera um pomar de 12 × 12, compara BFS, DFS, UCS e três versões do A*.
Seleciona 15 talhões por busca local, explica decisões por regras e calcula
alertas falsos do sensor com Bayes.

## Como rodar

Python 3.10 ou superior. Na raiz do repositório:

```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux; Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
python src/main.py 24114007
```

O programa recria `resultados/pomar.txt`, `resultados/resultados.csv`,
`resultados/grafico.png` e `resultados/analise.json`. Para a arguição, substitua
o número no mesmo comando pela nova matrícula. O código usa apenas uma
dependência direta (`matplotlib`) para criar o gráfico; suas dependências são
instaladas pelo pip. `requirements.txt` mantém a faixa 3.7–3.x, compatível com
Python 3.10+. Ambiente efetivamente testado: Python 3.13.3 e matplotlib 3.11.2
em macOS 12.7.6. Versões futuras dentro da faixa não foram testadas.

```bash
python -m unittest discover -s tests -v
python -m pip check
python src/main.py 24114007 --escala
```

O primeiro comando executa oito testes. O último recria os quatro arquivos
principais e `resultados/escala.json`; pode levar vários minutos e consumir
bastante memória. A escala foi validada em macOS (usa seleção de pipes Unix).
Para repetir apenas a escala: `python src/escala.py 24114007`.
O comando sem `--escala` recria os quatro artefatos principais rapidamente;
não altera a medição de escala previamente salva. Tempos variam por execução.
Rotas e contagens são determinísticas no ambiente registrado. Os resultados
são gravados na pasta do projeto, mesmo se o comando partir de outro diretório.

A referência 20231045 foi executada primeiro: **UCS 34; BFS 55 e 22 passos**.
Com 24114007, busca local em 30 rodadas: encosta **99,137 ± 2,246** pontos
(melhor 103,7); têmpera **88,043 ± 4,180** (melhor 96,2). Desvio amostral.
VPP do sensor: **50,1216%**; inspeções falsas: **11,4204 h/semana**.

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
- A escala local, com limite de 60 s por busca, está documentada na Parte 2.4
  do relatório e em `resultados/escala.json`: timeout em n=8000 (BFS/DFS) e
  n=4000 (UCS), primeiros tamanhos testados que excederam o limite.
  Não é teste em outro computador.
- O README recebido dizia que o gerador foi reconstruído do texto do enunciado;
  essa origem não pôde ser verificada nesta revisão.
  **compare-o com o arquivo original disponibilizado pelo professor** antes
  de entregar. O PDF do enunciado não está nesta pasta; sua obtenção no AVA depende do aluno.
- Os commits locais registram esta revisão usando somente a identidade Git
  configurada. Publicação no GitHub, teste em outra máquina, autorização para
  entrega individual, dois pares completos de prompts/respostas reais e o PDF
  para entrega no AVA dependem do aluno. Confira o enunciado original.
- Veja [AUDITORIA.md](AUDITORIA.md) para evidências e limitações da revisão.

## Para explicar na arguição

1. Estado é uma posição; vizinhos seguem N/S/O/L. BFS usa fila, DFS pilha,
   UCS fila de prioridade por custo, A* prioridade por custo mais heurística.
2. O dicionário de pais reconstrói a rota. A origem não é cobrada; entrar em
   `.` custa 1 e em `~` custa 4. Visitados evitam ciclos.
3. Manhattan é limite inferior; 4×Manhattan pode superestimar. Igualdade de
   custo em uma semente não demonstra garantia universal.
4. Busca local troca um dos 15 talhões. A encosta só aceita melhora;
   têmpera também aceita pioras, mas guarda o melhor conjunto encontrado.
5. O especialista prova premissas recursivamente e mostra regras usadas.
   Bayes distingue sensibilidade de probabilidade de praga após um alerta.
