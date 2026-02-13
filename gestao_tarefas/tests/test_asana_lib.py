#!/usr/bin/env python3
"""
Testes para AsanaLib

Para rodar:
    pytest tests/test_asana_lib.py -v
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.asana_lib import (
    AsanaLib,
    AsanaLibError,
    AsanaTaskNotFoundError,
    SUBTAREFAS_PADRAO
)


class TestAsanaLibInit:
    """Testes de inicialização."""

    def test_init_com_defaults(self):
        """Deve inicializar com IDs padrão."""
        asana = AsanaLib()
        assert asana.workspace_id is not None
        assert asana.project_id is not None

    def test_init_com_custom_ids(self):
        """Deve aceitar IDs customizados."""
        asana = AsanaLib(
            workspace_id="custom_workspace",
            project_id="custom_project"
        )
        assert asana.workspace_id == "custom_workspace"
        assert asana.project_id == "custom_project"


class TestAsanaLibFormatacao:
    """Testes de formatação de título e descrição."""

    def setup_method(self):
        """Setup para cada teste."""
        self.asana = AsanaLib()

    def test_formatar_titulo_simples(self):
        """Deve formatar título corretamente."""
        dados = {
            "cliente": "Empresa ABC",
            "local": "São Paulo - SP",
            "tipo_servico": "instalacao",
            "eh_licitacao": False
        }

        titulo = self.asana._formatar_titulo(dados)

        assert "[INSTALACAO]" in titulo
        assert "Empresa ABC" in titulo
        assert "São Paulo - SP" in titulo
        assert "[LIC]" not in titulo

    def test_formatar_titulo_licitacao(self):
        """Deve incluir prefixo LIC para licitações."""
        dados = {
            "cliente": "Prefeitura XYZ",
            "local": "Porto Alegre - RS",
            "tipo_servico": "projeto",
            "eh_licitacao": True
        }

        titulo = self.asana._formatar_titulo(dados)

        assert "[LIC]" in titulo
        assert "[PROJETO]" in titulo
        assert "Prefeitura XYZ" in titulo

    def test_formatar_descricao_completa(self):
        """Deve formatar descrição com todos os campos."""
        dados = {
            "cliente": "Empresa ABC Ltda",
            "cnpj_cpf": "12.345.678/0001-90",
            "contato": "João Silva",
            "telefone": "(11) 98765-4321",
            "email": "joao@abc.com",
            "local": "São Paulo - SP",
            "prazo": "2026-02-15",
            "tipo_servico": "manutencao",
            "eh_licitacao": False,
            "numero_edital": None,
            "porte": "medio",
            "origem": "comercial",
            "descricao": "PMOC completo"
        }

        descricao = self.asana._formatar_descricao(dados)

        # Verificar campos presentes
        assert "Empresa ABC Ltda" in descricao
        assert "12.345.678/0001-90" in descricao
        assert "João Silva" in descricao
        assert "(11) 98765-4321" in descricao
        assert "PMOC completo" in descricao
        assert "Comercial" in descricao  # origem formatada
        assert "Medio" in descricao or "Médio" in descricao  # porte formatado

    def test_formatar_descricao_minima(self):
        """Deve lidar com dados mínimos."""
        dados = {
            "cliente": "Cliente Teste",
            "local": "Local Teste",
            "tipo_servico": "instalacao",
            "origem": "cliente_direto",
            "descricao": "Teste"
        }

        descricao = self.asana._formatar_descricao(dados)

        assert "Cliente Teste" in descricao
        assert "N/A" in descricao  # Campos ausentes
        assert "Cliente Direto" in descricao  # origem formatada


class TestAsanaLibTags:
    """Testes de determinação de tags."""

    def setup_method(self):
        """Setup para cada teste."""
        self.asana = AsanaLib()

    def test_tags_basicas(self):
        """Deve incluir tags básicas (tipo e porte)."""
        dados = {
            "tipo_servico": "instalacao",
            "porte": "medio",
            "eh_licitacao": False,
            "urgente": False,
            "cliente_estrategico": False
        }

        tags = self.asana._determinar_tags(dados)

        assert "instalacao" in tags
        assert "medio" in tags
        assert len(tags) == 2

    def test_tags_licitacao(self):
        """Deve incluir tag de licitação."""
        dados = {
            "tipo_servico": "projeto",
            "porte": "grande",
            "eh_licitacao": True,
            "urgente": False,
            "cliente_estrategico": False
        }

        tags = self.asana._determinar_tags(dados)

        assert "licitacao" in tags

    def test_tags_urgente(self):
        """Deve incluir tag de urgente."""
        dados = {
            "tipo_servico": "manutencao",
            "porte": None,
            "eh_licitacao": False,
            "urgente": True,
            "cliente_estrategico": False
        }

        tags = self.asana._determinar_tags(dados)

        assert "urgente" in tags

    def test_tags_cliente_estrategico(self):
        """Deve incluir tag de cliente estratégico."""
        dados = {
            "tipo_servico": "instalacao",
            "porte": "grande",
            "eh_licitacao": False,
            "urgente": False,
            "cliente_estrategico": True
        }

        tags = self.asana._determinar_tags(dados)

        assert "cliente-estrategico" in tags

    def test_tags_completas(self):
        """Deve incluir todas as tags quando aplicável."""
        dados = {
            "tipo_servico": "projeto",
            "porte": "grande",
            "eh_licitacao": True,
            "urgente": True,
            "cliente_estrategico": True
        }

        tags = self.asana._determinar_tags(dados)

        assert "projeto" in tags
        assert "grande" in tags
        assert "licitacao" in tags
        assert "urgente" in tags
        assert "cliente-estrategico" in tags
        assert len(tags) == 5


class TestAsanaLibCriarOrcamento:
    """Testes de criação de orçamento."""

    def setup_method(self):
        """Setup para cada teste."""
        self.asana = AsanaLib()

    def test_criar_orcamento_dados_validos(self):
        """Deve criar orçamento com dados válidos."""
        dados = {
            "cliente": "Empresa ABC",
            "local": "São Paulo - SP",
            "tipo_servico": "instalacao",
            "origem": "comercial",
            "descricao": "Instalação de split"
        }

        task_id = self.asana.criar_orcamento(dados)

        # No modo simulação, retorna um ID
        assert task_id is not None
        assert len(task_id) > 0


class TestAsanaLibFechamento:
    """Testes de registro de fechamento."""

    def setup_method(self):
        """Setup para cada teste."""
        self.asana = AsanaLib()

    def test_gerar_comentario_fechado(self):
        """Deve gerar comentário de orçamento fechado."""
        comentario = self.asana._gerar_comentario_fechamento(
            "fechado",
            "R$ 15.000,00",
            None,
            "Cliente aprovou"
        )

        assert "FECHADO" in comentario
        assert "R$ 15.000,00" in comentario
        assert "Cliente aprovou" in comentario
        assert "✅" in comentario

    def test_gerar_comentario_perdido(self):
        """Deve gerar comentário de orçamento perdido."""
        comentario = self.asana._gerar_comentario_fechamento(
            "perdido",
            None,
            "Preço alto",
            "Cliente escolheu concorrente"
        )

        assert "PERDIDO" in comentario
        assert "Preço alto" in comentario
        assert "Cliente escolheu concorrente" in comentario
        assert "❌" in comentario

    def test_registrar_fechamento_fechado(self):
        """Deve registrar fechamento com sucesso."""
        task_id = "test_task_123"

        resultado = self.asana.registrar_fechamento(
            task_id,
            "fechado",
            valor="R$ 10.000,00"
        )

        # Em modo simulação, retorna True
        assert resultado is True

    def test_registrar_fechamento_perdido(self):
        """Deve registrar perda com sucesso."""
        task_id = "test_task_123"

        resultado = self.asana.registrar_fechamento(
            task_id,
            "perdido",
            motivo="Concorrência"
        )

        assert resultado is True


class TestAsanaLibAvancarEtapa:
    """Testes de avanço de etapas."""

    def setup_method(self):
        """Setup para cada teste."""
        self.asana = AsanaLib()

    def test_avancar_etapa_valida(self):
        """Deve avançar etapa válida."""
        task_id = "test_task_123"

        resultado = self.asana.avancar_etapa(task_id, 1)

        assert resultado is True

    def test_avancar_etapa_com_observacao(self):
        """Deve aceitar observação."""
        task_id = "test_task_123"

        resultado = self.asana.avancar_etapa(
            task_id,
            1,
            observacao="Triagem concluída"
        )

        assert resultado is True

    def test_avancar_etapa_invalida_baixa(self):
        """Deve rejeitar etapa < 1."""
        task_id = "test_task_123"

        with pytest.raises(AsanaLibError, match="Etapa inválida"):
            self.asana.avancar_etapa(task_id, 0)

    def test_avancar_etapa_invalida_alta(self):
        """Deve rejeitar etapa > 7."""
        task_id = "test_task_123"

        with pytest.raises(AsanaLibError, match="Etapa inválida"):
            self.asana.avancar_etapa(task_id, 8)


class TestAsanaLibConstantes:
    """Testes de constantes do projeto."""

    def test_subtarefas_padrao_quantidade(self):
        """Deve ter exatamente 7 subtarefas."""
        assert len(SUBTAREFAS_PADRAO) == 7

    def test_subtarefas_padrao_estrutura(self):
        """Cada subtarefa deve ter nome e notes."""
        for subtarefa in SUBTAREFAS_PADRAO:
            assert "nome" in subtarefa
            assert "notes" in subtarefa
            assert len(subtarefa["nome"]) > 0
            assert len(subtarefa["notes"]) > 0

    def test_subtarefas_padrao_ordem(self):
        """Subtarefas devem estar em ordem reversa (7 a 1)."""
        # Primeira subtarefa deve ser a 7
        assert "7." in SUBTAREFAS_PADRAO[0]["nome"]
        assert "Fechamento" in SUBTAREFAS_PADRAO[0]["nome"]

        # Última subtarefa deve ser a 1
        assert "1." in SUBTAREFAS_PADRAO[-1]["nome"]
        assert "Triagem" in SUBTAREFAS_PADRAO[-1]["nome"]


# ===== Testes de Integração (quando MCP/API estiver disponível) =====

@pytest.mark.integration
@pytest.mark.skip(reason="Requer integração com MCP ou API Asana configurada")
class TestAsanaLibIntegration:
    """
    Testes de integração com Asana real.

    Para rodar: pytest tests/test_asana_lib.py -v -m integration
    """

    def setup_method(self):
        """Setup para testes de integração."""
        self.asana = AsanaLib()

    def test_criar_orcamento_real(self):
        """Teste de criação real no Asana."""
        dados = {
            "cliente": "[TESTE] Empresa Teste Ltda",
            "local": "São Paulo - SP",
            "prazo": "2026-12-31",
            "tipo_servico": "instalacao",
            "origem": "comercial",
            "descricao": "Teste automatizado - pode deletar"
        }

        task_id = self.asana.criar_orcamento(dados)

        assert task_id is not None
        print(f"\n✓ Tarefa de teste criada: {task_id}")
        print("ATENÇÃO: Lembre-se de deletar esta tarefa no Asana!")

    def test_buscar_tarefas_real(self):
        """Teste de busca real de tarefas."""
        tarefas = self.asana.buscar_tarefas({
            "completed": False
        })

        assert isinstance(tarefas, list)
        if tarefas:
            print(f"\n✓ Encontradas {len(tarefas)} tarefas em andamento")
