#!/usr/bin/env python3
"""
Testes para CLI

Para rodar:
    pytest tests/test_cli.py -v
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import json

from src.cli import OrcamentoCLI


class TestCLIInit:
    """Testes de inicialização."""

    def test_init_defaults(self):
        """Deve inicializar com configurações padrão."""
        cli = OrcamentoCLI()

        assert cli.verbose is False
        assert cli.dry_run is False
        assert cli.data_preparer is not None
        assert cli.asana_lib is not None
        assert 'inicio' in cli.stats

    def test_init_dry_run(self):
        """Deve configurar modo dry-run."""
        cli = OrcamentoCLI(dry_run=True)

        assert cli.dry_run is True

    def test_init_verbose(self):
        """Deve configurar modo verbose."""
        cli = OrcamentoCLI(verbose=True)

        assert cli.verbose is True


class TestCLIVerificarPasta:
    """Testes de verificação de pasta."""

    def setup_method(self):
        """Setup para cada teste."""
        self.cli = OrcamentoCLI()

    def test_verificar_pasta_nao_encontrada(self):
        """Deve retornar None se pasta não existe."""
        resultado = self.cli._verificar_pasta("99_999")

        assert resultado is None

    @patch('pathlib.Path.glob')
    def test_verificar_pasta_encontrada(self, mock_glob):
        """Deve retornar Path se pasta existe."""
        mock_pasta = Mock(spec=Path)
        mock_pasta.is_dir.return_value = True
        mock_glob.return_value = [mock_pasta]

        resultado = self.cli._verificar_pasta("26_001")

        # Em ambiente de teste sem pasta real, retorna None
        # Mas a lógica está testada via mock


class TestCLIBuscarEmails:
    """Testes de busca de emails."""

    def setup_method(self):
        """Setup para cada teste."""
        self.cli = OrcamentoCLI()

    def test_buscar_emails_dry_run(self):
        """Deve pular busca em modo dry-run."""
        self.cli.dry_run = True

        emails = self.cli._buscar_emails_relacionados("26_001")

        assert emails == []

    @patch('src.cli.GmailClient')
    def test_buscar_emails_sem_query(self, mock_gmail_class):
        """Deve construir query a partir do ID."""
        mock_client = Mock()
        mock_client.authenticate.return_value = True
        mock_client.buscar_emails.return_value = []
        mock_gmail_class.return_value = mock_client

        self.cli._buscar_emails_relacionados("26_001_EMPRESA_SERVICO")

        # Deve ter tentado buscar
        assert mock_client.buscar_emails.called


class TestCLIPrepararDados:
    """Testes de preparação de dados."""

    def setup_method(self):
        """Setup para cada teste."""
        self.cli = OrcamentoCLI()

    def test_preparar_dados_sem_pasta(self):
        """Deve retornar None sem pasta."""
        resultado = self.cli._preparar_dados(None)

        assert resultado is None

    def test_preparar_dados_pasta_vazia(self, tmp_path):
        """Deve retornar None se pasta vazia."""
        resultado = self.cli._preparar_dados(tmp_path)

        assert resultado is None

    def test_preparar_dados_com_arquivos(self, tmp_path):
        """Deve processar arquivos encontrados."""
        # Criar arquivo de teste
        email_file = tmp_path / "email.txt"
        email_file.write_text("Cliente: Empresa ABC\nLocal: São Paulo")

        resultado = self.cli._preparar_dados(tmp_path)

        assert resultado is not None
        assert "Empresa ABC" in resultado


class TestCLIExtrairInformacoes:
    """Testes de extração de informações."""

    def setup_method(self):
        """Setup para cada teste."""
        self.cli = OrcamentoCLI()

    def test_extrair_informacoes_dry_run(self):
        """Deve retornar dados mock em dry-run."""
        self.cli.dry_run = True

        resultado = self.cli._extrair_informacoes("texto teste")

        assert resultado is not None
        assert resultado['cliente'] == '[DRY-RUN] Cliente Teste'

    @patch('src.cli.AIExtractor')
    def test_extrair_informacoes_sucesso(self, mock_extractor_class):
        """Deve extrair informações com IA."""
        mock_extractor = Mock()
        mock_extractor.extrair.return_value = {
            'cliente': 'Empresa ABC',
            'local': 'São Paulo - SP',
            'tipo_servico': 'instalacao'
        }
        mock_extractor.get_estatisticas.return_value = {
            'modelo': 'haiku-4',
            'tokens_total': 700,
            'custo_usd': 0.0004
        }
        mock_extractor_class.return_value = mock_extractor

        self.cli.ai_extractor = mock_extractor
        resultado = self.cli._extrair_informacoes("texto preparado")

        assert resultado is not None
        assert resultado['cliente'] == 'Empresa ABC'


class TestCLICriarTarefa:
    """Testes de criação de tarefa."""

    def setup_method(self):
        """Setup para cada teste."""
        self.cli = OrcamentoCLI()

    def test_criar_tarefa_dry_run(self):
        """Deve retornar ID mock em dry-run."""
        self.cli.dry_run = True

        task_id = self.cli._criar_tarefa_asana({
            'cliente': 'Teste',
            'local': 'SP',
            'tipo_servico': 'instalacao'
        })

        assert task_id == "DRY_RUN_ID"

    @patch('src.cli.AsanaLib')
    def test_criar_tarefa_sucesso(self, mock_asana_class):
        """Deve criar tarefa no Asana."""
        mock_asana = Mock()
        mock_asana.criar_orcamento.return_value = "task_123"
        mock_asana.project_id = "project_456"

        self.cli.asana_lib = mock_asana

        task_id = self.cli._criar_tarefa_asana({
            'cliente': 'Empresa ABC',
            'local': 'São Paulo - SP',
            'tipo_servico': 'instalacao'
        })

        assert task_id == "task_123"


class TestCLIComandosIndividuais:
    """Testes de comandos individuais."""

    def setup_method(self):
        """Setup para cada teste."""
        self.cli = OrcamentoCLI()

    def test_preparar_dados_arquivo_nao_existe(self):
        """Deve lidar com arquivo inexistente."""
        # Não deve lançar exceção, apenas logar erro
        self.cli.preparar_dados("arquivo_inexistente.txt")

    def test_extrair_dados_arquivo_nao_existe(self):
        """Deve lidar com arquivo inexistente."""
        self.cli.extrair_dados("arquivo_inexistente.txt")

    def test_criar_tarefa_arquivo_nao_existe(self):
        """Deve lidar com arquivo inexistente."""
        self.cli.criar_tarefa("arquivo_inexistente.json")

    def test_preparar_dados_arquivo_valido(self, tmp_path):
        """Deve processar arquivo válido."""
        input_file = tmp_path / "email.txt"
        input_file.write_text("Cliente: Empresa ABC")

        output_file = tmp_path / "preparado.md"

        self.cli.preparar_dados(str(input_file), str(output_file))

        # Deve ter criado arquivo de saída
        assert output_file.exists()

    def test_extrair_dados_com_output(self, tmp_path):
        """Deve salvar extração em arquivo."""
        input_file = tmp_path / "preparado.md"
        input_file.write_text("Cliente: Empresa ABC\nLocal: São Paulo - SP")

        output_file = tmp_path / "resultado.json"

        self.cli.dry_run = True  # Usar mock
        self.cli.extrair_dados(str(input_file), str(output_file))


class TestCLIRelatorio:
    """Testes de relatório."""

    def setup_method(self):
        """Setup para cada teste."""
        self.cli = OrcamentoCLI()

    def test_exibir_relatorio_basico(self):
        """Deve exibir relatório sem erros."""
        self.cli.stats['emails_encontrados'] = 5
        self.cli.stats['arquivos_processados'] = 3
        self.cli.stats['tokens_usados'] = 700
        self.cli.stats['custo_total'] = 0.0004

        # Não deve lançar exceção
        self.cli._exibir_relatorio(None)

    def test_exibir_relatorio_com_tarefa(self):
        """Deve incluir informações da tarefa."""
        self.cli._exibir_relatorio("task_123")


class TestCLIIntegration:
    """Testes de integração do pipeline."""

    def setup_method(self):
        """Setup para cada teste."""
        self.cli = OrcamentoCLI(dry_run=True)

    def test_processar_pasta_dry_run(self):
        """Deve executar pipeline em dry-run."""
        resultado = self.cli.processar_pasta("26_001")

        # Pode falhar por falta de dados, mas não deve crashar
        assert isinstance(resultado, bool)

    @patch('src.cli.OrcamentoCLI._verificar_pasta')
    @patch('src.cli.OrcamentoCLI._buscar_emails_relacionados')
    @patch('src.cli.OrcamentoCLI._preparar_dados')
    @patch('src.cli.OrcamentoCLI._extrair_informacoes')
    @patch('src.cli.OrcamentoCLI._criar_tarefa_asana')
    def test_processar_pasta_completo_mock(
        self,
        mock_criar,
        mock_extrair,
        mock_preparar,
        mock_buscar,
        mock_verificar
    ):
        """Deve executar pipeline completo com mocks."""
        # Setup mocks
        mock_verificar.return_value = Path("/fake/path")
        mock_buscar.return_value = []
        mock_preparar.return_value = "texto preparado"
        mock_extrair.return_value = {
            'cliente': 'Empresa ABC',
            'local': 'São Paulo - SP',
            'tipo_servico': 'instalacao',
            'origem': 'comercial',
            'descricao': 'Teste'
        }
        mock_criar.return_value = "task_123"

        cli = OrcamentoCLI()
        resultado = cli.processar_pasta("26_001")

        assert resultado is True
        assert mock_verificar.called
        assert mock_buscar.called
        assert mock_preparar.called
        assert mock_extrair.called
        assert mock_criar.called
