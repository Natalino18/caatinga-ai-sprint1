"""Escala em subprocessos: limite real de 60 s por busca, sem incluir geração.

O experimento usa subprocessos e interrompe cada busca após 60 segundos.
"""
import argparse
import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter


def trabalhador(semente, n, metodo):
    from gerador_pomar import gerar_pomar
    from buscas import bfs, dfs, ucs
    fase = 'geracao'
    try:
        grade = gerar_pomar(semente, n)
        print('PRONTO', flush=True)
        fase = 'busca'
        inicio = perf_counter()
        r = {'BFS': bfs, 'DFS': dfs, 'UCS': ucs}[metodo](grade)
        print(json.dumps({'status': 'concluido', 'tempo_s': perf_counter()-inicio,
                          'expandidos': r.nos_expandidos, 'fronteira_max': r.fronteira_max,
                          'custo': r.custo, 'passos': r.passos}), flush=True)
    except MemoryError:
        print(json.dumps({'status': 'limite_memoria', 'fase': fase}), flush=True)


def executar(semente, pasta):
    registros = []
    for metodo in ('BFS', 'DFS', 'UCS'):
        for n in (100, 400, 1000, 2000, 4000, 8000):
            comando = [sys.executable, __file__, str(semente), '--worker', str(n), metodo]
            with subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as p:
                # Geração tem limite separado: nenhum tempo de busca inventado.
                import selectors
                with selectors.DefaultSelector() as seletor:
                    seletor.register(p.stdout, selectors.EVENT_READ)
                    pronta = bool(seletor.select(60))
                primeira = p.stdout.readline().strip() if pronta else ''
                if primeira == 'PRONTO':
                    try:
                        saida, erro = p.communicate(timeout=60)
                        dado = json.loads(saida) if saida.strip() else {'status': 'erro', 'erro': erro}
                    except subprocess.TimeoutExpired:
                        p.kill()
                        p.communicate()
                        dado = {'status': 'limite_tempo', 'tempo_s_minimo': 60, 'fase': 'busca'}
                elif primeira:
                    p.communicate()
                    dado = json.loads(primeira)
                else:
                    p.kill()
                    _, erro = p.communicate()
                    dado = {'status': 'erro_ou_limite_geracao', 'erro': erro}
            registro = {'metodo': metodo, 'n': n, **dado}
            registros.append(registro)
            print(registro, flush=True)
            if dado['status'] != 'concluido':
                break
    dados = {'semente': semente, 'data_utc': datetime.now(timezone.utc).isoformat(),
             'python': sys.version, 'plataforma': platform.platform(),
             'processador': platform.processor(), 'cpus_logicas': os.cpu_count(),
             'limite_busca_s': 60,
             'repeticoes_por_caso': 1, 'registros': registros}
    pasta.mkdir(exist_ok=True)
    (pasta / 'escala.json').write_text(json.dumps(dados, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    return dados


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('semente', type=int)
    parser.add_argument('--worker', nargs=2, metavar=('N', 'METODO'))
    args = parser.parse_args()
    if args.worker:
        trabalhador(args.semente, int(args.worker[0]), args.worker[1])
    else:
        executar(args.semente, Path(__file__).resolve().parents[1] / 'resultados')
