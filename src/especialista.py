"""Base pequena de regras e prova por encadeamento para trás."""
REGRAS = [
    ("sensor_positivo", ("leitura_positiva",), "R1"),
    ("risco_elevado", ("sensor_positivo", "umidade_alta"), "R2"),
    ("pulverizacao_antiga", ("dias_maior_14",), "R3"),
    ("inspecionar_prioridade_alta", ("risco_elevado", "pulverizacao_antiga"), "R4"),
    ("inspecionar_prioridade_normal", ("sensor_positivo",), "R5"),
    ("manter_monitoramento", ("sensor_negativo", "sem_sintomas_visuais"), "R6"),
    ("nao_pulverizar_automaticamente", ("sem_laudo_humano",), "R7"),
]

def provar(meta, fatos, regras=REGRAS, visitados=None):
    visitados = set() if visitados is None else visitados
    if meta in fatos:
        return [f"Fato observado: {meta}"]
    if meta in visitados:
        return None
    for consequencia, premissas, identificador in regras:
        if consequencia != meta:
            continue
        trilha = []
        for premissa in premissas:
            prova = provar(premissa, fatos, regras, visitados | {meta})
            if prova is None:
                break
            trilha.extend(prova)
        else:
            return trilha + [f"{identificador}: SE {' E '.join(premissas)} ENTÃO {meta}"]
    return None

def demonstracao():
    fatos = {"leitura_positiva", "umidade_alta", "dias_maior_14", "sem_laudo_humano"}
    caso = {"sensor_negativo", "sintomas_visuais", "sem_laudo_humano"}
    corrigidas = REGRAS + [("inspecionar_prioridade_alta", ("sintomas_visuais",), "R8")]
    return {"exemplo": provar("inspecionar_prioridade_alta", fatos),
            "antes": provar("inspecionar_prioridade_alta", caso),
            "depois": provar("inspecionar_prioridade_alta", caso, corrigidas)}
