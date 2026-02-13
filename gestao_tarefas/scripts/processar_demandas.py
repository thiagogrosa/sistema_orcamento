#!/usr/bin/env python3
"""
Processador de Demandas em Lote

Lê a fila de pesquisa, busca emails no Gmail para cada demanda,
extrai dados estruturados e salva os resultados.

Uso:
    python scripts/processar_demandas.py                    # Processar todas pendentes
    python scripts/processar_demandas.py --id 26_049        # Processar uma específica
    python scripts/processar_demandas.py --prioridade alta  # Filtrar por prioridade
    python scripts/processar_demandas.py --limite 5         # Processar apenas 5
    python scripts/processar_demandas.py --dry-run          # Simular sem baixar
"""

import sys
import os
import json
import logging
import argparse
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import asdict

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from gmail_client import GmailClient
from extrator_dados_email import ExtratorDadosEmail, DadosExtraidos

logger = logging.getLogger(__name__)

# Caminhos dos arquivos
BASE_DIR = Path(__file__).parent.parent
FILA_PESQUISA = BASE_DIR / "gemini-tasks" / "fila-pesquisa.json"
RESULTADOS_FILE = BASE_DIR / "gemini-tasks" / "resultados-pesquisa-gmail.json"
EMAILS_DIR = BASE_DIR / "emails-extraidos"


class ProcessadorDemandas:
    """Processa demandas em lote: busca emails, extrai dados, salva resultados."""

    def __init__(self, dry_run: bool = False, max_emails: int = 10):
        self.dry_run = dry_run
        self.max_emails = max_emails
        self.gmail = None
        self.extrator = ExtratorDadosEmail()
        self.resultados_existentes = self._carregar_resultados_existentes()

    def _carregar_resultados_existentes(self) -> Dict:
        """Carrega resultados anteriores para não reprocessar."""
        if RESULTADOS_FILE.exists():
            with open(RESULTADOS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"metadata": {}, "resultados": []}

    def _conectar_gmail(self):
        """Inicializa e autentica cliente Gmail."""
        if self.gmail is None:
            self.gmail = GmailClient()
            self.gmail.authenticate()
            logger.info("Cliente Gmail conectado")

    def carregar_fila(
        self,
        prioridade: Optional[str] = None,
        demanda_id: Optional[str] = None,
        limite: Optional[int] = None
    ) -> List[Dict]:
        """
        Carrega fila de pesquisa com filtros.

        Args:
            prioridade: Filtrar por prioridade (alta, media, baixa)
            demanda_id: Processar apenas uma demanda específica
            limite: Limitar número de demandas

        Returns:
            Lista de demandas para processar
        """
        with open(FILA_PESQUISA, 'r', encoding='utf-8') as f:
            fila = json.load(f)

        demandas = fila.get('fila', [])

        # Filtrar por ID específico
        if demanda_id:
            demandas = [d for d in demandas if d['asana'] == demanda_id]
            if not demandas:
                logger.warning(f"Demanda {demanda_id} não encontrada na fila")
            return demandas

        # Filtrar por prioridade
        if prioridade:
            demandas = [d for d in demandas if d['prioridade'] == prioridade]

        # Filtrar apenas pendentes
        demandas = [d for d in demandas if d['status'] == 'pendente']

        # Aplicar limite
        if limite:
            demandas = demandas[:limite]

        return demandas

    def _construir_query(self, demanda: Dict) -> str:
        """
        Constrói query de busca Gmail para uma demanda.

        Args:
            demanda: Dict com dados da demanda (asana, cliente)

        Returns:
            Query string para Gmail API
        """
        asana_id = demanda['asana']
        cliente = demanda['cliente']

        # Construir query com variações do ID
        id_parts = asana_id.replace('_', '/')
        queries = []

        # Buscar por ID em diferentes formatos
        queries.append(f'"{id_parts}"')
        queries.append(f'"{asana_id}"')

        # Buscar por nome do cliente (palavras-chave)
        # Remover sufixos comuns para melhorar a busca
        cliente_limpo = cliente.split(' - ')[0].strip()
        cliente_limpo = cliente_limpo.split(' / ')[0].strip()
        queries.append(f'"{cliente_limpo}"')

        query = f'({" OR ".join(queries)})'
        return query

    def processar_demanda(self, demanda: Dict) -> Dict:
        """
        Processa uma demanda: busca emails, extrai dados.

        Args:
            demanda: Dict com dados da demanda

        Returns:
            Dict com resultado do processamento
        """
        asana_id = demanda['asana']
        cliente = demanda['cliente']
        task_id = demanda['id']

        print(f"\n{'─'*60}")
        print(f"  Processando: {asana_id} - {cliente}")
        print(f"{'─'*60}")

        resultado = {
            "task_id": task_id,
            "asana_id": asana_id,
            "status": "nao_encontrado",
            "emails_analisados": 0,
            "dados": {
                "cliente": cliente,
                "cnpj": None,
                "contato_nome": None,
                "contato_telefone": None,
                "contato_email": None,
                "endereco": None,
                "local_servico": None,
                "tipo_servico": None,
                "detalhes": None,
                "prazo": None,
                "porte": None,
                "origem": None,
                "licitacao": None,
                "observacoes": None
            },
            "emails_fonte": [],
            "campos_nao_encontrados": [],
            "processado_em": datetime.now().isoformat()
        }

        if self.dry_run:
            query = self._construir_query(demanda)
            print(f"  [DRY-RUN] Query: {query}")
            resultado['status'] = 'dry_run'
            return resultado

        # Conectar Gmail
        self._conectar_gmail()

        # Buscar emails
        query = self._construir_query(demanda)
        print(f"  Query: {query}")

        emails = self.gmail.buscar_emails(query, max_results=self.max_emails)
        resultado['emails_analisados'] = len(emails)

        if not emails:
            print(f"  ✗ Nenhum email encontrado")
            resultado['campos_nao_encontrados'] = list(resultado['dados'].keys())
            return resultado

        print(f"  ✓ Encontrados {len(emails)} emails")

        # Criar diretório para emails desta demanda
        demanda_dir = EMAILS_DIR / asana_id
        demanda_dir.mkdir(parents=True, exist_ok=True)

        # Baixar e processar emails (máximo 5 para extração)
        dados_consolidados = DadosExtraidos()
        emails_processados = min(5, len(emails))

        for i, email_meta in enumerate(emails[:emails_processados]):
            email_id = email_meta['id']
            subject = email_meta.get('subject', '(sem assunto)')

            print(f"  Processando email {i+1}/{emails_processados}: {subject[:45]}...")

            try:
                # Baixar email
                filepath = self.gmail.baixar_email(
                    email_id=email_id,
                    output_dir=str(demanda_dir),
                    format='txt'
                )

                # Extrair dados
                with open(filepath, 'r', encoding='utf-8') as f:
                    texto = f.read()

                dados_email = self.extrator.extrair(texto)

                # Consolidar dados (manter primeiro valor encontrado)
                self._consolidar_dados(dados_consolidados, dados_email)

                # Registrar fonte
                resultado['emails_fonte'].append({
                    "data": email_meta.get('date', ''),
                    "assunto": subject,
                    "de": email_meta.get('from', ''),
                    "arquivo": os.path.basename(filepath)
                })

            except Exception as e:
                logger.warning(f"Erro ao processar email {email_id}: {e}")
                continue

        # Preencher resultado com dados consolidados
        self._preencher_resultado(resultado, dados_consolidados)

        # Determinar status
        campos_preenchidos = sum(1 for v in resultado['dados'].values() if v)
        total_campos = len(resultado['dados'])

        if campos_preenchidos >= total_campos * 0.7:
            resultado['status'] = 'encontrado'
        elif campos_preenchidos >= total_campos * 0.3:
            resultado['status'] = 'parcial'
        else:
            resultado['status'] = 'nao_encontrado'

        # Listar campos não encontrados
        resultado['campos_nao_encontrados'] = [
            k for k, v in resultado['dados'].items() if not v
        ]

        status_icon = {'encontrado': '✓', 'parcial': '◐', 'nao_encontrado': '✗'}
        print(f"  {status_icon.get(resultado['status'], '?')} Status: {resultado['status']} "
              f"({campos_preenchidos}/{total_campos} campos)")

        return resultado

    def _consolidar_dados(self, consolidado: DadosExtraidos, novo: DadosExtraidos):
        """Consolida dados de múltiplos emails (mantém primeiro valor encontrado)."""
        if not consolidado.cnpj and novo.cnpj:
            consolidado.cnpj = novo.cnpj

        if not consolidado.razao_social and novo.razao_social:
            consolidado.razao_social = novo.razao_social

        if not consolidado.localizacao and novo.localizacao:
            consolidado.localizacao = novo.localizacao

        if not consolidado.condicoes_pagamento and novo.condicoes_pagamento:
            consolidado.condicoes_pagamento = novo.condicoes_pagamento

        # Listas: acumular sem duplicatas
        for tel in novo.telefone:
            if tel not in consolidado.telefone:
                consolidado.telefone.append(tel)

        for email in novo.email:
            if email not in consolidado.email:
                consolidado.email.append(email)

        for valor in novo.valores:
            if valor not in consolidado.valores:
                consolidado.valores.append(valor)

        for pessoa in novo.pessoas_envolvidas:
            if pessoa not in consolidado.pessoas_envolvidas:
                consolidado.pessoas_envolvidas.append(pessoa)

    def _preencher_resultado(self, resultado: Dict, dados: DadosExtraidos):
        """Preenche o resultado com dados consolidados."""
        d = resultado['dados']

        if dados.cnpj:
            d['cnpj'] = dados.cnpj
        if dados.razao_social:
            d['cliente'] = dados.razao_social
        if dados.telefone:
            d['contato_telefone'] = ', '.join(dados.telefone[:3])
        if dados.email:
            d['contato_email'] = ', '.join(dados.email[:3])
        if dados.localizacao:
            d['local_servico'] = dados.localizacao
        if dados.valores:
            d['detalhes'] = f"Valores encontrados: {', '.join(dados.valores)}"
        if dados.condicoes_pagamento:
            d['observacoes'] = dados.condicoes_pagamento

    def processar_lote(
        self,
        prioridade: Optional[str] = None,
        demanda_id: Optional[str] = None,
        limite: Optional[int] = None
    ) -> List[Dict]:
        """
        Processa múltiplas demandas.

        Args:
            prioridade: Filtrar por prioridade
            demanda_id: Processar apenas uma específica
            limite: Limitar quantidade

        Returns:
            Lista de resultados
        """
        demandas = self.carregar_fila(prioridade, demanda_id, limite)

        if not demandas:
            print("Nenhuma demanda para processar.")
            return []

        print("="*60)
        print(f"  PROCESSAMENTO EM LOTE - {len(demandas)} demandas")
        print("="*60)

        resultados = []
        for demanda in demandas:
            try:
                resultado = self.processar_demanda(demanda)
                resultados.append(resultado)
            except Exception as e:
                logger.error(f"Erro ao processar {demanda['asana']}: {e}")
                resultados.append({
                    "task_id": demanda['id'],
                    "asana_id": demanda['asana'],
                    "status": "erro",
                    "erro": str(e),
                    "processado_em": datetime.now().isoformat()
                })

        # Salvar resultados
        self._salvar_resultados(resultados)

        # Atualizar fila
        self._atualizar_fila(resultados)

        # Imprimir resumo
        self._imprimir_resumo(resultados)

        return resultados

    def _salvar_resultados(self, novos_resultados: List[Dict]):
        """Salva resultados, mesclando com existentes."""
        existentes = self.resultados_existentes

        # Criar índice dos existentes por asana_id
        indice = {}
        for r in existentes.get('resultados', []):
            indice[r.get('asana_id', '')] = r

        # Mesclar novos
        for r in novos_resultados:
            indice[r['asana_id']] = r

        # Atualizar metadata
        total = len(indice)
        encontrados = sum(1 for r in indice.values() if r.get('status') == 'encontrado')
        parciais = sum(1 for r in indice.values() if r.get('status') == 'parcial')
        nao_encontrados = sum(1 for r in indice.values() if r.get('status') == 'nao_encontrado')

        resultado_final = {
            "metadata": {
                "gerado_em": existentes.get('metadata', {}).get('gerado_em', datetime.now().strftime('%Y-%m-%d')),
                "atualizado_em": datetime.now().strftime('%Y-%m-%d %H:%M'),
                "conta_gmail": "orcamentos2@armant.com.br",
                "total_tasks": total,
                "processadas": total,
                "encontradas": encontrados,
                "parciais": parciais,
                "nao_encontradas": nao_encontrados
            },
            "resultados": list(indice.values())
        }

        with open(RESULTADOS_FILE, 'w', encoding='utf-8') as f:
            json.dump(resultado_final, f, indent=2, ensure_ascii=False)

        print(f"\n✓ Resultados salvos em: {RESULTADOS_FILE}")

    def _atualizar_fila(self, resultados: List[Dict]):
        """Atualiza status das demandas na fila."""
        with open(FILA_PESQUISA, 'r', encoding='utf-8') as f:
            fila = json.load(f)

        # Mapear resultados por asana_id
        status_map = {r['asana_id']: r['status'] for r in resultados}

        for demanda in fila.get('fila', []):
            if demanda['asana'] in status_map:
                status = status_map[demanda['asana']]
                if status in ('encontrado', 'parcial'):
                    demanda['status'] = 'processado'
                elif status == 'nao_encontrado':
                    demanda['status'] = 'sem_resultado'

        fila['ultima_atualizacao'] = datetime.now().isoformat()

        with open(FILA_PESQUISA, 'w', encoding='utf-8') as f:
            json.dump(fila, f, indent=2, ensure_ascii=False)

        print(f"✓ Fila atualizada em: {FILA_PESQUISA}")

    def _imprimir_resumo(self, resultados: List[Dict]):
        """Imprime resumo do processamento."""
        print(f"\n{'='*60}")
        print(f"  RESUMO DO PROCESSAMENTO")
        print(f"{'='*60}")

        total = len(resultados)
        encontrados = sum(1 for r in resultados if r.get('status') == 'encontrado')
        parciais = sum(1 for r in resultados if r.get('status') == 'parcial')
        nao_encontrados = sum(1 for r in resultados if r.get('status') == 'nao_encontrado')
        erros = sum(1 for r in resultados if r.get('status') == 'erro')

        print(f"  Total processadas: {total}")
        print(f"  ✓ Encontrados:     {encontrados}")
        print(f"  ◐ Parciais:        {parciais}")
        print(f"  ✗ Não encontrados: {nao_encontrados}")
        if erros:
            print(f"  ⚠ Erros:           {erros}")

        print(f"\n  Emails salvos em:  {EMAILS_DIR}")
        print(f"  Resultados em:     {RESULTADOS_FILE}")
        print(f"{'='*60}")


def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    # Reduzir verbosidade de módulos externos
    logging.getLogger('googleapiclient').setLevel(logging.WARNING)
    logging.getLogger('google').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)

    parser = argparse.ArgumentParser(
        description='Processador de Demandas em Lote',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python scripts/processar_demandas.py                    # Todas pendentes
  python scripts/processar_demandas.py --id 26_049        # Uma específica
  python scripts/processar_demandas.py --prioridade alta  # Por prioridade
  python scripts/processar_demandas.py --limite 3         # Apenas 3
  python scripts/processar_demandas.py --dry-run          # Simular
        """
    )
    parser.add_argument('--id', type=str, help='ID da demanda específica (ex: 26_049)')
    parser.add_argument('--prioridade', choices=['alta', 'media', 'baixa'],
                        help='Filtrar por prioridade')
    parser.add_argument('--limite', type=int, help='Número máximo de demandas')
    parser.add_argument('--max-emails', type=int, default=10,
                        help='Máximo de emails por demanda (default: 10)')
    parser.add_argument('--dry-run', action='store_true',
                        help='Simular sem executar buscas')

    args = parser.parse_args()

    processador = ProcessadorDemandas(
        dry_run=args.dry_run,
        max_emails=args.max_emails
    )

    processador.processar_lote(
        prioridade=args.prioridade,
        demanda_id=args.id,
        limite=args.limite
    )


if __name__ == '__main__':
    main()
