"""python src/main.py 24114007"""
import argparse
import csv
import json
import os
import platform
from pathlib import Path
from gerador_pomar import gerar_pomar
from buscas import bfs, dfs, ucs, astar
from busca_local import executar
from bayes import calcular
from especialista import demonstracao

def main(matricula, pasta=None):
    pasta = Path(pasta) if pasta is not None else Path(__file__).resolve().parent.parent / "resultados"
    pasta.mkdir(exist_ok=True)
    grade = gerar_pomar(matricula)
    (pasta / "pomar.txt").write_text(f"Matrícula-semente: {matricula}\n" +
                                     "\n".join(" ".join(l) for l in grade) + "\n", encoding="utf-8")
    resultados = [bfs(grade), dfs(grade), ucs(grade),
                  astar(grade, 0), astar(grade, 1), astar(grade, 4)]
    with (pasta / "resultados.csv").open("w", newline="", encoding="utf-8") as arquivo:
        colunas = ["estrategia", "heuristica", "custo", "passos", "nos_expandidos", "fronteira_max", "tempo_ms"]
        escritor = csv.DictWriter(arquivo, fieldnames=colunas, lineterminator="\n")
        escritor.writeheader()
        for r in resultados:
            escritor.writerow({campo: getattr(r, campo) for campo in colunas})
    os.environ.setdefault("MPLCONFIGDIR", str(pasta.parent / ".cache" / "matplotlib"))
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    rotulos = [r.estrategia + (" " + r.heuristica if r.heuristica else "") for r in resultados]
    fig, eixo = plt.subplots(figsize=(10, 5))
    barras = eixo.bar(rotulos, [r.nos_expandidos for r in resultados])
    eixo.bar_label(barras)
    eixo.set_ylim(0, max(r.nos_expandidos for r in resultados) * 1.15)
    eixo.set_xlabel("Estratégia e heurística")
    eixo.set_ylabel("Nós expandidos (quantidade)")
    eixo.set_title(f"Nós expandidos no pomar: semente {matricula}")
    fig.autofmt_xdate(rotation=25)
    fig.tight_layout()
    fig.savefig(pasta / "grafico.png", dpi=150)
    plt.close(fig)
    adicionais = {
        "matricula": matricula,
        "ambiente": {"python": platform.python_version(), "plataforma": platform.platform(),
                     "matplotlib": matplotlib.__version__},
        "estados_livres": sum(c != "#" for linha in grade for c in linha),
        "sensor": calcular(matricula),
        "busca_local": {metodo: executar(grade, metodo, semente=matricula)
                        for metodo in ("encosta", "tempera")},
        "especialista": demonstracao(),
        "rotas": {rotulos[i]: r.rota for i, r in enumerate(resultados)},
    }
    (pasta / "analise.json").write_text(json.dumps(adicionais, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Pomar da matrícula {matricula}. Arquivos gerados em {pasta}")
    for r in resultados:
        print(f"{r.estrategia:3} {r.heuristica:16} custo={r.custo:3} passos={r.passos:3} "
              f"expandidos={r.nos_expandidos:3} fronteira={r.fronteira_max:3}")
    print("\nPor que inspecionar com prioridade alta?")
    for passo in adicionais["especialista"]["exemplo"]:
        print(" ", passo)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("matricula", type=int, help="Matrícula sem pontos")
    parser.add_argument("--escala", action="store_true", help="Também executa o experimento até 60 s por busca")
    args = parser.parse_args()
    if args.matricula < 0:
        parser.error("Use uma matrícula não negativa, sem pontos")
    main(args.matricula)
    if args.escala:
        from escala import executar as executar_escala
        executar_escala(args.matricula, Path(__file__).resolve().parents[1] / "resultados")
