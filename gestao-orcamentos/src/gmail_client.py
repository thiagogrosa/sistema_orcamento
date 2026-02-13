#!/usr/bin/env python3
"""
Gmail Client - Autenticação e acesso à Gmail API

Este módulo gerencia toda comunicação com Gmail API usando OAuth 2.0,
incluindo busca de emails, download de mensagens e extração de anexos.

Uso:
    client = GmailClient()
    client.authenticate()
    emails = client.buscar_emails("from:cliente@empresa.com", max_results=10)
"""

import os
import json
import base64
import pickle
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Literal
from email.mime.text import MIMEText

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)

logger = logging.getLogger(__name__)

# Scopes necessários (somente leitura por segurança)
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.modify'  # Para marcar como lido
]


class GmailClientError(Exception):
    """Exceção base para erros do Gmail Client."""
    pass


class AuthenticationError(GmailClientError):
    """Erro durante autenticação OAuth."""
    pass


class EmailNotFoundError(GmailClientError):
    """Email não encontrado."""
    pass


class GmailClient:
    """
    Cliente para interagir com Gmail API.

    Gerencia autenticação OAuth 2.0 e fornece métodos para:
    - Buscar emails por query
    - Baixar emails em diferentes formatos
    - Extrair anexos
    - Acessar threads de conversas

    Attributes:
        service: Objeto do serviço Gmail API
        credentials: Credenciais OAuth 2.0
    """

    def __init__(
        self,
        credentials_file: str = "config/gmail_credentials.json",
        token_file: str = "config/gmail_token.pickle"
    ):
        """
        Inicializa cliente Gmail.

        Args:
            credentials_file: Caminho para arquivo credentials.json do Google Cloud
            token_file: Caminho para salvar/carregar token de acesso
        """
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.service = None
        self.credentials = None

        # Verificar se arquivo de credenciais existe ou se temos variáveis de ambiente
        if not os.path.exists(credentials_file):
            if not (os.environ.get("GOOGLE_CLIENT_ID") and os.environ.get("GOOGLE_CLIENT_SECRET")):
                raise AuthenticationError(
                    f"Arquivo de credenciais não encontrado: {credentials_file}\n"
                    f"E variáveis GOOGLE_CLIENT_ID/GOOGLE_CLIENT_SECRET não definidas.\n"
                    f"Veja docs/SETUP_GMAIL_API.md para instruções de configuração."
                )
            else:
                logger.info("Arquivo de credenciais não encontrado, usará variáveis de ambiente.")

    def authenticate(self) -> bool:
        """
        Executa fluxo de autenticação OAuth 2.0.

        Se já existe token válido, usa ele. Caso contrário, abre navegador
        para o usuário autorizar o acesso.

        Returns:
            True se autenticação bem-sucedida

        Raises:
            AuthenticationError: Se falhar na autenticação
        """
        creds = None

        # Tentar carregar token salvo
        if os.path.exists(self.token_file):
            logger.info(f"Carregando token salvo de {self.token_file}")
            with open(self.token_file, 'rb') as token:
                creds = pickle.load(token)

        # Se não tem credenciais válidas, fazer login
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                logger.info("Token expirado, renovando...")
                try:
                    creds.refresh(Request())
                    logger.info("Token renovado com sucesso")
                except Exception as e:
                    logger.error(f"Erro ao renovar token: {e}")
                    # Se falhar renovação, fazer novo login
                    creds = None

            if not creds:
                logger.info("Iniciando fluxo de autenticação OAuth...")
                try:
                    if os.path.exists(self.credentials_file):
                        flow = InstalledAppFlow.from_client_secrets_file(
                            self.credentials_file,
                            SCOPES
                        )
                    else:
                        # Usar variáveis de ambiente
                        client_config = {
                            "installed": {
                                "client_id": os.environ.get("GOOGLE_CLIENT_ID"),
                                "client_secret": os.environ.get("GOOGLE_CLIENT_SECRET"),
                                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                                "token_uri": "https://oauth2.googleapis.com/token",
                                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                                "redirect_uris": ["http://localhost"]
                            }
                        }
                        flow = InstalledAppFlow.from_client_config(
                            client_config,
                            SCOPES
                        )
                    
                    creds = flow.run_local_server(port=0)
                    logger.info("Autenticação concluída com sucesso")
                except Exception as e:
                    raise AuthenticationError(f"Erro na autenticação: {e}")

            # Salvar token para próximas execuções
            logger.info(f"Salvando token em {self.token_file}")
            os.makedirs(os.path.dirname(self.token_file), exist_ok=True)
            with open(self.token_file, 'wb') as token:
                pickle.dump(creds, token)

        self.credentials = creds

        # Criar serviço Gmail
        try:
            self.service = build('gmail', 'v1', credentials=creds)
            logger.info("Cliente Gmail inicializado com sucesso")
            return True
        except Exception as e:
            raise AuthenticationError(f"Erro ao criar serviço Gmail: {e}")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(HttpError)
    )
    def buscar_emails(
        self,
        query: str,
        max_results: int = 10,
        include_spam_trash: bool = False,
        label_ids: Optional[List[str]] = None
    ) -> List[Dict]:
        """
        Busca emails usando query do Gmail.

        Args:
            query: Query de busca (ex: "from:cliente@empresa.com subject:orçamento")
            max_results: Número máximo de resultados (padrão: 10)
            include_spam_trash: Incluir spam e lixeira (padrão: False)
            label_ids: Filtrar por labels específicas

        Returns:
            Lista de dicts com metadados dos emails:
            [
                {
                    "id": "18d1f2a3b4c5d6e7",
                    "thread_id": "18d1f2a3b4c5d6e7",
                    "subject": "Orçamento climatização",
                    "from": "João Silva <joao@empresa.com>",
                    "to": "orcamentos2@armant.com.br",
                    "date": "2026-01-25T14:30:00Z",
                    "snippet": "Prezados, gostaria de solicitar..."
                }
            ]

        Raises:
            GmailClientError: Se falhar na busca

        Exemplo:
            >>> client = GmailClient()
            >>> client.authenticate()
            >>> emails = client.buscar_emails(
            ...     "from:cliente@empresa.com subject:orçamento after:2026/01/01",
            ...     max_results=5
            ... )
        """
        if not self.service:
            raise GmailClientError("Cliente não autenticado. Execute authenticate() primeiro.")

        try:
            logger.info(f"Buscando emails: query='{query}', max={max_results}")

            # Construir parâmetros da busca
            params = {
                'userId': 'me',
                'q': query,
                'maxResults': max_results,
                'includeSpamTrash': include_spam_trash
            }

            if label_ids:
                params['labelIds'] = label_ids

            # Buscar IDs dos emails
            results = self.service.users().messages().list(**params).execute()
            messages = results.get('messages', [])

            if not messages:
                logger.info("Nenhum email encontrado")
                return []

            logger.info(f"Encontrados {len(messages)} emails")

            # Obter metadados completos de cada email
            emails_data = []
            for msg in messages:
                try:
                    email_data = self._get_email_metadata(msg['id'])
                    emails_data.append(email_data)
                except Exception as e:
                    logger.warning(f"Erro ao obter metadados do email {msg['id']}: {e}")
                    continue

            return emails_data

        except HttpError as e:
            error_content = json.loads(e.content.decode('utf-8'))
            error_message = error_content.get('error', {}).get('message', str(e))
            logger.error(f"Erro HTTP ao buscar emails: {error_message}")
            raise GmailClientError(f"Erro ao buscar emails: {error_message}")
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar emails: {e}")
            raise GmailClientError(f"Erro ao buscar emails: {e}")

    def _get_email_metadata(self, email_id: str) -> Dict:
        """
        Obtém metadados de um email específico.

        Args:
            email_id: ID do email

        Returns:
            Dict com metadados do email
        """
        msg = self.service.users().messages().get(
            userId='me',
            id=email_id,
            format='metadata',
            metadataHeaders=['From', 'To', 'Subject', 'Date']
        ).execute()

        headers = {h['name']: h['value'] for h in msg['payload']['headers']}

        return {
            'id': msg['id'],
            'thread_id': msg['threadId'],
            'subject': headers.get('Subject', '(sem assunto)'),
            'from': headers.get('From', ''),
            'to': headers.get('To', ''),
            'date': headers.get('Date', ''),
            'snippet': msg.get('snippet', ''),
            'labels': msg.get('labelIds', [])
        }

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def baixar_email(
        self,
        email_id: str,
        output_dir: str,
        format: Literal["txt", "html", "raw"] = "txt",
        filename: Optional[str] = None
    ) -> str:
        """
        Baixa conteúdo de um email.

        Args:
            email_id: ID do email
            output_dir: Diretório onde salvar
            format: Formato do output ("txt", "html", ou "raw")
            filename: Nome do arquivo (opcional, gera automaticamente se None)

        Returns:
            Caminho do arquivo salvo

        Raises:
            EmailNotFoundError: Se email não existe
            GmailClientError: Se falhar no download

        Exemplo:
            >>> client.baixar_email(
            ...     "18d1f2a3b4c5d6e7",
            ...     "drive/26_062/emails",
            ...     format="txt"
            ... )
            'drive/26_062/emails/email_18d1f2a3b4c5d6e7.txt'
        """
        if not self.service:
            raise GmailClientError("Cliente não autenticado. Execute authenticate() primeiro.")

        try:
            logger.info(f"Baixando email {email_id} (formato: {format})")

            # Obter email completo
            msg = self.service.users().messages().get(
                userId='me',
                id=email_id,
                format='full'
            ).execute()

            # Extrair conteúdo
            content = self._extract_email_content(msg, format)

            # Criar diretório se não existe
            os.makedirs(output_dir, exist_ok=True)

            # Gerar nome do arquivo
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"email_{email_id[:8]}_{timestamp}.{format}"

            filepath = os.path.join(output_dir, filename)

            # Salvar arquivo
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            logger.info(f"Email salvo em: {filepath}")
            return filepath

        except HttpError as e:
            if e.resp.status == 404:
                raise EmailNotFoundError(f"Email {email_id} não encontrado")
            error_content = json.loads(e.content.decode('utf-8'))
            error_message = error_content.get('error', {}).get('message', str(e))
            raise GmailClientError(f"Erro ao baixar email: {error_message}")
        except Exception as e:
            logger.error(f"Erro ao baixar email {email_id}: {e}")
            raise GmailClientError(f"Erro ao baixar email: {e}")

    def _extract_email_content(
        self,
        msg: Dict,
        format: str
    ) -> str:
        """
        Extrai conteúdo do email no formato solicitado.

        Args:
            msg: Objeto message da API
            format: "txt", "html" ou "raw"

        Returns:
            Conteúdo do email como string
        """
        # Extrair headers para metadados
        headers = {h['name']: h['value'] for h in msg['payload']['headers']}

        metadata = f"""De: {headers.get('From', '')}
Para: {headers.get('To', '')}
Assunto: {headers.get('Subject', '')}
Data: {headers.get('Date', '')}

{'='*70}

"""

        # Extrair corpo do email
        parts = self._get_email_parts(msg['payload'])

        if format == "txt":
            # Preferir texto plano
            for part in parts:
                if part['mimeType'] == 'text/plain' and part['body']:
                    body = base64.urlsafe_b64decode(part['body']).decode('utf-8', errors='ignore')
                    return metadata + body

            # Se não tem texto plano, tentar HTML
            for part in parts:
                if part['mimeType'] == 'text/html' and part['body']:
                    body = base64.urlsafe_b64decode(part['body']).decode('utf-8', errors='ignore')
                    # Converter HTML para texto (básico)
                    import re
                    body = re.sub(r'<[^>]+>', '', body)  # Remove tags HTML
                    return metadata + body

            return metadata + "(conteúdo vazio)"

        elif format == "html":
            # Preferir HTML
            for part in parts:
                if part['mimeType'] == 'text/html' and part['body']:
                    body = base64.urlsafe_b64decode(part['body']).decode('utf-8', errors='ignore')
                    return metadata + body

            # Se não tem HTML, retornar texto
            for part in parts:
                if part['mimeType'] == 'text/plain' and part['body']:
                    body = base64.urlsafe_b64decode(part['body']).decode('utf-8', errors='ignore')
                    return metadata + f"<pre>{body}</pre>"

            return metadata + "<p>(conteúdo vazio)</p>"

        elif format == "raw":
            # Retornar raw (base64)
            if 'raw' in msg:
                return base64.urlsafe_b64decode(msg['raw']).decode('utf-8', errors='ignore')
            return metadata + str(msg)

        return metadata

    def _get_email_parts(self, payload: Dict) -> List[Dict]:
        """
        Extrai todas as partes de um email (recursivo para emails multipart).

        Args:
            payload: Payload do email

        Returns:
            Lista de partes do email
        """
        parts = []

        if 'parts' in payload:
            for part in payload['parts']:
                parts.extend(self._get_email_parts(part))
        else:
            parts.append({
                'mimeType': payload.get('mimeType', ''),
                'body': payload.get('body', {}).get('data', '')
            })

        return parts

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def extrair_anexos(
        self,
        email_id: str,
        output_dir: str
    ) -> List[str]:
        """
        Extrai todos os anexos de um email.

        Args:
            email_id: ID do email
            output_dir: Diretório onde salvar anexos

        Returns:
            Lista de caminhos dos arquivos salvos

        Raises:
            EmailNotFoundError: Se email não existe
            GmailClientError: Se falhar na extração

        Exemplo:
            >>> anexos = client.extrair_anexos(
            ...     "18d1f2a3b4c5d6e7",
            ...     "drive/26_062/anexos"
            ... )
            >>> print(anexos)
            ['drive/26_062/anexos/proposta.pdf', 'drive/26_062/anexos/planta.jpg']
        """
        if not self.service:
            raise GmailClientError("Cliente não autenticado. Execute authenticate() primeiro.")

        try:
            logger.info(f"Extraindo anexos do email {email_id}")

            # Obter email completo
            msg = self.service.users().messages().get(
                userId='me',
                id=email_id,
                format='full'
            ).execute()

            # Criar diretório se não existe
            os.makedirs(output_dir, exist_ok=True)

            # Encontrar e baixar anexos
            anexos_salvos = []
            parts = self._get_attachment_parts(msg['payload'])

            if not parts:
                logger.info("Email não possui anexos")
                return []

            logger.info(f"Encontrados {len(parts)} anexos")

            for i, part in enumerate(parts):
                filename = part.get('filename', f'anexo_{i+1}')
                attachment_id = part['body'].get('attachmentId')

                if attachment_id:
                    # Baixar anexo
                    attachment = self.service.users().messages().attachments().get(
                        userId='me',
                        messageId=email_id,
                        id=attachment_id
                    ).execute()

                    # Decodificar e salvar
                    file_data = base64.urlsafe_b64decode(attachment['data'])
                    filepath = os.path.join(output_dir, filename)

                    with open(filepath, 'wb') as f:
                        f.write(file_data)

                    logger.info(f"Anexo salvo: {filepath}")
                    anexos_salvos.append(filepath)

            return anexos_salvos

        except HttpError as e:
            if e.resp.status == 404:
                raise EmailNotFoundError(f"Email {email_id} não encontrado")
            error_content = json.loads(e.content.decode('utf-8'))
            error_message = error_content.get('error', {}).get('message', str(e))
            raise GmailClientError(f"Erro ao extrair anexos: {error_message}")
        except Exception as e:
            logger.error(f"Erro ao extrair anexos do email {email_id}: {e}")
            raise GmailClientError(f"Erro ao extrair anexos: {e}")

    def _get_attachment_parts(self, payload: Dict) -> List[Dict]:
        """
        Encontra todas as partes que são anexos (recursivo).

        Args:
            payload: Payload do email

        Returns:
            Lista de partes que são anexos
        """
        attachments = []

        if 'parts' in payload:
            for part in payload['parts']:
                attachments.extend(self._get_attachment_parts(part))
        else:
            # É um anexo se tem filename e attachmentId
            if payload.get('filename') and payload.get('body', {}).get('attachmentId'):
                attachments.append(payload)

        return attachments

    def get_thread(
        self,
        thread_id: str,
        format: Literal["minimal", "full"] = "minimal"
    ) -> Dict:
        """
        Obtém uma thread completa de conversa.

        Args:
            thread_id: ID da thread
            format: "minimal" (metadados) ou "full" (conteúdo completo)

        Returns:
            Dict com informações da thread

        Raises:
            GmailClientError: Se falhar ao obter thread

        Exemplo:
            >>> thread = client.get_thread("18d1f2a3b4c5d6e7")
            >>> print(f"Thread com {len(thread['messages'])} mensagens")
        """
        if not self.service:
            raise GmailClientError("Cliente não autenticado. Execute authenticate() primeiro.")

        try:
            logger.info(f"Obtendo thread {thread_id}")

            thread = self.service.users().threads().get(
                userId='me',
                id=thread_id,
                format=format
            ).execute()

            return thread

        except HttpError as e:
            error_content = json.loads(e.content.decode('utf-8'))
            error_message = error_content.get('error', {}).get('message', str(e))
            raise GmailClientError(f"Erro ao obter thread: {error_message}")
        except Exception as e:
            logger.error(f"Erro ao obter thread {thread_id}: {e}")
            raise GmailClientError(f"Erro ao obter thread: {e}")

    def buscar_emails_demanda(
        self,
        demanda_id: str,
        cliente: Optional[str] = None,
        after_date: Optional[str] = None
    ) -> List[Dict]:
        """
        Busca emails relacionados a uma demanda específica.

        Wrapper conveniente que constrói query automaticamente.

        Args:
            demanda_id: ID da demanda (ex: "26_062")
            cliente: Nome do cliente (opcional, melhora busca)
            after_date: Data mínima no formato YYYY/MM/DD

        Returns:
            Lista de emails encontrados

        Exemplo:
            >>> emails = client.buscar_emails_demanda(
            ...     "26_062",
            ...     cliente="Empresa XYZ",
            ...     after_date="2026/01/01"
            ... )
        """
        # Construir query
        query_parts = []

        # Buscar por menções ao ID ou cliente
        if cliente:
            query_parts.append(f'("{demanda_id}" OR "{cliente}")')
        else:
            query_parts.append(f'"{demanda_id}"')

        # Filtro de data
        if after_date:
            query_parts.append(f"after:{after_date}")

        # Buscar apenas em INBOX (ignora spam/trash)
        query_parts.append("in:inbox")

        query = " ".join(query_parts)

        return self.buscar_emails(query, max_results=20)


def main():
    """
    Função principal para testar o cliente ou executar setup.

    Uso:
        python gmail_client.py --setup    # Executar autenticação OAuth
        python gmail_client.py --test     # Testar busca de emails
    """
    import sys
    import argparse

    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    parser = argparse.ArgumentParser(description='Gmail Client - Setup e Testes')
    parser.add_argument('--setup', action='store_true', help='Executar setup de autenticação')
    parser.add_argument('--test', action='store_true', help='Testar busca de emails')
    parser.add_argument('--query', type=str, help='Query para teste de busca')

    args = parser.parse_args()

    try:
        client = GmailClient()

        if args.setup:
            print("\n" + "="*70)
            print("SETUP - Autenticação Gmail API")
            print("="*70)
            print("\nO navegador será aberto para você autorizar o acesso.")
            print("Após autorizar, volte para este terminal.\n")

            if client.authenticate():
                print("\n✓ Autenticação concluída com sucesso!")
                print(f"✓ Token salvo em: {client.token_file}")
                print("\nVocê pode agora usar o cliente normalmente.")
            else:
                print("\n✗ Falha na autenticação")
                sys.exit(1)

        elif args.test:
            print("\n" + "="*70)
            print("TESTE - Busca de Emails")
            print("="*70)

            client.authenticate()

            query = args.query or "is:inbox"
            print(f"\nBuscando emails com query: {query}")

            emails = client.buscar_emails(query, max_results=5)

            if emails:
                print(f"\n✓ Encontrados {len(emails)} emails:\n")
                for i, email in enumerate(emails, 1):
                    print(f"{i}. {email['subject']}")
                    print(f"   De: {email['from']}")
                    print(f"   Data: {email['date']}")
                    print(f"   Snippet: {email['snippet'][:80]}...")
                    print()
            else:
                print("\nNenhum email encontrado.")

        else:
            parser.print_help()

    except Exception as e:
        print(f"\n✗ Erro: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
