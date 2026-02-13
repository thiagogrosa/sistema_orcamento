"""
Testes de integridade para os dados da planilha HVAC.

Verifica:
- Estrutura das tuplas (campos obrigatórios)
- Unicidade de códigos
- Tipos de dados corretos
- Referências válidas nas composições
"""
import pytest
import sys
from pathlib import Path
from datetime import datetime

# Adicionar diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dados import MATERIAIS, MAO_DE_OBRA, FERRAMENTAS, EQUIPAMENTOS, COMPOSICOES


class TestMateriaisStructure:
    """Testes para estrutura de MATERIAIS."""

    def test_materiais_not_empty(self):
        """Lista de materiais não deve estar vazia."""
        assert len(MATERIAIS) > 0

    def test_materiais_tuple_length(self):
        """Cada material deve ter 7 campos."""
        for i, mat in enumerate(MATERIAIS):
            assert len(mat) == 7, f"Material índice {i} tem {len(mat)} campos, esperado 7"

    def test_materiais_codigo_format(self):
        """Códigos devem seguir padrão (não vazio, sem espaços)."""
        for mat in MATERIAIS:
            codigo = mat[0]
            assert codigo, f"Código vazio encontrado"
            assert ' ' not in codigo, f"Código com espaço: {codigo}"
            assert codigo == codigo.upper(), f"Código não está em maiúsculas: {codigo}"

    def test_materiais_preco_positive(self):
        """Preços devem ser positivos."""
        for mat in MATERIAIS:
            preco = mat[4]
            assert isinstance(preco, (int, float)), f"Preço não numérico: {mat[0]}"
            assert preco > 0, f"Preço não positivo: {mat[0]} = {preco}"

    def test_materiais_unidade_valid(self):
        """Unidades devem ser válidas."""
        unidades_validas = {'UN', 'M', 'KG', 'PAR', 'JG', 'SC', 'KT'}
        for mat in MATERIAIS:
            unidade = mat[3]
            assert unidade in unidades_validas, f"Unidade inválida: {mat[0]} = {unidade}"

    def test_materiais_codigo_unique(self):
        """Códigos devem ser únicos."""
        codigos = [mat[0] for mat in MATERIAIS]
        assert len(codigos) == len(set(codigos)), "Códigos duplicados em MATERIAIS"

    def test_materiais_validade_dias(self):
        """Validade em dias deve ser positiva."""
        for mat in MATERIAIS:
            validade = mat[6]
            assert isinstance(validade, int), f"Validade não é inteiro: {mat[0]}"
            assert validade > 0, f"Validade não positiva: {mat[0]} = {validade}"


class TestMaoDeObraStructure:
    """Testes para estrutura de MAO_DE_OBRA."""

    def test_mao_de_obra_not_empty(self):
        """Lista de mão de obra não deve estar vazia."""
        assert len(MAO_DE_OBRA) > 0

    def test_mao_de_obra_codigo_prefix(self):
        """Códigos devem começar com MO_."""
        for mo in MAO_DE_OBRA:
            codigo = mo[0]
            assert codigo.startswith('MO_'), f"Código não começa com MO_: {codigo}"

    def test_mao_de_obra_codigo_unique(self):
        """Códigos devem ser únicos."""
        codigos = [mo[0] for mo in MAO_DE_OBRA]
        assert len(codigos) == len(set(codigos)), "Códigos duplicados em MAO_DE_OBRA"


class TestFerramentasStructure:
    """Testes para estrutura de FERRAMENTAS."""

    def test_ferramentas_not_empty(self):
        """Lista de ferramentas não deve estar vazia."""
        assert len(FERRAMENTAS) > 0

    def test_ferramentas_codigo_prefix(self):
        """Códigos devem começar com FER_."""
        for fer in FERRAMENTAS:
            codigo = fer[0]
            assert codigo.startswith('FER_'), f"Código não começa com FER_: {codigo}"

    def test_ferramentas_vida_util_positive(self):
        """Vida útil deve ser positiva."""
        for fer in FERRAMENTAS:
            # Estrutura: (codigo, categoria, descricao, valor_aquisicao, vida_util, ...)
            vida_util = fer[4]
            assert vida_util > 0, f"Vida útil não positiva: {fer[0]} = {vida_util}"


class TestEquipamentosStructure:
    """Testes para estrutura de EQUIPAMENTOS."""

    def test_equipamentos_not_empty(self):
        """Lista de equipamentos não deve estar vazia."""
        assert len(EQUIPAMENTOS) > 0

    def test_equipamentos_codigo_prefix(self):
        """Códigos devem começar com EQP_."""
        for eqp in EQUIPAMENTOS:
            codigo = eqp[0]
            assert codigo.startswith('EQP_'), f"Código não começa com EQP_: {codigo}"


class TestComposicoesStructure:
    """Testes para estrutura de COMPOSIÇÕES."""

    def test_composicoes_not_empty(self):
        """Lista de composições não deve estar vazia."""
        assert len(COMPOSICOES) > 0

    def test_composicoes_codigo_prefix(self):
        """Códigos devem começar com COMP_."""
        for comp in COMPOSICOES:
            codigo = comp['codigo']
            assert codigo.startswith('COMP_'), f"Código não começa com COMP_: {codigo}"

    def test_composicoes_codigo_unique(self):
        """Códigos devem ser únicos."""
        codigos = [comp['codigo'] for comp in COMPOSICOES]
        assert len(codigos) == len(set(codigos)), "Códigos duplicados em COMPOSICOES"

    def test_composicoes_has_required_fields(self):
        """Cada composição deve ter campos obrigatórios."""
        required = ['codigo', 'descricao', 'itens']
        for comp in COMPOSICOES:
            for field in required:
                assert field in comp, f"Campo '{field}' faltando em {comp.get('codigo', 'DESCONHECIDO')}"

    def test_composicoes_itens_not_empty(self):
        """Cada composição deve ter pelo menos um item."""
        for comp in COMPOSICOES:
            assert len(comp['itens']) > 0, f"Composição sem itens: {comp['codigo']}"

    def test_composicoes_itens_valid_tipo(self):
        """Tipos de item devem ser válidos (MAT, MO, FER, EQP)."""
        tipos_validos = {'MAT', 'MO', 'FER', 'EQP'}
        for comp in COMPOSICOES:
            for item in comp['itens']:
                tipo = item[0]
                assert tipo in tipos_validos, f"Tipo inválido em {comp['codigo']}: {tipo}"


class TestComposicoesReferences:
    """Testes para validar referências nas composições."""

    @pytest.fixture
    def all_codes(self):
        """Fixture com todos os códigos disponíveis por tipo."""
        return {
            'MAT': {mat[0] for mat in MATERIAIS},
            'MO': {mo[0] for mo in MAO_DE_OBRA},
            'FER': {fer[0] for fer in FERRAMENTAS},
            'EQP': {eqp[0] for eqp in EQUIPAMENTOS},
        }

    def test_composicoes_references_exist(self, all_codes):
        """Todos os códigos referenciados nas composições devem existir."""
        for comp in COMPOSICOES:
            for item in comp['itens']:
                tipo, codigo, _, _ = item
                available = all_codes.get(tipo, set())
                assert codigo in available, (
                    f"Código inexistente em {comp['codigo']}: "
                    f"{tipo}:{codigo} não encontrado"
                )

    def test_composicoes_quantities_valid(self):
        """Quantidades nas composições devem ser não-negativas."""
        for comp in COMPOSICOES:
            for item in comp['itens']:
                _, codigo, qtd_base, qtd_var = item
                assert qtd_base >= 0, f"Qtd base negativa em {comp['codigo']}: {codigo}"
                assert qtd_var >= 0, f"Qtd var negativa em {comp['codigo']}: {codigo}"

    def test_composicoes_has_some_quantity(self):
        """Cada item deve ter pelo menos uma quantidade definida."""
        for comp in COMPOSICOES:
            for item in comp['itens']:
                _, codigo, qtd_base, qtd_var = item
                assert qtd_base > 0 or qtd_var > 0, (
                    f"Item sem quantidade em {comp['codigo']}: {codigo}"
                )


class TestDataConsistency:
    """Testes de consistência geral dos dados."""

    def test_no_negative_prices(self):
        """Nenhum preço deve ser negativo em qualquer catálogo."""
        all_items = list(MATERIAIS) + list(MAO_DE_OBRA)

        for item in all_items:
            # Preço geralmente na posição 4
            if len(item) > 4 and isinstance(item[4], (int, float)):
                assert item[4] >= 0, f"Preço negativo: {item[0]} = {item[4]}"

    def test_descriptions_not_empty(self):
        """Descrições não devem estar vazias."""
        all_items = list(MATERIAIS) + list(MAO_DE_OBRA) + list(FERRAMENTAS) + list(EQUIPAMENTOS)

        for item in all_items:
            descricao = item[2]
            assert descricao and descricao.strip(), f"Descrição vazia: {item[0]}"

    def test_categories_not_empty(self):
        """Categorias não devem estar vazias."""
        all_items = list(MATERIAIS) + list(MAO_DE_OBRA) + list(FERRAMENTAS) + list(EQUIPAMENTOS)

        for item in all_items:
            categoria = item[1]
            assert categoria and categoria.strip(), f"Categoria vazia: {item[0]}"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
