#!/usr/bin/env python3
"""
Preparador de Atualizações para o Asana

Lê os resultados das pesquisas no Gmail e gera um plano de atualização
formatado para ser executado via MCP Asana pelo Claude Code.

A execução real é feita via MCP Asana (interativo), não por API direta.
Motivo: o Asana tem uso ativo (criar, inserir, validar) onde o MCP
é mais adequado que scripts automatizados.

Uso:
    python scripts/atualizar_asana.py                    # Gera plano completo
    python scripts/atualizar_asana.py --id 26_049         # Uma específica
    python scripts/atualizar_asana.py --apenas-novos      # Apenas não atualizados
"""

import json
import logging
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

# Caminhos
BASE_DIR = Path(__file__).parent.parent
RESULTADOS_FILE = BASE_DIR / "gemini-tasks" / "resultados-pesquisa-gmail.json"
PLANO_FILE = BASE_DIR / "plano-atualizacao-asana.json"


class PreparadorAsana:
    """Prepara plano de atualização para execução via MCP Asana."""

    def carregar_resultados(self, demanda_id: Optional[str] = None) -> List[Dict]:
        """Carrega resultados da pesquisa Gmail."""
        with open(RESULTADOS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)

        resultados = data.get('resultados', [])

        # Filtrar por ID
        if demanda_id:
            resultados = [r for r in resultados if r.get('asana_id') == demanda_id]

        # Filtrar apenas com dados úteis
        resultados = [r for r in resultados
                      if r.get('status') in ('encontrado', 'parcial')]

        return resultados

    def formatar_notas(self, resultado: Dict) -> str:
        """
        Formata notas no padrão Asana.

        Segue o padrão documentado no CLAUDE.md:
        - Seções em CAPS com separadores (═══ e ---)
        - Campos no formato: Campo: Valor
        - NÃO usar markdown bold
        """
        dados = resultado.get('dados', {})

        linhas = []
        linhas.append("")
        linhas.append("═══════════════════════════════════")
        linhas.append("DADOS EXTRAIDOS DO GMAIL")
        linhas.append("═══════════════════════════════════")
        linhas.append(f"Atualizado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        linhas.append("")

        # Campos principais
        campos = [
            ("Cliente", dados.get('cliente')),
            ("CNPJ", dados.get('cnpj')),
            ("Contato", dados.get('contato_nome')),
            ("Telefone", dados.get('contato_telefone')),
            ("Email", dados.get('contato_email')),
            ("Endereco", dados.get('endereco')),
            ("Local do Servico", dados.get('local_servico')),
            ("Tipo de Servico", dados.get('tipo_servico')),
            ("Detalhes", dados.get('detalhes')),
            ("Prazo", dados.get('prazo')),
            ("Porte", dados.get('porte')),
            ("Origem", dados.get('origem')),
            ("Licitacao", dados.get('licitacao')),
        ]

        for nome, valor in campos:
            if valor:
                linhas.append(f"{nome}: {valor}")

        # Observações
        if dados.get('observacoes'):
            linhas.append("")
            linhas.append("-------------------")
            linhas.append("OBSERVACOES")
            linhas.append("-------------------")
            linhas.append(dados['observacoes'])

        # Fontes dos emails
        emails_fonte = resultado.get('emails_fonte', [])
        if emails_fonte:
            linhas.append("")
            linhas.append("-------------------")
            linhas.append("EMAILS FONTE")
            linhas.append("-------------------")
            for ef in emails_fonte[:3]:
                linhas.append(f"- {ef.get('assunto', 'N/A')}")
                linhas.append(f"  De: {ef.get('de', 'N/A')}")
                linhas.append(f"  Data: {ef.get('data', 'N/A')}")

        # Campos não encontrados
        nao_encontrados = resultado.get('campos_nao_encontrados', [])
        if nao_encontrados:
            linhas.append("")
            linhas.append("-------------------")
            linhas.append("CAMPOS NAO ENCONTRADOS")
            linhas.append("-------------------")
            linhas.append(', '.join(nao_encontrados))

        return '\n'.join(linhas)

    def gerar_plano(self, resultados: List[Dict]) -> List[Dict]:
        """
        Gera plano de atualização para execução via MCP.

        Cada item do plano contém:
        - asana_id: ID da demanda
        - notas_formatadas: Texto pronto para inserir no Asana
        - campos_encontrados/faltando: Resumo dos dados
        """
        plano = []

        for resultado in resultados:
            asana_id = resultado.get('asana_id', '')
            dados = resultado.get('dados', {})
            notas = self.formatar_notas(resultado)

            atualizacao = {
                "asana_id": asana_id,
                "task_id": resultado.get('task_id', ''),
                "status_pesquisa": resultado.get('status', ''),
                "campos_encontrados": [k for k, v in dados.items() if v],
                "campos_faltando": resultado.get('campos_nao_encontrados', []),
                "notas_formatadas": notas,
                "acao": "atualizar_notas_via_mcp"
            }

            plano.append(atualizacao)

        return plano

    def processar(
        self,
        demanda_id: Optional[str] = None,
        apenas_novos: bool = False
    ):
        """Gera plano de atualização."""
        resultados = self.carregar_resultados(demanda_id)

        if not resultados:
            print("Nenhum resultado para processar.")
            return

        print("="*60)
        print(f"  PLANO DE ATUALIZAÇÃO ASANA - {len(resultados)} tarefas")
        print("="*60)
        print("  Modo: PLANO (execução via MCP Asana no Claude Code)")

        plano = self.gerar_plano(resultados)

        # Salvar plano
        with open(PLANO_FILE, 'w', encoding='utf-8') as f:
            json.dump(plano, f, indent=2, ensure_ascii=False)

        # Mostrar preview
        for item in plano:
            print(f"\n{'─'*60}")
            print(f"  {item['asana_id']} ({item['status_pesquisa']})")
            print(f"  Campos encontrados: {', '.join(item['campos_encontrados'][:5])}")
            if item['campos_faltando']:
                print(f"  Campos faltando: {', '.join(item['campos_faltando'][:5])}")
            print(f"{'─'*60}")
            # Preview das notas (primeiras 8 linhas)
            notas_preview = item['notas_formatadas'].split('\n')[:8]
            for linha in notas_preview:
                print(f"  | {linha}")
            if len(item['notas_formatadas'].split('\n')) > 8:
                print(f"  | ...")

        print(f"\n{'='*60}")
        print(f"  Plano salvo em: {PLANO_FILE}")
        print(f"")
        print(f"  Para executar, peça ao Claude Code:")
        print(f"  'Atualize as tarefas no Asana conforme plano-atualizacao-asana.json'")
        print(f"{'='*60}")


def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    parser = argparse.ArgumentParser(
        description='Preparador de Atualizações para o Asana (via MCP)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python scripts/atualizar_asana.py                    # Plano completo
  python scripts/atualizar_asana.py --id 26_049         # Uma específica
  python scripts/atualizar_asana.py --apenas-novos      # Apenas novos

Execução:
  O plano gerado deve ser executado via MCP Asana no Claude Code.
  Peça: "Atualize as tarefas no Asana conforme plano-atualizacao-asana.json"
        """
    )
    parser.add_argument('--id', type=str,
                        help='ID da demanda específica (ex: 26_049)')
    parser.add_argument('--apenas-novos', action='store_true',
                        help='Processar apenas resultados não atualizados')

    args = parser.parse_args()

    preparador = PreparadorAsana()
    preparador.processar(
        demanda_id=args.id,
        apenas_novos=args.apenas_novos
    )


if __name__ == '__main__':
    main()
