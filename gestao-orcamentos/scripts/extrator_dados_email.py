#!/usr/bin/env python3
"""
Extrator Automático de Dados de Emails
Extrai informações estruturadas (CNPJ, telefone, email, valores, etc) de emails.
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict


@dataclass
class DadosExtraidos:
    """Estrutura para dados extraídos de emails."""
    cnpj: Optional[str] = None
    razao_social: Optional[str] = None
    telefone: List[str] = None
    email: List[str] = None
    valores: List[str] = None
    condicoes_pagamento: Optional[str] = None
    datas: List[str] = None
    localizacao: Optional[str] = None
    pessoas_envolvidas: List[str] = None
    escopo: Optional[str] = None

    def __post_init__(self):
        """Inicializar listas vazias se None."""
        if self.telefone is None:
            self.telefone = []
        if self.email is None:
            self.email = []
        if self.valores is None:
            self.valores = []
        if self.datas is None:
            self.datas = []
        if self.pessoas_envolvidas is None:
            self.pessoas_envolvidas = []


class ExtratorDadosEmail:
    """
    Extrator de dados estruturados de emails usando regex.

    Extrai:
    - CNPJ (formato XX.XXX.XXX/XXXX-XX)
    - Telefones (vários formatos)
    - Emails
    - Valores monetários (R$ X.XXX,XX)
    - Datas
    - Condições de pagamento
    """

    # Padrões regex
    REGEX_CNPJ = r'\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b'
    REGEX_TELEFONE = r'\b(?:\+55\s?)?(?:\(?\d{2}\)?\s?)?9?\d{4}[-\s]?\d{4}\b'
    REGEX_EMAIL = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    REGEX_VALOR = r'R\$\s*\d{1,3}(?:\.\d{3})*(?:,\d{2})?'
    REGEX_DATA = r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b'

    # Padrões para condições de pagamento
    REGEX_CONDICAO_PAGAMENTO = r'(?:condição|pagamento|prazo).*?(?:\d+%.*?\d+\s*dias?|à vista|[\d\s]+dias?)'

    # Padrões para localização (estado/cidade)
    REGEX_LOCALIZACAO = r'(?:[A-Z][a-zà-ú]+(?:\s+[A-Z][a-zà-ú]+)*)[,\s]+(?:[A-Z]{2}|[A-Z][a-zà-ú]+/[A-Z]{2})'

    def extrair(self, texto: str) -> DadosExtraidos:
        """
        Extrai dados estruturados de um texto de email.

        Args:
            texto: Conteúdo do email

        Returns:
            DadosExtraidos com informações encontradas
        """
        dados = DadosExtraidos()

        # CNPJ
        cnpjs = re.findall(self.REGEX_CNPJ, texto)
        if cnpjs:
            dados.cnpj = cnpjs[0]  # Primeiro CNPJ encontrado

        # Telefones
        telefones = re.findall(self.REGEX_TELEFONE, texto)
        dados.telefone = list(set(telefones))  # Remover duplicatas

        # Emails
        emails = re.findall(self.REGEX_EMAIL, texto)
        # Filtrar emails internos @armant
        emails_externos = [e for e in emails if '@armant.com.br' not in e.lower()]
        dados.email = list(set(emails_externos))

        # Valores monetários
        valores = re.findall(self.REGEX_VALOR, texto)
        dados.valores = list(set(valores))

        # Datas
        datas = re.findall(self.REGEX_DATA, texto)
        dados.datas = list(set(datas))

        # Condições de pagamento
        condicoes = re.search(
            self.REGEX_CONDICAO_PAGAMENTO,
            texto,
            re.IGNORECASE | re.MULTILINE
        )
        if condicoes:
            dados.condicoes_pagamento = condicoes.group(0).strip()

        # Localização
        localizacoes = re.findall(self.REGEX_LOCALIZACAO, texto)
        if localizacoes:
            dados.localizacao = localizacoes[0]

        # Extrair pessoas mencionadas (emails com @)
        pessoas = re.findall(r'@([A-Za-zÀ-ú\s]+?)\s*<', texto)
        dados.pessoas_envolvidas = list(set(pessoas))[:5]  # Limitar a 5

        # Tentar extrair razão social (antes de CNPJ ou em linhas específicas)
        razao_social = self._extrair_razao_social(texto)
        if razao_social:
            dados.razao_social = razao_social

        return dados

    def _extrair_razao_social(self, texto: str) -> Optional[str]:
        """Tenta extrair razão social do texto."""
        # Padrão: procurar por "Fornecedor:" ou similar
        padrao = r'(?:Fornecedor|Empresa|Razão Social):\s*([A-Za-zÀ-ú0-9\s\-]+)'
        match = re.search(padrao, texto, re.IGNORECASE)
        if match:
            return match.group(1).strip()

        # Padrão: linha antes do CNPJ
        if re.search(self.REGEX_CNPJ, texto):
            linhas = texto.split('\n')
            for i, linha in enumerate(linhas):
                if re.search(self.REGEX_CNPJ, linha) and i > 0:
                    linha_anterior = linhas[i-1].strip()
                    # Se a linha anterior tem caracteres razoáveis
                    if 10 < len(linha_anterior) < 100 and not re.match(r'^[A-Z\s:]+$', linha_anterior):
                        return linha_anterior

        return None

    def extrair_de_arquivo(self, caminho_arquivo: str) -> DadosExtraidos:
        """
        Extrai dados de um arquivo de email.

        Args:
            caminho_arquivo: Caminho para arquivo .txt com conteúdo do email

        Returns:
            DadosExtraidos com informações encontradas
        """
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            texto = f.read()

        return self.extrair(texto)

    def processar_lote(self, diretorio: str) -> Dict[str, DadosExtraidos]:
        """
        Processa todos os emails em um diretório.

        Args:
            diretorio: Caminho do diretório com arquivos .txt

        Returns:
            Dict mapeando nome do arquivo -> dados extraídos
        """
        resultados = {}

        dir_path = Path(diretorio)
        for arquivo in dir_path.glob('*.txt'):
            dados = self.extrair_de_arquivo(str(arquivo))
            resultados[arquivo.name] = asdict(dados)

        return resultados


def main():
    """Função de teste."""
    import sys

    if len(sys.argv) < 2:
        print("Uso: python extrator_dados_email.py <arquivo_ou_diretorio>")
        print("\nExemplos:")
        print("  python extrator_dados_email.py email.txt")
        print("  python extrator_dados_email.py /tmp/emails_26_049/")
        sys.exit(1)

    caminho = sys.argv[1]
    extrator = ExtratorDadosEmail()

    if Path(caminho).is_dir():
        print(f"Processando diretório: {caminho}\n")
        resultados = extrator.processar_lote(caminho)

        print(f"✓ Processados {len(resultados)} arquivos\n")
        print("="*70)

        for arquivo, dados in resultados.items():
            print(f"\n📧 {arquivo}")
            print("-"*70)

            if dados['cnpj']:
                print(f"  CNPJ: {dados['cnpj']}")
            if dados['razao_social']:
                print(f"  Razão Social: {dados['razao_social']}")
            if dados['telefone']:
                print(f"  Telefones: {', '.join(dados['telefone'])}")
            if dados['email']:
                print(f"  Emails: {', '.join(dados['email'])}")
            if dados['valores']:
                print(f"  Valores: {', '.join(dados['valores'])}")
            if dados['condicoes_pagamento']:
                print(f"  Pagamento: {dados['condicoes_pagamento'][:60]}...")
            if dados['localizacao']:
                print(f"  Localização: {dados['localizacao']}")

        # Salvar JSON
        output_file = "dados_extraidos.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(resultados, f, indent=2, ensure_ascii=False)

        print(f"\n{'='*70}")
        print(f"✓ Resultados salvos em: {output_file}")

    else:
        print(f"Processando arquivo: {caminho}\n")
        dados = extrator.extrair_de_arquivo(caminho)

        print("="*70)
        print("DADOS EXTRAÍDOS")
        print("="*70)
        print(json.dumps(asdict(dados), indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
