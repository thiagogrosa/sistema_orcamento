import unittest
import json
import shutil
from pathlib import Path
from hvac.generators.proposta_pdf import gerar_proposta_pdf
from hvac.generators.utils import carregar_configs

class TestGeradorPDFManual(unittest.TestCase):
    def setUp(self):
        self.base_dir = Path(__file__).parent.parent
        with open(self.base_dir / "tests/dados_teste_panvel.json", "r", encoding="utf-8") as f:
            self.dados = json.load(f)
        
        # Mock output dir to avoid clutter
        self.output_dir = self.base_dir / "output/testes_unitarios"
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)
        self.output_dir.mkdir(parents=True)

    def test_geracao_automatica(self):
        """Testa geracao sem parametros manuais (comportamento padrao)"""
        resultado = gerar_proposta_pdf(
            self.dados,
            output_path=self.output_dir / "auto.pdf"
        )
        self.assertTrue(resultado["sucesso"])
        self.assertIsNotNone(resultado["numero_orcamento"])
        # Deve ter formato padrao YYYY/XXX-RXX
        self.assertRegex(resultado["numero_orcamento"], r"\d{4}/\d{3}-R\d{2}")

    def test_numero_manual(self):
        """Testa geracao com numero manual"""
        numero_manual = "2023/001"
        resultado = gerar_proposta_pdf(
            self.dados,
            numero_orcamento=numero_manual,
            output_path=self.output_dir / "manual.pdf"
        )
        self.assertTrue(resultado["sucesso"])
        # Padrao adiciona revisao se nao tiver
        self.assertTrue(resultado["numero_orcamento"].startswith("2023/001"))
        self.assertIn("-R", resultado["numero_orcamento"])

    def test_numero_manual_com_revisao(self):
        """Testa geracao com numero manual ja contendo revisao"""
        numero_manual = "2023/001-R05"
        resultado = gerar_proposta_pdf(
            self.dados,
            numero_orcamento=numero_manual,
            output_path=self.output_dir / "manual_rev.pdf"
        )
        self.assertTrue(resultado["sucesso"])
        self.assertEqual(resultado["numero_orcamento"], "2023/001-R05")

    def test_revisao_manual(self):
        """Testa geracao com revisao manual explicita"""
        # Numero automatico, revisao manual
        resultado = gerar_proposta_pdf(
            self.dados,
            revisao="R09",
            output_path=self.output_dir / "rev_manual.pdf"
        )
        self.assertTrue(resultado["sucesso"])
        self.assertTrue(resultado["numero_orcamento"].endswith("-R09"))

    def test_revisao_manual_int(self):
        """Testa geracao com revisao manual como inteiro/string simples"""
        resultado = gerar_proposta_pdf(
            self.dados,
            revisao="3",
            output_path=self.output_dir / "rev_int.pdf"
        )
        self.assertTrue(resultado["sucesso"])
        self.assertTrue(resultado["numero_orcamento"].endswith("-R03"))

    def test_numero_e_revisao_manual(self):
        """Testa ambos manuais"""
        resultado = gerar_proposta_pdf(
            self.dados,
            numero_orcamento="2024/999",
            revisao="2",
            output_path=self.output_dir / "full_manual.pdf"
        )
        self.assertTrue(resultado["sucesso"])
        self.assertEqual(resultado["numero_orcamento"], "2024/999-R02")

if __name__ == "__main__":
    unittest.main()
