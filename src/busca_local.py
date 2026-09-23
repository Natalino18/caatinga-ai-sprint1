"""Escolhe 15 talhões por uma pontuação de risco e custo de deslocamento.

Pontuações são um modelo didático, não observações reais de pragas.
"""
import math
import random
import statistics

def candidatos(grade):
    return [(i, j) for i, linha in enumerate(grade) for j, celula in enumerate(linha)
            if celula != "#" and (i, j) not in ((0, 0), (len(grade)-1, len(grade)-1))]

def risco(grade, p):
    i, j = p
    molhados = sum(grade[a][b] == "~" for a, b in
                    ((i-1,j), (i+1,j), (i,j-1), (i,j+1))
                    if 0 <= a < len(grade) and 0 <= b < len(grade[a]))
    return 2 + 3 * (grade[i][j] == "~") + molhados

def pontuacao(grade, selecao):
    # Benefício esperado menos deslocamento mínimo aproximado (não é rota real).
    restantes, atual, deslocamento = set(selecao), (0, 0), 0
    while restantes:
        proximo = min(restantes, key=lambda p: (abs(atual[0]-p[0]) + abs(atual[1]-p[1]), p))
        deslocamento += abs(atual[0]-proximo[0]) + abs(atual[1]-proximo[1])
        atual = proximo
        restantes.remove(proximo)
    return sum(risco(grade, p) for p in selecao) - 0.3 * deslocamento

def vizinho(selecao, universo, rng):
    retirada = rng.choice(tuple(selecao))
    entrada = rng.choice(tuple(sorted(universo - selecao)))
    return selecao - {retirada} | {entrada}

def executar(grade, metodo, repeticoes=30, k=15, passos=300, semente=0):
    universo = set(candidatos(grade))
    if len(universo) < k:
        raise ValueError("Há menos de K talhões livres")
    resultados = []
    exemplos_piora = []
    for execucao in range(repeticoes):
        rng = random.Random(semente + execucao)
        atual = set(rng.sample(sorted(universo), k))
        valor = pontuacao(grade, atual)
        melhor = valor
        pioras = 0
        for t in range(passos):
            proximo = vizinho(atual, universo, rng)
            novo = pontuacao(grade, proximo)
            delta = novo - valor
            temperatura = max(0.05, 8 * (1 - t / passos))
            aceita = delta > 0 or (metodo == "tempera" and delta < 0 and rng.random() < math.exp(delta / temperatura))
            if aceita:
                if delta < 0:
                    pioras += 1
                atual, valor = proximo, novo
                melhor = max(melhor, valor)
        resultados.append(round(melhor, 3))
        exemplos_piora.append(pioras)
    return {"valores": resultados, "media": statistics.mean(resultados),
            "desvio": statistics.stdev(resultados), "melhor": max(resultados),
            "pioras_aceitas": exemplos_piora}
