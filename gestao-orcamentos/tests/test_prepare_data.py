#!/usr/bin/env python3
"""
Testes para DataPreparer

Para rodar:
    pytest tests/test_prepare_data.py -v
"""

import pytest
import os
import tempfile
from pathlib import Path
from src.prepare_data import DataPreparer, DataPreparerError


class TestDataPreparerLimparHTML:
    """Testes de limpeza de HTML."""

    def setup_method(self):
        """Setup para cada teste."""
        self.preparer = DataPreparer()

    def test_limpar_html_simples(self):
        """Deve remover tags HTML simples."""
        html = "<p>Olá <b>mundo</b>!</p>"
        result = self.preparer.limpar_html(html)
        assert "Olá" in result
        assert "mundo" in result
        assert "<p>" not in result
        assert "<b>" not in result

    def test_limpar_html_com_scripts(self):
        """Deve remover scripts e styles."""
        html = """
        <html>
            <script>alert('test')</script>
            <style>.test { color: red; }</style>
            <p>Conteúdo válido</p>
        </html>
        """
        result = self.preparer.limpar_html(html)
        assert "Conteúdo válido" in result
        assert "alert" not in result
        assert "color: red" not in result

    def test_limpar_html_com_links(self):
        """Deve preservar links em markdown."""
        html = '<p>Visite <a href="https://exemplo.com">nosso site</a></p>'
        result = self.preparer.limpar_html(html)
        assert "nosso site" in result
        # html2text converte para markdown: [texto](url)


class TestDataPreparerRemoverAssinatura:
    """Testes de remoção de assinatura."""

    def setup_method(self):
        """Setup para cada teste."""
        self.preparer = DataPreparer()

    def test_remover_assinatura_atenciosamente(self):
        """Deve remover assinatura com 'Atenciosamente'."""
        texto = """
Prezados,

Gostaria de solicitar um orçamento.

Atenciosamente,
João Silva
Gerente Comercial
(11) 98765-4321
        """
        result = self.preparer.remover_assinatura(texto)
        assert "orçamento" in result
        assert "Atenciosamente" not in result
        assert "João Silva" not in result

    def test_remover_assinatura_att(self):
        """Deve remover assinatura com 'Att'."""
        texto = """
Conteúdo do email.

Att,
Maria
        """
        result = self.preparer.remover_assinatura(texto)
        assert "Conteúdo" in result
        assert "Att," not in result

    def test_remover_assinatura_separador(self):
        """Deve remover assinatura com separador '--'."""
        texto = """
Mensagem importante.

--
João da Silva
Empresa XYZ
        """
        result = self.preparer.remover_assinatura(texto)
        assert "Mensagem" in result
        assert "Empresa XYZ" not in result

    def test_sem_assinatura(self):
        """Deve retornar texto inalterado se não tem assinatura."""
        texto = "Texto simples sem assinatura"
        result = self.preparer.remover_assinatura(texto)
        assert result == texto


class TestDataPreparerRemoverThread:
    """Testes de remoção de threads antigas."""

    def setup_method(self):
        """Setup para cada teste."""
        self.preparer = DataPreparer()

    def test_remover_thread_em_data(self):
        """Deve remover thread iniciada com 'Em DD/MM/AAAA'."""
        texto = """
Esta é a resposta mais recente.

Em 25/01/2026, João escreveu:
> Mensagem antiga
> Mais conteúdo antigo
        """
        result = self.preparer.remover_thread_antiga(texto)
        assert "resposta mais recente" in result
        assert "Em 25/01/2026" not in result
        assert "Mensagem antiga" not in result

    def test_remover_linhas_citadas(self):
        """Deve remover linhas começando com >."""
        texto = """
Conteúdo novo.

> Texto citado
> Mais citação
        """
        result = self.preparer.remover_thread_antiga(texto)
        assert "Conteúdo novo" in result
        assert "> Texto citado" not in result


class TestDataPreparerExtrairMetadados:
    """Testes de extração de metadados."""

    def setup_method(self):
        """Setup para cada teste."""
        self.preparer = DataPreparer()

    def test_extrair_cnpj(self):
        """Deve extrair e normalizar CNPJ."""
        texto = "CNPJ: 12.345.678/0001-90"
        result = self.preparer.extrair_metadados(texto)
        assert len(result['cnpj']) == 1
        assert "12.345.678/0001-90" in result['cnpj']

    def test_extrair_cnpj_sem_formatacao(self):
        """Deve extrair CNPJ mesmo sem formatação."""
        texto = "CNPJ 12345678000190"
        result = self.preparer.extrair_metadados(texto)
        assert len(result['cnpj']) == 1
        # Deve normalizar para formato padrão
        assert "12.345.678/0001-90" in result['cnpj']

    def test_extrair_telefone(self):
        """Deve extrair e normalizar telefones."""
        texto = "Telefone: (11) 98765-4321 ou 11987654321"
        result = self.preparer.extrair_metadados(texto)
        assert len(result['telefones']) >= 1
        # Pelo menos um deve estar normalizado
        assert any("(11)" in tel for tel in result['telefones'])

    def test_extrair_email(self):
        """Deve extrair emails."""
        texto = "Entre em contato: joao@empresa.com.br"
        result = self.preparer.extrair_metadados(texto)
        assert "joao@empresa.com.br" in result['emails']

    def test_extrair_cep(self):
        """Deve extrair e normalizar CEP."""
        texto = "CEP: 01234-567 ou 01234567"
        result = self.preparer.extrair_metadados(texto)
        assert len(result['ceps']) >= 1
        assert "01234-567" in result['ceps']

    def test_extrair_valor_monetario(self):
        """Deve extrair valores em reais."""
        texto = "O valor é R$ 15.000,00"
        result = self.preparer.extrair_metadados(texto)
        assert "R$ 15.000,00" in result['valores']

    def test_extrair_multiplos_dados(self):
        """Deve extrair múltiplos tipos de dados."""
        texto = """
        Empresa: ACME LTDA
        CNPJ: 12.345.678/0001-90
        Contato: João Silva
        Telefone: (11) 98765-4321
        Email: joao@acme.com.br
        CEP: 01234-567
        Valor: R$ 5.000,00
        """
        result = self.preparer.extrair_metadados(texto)

        assert len(result['cnpj']) > 0
        assert len(result['telefones']) > 0
        assert len(result['emails']) > 0
        assert len(result['ceps']) > 0
        assert len(result['valores']) > 0


class TestDataPreparerPrepararEmail:
    """Testes do pipeline completo."""

    def setup_method(self):
        """Setup para cada teste."""
        self.preparer = DataPreparer()
        self.temp_dir = tempfile.mkdtemp()

    def teardown_method(self):
        """Cleanup após cada teste."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_preparar_email_txt(self):
        """Deve processar arquivo .txt."""
        # Criar arquivo de teste
        input_file = os.path.join(self.temp_dir, "test.txt")
        with open(input_file, 'w', encoding='utf-8') as f:
            f.write("""
Prezados,

Gostaria de orçamento para instalação.

CNPJ: 12.345.678/0001-90
Telefone: (11) 98765-4321

Atenciosamente,
João Silva
            """)

        # Processar
        result = self.preparer.preparar_email(input_file)

        # Verificar resultado
        assert result['texto_limpo'] is not None
        assert len(result['metadados']['cnpj']) > 0
        assert len(result['metadados']['telefones']) > 0
        assert result['tokens_estimados_depois'] < result['tokens_estimados_antes']
        assert os.path.exists(result['output_file'])

    def test_preparar_email_html(self):
        """Deve processar arquivo .html."""
        input_file = os.path.join(self.temp_dir, "test.html")
        with open(input_file, 'w', encoding='utf-8') as f:
            f.write("""
<html>
    <body>
        <p>Solicito <b>orçamento</b> urgente.</p>
        <p>Telefone: (11) 98765-4321</p>
    </body>
</html>
            """)

        result = self.preparer.preparar_email(input_file)

        assert "orçamento" in result['texto_limpo']
        assert "urgente" in result['texto_limpo']
        assert len(result['metadados']['telefones']) > 0

    def test_preparar_email_reducao_tokens(self):
        """Deve reduzir número de tokens."""
        input_file = os.path.join(self.temp_dir, "test.txt")

        # Criar email com muito ruído
        with open(input_file, 'w', encoding='utf-8') as f:
            f.write("""
Conteúdo importante.

Atenciosamente,
João Silva
Gerente
Empresa XYZ
Tel: (11) 98765-4321
Email: joao@empresa.com
Site: www.empresa.com

AVISO LEGAL: Este email contém informações confidenciais...
            """)

        result = self.preparer.preparar_email(input_file)

        # Deve ter reduzido tokens
        assert result['reducao_percentual'] > 0

    def test_preparar_email_output_customizado(self):
        """Deve salvar em caminho customizado."""
        input_file = os.path.join(self.temp_dir, "test.txt")
        output_file = os.path.join(self.temp_dir, "output.md")

        with open(input_file, 'w', encoding='utf-8') as f:
            f.write("Teste")

        result = self.preparer.preparar_email(input_file, output_file)

        assert result['output_file'] == output_file
        assert os.path.exists(output_file)


class TestDataPreparerPrepararPasta:
    """Testes de processamento de pasta."""

    def setup_method(self):
        """Setup para cada teste."""
        self.preparer = DataPreparer()
        self.temp_dir = tempfile.mkdtemp()

    def teardown_method(self):
        """Cleanup após cada teste."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_preparar_pasta_multiplos_arquivos(self):
        """Deve processar múltiplos arquivos e consolidar."""
        # Criar vários arquivos
        for i in range(3):
            with open(os.path.join(self.temp_dir, f"email_{i}.txt"), 'w') as f:
                f.write(f"Email {i}\nTelefone: (11) 9876{i}-432{i}\n")

        result = self.preparer.preparar_pasta(self.temp_dir)

        assert result['arquivos_processados'] == 3
        assert "Email 0" in result['texto_limpo']
        assert "Email 2" in result['texto_limpo']
        assert len(result['metadados']['telefones']) == 3  # 3 telefones únicos

    def test_preparar_pasta_vazia(self):
        """Deve lançar erro se pasta vazia."""
        with pytest.raises(DataPreparerError):
            self.preparer.preparar_pasta(self.temp_dir)

    def test_preparar_pasta_metadados_consolidados(self):
        """Deve consolidar metadados sem duplicatas."""
        # Criar arquivos com dados repetidos
        for i in range(2):
            with open(os.path.join(self.temp_dir, f"email_{i}.txt"), 'w') as f:
                f.write("CNPJ: 12.345.678/0001-90\n")  # Mesmo CNPJ em ambos

        result = self.preparer.preparar_pasta(self.temp_dir)

        # Deve ter apenas 1 CNPJ (sem duplicatas)
        assert len(result['metadados']['cnpj']) == 1


class TestDataPreparerEstimarTokens:
    """Testes de estimativa de tokens."""

    def setup_method(self):
        """Setup para cada teste."""
        self.preparer = DataPreparer()

    def test_estimar_tokens_texto_curto(self):
        """Deve estimar tokens de texto curto."""
        texto = "Teste de tokens"
        tokens = self.preparer._estimar_tokens(texto)
        # "Teste de tokens" = 15 chars / 4 = ~3-4 tokens
        assert tokens > 0
        assert tokens < 10

    def test_estimar_tokens_texto_longo(self):
        """Deve estimar tokens de texto longo."""
        texto = "palavra " * 1000  # 1000 palavras
        tokens = self.preparer._estimar_tokens(texto)
        assert tokens > 1000  # Pelo menos 1 token por palavra


# ===== Testes de Integração =====

@pytest.mark.integration
class TestDataPreparerIntegration:
    """
    Testes de integração com dados reais.

    Para rodar: pytest tests/test_prepare_data.py -v -m integration
    """

    def setup_method(self):
        """Setup para testes de integração."""
        self.preparer = DataPreparer()

    def test_processar_email_real_exemplo(self):
        """Teste com exemplo de email real (anonimizado)."""
        email_exemplo = """
De: João Silva <joao.silva@empresaxyz.com.br>
Para: orcamentos2@armant.com.br
Assunto: Orçamento - Climatização Sala Reuniões
Data: 25/01/2026 14:30

Prezados,

Gostaria de solicitar um orçamento para instalação de sistema de
climatização em nossa sala de reuniões.

Dados da Empresa:
- Razão Social: Empresa XYZ Tecnologia LTDA
- CNPJ: 12.345.678/0001-90
- Endereço: Rua Exemplo, 123 - Centro - São Paulo/SP
- CEP: 01234-567

Especificações:
- Área: aproximadamente 50m²
- Pé direito: 2.80m
- Necessidade: Split 18.000 BTUs
- Prazo desejado: até 15/02/2026

Contato:
João Silva - Gerente de Facilities
Telefone: (11) 98765-4321
Email: joao.silva@empresaxyz.com.br

Aguardo retorno.

Atenciosamente,
João Silva
Gerente de Facilities
Empresa XYZ Tecnologia LTDA
Tel: (11) 98765-4321 | Cel: (11) 99999-8888
www.empresaxyz.com.br

--
AVISO LEGAL: Esta mensagem contém informações confidenciais...
        """

        # Salvar em arquivo temporário
        import tempfile
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.txt',
            delete=False,
            encoding='utf-8'
        ) as f:
            f.write(email_exemplo)
            temp_file = f.name

        try:
            # Processar
            result = self.preparer.preparar_email(temp_file)

            # Verificações
            assert result is not None

            # Deve conter informações importantes
            assert "orçamento" in result['texto_limpo'].lower()
            assert "climatização" in result['texto_limpo'].lower()

            # Deve ter removido assinatura e aviso legal
            assert "AVISO LEGAL" not in result['texto_limpo']

            # Deve ter extraído metadados
            assert len(result['metadados']['cnpj']) > 0
            assert "12.345.678/0001-90" in result['metadados']['cnpj']

            assert len(result['metadados']['telefones']) > 0
            assert len(result['metadados']['emails']) > 0
            assert len(result['metadados']['ceps']) > 0

            # Deve ter reduzido tokens
            assert result['reducao_percentual'] > 20  # Pelo menos 20% de redução

            print(f"\nResultado do teste de integração:")
            print(f"  Tokens antes:  {result['tokens_estimados_antes']}")
            print(f"  Tokens depois: {result['tokens_estimados_depois']}")
            print(f"  Redução:       {result['reducao_percentual']:.1f}%")
            print(f"\n  Metadados extraídos:")
            for tipo, valores in result['metadados'].items():
                if valores:
                    print(f"    {tipo}: {valores}")

        finally:
            # Limpar arquivo temporário
            os.unlink(temp_file)
            if os.path.exists(result['output_file']):
                os.unlink(result['output_file'])
