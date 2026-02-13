#!/usr/bin/env python3
"""
Gmail MCP Server - Expondo GmailClient via Model Context Protocol.

Este servidor permite que uma IA busque, leia e gerencie emails 
utilizando a infraestrutura já existente no projeto.
"""

import os
import sys
import json
from typing import Optional, List
from mcp.server.fastmcp import FastMCP

# Garantir que o diretório src está no path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.gmail_client import GmailClient

# Inicializar FastMCP
mcp = FastMCP("Gmail-Manager")

def get_client():
    """Retorna uma instância do GmailClient garantindo que os arquivos existem."""
    client = GmailClient(
        credentials_file="config/gmail_credentials.json",
        token_file="config/gmail_token.pickle"
    )
    return client

@mcp.tool()
def search_emails(query: str, max_results: int = 10) -> str:
    """
    Busca emails no Gmail usando a sintaxe de busca padrão do Gmail.
    
    Args:
        query: A query de busca (ex: "from:cliente@email.com", "subject:orçamento", "is:unread").
        max_results: Quantidade máxima de emails a retornar (padrão 10).
    """
    try:
        client = get_client()
        client.authenticate()
        emails = client.buscar_emails(query, max_results=max_results)
        if not emails:
            return "Nenhum email encontrado para esta busca."
        
        return json.dumps(emails, indent=2, ensure_ascii=False)
    except Exception as e:
        return f"Erro ao buscar emails: {str(e)}"

@mcp.tool()
def read_email_content(email_id: str) -> str:
    """
    Lê o conteúdo textual de um email específico pelo seu ID.
    
    Args:
        email_id: O ID único do email (obtido via search_emails).
    """
    try:
        client = get_client()
        client.authenticate()
        # Usamos o método interno de extração para retornar o texto diretamente para a IA
        msg = client.service.users().messages().get(
            userId='me',
            id=email_id,
            format='full'
        ).execute()
        
        content = client._extract_email_content(msg, format="txt")
        return content
    except Exception as e:
        return f"Erro ao ler email: {str(e)}"

@mcp.tool()
def list_threads(query: str, max_results: int = 5) -> str:
    """
    Lista threads (conversas agrupadas) baseadas em uma busca.
    """
    try:
        client = get_client()
        client.authenticate()
        results = client.service.users().threads().list(
            userId='me', q=query, maxResults=max_results
        ).execute()
        threads = results.get('threads', [])
        return json.dumps(threads, indent=2)
    except Exception as e:
        return f"Erro ao listar threads: {str(e)}"

@mcp.tool()
def mark_as_read(email_id: str) -> str:
    """
    Marca um email como lido (remove a label UNREAD).
    """
    try:
        client = get_client()
        client.authenticate()
        client.service.users().messages().modify(
            userId='me',
            id=email_id,
            body={'removeLabelIds': ['UNREAD']}
        ).execute()
        return f"Email {email_id} marcado como lido."
    except Exception as e:
        return f"Erro ao marcar como lido: {str(e)}"

if __name__ == "__main__":
    # Rodar o servidor
    mcp.run()
