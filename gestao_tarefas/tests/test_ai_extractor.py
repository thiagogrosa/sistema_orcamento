#!/usr/bin/env python3
"""
Testes para AIExtractor

Para rodar:
    pytest tests/test_ai_extractor.py -v

Para rodar testes de integração (requer API key):
    pytest tests/test_ai_extractor.py -v -m integration
"""

import pytest
import json
import os
from unittest.mock import Mock, patch, MagicMock
from src.ai_extractor import (
    AIExtractor,
    AIExtractorError,
    ExtractionValidationError,
    OrcamentoData
)


class TestOrcamentoDataValidation:
    """Testes de validação do schema Pydantic."""

    def test_schema_valido_minimo(self):
        """Deve validar dados mínimos obrigatórios."""
        dados = {
            "cliente": "Empresa ABC",
            "local": "São Paulo - SP",
            "tipo_servico": "instalacao",
            "origem": "comercial",
            "descricao": "Instalação de split"
        }

        orcamento = OrcamentoData(**dados)
        assert orcamento.cliente == "Empresa ABC"
        assert orcamento.tipo_servico == "instalacao"

    def test_schema_valido_completo(self):
        """Deve validar dados completos."""
        dados = {
            "cliente": "Empresa XYZ Ltda",
            "cnpj_cpf": "12.345.678/0001-90",
            "contato": "João Silva",
            "telefone": "(11) 98765-4321",
            "email": "joao@empresa.com",
            "local": "Porto Alegre - RS",
            "prazo": "2026-02-15",
            "tipo_servico": "manutencao",
            "eh_licitacao": False,
            "numero_edital": None,
            "porte": "medio",
            "origem": "cliente_direto",
            "descricao": "PMOC completo",
            "urgente": False,
            "cliente_estrategico": False
        }

        orcamento = OrcamentoData(**dados)
        assert orcamento.cliente == "Empresa XYZ Ltda"
        assert orcamento.porte == "medio"

    def test_validacao_cliente_vazio(self):
        """Deve rejeitar cliente vazio."""
        dados = {
            "cliente": "",
            "local": "São Paulo - SP",
            "tipo_servico": "instalacao",
            "origem": "comercial",
            "descricao": "Teste"
        }

        with pytest.raises(ValueError, match="não pode estar vazio"):
            OrcamentoData(**dados)

    def test_validacao_tipo_servico_invalido(self):
        """Deve rejeitar tipo_servico inválido."""
        dados = {
            "cliente": "Empresa ABC",
            "local": "São Paulo - SP",
            "tipo_servico": "outro",  # Inválido
            "origem": "comercial",
            "descricao": "Teste"
        }

        with pytest.raises(ValueError):
            OrcamentoData(**dados)

    def test_validacao_local_sem_uf(self):
        """Deve rejeitar local sem UF."""
        dados = {
            "cliente": "Empresa ABC",
            "local": "São Paulo",  # Faltando " - SP"
            "tipo_servico": "instalacao",
            "origem": "comercial",
            "descricao": "Teste"
        }

        with pytest.raises(ValueError, match="Local inválido"):
            OrcamentoData(**dados)

    def test_validacao_prazo_formato_invalido(self):
        """Deve rejeitar prazo em formato errado."""
        dados = {
            "cliente": "Empresa ABC",
            "local": "São Paulo - SP",
            "tipo_servico": "instalacao",
            "origem": "comercial",
            "descricao": "Teste",
            "prazo": "15/02/2026"  # Formato errado (deveria ser YYYY-MM-DD)
        }

        with pytest.raises(ValueError, match="Data inválida"):
            OrcamentoData(**dados)

    def test_validacao_prazo_null(self):
        """Deve aceitar prazo null."""
        dados = {
            "cliente": "Empresa ABC",
            "local": "São Paulo - SP",
            "tipo_servico": "instalacao",
            "origem": "comercial",
            "descricao": "Teste",
            "prazo": None
        }

        orcamento = OrcamentoData(**dados)
        assert orcamento.prazo is None


class TestAIExtractorInit:
    """Testes de inicialização do AIExtractor."""

    @patch.dict(os.environ, {"CLAUDE_API_KEY": "sk-test-123"})
    def test_init_com_env_var(self):
        """Deve inicializar com API key do ambiente."""
        extractor = AIExtractor()
        assert extractor.api_key == "sk-test-123"

    def test_init_com_api_key(self):
        """Deve aceitar API key como parâmetro."""
        extractor = AIExtractor(api_key="sk-custom-456")
        assert extractor.api_key == "sk-custom-456"

    @patch.dict(os.environ, {}, clear=True)
    def test_init_sem_api_key(self):
        """Deve lançar erro se não tem API key."""
        with pytest.raises(AIExtractorError, match="CLAUDE_API_KEY não encontrada"):
            AIExtractor()

    @patch.dict(os.environ, {"CLAUDE_API_KEY": "sk-test-123"})
    def test_init_carrega_prompts(self):
        """Deve carregar templates de prompt."""
        extractor = AIExtractor()
        assert extractor.prompt_haiku is not None
        assert extractor.prompt_sonnet is not None
        assert len(extractor.prompt_haiku) > 100
        assert "{texto_preparado}" in extractor.prompt_haiku


class TestAIExtractorCustos:
    """Testes de cálculo de custos."""

    @patch.dict(os.environ, {"CLAUDE_API_KEY": "sk-test-123"})
    def test_calcular_custo_haiku(self):
        """Deve calcular custo corretamente para Haiku."""
        extractor = AIExtractor()

        # Haiku: $0.25 input / $1.25 output por 1M tokens
        custo = extractor._calcular_custo("haiku", 1000, 500)

        # (1000/1M * 0.25) + (500/1M * 1.25) = 0.00025 + 0.000625 = 0.000875
        assert abs(custo - 0.000875) < 0.0001

    @patch.dict(os.environ, {"CLAUDE_API_KEY": "sk-test-123"})
    def test_calcular_custo_sonnet(self):
        """Deve calcular custo corretamente para Sonnet."""
        extractor = AIExtractor()

        # Sonnet: $3 input / $15 output por 1M tokens
        custo = extractor._calcular_custo("sonnet", 1000, 500)

        # (1000/1M * 3) + (500/1M * 15) = 0.003 + 0.0075 = 0.0105
        assert abs(custo - 0.0105) < 0.0001


# ===== Testes de Integração (requerem API key real) =====

@pytest.mark.integration
@pytest.mark.skipif(
    not os.environ.get("CLAUDE_API_KEY"),
    reason="CLAUDE_API_KEY não configurada"
)
class TestAIExtractorIntegration:
    """
    Testes de integração com Claude API real.

    Requer CLAUDE_API_KEY configurada.
    Para rodar: pytest tests/test_ai_extractor.py -v -m integration
    """

    def setup_method(self):
        """Setup para testes de integração."""
        self.extractor = AIExtractor()

    def test_extrair_caso_simples_haiku(self):
        """Teste de extração simples com Haiku."""
        texto = """
# Dados Preparados

## Metadados Detectados
- CNPJ: 12.345.678/0001-90
- Telefones: (11) 98765-4321
- Emails: joao@empresaabc.com

## Conteúdo Principal

Cliente: Empresa ABC Ltda
Local: São Paulo - SP

Gostaria de orçamento para instalação de split 18.000 BTUs
na sala de reuniões. Área de 50m².

Prazo: 15/02/2026
        """

        resultado = self.extractor.extrair(texto)

        # Verificar campos obrigatórios
        assert resultado['cliente'] is not None
        assert resultado['local'] == "São Paulo - SP" or "São Paulo" in resultado['local']
        assert resultado['tipo_servico'] == "instalacao"
        assert resultado['descricao'] is not None

        # Verificar que usou Haiku
        stats = self.extractor.get_estatisticas()
        print(f"\nEstatísticas:")
        print(f"  Modelo: {stats['modelo']}")
        print(f"  Tokens: {stats['tokens_total']}")
        print(f"  Custo: ${stats['custo_usd']:.4f}")

        assert stats['modelo'] == "haiku"
        assert stats['custo_usd'] < 0.01  # Deve ser muito barato

    def test_extrair_caso_licitacao(self):
        """Teste de extração de licitação."""
        texto = """
# Dados Preparados

## Conteúdo Principal

Cliente: Prefeitura de Uberlândia
Pregão: 045/2025
Local: Uberlândia - MG
Prazo: 28/02/2026

PMOC para 97 máquinas em 4 unidades da cidade.
Grande porte.
        """

        resultado = self.extractor.extrair(texto)

        assert resultado['eh_licitacao'] is True
        assert "045/2025" in (resultado['numero_edital'] or "")
        assert resultado['tipo_servico'] == "manutencao"
        assert resultado['porte'] in ["medio", "grande"]

    def test_extrair_caso_projeto_urgente(self):
        """Teste de extração de projeto urgente."""
        texto = """
# Dados Preparados

## Metadados Detectados
- Telefones: (49) 99159-1759
- Emails: cesar@seara.com.br

## Conteúdo Principal

JBS Seara - Nova Veneza/SC
Contato: Cesar Felicetti

Projeto de climatização e exaustão para cozinha industrial.
URGENTE - precisam até semana que vem.
        """

        resultado = self.extractor.extrair(texto)

        assert resultado['tipo_servico'] == "projeto"
        assert resultado['urgente'] is True
        assert "Nova Veneza" in resultado['local']

    def test_comparar_custo_haiku_vs_sonnet(self):
        """Compara custo de Haiku vs Sonnet."""
        texto = """
# Dados Preparados

Cliente: Empresa Teste Ltda
Local: Porto Alegre - RS
Tipo: Instalação de sistema split
        """

        # Extrair com Haiku
        extractor_haiku = AIExtractor()
        resultado_haiku = extractor_haiku.extrair(texto)
        stats_haiku = extractor_haiku.get_estatisticas()

        # Extrair com Sonnet
        extractor_sonnet = AIExtractor(force_sonnet=True)
        resultado_sonnet = extractor_sonnet.extrair(texto)
        stats_sonnet = extractor_sonnet.get_estatisticas()

        print(f"\n{'='*70}")
        print("Comparação Haiku vs Sonnet:")
        print(f"{'='*70}")
        print(f"\nHaiku:")
        print(f"  Tokens total: {stats_haiku['tokens_total']}")
        print(f"  Custo: ${stats_haiku['custo_usd']:.4f}")
        print(f"\nSonnet:")
        print(f"  Tokens total: {stats_sonnet['tokens_total']}")
        print(f"  Custo: ${stats_sonnet['custo_usd']:.4f}")
        print(f"\nEconomia com Haiku: ${stats_sonnet['custo_usd'] - stats_haiku['custo_usd']:.4f}")
        print(f"Percentual: {(1 - stats_haiku['custo_usd'] / stats_sonnet['custo_usd']) * 100:.1f}%")
        print(f"{'='*70}\n")

        # Haiku deve ser mais barato
        assert stats_haiku['custo_usd'] < stats_sonnet['custo_usd']

        # Ambos devem ter extraído dados válidos
        assert resultado_haiku['cliente'] is not None
        assert resultado_sonnet['cliente'] is not None


@pytest.mark.integration
@pytest.mark.skipif(
    not os.environ.get("CLAUDE_API_KEY"),
    reason="CLAUDE_API_KEY não configurada"
)
class TestAIExtractorCasosReais:
    """
    Testes com casos reais de emails processados.
    """

    def setup_method(self):
        """Setup para testes."""
        self.extractor = AIExtractor()

    def test_email_exemplo_fixture(self):
        """Teste com fixture de exemplo."""
        fixture_path = "tests/fixtures/email_exemplo_preparado.md"

        if not os.path.exists(fixture_path):
            pytest.skip(f"Fixture não encontrada: {fixture_path}")

        with open(fixture_path, 'r', encoding='utf-8') as f:
            texto = f.read()

        resultado = self.extractor.extrair(texto)

        # Verificar estrutura
        assert isinstance(resultado, dict)
        assert 'cliente' in resultado
        assert 'tipo_servico' in resultado
        assert 'local' in resultado

        # Exibir resultado
        print(f"\nResultado da extração:")
        print(json.dumps(resultado, indent=2, ensure_ascii=False))

        stats = self.extractor.get_estatisticas()
        print(f"\nEstatísticas:")
        print(f"  Modelo: {stats['modelo']}")
        print(f"  Tokens: {stats['tokens_total']}")
        print(f"  Custo: ${stats['custo_usd']:.4f}")
