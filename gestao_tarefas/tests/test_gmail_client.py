#!/usr/bin/env python3
"""
Testes para GmailClient

Para rodar:
    pytest tests/test_gmail_client.py -v
"""

import pytest
import os
from unittest.mock import Mock, patch, MagicMock
from src.gmail_client import (
    GmailClient,
    GmailClientError,
    AuthenticationError,
    EmailNotFoundError
)


class TestGmailClientInit:
    """Testes de inicialização do cliente."""

    def test_init_with_default_paths(self):
        """Deve criar cliente com caminhos padrão."""
        with patch('os.path.exists', return_value=True):
            client = GmailClient()
            assert client.credentials_file == "config/gmail_credentials.json"
            assert client.token_file == "config/gmail_token.pickle"

    def test_init_with_custom_paths(self):
        """Deve aceitar caminhos customizados."""
        with patch('os.path.exists', return_value=True):
            client = GmailClient(
                credentials_file="custom/creds.json",
                token_file="custom/token.pickle"
            )
            assert client.credentials_file == "custom/creds.json"
            assert client.token_file == "custom/token.pickle"

    def test_init_without_credentials_file(self):
        """Deve lançar erro se arquivo de credenciais não existe."""
        with patch('os.path.exists', return_value=False):
            with pytest.raises(AuthenticationError) as exc:
                GmailClient()
            assert "não encontrado" in str(exc.value)


class TestGmailClientAuthentication:
    """Testes de autenticação."""

    @patch('src.gmail_client.build')
    @patch('os.path.exists')
    @patch('builtins.open')
    @patch('pickle.load')
    def test_authenticate_with_valid_token(
        self,
        mock_pickle_load,
        mock_open,
        mock_exists,
        mock_build
    ):
        """Deve usar token existente se válido."""
        # Setup
        mock_exists.side_effect = [True, True]  # credentials e token existem

        mock_creds = Mock()
        mock_creds.valid = True
        mock_pickle_load.return_value = mock_creds

        mock_service = Mock()
        mock_build.return_value = mock_service

        # Execute
        client = GmailClient()
        result = client.authenticate()

        # Assert
        assert result is True
        assert client.service == mock_service
        mock_build.assert_called_once_with('gmail', 'v1', credentials=mock_creds)

    @patch('src.gmail_client.InstalledAppFlow')
    @patch('src.gmail_client.build')
    @patch('os.path.exists')
    @patch('builtins.open')
    @patch('pickle.dump')
    @patch('os.makedirs')
    def test_authenticate_new_login(
        self,
        mock_makedirs,
        mock_pickle_dump,
        mock_open,
        mock_exists,
        mock_build,
        mock_flow_class
    ):
        """Deve fazer novo login se não tem token."""
        # Setup
        mock_exists.side_effect = [True, False]  # credentials existe, token não

        mock_creds = Mock()
        mock_creds.valid = True

        mock_flow = Mock()
        mock_flow.run_local_server.return_value = mock_creds
        mock_flow_class.from_client_secrets_file.return_value = mock_flow

        mock_service = Mock()
        mock_build.return_value = mock_service

        # Execute
        client = GmailClient()
        result = client.authenticate()

        # Assert
        assert result is True
        assert client.service == mock_service
        mock_flow.run_local_server.assert_called_once()


class TestGmailClientBuscarEmails:
    """Testes de busca de emails."""

    def setup_method(self):
        """Setup para cada teste."""
        with patch('os.path.exists', return_value=True):
            self.client = GmailClient()
            self.client.service = Mock()

    def test_buscar_emails_success(self):
        """Deve retornar lista de emails."""
        # Setup
        mock_messages = {
            'messages': [
                {'id': '123', 'threadId': 'thread1'},
                {'id': '456', 'threadId': 'thread2'}
            ]
        }

        self.client.service.users().messages().list().execute.return_value = mock_messages

        # Mock para _get_email_metadata
        with patch.object(self.client, '_get_email_metadata') as mock_metadata:
            mock_metadata.side_effect = [
                {
                    'id': '123',
                    'subject': 'Test 1',
                    'from': 'sender1@test.com',
                    'date': '2026-01-25'
                },
                {
                    'id': '456',
                    'subject': 'Test 2',
                    'from': 'sender2@test.com',
                    'date': '2026-01-26'
                }
            ]

            # Execute
            result = self.client.buscar_emails("test query", max_results=10)

            # Assert
            assert len(result) == 2
            assert result[0]['id'] == '123'
            assert result[1]['id'] == '456'

    def test_buscar_emails_no_results(self):
        """Deve retornar lista vazia se não encontrar emails."""
        # Setup
        self.client.service.users().messages().list().execute.return_value = {}

        # Execute
        result = self.client.buscar_emails("test query")

        # Assert
        assert result == []

    def test_buscar_emails_not_authenticated(self):
        """Deve lançar erro se não autenticado."""
        # Setup
        self.client.service = None

        # Execute & Assert
        with pytest.raises(GmailClientError) as exc:
            self.client.buscar_emails("test query")
        assert "não autenticado" in str(exc.value)


class TestGmailClientBaixarEmail:
    """Testes de download de emails."""

    def setup_method(self):
        """Setup para cada teste."""
        with patch('os.path.exists', return_value=True):
            self.client = GmailClient()
            self.client.service = Mock()

    @patch('builtins.open', create=True)
    @patch('os.makedirs')
    def test_baixar_email_txt_format(self, mock_makedirs, mock_open):
        """Deve baixar email em formato txt."""
        # Setup
        mock_msg = {
            'id': '123',
            'payload': {
                'headers': [
                    {'name': 'From', 'value': 'sender@test.com'},
                    {'name': 'To', 'value': 'receiver@test.com'},
                    {'name': 'Subject', 'value': 'Test Subject'},
                    {'name': 'Date', 'value': '2026-01-25'}
                ],
                'mimeType': 'text/plain',
                'body': {'data': 'VGVzdCBjb250ZW50'}  # "Test content" em base64
            }
        }

        self.client.service.users().messages().get().execute.return_value = mock_msg

        # Execute
        result = self.client.baixar_email(
            '123',
            'output',
            format='txt'
        )

        # Assert
        assert 'email_' in result
        assert result.endswith('.txt')
        mock_makedirs.assert_called_once_with('output', exist_ok=True)


class TestGmailClientExtrairAnexos:
    """Testes de extração de anexos."""

    def setup_method(self):
        """Setup para cada teste."""
        with patch('os.path.exists', return_value=True):
            self.client = GmailClient()
            self.client.service = Mock()

    def test_extrair_anexos_no_attachments(self):
        """Deve retornar lista vazia se não tem anexos."""
        # Setup
        mock_msg = {
            'id': '123',
            'payload': {
                'mimeType': 'text/plain',
                'body': {'data': 'test'}
            }
        }

        self.client.service.users().messages().get().execute.return_value = mock_msg

        # Execute
        result = self.client.extrair_anexos('123', 'output')

        # Assert
        assert result == []


class TestGmailClientBuscarEmailsDemanda:
    """Testes do helper buscar_emails_demanda."""

    def setup_method(self):
        """Setup para cada teste."""
        with patch('os.path.exists', return_value=True):
            self.client = GmailClient()
            self.client.service = Mock()

    @patch.object(GmailClient, 'buscar_emails')
    def test_buscar_emails_demanda_basic(self, mock_buscar):
        """Deve construir query e buscar emails."""
        # Setup
        mock_buscar.return_value = []

        # Execute
        self.client.buscar_emails_demanda('26_062')

        # Assert
        mock_buscar.assert_called_once()
        call_args = mock_buscar.call_args[0]
        assert '26_062' in call_args[0]
        assert 'in:inbox' in call_args[0]

    @patch.object(GmailClient, 'buscar_emails')
    def test_buscar_emails_demanda_with_cliente(self, mock_buscar):
        """Deve incluir nome do cliente na query."""
        # Setup
        mock_buscar.return_value = []

        # Execute
        self.client.buscar_emails_demanda('26_062', cliente='Empresa XYZ')

        # Assert
        call_args = mock_buscar.call_args[0]
        assert 'Empresa XYZ' in call_args[0]

    @patch.object(GmailClient, 'buscar_emails')
    def test_buscar_emails_demanda_with_date(self, mock_buscar):
        """Deve incluir filtro de data."""
        # Setup
        mock_buscar.return_value = []

        # Execute
        self.client.buscar_emails_demanda(
            '26_062',
            after_date='2026/01/01'
        )

        # Assert
        call_args = mock_buscar.call_args[0]
        assert 'after:2026/01/01' in call_args[0]


# ===== Testes de Integração (requerem autenticação real) =====

@pytest.mark.integration
@pytest.mark.skipif(
    not os.path.exists('config/gmail_token.pickle'),
    reason="Token não configurado. Execute: python src/gmail_client.py --setup"
)
class TestGmailClientIntegration:
    """
    Testes de integração com Gmail API real.

    Requer autenticação configurada.
    Para rodar: pytest tests/test_gmail_client.py -v -m integration
    """

    def setup_method(self):
        """Setup para testes de integração."""
        self.client = GmailClient()
        self.client.authenticate()

    def test_buscar_emails_real(self):
        """Teste real de busca de emails."""
        # Buscar últimos 5 emails
        emails = self.client.buscar_emails("is:inbox", max_results=5)

        # Verificar estrutura
        assert isinstance(emails, list)
        if emails:
            assert 'id' in emails[0]
            assert 'subject' in emails[0]
            assert 'from' in emails[0]

    def test_baixar_email_real(self, tmp_path):
        """Teste real de download de email."""
        # Primeiro buscar um email
        emails = self.client.buscar_emails("is:inbox", max_results=1)

        if not emails:
            pytest.skip("Nenhum email encontrado na inbox")

        email_id = emails[0]['id']

        # Baixar email
        filepath = self.client.baixar_email(
            email_id,
            str(tmp_path),
            format='txt'
        )

        # Verificar arquivo criado
        assert os.path.exists(filepath)

        # Verificar conteúdo
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            assert len(content) > 0
            assert 'De:' in content or 'From:' in content
