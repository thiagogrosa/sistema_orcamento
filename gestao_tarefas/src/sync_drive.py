#!/usr/bin/env python3
"""
Sincronização Drive ↔ Asana

Mantém Google Drive e Asana sincronizados:
- Detecta novos PDFs e anexa no Asana
- Cria pastas no Drive ao criar tarefas
- Mapeia IDs de pastas → task_gid do Asana

Uso:
    # Sincronizar demanda específica
    python src/sync_drive.py sync 26_062

    # Sincronizar todas
    python src/sync_drive.py sync --all

    # Criar pasta no Drive
    python src/sync_drive.py criar-pasta 26_062 "CLIENTE SERVICO"
"""

import argparse
import json
import logging
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime

# Imports locais
try:
    from asana_lib import AsanaLib, AsanaLibError
except ImportError:
    from src.asana_lib import AsanaLib, AsanaLibError


# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DriveSync:
    """Sincronização entre Google Drive e Asana."""

    def __init__(
        self,
        drive_base: Optional[str] = None,
        mapping_file: str = "config/ids_mapping.json"
    ):
        """
        Inicializa DriveSync.

        Args:
            drive_base: Caminho base do Drive (usa padrão se None)
            mapping_file: Arquivo de mapeamento ID → task_gid
        """
        # Caminho padrão do Drive
        if drive_base is None:
            drive_base = os.path.expanduser(
                "~/Library/CloudStorage/GoogleDrive-orcamentos2@armant.com.br/"
                "Shared drives/02Orcamentos/2026"
            )

        self.drive_base = Path(drive_base)
        self.mapping_file = Path(mapping_file)
        self.asana_lib = AsanaLib()

        # Carregar mapeamento
        self.mapping = self._carregar_mapping()

        logger.info(f"DriveSync inicializado")
        logger.info(f"Drive base: {self.drive_base}")
        logger.info(f"Mapping: {len(self.mapping)} entradas")

    def _carregar_mapping(self) -> Dict[str, str]:
        """
        Carrega mapeamento de IDs.

        Returns:
            Dicionário {pasta_id: task_gid}
        """
        if not self.mapping_file.exists():
            logger.info("Arquivo de mapeamento não existe, criando vazio")
            self._salvar_mapping({})
            return {}

        try:
            with open(self.mapping_file, 'r', encoding='utf-8') as f:
                mapping = json.load(f)
            logger.info(f"Mapeamento carregado: {len(mapping)} entradas")
            return mapping

        except Exception as e:
            logger.error(f"Erro ao carregar mapeamento: {e}")
            return {}

    def _salvar_mapping(self, mapping: Dict[str, str]):
        """
        Salva mapeamento de IDs.

        Args:
            mapping: Dicionário {pasta_id: task_gid}
        """
        try:
            # Criar diretório se não existe
            self.mapping_file.parent.mkdir(parents=True, exist_ok=True)

            with open(self.mapping_file, 'w', encoding='utf-8') as f:
                json.dump(mapping, f, indent=2, ensure_ascii=False)

            logger.debug(f"Mapeamento salvo: {len(mapping)} entradas")

        except Exception as e:
            logger.error(f"Erro ao salvar mapeamento: {e}")

    def registrar_mapeamento(self, pasta_id: str, task_gid: str):
        """
        Registra mapeamento pasta → tarefa.

        Args:
            pasta_id: ID da pasta (ex: "26_062")
            task_gid: GID da tarefa no Asana
        """
        self.mapping[pasta_id] = task_gid
        self._salvar_mapping(self.mapping)
        logger.info(f"Mapeamento registrado: {pasta_id} → {task_gid}")

    def obter_task_gid(self, pasta_id: str) -> Optional[str]:
        """
        Obtém task_gid a partir do pasta_id.

        Args:
            pasta_id: ID da pasta (ex: "26_062")

        Returns:
            task_gid se encontrado, None caso contrário
        """
        return self.mapping.get(pasta_id)

    def listar_pastas_drive(self) -> List[Tuple[str, Path]]:
        """
        Lista todas as pastas no Drive.

        Returns:
            Lista de tuplas (pasta_id, path)
        """
        if not self.drive_base.exists():
            logger.warning(f"Drive base não encontrado: {self.drive_base}")
            return []

        pastas = []

        for pasta in self.drive_base.iterdir():
            if not pasta.is_dir():
                continue

            # Extrair ID da pasta (formato: 26_XXX_...)
            nome = pasta.name
            partes = nome.split('_')

            if len(partes) >= 2:
                pasta_id = f"{partes[0]}_{partes[1]}"
                pastas.append((pasta_id, pasta))

        logger.info(f"Encontradas {len(pastas)} pastas no Drive")
        return pastas

    def detectar_pdfs_novos(self, pasta_id: str) -> List[Path]:
        """
        Detecta PDFs na pasta 03_Orcamento.

        Args:
            pasta_id: ID da pasta (ex: "26_062")

        Returns:
            Lista de caminhos para PDFs encontrados
        """
        # Encontrar pasta
        pastas_drive = self.listar_pastas_drive()
        pasta_path = None

        for pid, path in pastas_drive:
            if pid == pasta_id:
                pasta_path = path
                break

        if not pasta_path:
            logger.warning(f"Pasta {pasta_id} não encontrada no Drive")
            return []

        # Verificar pasta de orçamentos
        orcamento_dir = pasta_path / "03_Orcamento"

        if not orcamento_dir.exists():
            logger.debug(f"Pasta 03_Orcamento não existe: {pasta_id}")
            return []

        # Buscar PDFs com prefixo ORC_
        pdfs = list(orcamento_dir.glob("ORC_*.pdf"))

        if pdfs:
            logger.info(f"Encontrados {len(pdfs)} PDFs em {pasta_id}")

        return pdfs

    def anexar_pdfs_asana(self, pasta_id: str, pdfs: List[Path]) -> int:
        """
        Anexa PDFs à tarefa no Asana.

        Args:
            pasta_id: ID da pasta
            pdfs: Lista de PDFs para anexar

        Returns:
            Número de PDFs anexados com sucesso
        """
        # Obter task_gid
        task_gid = self.obter_task_gid(pasta_id)

        if not task_gid:
            logger.warning(f"Pasta {pasta_id} não tem mapeamento para Asana")
            return 0

        anexados = 0

        for pdf in pdfs:
            try:
                logger.info(f"Anexando: {pdf.name}")

                sucesso = self.asana_lib.anexar_arquivo(task_gid, str(pdf))

                if sucesso:
                    anexados += 1
                    logger.info(f"✓ {pdf.name} anexado")
                else:
                    logger.warning(f"✗ Falha ao anexar {pdf.name}")

            except Exception as e:
                logger.error(f"Erro ao anexar {pdf.name}: {e}")

        return anexados

    def sincronizar_demanda(self, pasta_id: str) -> Dict:
        """
        Sincroniza uma demanda específica.

        Args:
            pasta_id: ID da pasta (ex: "26_062")

        Returns:
            Dicionário com estatísticas da sincronização
        """
        logger.info(f"\n{'='*60}")
        logger.info(f"Sincronizando: {pasta_id}")
        logger.info(f"{'='*60}")

        stats = {
            'pasta_id': pasta_id,
            'task_gid': None,
            'pdfs_encontrados': 0,
            'pdfs_anexados': 0,
            'erros': []
        }

        try:
            # 1. Verificar mapeamento
            task_gid = self.obter_task_gid(pasta_id)

            if not task_gid:
                msg = f"Pasta {pasta_id} não mapeada"
                logger.warning(msg)
                stats['erros'].append(msg)
                return stats

            stats['task_gid'] = task_gid
            logger.info(f"✓ Tarefa mapeada: {task_gid}")

            # 2. Detectar PDFs
            pdfs = self.detectar_pdfs_novos(pasta_id)
            stats['pdfs_encontrados'] = len(pdfs)

            if not pdfs:
                logger.info("Nenhum PDF encontrado")
                return stats

            logger.info(f"✓ {len(pdfs)} PDFs encontrados")

            # 3. Anexar PDFs
            anexados = self.anexar_pdfs_asana(pasta_id, pdfs)
            stats['pdfs_anexados'] = anexados

            logger.info(f"✓ {anexados}/{len(pdfs)} PDFs anexados")

            return stats

        except Exception as e:
            logger.error(f"Erro na sincronização: {e}", exc_info=True)
            stats['erros'].append(str(e))
            return stats

    def sincronizar_todas(self) -> Dict:
        """
        Sincroniza todas as demandas mapeadas.

        Returns:
            Dicionário com estatísticas gerais
        """
        logger.info(f"\n{'='*60}")
        logger.info(f"Sincronizando todas as demandas")
        logger.info(f"{'='*60}\n")

        stats_geral = {
            'total_demandas': 0,
            'sincronizadas': 0,
            'com_pdfs': 0,
            'total_pdfs_anexados': 0,
            'erros': 0
        }

        # Sincronizar cada demanda mapeada
        for pasta_id in self.mapping.keys():
            stats_geral['total_demandas'] += 1

            stats = self.sincronizar_demanda(pasta_id)

            if not stats['erros']:
                stats_geral['sincronizadas'] += 1

                if stats['pdfs_anexados'] > 0:
                    stats_geral['com_pdfs'] += 1
                    stats_geral['total_pdfs_anexados'] += stats['pdfs_anexados']
            else:
                stats_geral['erros'] += 1

        # Relatório
        logger.info(f"\n{'='*60}")
        logger.info(f"Sincronização completa")
        logger.info(f"{'='*60}")
        logger.info(f"Total de demandas: {stats_geral['total_demandas']}")
        logger.info(f"Sincronizadas: {stats_geral['sincronizadas']}")
        logger.info(f"Com PDFs anexados: {stats_geral['com_pdfs']}")
        logger.info(f"Total de PDFs: {stats_geral['total_pdfs_anexados']}")

        if stats_geral['erros'] > 0:
            logger.warning(f"Erros: {stats_geral['erros']}")

        return stats_geral

    def criar_pasta_drive(
        self,
        pasta_id: str,
        descricao: str,
        criar_subpastas: bool = True
    ) -> Optional[Path]:
        """
        Cria pasta no Drive.

        Args:
            pasta_id: ID da pasta (ex: "26_062")
            descricao: Descrição (ex: "EMPRESA_SERVICO")
            criar_subpastas: Se True, cria subpastas padrão

        Returns:
            Path da pasta criada ou None se falhar
        """
        logger.info(f"Criando pasta: {pasta_id}_{descricao}")

        # Nome da pasta
        nome_pasta = f"{pasta_id}_{descricao}"
        pasta_path = self.drive_base / nome_pasta

        try:
            # Criar pasta principal
            pasta_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"✓ Pasta criada: {pasta_path}")

            # Criar subpastas padrão
            if criar_subpastas:
                subpastas = [
                    "01_Projetos",
                    "02_Levantamento",
                    "03_Orcamento",
                    "04_Cotacoes"
                ]

                for subpasta in subpastas:
                    sub_path = pasta_path / subpasta
                    sub_path.mkdir(exist_ok=True)
                    logger.debug(f"  ✓ {subpasta}")

                logger.info("✓ Subpastas criadas")

            return pasta_path

        except Exception as e:
            logger.error(f"Erro ao criar pasta: {e}")
            return None

    def exportar_mapeamento(self, output_file: str):
        """
        Exporta mapeamento para arquivo legível.

        Args:
            output_file: Arquivo de saída
        """
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("# Mapeamento Drive → Asana\n")
                f.write(f"# Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"# Total: {len(self.mapping)} mapeamentos\n\n")

                for pasta_id, task_gid in sorted(self.mapping.items()):
                    project_id = self.asana_lib.project_id
                    url = f"https://app.asana.com/0/{project_id}/{task_gid}"
                    f.write(f"{pasta_id} → {task_gid}\n")
                    f.write(f"  {url}\n\n")

            logger.info(f"Mapeamento exportado: {output_file}")

        except Exception as e:
            logger.error(f"Erro ao exportar: {e}")


def main():
    """Função principal CLI."""
    parser = argparse.ArgumentParser(
        description='Sincronização Drive ↔ Asana',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  # Sincronizar demanda específica
  %(prog)s sync 26_062

  # Sincronizar todas
  %(prog)s sync --all

  # Criar pasta no Drive
  %(prog)s criar-pasta 26_062 "CLIENTE_SERVICO"

  # Registrar mapeamento
  %(prog)s registrar 26_062 1234567890123456

  # Exportar mapeamento
  %(prog)s exportar mapeamento.txt
        """
    )

    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Log detalhado')

    subparsers = parser.add_subparsers(dest='command', help='Comando a executar')

    # sync
    parser_sync = subparsers.add_parser('sync', help='Sincronizar Drive → Asana')
    parser_sync.add_argument('pasta_id', nargs='?', help='ID da pasta (ex: 26_062)')
    parser_sync.add_argument('--all', action='store_true',
                            help='Sincronizar todas as demandas')

    # criar-pasta
    parser_criar = subparsers.add_parser('criar-pasta',
                                        help='Criar pasta no Drive')
    parser_criar.add_argument('pasta_id', help='ID da pasta')
    parser_criar.add_argument('descricao', help='Descrição (ex: CLIENTE_SERVICO)')
    parser_criar.add_argument('--sem-subpastas', action='store_true',
                             help='Não criar subpastas padrão')

    # registrar
    parser_reg = subparsers.add_parser('registrar',
                                      help='Registrar mapeamento')
    parser_reg.add_argument('pasta_id', help='ID da pasta')
    parser_reg.add_argument('task_gid', help='GID da tarefa no Asana')

    # exportar
    parser_exp = subparsers.add_parser('exportar',
                                      help='Exportar mapeamento')
    parser_exp.add_argument('output', help='Arquivo de saída')

    # listar
    parser_list = subparsers.add_parser('listar',
                                       help='Listar pastas e mapeamentos')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Configurar logging
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Criar DriveSync
    sync = DriveSync()

    # Executar comando
    try:
        if args.command == 'sync':
            if args.all:
                sync.sincronizar_todas()
            elif args.pasta_id:
                sync.sincronizar_demanda(args.pasta_id)
            else:
                logger.error("Especifique pasta_id ou use --all")
                return 1

        elif args.command == 'criar-pasta':
            pasta = sync.criar_pasta_drive(
                args.pasta_id,
                args.descricao,
                criar_subpastas=not args.sem_subpastas
            )
            if pasta:
                logger.info(f"✓ Pasta criada: {pasta}")
            else:
                return 1

        elif args.command == 'registrar':
            sync.registrar_mapeamento(args.pasta_id, args.task_gid)
            logger.info("✓ Mapeamento registrado")

        elif args.command == 'exportar':
            sync.exportar_mapeamento(args.output)

        elif args.command == 'listar':
            pastas = sync.listar_pastas_drive()

            logger.info(f"\nPastas no Drive: {len(pastas)}")
            logger.info(f"Mapeamentos: {len(sync.mapping)}\n")

            for pasta_id, path in pastas:
                task_gid = sync.obter_task_gid(pasta_id)
                status = "✓ mapeado" if task_gid else "✗ não mapeado"

                logger.info(f"{pasta_id}: {status}")

                if task_gid:
                    project_id = sync.asana_lib.project_id
                    url = f"https://app.asana.com/0/{project_id}/{task_gid}"
                    logger.info(f"  {url}")

        return 0

    except KeyboardInterrupt:
        logger.info("\n\n⚠️  Interrompido pelo usuário")
        return 130
    except Exception as e:
        logger.error(f"\n❌ Erro: {e}", exc_info=args.verbose)
        return 1


if __name__ == '__main__':
    sys.exit(main())
