# Auditoria local desta revisão

A pasta recebida não continha `.git`, `AGENTS.md`, PDF do enunciado ou cópia
independente do gerador. Foram lidos README, relatório, anexo, todos os seis
módulos Python originais; os artefatos principais foram recriados e conferidos. A revisão cobre os requisitos descritos
nesses documentos e no pedido atual; a conformidade integral depende do PDF.

## Evidências e correções

- O gerador foi preservado. SHA-256:
  `835fd5a3017e320c62ed0e83bb9ea1a88eb683436c523338c73cdd08c9b6306a`.
  Esse hash identifica o arquivo recebido, não comprova igualdade com o original.
- Antes das alterações, a referência 20231045 já produziu BFS=55/22 passos
  e UCS=34. Não foi necessário mudar a lógica dessas buscas para obter isso.
- As buscas agora rejeitam grades vazias, irregulares, símbolos desconhecidos
  e origem/destino bloqueados. Testes conferem movimentos, custo e objetivo.
- A busca local agora sorteia sobre listas ordenadas, trata a seleção do
  universo inteiro, valida parâmetros e salva as melhores seleções.
  A têmpera aceita também empates; mantém a melhor solução visitada.
- A pontuação usa percurso guloso Manhattan; não é deslocamento mínimo,
  rota viável entre obstáculos, probabilidade de praga nem restrição de bateria.
- R8 antes só existia dentro da demonstração; agora integra a base padrão.
  Provas positivas, falha de prova, ciclos e regras alternativas são testados.
  Falta de prova não significa prova de falsidade. R5 e R4 podem ser ambas
  demonstráveis: o exemplo consulta prioridade alta, não implementa arbitragem
  de todas as recomendações possíveis. Fatos contraditórios não são saneados.
- Bayes passou a exportar o VPP de duas leituras positivas condicionadamente
  independentes, permitindo verificar a auditoria do fornecedor.
- O anexo recebido atribuía um erro a uma conversa não disponível. Essa
  atribuição foi retirada e substituída por uma imprecisão observada no código.
- Os tempos antigos da escala não tinham artefato de comprovação; foram
  substituídos por uma nova medição local com ambiente e critério de parada.
- O gráfico foi recriado e inspecionado visualmente: seis barras, contagens,
  rótulos, unidades e semente legíveis. Cache fica ignorado pelo Git.

## Execução e limitações

Ambiente: macOS 12.7.6, x86_64, Intel Core i7-4870HQ @ 2,50 GHz,
8 CPUs lógicas, 16 GiB RAM, Python 3.13.3, matplotlib 3.11.2. CPU e memória
foram consultadas por `sysctl -n machdep.cpu.brand_string hw.memsize`.
O comando `python` não existia fora do ambiente virtual. Após ativar `.venv`,
as instruções do README usam `python` normalmente. A instalação inicial de
matplotlib falhou por rede bloqueada; a repetição autorizada concluiu.
Na construção do experimento, uma tentativa de limitar memória virtual via
`RLIMIT_AS` foi rejeitada pelo sistema; esse mecanismo foi removido antes da
medição final. Isso não foi contado como falha de algoritmo.
Durante a escrita de um teste Bayes, um literal esperado foi digitado com
precisão incorreta; o teste falhou e o literal foi corrigido pelo cálculo.

Não houve teste em outro computador, publicação remota, comparação com o
original do professor nem acesso ao AVA. Os commits são etapas desta revisão,
com a identidade Git preexistente; não representam contribuições anteriores,
trabalho de uma dupla ou histórico retroativo.

## Verificação final

- `python -m unittest discover -s tests -v`: oito testes (buscas, busca local,
  especialista, Bayes e integração); inclui dois ciclos de geração em pasta temporária.
- `python src/main.py 24114007`: quatro artefatos recriados e resultados conferidos.
- `python src/escala.py 24114007`: medição crescente com 60 s por busca;
  resultados individuais em `resultados/escala.json`.
- `python -m compileall -q src tests` e `python -m pip check`: sem falhas.
- Semente 0: UCS=33 e A* 4×Manhattan=37, contraexemplo real de otimalidade.
- SHA-256 do gerador conferido novamente ao final; sem alterações desde a entrada.
