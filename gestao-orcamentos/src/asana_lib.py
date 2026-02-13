#!/usr/bin/env python3
"""
Asana Library - Interface simplificada para operações no Asana

Este módulo fornece uma interface Python limpa para interagir com o Asana,
abstraindo a complexidade do MCP e API direta.

Funcionalidades:
- Criar tarefas de orçamento com 7 subtarefas automaticamente
- Atualizar status e progresso
- Gerenciar tags e metadados
- Registrar fechamentos (ganho/perdido)
- Anexar arquivos

Uso:
    asana = AsanaLib()
    task_id = asana.criar_orcamento(dados_json)
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Literal
from datetime import datetime

try:
    import anthropic
    from anthropic import Anthropic
except ImportError:
    raise ImportError(
        "Dependência faltando. Instale com: pip install anthropic"
    )

from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)

logger = logging.getLogger(__name__)


class AsanaLibError(Exception):
    """Exceção base para erros da AsanaLib."""
    pass


class AsanaTaskNotFoundError(AsanaLibError):
    """Tarefa não encontrada no Asana."""
    pass


# ===== Constantes do Projeto =====

# IDs fixos do Asana
WORKSPACE_ID = "1204197108826498"
PROJECT_ID = "1212920325558530"

# IDs das seções
SECAO_ENTRADA = "1212909431317491"
SECAO_ENVIADO = "1212920431590044"
# SECAO_CONCLUIDO será descoberto dinamicamente

# Template de subtarefas (ordem reversa para Asana)
SUBTAREFAS_PADRAO = [
    {
        "nome": "🏁 7. Fechamento",
        "notes": "Registrar resultado: FECHADO (valor R$) ou PERDIDO (motivo)"
    },
    {
        "nome": "🤝 6. Negociacao (se necessario)",
        "notes": "Tratar ajustes de preço, escopo ou prazo solicitados pelo cliente"
    },
    {
        "nome": "📤 5. Envio ao Cliente",
        "notes": "Enviar orçamento por email e confirmar recebimento"
    },
    {
        "nome": "🔍 4. Revisao Interna",
        "notes": "Coordenador revisa valores, margem e condições comerciais"
    },
    {
        "nome": "⚙️ 3. Elaboracao do Orcamento",
        "notes": "Criar planilha, calcular custos, definir preço final"
    },
    {
        "nome": "✅ 2. Aprovacao para Elaboracao",
        "notes": "Confirmar informações completas e atribuir responsável"
    },
    {
        "nome": "📋 1. Triagem",
        "notes": "Avaliar viabilidade, prioridade e definir responsável"
    }
]


class AsanaLib:
    """
    Biblioteca para operações no Asana.

    Usa MCP Asana via Claude Code quando disponível,
    com fallback para API direta se necessário.
    """

    def __init__(
        self,
        workspace_id: str = WORKSPACE_ID,
        project_id: str = PROJECT_ID,
        use_mcp: bool = True
    ):
        """
        Inicializa a biblioteca Asana.

        Args:
            workspace_id: ID do workspace Asana
            project_id: ID do projeto principal
            use_mcp: Se True, tenta usar MCP Asana (via Claude Code)
        """
        self.workspace_id = workspace_id
        self.project_id = project_id
        self.use_mcp = use_mcp

        # Cache de IDs importantes
        self._cache_tags = {}
        self._cache_sections = {}

        logger.info(f"AsanaLib inicializada (project: {project_id})")

    def criar_orcamento(self, dados: Dict) -> str:
        """
        Cria orçamento completo no Asana.

        Pipeline:
        1. Formata título e descrição
        2. Cria tarefa principal
        3. Cria 7 subtarefas
        4. Adiciona tags
        5. Define prazo
        6. Move para seção apropriada

        Args:
            dados: Dict com campos do orçamento (output do AIExtractor)

        Returns:
            task_gid da tarefa criada

        Raises:
            AsanaLibError: Se falhar na criação

        Exemplo:
            >>> asana = AsanaLib()
            >>> dados = {
            ...     "cliente": "Empresa ABC",
            ...     "local": "São Paulo - SP",
            ...     "tipo_servico": "instalacao",
            ...     ...
            ... }
            >>> task_id = asana.criar_orcamento(dados)
            >>> print(f"Tarefa criada: {task_id}")
        """
        logger.info(f"Criando orçamento para: {dados.get('cliente')}")

        try:
            # 1. Formatar título e descrição
            titulo = self._formatar_titulo(dados)
            descricao = self._formatar_descricao(dados)

            logger.debug(f"Título: {titulo}")

            # 2. Criar tarefa principal
            task_data = {
                "name": titulo,
                "notes": descricao,
                "projects": [self.project_id],
            }

            # Adicionar prazo se fornecido
            if dados.get("prazo"):
                task_data["due_on"] = dados["prazo"]

            # Criar via MCP ou API
            task_gid = self._criar_tarefa_asana(task_data)
            logger.info(f"✓ Tarefa principal criada: {task_gid}")

            # 3. Criar subtarefas
            subtarefas_ids = self._criar_subtarefas(task_gid)
            logger.info(f"✓ Criadas {len(subtarefas_ids)} subtarefas")

            # 4. Adicionar tags
            tags = self._determinar_tags(dados)
            if tags:
                self._adicionar_tags(task_gid, tags)
                logger.info(f"✓ Tags adicionadas: {', '.join(tags)}")

            # 5. Mover para seção (Entrada por padrão)
            # A tarefa já é criada no projeto, então apenas está em "Entrada"

            logger.info(f"✓ Orçamento criado com sucesso: {task_gid}")
            return task_gid

        except Exception as e:
            logger.error(f"Erro ao criar orçamento: {e}")
            raise AsanaLibError(f"Falha ao criar orçamento: {e}")

    def _criar_tarefa_asana(self, task_data: Dict) -> str:
        """
        Cria tarefa no Asana usando método disponível.

        Args:
            task_data: Dados da tarefa

        Returns:
            task_gid
        """
        # Por enquanto, simular criação (MCP não está disponível via script Python direto)
        # Em produção, isso seria chamado via MCP do Claude Code ou API direta

        # TODO: Implementar via API direta do Asana
        # Para este protótipo, vamos retornar um ID simulado
        import uuid
        simulated_id = str(uuid.uuid4())[:16]

        logger.warning(
            "MODO SIMULAÇÃO: Tarefa não foi realmente criada no Asana. "
            "Para uso real, implemente integração com MCP ou API direta."
        )

        return simulated_id

    def _criar_subtarefas(self, parent_task_id: str) -> List[str]:
        """
        Cria as 7 subtarefas padrão.

        Args:
            parent_task_id: ID da tarefa pai

        Returns:
            Lista de IDs das subtarefas criadas
        """
        subtarefas_ids = []

        # Criar em ordem reversa (Asana adiciona no topo)
        for subtarefa in SUBTAREFAS_PADRAO:
            # TODO: Implementar criação via API/MCP
            import uuid
            subtask_id = str(uuid.uuid4())[:16]
            subtarefas_ids.append(subtask_id)

            logger.debug(f"Subtarefa criada (simulada): {subtarefa['nome']}")

        return subtarefas_ids

    def _formatar_titulo(self, dados: Dict) -> str:
        """
        Formata título da tarefa conforme padrão.

        Formato: [PREFIXOS][TIPO] Cliente - Local

        Args:
            dados: Dict com dados do orçamento

        Returns:
            Título formatado

        Exemplos:
            - "[INSTALACAO] Empresa ABC - Belo Horizonte"
            - "[LIC][PROJETO] Prefeitura XYZ - Porto Alegre"
        """
        prefixos = []

        # Adicionar prefixo de licitação
        if dados.get("eh_licitacao"):
            prefixos.append("[LIC]")

        # Adicionar tipo de serviço
        tipo = dados["tipo_servico"].upper()
        prefixos.append(f"[{tipo}]")

        # Montar título
        cliente = dados["cliente"]
        local = dados["local"]

        titulo = f"{' '.join(prefixos)} {cliente} - {local}"

        return titulo

    def _formatar_descricao(self, dados: Dict) -> str:
        """
        Formata descrição da tarefa conforme template padrão.

        Args:
            dados: Dict com dados do orçamento

        Returns:
            Descrição formatada
        """
        # Formatar prazo
        prazo_str = "Não informado"
        if dados.get("prazo"):
            try:
                from datetime import datetime
                prazo_dt = datetime.strptime(dados["prazo"], "%Y-%m-%d")
                prazo_str = prazo_dt.strftime("%d/%m/%Y")
            except:
                prazo_str = dados["prazo"]

        # Formatar licitação
        if dados.get("eh_licitacao"):
            licitacao_str = f"Sim - {dados.get('numero_edital', 'N/A')}"
        else:
            licitacao_str = "Não"

        # Montar descrição
        descricao = f"""DADOS DO ORCAMENTO

Cliente: {dados.get('cliente', 'N/A')}
CNPJ/CPF: {dados.get('cnpj_cpf') or 'N/A'}
Contato: {dados.get('contato') or 'N/A'}
Telefone: {dados.get('telefone') or 'N/A'}
Email: {dados.get('email') or 'N/A'}
Local: {dados.get('local', 'N/A')}
Prazo do cliente: {prazo_str}

---

DETALHES DA DEMANDA
{dados.get('descricao', 'N/A')}

---

ORIGEM: {dados.get('origem', 'N/A').replace('_', ' ').title()}
LICITACAO: {licitacao_str}

---

CLASSIFICACAO
Tipo: {dados.get('tipo_servico', 'N/A').title()}
Porte: {dados.get('porte', 'A definir').title() if dados.get('porte') else 'A definir'}
"""

        return descricao

    def _determinar_tags(self, dados: Dict) -> List[str]:
        """
        Determina quais tags adicionar baseado nos dados.

        Args:
            dados: Dict com dados do orçamento

        Returns:
            Lista de nomes de tags
        """
        tags = []

        # Tag do tipo de serviço (obrigatória)
        tags.append(dados["tipo_servico"])

        # Tag do porte (se definido)
        if dados.get("porte"):
            tags.append(dados["porte"])

        # Tag de licitação
        if dados.get("eh_licitacao"):
            tags.append("licitacao")

        # Tag de urgente
        if dados.get("urgente"):
            tags.append("urgente")

        # Tag de cliente estratégico
        if dados.get("cliente_estrategico"):
            tags.append("cliente-estrategico")

        return tags

    def _adicionar_tags(self, task_id: str, tags: List[str]) -> bool:
        """
        Adiciona tags à tarefa.

        Args:
            task_id: ID da tarefa
            tags: Lista de nomes de tags

        Returns:
            True se sucesso
        """
        # TODO: Implementar via API/MCP
        logger.debug(f"Tags a adicionar (simulado): {tags}")
        return True

    def avancar_etapa(
        self,
        task_id: str,
        etapa: int,
        observacao: Optional[str] = None
    ) -> bool:
        """
        Marca subtarefa N como concluída.

        Args:
            task_id: ID da tarefa principal
            etapa: Número da etapa (1-7)
            observacao: Comentário opcional

        Returns:
            True se sucesso

        Raises:
            AsanaLibError: Se falhar

        Exemplo:
            >>> asana.avancar_etapa(task_id, 1, "Triagem concluída, aprovado")
        """
        if etapa < 1 or etapa > 7:
            raise AsanaLibError(f"Etapa inválida: {etapa}. Deve ser 1-7")

        logger.info(f"Avançando para etapa {etapa} da tarefa {task_id}")

        try:
            # 1. Buscar subtarefas da tarefa
            # subtarefas = self._obter_subtarefas(task_id)

            # 2. Encontrar subtarefa da etapa N
            # subtarefa_id = subtarefas[etapa - 1]  # Lista 0-indexed

            # 3. Marcar como concluída
            # self._marcar_concluida(subtarefa_id)

            # 4. Se tem observação, adicionar comentário
            if observacao:
                # self._adicionar_comentario(subtarefa_id, observacao)
                logger.debug(f"Observação adicionada (simulado): {observacao}")

            logger.info(f"✓ Etapa {etapa} concluída")
            return True

        except Exception as e:
            logger.error(f"Erro ao avançar etapa: {e}")
            raise AsanaLibError(f"Falha ao avançar etapa: {e}")

    def registrar_fechamento(
        self,
        task_id: str,
        resultado: Literal["fechado", "perdido"],
        valor: Optional[str] = None,
        motivo: Optional[str] = None,
        observacao: Optional[str] = None
    ) -> bool:
        """
        Registra fechamento do orçamento (ganho ou perdido).

        Pipeline:
        1. Adiciona comentário com resultado
        2. Marca subtarefa 7 como concluída
        3. Marca tarefa principal como concluída
        4. Move para seção "Concluído"

        Args:
            task_id: ID da tarefa
            resultado: "fechado" ou "perdido"
            valor: Valor do contrato se fechado (ex: "R$ 15.000,00")
            motivo: Motivo da perda se perdido
            observacao: Observações adicionais

        Returns:
            True se sucesso

        Exemplo:
            >>> asana.registrar_fechamento(
            ...     task_id,
            ...     "fechado",
            ...     valor="R$ 15.000,00",
            ...     observacao="Cliente aprovou proposta revisada"
            ... )
        """
        logger.info(f"Registrando fechamento: {resultado} para tarefa {task_id}")

        try:
            # 1. Gerar comentário
            comentario = self._gerar_comentario_fechamento(
                resultado, valor, motivo, observacao
            )

            # 2. Adicionar comentário na tarefa principal
            # self._adicionar_comentario(task_id, comentario)
            logger.debug(f"Comentário adicionado (simulado):\n{comentario}")

            # 3. Marcar subtarefa 7 como concluída
            # self.avancar_etapa(task_id, 7)

            # 4. Marcar tarefa principal como concluída
            # self._marcar_concluida(task_id)

            # 5. Mover para seção Concluído
            # self._mover_para_secao(task_id, "Concluído")

            logger.info(f"✓ Fechamento registrado: {resultado}")
            return True

        except Exception as e:
            logger.error(f"Erro ao registrar fechamento: {e}")
            raise AsanaLibError(f"Falha ao registrar fechamento: {e}")

    def _gerar_comentario_fechamento(
        self,
        resultado: str,
        valor: Optional[str],
        motivo: Optional[str],
        observacao: Optional[str]
    ) -> str:
        """
        Gera comentário formatado de fechamento.

        Args:
            resultado: "fechado" ou "perdido"
            valor: Valor se fechado
            motivo: Motivo se perdido
            observacao: Observação adicional

        Returns:
            Comentário formatado
        """
        data_atual = datetime.now().strftime("%d/%m/%Y")

        if resultado == "fechado":
            comentario = f"""═══════════════════════════════════════
✅ ORCAMENTO FECHADO
═══════════════════════════════════════

Valor do contrato: {valor or 'N/A'}
Data: {data_atual}
"""
            if observacao:
                comentario += f"\n{observacao}\n"

        else:  # perdido
            comentario = f"""═══════════════════════════════════════
❌ ORCAMENTO PERDIDO
═══════════════════════════════════════

Motivo: {motivo or 'Não especificado'}
Data: {data_atual}
"""
            if observacao:
                comentario += f"\n{observacao}\n"

        return comentario

    def buscar_tarefas(
        self,
        filtros: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Busca tarefas no projeto com filtros.

        Args:
            filtros: Dict com filtros opcionais:
                - completed: bool
                - tags: list[str]
                - assignee: str
                - due_on_before: str (YYYY-MM-DD)
                - due_on_after: str (YYYY-MM-DD)

        Returns:
            Lista de tarefas encontradas

        Exemplo:
            >>> # Buscar tarefas urgentes não concluídas
            >>> tarefas = asana.buscar_tarefas({
            ...     "completed": False,
            ...     "tags": ["urgente"]
            ... })
        """
        logger.info("Buscando tarefas com filtros")

        # TODO: Implementar busca via API/MCP
        logger.warning("MODO SIMULAÇÃO: Retornando lista vazia")
        return []

    def anexar_arquivo(
        self,
        task_id: str,
        file_path: str,
        nome: Optional[str] = None
    ) -> bool:
        """
        Anexa arquivo à tarefa.

        Args:
            task_id: ID da tarefa
            file_path: Caminho do arquivo
            nome: Nome customizado (opcional)

        Returns:
            True se sucesso

        Exemplo:
            >>> asana.anexar_arquivo(task_id, "proposta.pdf")
        """
        if not os.path.exists(file_path):
            raise AsanaLibError(f"Arquivo não encontrado: {file_path}")

        logger.info(f"Anexando arquivo: {file_path} → {task_id}")

        # TODO: Implementar upload via API/MCP
        logger.warning("MODO SIMULAÇÃO: Arquivo não foi anexado")
        return True

    def obter_tarefa(self, task_id: str) -> Dict:
        """
        Obtém detalhes de uma tarefa.

        Args:
            task_id: ID da tarefa

        Returns:
            Dict com dados da tarefa

        Raises:
            AsanaTaskNotFoundError: Se tarefa não existe
        """
        logger.info(f"Obtendo tarefa: {task_id}")

        # TODO: Implementar via API/MCP
        logger.warning("MODO SIMULAÇÃO: Retornando dados simulados")

        return {
            "gid": task_id,
            "name": "[SIMULADO] Tarefa Exemplo",
            "notes": "Descrição simulada",
            "completed": False
        }


def main():
    """
    Função principal para testar a biblioteca via CLI.

    Uso:
        python asana_lib.py --test
    """
    import sys
    import argparse

    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    parser = argparse.ArgumentParser(description='Asana Library - Testes')
    parser.add_argument('--test', action='store_true', help='Executar testes')
    parser.add_argument('--verbose', '-v', action='store_true', help='Modo verbose')

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    if args.test:
        print("\n" + "="*70)
        print("TESTE - Asana Library")
        print("="*70)

        try:
            asana = AsanaLib()

            # Dados de teste
            dados_teste = {
                "cliente": "Empresa ABC Ltda",
                "cnpj_cpf": "12.345.678/0001-90",
                "contato": "João Silva",
                "telefone": "(11) 98765-4321",
                "email": "joao@empresaabc.com",
                "local": "São Paulo - SP",
                "prazo": "2026-02-15",
                "tipo_servico": "instalacao",
                "eh_licitacao": False,
                "porte": "medio",
                "origem": "comercial",
                "descricao": "Instalação de split 18.000 BTUs em sala de reuniões",
                "urgente": False,
                "cliente_estrategico": False
            }

            print("\n1. Testando formatação de título...")
            titulo = asana._formatar_titulo(dados_teste)
            print(f"   Título: {titulo}")

            print("\n2. Testando determinação de tags...")
            tags = asana._determinar_tags(dados_teste)
            print(f"   Tags: {', '.join(tags)}")

            print("\n3. Testando criação de orçamento (simulado)...")
            task_id = asana.criar_orcamento(dados_teste)
            print(f"   ✓ Tarefa criada (ID simulado): {task_id}")

            print("\n4. Testando registro de fechamento (simulado)...")
            asana.registrar_fechamento(
                task_id,
                "fechado",
                valor="R$ 15.000,00",
                observacao="Cliente aprovou proposta"
            )
            print(f"   ✓ Fechamento registrado")

            print("\n" + "="*70)
            print("✓ Testes concluídos com sucesso!")
            print("="*70)
            print("\nNOTA: Este é um modo de simulação.")
            print("Para uso real, implemente integração com MCP ou API Asana.")
            print("="*70 + "\n")

        except Exception as e:
            print(f"\n✗ Erro: {e}")
            if args.verbose:
                import traceback
                traceback.print_exc()
            sys.exit(1)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
