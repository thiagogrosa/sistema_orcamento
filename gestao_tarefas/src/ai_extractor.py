#!/usr/bin/env python3
"""
AI Extractor - Extração de dados usando Claude API

Este módulo gerencia a extração de informações estruturadas de texto
preparado usando Claude API (Haiku por padrão, com fallback para Sonnet).

Estratégia de custos:
- Haiku: $0.25/$1.25 por M tokens (~$0.0015 por demanda)
- Sonnet: $3/$15 por M tokens (~$0.024 por demanda)
- Fallback automático se Haiku falhar validação

Uso:
    extractor = AIExtractor()
    result = extractor.extrair(texto_preparado)
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Optional, Literal, Tuple
from datetime import datetime

try:
    from anthropic import Anthropic
    from pydantic import BaseModel, field_validator, ValidationError
except ImportError:
    raise ImportError(
        "Dependências faltando. Instale com: "
        "pip install anthropic pydantic"
    )

logger = logging.getLogger(__name__)


class AIExtractorError(Exception):
    """Exceção base para erros do AIExtractor."""
    pass


class ExtractionValidationError(AIExtractorError):
    """Erro de validação do JSON extraído."""
    pass


# ===== Schema Pydantic =====

class OrcamentoData(BaseModel):
    """
    Schema de validação para dados de orçamento.

    Garante que o JSON retornado pela IA está no formato correto.
    """
    cliente: str
    cnpj_cpf: Optional[str] = None
    contato: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None
    local: str
    prazo: Optional[str] = None
    tipo_servico: Literal["instalacao", "manutencao", "projeto"]
    eh_licitacao: bool = False
    numero_edital: Optional[str] = None
    porte: Optional[Literal["pequeno", "medio", "grande"]] = None
    origem: Literal["comercial", "cliente_direto", "diretoria", "engenharia"]
    descricao: str
    urgente: bool = False
    cliente_estrategico: bool = False

    @field_validator("prazo")
    @classmethod
    def validar_prazo(cls, v):
        """Valida formato de data (YYYY-MM-DD)."""
        if v is not None:
            try:
                datetime.strptime(v, "%Y-%m-%d")
            except ValueError:
                raise ValueError(f"Data inválida: {v}. Use formato YYYY-MM-DD")
        return v

    @field_validator("local")
    @classmethod
    def validar_local(cls, v):
        """Valida formato do local (Cidade - UF)."""
        if not v or " - " not in v:
            raise ValueError(
                f"Local inválido: '{v}'. Use formato: 'Cidade - UF'"
            )
        partes = v.split(" - ")
        if len(partes) != 2:
            raise ValueError(
                f"Local inválido: '{v}'. Use formato: 'Cidade - UF'"
            )
        return v

    @field_validator("cliente", "descricao")
    @classmethod
    def validar_nao_vazio(cls, v, info):
        """Valida que campos obrigatórios não estão vazios."""
        if not v or not v.strip():
            raise ValueError(f"Campo '{info.field_name}' não pode estar vazio")
        return v.strip()


# ===== AIExtractor =====

class AIExtractor:
    """
    Extrator de dados usando Claude API.

    Usa Haiku por padrão (barato e rápido), com fallback automático
    para Sonnet em casos complexos.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        force_sonnet: bool = False
    ):
        """
        Inicializa o extrator.

        Args:
            api_key: Claude API key (usa env var se não fornecida)
            force_sonnet: Se True, sempre usa Sonnet (para testes)
        """
        # Obter API key
        self.api_key = api_key or os.environ.get("CLAUDE_API_KEY")
        if not self.api_key:
            raise AIExtractorError(
                "CLAUDE_API_KEY não encontrada. "
                "Configure no .env ou passe como parâmetro."
            )

        # Inicializar cliente Anthropic
        self.client = Anthropic(api_key=self.api_key)

        self.force_sonnet = force_sonnet

        # Carregar prompts
        self.prompt_haiku = self._carregar_prompt("extracao_orcamento_haiku.txt")
        self.prompt_sonnet = self._carregar_prompt("extracao_orcamento_sonnet.txt")

        # Estatísticas da última chamada
        self.last_model_used = None
        self.last_tokens_input = 0
        self.last_tokens_output = 0
        self.last_cost_usd = 0.0

    def _carregar_prompt(self, filename: str) -> str:
        """
        Carrega template de prompt.

        Args:
            filename: Nome do arquivo em prompts/

        Returns:
            Conteúdo do prompt
        """
        prompt_path = Path(__file__).parent.parent / "prompts" / filename

        if not prompt_path.exists():
            raise AIExtractorError(f"Prompt não encontrado: {prompt_path}")

        with open(prompt_path, 'r', encoding='utf-8') as f:
            return f.read()

    def extrair(
        self,
        texto_preparado: str,
        tentar_sonnet_se_falhar: bool = True
    ) -> Dict:
        """
        Extrai dados estruturados do texto.

        Estratégia:
        1. Tentar com Haiku (rápido e barato)
        2. Validar resultado com Pydantic
        3. Se falhar, tentar com Sonnet (mais robusto)

        Args:
            texto_preparado: Texto limpo para processar
            tentar_sonnet_se_falhar: Se True, usa Sonnet como fallback

        Returns:
            Dict com dados extraídos e validados

        Raises:
            AIExtractorError: Se extração falhar completamente

        Exemplo:
            >>> extractor = AIExtractor()
            >>> texto = "Cliente ABC em SP, instalação de split..."
            >>> dados = extractor.extrair(texto)
            >>> print(dados['cliente'])
            'Cliente ABC'
        """
        logger.info("Iniciando extração de dados")

        # Tentar com Haiku primeiro (a menos que force_sonnet=True)
        if not self.force_sonnet:
            try:
                logger.info("Tentando extração com Haiku...")
                resultado = self._extrair_com_haiku(texto_preparado)
                logger.info("✓ Extração com Haiku bem-sucedida")
                return resultado
            except (ExtractionValidationError, json.JSONDecodeError) as e:
                logger.warning(f"Haiku falhou: {e}")
                if not tentar_sonnet_se_falhar:
                    raise
                logger.info("Tentando fallback para Sonnet...")
            except Exception as e:
                logger.error(f"Erro inesperado com Haiku: {e}")
                if not tentar_sonnet_se_falhar:
                    raise
                logger.info("Tentando fallback para Sonnet...")

        # Fallback para Sonnet ou uso direto se force_sonnet=True
        try:
            logger.info("Extraindo com Sonnet...")
            resultado = self._extrair_com_sonnet(texto_preparado)
            logger.info("✓ Extração com Sonnet bem-sucedida")
            return resultado
        except Exception as e:
            logger.error(f"Extração falhou completamente: {e}")
            raise AIExtractorError(f"Não foi possível extrair dados: {e}")

    def _extrair_com_haiku(self, texto: str) -> Dict:
        """
        Extrai dados usando Claude Haiku.

        Args:
            texto: Texto para processar

        Returns:
            Dict validado com dados extraídos
        """
        # Preparar prompt
        prompt = self.prompt_haiku.replace("{texto_preparado}", texto)

        # Chamar API
        response = self.client.messages.create(
            model="claude-haiku-4-20250514",
            max_tokens=1000,
            temperature=0,  # Determinístico
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # Extrair texto da resposta
        resposta_texto = response.content[0].text.strip()

        # Registrar estatísticas
        self.last_model_used = "haiku"
        self.last_tokens_input = response.usage.input_tokens
        self.last_tokens_output = response.usage.output_tokens
        self.last_cost_usd = self._calcular_custo(
            "haiku",
            self.last_tokens_input,
            self.last_tokens_output
        )

        logger.debug(f"Resposta Haiku ({self.last_tokens_output} tokens): {resposta_texto[:200]}")

        # Parse JSON
        try:
            dados = json.loads(resposta_texto)
        except json.JSONDecodeError as e:
            # Tentar extrair JSON de resposta com texto extra
            import re
            match = re.search(r'\{[^}]+\}', resposta_texto, re.DOTALL)
            if match:
                dados = json.loads(match.group())
            else:
                raise json.JSONDecodeError(
                    f"Resposta não é JSON válido: {resposta_texto[:200]}",
                    resposta_texto,
                    0
                )

        # Validar com Pydantic
        try:
            validado = OrcamentoData(**dados)
            return validado.model_dump()
        except ValidationError as e:
            raise ExtractionValidationError(f"Validação falhou: {e}")

    def _extrair_com_sonnet(self, texto: str) -> Dict:
        """
        Extrai dados usando Claude Sonnet (mais robusto).

        Args:
            texto: Texto para processar

        Returns:
            Dict validado com dados extraídos
        """
        # Preparar prompt
        prompt = self.prompt_sonnet.replace("{texto_preparado}", texto)

        # Chamar API
        response = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1500,
            temperature=0,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # Extrair texto da resposta
        resposta_texto = response.content[0].text.strip()

        # Registrar estatísticas
        self.last_model_used = "sonnet"
        self.last_tokens_input = response.usage.input_tokens
        self.last_tokens_output = response.usage.output_tokens
        self.last_cost_usd = self._calcular_custo(
            "sonnet",
            self.last_tokens_input,
            self.last_tokens_output
        )

        logger.debug(f"Resposta Sonnet ({self.last_tokens_output} tokens): {resposta_texto[:200]}")

        # Parse JSON
        try:
            dados = json.loads(resposta_texto)
        except json.JSONDecodeError as e:
            # Tentar extrair JSON de resposta com texto extra
            import re
            match = re.search(r'\{[^}]+\}', resposta_texto, re.DOTALL)
            if match:
                dados = json.loads(match.group())
            else:
                raise json.JSONDecodeError(
                    f"Resposta não é JSON válido: {resposta_texto[:200]}",
                    resposta_texto,
                    0
                )

        # Validar com Pydantic
        try:
            validado = OrcamentoData(**dados)
            return validado.model_dump()
        except ValidationError as e:
            raise ExtractionValidationError(f"Validação falhou: {e}")

    def _calcular_custo(
        self,
        modelo: Literal["haiku", "sonnet"],
        tokens_input: int,
        tokens_output: int
    ) -> float:
        """
        Calcula custo em USD da chamada.

        Preços (por 1M tokens):
        - Haiku: $0.25 input / $1.25 output
        - Sonnet: $3 input / $15 output

        Args:
            modelo: "haiku" ou "sonnet"
            tokens_input: Tokens de entrada
            tokens_output: Tokens de saída

        Returns:
            Custo total em USD
        """
        precos = {
            "haiku": {"input": 0.25, "output": 1.25},
            "sonnet": {"input": 3.0, "output": 15.0}
        }

        preco = precos[modelo]
        custo = (
            (tokens_input / 1_000_000) * preco["input"] +
            (tokens_output / 1_000_000) * preco["output"]
        )

        return custo

    def get_estatisticas(self) -> Dict:
        """
        Retorna estatísticas da última extração.

        Returns:
            Dict com métricas:
            {
                "modelo": "haiku" ou "sonnet",
                "tokens_input": int,
                "tokens_output": int,
                "tokens_total": int,
                "custo_usd": float
            }
        """
        return {
            "modelo": self.last_model_used,
            "tokens_input": self.last_tokens_input,
            "tokens_output": self.last_tokens_output,
            "tokens_total": self.last_tokens_input + self.last_tokens_output,
            "custo_usd": self.last_cost_usd
        }


def main():
    """
    Função principal para testar o extrator via CLI.

    Uso:
        python ai_extractor.py texto.md
        python ai_extractor.py texto.md --sonnet
    """
    import sys
    import argparse

    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    parser = argparse.ArgumentParser(description='AI Extractor - Extração de Dados')
    parser.add_argument('input', help='Arquivo .md com texto preparado')
    parser.add_argument('--sonnet', action='store_true', help='Forçar uso de Sonnet')
    parser.add_argument('--output', '-o', help='Salvar JSON em arquivo')
    parser.add_argument('--verbose', '-v', action='store_true', help='Modo verbose')

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        # Ler arquivo
        print(f"\n{'='*70}")
        print(f"Extraindo dados de: {args.input}")
        print(f"{'='*70}\n")

        with open(args.input, 'r', encoding='utf-8') as f:
            texto = f.read()

        # Extrair
        extractor = AIExtractor(force_sonnet=args.sonnet)
        resultado = extractor.extrair(texto)

        # Exibir resultado
        print("✓ Extração concluída!\n")
        print("Dados extraídos:")
        print(json.dumps(resultado, indent=2, ensure_ascii=False))

        # Estatísticas
        stats = extractor.get_estatisticas()
        print(f"\n{'='*70}")
        print("Estatísticas:")
        print(f"  Modelo usado:    {stats['modelo'].upper()}")
        print(f"  Tokens input:    {stats['tokens_input']:,}")
        print(f"  Tokens output:   {stats['tokens_output']:,}")
        print(f"  Tokens total:    {stats['tokens_total']:,}")
        print(f"  Custo estimado:  ${stats['custo_usd']:.4f}")
        print(f"{'='*70}\n")

        # Salvar se solicitado
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(resultado, f, indent=2, ensure_ascii=False)
            print(f"✓ Resultado salvo em: {args.output}\n")

    except FileNotFoundError:
        print(f"✗ Erro: Arquivo não encontrado: {args.input}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Erro: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
