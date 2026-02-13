#!/usr/bin/env python3
"""
Scheduler para Automação de Processamento

Processa automaticamente novas demandas em horários agendados.

IMPORTANTE: Este script está pronto mas NÃO ATIVO por padrão.
Para ativar, configure cron job conforme automation/README.md

Uso:
    # Processar novas demandas
    python automation/scheduler.py processar-novas

    # Sincronizar Drive
    python automation/scheduler.py sync-drive

    # Verificar emails
    python automation/scheduler.py verificar-emails

    # Job completo (processar + sync)
    python automation/scheduler.py job-completo
"""

import argparse
import json
import logging
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from cli import OrcamentoCLI
from sync_drive import DriveSync
from gmail_client import GmailClient


# Configuração de logging
LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / f"scheduler_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class Scheduler:
    """Scheduler para automação de processamentos."""

    def __init__(self, config_file: str = "automation/config.json"):
        """
        Inicializa scheduler.

        Args:
            config_file: Arquivo de configuração
        """
        self.config_file = Path(config_file)
        self.config = self._carregar_config()

        self.cli = OrcamentoCLI(
            verbose=self.config.get('verbose', False),
            dry_run=self.config.get('dry_run', False)
        )

        self.sync = DriveSync()
        self.gmail_client = None

        logger.info("Scheduler inicializado")

    def _carregar_config(self) -> Dict:
        """Carrega configuração."""
        if not self.config_file.exists():
            logger.warning(f"Config não encontrado: {self.config_file}")
            return self._config_padrao()

        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            logger.info("Configuração carregada")
            return config
        except Exception as e:
            logger.error(f"Erro ao carregar config: {e}")
            return self._config_padrao()

    def _config_padrao(self) -> Dict:
        """Configuração padrão."""
        return {
            'dry_run': False,
            'verbose': False,
            'processar_automatico': True,
            'max_demandas_por_vez': 5,
            'horarios_processamento': ['09:00', '14:00', '17:00'],
            'notificar_email': False,
            'email_destino': 'orcamentos2@armant.com.br'
        }

    def processar_novas_demandas(self) -> Dict:
        """
        Processa demandas que ainda não foram processadas.

        Returns:
            Estatísticas do processamento
        """
        logger.info("\n" + "="*60)
        logger.info("Processando novas demandas")
        logger.info("="*60 + "\n")

        stats = {
            'inicio': datetime.now(),
            'demandas_encontradas': 0,
            'demandas_processadas': 0,
            'erros': 0,
            'tarefas_criadas': []
        }

        try:
            # Listar pastas no Drive
            pastas = self.sync.listar_pastas_drive()
            stats['demandas_encontradas'] = len(pastas)

            logger.info(f"Encontradas {len(pastas)} pastas no Drive")

            # Filtrar pastas não mapeadas (não processadas)
            nao_processadas = []

            for pasta_id, path in pastas:
                if not self.sync.obter_task_gid(pasta_id):
                    nao_processadas.append(pasta_id)

            logger.info(f"Novas demandas: {len(nao_processadas)}")

            if not nao_processadas:
                logger.info("✓ Nenhuma demanda nova")
                return stats

            # Limitar quantidade
            max_demandas = self.config.get('max_demandas_por_vez', 5)
            a_processar = nao_processadas[:max_demandas]

            logger.info(f"Processando {len(a_processar)} demandas...")

            # Processar cada demanda
            for pasta_id in a_processar:
                try:
                    logger.info(f"\nProcessando: {pasta_id}")

                    sucesso = self.cli.processar_pasta(
                        pasta_id,
                        confirm=False  # Automático, sem confirmação
                    )

                    if sucesso:
                        stats['demandas_processadas'] += 1

                        # Obter task_id do último processamento
                        task_id = self.cli.stats.get('tarefa_criada')
                        if task_id:
                            stats['tarefas_criadas'].append({
                                'pasta_id': pasta_id,
                                'task_id': task_id
                            })

                        logger.info(f"✓ {pasta_id} processado")
                    else:
                        stats['erros'] += 1
                        logger.error(f"✗ Falha ao processar {pasta_id}")

                except Exception as e:
                    stats['erros'] += 1
                    logger.error(f"✗ Erro em {pasta_id}: {e}")

            # Resumo
            duracao = (datetime.now() - stats['inicio']).total_seconds()

            logger.info("\n" + "="*60)
            logger.info("Processamento concluído")
            logger.info("="*60)
            logger.info(f"Duração: {duracao:.1f}s")
            logger.info(f"Processadas: {stats['demandas_processadas']}/{len(a_processar)}")
            logger.info(f"Erros: {stats['erros']}")

            return stats

        except Exception as e:
            logger.error(f"Erro no processamento: {e}", exc_info=True)
            stats['erros'] += 1
            return stats

    def sincronizar_drive(self) -> Dict:
        """
        Sincroniza Drive → Asana.

        Returns:
            Estatísticas da sincronização
        """
        logger.info("\n" + "="*60)
        logger.info("Sincronizando Drive → Asana")
        logger.info("="*60 + "\n")

        try:
            stats = self.sync.sincronizar_todas()

            logger.info("\n✓ Sincronização concluída")
            logger.info(f"  {stats['total_pdfs_anexados']} PDFs anexados")

            return stats

        except Exception as e:
            logger.error(f"Erro na sincronização: {e}", exc_info=True)
            return {'erros': 1}

    def verificar_emails_novos(self, dias: int = 1) -> List[Dict]:
        """
        Verifica emails novos.

        Args:
            dias: Quantos dias atrás verificar

        Returns:
            Lista de emails encontrados
        """
        logger.info("\n" + "="*60)
        logger.info(f"Verificando emails dos últimos {dias} dias")
        logger.info("="*60 + "\n")

        try:
            if not self.gmail_client:
                self.gmail_client = GmailClient()
                if not self.gmail_client.authenticate():
                    logger.error("Falha na autenticação Gmail")
                    return []

            # Query para emails recentes
            data_inicio = (datetime.now() - timedelta(days=dias)).strftime('%Y/%m/%d')
            query = f"orçamento OR orcamento after:{data_inicio}"

            emails = self.gmail_client.buscar_emails(query, max_results=20)

            logger.info(f"✓ {len(emails)} emails encontrados")

            for i, email in enumerate(emails[:5], 1):
                logger.info(f"  {i}. {email.get('subject', 'Sem assunto')[:50]}")

            return emails

        except Exception as e:
            logger.error(f"Erro ao verificar emails: {e}")
            return []

    def job_completo(self) -> Dict:
        """
        Executa job completo: processar + sincronizar.

        Returns:
            Estatísticas consolidadas
        """
        logger.info("\n" + "="*80)
        logger.info("JOB COMPLETO - Processamento + Sincronização")
        logger.info("="*80 + "\n")

        inicio = datetime.now()

        # 1. Processar novas
        logger.info("\n### ETAPA 1: Processar Novas Demandas ###\n")
        stats_processar = self.processar_novas_demandas()

        # 2. Sincronizar Drive
        logger.info("\n### ETAPA 2: Sincronizar Drive ###\n")
        stats_sync = self.sincronizar_drive()

        # 3. Verificar emails
        logger.info("\n### ETAPA 3: Verificar Emails ###\n")
        emails = self.verificar_emails_novos()

        # Resumo consolidado
        duracao_total = (datetime.now() - inicio).total_seconds()

        logger.info("\n" + "="*80)
        logger.info("JOB COMPLETO FINALIZADO")
        logger.info("="*80)
        logger.info(f"Duração total: {duracao_total:.1f}s")
        logger.info(f"Demandas processadas: {stats_processar.get('demandas_processadas', 0)}")
        logger.info(f"PDFs anexados: {stats_sync.get('total_pdfs_anexados', 0)}")
        logger.info(f"Emails verificados: {len(emails)}")
        logger.info("="*80 + "\n")

        return {
            'duracao_total': duracao_total,
            'processar': stats_processar,
            'sync': stats_sync,
            'emails': len(emails)
        }

    def gerar_relatorio(self, stats: Dict) -> str:
        """
        Gera relatório do processamento.

        Args:
            stats: Estatísticas do processamento

        Returns:
            Texto do relatório
        """
        relatorio = []
        relatorio.append("=" * 60)
        relatorio.append("RELATÓRIO DE PROCESSAMENTO AUTOMÁTICO")
        relatorio.append("=" * 60)
        relatorio.append(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        relatorio.append("")

        if 'processar' in stats:
            p = stats['processar']
            relatorio.append("PROCESSAMENTO DE DEMANDAS:")
            relatorio.append(f"  - Encontradas: {p.get('demandas_encontradas', 0)}")
            relatorio.append(f"  - Processadas: {p.get('demandas_processadas', 0)}")
            relatorio.append(f"  - Erros: {p.get('erros', 0)}")
            relatorio.append("")

        if 'sync' in stats:
            s = stats['sync']
            relatorio.append("SINCRONIZAÇÃO DRIVE:")
            relatorio.append(f"  - Total demandas: {s.get('total_demandas', 0)}")
            relatorio.append(f"  - PDFs anexados: {s.get('total_pdfs_anexados', 0)}")
            relatorio.append("")

        if 'emails' in stats:
            relatorio.append("VERIFICAÇÃO DE EMAILS:")
            relatorio.append(f"  - Emails novos: {stats['emails']}")
            relatorio.append("")

        relatorio.append(f"Duração total: {stats.get('duracao_total', 0):.1f}s")
        relatorio.append("=" * 60)

        return "\n".join(relatorio)


def main():
    """Função principal."""
    parser = argparse.ArgumentParser(
        description='Scheduler para Automação de Processamento',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  # Processar novas demandas
  %(prog)s processar-novas

  # Sincronizar Drive
  %(prog)s sync-drive

  # Verificar emails
  %(prog)s verificar-emails --dias 2

  # Job completo
  %(prog)s job-completo

Configuração de Cron:
  # Processar novas demandas 3x por dia (9h, 14h, 17h)
  0 9,14,17 * * * cd /path/to/projeto && python automation/scheduler.py job-completo

  # Sincronizar Drive a cada hora
  0 * * * * cd /path/to/projeto && python automation/scheduler.py sync-drive
        """
    )

    parser.add_argument('command',
                       choices=['processar-novas', 'sync-drive', 'verificar-emails', 'job-completo'],
                       help='Comando a executar')
    parser.add_argument('--dias', type=int, default=1,
                       help='Dias atrás para verificar emails (padrão: 1)')
    parser.add_argument('--config', default='automation/config.json',
                       help='Arquivo de configuração')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Log detalhado')

    args = parser.parse_args()

    # Configurar logging
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Criar scheduler
    scheduler = Scheduler(config_file=args.config)

    try:
        if args.command == 'processar-novas':
            stats = scheduler.processar_novas_demandas()
            relatorio = scheduler.gerar_relatorio({'processar': stats})
            print("\n" + relatorio)

        elif args.command == 'sync-drive':
            stats = scheduler.sincronizar_drive()
            relatorio = scheduler.gerar_relatorio({'sync': stats})
            print("\n" + relatorio)

        elif args.command == 'verificar-emails':
            emails = scheduler.verificar_emails_novos(dias=args.dias)
            relatorio = scheduler.gerar_relatorio({'emails': len(emails)})
            print("\n" + relatorio)

        elif args.command == 'job-completo':
            stats = scheduler.job_completo()
            relatorio = scheduler.gerar_relatorio(stats)
            print("\n" + relatorio)

        return 0

    except KeyboardInterrupt:
        logger.info("\n⚠️  Interrompido pelo usuário")
        return 130
    except Exception as e:
        logger.error(f"\n❌ Erro fatal: {e}", exc_info=args.verbose)
        return 1


if __name__ == '__main__':
    sys.exit(main())
