import unittest
from test_buscas import gerar_pomar
from especialista import provar, demonstracao
from bayes import calcular


class RegrasBayesTest(unittest.TestCase):
    def test_provas(self):
        r = demonstracao()
        self.assertIsNone(r['antes'])
        self.assertIn('R8:', r['depois'][-1])
        self.assertIn('R7:', r['bloqueio_pulverizacao'][-1])
        self.assertEqual([p.split(':')[0] for p in r['exemplo'] if p.startswith('R')], ['R1', 'R2', 'R3', 'R4'])
        self.assertIsNone(provar('manter_monitoramento', {'sensor_negativo', 'sintomas_visuais'}))
        self.assertIsNone(provar('a', set(), [('a', ('b',), 'X'), ('b', ('a',), 'Y')]))
        self.assertIsNotNone(provar('a', {'c'}, [('a', ('a',), 'X'), ('a', ('c',), 'Y')]))

    def test_bayes(self):
        r = calcular(24114007)
        self.assertAlmostEqual(r['vpp'], .5012159074233244)
        self.assertAlmostEqual(r['falsos_por_semana'], 57.102)
        self.assertAlmostEqual(r['horas_perdidas'], 11.4204)
        self.assertAlmostEqual(r['vpp_dois_positivos_independentes'], .9521451753567314)
        self.assertGreater(r['vpp_999'], r['vpp'])
