#!/usr/bin/env python3
"""
Data Preparer - Preparação e limpeza de dados

Este módulo processa dados brutos (emails, HTML, texto) e os converte em
formato limpo e estruturado para otimizar o processamento por IA.

Responsabilidades:
- Remover HTML mantendo formatação legível
- Detectar e remover assinaturas de email
- Extrair metadados via regex (CNPJ, telefone, email, CEP)
- Consolidar informações em arquivo .md estruturado

Uso:
    preparer = DataPreparer()
    result = preparer.preparar_email("email.html", "output.md")
"""

import os
import re
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime

try:
    from bs4 import BeautifulSoup
    import html2text
except ImportError:
    raise ImportError(
        "Dependências faltando. Instale com: "
        "pip install beautifulsoup4 html2text lxml"
    )

logger = logging.getLogger(__name__)


class DataPreparerError(Exception):
    """Exceção base para erros do DataPreparer."""
    pass


class DataPreparer:
    """
    Prepara e limpa dados brutos para processamento eficiente.

    Reduz significativamente o número de tokens necessários para IA
    ao remover ruído e extrair metadados estruturados previamente.
    """

    # Padrões regex para dados brasileiros
    PATTERNS = {
        'cnpj': r'\b\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}\b',
        'cpf': r'\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b',
        'telefone': r'\(?\d{2}\)?\s?\d{4,5}-?\d{4}',
        'email': r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b',
        'cep': r'\b\d{5}-?\d{3}\b',
        'data_br': r'\b\d{2}/\d{2}/\d{4}\b',
        'valor_monetario': r'R\$\s?\d{1,3}(?:\.\d{3})*(?:,\d{2})?',
        'url': r'https?://[^\s<>"{}|\\^`\[\]]+',
    }

    # Padrões comuns de assinaturas
    SIGNATURE_PATTERNS = [
        r'--\s*$',  # -- (separador comum)
        r'Enviado do meu iPhone',
        r'Sent from my iPhone',
        r'Enviado via Gmail',
        r'Get Outlook for',
        r'Atenciosamente,?\s*$',
        r'Cordialmente,?\s*$',
        r'Att\.?,?\s*$',
        r'Abraços,?\s*$',
    ]

    # Disclaimers legais comuns
    DISCLAIMER_PATTERNS = [
        r'AVISO LEGAL:.*?(?=\n\n|\Z)',
        r'CONFIDENCIAL:.*?(?=\n\n|\Z)',
        r'Este e-mail.*?destinatário.*?(?=\n\n|\Z)',
        r'This email.*?intended recipient.*?(?=\n\n|\Z)',
    ]

    def __init__(self):
        """Inicializa o DataPreparer."""
        # Configurar html2text
        self.html_converter = html2text.HTML2Text()
        self.html_converter.ignore_links = False
        self.html_converter.ignore_images = True
        self.html_converter.ignore_emphasis = False
        self.html_converter.body_width = 0  # Não quebrar linhas
        self.html_converter.unicode_snob = True

    def limpar_html(self, html: str) -> str:
        """
        Remove HTML e retorna texto limpo.

        Args:
            html: String HTML

        Returns:
            Texto limpo em Markdown

        Exemplo:
            >>> preparer = DataPreparer()
            >>> texto = preparer.limpar_html("<p>Olá <b>mundo</b>!</p>")
            >>> print(texto)
            'Olá **mundo**!'
        """
        try:
            # Usar BeautifulSoup para parse robusto
            soup = BeautifulSoup(html, 'lxml')

            # Remover scripts e styles
            for tag in soup(['script', 'style', 'meta', 'link']):
                tag.decompose()

            # Converter para string HTML limpo
            html_limpo = str(soup)

            # Converter para Markdown
            markdown = self.html_converter.handle(html_limpo)

            # Limpeza adicional
            markdown = self._limpar_markdown(markdown)

            return markdown

        except Exception as e:
            logger.warning(f"Erro ao limpar HTML: {e}")
            # Fallback: remover tags brutalmente
            return re.sub(r'<[^>]+>', '', html)

    def _limpar_markdown(self, markdown: str) -> str:
        """
        Limpa markdown gerado pelo html2text.

        Args:
            markdown: String Markdown

        Returns:
            Markdown limpo
        """
        # Remover linhas vazias consecutivas (mais de 2)
        markdown = re.sub(r'\n{3,}', '\n\n', markdown)

        # Remover espaços no final das linhas
        markdown = re.sub(r' +\n', '\n', markdown)

        # Remover espaços múltiplos
        markdown = re.sub(r' {2,}', ' ', markdown)

        # Remover caracteres de controle
        markdown = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f]', '', markdown)

        return markdown.strip()

    def remover_assinatura(self, texto: str) -> str:
        """
        Detecta e remove assinatura de email.

        Usa heurísticas para identificar onde começa a assinatura:
        - Padrões comuns (Atenciosamente, Att, --)
        - Múltiplas linhas curtas no final
        - Informações de contato agrupadas

        Args:
            texto: Texto do email

        Returns:
            Texto sem assinatura

        Exemplo:
            >>> texto = "Conteúdo do email\\n\\nAtenciosamente,\\nJoão Silva"
            >>> preparer.remover_assinatura(texto)
            'Conteúdo do email'
        """
        linhas = texto.split('\n')

        # Procurar por padrões de assinatura
        for i, linha in enumerate(linhas):
            for pattern in self.SIGNATURE_PATTERNS:
                if re.search(pattern, linha, re.IGNORECASE | re.MULTILINE):
                    # Encontrou início de assinatura
                    logger.debug(f"Assinatura detectada na linha {i}: {linha[:50]}")
                    # Retornar apenas conteúdo até essa linha
                    return '\n'.join(linhas[:i]).strip()

        # Heurística adicional: se últimas 5 linhas são todas curtas (<40 chars)
        # e contêm telefone ou email, provavelmente é assinatura
        if len(linhas) > 5:
            ultimas_linhas = linhas[-5:]
            linhas_curtas = sum(1 for l in ultimas_linhas if len(l.strip()) < 40)
            tem_contato = any(
                re.search(self.PATTERNS['telefone'], l) or
                re.search(self.PATTERNS['email'], l)
                for l in ultimas_linhas
            )

            if linhas_curtas >= 4 and tem_contato:
                logger.debug("Assinatura detectada por heurística")
                return '\n'.join(linhas[:-5]).strip()

        return texto

    def remover_disclaimers(self, texto: str) -> str:
        """
        Remove disclaimers legais comuns.

        Args:
            texto: Texto do email

        Returns:
            Texto sem disclaimers
        """
        for pattern in self.DISCLAIMER_PATTERNS:
            texto = re.sub(pattern, '', texto, flags=re.IGNORECASE | re.DOTALL)

        return texto.strip()

    def remover_thread_antiga(self, texto: str) -> str:
        """
        Remove threads antigas de email (replies anteriores).

        Detecta padrões como:
        - "Em 25/01/2026, João escreveu:"
        - "On Mon, Jan 25, 2026 at 2:30 PM"
        - "> texto citado"

        Args:
            texto: Texto do email

        Returns:
            Apenas a mensagem mais recente
        """
        # Padrões de início de thread antiga
        thread_patterns = [
            r'Em \d{2}/\d{2}/\d{4}.*?escreveu:',
            r'On .+? wrote:',
            r'De:.*?Enviado:.*?Para:.*?Assunto:',
            r'From:.*?Sent:.*?To:.*?Subject:',
            r'-+ ?Original Message ?-+',
            r'-+ ?Mensagem Original ?-+',
        ]

        for pattern in thread_patterns:
            match = re.search(pattern, texto, re.IGNORECASE | re.MULTILINE | re.DOTALL)
            if match:
                # Retornar apenas texto antes do match
                logger.debug(f"Thread antiga detectada: {match.group()[:50]}")
                return texto[:match.start()].strip()

        # Remover linhas citadas (começam com >)
        linhas = texto.split('\n')
        linhas_sem_citacao = [l for l in linhas if not l.strip().startswith('>')]

        return '\n'.join(linhas_sem_citacao)

    def extrair_metadados(self, texto: str) -> Dict[str, List[str]]:
        """
        Extrai metadados estruturados via regex.

        Args:
            texto: Texto para processar

        Returns:
            Dict com listas de valores encontrados:
            {
                "cnpj": ["12.345.678/0001-90"],
                "telefones": ["(11) 98765-4321", "(11) 3456-7890"],
                "emails": ["contato@empresa.com"],
                "ceps": ["01234-567"],
                "datas": ["25/01/2026"],
                "valores": ["R$ 15.000,00"],
                "urls": ["https://exemplo.com"]
            }

        Exemplo:
            >>> texto = "CNPJ: 12.345.678/0001-90 Tel: (11) 98765-4321"
            >>> metadados = preparer.extrair_metadados(texto)
            >>> print(metadados['cnpj'])
            ['12.345.678/0001-90']
        """
        metadados = {
            'cnpj': [],
            'cpf': [],
            'telefones': [],
            'emails': [],
            'ceps': [],
            'datas': [],
            'valores': [],
            'urls': []
        }

        # Extrair cada tipo de dado
        for tipo, pattern in self.PATTERNS.items():
            matches = re.findall(pattern, texto)
            if matches:
                # Normalizar e deduplica
                matches_unicos = list(set(self._normalizar_match(m, tipo) for m in matches))

                # Mapear nome do pattern para chave do dict
                if tipo == 'cnpj':
                    metadados['cnpj'] = matches_unicos
                elif tipo == 'cpf':
                    metadados['cpf'] = matches_unicos
                elif tipo == 'telefone':
                    metadados['telefones'] = matches_unicos
                elif tipo == 'email':
                    metadados['emails'] = matches_unicos
                elif tipo == 'cep':
                    metadados['ceps'] = matches_unicos
                elif tipo == 'data_br':
                    metadados['datas'] = matches_unicos
                elif tipo == 'valor_monetario':
                    metadados['valores'] = matches_unicos
                elif tipo == 'url':
                    metadados['urls'] = matches_unicos

        return metadados

    def _normalizar_match(self, match: str, tipo: str) -> str:
        """
        Normaliza valor extraído para formato padrão.

        Args:
            match: Valor encontrado
            tipo: Tipo de dado (cnpj, telefone, etc)

        Returns:
            Valor normalizado
        """
        if tipo == 'cnpj':
            # Remover pontuação e reformatar
            digitos = re.sub(r'\D', '', match)
            if len(digitos) == 14:
                return f"{digitos[:2]}.{digitos[2:5]}.{digitos[5:8]}/{digitos[8:12]}-{digitos[12:]}"
            return match

        elif tipo == 'cpf':
            digitos = re.sub(r'\D', '', match)
            if len(digitos) == 11:
                return f"{digitos[:3]}.{digitos[3:6]}.{digitos[6:9]}-{digitos[9:]}"
            return match

        elif tipo == 'telefone':
            digitos = re.sub(r'\D', '', match)
            if len(digitos) == 11:  # Celular
                return f"({digitos[:2]}) {digitos[2:7]}-{digitos[7:]}"
            elif len(digitos) == 10:  # Fixo
                return f"({digitos[:2]}) {digitos[2:6]}-{digitos[6:]}"
            return match

        elif tipo == 'cep':
            digitos = re.sub(r'\D', '', match)
            if len(digitos) == 8:
                return f"{digitos[:5]}-{digitos[5:]}"
            return match

        return match

    def preparar_email(
        self,
        input_path: str,
        output_path: Optional[str] = None,
        metadados_adicionais: Optional[Dict] = None
    ) -> Dict:
        """
        Pipeline completo de preparação de email.

        Args:
            input_path: Caminho do arquivo de entrada (.txt, .html, .eml)
            output_path: Caminho do arquivo de saída .md (opcional)
            metadados_adicionais: Metadados extras para incluir (ex: de GmailClient)

        Returns:
            Dict com resultado:
            {
                "texto_limpo": str,
                "metadados": dict,
                "output_file": str,
                "tokens_estimados_antes": int,
                "tokens_estimados_depois": int,
                "reducao_percentual": float
            }

        Exemplo:
            >>> result = preparer.preparar_email(
            ...     "emails/email_123.html",
            ...     "prepared/email_123.md"
            ... )
            >>> print(f"Redução: {result['reducao_percentual']:.1f}%")
        """
        logger.info(f"Preparando email: {input_path}")

        # Ler arquivo
        with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
            conteudo_original = f.read()

        tokens_antes = self._estimar_tokens(conteudo_original)

        # Detectar formato e processar
        if input_path.endswith('.html'):
            texto = self.limpar_html(conteudo_original)
        else:
            texto = conteudo_original

        # Pipeline de limpeza
        texto = self.remover_thread_antiga(texto)
        texto = self.remover_disclaimers(texto)
        texto = self.remover_assinatura(texto)

        # Limpeza final
        texto = self._limpar_markdown(texto)

        # Truncar se muito longo (> 2000 palavras)
        palavras = texto.split()
        if len(palavras) > 2000:
            logger.warning(f"Texto muito longo ({len(palavras)} palavras), truncando para 2000")
            texto = ' '.join(palavras[:2000]) + "\n\n[...texto truncado...]"

        # Extrair metadados
        metadados = self.extrair_metadados(texto)

        # Mesclar com metadados adicionais
        if metadados_adicionais:
            metadados.update(metadados_adicionais)

        # Gerar markdown estruturado
        markdown = self._gerar_markdown_estruturado(texto, metadados, input_path)

        tokens_depois = self._estimar_tokens(markdown)
        reducao = ((tokens_antes - tokens_depois) / tokens_antes * 100) if tokens_antes > 0 else 0

        logger.info(f"Tokens: {tokens_antes} → {tokens_depois} (redução: {reducao:.1f}%)")

        # Salvar se output_path fornecido
        if output_path:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(markdown)
            logger.info(f"Arquivo salvo: {output_path}")
        else:
            # Gerar nome automático
            output_path = input_path.rsplit('.', 1)[0] + '_preparado.md'
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(markdown)

        return {
            'texto_limpo': texto,
            'metadados': metadados,
            'output_file': output_path,
            'tokens_estimados_antes': tokens_antes,
            'tokens_estimados_depois': tokens_depois,
            'reducao_percentual': reducao
        }

    def preparar_pasta(
        self,
        pasta_path: str,
        output_path: Optional[str] = None
    ) -> Dict:
        """
        Processa todos os arquivos de uma pasta e consolida.

        Args:
            pasta_path: Caminho da pasta com emails
            output_path: Caminho do arquivo consolidado (opcional)

        Returns:
            Dict com resultado consolidado

        Exemplo:
            >>> result = preparer.preparar_pasta("drive/26_062/emails")
        """
        logger.info(f"Preparando pasta: {pasta_path}")

        # Encontrar todos os arquivos de texto/html
        arquivos = []
        for ext in ['*.txt', '*.html', '*.eml']:
            arquivos.extend(Path(pasta_path).glob(ext))

        if not arquivos:
            raise DataPreparerError(f"Nenhum arquivo encontrado em {pasta_path}")

        logger.info(f"Encontrados {len(arquivos)} arquivos")

        # Processar cada arquivo
        textos_limpos = []
        metadados_consolidados = {
            'cnpj': set(),
            'cpf': set(),
            'telefones': set(),
            'emails': set(),
            'ceps': set(),
            'datas': set(),
            'valores': set(),
            'urls': set()
        }

        for arquivo in sorted(arquivos):
            try:
                result = self.preparar_email(str(arquivo))
                textos_limpos.append(result['texto_limpo'])

                # Consolidar metadados (usar set para evitar duplicatas)
                for chave, valores in result['metadados'].items():
                    if chave in metadados_consolidados:
                        metadados_consolidados[chave].update(valores)

            except Exception as e:
                logger.error(f"Erro ao processar {arquivo}: {e}")
                continue

        # Converter sets para listas
        metadados_finais = {k: list(v) for k, v in metadados_consolidados.items()}

        # Consolidar textos
        texto_consolidado = '\n\n---\n\n'.join(textos_limpos)

        # Gerar markdown final
        markdown = self._gerar_markdown_estruturado(
            texto_consolidado,
            metadados_finais,
            pasta_path
        )

        # Salvar
        if not output_path:
            output_path = os.path.join(pasta_path, 'dados_preparados.md')

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown)

        logger.info(f"Pasta processada e salva em: {output_path}")

        return {
            'texto_limpo': texto_consolidado,
            'metadados': metadados_finais,
            'output_file': output_path,
            'arquivos_processados': len(arquivos)
        }

    def _gerar_markdown_estruturado(
        self,
        texto: str,
        metadados: Dict,
        fonte: str
    ) -> str:
        """
        Gera markdown estruturado para processamento por IA.

        Args:
            texto: Texto limpo
            metadados: Dict com metadados extraídos
            fonte: Caminho do arquivo original

        Returns:
            Markdown formatado
        """
        # Cabeçalho
        md = f"# Dados Preparados\n\n"
        md += f"**Fonte:** {fonte}\n"
        md += f"**Data de Processamento:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        md += "---\n\n"

        # Metadados detectados
        md += "## Metadados Detectados Automaticamente\n\n"

        tem_metadados = False

        if metadados.get('cnpj'):
            md += f"- **CNPJ:** {', '.join(metadados['cnpj'])}\n"
            tem_metadados = True

        if metadados.get('cpf'):
            md += f"- **CPF:** {', '.join(metadados['cpf'])}\n"
            tem_metadados = True

        if metadados.get('telefones'):
            md += f"- **Telefones:** {', '.join(metadados['telefones'])}\n"
            tem_metadados = True

        if metadados.get('emails'):
            # Filtrar emails comuns de sistema
            emails_relevantes = [
                e for e in metadados['emails']
                if not any(x in e.lower() for x in ['noreply', 'no-reply', 'mailer-daemon'])
            ]
            if emails_relevantes:
                md += f"- **Emails:** {', '.join(emails_relevantes)}\n"
                tem_metadados = True

        if metadados.get('ceps'):
            md += f"- **CEPs:** {', '.join(metadados['ceps'])}\n"
            tem_metadados = True

        if metadados.get('datas'):
            md += f"- **Datas Mencionadas:** {', '.join(metadados['datas'][:5])}\n"  # Máx 5
            tem_metadados = True

        if metadados.get('valores'):
            md += f"- **Valores Monetários:** {', '.join(metadados['valores'][:5])}\n"  # Máx 5
            tem_metadados = True

        if not tem_metadados:
            md += "*Nenhum metadado estruturado detectado*\n"

        md += "\n---\n\n"

        # Conteúdo principal
        md += "## Conteúdo Principal\n\n"
        md += texto
        md += "\n"

        return md

    def _estimar_tokens(self, texto: str) -> int:
        """
        Estima número de tokens (aproximado).

        Heurística: ~4 caracteres por token em português.

        Args:
            texto: Texto para estimar

        Returns:
            Número aproximado de tokens
        """
        return len(texto) // 4


def main():
    """
    Função principal para testar o preparer via CLI.

    Uso:
        python prepare_data.py arquivo.html
        python prepare_data.py pasta/
    """
    import sys
    import argparse

    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    parser = argparse.ArgumentParser(description='Data Preparer - Preparação de Dados')
    parser.add_argument('input', help='Arquivo ou pasta para processar')
    parser.add_argument('-o', '--output', help='Arquivo de saída (opcional)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Modo verbose')

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        preparer = DataPreparer()

        # Verificar se é arquivo ou pasta
        if os.path.isfile(args.input):
            print(f"\n{'='*70}")
            print(f"Processando arquivo: {args.input}")
            print(f"{'='*70}\n")

            result = preparer.preparar_email(args.input, args.output)

            print(f"\n✓ Processamento concluído!")
            print(f"\nEstatísticas:")
            print(f"  Tokens antes:  {result['tokens_estimados_antes']:,}")
            print(f"  Tokens depois: {result['tokens_estimados_depois']:,}")
            print(f"  Redução:       {result['reducao_percentual']:.1f}%")
            print(f"\nMetadados encontrados:")
            for chave, valores in result['metadados'].items():
                if valores:
                    print(f"  {chave}: {len(valores)} item(s)")
            print(f"\nArquivo salvo: {result['output_file']}")

        elif os.path.isdir(args.input):
            print(f"\n{'='*70}")
            print(f"Processando pasta: {args.input}")
            print(f"{'='*70}\n")

            result = preparer.preparar_pasta(args.input, args.output)

            print(f"\n✓ Processamento concluído!")
            print(f"\nEstatísticas:")
            print(f"  Arquivos processados: {result['arquivos_processados']}")
            print(f"\nMetadados consolidados:")
            for chave, valores in result['metadados'].items():
                if valores:
                    print(f"  {chave}: {len(valores)} item(s)")
            print(f"\nArquivo salvo: {result['output_file']}")

        else:
            print(f"✗ Erro: {args.input} não é arquivo nem pasta válida")
            sys.exit(1)

    except Exception as e:
        print(f"\n✗ Erro: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
