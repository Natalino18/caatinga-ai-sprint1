"""Buscas em grafo. Ordem de vizinhos: Norte, Sul, Oeste, Leste."""
from collections import deque
from dataclasses import dataclass
from heapq import heappop, heappush
from itertools import count
from time import perf_counter
from gerador_pomar import CUSTO

ORDEM = ((-1, 0), (1, 0), (0, -1), (0, 1))

@dataclass
class Resultado:
    estrategia: str
    heuristica: str
    rota: list
    custo: int
    passos: int
    nos_expandidos: int
    fronteira_max: int
    tempo_ms: float

def validar_grade(grade):
    if not grade or not grade[0] or any(len(l) != len(grade[0]) for l in grade):
        raise ValueError("A grade deve ser retangular e não vazia")
    if any(c not in {".", "~", "#"} for linha in grade for c in linha):
        raise ValueError("Símbolo desconhecido na grade")
    if grade[0][0] not in CUSTO or grade[-1][-1] not in CUSTO:
        raise ValueError("Origem e destino devem ser transitáveis")

def vizinhos(grade, atual):
    i, j = atual
    for di, dj in ORDEM:
        a, b = i + di, j + dj
        if 0 <= a < len(grade) and 0 <= b < len(grade[a]) and grade[a][b] in CUSTO:
            yield (a, b)

def reconstruir(pais, fim):
    rota = [fim]
    while pais[rota[-1]] is not None:
        rota.append(pais[rota[-1]])
    return rota[::-1]

def resultado(nome, heuristica, grade, pais, fim, expandidos, maior, inicio):
    rota = reconstruir(pais, fim)
    return Resultado(nome, heuristica, rota,
                     sum(CUSTO[grade[i][j]] for i, j in rota[1:]),
                     len(rota) - 1, expandidos, maior, (perf_counter() - inicio) * 1000)

def busca_cega(grade, metodo):
    if metodo not in ("BFS", "DFS"):
        raise ValueError("Método deve ser BFS ou DFS")
    inicio = perf_counter()
    validar_grade(grade)
    raiz, alvo = (0, 0), (len(grade) - 1, len(grade[0]) - 1)
    fronteira = deque([raiz]) if metodo == "BFS" else [raiz]
    pais = {raiz: None}
    expandidos, maior = 0, 1
    while fronteira:
        atual = fronteira.popleft() if metodo == "BFS" else fronteira.pop()
        expandidos += 1
        if atual == alvo:
            return resultado(metodo, "", grade, pais, alvo, expandidos, maior, inicio)
        adj = list(vizinhos(grade, atual))
        if metodo == "DFS":
            adj.reverse()  # pilha: inverter para expandir Norte, Sul, Oeste, Leste
        for proximo in adj:
            if proximo not in pais:
                pais[proximo] = atual
                fronteira.append(proximo)
        maior = max(maior, len(fronteira))
    raise ValueError("Objetivo inacessível")

def bfs(grade):
    return busca_cega(grade, "BFS")

def dfs(grade):
    return busca_cega(grade, "DFS")

def heuristica(pos, alvo, fator):
    return fator * (abs(pos[0] - alvo[0]) + abs(pos[1] - alvo[1]))

def busca_custo(grade, nome="UCS", fator=0):
    inicio = perf_counter()
    validar_grade(grade)
    raiz, alvo = (0, 0), (len(grade) - 1, len(grade[0]) - 1)
    sequencia = count()
    fronteira = [(heuristica(raiz, alvo, fator), next(sequencia), 0, raiz)]
    g = {raiz: 0}
    pais = {raiz: None}
    expandidos, maior = 0, 1
    while fronteira:
        _, _, custo_atual, atual = heappop(fronteira)
        if custo_atual != g[atual]:
            continue  # entrada antiga; nós com custo menor podem ser reabertos
        expandidos += 1
        if atual == alvo:
            etiqueta = "" if nome == "UCS" else f"h={fator}×Manhattan"
            return resultado(nome, etiqueta, grade, pais, alvo, expandidos, maior, inicio)
        for proximo in vizinhos(grade, atual):
            novo = custo_atual + CUSTO[grade[proximo[0]][proximo[1]]]
            if novo < g.get(proximo, float("inf")):
                g[proximo] = novo
                pais[proximo] = atual
                heappush(fronteira, (novo + heuristica(proximo, alvo, fator),
                                    next(sequencia), novo, proximo))
        maior = max(maior, len(fronteira))
    raise ValueError("Objetivo inacessível")

def ucs(grade):
    return busca_custo(grade)

def astar(grade, fator):
    return busca_custo(grade, "A*", fator)
