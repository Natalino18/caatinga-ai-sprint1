import contextlib
import csv
import io
import json
import tempfile
import unittest
from pathlib import Path
from test_buscas import gerar_pomar
from main import main


class IntegracaoTest(unittest.TestCase):
    def test_arquivos_e_reexecucao(self):
        from PIL import Image
        with tempfile.TemporaryDirectory() as temporario:
            pasta = Path(temporario)
            with contextlib.redirect_stdout(io.StringIO()):
                main(24114007, pasta)
            anterior = json.loads((pasta / 'analise.json').read_text())
            with (pasta / 'resultados.csv').open() as arquivo:
                linhas = list(csv.DictReader(arquivo))
            self.assertEqual([int(r['custo']) for r in linhas], [40, 103, 37, 37, 37, 37])
            self.assertTrue(
                (pasta / 'pomar.txt')
                .read_text(encoding='utf-8')
                .startswith('Matrícula-semente: 24114007')
            )
            with Image.open(pasta / 'grafico.png') as imagem:
                imagem.verify()
            (pasta / 'pomar.txt').write_text('arquivo danificado')
            with contextlib.redirect_stdout(io.StringIO()):
                main(24114007, pasta)
            self.assertEqual(anterior, json.loads((pasta / 'analise.json').read_text()))
            self.assertNotIn(
                'danificado',
                (pasta / 'pomar.txt').read_text(encoding='utf-8')
            )