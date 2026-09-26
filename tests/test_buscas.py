import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from buscas import bfs, dfs, ucs, astar
from gerador_pomar import gerar_pomar, CUSTO


class BuscasTest(unittest.TestCase):
    def test_bfs_nao_garante_menor_custo(self):
        grade = gerar_pomar(20231045)

        resultado_bfs = bfs(grade)
        resultado_ucs = ucs(grade)

        self.assertEqual(resultado_bfs.passos, 22)
        self.assertEqual(resultado_ucs.passos, 22)
        self.assertGreater(resultado_bfs.custo, resultado_ucs.custo)

    def test_rotas_e_otimalidade(self):
        for semente in (24114007, 20231045, 1, 2, 3):
            grade = gerar_pomar(semente)
            referencia = ucs(grade)
            for r in (bfs(grade), dfs(grade), referencia, astar(grade, 0), astar(grade, 1), astar(grade, 4)):
                self.assertEqual(r.rota[0], (0, 0))
                self.assertEqual(r.rota[-1], (11, 11))
                self.assertEqual(r.passos, len(r.rota) - 1)
                self.assertEqual(r.custo, sum(CUSTO[grade[i][j]] for i, j in r.rota[1:]))
                for a, b in zip(r.rota, r.rota[1:]):
                    self.assertEqual(abs(a[0]-b[0])+abs(a[1]-b[1]), 1)
            self.assertEqual(astar(grade, 0).custo, referencia.custo)
            self.assertEqual(astar(grade, 1).custo, referencia.custo)

    def test_custos_distintos_e_sem_caminho(self):
        grade = [list('.~.'), list('...')]
        self.assertEqual(ucs(grade).custo, 3)
        self.assertEqual(astar(grade, 1).custo, 3)
        for busca in (bfs, dfs, ucs, lambda g: astar(g, 1)):
            self.assertEqual(busca([['.']]).custo, 0)
            with self.assertRaises(ValueError):
                busca([list('.#'), list('#.')])
            for invalida in ([], [[]], [list('..'), ['.']], [['#']], [['x']]):
                with self.assertRaises(ValueError):
                    busca(invalida)

    def test_heuristica_nao_admissivel(self):
        grade = gerar_pomar(3)

        resultado_ucs = ucs(grade)
        resultado_astar = astar(grade, 4)

        self.assertEqual(resultado_ucs.custo, 33)
        self.assertEqual(resultado_astar.custo, 40)
        self.assertGreater(resultado_astar.custo, resultado_ucs.custo)