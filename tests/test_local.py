import unittest
from test_buscas import gerar_pomar
from busca_local import executar, candidatos, pontuacao


class LocalTest(unittest.TestCase):
    def test_reproducao_e_selecoes(self):
        grade = gerar_pomar(24114007)
        for metodo in ('encosta', 'tempera'):
            r = executar(grade, metodo, repeticoes=2, passos=30, semente=24114007)
            self.assertEqual(r, executar(grade, metodo, repeticoes=2, passos=30, semente=24114007))
            for selecao, valor in zip(r['selecoes'], r['valores']):
                self.assertEqual(len(set(selecao)), 15)
                self.assertTrue(set(selecao) <= set(candidatos(grade)))
                self.assertAlmostEqual(pontuacao(grade, selecao), valor)
            if metodo == 'encosta':
                self.assertEqual(r['pioras_aceitas'], [0, 0])

    def test_limites(self):
        grade = [list('...')]
        self.assertEqual(executar(grade, 'encosta', k=1, repeticoes=2)['selecoes'], [[(0, 1)], [(0, 1)]])
        for parametros in ({'metodo':'invalido'}, {'metodo':'encosta','k':0}, {'metodo':'encosta','k':15}, {'metodo':'encosta','repeticoes':1}):
            with self.assertRaises(ValueError):
                executar(grade, **parametros)
