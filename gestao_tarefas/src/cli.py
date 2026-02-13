#!/usr/bin/env python3
"""
CLI para Sistema de Gestão de Orçamentos

Orquestra o pipeline completo:
- Buscar emails (Gmail API)
- Preparar dados (limpeza)
- Extrair informações (IA)
- Criar tarefa (Asana)

Uso:
    # Pipeline completo
    python src/cli.py processar-pasta 26_062

    # Comandos individuais
    python src/cli.py buscar-emails 26_062 --query "JBS Seara"
    python src/cli.py preparar-dados pasta/26_062/emails
    python src/cli.py extrair-dados pasta/26_062/dados_preparados.md
    python src/cli.py criar-tarefa pasta/26_062/orcamento.json
"""

import argparse
import json
import logging
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

# Imports locais
try:
    from gmail_client import GmailClient
    from prepare_data import DataPreparer
    from ai_extractor import AIExtractor
    from asana_lib import AsanaLib, AsanaLibError
    from sync_drive import DriveSync
except ImportError:
    # Se rodado como módulo
    from src.gmail_client import GmailClient
    from src.prepare_data import DataPreparer
    from src.ai_extractor import AIExtractor
    from src.asana_lib import AsanaLib, AsanaLibError
    from src.sync_drive import DriveSync


# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class OrcamentoCLI:
    """Interface CLI para gestão de orçamentos."""

    def __init__(self, verbose: bool = False, dry_run: bool = False):
        """
        Inicializa CLI.

        Args:
            verbose: Log detalhado
            dry_run: Simular sem executar
        """
        self.verbose = verbose
        self.dry_run = dry_run

        if verbose:
            logging.getLogger().setLevel(logging.DEBUG)

        if dry_run:
            logger.info("🔍 Modo DRY-RUN ativado - nenhuma alteração será feita")

        # Inicializar componentes
        self.gmail_client = None
        self.data_preparer = DataPreparer()
        self.ai_extractor = None
        self.asana_lib = AsanaLib()

        # Estatísticas
        self.stats = {
            'inicio': datetime.now(),
            'emails_encontrados': 0,
            'arquivos_processados': 0,
            'tokens_usados': 0,
            'custo_total': 0.0,
            'tarefa_criada': None
        }

    def processar_pasta(
        self,
        pasta_id: str,
        query: Optional[str] = None,
        confirm: bool = False,
        force_sonnet: bool = False
    ) -> bool:
        """
        Pipeline completo de processamento.

        Args:
            pasta_id: ID da pasta (ex: 26_062)
            query: Query opcional para busca de emails
            confirm: Pedir confirmação antes de criar tarefa
            force_sonnet: Forçar uso do Sonnet

        Returns:
            True se processado com sucesso
        """
        logger.info(f"\n{'='*60}")
        logger.info(f"📁 Processando pasta: {pasta_id}")
        logger.info(f"{'='*60}\n")

        try:
            # Passo 1: Verificar pasta existe
            pasta_path = self._verificar_pasta(pasta_id)
            if not pasta_path:
                return False

            # Passo 2: Buscar emails relacionados
            emails = self._buscar_emails_relacionados(pasta_id, query)

            # Passo 3: Preparar dados
            dados_preparados = self._preparar_dados(pasta_path)
            if not dados_preparados:
                return False

            # Passo 4: Extrair informações com IA
            self.ai_extractor = AIExtractor(force_sonnet=force_sonnet)
            orcamento_json = self._extrair_informacoes(dados_preparados)
            if not orcamento_json:
                return False

            # Passo 5: Validar e revisar
            if confirm:
                if not self._confirmar_criacao(orcamento_json):
                    logger.info("❌ Cancelado pelo usuário")
                    return False

            # Passo 6: Criar tarefa no Asana
            task_id = self._criar_tarefa_asana(orcamento_json)
            if not task_id:
                return False

            # Passo 7: Anexar arquivos relevantes
            self._anexar_arquivos(task_id, pasta_path)

            # Passo 8: Relatório final
            self._exibir_relatorio(task_id)

            logger.info(f"\n✅ Pipeline concluído com sucesso!")
            return True

        except Exception as e:
            logger.error(f"❌ Erro no pipeline: {e}", exc_info=self.verbose)
            return False

    def _verificar_pasta(self, pasta_id: str) -> Optional[Path]:
        """Verifica se pasta existe no Drive."""
        logger.info(f"🔍 Verificando pasta {pasta_id}...")

        # Padrões de pasta possíveis
        drive_base = Path.home() / "Library/CloudStorage/GoogleDrive-orcamentos2@armant.com.br/Shared drives/02Orcamentos/2026"
        local_base = Path("drive")

        for base in [drive_base, local_base]:
            # Tentar encontrar pasta com padrão AA_XXX_*
            for pasta in base.glob(f"{pasta_id}*"):
                if pasta.is_dir():
                    logger.info(f"✓ Pasta encontrada: {pasta}")
                    return pasta

        logger.warning(f"⚠️  Pasta {pasta_id} não encontrada no Drive")
        logger.info(f"   Continuando sem pasta local...")
        return None

    def _buscar_emails_relacionados(
        self,
        pasta_id: str,
        query: Optional[str] = None
    ) -> List[Dict]:
        """Busca emails relacionados no Gmail."""
        logger.info(f"\n📧 Buscando emails relacionados...")

        if self.dry_run:
            logger.info("   [DRY-RUN] Pulando busca de emails")
            return []

        try:
            # Inicializar Gmail client
            if not self.gmail_client:
                self.gmail_client = GmailClient()
                if not self.gmail_client.authenticate():
                    logger.warning("⚠️  Não foi possível autenticar no Gmail")
                    return []

            # Construir query
            if not query:
                # Extrair informações do ID da pasta
                parts = pasta_id.split('_')
                if len(parts) >= 3:
                    query = ' '.join(parts[2:])
                else:
                    query = pasta_id

            logger.info(f"   Query: {query}")

            # Buscar
            emails = self.gmail_client.buscar_emails(query, max_results=10)
            self.stats['emails_encontrados'] = len(emails)

            if emails:
                logger.info(f"✓ Encontrados {len(emails)} emails")
                for i, email in enumerate(emails[:3], 1):
                    logger.info(f"   {i}. {email.get('subject', 'Sem assunto')[:50]}")
                if len(emails) > 3:
                    logger.info(f"   ... e mais {len(emails) - 3} emails")
            else:
                logger.info("   Nenhum email encontrado")

            return emails

        except Exception as e:
            logger.warning(f"⚠️  Erro ao buscar emails: {e}")
            return []

    def _preparar_dados(self, pasta_path: Optional[Path]) -> Optional[str]:
        """Prepara dados para extração."""
        logger.info(f"\n🧹 Preparando dados...")

        if not pasta_path:
            logger.info("   Sem pasta local para processar")
            return None

        # Procurar arquivos de email
        email_files = []
        for ext in ['*.html', '*.txt', '*.eml']:
            email_files.extend(pasta_path.rglob(ext))

        if not email_files:
            logger.warning("⚠️  Nenhum arquivo de email encontrado na pasta")
            return None

        logger.info(f"   Encontrados {len(email_files)} arquivos")

        # Processar cada arquivo
        textos_preparados = []

        for arquivo in email_files[:5]:  # Limitar a 5 arquivos
            logger.info(f"   Processando: {arquivo.name}")

            try:
                resultado = self.data_preparer.preparar_email(
                    str(arquivo),
                    None  # Não salvar, apenas retornar
                )

                textos_preparados.append(resultado['texto_preparado'])
                self.stats['arquivos_processados'] += 1

                if self.verbose:
                    logger.debug(f"      Tokens: {resultado['tokens_antes']} → {resultado['tokens_depois']} "
                               f"({resultado['reducao_percentual']:.1f}% redução)")

            except Exception as e:
                logger.warning(f"      Erro ao processar {arquivo.name}: {e}")

        if not textos_preparados:
            logger.error("❌ Nenhum arquivo processado com sucesso")
            return None

        # Consolidar textos
        texto_final = "\n\n---\n\n".join(textos_preparados)

        logger.info(f"✓ Dados preparados ({len(textos_preparados)} arquivos)")

        return texto_final

    def _extrair_informacoes(self, texto_preparado: str) -> Optional[Dict]:
        """Extrai informações com IA."""
        logger.info(f"\n🤖 Extraindo informações com IA...")

        if self.dry_run:
            logger.info("   [DRY-RUN] Pulando extração")
            return {
                'cliente': '[DRY-RUN] Cliente Teste',
                'local': 'São Paulo - SP',
                'tipo_servico': 'instalacao',
                'origem': 'comercial',
                'descricao': 'Teste em modo dry-run'
            }

        try:
            resultado = self.ai_extractor.extrair(texto_preparado)

            # Estatísticas
            stats = self.ai_extractor.get_estatisticas()
            self.stats['tokens_usados'] = stats['tokens_total']
            self.stats['custo_total'] = stats['custo_usd']

            logger.info(f"✓ Extração concluída")
            logger.info(f"   Modelo: {stats['modelo']}")
            logger.info(f"   Tokens: {stats['tokens_total']}")
            logger.info(f"   Custo: ${stats['custo_usd']:.4f}")

            if self.verbose:
                logger.debug(f"\n   Dados extraídos:")
                logger.debug(f"   Cliente: {resultado.get('cliente')}")
                logger.debug(f"   Local: {resultado.get('local')}")
                logger.debug(f"   Tipo: {resultado.get('tipo_servico')}")

            return resultado

        except Exception as e:
            logger.error(f"❌ Erro na extração: {e}", exc_info=self.verbose)
            return None

    def _confirmar_criacao(self, orcamento_json: Dict) -> bool:
        """Pede confirmação antes de criar tarefa."""
        logger.info(f"\n📋 Resumo do orçamento:")
        logger.info(f"   Cliente: {orcamento_json.get('cliente', 'N/A')}")
        logger.info(f"   Local: {orcamento_json.get('local', 'N/A')}")
        logger.info(f"   Tipo: {orcamento_json.get('tipo_servico', 'N/A')}")
        logger.info(f"   Prazo: {orcamento_json.get('prazo', 'N/A')}")

        resposta = input("\n   Criar tarefa no Asana? (s/n): ").strip().lower()
        return resposta in ['s', 'sim', 'y', 'yes']

    def _criar_tarefa_asana(self, orcamento_json: Dict) -> Optional[str]:
        """Cria tarefa no Asana."""
        logger.info(f"\n📝 Criando tarefa no Asana...")

        if self.dry_run:
            logger.info("   [DRY-RUN] Tarefa não será criada")
            return "DRY_RUN_ID"

        try:
            task_id = self.asana_lib.criar_orcamento(orcamento_json)
            self.stats['tarefa_criada'] = task_id

            logger.info(f"✓ Tarefa criada: {task_id}")

            # URL da tarefa (funciona em simulação e produção)
            project_id = self.asana_lib.project_id
            logger.info(f"   URL: https://app.asana.com/0/{project_id}/{task_id}")

            return task_id

        except AsanaLibError as e:
            logger.error(f"❌ Erro ao criar tarefa: {e}")
            return None

    def _anexar_arquivos(self, task_id: str, pasta_path: Optional[Path]):
        """Anexa arquivos relevantes à tarefa."""
        if not pasta_path or self.dry_run:
            return

        logger.info(f"\n📎 Anexando arquivos...")

        # Procurar PDFs de orçamento
        orcamento_dir = pasta_path / "03_Orcamento"
        if orcamento_dir.exists():
            pdfs = list(orcamento_dir.glob("ORC_*.pdf"))

            for pdf in pdfs:
                try:
                    logger.info(f"   Anexando: {pdf.name}")
                    self.asana_lib.anexar_arquivo(task_id, str(pdf))
                except Exception as e:
                    logger.warning(f"      Erro: {e}")

    def _exibir_relatorio(self, task_id: Optional[str]):
        """Exibe relatório final do processamento."""
        duracao = (datetime.now() - self.stats['inicio']).total_seconds()

        logger.info(f"\n{'='*60}")
        logger.info(f"📊 Relatório de Processamento")
        logger.info(f"{'='*60}")
        logger.info(f"⏱️  Duração: {duracao:.1f}s")
        logger.info(f"📧 Emails encontrados: {self.stats['emails_encontrados']}")
        logger.info(f"📄 Arquivos processados: {self.stats['arquivos_processados']}")
        logger.info(f"🎯 Tokens usados: {self.stats['tokens_usados']}")
        logger.info(f"💰 Custo total: ${self.stats['custo_total']:.4f}")

        if task_id and task_id != "DRY_RUN_ID":
            logger.info(f"✅ Tarefa criada: {task_id}")
            project_id = self.asana_lib.project_id
            logger.info(f"🔗 https://app.asana.com/0/{project_id}/{task_id}")

        logger.info(f"{'='*60}\n")

    def buscar_emails(self, pasta_id: str, query: Optional[str] = None, max_results: int = 10):
        """Comando para buscar emails."""
        logger.info(f"📧 Buscando emails para: {pasta_id}")

        if not query:
            # Extrair query do ID
            parts = pasta_id.split('_')
            query = ' '.join(parts[2:]) if len(parts) >= 3 else pasta_id

        logger.info(f"   Query: {query}")

        if self.dry_run:
            logger.info("   [DRY-RUN] Busca não será executada")
            return

        try:
            if not self.gmail_client:
                self.gmail_client = GmailClient()
                if not self.gmail_client.authenticate():
                    logger.error("❌ Falha na autenticação Gmail")
                    return

            emails = self.gmail_client.buscar_emails(query, max_results=max_results)

            logger.info(f"\n✓ Encontrados {len(emails)} emails:\n")

            for i, email in enumerate(emails, 1):
                logger.info(f"{i}. {email.get('subject', 'Sem assunto')}")
                logger.info(f"   De: {email.get('from', 'Desconhecido')}")
                logger.info(f"   Data: {email.get('date', 'N/A')}")
                logger.info(f"   ID: {email.get('id')}\n")

        except Exception as e:
            logger.error(f"❌ Erro: {e}", exc_info=self.verbose)

    def preparar_dados(self, input_path: str, output_path: Optional[str] = None):
        """Comando para preparar dados."""
        logger.info(f"🧹 Preparando dados: {input_path}")

        input_path = Path(input_path)

        if not input_path.exists():
            logger.error(f"❌ Caminho não encontrado: {input_path}")
            return

        try:
            if input_path.is_file():
                # Processar arquivo único
                resultado = self.data_preparer.preparar_email(
                    str(input_path),
                    output_path
                )

                logger.info(f"\n✓ Arquivo processado:")
                logger.info(f"   Tokens: {resultado['tokens_antes']} → {resultado['tokens_depois']}")
                logger.info(f"   Redução: {resultado['reducao_percentual']:.1f}%")

                if output_path:
                    logger.info(f"   Salvo em: {output_path}")

            else:
                # Processar pasta
                resultado = self.data_preparer.preparar_pasta(str(input_path))

                logger.info(f"\n✓ Pasta processada:")
                logger.info(f"   Arquivos: {resultado['arquivos_processados']}")
                logger.info(f"   Output: {resultado['arquivo_consolidado']}")
                logger.info(f"   Redução média: {resultado['reducao_media']:.1f}%")

        except Exception as e:
            logger.error(f"❌ Erro: {e}", exc_info=self.verbose)

    def extrair_dados(self, input_file: str, output_file: Optional[str] = None, force_sonnet: bool = False):
        """Comando para extrair dados com IA."""
        logger.info(f"🤖 Extraindo dados: {input_file}")

        if not os.path.exists(input_file):
            logger.error(f"❌ Arquivo não encontrado: {input_file}")
            return

        try:
            # Ler arquivo
            with open(input_file, 'r', encoding='utf-8') as f:
                texto = f.read()

            # Extrair
            self.ai_extractor = AIExtractor(force_sonnet=force_sonnet)
            resultado = self.ai_extractor.extrair(texto)

            # Estatísticas
            stats = self.ai_extractor.get_estatisticas()

            logger.info(f"\n✓ Extração concluída:")
            logger.info(f"   Modelo: {stats['modelo']}")
            logger.info(f"   Tokens: {stats['tokens_total']}")
            logger.info(f"   Custo: ${stats['custo_usd']:.4f}")

            # Salvar se solicitado
            if output_file:
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(resultado, f, indent=2, ensure_ascii=False)
                logger.info(f"   Salvo em: {output_file}")
            else:
                # Exibir resultado
                logger.info(f"\n📋 Dados extraídos:")
                print(json.dumps(resultado, indent=2, ensure_ascii=False))

        except Exception as e:
            logger.error(f"❌ Erro: {e}", exc_info=self.verbose)

    def criar_tarefa(self, json_file: str):
        """Comando para criar tarefa no Asana."""
        logger.info(f"📝 Criando tarefa: {json_file}")

        if not os.path.exists(json_file):
            logger.error(f"❌ Arquivo não encontrado: {json_file}")
            return

        try:
            # Ler JSON
            with open(json_file, 'r', encoding='utf-8') as f:
                dados = json.load(f)

            # Criar tarefa
            task_id = self.asana_lib.criar_orcamento(dados)

            logger.info(f"\n✓ Tarefa criada: {task_id}")
            project_id = self.asana_lib.project_id
            logger.info(f"🔗 https://app.asana.com/0/{project_id}/{task_id}")

        except Exception as e:
            logger.error(f"❌ Erro: {e}", exc_info=self.verbose)

    def sync_drive(self, pasta_id: Optional[str] = None, sync_all: bool = False):
        """Comando para sincronizar Drive → Asana."""
        logger.info(f"🔄 Sincronizando Drive → Asana")

        try:
            sync = DriveSync()

            if sync_all:
                stats = sync.sincronizar_todas()
                logger.info(f"\n✓ Sincronização completa")
                logger.info(f"  {stats['total_pdfs_anexados']} PDFs anexados")

            elif pasta_id:
                stats = sync.sincronizar_demanda(pasta_id)

                if not stats['erros']:
                    logger.info(f"\n✓ Sincronização concluída")
                    logger.info(f"  {stats['pdfs_anexados']} PDFs anexados")
                else:
                    logger.error(f"❌ Erros: {stats['erros']}")

            else:
                logger.error("Especifique pasta_id ou use --all")

        except Exception as e:
            logger.error(f"❌ Erro: {e}", exc_info=self.verbose)


def main():
    """Função principal CLI."""
    parser = argparse.ArgumentParser(
        description='Sistema de Gestão de Orçamentos - CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  # Pipeline completo
  %(prog)s processar-pasta 26_062
  %(prog)s processar-pasta 26_062 --confirm --query "JBS Seara"

  # Comandos individuais
  %(prog)s buscar-emails 26_062 --query "orçamento climatização"
  %(prog)s preparar-dados pasta/26_062/emails -o dados_preparados.md
  %(prog)s extrair-dados dados_preparados.md -o orcamento.json
  %(prog)s criar-tarefa orcamento.json

  # Opções úteis
  %(prog)s processar-pasta 26_062 --dry-run  # Simular sem executar
  %(prog)s processar-pasta 26_062 --sonnet   # Forçar Sonnet
  %(prog)s processar-pasta 26_062 -v         # Verbose
        """
    )

    # Opções globais
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Log detalhado')
    parser.add_argument('--dry-run', action='store_true',
                       help='Simular sem executar alterações')

    # Subcomandos
    subparsers = parser.add_subparsers(dest='command', help='Comando a executar')

    # processar-pasta
    parser_processar = subparsers.add_parser('processar-pasta',
                                            help='Pipeline completo de processamento')
    parser_processar.add_argument('pasta_id', help='ID da pasta (ex: 26_062)')
    parser_processar.add_argument('--query', help='Query para busca de emails')
    parser_processar.add_argument('--confirm', action='store_true',
                                 help='Pedir confirmação antes de criar tarefa')
    parser_processar.add_argument('--sonnet', action='store_true',
                                 help='Forçar uso do Sonnet')

    # buscar-emails
    parser_buscar = subparsers.add_parser('buscar-emails',
                                         help='Buscar emails no Gmail')
    parser_buscar.add_argument('pasta_id', help='ID da pasta (ex: 26_062)')
    parser_buscar.add_argument('--query', help='Query de busca customizada')
    parser_buscar.add_argument('--max-results', type=int, default=10,
                              help='Máximo de resultados (padrão: 10)')

    # preparar-dados
    parser_preparar = subparsers.add_parser('preparar-dados',
                                           help='Preparar dados para extração')
    parser_preparar.add_argument('input', help='Arquivo ou pasta de entrada')
    parser_preparar.add_argument('-o', '--output', help='Arquivo de saída')

    # extrair-dados
    parser_extrair = subparsers.add_parser('extrair-dados',
                                          help='Extrair informações com IA')
    parser_extrair.add_argument('input', help='Arquivo de entrada')
    parser_extrair.add_argument('-o', '--output', help='Arquivo JSON de saída')
    parser_extrair.add_argument('--sonnet', action='store_true',
                               help='Forçar uso do Sonnet')

    # criar-tarefa
    parser_criar = subparsers.add_parser('criar-tarefa',
                                        help='Criar tarefa no Asana')
    parser_criar.add_argument('json_file', help='Arquivo JSON com dados')

    # sync-drive
    parser_sync = subparsers.add_parser('sync-drive',
                                       help='Sincronizar Drive → Asana')
    parser_sync.add_argument('pasta_id', nargs='?',
                            help='ID da pasta (ex: 26_062)')
    parser_sync.add_argument('--all', action='store_true',
                            help='Sincronizar todas as demandas')

    # Parse argumentos
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Criar CLI
    cli = OrcamentoCLI(verbose=args.verbose, dry_run=args.dry_run)

    # Executar comando
    try:
        if args.command == 'processar-pasta':
            sucesso = cli.processar_pasta(
                args.pasta_id,
                query=args.query,
                confirm=args.confirm,
                force_sonnet=args.sonnet
            )
            return 0 if sucesso else 1

        elif args.command == 'buscar-emails':
            cli.buscar_emails(
                args.pasta_id,
                query=args.query,
                max_results=args.max_results
            )
            return 0

        elif args.command == 'preparar-dados':
            cli.preparar_dados(args.input, args.output)
            return 0

        elif args.command == 'extrair-dados':
            cli.extrair_dados(
                args.input,
                args.output,
                force_sonnet=args.sonnet
            )
            return 0

        elif args.command == 'criar-tarefa':
            cli.criar_tarefa(args.json_file)
            return 0

        elif args.command == 'sync-drive':
            cli.sync_drive(args.pasta_id, sync_all=args.all)
            return 0

        else:
            parser.print_help()
            return 1

    except KeyboardInterrupt:
        logger.info("\n\n⚠️  Interrompido pelo usuário")
        return 130
    except Exception as e:
        logger.error(f"\n❌ Erro fatal: {e}", exc_info=args.verbose)
        return 1


if __name__ == '__main__':
    sys.exit(main())
